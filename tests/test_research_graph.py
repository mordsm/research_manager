from __future__ import annotations

from app.schemas.research import ResearchState, SupervisorDecision
from app.workflows.research_graph import run_research_graph


def test_graph_execution_creates_plan_studies_claims_and_report():
    state = ResearchState(original_user_request="Does intervention X improve outcome Y?")

    result = run_research_graph(state)

    assert result.research_plan is not None
    assert result.primary_question == "Does intervention X improve outcome Y?"
    assert len(result.included_studies) >= 2
    assert len(result.claims) == 1
    assert result.supervisor_decision == SupervisorDecision.STOP
    assert result.final_report is not None


def test_supervisor_stops_after_configured_iterations():
    state = ResearchState(original_user_request="What evidence exists for X?")

    result = run_research_graph(state)

    assert result.iteration_count == 2
    assert result.supervisor_decision == SupervisorDecision.STOP
    assert result.stopping_reason == "RESOURCE_LIMIT"


def test_claim_evidence_traceability():
    state = ResearchState(original_user_request="Can X cause Y?")

    result = run_research_graph(state)
    study_source_ids = {study.source_id for study in result.included_studies}
    claim = result.claims[0]

    assert claim.traceability["source_ids"]
    assert set(claim.traceability["source_ids"]).issubset(study_source_ids)
    assert claim.supporting_studies or claim.contradicting_studies

