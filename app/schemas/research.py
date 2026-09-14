from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


class ClaimType(StrEnum):
    DIRECT_EVIDENCE = "DIRECT_EVIDENCE"
    INDIRECT_EVIDENCE = "INDIRECT_EVIDENCE"
    INFERENCE = "INFERENCE"
    HYPOTHESIS = "HYPOTHESIS"
    SPECULATION = "SPECULATION"


class EvidenceStrength(StrEnum):
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"
    VERY_LOW = "VERY_LOW"
    INSUFFICIENT = "INSUFFICIENT"


class HypothesisStatus(StrEnum):
    ACTIVE = "ACTIVE"
    WEAKENED = "WEAKENED"
    SUPPORTED = "SUPPORTED"
    REJECTED = "REJECTED"
    UNTESTED = "UNTESTED"


class SupervisorDecision(StrEnum):
    CONTINUE = "CONTINUE"
    OPEN_NEW_BRANCH = "OPEN_NEW_BRANCH"
    STOP = "STOP"
    REQUEST_HUMAN = "REQUEST_HUMAN"


class Hypothesis(BaseModel):
    hypothesis_id: str = Field(default_factory=lambda: new_id("hypothesis"))
    statement: str
    origin: str = "planner"
    direct_evidence: list[str] = Field(default_factory=list)
    indirect_evidence: list[str] = Field(default_factory=list)
    supporting_claims: list[str] = Field(default_factory=list)
    contradicting_claims: list[str] = Field(default_factory=list)
    mechanistic_plausibility: str = "UNKNOWN"
    assumptions: list[str] = Field(default_factory=list)
    unknowns: list[str] = Field(default_factory=list)
    falsification_conditions: list[str] = Field(default_factory=list)
    proposed_test: str = "UNKNOWN"
    proposed_experiment: str = "UNKNOWN"
    confidence: int = Field(default=0, ge=0, le=100)
    status: HypothesisStatus = HypothesisStatus.UNTESTED


class ResearchPlan(BaseModel):
    primary_question: str
    secondary_questions: list[str] = Field(default_factory=list)
    hypotheses: list[Hypothesis] = Field(default_factory=list)
    search_domains: list[str] = Field(default_factory=list)
    inclusion_criteria: list[str] = Field(default_factory=list)
    exclusion_criteria: list[str] = Field(default_factory=list)
    evidence_quality_criteria: list[str] = Field(default_factory=list)
    branch_candidates: list[str] = Field(default_factory=list)
    stop_policy: dict[str, Any] = Field(default_factory=lambda: {"max_iterations": 2})


class StudyRecord(BaseModel):
    study_id: str = Field(default_factory=lambda: new_id("study"))
    source_id: str
    citation: str
    authors: list[str] = Field(default_factory=list)
    year: int | str = "UNKNOWN"
    journal: str = "UNKNOWN"
    country: str = "UNKNOWN"
    study_type: str = "UNKNOWN"
    population: str = "UNKNOWN"
    sample_size: int | str = "UNKNOWN"
    intervention: str = "UNKNOWN"
    comparator: str = "UNKNOWN"
    duration: str = "UNKNOWN"
    primary_outcomes: list[str] = Field(default_factory=list)
    secondary_outcomes: list[str] = Field(default_factory=list)
    effect_size: str = "UNKNOWN"
    confidence_interval: str = "UNKNOWN"
    p_value: str = "UNKNOWN"
    clinical_significance: str = "UNKNOWN"
    statistical_significance: str = "UNKNOWN"
    randomization: str = "UNKNOWN"
    blinding: str = "UNKNOWN"
    attrition: str = "UNKNOWN"
    confounders: list[str] = Field(default_factory=list)
    risk_of_bias: str = "UNKNOWN"
    funding: str = "UNKNOWN"
    conflicts_of_interest: str = "UNKNOWN"
    replication_status: str = "UNKNOWN"
    directness: str = "UNKNOWN"
    major_limitations: list[str] = Field(default_factory=list)
    evidence_weight: EvidenceStrength = EvidenceStrength.LOW
    fulltext_available: bool = False
    citation_verified: bool = False


class EvidenceClaim(BaseModel):
    claim_id: str = Field(default_factory=lambda: new_id("claim"))
    text: str
    claim_type: ClaimType
    status: str = "ACTIVE"
    supporting_studies: list[str] = Field(default_factory=list)
    contradicting_studies: list[str] = Field(default_factory=list)
    direct_evidence_count: int = 0
    indirect_evidence_count: int = 0
    evidence_strength: EvidenceStrength = EvidenceStrength.INSUFFICIENT
    confidence_score: int = Field(default=0, ge=0, le=100)
    assumptions: list[str] = Field(default_factory=list)
    unknowns: list[str] = Field(default_factory=list)
    alternative_explanations: list[str] = Field(default_factory=list)
    traceability: dict[str, list[str]] = Field(default_factory=lambda: {"source_ids": []})
    review_status: str = "UNREVIEWED"


class ResearchState(BaseModel):
    research_id: str = Field(default_factory=lambda: new_id("research"))
    original_user_request: str
    primary_question: str = ""
    research_plan: ResearchPlan | None = None
    active_hypotheses: list[Hypothesis] = Field(default_factory=list)
    rejected_hypotheses: list[Hypothesis] = Field(default_factory=list)
    candidate_branches: list[str] = Field(default_factory=list)
    active_branches: list[str] = Field(default_factory=list)
    completed_branches: list[str] = Field(default_factory=list)
    unexplored_branches: list[str] = Field(default_factory=list)
    discovered_sources: list[dict[str, Any]] = Field(default_factory=list)
    screened_sources: list[str] = Field(default_factory=list)
    included_studies: list[StudyRecord] = Field(default_factory=list)
    excluded_studies: list[dict[str, str]] = Field(default_factory=list)
    inaccessible_sources: list[dict[str, str]] = Field(default_factory=list)
    claims: list[EvidenceClaim] = Field(default_factory=list)
    contradictions: list[str] = Field(default_factory=list)
    current_conclusion: str | None = None
    current_confidence: float = 0.0
    unknowns: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    iteration_count: int = 0
    search_budget_used: float = 0.0
    stopping_reason: str | None = None
    specialist_agent_proposals: list[dict[str, Any]] = Field(default_factory=list)
    supervisor_decision: SupervisorDecision | None = None
    final_report: str | None = None
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)


class ResearchCreateRequest(BaseModel):
    question: str

