"""W7 — 계획 분해 (plan-and-execute).

질문을 하위 단계 리스트로 분해하고(계획), 단계를 순서대로 실행한다(실행).
ReAct(한 발씩)와 달리 계획을 먼저 다 세운다 — ReWOO의 아이디어.
"""

from __future__ import annotations

import re

PLAN_PROMPT = """\
다음 질문에 답하기 위한 단계를 2~4개로 나눠, 번호 목록으로만 답하라.
각 단계는 한 문장. 마지막 단계는 반드시 "앞 결과를 종합해 최종 답을 쓴다"류여야 한다.

Question: {question}"""

STEP_PROMPT = """\
원래 질문: {question}

지금까지 단계별 결과:
{notes}

이번 단계: {step}
이 단계만 수행하고 결과를 간결히 답하라."""


def parse_steps(text: str) -> list[str]:
    """번호 목록 텍스트에서 단계 리스트를 뽑는다.

    "1. ..." / "2) ..." 형식 모두 허용. 번호 목록이 하나도 없으면
    전체 텍스트를 단계 1개짜리 계획으로 취급한다.

    TODO(W7): 3~5줄. 힌트: re.findall(r"^\\s*\\d+[.)]\\s*(.+)$", text, re.M)
    """
    raise NotImplementedError("TODO(W7): parse_steps() 를 구현하세요")


def make_plan(question: str, llm_fn=None) -> list[str]:
    """질문 → 단계 리스트. (제공됨)"""
    if llm_fn is None:
        from . import llm
        llm_fn = lambda messages: llm.chat(messages, temperature=0.0)
    out = llm_fn([{"role": "user", "content": PLAN_PROMPT.format(question=question)}])
    return parse_steps(out)


def run_plan(question: str, plan: list[str] | None = None, llm_fn=None, verbose: bool = True) -> str:
    """계획을 단계 순서대로 실행하고 마지막 단계의 출력을 반환한다.

    - plan이 None이면 make_plan()으로 만든다.
    - 각 단계 실행 시 STEP_PROMPT에 **지금까지의 결과(notes)** 를 넣어 전달한다.
      (앞 단계 결과가 뒤 단계의 재료 — 이게 없으면 계획이 무의미)
    - notes 형식 예: "1. <step>: <result>" 줄들의 누적.

    TODO(W7): 7~10줄.
    """
    raise NotImplementedError("TODO(W7): run_plan() 을 구현하세요")
