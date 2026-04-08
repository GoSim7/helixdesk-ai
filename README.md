# HelixDesk AI

Current implementation focus:

- `apps/control-api`: FastAPI backend with SQLite/PostgreSQL-compatible persistence

Next steps:

- connect Chatwoot and AstrBot to real runtime endpoints
- scaffold admin frontend

Quick start:

```powershell
.\scripts\dev.ps1
```

Current backend status:

- persistent settings, presets, conversation state, and audit logs
- Chatwoot webhook verification and reply-delivery skeleton
- AstrBot bridge adapter with mock mode for local development
- automated smoke tests for routing, handover, and webhook validation

Project name:

- product name: `HelixDesk AI`
- suggested repository slug: `helixdesk-ai`
