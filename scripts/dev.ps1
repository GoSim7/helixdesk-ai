$ErrorActionPreference = "Stop"

Set-Location "$PSScriptRoot\..\apps\control-api"

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

.\.venv\Scripts\python -m pip install -e .[dev]
.\.venv\Scripts\python -m uvicorn app.main:app --reload
