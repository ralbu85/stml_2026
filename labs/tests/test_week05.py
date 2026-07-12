"""W5 오프라인 테스트 — planner. 실행: pytest tests/test_week05.py -v"""

from docqa.planner import parse_steps, run_plan


def test_parse_numbered_dots():
    assert parse_steps("1. 검색한다\n2. 종합한다") == ["검색한다", "종합한다"]


def test_parse_numbered_parens_and_indent():
    assert parse_steps("  1) A\n  2) B\n  3) C") == ["A", "B", "C"]


def test_parse_fallback_whole_text():
    assert parse_steps("그냥 바로 답한다") == ["그냥 바로 답한다"]


def test_run_plan_returns_last_step_output():
    plan = ["ReAct 논문의 벤치마크를 찾는다", "종합해 최종 답을 쓴다"]
    outs = iter(["HotpotQA와 ALFWorld", "최종: HotpotQA·ALFWorld에서 평가했다"])
    fake_llm = lambda messages: next(outs)
    result = run_plan("ReAct는 어디서 평가됐나?", plan=plan, llm_fn=fake_llm, verbose=False)
    assert result == "최종: HotpotQA·ALFWorld에서 평가했다"


def test_run_plan_passes_notes_forward():
    """2번째 단계 프롬프트에 1번째 단계의 결과가 들어 있어야 한다."""
    plan = ["단계A", "단계B"]
    prompts = []

    def fake_llm(messages):
        prompts.append(messages[-1]["content"])
        return f"결과{len(prompts)}"

    run_plan("q", plan=plan, llm_fn=fake_llm, verbose=False)
    assert "결과1" in prompts[1]  # 앞 결과가 뒤 단계의 재료
