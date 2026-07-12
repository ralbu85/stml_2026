"""W13 데모 — 내 에이전트 점수표 (에이전트 vs 베이스라인).

실행: python demos/week13_eval.py
✅ W13 완료 기준: 정확도·지연이 담긴 점수표가 출력된다.

W16 최종 발표에서 이 점수표로 방어한다. 숫자 없이는 주장도 없다.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import agent_answer, baseline_answer, build_corpus
from eval.harness import load_testset, report, run_eval

if __name__ == "__main__":
    docs = sys.argv[1:] or [str(Path(__file__).resolve().parents[1] / "data" / "sample_doc.txt")]
    retriever = build_corpus(docs)
    testset = load_testset()

    print("── 에이전트 ──")
    print(report(run_eval(lambda q: agent_answer(q, retriever), testset)))
    print("\n── 베이스라인(고정 파이프라인) ──")
    print(report(run_eval(lambda q: baseline_answer(q, retriever), testset)))
