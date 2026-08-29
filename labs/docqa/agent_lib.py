"""docqa 에이전트 공용 라이브러리 — 제공 코드(학생은 수정하지 않는다).

실습에서 학생이 채우는 것은 노트북 셀의 **프롬프트와 흐름 조립**이다.
LLM 호출·답 추출·다수결 채점 같은 배관은 모두 여기에 제공된다.

모델 교체: 환경변수 DOCQA_MODEL 문자열 하나로.
    openai:gpt-4o-mini · anthropic:claude-haiku-4-5 · ollama:llama3.2(로컬·무료)
배관 출처: aisuite(Andrew Ng)의 Chat Completions 계층.
"""

from __future__ import annotations

import json
import os
import re
from collections import Counter
from pathlib import Path

_client = None


def _get_client():
    global _client
    if _client is None:
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass
        import aisuite
        _client = aisuite.Client()
    return _client


def default_model() -> str:
    return os.getenv("DOCQA_MODEL", "openai:gpt-4o-mini")


# ── LLM 호출 ─────────────────────────────────────────────────

def chat(messages: list[dict], model: str | None = None,
         temperature: float = 0.0, **kwargs) -> str:
    """대화 메시지 목록을 보내고 응답 텍스트를 돌려준다.

    messages: [{"role": "system"|"user"|"assistant", "content": str}, ...]
    temperature: 0이면 결정적에 가깝고, 높이면 표집이 다양해진다(W3에서 사용).
    """
    resp = _get_client().chat.completions.create(
        model=model or default_model(), messages=messages,
        temperature=temperature, **kwargs)
    return resp.choices[0].message.content


def ask(prompt: str, system: str | None = None, **kwargs) -> str:
    """단일 질문 편의 함수 — chat()을 감싼다."""
    messages = [{"role": "system", "content": system}] if system else []
    messages.append({"role": "user", "content": prompt})
    return chat(messages, **kwargs)


# ── 답 추출·채점 ─────────────────────────────────────────────

def extract_answer(text: str) -> str | None:
    """모델 출력에서 최종 답만 뽑는다.

    "Final Answer:" 가 있으면 그 뒤 한 줄, 없으면 마지막 비어 있지 않은 줄.
    """
    m = re.search(r"Final Answer:\s*(.+)", text, re.I | re.S)
    if m:
        return m.group(1).strip().splitlines()[0].strip()
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return lines[-1] if lines else None


def normalize(answer: str) -> str:
    """표기 차이로 채점·집계가 갈리지 않게 정규화한다(소문자·공백·끝부호 정리)."""
    return re.sub(r"\s+", " ", answer.strip().lower().rstrip(".!?"))


def contains_answer(output: str, gold: str) -> bool:
    """정규화한 정답 문자열이 출력 안에 들어 있으면 정답으로 친다."""
    return normalize(gold) in normalize(output)


def majority_vote(answers: list[str | None]) -> str | None:
    """답 목록에서 최다 득표 답을 돌려준다.

    None(추출 실패)은 제외하고, normalize 후 센다. 동률이면 먼저 나온 답.
    """
    valid = [normalize(a) for a in answers if a]
    return Counter(valid).most_common(1)[0][0] if valid else None


# ── 평가 세트 ────────────────────────────────────────────────

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def load_evalset(name: str) -> list[dict]:
    """labs/data/<name> 의 JSONL 평가 문항을 읽는다. 각 줄: {"question", "answer"}."""
    path = DATA_DIR / name
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def accuracy(answer_fn, evalset: list[dict], verbose: bool = True) -> float:
    """answer_fn(question)->str 을 evalset 전체에 돌려 정답률을 잰다."""
    correct = 0
    for item in evalset:
        out = answer_fn(item["question"])
        ok = contains_answer(out, item["answer"])
        correct += ok
        if verbose:
            print(("✅" if ok else "❌"), item["question"][:45], "→", extract_answer(out))
    return correct / len(evalset) if evalset else 0.0


# ═══════════════════════════════════════════════════════════════
# W4–W10 배관 (제공 코드 — 학생은 프롬프트·흐름만 다룬다)
# ═══════════════════════════════════════════════════════════════

# ── 검색 도구 (W4·W9) : aisuite tools= 에 그대로 넘길 수 있다 ──
from .research_tools import arxiv_search_tool, wikipedia_search_tool  # noqa: E402


def run_with_tools(prompt: str, tools: list, system: str | None = None,
                   model: str | None = None, max_turns: int = 5) -> str:
    """도구 목록을 넘기면 aisuite가 호출·실행·재주입을 자동으로 반복한다(W4·W6).

    학생은 도구 함수와 프롬프트만 주고, 파싱·실행 배관은 여기에 맡긴다.
    """
    messages = [{"role": "system", "content": system}] if system else []
    messages.append({"role": "user", "content": prompt})
    resp = _get_client().chat.completions.create(
        model=model or default_model(), messages=messages,
        tools=tools, max_turns=max_turns, temperature=0.0)
    return resp.choices[0].message.content or ""


