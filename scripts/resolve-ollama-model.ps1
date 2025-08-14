param(
  [string]$DefaultModel = "llama3.1:latest",
  [string]$BenchmarkJson = "FOR_AI-AGENT/ollama_benchmark_result.json"
)

# Priority 1: explicit env var override
if ($env:OLLAMA_MODEL -and $env:OLLAMA_MODEL.Trim() -ne "") {
  Write-Output $env:OLLAMA_MODEL
  exit 0
}

# Priority 2: benchmark recommendation
if (Test-Path $BenchmarkJson) {
  try {
    $raw = Get-Content -Raw -Path $BenchmarkJson | ConvertFrom-Json -ErrorAction Stop
    if ($null -ne $raw.recommended -and ($raw.recommended | Out-String).Trim() -ne "") {
      Write-Output $raw.recommended
      exit 0
    }
  } catch {
    # ignore and fall back
  }
}

# Priority 3: static default
Write-Output $DefaultModel

