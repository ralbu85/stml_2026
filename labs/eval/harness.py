"""W13 — 평가 하네스: 내 에이전트의 점수표.

"비싼 모델로 바꿨더니 좋아진 *느낌*" 금지 — 측정이 근거다 (W3·W13 강의).
정확도만이 아니라 **비용(호출 수)·지연**까지 잰다. W16 최종 발표에서
이 점수표로 자기 에이전트를 방어한다.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

DEFAULT_TESTSET = Path(__file__).resolve().parent / "testset.jsonl"


def load_testset(path=None) -> list[dict]:
    """{"q": 질문, "keywords": [정답에 들어야 할 키워드...]} 목록. (제공됨)"""
    p = Path(path) if path else DEFAULT_TESTSET
    return [json.loads(ln) for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]


def grade(answer: str, keywords: list[str]) -> bool:
    """답이 맞았나 — 키워드 중 **하나라도** 답 안에 있으면 정답.

    - 대소문자 무시, 답의 쉼표(1,000 표기)는 제거 후 비교.
    - answer가 None/빈 문자열이면 오답.

    TODO(W13): 3~5줄.
    """
    raise NotImplementedError("TODO(W13): grade() 를 구현하세요")


def run_eval(agent_fn, testset: list[dict], verbose: bool = True) -> dict:
    """전 문항을 돌려 점수표를 만든다.

    agent_fn: (질문 str) -> 답 str.  (진짜 에이전트든 베이스라인이든 동일 취급)

    Returns dict:
      n, correct, accuracy(0~1), avg_latency_s, failures(list of {"q","got"})

    TODO(W13): 10~14줄.
      힌트: time.perf_counter()로 문항별 지연 측정. 예외가 나면 그 문항은
      오답 처리하고 계속 진행 (평가 하네스는 죽지 않는다 — W4의 교훈).
    """
    raise NotImplementedError("TODO(W13): run_eval() 을 구현하세요")


def report(result: dict) -> str:
    """점수표를 사람이 읽을 표로. (제공됨)"""
    lines = [
        "─── 내 에이전트 점수표 ───",
        f"정확도   : {result['correct']}/{result['n']} = {result['accuracy']:.0%}",
        f"평균 지연: {result['avg_latency_s']:.2f}s/문항",
    ]
    for f in result["failures"]:
        lines.append(f"  ✗ {f['q'][:40]} → {str(f['got'])[:40]}")
    return "\n".join(lines)
