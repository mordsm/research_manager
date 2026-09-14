# Research Manager

Phase 1 backend-only Research Manager using FastAPI, LangGraph, Pydantic v2, SQLite, and
pytest.

This phase proves orchestration:

```text
START -> planner -> executor -> evidence_analyst -> critic -> synthesizer -> supervisor
```

The executor currently uses mocked medical-source adapters. It is structured around PubMed, ClinicalTrials.gov, NCCIH, Cochrane Complementary Medicine, CAM-Quest, NIEHS, NINDS Parkinson's Disease Research, NIH Office of Autoimmune Disease Research, and Michael J. Fox Foundation so the next phase can replace mocks with live connectors. No frontend is included.


## Medical Research Scope

Research Manager is being shaped for careful investigation of possible treatments for illnesses. It separates published literature, trial registry evidence, and complementary/integrative medicine so findings can be traced before anyone treats them as actionable.

Current source targets:

- PubMed: published biomedical papers, reviews, meta-analyses, and clinical study publications.
- ClinicalTrials.gov: registered clinical studies, trial phase/status, outcomes, eligibility, and NCT identifiers.
- NCCIH: NIH complementary and integrative health research, including exercise, yoga, mindfulness, nutrition, supplements, acupuncture, sleep, stress, and related approaches.
- Cochrane Complementary Medicine: systematic reviews and evidence summaries for complementary/alternative interventions.
- CAM-Quest: broad complementary and alternative medicine evidence map by condition, therapy, and study type.
- NIEHS: environmental exposures, pesticides, toxins, and gene-environment factors relevant to autoimmune disease and Parkinson's disease.
- NINDS Parkinson's Disease Research: NIH neurological research on Parkinson's mechanisms, biomarkers, genetics, and disease-modifying treatment research.
- NIH Office of Autoimmune Disease Research: NIH-wide autoimmune disease strategy, mechanisms, sex differences, and immune dysregulation.
- Michael J. Fox Foundation: Parkinson's biomarkers, genetics, therapeutic pipeline, PPMI, prevention, and progression research.
The current reports are research-organization support only. They are not diagnosis or treatment advice.

## Idea Exploration

Use `IDEA_EXPLORATION` when the input is a hypothesis or cross-study idea rather than a direct evidence-review question. The report will add mechanism mapping, bridge inferences, and falsification tests so indirect conclusions stay separate from direct evidence.

Example request body:

```json
{
  "question": "Could gut inflammation connect autoimmune disease and Parkinson's disease?",
  "mode": "IDEA_EXPLORATION"
}
```
## Run

```powershell
cd C:\workspace\research_manager
uv --system-certs sync --group dev
uv run uvicorn app.main:app --reload --port 8020
```

## Test

```powershell
uv run pytest
```







