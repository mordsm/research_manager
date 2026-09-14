# Implementation Plan

## Scope

Build Phase 1 only: a backend-only Research Manager proving orchestration, state
persistence, claim/evidence traceability, and supervisor stopping behavior.

## Ambiguities

- The user did not specify a repository path. I chose `C:\workspace\research_manager`.
- The executor is allowed to use mocked search results, so Phase 1 does not use external
  search APIs or real literature databases.
- `OPEN_NEW_BRANCH` is required as a supervisor decision, but no branch execution behavior
  is requested for Phase 1. The graph records the decision shape but treats only
  `CONTINUE` and `STOP` as executable routing.
- No frontend is requested, so only FastAPI endpoints and tests are implemented.
- Medical/scientific rigor rules are represented in schemas and report fields, but Phase 1
  uses deterministic mock data rather than real medical evidence.

## Smallest Viable Architecture

- Pydantic v2 models in `app/schemas/research.py`:
  - `ResearchState`
  - `StudyRecord`
  - `EvidenceClaim`
  - `Hypothesis`
  - `ResearchPlan`
- LangGraph workflow in `app/workflows/research_graph.py`:
  - `planner`
  - `executor`
  - `evidence_analyst`
  - `critic`
  - `synthesizer`
  - `supervisor`
- SQLite JSON persistence in `app/storage.py`.
- FastAPI routes in `app/main.py`.
- Deterministic mock executor results in `app/mock_search.py`.
- Tests cover graph execution, supervisor stopping, traceability, and persistence.

## Workflow

```text
START -> planner -> executor -> evidence_analyst -> critic -> synthesizer -> supervisor
```

Supervisor decisions:

- `CONTINUE`: route back to `executor`
- `STOP`: end graph and make final report available
- `OPEN_NEW_BRANCH`: recorded for Phase 1, returned to API caller for human/product handling
- `REQUEST_HUMAN`: recorded for Phase 1, returned to API caller for human/product handling

## Phase 1 Done

- A research run can be created with `POST /research`.
- State can be fetched with `GET /research/{research_id}`.
- A run can continue with `POST /research/{research_id}/continue`.
- A final/current report can be fetched with `GET /research/{research_id}/report`.
- The state persists across service instances through SQLite.
- Every generated claim references included study IDs.
