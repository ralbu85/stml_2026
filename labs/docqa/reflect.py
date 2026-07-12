"""W6 — 자기반성 (실패 → 언어 피드백 → 재시도).

핵심 교훈(강의): 순진한 "다시 생각해봐"는 안 된다 — **외부 검증 신호**가
있을 때만 반성이 작동한다. 그래서 이 모듈은 verify_fn(검증기)을 요구한다.
"""

from __future__ import annotations

RETRY_PROMPT = """\
질문: {question}

이전 답: {answer}
검증 결과(피드백): {feedback}

피드백을 반영해 다시 답하라. 답만 간결히."""


def reflect_retry(question: str, answer_fn, verify_fn, max_retries: int = 3, verbose: bool = True):
    """답하고 → 검증하고 → 실패하면 피드백을 붙여 재시도한다.

    Args:
        answer_fn: (question, feedback_or_None, prev_answer_or_None) -> answer(str)
                   첫 시도는 feedback=None. 재시도부터 피드백·이전 답이 들어온다.
        verify_fn: (answer) -> (ok: bool, feedback: str)
                   테스트 통과 여부 같은 **외부 신호**. 자기비평보다 위계가 높다.
        max_retries: 재시도 예산. 소진하면 마지막 답을 그대로 반환 (언제 포기하나).

    Returns:
        (최종 답, 시도 횟수)

    TODO(W6): 8~11줄.
      1) answer_fn(question, None, None) 으로 첫 답.
      2) verify_fn 통과면 즉시 반환.
      3) 실패면 feedback·이전 답을 넣어 answer_fn 재호출 — 최대 max_retries번.
      4) 끝까지 실패해도 예외 대신 마지막 답 반환.
    """
    raise NotImplementedError("TODO(W6): reflect_retry() 를 구현하세요")


def llm_answer_fn(llm_fn=None):
    """LLM 기반 answer_fn을 만들어 준다. (제공됨 — 데모용)"""
    if llm_fn is None:
        from . import llm
        llm_fn = lambda messages: llm.chat(messages, temperature=0.0)

    def answer(question, feedback=None, prev_answer=None):
        if feedback is None:
            return llm_fn([{"role": "user", "content": question}])
        prompt = RETRY_PROMPT.format(question=question, answer=prev_answer, feedback=feedback)
        return llm_fn([{"role": "user", "content": prompt}])

    return answer
