"""W15 — 통합: 연구보조 검색·종합 에이전트 완성본.

한 학기 부품을 전부 조립하고, 단순 파이프라인(베이스라인)과 비교한다.
실행: python app.py --docs data/sample_doc.txt [다른 txt들...]
      (질문 앞에 "baseline:" 을 붙이면 고정 파이프라인으로 답해 비교)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from docqa import guardrails, tools
from docqa.loop import react_loop
from docqa.retriever import Retriever


def build_corpus(paths: list[str]) -> Retriever:
    """텍스트 파일들을 읽어 검색기를 만든다. (제공됨)"""
    r = Retriever()
    for p in paths:
        r.add(Path(p).read_text(encoding="utf-8"))
    r.build()
    return r


def baseline_answer(question: str, retriever: Retriever, llm_fn=None) -> str:
    """베이스라인 = 고정 파이프라인: 무조건 검색 → 붙여넣기 → 1회 호출. (제공됨)

    W1의 정의 그대로 — LLM이 아무 제어 흐름도 결정하지 않는다.
    """
    if llm_fn is None:
        from docqa import llm
        llm_fn = lambda messages: llm.chat(messages, temperature=0.0)
    context = "\n---\n".join(retriever.query(question, k=3))
    prompt = f"다음 발췌만 근거로 답하라.\n\n{context}\n\n질문: {question}"
    return llm_fn([{"role": "user", "content": prompt}])


def agent_answer(question: str, retriever: Retriever, llm_fn=None) -> str:
    """에이전트 = 한 학기 부품의 조립.

    조립 순서 (전부 이미 만든 것들이다):
      1) tools.TOOLS.clear() 후 tools.register_defaults()      (W3)
      2) tools.register_search(retriever)                       (W6)
      3) guardrails.install()                                   (W14)
      4) react_loop(question, llm_fn=llm_fn) 반환               (W4)

    TODO(W15): 4~6줄. — 마지막 빈칸. 새 코드는 없다, 조립뿐.
    """
    raise NotImplementedError("TODO(W15): agent_answer() 를 구현하세요")


def main():
    ap = argparse.ArgumentParser(description="연구보조 에이전트")
    ap.add_argument("--docs", nargs="+", default=["data/sample_doc.txt"])
    args = ap.parse_args()
    retriever = build_corpus(args.docs)
    print(f"코퍼스 준비 완료: 청크 {len(retriever.chunks)}개. 질문하세요 (빈 줄 = 종료)")
    print("팁: 'baseline: <질문>' 으로 물으면 고정 파이프라인과 비교할 수 있다.\n")
    while True:
        try:
            q = input("Q> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not q:
            break
        if q.startswith("baseline:"):
            print("A(베이스라인)>", baseline_answer(q[len("baseline:"):].strip(), retriever))
        else:
            print("A(에이전트)>", agent_answer(q, retriever))


if __name__ == "__main__":
    main()
