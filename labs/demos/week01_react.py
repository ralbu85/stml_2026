"""W1 데모 ② — ReAct 루프를 진짜 LLM으로 돌려 본다.

실행: python demos/week01_react.py "질문"
✅ W1 완료 기준: 간단한 질문에 루프가 한 바퀴 돌아 Final Answer를 낸다.

관전 포인트: 도구가 아직 없어서 Action을 시도하면 하네스가
"도구 없음" Observation을 돌려주고, 모델이 스스로 Final Answer로 전환한다.
이 빈자리를 W3의 tools.py가 채운다.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from docqa.loop import react_loop

if __name__ == "__main__":
    question = sys.argv[1] if len(sys.argv) > 1 else "1400의 29%는 얼마야?"
    answer = react_loop(question, verbose=True)
    print(f"\n{'='*40}\n최종 답: {answer}")
