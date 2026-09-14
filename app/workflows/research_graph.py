from __future__ import annotations

from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph

from app.config import get_settings
from app.medical_sources import COMPLEMENTARY_MEDICINE_DOMAINS, source_focus_lines, source_names
from app.mock_search import mocked_search
from app.schemas.research import (
    ClaimType,
    EvidenceClaim,
    EvidenceStrength,
    Hypothesis,
    HypothesisStatus,
    ResearchPlan,
    ResearchState,
    StudyRecord,
    SupervisorDecision,
)


class GraphState(TypedDict):
    research: dict


def _load(graph_state: GraphState) -> ResearchState:
    return ResearchState.model_validate(graph_state["research"])


def _dump(state: ResearchState) -> GraphState:
    return {"research": state.model_dump(mode="json")}


def planner(graph_state: GraphState) -> GraphState:
    state = _load(graph_state)
    if state.research_plan:
        return _dump(state)

    primary_question = state.original_user_request.strip()
    hypothesis = Hypothesis(
        hypothesis_id="H1",
        statement=f"The available evidence can answer: {primary_question}",
        origin="planner",
        assumptions=["Phase 1 uses mocked medical-source search results."],
        unknowns=["Live database coverage is unavailable until PubMed, ClinicalTrials.gov, and NCCIH connectors are wired."],
        falsification_conditions=["High-quality contradictory evidence outweighs supporting evidence."],
        proposed_test="Replace mocked source adapters with live PubMed, ClinicalTrials.gov, and NCCIH searches.",
        proposed_experiment="Run the same plan against PubMed, ClinicalTrials.gov, and NCCIH in a later phase.",
        confidence=10,
        status=HypothesisStatus.ACTIVE,
    )
    state.primary_question = primary_question
    state.research_plan = ResearchPlan(
        primary_question=primary_question,
        secondary_questions=[
            "What published evidence exists in PubMed?",
            "What registered or completed trials exist in ClinicalTrials.gov?",
            "What complementary, integrative, exercise, yoga, nutrition, or mind-body evidence exists?",
            "What safety concerns, contraindications, or evidence gaps remain?",
        ],
        hypotheses=[hypothesis],
        search_domains=source_names() + COMPLEMENTARY_MEDICINE_DOMAINS,
        inclusion_criteria=["Material to the illness, treatment, or outcome question", "Traceable PMID, NCT ID, DOI, URL, or source ID", "Human clinical relevance when available", "Safety, adverse-event, and contraindication information when available"],
        exclusion_criteria=["Duplicate source IDs", "Untraceable claims", "Treatment claims without identifiable evidence", "Content that presents medical advice without research support"],
        evidence_quality_criteria=["Directness", "study design", "risk of bias", "sample size", "clinical significance", "safety reporting", "citation verification"],
        branch_candidates=["published literature branch", "clinical trials branch", "complementary medicine branch", "safety and contraindications branch"],
        stop_policy={"max_iterations": get_settings().max_iterations},
    )
    state.active_hypotheses = [hypothesis]
    state.candidate_branches = ["published literature branch", "clinical trials branch", "complementary medicine branch", "safety and contraindications branch"]
    state.active_branches = ["published literature branch", "clinical trials branch", "complementary medicine branch"]
    state.unknowns.append("Phase 1 does not yet access live PubMed, ClinicalTrials.gov, or NCCIH databases.")
    return _dump(state)


def executor(graph_state: GraphState) -> GraphState:
    state = _load(graph_state)
    next_iteration = state.iteration_count + 1
    results = mocked_search(state.primary_question, next_iteration)
    known_source_ids = {source["source_id"] for source in state.discovered_sources}
    for result in results:
        if result["source_id"] not in known_source_ids:
            state.discovered_sources.append(result)
            state.screened_sources.append(result["source_id"])
    state.search_budget_used += 1.0
    return _dump(state)


def evidence_analyst(graph_state: GraphState) -> GraphState:
    state = _load(graph_state)
    included_source_ids = {study.source_id for study in state.included_studies}
    for source in state.discovered_sources:
        if source["source_id"] in included_source_ids:
            continue
        state.included_studies.append(
            StudyRecord(
                source_id=source["source_id"],
                citation=source["citation"],
                authors=source.get("authors", []),
                year=source.get("year", "UNKNOWN"),
                study_type=source.get("study_type", "UNKNOWN"),
                primary_outcomes=[source["result"]],
                directness=source["directness"],
                major_limitations=["Mocked source adapter; citation not externally verified yet."],
                evidence_weight=EvidenceStrength.LOW,
                fulltext_available=False,
                citation_verified=False,
            )
        )
    return _dump(state)


