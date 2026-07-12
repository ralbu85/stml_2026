"""W10 — 메모리 📦: 단기(대화 버퍼) + 장기(파일 저장·검색).

컨텍스트(W9)가 책상이라면 메모리는 서랍이다 — 밖에 저장했다가 필요할 때 회수.
장기 메모리 '검색'은 W7 Retriever를 그대로 재사용한다 (같은 부품, 다른 데이터).
"""

from __future__ import annotations

import json
from pathlib import Path


class Memory:
    def __init__(self, path: str | Path):
        self.path = Path(path)          # 장기 저장소 (JSONL — 한 줄 한 사실)
        self.turns: list[dict] = []     # 단기: 이번 세션의 대화 버퍼

    # ── 단기 (제공됨) ──
    def add_turn(self, role: str, content: str) -> None:
        self.turns.append({"role": role, "content": content})

    def recent(self, n: int = 6) -> list[dict]:
        return self.turns[-n:]

    # ── 장기 ──
    def remember(self, fact: str) -> None:
        """사실 하나를 장기 저장소에 **영구 저장**한다 (세션이 끝나도 남게).

        TODO(W10): 2~3줄.
          힌트: JSONL 한 줄 append — json.dumps({"fact": fact}, ensure_ascii=False)
          (self.path.parent.mkdir(parents=True, exist_ok=True) 로 폴더 보장)
        """
        raise NotImplementedError("TODO(W10): remember() 를 구현하세요")

    def recall(self, query: str, k: int = 2) -> list[str]:
        """저장된 사실 중 query와 관련된 것 k개를 회수한다.

        - 저장소가 없으면 빈 리스트.
        - W7 Retriever를 재사용: 사실들을 넣고 build → query.
          (사실이 k개 이하면 전부 반환해도 된다)

        TODO(W10): 6~9줄.
          힌트: facts = [json.loads(ln)["fact"] for ln in self.path.read_text().splitlines() if ln.strip()]
        """
        raise NotImplementedError("TODO(W10): recall() 를 구현하세요")
