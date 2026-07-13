"""W2 — Self-consistency (Wang et al., 2022).

같은 질문을 temperature>0 으로 N번 샘플링해 **서로 다른 추론 경로**를 얻고,
최종 답만 뽑아 **다수결**한다. 추론 경로는 달라도 옳은 답은 한 점으로 모인다.
"""

from __future__ import annotations

from collections import Counter
import re

COT_PROMPT = """\
다음 질문에 단계적으로 추론한 뒤, 마지막 줄에 반드시 "Final Answer: <답>" 형식으로 답하라.
답은 최대한 짧게(숫자면 숫자만, 이름이면 이름만) 쓴다.

Question: {question}"""


def extract_answer(text: str) -> str | None:
    """모델 출력에서 최종 답만 뽑는다. (제공됨)

    "Final Answer:" 가 있으면 그 뒤, 없으면 마지막 비어있지 않은 줄.
    """
    m = re.search(r"Final Answer:\s*(.+)", text, re.S | re.I)
    if m:
        return m.group(1).strip().splitlines()[0].strip()
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return lines[-1] if lines else None


def normalize(answer: str) -> str:
    """표기 차이로 표가 갈리지 않게 정규화한다. (제공됨)

    소문자화 · 앞뒤 공백 제거 · 끝 문장부호 제거 · 연속 공백 1칸으로.
    """
    ans = answer.strip().lower().rstrip(".!?")
    return re.sub(r"\s+", " ", ans)


def majority_vote(answers: list[str | None]) -> str | None:
    """답 목록에서 최다 득표 답을 돌려준다.

    - None(추출 실패)은 표에서 제외한다.
    - normalize() 를 거친 뒤 센다.
    - 동률이면 먼저 나온 답이 이긴다. 유효 표가 없으면 None.

    TODO(W2): 4~6줄. 힌트: collections.Counter 와 .most_common(1).
      (Counter 는 동률일 때 먼저 들어온 키를 앞에 준다.)
    """
    raise NotImplementedError("TODO(W2): majority_vote() 를 구현하세요")


def self_consistency(question: str, n: int = 5, llm_fn=None, temperature: float = 0.8):
    """같은 질문을 n번 샘플링해 다수결 답을 낸다.

    llm_fn: (messages, temperature) -> str.  None이면 docqa.llm.chat 사용.
            테스트에서는 가짜 함수를 주입한다.

    Returns:
        (다수결 답, 전체 답 리스트) — 리스트는 표 분포를 보여주는 데 쓴다.

    TODO(W2): 6~9줄.
      1) llm_fn 이 None 이면:
         from . import llm
         llm_fn = lambda messages, temperature: llm.chat(messages, temperature=temperature)
      2) n번 반복: COT_PROMPT.format(question=...) 을 user 메시지로 보내고
         extract_answer() 로 답을 뽑아 리스트에 모은다. (temperature 를 그대로 전달!)
      3) (majority_vote(리스트), 리스트) 반환.
    """
    raise NotImplementedError("TODO(W2): self_consistency() 를 구현하세요")
