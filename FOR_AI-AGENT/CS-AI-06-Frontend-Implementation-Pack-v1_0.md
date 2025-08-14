# CS-AI-06-Frontend-Implementation-Pack-v1_0.md

Version: v1.1 | Date: 2025-08-10

Purpose

- Build the role-based web UI and integrate with API.

Sources

- 05-FrontendDev/CS-Frontend-AppScaffold-v1_0.zip
- 05-FrontendDev/CS-Frontend-IntegrationTests-v1_0.md
- 05-FrontendDev/CS-Frontend-ScannerPrinterConfig-v1_0.md

Project Structure (from zip)

- Summarize app folders (src, pages/routes, components, services) after extraction.

Source Structure Manifest (zip listing)

- src/components/Dashboard.jsx
- src/components/BoardTracker.jsx
- src/components/SKUOnboarding.jsx
- src/components/ERPSyncView.jsx
- src/App.jsx
- package.json
- vite.config.js

Key Tasks

- Implement routes/screens per UI pack.
- Use generated typed API client from canonical OpenAPI; develop on mock server initially.
- Bind to API endpoints; handle auth with role claims.
- Implement integration tests and device config.
- Resolve Ollama model at runtime (no hardcoding):
  - powershell -ExecutionPolicy Bypass -File scripts/resolve-ollama-model.ps1 | Tee-Object -Variable OLLAMA_MODEL
  - $env:OLLAMA_MODEL=$OLLAMA_MODEL
- Re-benchmark with custom weights (optional):
  - powershell -ExecutionPolicy Bypass -File scripts/ollama-benchmark.ps1 -AccuracyWeight 0.7 -ReliabilityWeight 0.2 -SpeedWeight 0.1

Readiness Checklist

- [ ] Core screens functional
- [ ] API calls & error handling verified (mock + real)
- [ ] Integration tests pass locally; basic a11y checks

Exit Criteria

- Frontend passes QA smoke and integration tests.


Markdown Style & Linting Guidelines (for future edits)

- See: CS-AI-Common-Markdown-Guidelines-v1_0.md
