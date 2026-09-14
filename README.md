# Research Manager

Phase 1 backend-only Research Manager using FastAPI, LangGraph, Pydantic v2, SQLite, and
pytest.

This phase proves orchestration:

```text
START -> planner -> executor -> evidence_analyst -> critic -> synthesizer -> supervisor
```

The executor uses mocked search results. No frontend is included.

## Run

```powershell
cd C:\workspace\research_manager
uv --system-certs sync --group dev
uv run uvicorn app.main:app --reload --port 8020
```

## Test

```powershell
uv run pytest
```

