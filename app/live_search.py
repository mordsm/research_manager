from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen


PUBMED_ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_ESUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
CLINICALTRIALS_URL = "https://clinicaltrials.gov/api/v2/studies"


def live_medical_search(question: str, max_results: int = 5, timeout: float = 12.0) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    results.extend(search_pubmed(question, max_results=max_results, timeout=timeout))
    results.extend(search_clinical_trials(question, max_results=max_results, timeout=timeout))
    return results


def _get_json(url: str, timeout: float) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": "research-manager/0.1"})
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def search_pubmed(question: str, max_results: int, timeout: float) -> list[dict[str, Any]]:
    search_params = urlencode({"db": "pubmed", "term": question, "retmode": "json", "retmax": max_results})
    search_payload = _get_json(f"{PUBMED_ESEARCH_URL}?{search_params}", timeout)
    pmids = search_payload.get("esearchresult", {}).get("idlist", [])
    if not pmids:
        return []

    summary_params = urlencode({"db": "pubmed", "id": ",".join(pmids), "retmode": "json"})
    summary_payload = _get_json(f"{PUBMED_ESUMMARY_URL}?{summary_params}", timeout)
    summaries = summary_payload.get("result", {})

    records: list[dict[str, Any]] = []
    for pmid in pmids:
        item = summaries.get(pmid, {})
        title = item.get("title") or "Untitled PubMed record"
        authors = [author.get("name", "UNKNOWN") for author in item.get("authors", [])[:6]]
        pubdate = item.get("pubdate", "UNKNOWN")
        year = pubdate[:4] if pubdate else "UNKNOWN"
        journal = item.get("fulljournalname") or item.get("source") or "UNKNOWN"
        records.append(
            {
                "source_id": f"pubmed_{pmid}",
                "database": "PubMed",
                "title": title,
                "citation": f"{title} {journal}. {pubdate}. PMID:{pmid}",
                "authors": authors,
                "year": year,
                "journal": journal,
                "study_type": item.get("pubtype", ["PubMed record"])[0],
                "abstract": "Abstract retrieval is not yet wired; PubMed summary metadata was retrieved live.",
                "directness": "DIRECT",
                "result": "live PubMed result requiring evidence extraction and full abstract review",
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            }
        )
    return records


def search_clinical_trials(question: str, max_results: int, timeout: float) -> list[dict[str, Any]]:
    params = urlencode({"query.term": question, "pageSize": max_results, "format": "json"})
    payload = _get_json(f"{CLINICALTRIALS_URL}?{params}", timeout)
    records: list[dict[str, Any]] = []
    for study in payload.get("studies", []):
        protocol = study.get("protocolSection", {})
        identification = protocol.get("identificationModule", {})
        status = protocol.get("statusModule", {})
        design = protocol.get("designModule", {})
        conditions = protocol.get("conditionsModule", {})
        nct_id = identification.get("nctId", "UNKNOWN")
        title = identification.get("briefTitle") or identification.get("officialTitle") or "Untitled clinical trial"
        phase_list = design.get("phases", [])
        records.append(
            {
                "source_id": f"clinicaltrials_{nct_id}",
                "database": "ClinicalTrials.gov",
                "title": title,
                "citation": f"{title}. ClinicalTrials.gov {nct_id}.",
                "authors": ["ClinicalTrials.gov registry"],
                "year": status.get("startDateStruct", {}).get("date", "UNKNOWN")[:4],
                "study_type": design.get("studyType", "registered clinical trial"),
                "abstract": "; ".join(conditions.get("conditions", [])) or "Live clinical trial registry metadata was retrieved.",
                "directness": "INDIRECT",
                "result": f"registry status: {status.get('overallStatus', 'UNKNOWN')}; phase: {', '.join(phase_list) if phase_list else 'UNKNOWN'}",
                "url": f"https://clinicaltrials.gov/study/{nct_id}",
            }
        )
    return records
