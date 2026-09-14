from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from app.schemas.research import ResearchCreateRequest, ResearchState
from app.storage import ResearchStore, init_db
from app.workflows.research_graph import run_research_graph


def create_app() -> FastAPI:
    app = FastAPI(title="Research Manager", version="0.1.0")
    store = ResearchStore()

    @app.get("/", include_in_schema=False)
    def index() -> FileResponse:
        return FileResponse("app/static/index.html")

    @app.on_event("startup")
    def startup() -> None:
        init_db()

    @app.post("/research", response_model=ResearchState)
    def create_research(request: ResearchCreateRequest) -> ResearchState:
        init_db()
        state = ResearchState(original_user_request=request.question, mode=request.mode, live_search=request.live_search)
        state = run_research_graph(state)
        return store.save(state)

    @app.get("/research/{research_id}", response_model=ResearchState)
    def get_research(research_id: str) -> ResearchState:
        state = store.get(research_id)
        if not state:
            raise HTTPException(status_code=404, detail="research_not_found")
        return state

    @app.post("/research/{research_id}/continue", response_model=ResearchState)
    def continue_research(research_id: str) -> ResearchState:
        state = store.get(research_id)
        if not state:
            raise HTTPException(status_code=404, detail="research_not_found")
        state.stopping_reason = None
        state.final_report = None
        state = run_research_graph(state)
        return store.save(state)

    @app.get("/research/{research_id}/report")
    def get_report(research_id: str) -> dict[str, str | None]:
        state = store.get(research_id)
        if not state:
            raise HTTPException(status_code=404, detail="research_not_found")
        return {"research_id": research_id, "report": state.final_report}

    return app


app = create_app()





