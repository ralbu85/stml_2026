"""W3 데모 — 루프가 진짜 도구를 부른다.

실행: python demos/week03_tools.py "질문"
✅ W3 완료 기준: 루프가 계산기 도구를 실제로 호출해 답한다.

관전 포인트 두 가지:
1. 지난주 "(아직 도구가 없습니다)" Observation이 사라지고 진짜 계산 결과가 들어온다.
2. 일부러 이상한 질문을 던져 도구 오호출·에러가 나도 루프가 죽지 않는 것을 본다.
   (예: python demos/week03_tools.py "이 수업 평가 방식 알려줘"  ← text_search를 쓴다)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from docqa import tools
from docqa.loop import react_loop

if __name__ == "__main__":
    tools.register_defaults()
    question = sys.argv[1] if len(sys.argv) > 1 else "1400의 29%는 얼마야?"
    answer = react_loop(question, verbose=True)
    print(f"\n{'='*40}\n최종 답: {answer}")
