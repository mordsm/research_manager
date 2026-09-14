from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MedicalResearchSource:
    source_id: str
    name: str
    purpose: str
    search_url: str
    evidence_focus: str


MEDICAL_RESEARCH_SOURCES = [
    MedicalResearchSource(
        source_id="pubmed",
        name="PubMed",
        purpose="Published biomedical and clinical literature.",
        search_url="https://pubmed.ncbi.nlm.nih.gov/",
        evidence_focus="papers, reviews, meta-analyses, clinical study publications",
    ),
    MedicalResearchSource(
        source_id="clinicaltrials",
        name="ClinicalTrials.gov",
        purpose="Registered clinical studies and trial protocols.",
        search_url="https://clinicaltrials.gov/",
        evidence_focus="trial phase, recruitment status, outcomes, eligibility, NCT identifiers",
    ),
    MedicalResearchSource(
        source_id="nccih",
        name="NCCIH",
        purpose="NIH complementary and integrative health research.",
        search_url="https://www.nccih.nih.gov/research",
        evidence_focus="alternative medicine, complementary therapies, mind-body practices, exercise, yoga",
    ),
    MedicalResearchSource(
        source_id="cochrane_cam",
        name="Cochrane Complementary Medicine",
        purpose="Systematic reviews and evidence summaries for complementary medicine.",
        search_url="https://cam.cochrane.org/evidence",
        evidence_focus="systematic reviews of acupuncture, herbal medicine, massage, mind-body therapies, and other CAM interventions",
    ),
    MedicalResearchSource(
        source_id="cam_quest",
        name="CAM-Quest",
        purpose="Complementary and alternative medicine evidence database.",
        search_url="https://www.cam-quest.org/en",
        evidence_focus="CAM searches by condition, therapy, and study type; useful as a broad historical evidence map",
    ),
    MedicalResearchSource(
        source_id="niehs",
        name="NIEHS",
        purpose="NIH environmental health research for disease causes and risk factors.",
        search_url="https://www.niehs.nih.gov/health/topics",
        evidence_focus="environmental exposures, pesticides, toxins, gene-environment interaction, autoimmune disease, Parkinson's disease",
    ),
    MedicalResearchSource(
        source_id="ninds_parkinson",
        name="NINDS Parkinson's Disease Research",
        purpose="NIH neurological research focused on Parkinson's disease.",
        search_url="https://www.ninds.nih.gov/current-research/focus-disorders/parkinsons-disease-research",
        evidence_focus="neurodegeneration, dopamine pathways, biomarkers, genetics, mechanisms, disease-modifying treatment research",
    ),
    MedicalResearchSource(
        source_id="nih_autoimmune_research",
        name="NIH Office of Autoimmune Disease Research",
        purpose="NIH-wide autoimmune disease research strategy and coordination.",
        search_url="https://orwh.od.nih.gov/OADR-ORWH",
        evidence_focus="autoimmune disease mechanisms, sex differences, immune dysregulation, strategic research priorities",
    ),
    MedicalResearchSource(
        source_id="mjff",
        name="Michael J. Fox Foundation",
        purpose="Parkinson's disease research foundation and translational research programs.",
        search_url="https://www.michaeljfox.org/our-research",
        evidence_focus="Parkinson's biomarkers, genetics, therapeutic pipeline, PPMI, prevention and disease progression research",
    ),
]


COMPLEMENTARY_MEDICINE_DOMAINS = [
    "exercise and supervised physical activity",
    "yoga and breathwork",
    "mindfulness and meditation",
    "nutrition and dietary patterns",
    "supplements and herbal products",
    "acupuncture and manual therapies",
    "sleep, stress, and behavioral interventions",
]


def source_names() -> list[str]:
    return [source.name for source in MEDICAL_RESEARCH_SOURCES]


def source_focus_lines() -> list[str]:
    return [f"{source.name}: {source.evidence_focus}" for source in MEDICAL_RESEARCH_SOURCES]


