# Week 01. 에이전트란 무엇인가 — 추론과 행동의 결합

> **Part:** 에이전트 기초 · 난이도: 🟢 기초 · 🟡 중급 · 🔴 심화 · [📋 발표 가이드](../docs/presentation-guide.md)

## 📖 보조읽기 (발표 대상 아님)
Anthropic — *Building Effective Agents* (워크플로우 vs 에이전트)

## 📄 발표 논문
#### 🟢 ReAct: Synergizing Reasoning and Acting in LLMs
- **출처:** Yao et al., ICLR 2023 · arXiv:2210.03629
- **발표 필수:** Think–Act–Observe 루프 구조와 추론·행동을 엮는 이유
- **선택 심화:** HotpotQA·ALFWorld 셋업과 프롬프트 구성
- **PDF:** [`W01_ReAct_2210.03629.pdf`](../papers/W01_ReAct_2210.03629.pdf)

#### 🟢 Chain-of-Thought Prompting Elicits Reasoning in LLMs
- **출처:** Wei et al., NeurIPS 2022 · arXiv:2201.11903
- **발표 필수:** CoT 핵심 아이디어와 추론 창발 조건
- **선택 심화:** 규모별 창발 곡선, self-consistency
- **PDF:** [`W01_Chain-of-Thought_2201.11903.pdf`](../papers/W01_Chain-of-Thought_2201.11903.pdf)

## 💬 토론 포인트 (교수 백업 질문)
에이전트와 단순 워크플로우의 경계는? CoT 없는 ReAct는 가능한가?

## 🛠 실습 (from-scratch)
환경 세팅, LLM API 단일 호출 → ReAct 루프 골격(while 루프)

> 실습 코드·노트는 이 파일 아래에 이어 적거나, 분량이 커지면 `week01/` 폴더로 분리한다.

## 🎤 발표 진행 (요약 · 상세는 [발표 가이드](../docs/presentation-guide.md))
- 편당 **25분**: 발표 15분(슬라이드 6장 상한·하드 스톱) + 이해검증 8분 + 정리 2분
- 발표 템플릿 6장: ①한 문장 기여 ②문제·동기 ③핵심 메커니즘(직접 그린 그림) ④결과 1개 ⑤약한 가정·한계 ⑥연결
- 교수 콜드 질문(슬라이드 끄고): *X 단계 빼면? / 처음부터 구현 첫 3단계? / 실패하는 입력?*
- 지정 토론자 1명 사전 배정 → 발표 후 2분 반박·보완

## 📊 평가 루브릭
| 항목 | 배점 | 기준 |
|---|---|---|
| 핵심 기여 | 30% | 논문의 기여를 한 문장으로 정확히 압축했는가 |
| 방법 이해 | 25% | 핵심 아이디어·메커니즘을 정확히 설명했는가 (심화는 직관 허용, 수식 생략 가능) |
| 비판적 분석 | 25% | 가장 약한 가정·한계를 스스로 짚었는가 |
| 연결·확장 | 20% | 후속 논문 또는 본인/연구실 주제와 연결했는가 |
