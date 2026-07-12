"""W9 오프라인 테스트 — context. 실행: pytest tests/test_week09.py -v"""

from docqa.context import count_tokens, fit_budget

# 청크 하나 ≈ 40토큰 (100자 / 2.5)
A = ("가" * 100, 0.9)   # 1등
B = ("나" * 100, 0.7)   # 2등
C = ("다" * 100, 0.5)   # 3등
D = ("라" * 100, 0.3)   # 4등


def test_respects_budget():
    kept = fit_budget([A, B, C, D], budget=90)   # 2개까지만 들어감
    assert len(kept) == 2
    assert sum(count_tokens(c) for c in kept) <= 90


def test_selects_by_score():
    kept = fit_budget([D, B, A, C], budget=90)   # 입력 순서와 무관하게 점수로
    assert set(kept) == {A[0], B[0]}


def test_important_at_both_ends():
    """양끝 배치: [1등, 3등, ..., 4등, 2등] — 중간에 덜 중요한 것."""
    kept = fit_budget([A, B, C, D], budget=1000)  # 전부 채택
    assert kept[0] == A[0] and kept[-1] == B[0]
    assert kept == [A[0], C[0], D[0], B[0]]


def test_skips_oversized_chunk():
    big = ("바" * 1000, 0.99)                     # 400tok — 예산 초과
    kept = fit_budget([big, A], budget=100)
    assert kept == [A[0]]                          # 건너뛰고 다음 후보
