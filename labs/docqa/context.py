"""W9 — 컨텍스트 예산 관리 (컨텍스트는 유한 자원이다).

검색이 잘될수록 청크가 넘친다. 예산 안에서 ①중요한 것을 고르고
②모델이 잘 보는 위치에 배치한다 (Lost-in-the-Middle: 중간은 잘 안 읽힌다).
"""

from __future__ import annotations


def count_tokens(text: str) -> int:
    """근사 토큰 수. (제공됨 — 한글 혼용 기준 대략 문자 수 / 2.5)

    실전은 tiktoken 등 정확한 카운터를 쓴다. 여기선 결정적 근사면 충분.
    """
    return max(1, int(len(text) / 2.5))


def fit_budget(scored_chunks: list[tuple[str, float]], budget: int) -> list[str]:
    """점수 달린 청크들을 토큰 예산 안에 맞춘다.

    규칙:
      1) **선별**: 점수 내림차순으로 훑으며, 예산이 남는 동안만 채택한다.
         (청크 하나가 예산을 넘기면 건너뛰고 다음 후보를 본다)
      2) **정렬**: 채택된 청크는 **점수 순으로 재배열해 반환** — 가장 중요한 것이
         맨 앞·맨 뒤(양끝)에 오도록: [1등, 3등, 5등, ..., 4등, 2등]
         (Lost-in-the-Middle 대비 — 중간엔 덜 중요한 것)

    Returns: 배치 순서의 청크 리스트.

    TODO(W9): 10~14줄.
      힌트: 선별 후 [::2] 는 앞쪽에 그대로, [1::2] 는 뒤집어 뒤쪽에.
    """
    raise NotImplementedError("TODO(W9): fit_budget() 을 구현하세요")


def audit(scored_chunks: list[tuple[str, float]], budget: int) -> str:
    """컨텍스트 감사 리포트 — 뭐가 몇 토큰 먹는지, 뭘 버렸는지. (제공됨)"""
    total = sum(count_tokens(c) for c, _ in scored_chunks)
    kept = fit_budget(scored_chunks, budget)
    used = sum(count_tokens(c) for c in kept)
    return (f"후보 {len(scored_chunks)}개({total}tok) → "
            f"채택 {len(kept)}개({used}tok) / 예산 {budget}tok")
