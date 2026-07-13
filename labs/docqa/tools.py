"""W3 — 도구 레지스트리·실행.

스키마 제공 → 호출 의도 출력 → 파싱 → 실행 → 결과 재주입의 단발 왕복을
오늘 완성한다. 다음 주(W4)의 ReAct 루프가 이 레지스트리를 반복 호출한다.
레지스트리는 dict 하나다 — 이름 → (함수, 설명).

설계 대원칙 (강의 '현장 노트'):
    **에러도 Observation이다.** 도구가 무슨 짓을 해도 루프는 죽지 않는다.
    없는 도구·깨진 인자·실행 예외 전부 *문자열*로 모델에게 돌려주고,
    모델이 그걸 읽고 다음 수(재시도·다른 도구·포기)를 정하게 한다.
"""

from __future__ import annotations

import ast
import operator
from pathlib import Path

TOOLS: dict = {}          # name -> {"fn": callable, "description": str}
OBS_MAX_CHARS = 500       # 관찰이 컨텍스트를 삼키지 않게 자른다 (W9 복선)


def register(name: str, description: str, fn) -> None:
    """도구를 레지스트리에 등록한다. (제공됨)

    description은 모델이 읽는다 — '언제 쓰나/안 쓰나'까지 적을 것.
    """
    TOOLS[name] = {"fn": fn, "description": description}


def tool_list_prompt() -> str:
    """시스템 프롬프트에 붙일 도구 목록 텍스트. (제공됨)"""
    lines = [f"- {name}: {spec['description']}" for name, spec in TOOLS.items()]
    return "사용 가능한 도구:\n" + "\n".join(lines)


def run_tool(name: str, tool_input: str) -> str:
    """도구를 실행하고 결과를 **문자열 관찰**로 돌려준다.

    규칙 (전부 문자열 반환 — 절대 예외를 밖으로 던지지 않는다):
      1) 없는 도구  → "(등록되지 않은 도구 '<name>'. 사용 가능: a, b, ...)"
      2) 실행 예외  → "(도구 '<name>' 실행 오류: <예외 메시지>)"
      3) 정상 결과  → str(결과), 단 OBS_MAX_CHARS 넘으면 자르고 " ...(잘림)" 붙임

    TODO(W3): 8~12줄.
      힌트: TOOLS[name]["fn"](tool_input) 을 try/except Exception 으로 감싼다.
    """
    raise NotImplementedError("TODO(W3): run_tool() 을 구현하세요")


# ── 기본 도구 1: 계산기 ─────────────────────────────────────

_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub,
    ast.Mult: operator.mul, ast.Div: operator.truediv,
    ast.Mod: operator.mod, ast.Pow: operator.pow,
    ast.USub: operator.neg, ast.UAdd: operator.pos,
}


def _safe_eval(expression: str):
    """산술식만 허용하는 안전한 평가기. (제공됨 — eval()을 쓰면 안 되는 이유는 W14에서)"""

    def walk(node):
        if isinstance(node, ast.Expression):
            return walk(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](walk(node.left), walk(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](walk(node.operand))
        raise ValueError(f"허용되지 않는 식: {ast.dump(node)[:50]}")

    return walk(ast.parse(expression.strip(), mode="eval"))


def calculator(expression: str) -> str:
    """산술식을 계산해 문자열로 돌려준다.

    - _safe_eval() 로 계산한다 (제공된 안전 평가기 — 숫자·사칙연산·%·** 만 허용).
    - 결과가 정수값이면 "406", 아니면 소수로 "0.2857142857142857" 처럼 str로.
      (힌트: float인데 .is_integer() 면 int로 바꿔서 str)
    - 잘못된 식이면 예외가 나는데, 잡지 마라 — run_tool() 이 관찰로 바꿔준다.

    TODO(W3): 3~5줄.
    """
    raise NotImplementedError("TODO(W3): calculator() 를 구현하세요")


# ── 기본 도구 2: 문서 검색 (원시적 — W5에서 임베딩으로 대체) ──

_DOC_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_doc.txt"


def text_search(query: str) -> str:
    """샘플 문서에서 query가 포함된 줄을 찾는다 (최대 3줄). (제공됨)

    단순 부분 문자열 매칭 — 동의어·의미 검색이 안 되는 게 보이면 성공.
    그 갈증이 W5(임베딩 검색)의 동기가 된다.
    """
    query = query.strip()
    if not query:
        return "(빈 검색어)"
    lines = _DOC_PATH.read_text(encoding="utf-8").splitlines()
    hits = [ln.strip() for ln in lines if query.lower() in ln.lower()][:3]
    return "\n".join(hits) if hits else f"(문서에서 '{query}'를 찾지 못함)"


# ── W6: 검색을 도구로 — 두 모듈(retriever·tools)이 처음 만난다 ──

def register_search(retriever) -> None:
    """W5의 Retriever를 'search_papers' 도구로 등록한다.

    이걸로 "매번 검색"(워크플로우)이 "필요할 때만 검색"(에이전트)이 된다 —
    W1 미니체크 3번의 답. 검색할지 말지는 이제 모델이 description을 읽고 정한다.

    TODO(W6): 4~7줄.
      1) fn: 질문 문자열 → retriever.query(q, k=3) 결과를 "\\n---\\n"으로 join.
      2) register("search_papers", <설명>, fn).
         설명에는 반드시 "언제 쓰나"(수업 논문 내용 질문)와
         "언제 안 쓰나"(일반 상식·계산에는 사용 금지)를 둘 다 적어라 — W3 체크리스트.
    """
    raise NotImplementedError("TODO(W6): register_search() 를 구현하세요")


def register_defaults() -> None:
    """기본 도구 2종을 등록한다. (제공됨 — 데모·실전에서 호출)"""
    register(
        "calculator",
        "산술식을 계산한다. 예: '1400*0.29'. 수식 계산이 필요할 때만 사용.",
        calculator,
    )
    register(
        "text_search",
        "강의 소개 문서에서 키워드가 든 줄을 찾는다. 이 수업에 관한 질문에만 사용.",
        text_search,
    )
