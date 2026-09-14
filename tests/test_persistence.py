from __future__ import annotations

import os
import tempfile
from pathlib import Path


def test_state_persistence_round_trip():
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ["RESEARCH_MANAGER_DATABASE_PATH"] = str(Path(tmpdir) / "research.db")

        from app.config import get_settings
        from app.schemas.research import ResearchState
        from app.storage import ResearchStore, init_db
        from app.workflows.research_graph import run_research_graph

        get_settings.cache_clear()
        init_db()
        store = ResearchStore()
        state = run_research_graph(ResearchState(original_user_request="Does X affect Y?"))
        store.save(state)

        loaded = ResearchStore().get(state.research_id)

        assert loaded is not None
        assert loaded.research_id == state.research_id
        assert loaded.claims[0].traceability == state.claims[0].traceability
        assert loaded.final_report == state.final_report