# ── 검색기 (W9) : 청킹·임베딩·코사인은 전부 여기 감춘다 ─────────
def _chunk(text: str, size: int = 500, overlap: int = 100) -> list[str]:
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    pieces = []
    for p in paras:
        if len(p) <= size:
            pieces.append(p)
        else:
            pieces += [p[i:i + size] for i in range(0, len(p), size - overlap)]
    chunks, cur = [], ""
    for p in pieces:
        if cur and len(cur) + len(p) + 2 > size:
            chunks.append(cur); cur = p
        else:
            cur = f"{cur}\n\n{p}" if cur else p
    if cur:
        chunks.append(cur)
    return chunks


def _embed(texts: list[str]):
    """OPENAI_API_KEY가 있으면 임베딩 API, 없으면 결정적 해시 임베딩(단어 겹침)."""
    import numpy as np
    if os.getenv("OPENAI_API_KEY"):
        from openai import OpenAI
        data = OpenAI().embeddings.create(model="text-embedding-3-small", input=texts).data
        arr = np.array([d.embedding for d in data], dtype="float32")
    else:
        import hashlib
        arr = np.zeros((len(texts), 512), dtype="float32")
        for i, t in enumerate(texts):
            for w in re.findall(r"[\w가-힣]+", t.lower()):
                arr[i, int(hashlib.md5(w.encode()).hexdigest(), 16) % 512] += 1.0
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    return arr / np.maximum(norms, 1e-8)


class Retriever:
    """문서를 색인하고 코사인 유사도 top-k로 검색한다(W9·W10 제공 부품)."""

    def __init__(self):
        self.chunks: list[str] = []
        self._vecs = None

    def index(self, documents: list[str]) -> int:
        self.chunks = [c for doc in documents for c in _chunk(doc)]
        self._vecs = _embed(self.chunks) if self.chunks else None
        return len(self.chunks)

    def search(self, query: str, k: int = 3) -> list[str]:
        if self._vecs is None:
            return []
        import numpy as np
        scores = self._vecs @ _embed([query])[0]
        return [self.chunks[i] for i in np.argsort(scores)[::-1][:k]]


# ── 메모리 (W10) : 저장은 append, 반입은 검색 ───────────────────
class Memory:
    """세션을 넘는 장기 메모리 — 저장한 사실을 검색으로 반입한다(W10 제공 부품)."""

    def __init__(self):
        self.facts: list[str] = []
        self._r = Retriever()
        self._dirty = False

    def remember(self, fact: str) -> None:
        self.facts.append(fact); self._dirty = True

    def recall(self, query: str, k: int = 3) -> list[str]:
        if not self.facts:
            return []
        if self._dirty:
            self._r.index(self.facts); self._dirty = False
        return self._r.search(query, k)


# ── 컨텍스트 예산 조립 (W10) ─────────────────────────────────
def est_tokens(text: str) -> int:
    """문자 수로 토큰 수를 근사한다(4자≈1토큰)."""
    return max(1, len(text) // 4)


def assemble_context(system: str, history: list, evidence: list[str],
                     question: str, budget_tokens: int) -> list[dict]:
    """예산 안에서 컨텍스트를 조립한다 — 고정부는 앞, 질문·근거는 끝, 오래된 이력부터 절단."""
    tail = "\n".join(f"[근거] {e}" for e in evidence) + f"\n질문: {question}"
    remaining = budget_tokens - est_tokens(system) - est_tokens(tail)
    kept = []
    for role, content in reversed(history):
        if est_tokens(content) > remaining:
            break
        kept.append((role, content)); remaining -= est_tokens(content)
    kept.reverse()
    return ([{"role": "system", "content": system}]
            + [{"role": r, "content": c} for r, c in kept]
            + [{"role": "user", "content": tail}])


# ── 계산 배관 (W6 도구 예시) : 학생은 도구의 '설명'만 쓴다 ──────
import ast as _ast  # noqa: E402
import operator as _op  # noqa: E402
_OPS = {_ast.Add: _op.add, _ast.Sub: _op.sub, _ast.Mult: _op.mul,
        _ast.Div: _op.truediv, _ast.Pow: _op.pow, _ast.USub: _op.neg}


def safe_calc(expression: str) -> str:
    """산술식 문자열을 안전하게 계산한다(eval 없이 AST로). W6 도구의 실행 배관."""
    def ev(n):
        if isinstance(n, _ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, _ast.BinOp) and type(n.op) in _OPS:
            return _OPS[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, _ast.UnaryOp) and type(n.op) in _OPS:
            return _OPS[type(n.op)](ev(n.operand))
        raise ValueError("허용되지 않은 식")
    return str(ev(_ast.parse(expression, mode="eval").body))
