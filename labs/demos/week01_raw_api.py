"""W1 데모 — 래퍼를 만들기 전에, 원시 HTTP 호출의 '내부'를 본다.

LLM API는 결국 JSON을 실어 나르는 HTTP POST 하나다.
이걸 눈으로 확인한 뒤에 aisuite로 감싼다 (같은 일을 한 줄로).
✅ W1 완료 기준: 원시 HTTP와 aisuite 래퍼(직접 채운 chat()) 양쪽으로 호출이 된다.

실행: python demos/week01_raw_api.py
(OPENAI_API_KEY 필요 — 없으면 aisuite 파트만 Ollama로 실행됨)
"""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
except ImportError:
    pass

QUESTION = "에이전트를 한 문장으로 정의해줘."


def raw_http_call():
    """1단계: requests 로 직접 POST — SDK 없이 API의 정체를 본다."""
    import requests

    key = os.getenv("OPENAI_API_KEY")
    if not key:
        print("(OPENAI_API_KEY 없음 — 원시 호출 데모는 건너뜀)\n")
        return

    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}"},
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": QUESTION}],
        },
        timeout=60,
    )
    body = resp.json()
    print("── 원시 응답 JSON (일부) ──")
    print(json.dumps(body, ensure_ascii=False, indent=2)[:800])
    print("\n→ 우리가 쓰는 건 결국 choices[0].message.content 하나:")
    print("   ", body["choices"][0]["message"]["content"])


def aisuite_call():
    """2단계: 같은 일을 aisuite로 — provider가 바뀌어도 이 코드는 그대로다."""
    from docqa import llm

    print("\n── aisuite 래퍼 (docqa/llm.py — 여러분이 채운 chat()) ──")
    print("모델:", llm.default_model())
    print(llm.ask(QUESTION))


if __name__ == "__main__":
    raw_http_call()
    aisuite_call()
