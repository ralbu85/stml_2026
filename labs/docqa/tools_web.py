"""W12 — 웹 도구: 에이전트가 리포 밖 세상(웹)을 읽는다.

안전 기본값(현장 노트): 읽기 전용 + 응답 길이 제한. 도메인 화이트리스트·
승인 게이트 같은 본격 방어는 W14에서 — 여기서는 배관만.
"""

from __future__ import annotations

import re

import requests

USER_AGENT = {"User-Agent": "stml-2026-docqa-agent (course exercise)"}
MAX_CHARS = 2000  # 관찰이 컨텍스트를 삼키지 않게 (W9의 교훈)


def _strip_html(html: str) -> str:
    """태그·스크립트를 걷어내고 본문 텍스트만. (제공됨 — 조악해도 배관 검증엔 충분)"""
    html = re.sub(r"(?is)<(script|style).*?</\1>", " ", html)
    text = re.sub(r"(?s)<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", text).strip()


def fetch_url(url: str, timeout: int = 10) -> str:
    """URL을 받아 본문 텍스트를 돌려준다.

    규칙:
      1) requests.get(url, headers=USER_AGENT, timeout=timeout)
      2) resp.raise_for_status()  — 4xx/5xx면 예외 (잡지 마라! W4 run_tool이 관찰로 바꾼다)
      3) _strip_html(resp.text) 후 MAX_CHARS로 잘라 반환 (넘으면 " ...(잘림)" 붙임)

    TODO(W12): 5~7줄.
    """
    raise NotImplementedError("TODO(W12): fetch_url() 을 구현하세요")


def arxiv_search(query: str, max_results: int = 3) -> str:
    """arXiv API로 논문 제목·ID를 찾는다. (제공됨 — 연구보조 에이전트의 눈)"""
    resp = requests.get(
        "https://export.arxiv.org/api/query",
        params={"search_query": f"all:{query}", "max_results": max_results},
        headers=USER_AGENT, timeout=15,
    )
    resp.raise_for_status()
    entries = re.findall(r"<entry>(.*?)</entry>", resp.text, re.S)
    lines = []
    for e in entries:
        title = re.search(r"<title>(.*?)</title>", e, re.S)
        aid = re.search(r"<id>http://arxiv.org/abs/(.*?)</id>", e)
        if title and aid:
            clean_title = re.sub(r"\s+", " ", title.group(1)).strip()
            lines.append(f"- {clean_title} (arXiv:{aid.group(1)})")
    return "\n".join(lines) if lines else f"(arXiv에서 '{query}' 결과 없음)"


def register_web_tools() -> None:
    """웹 도구 2종을 레지스트리에 등록한다. (제공됨)"""
    from . import tools
    tools.register(
        "fetch_url",
        "URL의 본문 텍스트를 가져온다. 입력은 http(s) URL 하나. 웹페이지 내용이 필요할 때만.",
        fetch_url,
    )
    tools.register(
        "arxiv_search",
        "arXiv에서 논문 제목·ID를 검색한다. 입력은 영문 키워드. 새 논문을 찾을 때만.",
        arxiv_search,
    )
