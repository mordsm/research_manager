from __future__ import annotations

from typing import Any

from app.medical_sources import COMPLEMENTARY_MEDICINE_DOMAINS


def mocked_search(question: str, iteration: int) -> list[dict[str, Any]]:
    normalized = " ".join(question.split())
    return [
        {
            "source_id": f"pubmed_mock_{iteration}_review",
            "database": "PubMed",
            "title": f"Published evidence candidate for {normalized}",
            "citation": f"PubMed Mock Review {iteration}",
            "authors": ["Research Manager Medical Mock"],
            "year": 2026,
            "study_type": "systematic review",
            "abstract": f"Mocked PubMed result summarizing published evidence about {normalized}.",
            "directness": "DIRECT",
            "result": "summarizes published benefits, harms, and uncertainty",
            "url": "https://pubmed.ncbi.nlm.nih.gov/",
        },
        {
            "source_id": f"clinicaltrials_mock_{iteration}_trial",
            "database": "ClinicalTrials.gov",
            "title": f"Registered trial candidate for {normalized}",
            "citation": f"ClinicalTrials.gov Mock Trial {iteration}",
            "authors": ["Research Manager Medical Mock"],
            "year": 2025,
            "study_type": "registered clinical trial",
            "abstract": f"Mocked clinical trial registry result testing {normalized}.",
            "directness": "INDIRECT",
            "result": "identifies investigational status, eligibility, and outcome measures",
            "url": "https://clinicaltrials.gov/",
        },
        {
            "source_id": f"nccih_mock_{iteration}_integrative",
            "database": "NCCIH",
            "title": f"Complementary and integrative intervention candidate for {normalized}",
            "citation": f"NCCIH Mock Integrative Health Evidence {iteration}",
            "authors": ["Research Manager Medical Mock"],
            "year": 2026,
            "study_type": "complementary medicine evidence scan",
            "abstract": f"Mocked NCCIH-style result covering {', '.join(COMPLEMENTARY_MEDICINE_DOMAINS)} for {normalized}.",
            "directness": "INDIRECT",
            "result": "maps exercise, yoga, mind-body, nutrition, supplements, and related alternatives for evidence review",
            "url": "https://www.nccih.nih.gov/research",
        },
    ]