def critic(graph_state: GraphState) -> GraphState:
    state = _load(graph_state)
    if "Mock medical evidence cannot establish real-world treatment safety or effectiveness." not in state.contradictions:
        state.contradictions.append("Mock medical evidence cannot establish real-world treatment safety or effectiveness.")
    if "Citation and trial-registry verification are unavailable in Phase 1." not in state.unknowns:
        state.unknowns.append("Citation and trial-registry verification are unavailable in Phase 1.")
    return _dump(state)


def synthesizer(graph_state: GraphState) -> GraphState:
    state = _load(graph_state)
    source_ids = [study.source_id for study in state.included_studies]
    direct_count = sum(1 for study in state.included_studies if study.directness == "DIRECT")
    indirect_count = max(0, len(state.included_studies) - direct_count)
    support = [study.study_id for study in state.included_studies if study.directness == "DIRECT"]
    contradict = [study.study_id for study in state.included_studies if study.directness != "DIRECT"]

    claim = EvidenceClaim(
        claim_id="C1",
        text=f"Phase 1 medical-source mock evidence provides a traceable but low-confidence treatment research synthesis for: {state.primary_question}",
        claim_type=ClaimType.INFERENCE,
        supporting_studies=support,
        contradicting_studies=contradict,
        direct_evidence_count=direct_count,
        indirect_evidence_count=indirect_count,
        evidence_strength=EvidenceStrength.LOW if source_ids else EvidenceStrength.INSUFFICIENT,
        confidence_score=30 if source_ids else 0,
        assumptions=["Executor uses mocked medical-source adapters."],
        unknowns=state.unknowns,
        alternative_explanations=["The treatment picture may change when live medical databases are searched."],
        traceability={"source_ids": source_ids},
        review_status="CRITIC_REVIEWED",
    )
    state.claims = [claim]
    state.current_conclusion = claim.text
    state.current_confidence = float(claim.confidence_score)
    return _dump(state)


def supervisor(graph_state: GraphState) -> GraphState:
    state = _load(graph_state)
    state.iteration_count += 1
    max_iterations = 2
    if state.research_plan:
        max_iterations = int(state.research_plan.stop_policy.get("max_iterations", max_iterations))

    if not state.claims:
        state.supervisor_decision = SupervisorDecision.REQUEST_HUMAN
        state.stopping_reason = "NO_TRACEABLE_CLAIMS"
    elif state.iteration_count >= max_iterations:
        state.supervisor_decision = SupervisorDecision.STOP
        state.stopping_reason = "RESOURCE_LIMIT"
        state.final_report = generate_final_report(state)
    else:
        state.supervisor_decision = SupervisorDecision.CONTINUE

    return _dump(state)


def route_after_supervisor(graph_state: GraphState) -> Literal["executor", "__end__"]:
    state = _load(graph_state)
    if state.supervisor_decision == SupervisorDecision.CONTINUE:
        return "executor"
    return "__end__"


def generate_final_report(state: ResearchState) -> str:
    claim_lines = "\n".join(
        f"- {claim.claim_id}: {claim.text} | sources: {', '.join(claim.traceability.get('source_ids', []))}"
        for claim in state.claims
    )
    reference_lines = "\n".join(f"- {study.study_id}: {study.citation} ({study.source_id})" for study in state.included_studies)
    return f"""# Final Research Report

## Research Question

{state.primary_question}

## Research Method

Phase 1 LangGraph orchestration with mocked medical-source adapters for PubMed, ClinicalTrials.gov, and NCCIH. Workflow: planner -> executor -> evidence_analyst -> critic -> synthesizer -> supervisor.

## Search Sources

{chr(10).join('- ' + line for line in source_focus_lines())}

## Complementary Medicine Domains

{chr(10).join('- ' + domain for domain in COMPLEMENTARY_MEDICINE_DOMAINS)}

## Key Claims

{claim_lines}

## Limitations

- Executor used mocked medical-source adapters only.
- Citation and trial-registry verification are unavailable in Phase 1.
- No live medical literature or trial databases were searched yet.
- This is research organization support, not diagnosis or treatment advice.

## Why Research Stopped

{state.stopping_reason or "UNKNOWN"}

## References

{reference_lines}
"""


def build_research_graph():
    graph = StateGraph(GraphState)
    graph.add_node("planner", planner)
    graph.add_node("executor", executor)
    graph.add_node("evidence_analyst", evidence_analyst)
    graph.add_node("critic", critic)
    graph.add_node("synthesizer", synthesizer)
    graph.add_node("supervisor", supervisor)
    graph.add_edge(START, "planner")
    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "evidence_analyst")
    graph.add_edge("evidence_analyst", "critic")
    graph.add_edge("critic", "synthesizer")
    graph.add_edge("synthesizer", "supervisor")
    graph.add_conditional_edges("supervisor", route_after_supervisor, {"executor": "executor", "__end__": END})
    return graph.compile()


def run_research_graph(state: ResearchState) -> ResearchState:
    result = build_research_graph().invoke({"research": state.model_dump(mode="json")})
    return ResearchState.model_validate(result["research"])




