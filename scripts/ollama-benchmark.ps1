param(
  [string]$BaseUrl = $env:OLLAMA_BASE_URL,
  [string[]]$Models,
  [string]$OutJson = "FOR_AI-AGENT/ollama_benchmark_result.json",
  [double]$AccuracyWeight = 0.6,
  [double]$ReliabilityWeight = 0.3,
  [double]$SpeedWeight = 0.1,
  [int]$SpeedCapMs = 5000
)

if (-not $BaseUrl -or $BaseUrl.Trim() -eq "") {
  $BaseUrl = "http://192.168.1.13:11434"
}

function Invoke-OllamaGenerate {
  param(
    [string]$Model,
    [string]$Prompt,
    [int]$TimeoutSec = 60
  )
  $uri = "$BaseUrl/api/generate"
  $body = @{ model = $Model; prompt = $Prompt; stream = $false } | ConvertTo-Json -Depth 5
  try {
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $resp = Invoke-RestMethod -Uri $uri -Method Post -ContentType 'application/json' -Body $body -TimeoutSec $TimeoutSec
    $sw.Stop()
    return @{ ok=$true; ms=[int]$sw.ElapsedMilliseconds; text=([string]$resp.response) }
  } catch {
    return @{ ok=$false; ms=$null; text=""; error=$_.Exception.Message }
  }
}

function Get-InstalledModels {
  try {
    $tags = Invoke-RestMethod -Uri "$BaseUrl/api/tags" -TimeoutSec 10
    if ($null -ne $tags.models) {
      return ($tags.models | ForEach-Object { $_.name })
    }
  } catch {}
  return @()
}

# Define a small, relevant benchmark set with simple scoring
$tests = @(
  @{ name="math_simple"; prompt="What is 37*23? Provide only the number."; expect=@("851"); type="equals" },
  @{ name="routes_from_list"; prompt="From this list of files: CS-Backend-Service-v1_0/src/routes/auth.js, boards.js, stages.js, stageEvents.js, sku.js, erpSync.js, dashboard.js; enumerate backend API route names that likely exist. Return a comma-separated list in lowercase."; expect=@("auth","boards","stages","stageevents","sku","erpsync","dashboard"); type="contains" },
  @{ name="ac_list"; prompt="Given acceptance criteria: AC-001 role-based auth, AC-002 scan ingestion, AC-003 board details, AC-004 ERP sync; list them as AC-001..AC-004."; expect=@("AC-001","AC-002","AC-003","AC-004"); type="contains" },
  # Added domain-specific tests
  @{ name="schema_entities"; prompt="From the ClearSight domain, list likely database table names for entities: boards, stations, scans, users, roles. Return a comma-separated lowercase list."; expect=@("boards","stations","scans","users","roles"); type="contains" },
  @{ name="rbac_roles"; prompt="In this system, name three user roles with increasing privilege relevant to manufacturing traceability."; expect=@("operator","floor manager","admin"); type="contains" },
  @{ name="endpoints_inference"; prompt="Infer likely REST endpoint base paths for the backend given files auth.js, boards.js, scans, dashboard.js. Return a comma-separated list of base paths (e.g., /auth, /boards, /scans, /dashboard)."; expect=@("/auth","/boards","/scans","/dashboard"); type="contains" },
  @{ name="erp_idempotency"; prompt="For ERP sync operations, list three reliability mechanisms we should implement."; expect=@("idempotency","retry","backoff"); type="contains" },
  @{ name="device_config"; prompt="Name two device configuration areas the frontend must handle for factory stations."; expect=@("scanner","printer"); type="contains" },
  @{ name="compose_services"; prompt="Name two core services likely to appear in a Docker stack for this app (reverse proxy and database)."; expect=@("nginx","postgres"); type="contains" },
  @{ name="perf_budget"; prompt="Name two performance budget concepts we might track for UI and API latency."; expect=@("p95","latency"); type="contains" }
)

if (-not $Models -or $Models.Count -eq 0) {
  $Models = Get-InstalledModels
}
if (-not $Models -or $Models.Count -eq 0) {
  Write-Error "No models found at $BaseUrl. Start Ollama or set -Models explicitly."
  exit 1
}

$results = @()
foreach ($m in $Models) {
  $okCount = 0; $errCount = 0; $accSum = 0; $times = @();
  foreach ($t in $tests) {
    $res = Invoke-OllamaGenerate -Model $m -Prompt $t.prompt
    if ($res.ok) {
      $times += $res.ms
      $okCount++
      $txt = ($res.text | Out-String).Trim()
      $acc = 0
      if ($t.type -eq "equals") {
        if ($txt -match "^\s*" + [regex]::Escape($t.expect[0]) + "\s*$") { $acc = 1 }
      } else {
        foreach ($kw in $t.expect) {
          if ($txt.ToLower().Contains($kw.ToLower())) { $acc++ }
        }
        $acc = $acc / [double]$t.expect.Count
      }
      $accSum += $acc
    } else {
      $errCount++
    }
  }
  $total = $tests.Count
  $reliability = if ($total -gt 0) { $okCount / [double]$total } else { 0 }
  $accuracy = if ($total -gt 0) { $accSum / [double]$total } else { 0 }
  $avgMs = if ($times.Count -gt 0) { [int]($times | Measure-Object -Average | Select-Object -ExpandProperty Average) } else { $null }
  # Composite score with configurable weights (normalized inverse by SpeedCapMs)
  $speedScore = if ($avgMs -ne $null) { [Math]::Max(0, 1 - [Math]::Min($avgMs,$SpeedCapMs)/[double]$SpeedCapMs) } else { 0 }
  $score = [Math]::Round(($accuracy*$AccuracyWeight + $reliability*$ReliabilityWeight + $speedScore*$SpeedWeight), 4)
  $results += [PSCustomObject]@{
    model=$m; reliability=$reliability; accuracy=$accuracy; avg_ms=$avgMs; score=$score
  }
}

$sorted = $results | Sort-Object -Property @{Expression='score';Descending=$true}, @{Expression='avg_ms';Ascending=$true}
$recommended = $sorted | Select-Object -First 1

Write-Host "Ollama benchmark @ $BaseUrl" -ForegroundColor Cyan
$sorted | Format-Table -AutoSize
Write-Host "Recommended model: $($recommended.model) (score $($recommended.score), avg_ms $($recommended.avg_ms))" -ForegroundColor Green

# Persist JSON report
$report = [PSCustomObject]@{
  base_url = $BaseUrl
  timestamp = (Get-Date).ToString('s')
  tests = $tests
  results = $sorted
  recommended = $recommended.model
}
$dir = Split-Path -Parent $OutJson
if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
$report | ConvertTo-Json -Depth 6 | Out-File -FilePath $OutJson -Encoding UTF8

