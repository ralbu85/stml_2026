"""W6 오프라인 테스트 — reflect. 실행: pytest tests/test_week06.py -v"""

from docqa.reflect import reflect_retry


def _verify_equals(expected):
    def verify(answer):
        ok = answer.strip() == expected
        return ok, "" if ok else f"오답. 기대값과 다르다 (힌트: 숫자만 답하라)"
    return verify


def test_pass_on_first_try():
    answer_fn = lambda q, fb, prev: "42"
    ans, attempts = reflect_retry("q", answer_fn, _verify_equals("42"), verbose=False)
    assert ans == "42" and attempts == 1


def test_retry_with_feedback_fixes_answer():
    def answer_fn(q, feedback, prev):
        return "정답은 42입니다" if feedback is None else "42"  # 피드백 받으면 형식 교정
    ans, attempts = reflect_retry("q", answer_fn, _verify_equals("42"), verbose=False)
    assert ans == "42" and attempts == 2


def test_feedback_and_prev_answer_are_passed():
    seen = []

    def answer_fn(q, feedback, prev):
        seen.append((feedback, prev))
        return "wrong"

    reflect_retry("q", answer_fn, _verify_equals("42"), max_retries=2, verbose=False)
    assert seen[0] == (None, None)          # 첫 시도
    assert seen[1][0] and seen[1][1] == "wrong"  # 재시도엔 피드백+이전 답


def test_gives_up_after_budget():
    calls = []
    answer_fn = lambda q, fb, prev: (calls.append(1), "wrong")[1]
    ans, attempts = reflect_retry("q", answer_fn, _verify_equals("42"), max_retries=3, verbose=False)
    assert ans == "wrong"                    # 예외 없이 마지막 답 반환
    assert len(calls) == 4                   # 첫 시도 1 + 재시도 3
