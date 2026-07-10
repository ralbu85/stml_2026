"""W2 데모 ② — 단일 답 vs self-consistency(N표 다수결) 비교.

실행: python demos/week02_selfconsistency.py "질문" [N]
✅ W2 완료 기준 ②: 애매한 질문에서 단일 답보다 다수결 정확도가 높다.

관전 포인트: 표 분포. 5표가 4:1로 갈리면 — 단일 호출이었다면
5번 중 1번은 틀린 답을 받았다는 뜻이다.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from collections import Counter

from docqa import llm
from docqa.reasoning import COT_PROMPT, extract_answer, normalize, self_consistency

if __name__ == "__main__":
    question = sys.argv[1] if len(sys.argv) > 1 else (
        "기차가 시속 60km로 30분 달린 뒤 시속 90km로 20분 달렸다. 총 이동 거리는 몇 km인가?"
    )
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    # 1) 단일 답 (temperature 0)
    single = extract_answer(llm.ask(COT_PROMPT.format(question=question), temperature=0.0))
    print(f"단일 답 (1표):      {single}")

    # 2) self-consistency (n표 다수결)
    best, answers = self_consistency(question, n=n)
    votes = Counter(normalize(a) for a in answers if a)
    print(f"다수결 답 ({n}표):   {best}")
    print(f"표 분포:            {dict(votes)}")
