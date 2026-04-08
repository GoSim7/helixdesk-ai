# Control API

Run locally:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e .[dev]
.\.venv\Scripts\python -m uvicorn app.main:app --reload
```

Default local database:

- `sqlite:///./data/app.db`

Key endpoints:

- `GET /api/admin/system-settings`
- `POST /api/runtime/route-message`
- `POST /api/runtime/chatwoot/webhook`
- `GET /api/runtime/health`

Integration notes:

- `POST /api/runtime/chatwoot/webhook` now verifies `X-Chatwoot-Timestamp` and `X-Chatwoot-Signature` when `CHATWOOT_MOCK_MODE=false`.
- Chatwoot reply delivery uses `POST /api/v1/accounts/{account_id}/conversations/{conversation_id}/messages`.
- AstrBot integration is currently implemented as a configurable bridge contract at `ASTRBOT_CHAT_PATH`.
- In local development, both external adapters default to mock mode.
