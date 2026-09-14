from __future__ import annotations

from typing import Any


def mocked_search(question: str, iteration: int) -> list[dict[str, Any]]:
    normalized = " ".join(question.split())
    return [
        {
            "source_id": f"mock_source_{iteration}_direct",
            "title": f"Direct evidence candidate for {normalized}",
            "citation": f"Mock Direct Study {iteration}",
            "authors": ["Research Manager Mock"],
            "year": 2026,
            "study_type": "controlled clinical study",
            "abstract": f"Mocked direct evidence discussing whether {normalized}.",
            "directness": "DIRECT",
            "result": "supports a cautious preliminary claim",
        },
        {
            "source_id": f"mock_source_{iteration}_contrary",
            "title": f"Contradictory evidence candidate for {normalized}",
            "citation": f"Mock Contrary Study {iteration}",
            "authors": ["Research Manager Mock"],
            "year": 2025,
            "study_type": "prospective cohort",
            "abstract": f"Mocked contradictory evidence showing uncertainty around {normalized}.",
            "directness": "INDIRECT",
            "result": "raises uncertainty and possible confounding",
        },
    ]

