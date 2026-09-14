from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import timezone
from pathlib import Path
from typing import Iterator

from app.config import get_settings
from app.schemas.research import ResearchState, now_utc


def connect() -> sqlite3.Connection:
    path = Path(get_settings().database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def db() -> Iterator[sqlite3.Connection]:
    conn = connect()
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with db() as conn:
        conn.execute(
            """
            create table if not exists research_states (
                research_id text primary key,
                state_json text not null,
                created_at text not null,
                updated_at text not null
            )
            """
        )


class ResearchStore:
    def save(self, state: ResearchState) -> ResearchState:
        state.updated_at = now_utc()
        payload = state.model_dump_json()
        created_at = state.created_at.astimezone(timezone.utc).isoformat()
        updated_at = state.updated_at.astimezone(timezone.utc).isoformat()
        with db() as conn:
            conn.execute(
                """
                insert into research_states (research_id, state_json, created_at, updated_at)
                values (?, ?, ?, ?)
                on conflict(research_id) do update set
                    state_json = excluded.state_json,
                    updated_at = excluded.updated_at
                """,
                (state.research_id, payload, created_at, updated_at),
            )
        return state

    def get(self, research_id: str) -> ResearchState | None:
        with db() as conn:
            row = conn.execute("select state_json from research_states where research_id = ?", (research_id,)).fetchone()
        if not row:
            return None
        return ResearchState.model_validate_json(row["state_json"])


