"""W4 — 리서치 검색 도구 (제공됨).

코드 구조 출처: Andrew Ng *Agentic AI* Module 1 `src/research_tools.py`
(arxiv/tavily/wikipedia 3종 도구). 수업용으로 간소화 — 원본의 PDF 다운로드·
세션 재시도 로직은 제외하고 검색·요약 반환만 유지한다.

- arxiv_search_tool · wikipedia_search_tool: API 키 불필요.
- tavily_search_tool: TAVILY_API_KEY 가 .env 에 있을 때만 실제 검색.

세 함수 모두 aisuite 의 tools= 인자에 그대로 넘길 수 있다(W4 워크플로에서 사용).
"""

from __future__ import annotations

import os
import re
import xml.etree.ElementTree as ET

import requests

REQUEST_TIMEOUT = 20
_ATOM = "{http://www.w3.org/2005/Atom}"


def arxiv_search_tool(query: str, max_results: int = 5) -> list[dict]:
    """arXiv에서 학술 논문을 검색한다. 논문·기술 보고서가 필요할 때만 사용.

    Args:
        query: 찾으려는 주제를 서술한 검색어 (영어 권장).
        max_results: 반환할 논문 수 (기본 5).

    Returns:
        [{title, authors, published, summary, url}, ...]
    """
    resp = requests.get(
        "https://export.arxiv.org/api/query",
        params={"search_query": f"all:{query}", "max_results": max_results,
                "sortBy": "relevance"},
        timeout=REQUEST_TIMEOUT,
    )
    resp.raise_for_status()
    results = []
    for entry in ET.fromstring(resp.text).findall(f"{_ATOM}entry"):
        results.append({
            "title": " ".join(entry.findtext(f"{_ATOM}title", "").split()),
            "authors": [a.findtext(f"{_ATOM}name", "")
                        for a in entry.findall(f"{_ATOM}author")][:5],
            "published": entry.findtext(f"{_ATOM}published", "")[:10],
            "summary": " ".join(entry.findtext(f"{_ATOM}summary", "").split())[:600],
            "url": entry.findtext(f"{_ATOM}id", ""),
        })
    return results


def wikipedia_search_tool(query: str, max_results: int = 3) -> list[dict]:
    """위키백과에서 배경 지식·정의·개요를 검색한다. 기초 개념 확인에 사용.

    Args:
        query: 검색어.
        max_results: 반환할 문서 수 (기본 3).

    Returns:
        [{title, snippet, url}, ...]
    """
    resp = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={"action": "query", "list": "search", "srsearch": query,
                "srlimit": max_results, "format": "json"},
        timeout=REQUEST_TIMEOUT,
        headers={"User-Agent": "STML2026-lab/1.0"},
    )
    resp.raise_for_status()
    results = []
    for hit in resp.json().get("query", {}).get("search", []):
        snippet = re.sub(r"<[^>]+>", "", hit.get("snippet", ""))  # HTML 태그 제거
        results.append({
            "title": hit["title"],
            "snippet": snippet,
            "url": f'https://en.wikipedia.org/wiki/{hit["title"].replace(" ", "_")}',
        })
    return results


def tavily_search_tool(query: str, max_results: int = 5) -> list[dict]:
    """일반 웹을 검색한다. 최신 동향·비학술 자료가 필요할 때 사용.

    TAVILY_API_KEY 가 없으면 검색하지 않고 안내를 반환한다(랩 진행에는 지장 없음).

    Args:
        query: 검색어.
        max_results: 반환할 결과 수 (기본 5).

    Returns:
        [{title, content, url}, ...] 또는 [{notice}] (키 없음).
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return [{"notice": "TAVILY_API_KEY 미설정 — 웹 검색을 건너뜀. "
                           "arxiv/wikipedia 도구를 사용하라."}]
    resp = requests.post(
        "https://api.tavily.com/search",
        json={"api_key": api_key, "query": query, "max_results": max_results},
        timeout=REQUEST_TIMEOUT,
    )
    resp.raise_for_status()
    return [{"title": r.get("title", ""), "content": r.get("content", "")[:600],
             "url": r.get("url", "")}
            for r in resp.json().get("results", [])]
