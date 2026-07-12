"""W13 오프라인 테스트 — eval harness. 실행: pytest tests/test_week13.py -v"""

from eval.harness import grade, load_testset, run_eval

TESTSET = [
    {"q": "1+1은?", "keywords": ["2"]},
    {"q": "수도는?", "keywords": ["서울", "seoul"]},
    {"q": "어려운 질문", "keywords": ["불가능한답"]},
]


def test_grade_case_insensitive():
    assert grade("정답은 Seoul 입니다", ["서울", "seoul"])


def test_grade_ignores_commas():
    assert grade("총 16,464개입니다", ["16464"])


def test_grade_none_is_wrong():
    assert not grade("", ["2"]) and not grade(None, ["2"])


def test_run_eval_scores():
    answers = {"1+1은?": "2입니다", "수도는?": "서울", "어려운 질문": "모르겠다"}
    result = run_eval(lambda q: answers[q], TESTSET, verbose=False)
    assert result["n"] == 3 and result["correct"] == 2
    assert abs(result["accuracy"] - 2 / 3) < 1e-9
    assert result["failures"][0]["q"] == "어려운 질문"
    assert result["avg_latency_s"] >= 0


def test_run_eval_survives_agent_crash():
    def flaky(q):
        raise RuntimeError("에이전트 사망")
    result = run_eval(flaky, TESTSET[:2], verbose=False)
    assert result["n"] == 2 and result["correct"] == 0   # 죽지 않고 오답 처리


def test_default_testset_loads():
    ts = load_testset()
    assert len(ts) == 10 and all("q" in t and "keywords" in t for t in ts)
