"""W4 데모 — 첫 완전한 에이전트: 루프가 도구를 반복 호출한다.

실행: python demos/week04_react.py "질문"
      python demos/week04_react.py --eval        # 미니 evalset 5문항 채점
✅ W4 완료 기준: 루프가 계산기 도구를 실제로 호출해 답하고, 미니 evalset 결과가 기록된다.

관전 포인트:
1. W3의 단발 왕복이 while 루프가 되면서 다단계 질문이 풀린다.
2. 일부러 이상한 질문을 던져 도구 오호출·에러가 나도 루프가 죽지 않는 것을 본다.
   (예: python demos/week04_react.py "이 수업 평가 방식 알려줘"  ← text_search를 쓴다)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from docqa import tools
from docqa.loop import react_loop

# 미니 evalset: (질문, 정답에 포함되어야 할 문자열). W13에서 eval/harness.py로 정식화한다.
MINI_EVALSET = [
    ("1400의 29%는 얼마야?", "406"),
    ("12 곱하기 34는?", "408"),
    ("2의 10제곱은?", "1024"),
    ("100을 7로 나눈 나머지는?", "2"),
    ("(3+5)*(10-4)는?", "48"),
]


def run_mini_eval() -> None:
    passed = 0
    for question, expected in MINI_EVALSET:
        answer = react_loop(question, verbose=False)
        ok = expected in answer
        passed += ok
        print(f"[{'PASS' if ok else 'FAIL'}] {question} → {answer}")
    print(f"\n점수: {passed}/{len(MINI_EVALSET)}")


if __name__ == "__main__":
    tools.register_defaults()
    if len(sys.argv) > 1 and sys.argv[1] == "--eval":
        run_mini_eval()
    else:
        question = sys.argv[1] if len(sys.argv) > 1 else "1400의 29%는 얼마야?"
        answer = react_loop(question, verbose=True)
        print(f"\n{'='*40}\n최종 답: {answer}")
