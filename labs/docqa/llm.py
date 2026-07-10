"""W1 — LLM 호출 래퍼.

aisuite(Andrew Ng)의 **Chat Completions 계층만** 사용한다.
aisuite의 Agents/tools 레이어는 쓰지 않는다 — 그건 W3에서 우리가 직접 만든다.

모델은 "provider:model" 문자열 하나로 교체된다:
    openai:gpt-4o-mini · anthropic:claude-haiku-4-5 · ollama:llama3.2
"""

from __future__ import annotations

import os

_client = None


def _get_client():
    """aisuite Client를 1회만 생성해 재사용한다. (제공됨)"""
    global _client
    if _client is None:
        try:  # .env 가 있으면 읽는다 (없어도 동작)
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass
        import aisuite as ai
        _client = ai.Client()
    return _client


def default_model() -> str:
    """(제공됨) .env 의 DOCQA_MODEL, 없으면 openai:gpt-4o-mini."""
    return os.getenv("DOCQA_MODEL", "openai:gpt-4o-mini")


def chat(messages, model=None, temperature=0.0, **kwargs) -> str:
    """대화 이력을 보내고 응답 **텍스트**를 돌려받는다.

    Args:
        messages: [{"role": "system"|"user"|"assistant", "content": str}, ...]
        model: "provider:model" 문자열. None이면 default_model().
        temperature: 0.0이면 결정적에 가깝게, 높이면 다양하게 (W2에서 사용).

    Returns:
        응답 본문 문자열 (choices[0].message.content).

    TODO(W1): 3~5줄.
      1) _get_client() 로 클라이언트를 얻는다.
      2) client.chat.completions.create(model=..., messages=..., temperature=..., **kwargs) 호출.
         (model이 None이면 default_model() 사용)
      3) 첫 번째 choice의 message.content 를 반환.
    """
    raise NotImplementedError("TODO(W1): chat() 을 구현하세요")


def ask(prompt: str, system: str | None = None, **kwargs) -> str:
    """단일 질문 편의 함수 — chat()을 감싼다. (제공됨)"""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    return chat(messages, **kwargs)
