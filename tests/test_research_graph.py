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



def test_medical_research_sources_and_complementary_domains_are_planned():
    state = ResearchState(original_user_request="What new treatments may help chronic migraine?")

    result = run_research_graph(state)

    assert result.research_plan is not None
    assert "PubMed" in result.research_plan.search_domains
    assert "ClinicalTrials.gov" in result.research_plan.search_domains
    assert "NCCIH" in result.research_plan.search_domains
    assert "exercise and supervised physical activity" in result.research_plan.search_domains
    assert "yoga and breathwork" in result.research_plan.search_domains


def test_medical_research_report_names_sources_and_safety_boundary():
    state = ResearchState(original_user_request="What alternative treatments may help insomnia?")

    result = run_research_graph(state)

    assert result.final_report is not None
    assert "PubMed" in result.final_report
    assert "ClinicalTrials.gov" in result.final_report
    assert "NCCIH" in result.final_report
    assert "yoga and breathwork" in result.final_report
    assert "not diagnosis or treatment advice" in result.final_report




def test_idea_exploration_mode_creates_bridge_inference_and_falsification_tests():
    from app.schemas.research import ResearchMode

    state = ResearchState(
        original_user_request="Could gut inflammation connect autoimmune disease and Parkinson's?",
        mode=ResearchMode.IDEA_EXPLORATION,
    )

    result = run_research_graph(state)

    assert result.mode == ResearchMode.IDEA_EXPLORATION
    assert result.explored_idea == "Could gut inflammation connect autoimmune disease and Parkinson's?"
    assert result.mechanism_map
    assert result.bridge_inferences
    assert result.falsification_tests
    assert result.final_report is not None
    assert "## Idea Exploration" in result.final_report
    assert "## Bridge Inferences" in result.final_report
    assert "## Falsification Tests" in result.final_report

