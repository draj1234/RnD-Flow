# CS-AI-08-DevOps-and-Local-Deployment-Pack-v1_0.md

Version: v1.1 | Date: 2025-08-10

Purpose

- Provide reproducible local and stack deployments with monitoring and backups.

Sources

- 07-DevOps/CS-Compose-DockerStack-v1_0.yml
- 07-DevOps/CS-Nginx-Config-v1_0.conf
- 10-DeploymentLocal/CS-Deploy-LocalWin11-Guide-v1_0.md
- 10-DeploymentLocal/CS-Compose-LOCAL-v1_0.yml
- 10-DeploymentLocal/CS-Env-LOCAL-v1_0.example
- 10-DeploymentLocal/CS-Deploy-SmokeChecklist-v1_0.md
- 10-DeploymentLocal/Start-LocalClearSight.ps1
- 07-DevOps/CS-Backup-RetentionPolicy-v1_0.md
- 07-DevOps/CS-Monitoring-Setup-v1_0.md

Local Run (Windows 11)

- Use Env-LOCAL example; run Start-LocalClearSight.ps1
- Execute SmokeChecklist for verification.

Stack Run

- Apply DockerStack compose and Nginx config; set secrets/env.

CI/CD & Security (Minimal)

- Establish early pipeline (build, test, lint, contract tests)
- Secrets via env/secret manager; image scanning and SBOM generation

Ops

- Monitoring dashboards; log collection; backup/retention timelines.

LLM Model Benchmark (Ollama)

- Script: scripts/ollama-benchmark.ps1 (no hardcoded models)
- Usage examples:
  - powershell -ExecutionPolicy Bypass -File scripts/ollama-benchmark.ps1 -BaseUrl http://192.168.1.13:11434
  - powershell -ExecutionPolicy Bypass -File scripts/ollama-benchmark.ps1 -BaseUrl $env:OLLAMA_BASE_URL -Models "llama3.1:latest","qwen3-coder:30b"
- Output: FOR_AI-AGENT/ollama_benchmark_result.json with recommended model and scores
- Policy: choose recommended model at runtime via env var OLLAMA_MODEL, fallback to benchmark recommendation

Exit Criteria

- Services healthy; smoke tests pass; dashboards populated; basic pipeline green.


Markdown Style & Linting Guidelines (for future edits)

- See: CS-AI-Common-Markdown-Guidelines-v1_0.md
