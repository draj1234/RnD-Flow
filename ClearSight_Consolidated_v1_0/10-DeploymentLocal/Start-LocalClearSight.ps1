# Start-LocalClearSight.ps1
param(
  [switch]$Rebuild = $false
)

Write-Host "Starting ClearSight (local)..." -ForegroundColor Cyan
Push-Location $PSScriptRoot

$compose = ".\CS-Compose-LOCAL-v1_0.yml"
if ($Rebuild) {
  docker compose -f $compose up --build -d
} else {
  docker compose -f $compose up -d
}

docker compose -f $compose ps
Write-Host "Health check: GET http://localhost:8080/health" -ForegroundColor Green
Pop-Location
