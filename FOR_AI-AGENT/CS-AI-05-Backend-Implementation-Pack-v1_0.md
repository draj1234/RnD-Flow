# CS-AI-05-Backend-Implementation-Pack-v1_0.md

Version: v1.1 | Date: 2025-08-10

Purpose

- Stand up API service, database migrations, and basic test coverage.

Sources

- 04-BackendDev/CS-Backend-Service-v1_0.zip
- 04-BackendDev/CS-Backend-PostmanCollection-v1_0.json
- 04-BackendDev/CS-Backend-DeploymentGuide-v1_0.md

Project Structure (from zip)

- Summarize folders (src, routes, models, migrations, tests) after extraction.

Source Structure Manifest (zip listing)

- CS-Backend-Service-v1_0/package.json
- CS-Backend-Service-v1_0/.env.example
- CS-Backend-Service-v1_0/Dockerfile
- CS-Backend-Service-v1_0/docker-compose.yml
- CS-Backend-Service-v1_0/README.md
- CS-Backend-Service-v1_0/src/index.js
- CS-Backend-Service-v1_0/src/routes/auth.js
- CS-Backend-Service-v1_0/src/routes/boards.js
- CS-Backend-Service-v1_0/src/routes/stages.js
- CS-Backend-Service-v1_0/src/routes/stageEvents.js
- CS-Backend-Service-v1_0/src/routes/sku.js
- CS-Backend-Service-v1_0/src/routes/erpSync.js
- CS-Backend-Service-v1_0/src/routes/dashboard.js
- CS-Backend-Service-v1_0/src/config/db.js
- CS-Backend-Service-v1_0/migrations/001_init_placeholder.sql

Key Tasks

- Implement DB migrations and seeds matching DDL.
- Implement endpoints per API spec with auth/roles.
- Run Postman collection against local stack.
- Resolve Ollama model at runtime (no hardcoding):
  - powershell -ExecutionPolicy Bypass -File scripts/resolve-ollama-model.ps1 | Tee-Object -Variable OLLAMA_MODEL
  - $env:OLLAMA_MODEL=$OLLAMA_MODEL
- Re-benchmark with custom weights (optional):
  - powershell -ExecutionPolicy Bypass -File scripts/ollama-benchmark.ps1 -AccuracyWeight 0.7 -ReliabilityWeight 0.2 -SpeedWeight 0.1

Quality & Observability (Minimal)
- Contract tests vs. OpenAPI; unit + integration tests with coverage target
- Error contract, structured logs with correlation IDs; basic traces/metrics
- Security: authZ checks, secrets from env, audit log for critical actions

Readiness Checklist

- [ ] All endpoints implemented
- [ ] 200/4xx/5xx handling validated
- [ ] Seeds load and basic data present
- [ ] Logs/metrics visible; contract tests passing

Exit Criteria

- Backend passes Postman suite and QA smoke.

Markdown Style & Linting Guidelines (for future edits)

- See: CS-AI-Common-Markdown-Guidelines-v1_0.md
