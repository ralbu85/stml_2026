"""W8 데모 — 검색이 도구가 되는 순간.

실행: python demos/week08_search.py "ReAct는 어디서 평가됐어?"
✅ W8 완료 기준: 상식 질문은 검색 안 하고, 논문 질문만 검색한다.

관전 포인트: 같은 루프에 질문 두 개를 던져 보라 —
  "3 더하기 4는?"          → calculator만 (검색 안 함)
  "이 수업 평가 방식은?"    → search_papers 호출
검색할지 말지를 모델이 정한다 (W1 미니체크 3번의 답).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from docqa import tools
from docqa.loop import react_loop
from docqa.retriever import Retriever

if __name__ == "__main__":
    r = Retriever()
    r.add((Path(__file__).resolve().parents[1] / "data" / "sample_doc.txt").read_text(encoding="utf-8"))
    r.build()
    tools.register_defaults()
    tools.register_search(r)
    question = sys.argv[1] if len(sys.argv) > 1 else "이 수업의 평가 방식은?"
    answer = react_loop(question, verbose=True)
    print(f"\n{'='*40}\n최종 답: {answer}")
