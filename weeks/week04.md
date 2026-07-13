# Week 04. 에이전트 루프 (ReAct)

> **Part:** 부품에서 루프까지 · 난이도: 🟢 기초 · 🟡 중급 · 🔴 심화 · [📋 발표 가이드](../docs/presentation-guide.md)

## 🧭 개요
추론(W2)과 도구(W3)를 하나의 제어 루프로 결합하는 주. 이론에서 그냥 묻기→CoT→Act-only→**ReAct의 추론–행동–관찰 루프** 계보를 다루고 트레이스를 라이브로 읽는다. 실습에서 그 루프를 while 문으로 직접 구현해 **첫 완전한 에이전트**를 완성하고, 이후 매주 쓰는 **미니 evalset**(5문항)을 시작한다. ReAct·DeepSeek-R1. R1 발표는 RL 사전 지식을 가정하지 않는다 — 발표 필수는 보상 서사의 큰 그림까지.

## 📖 보조읽기 (발표 대상 아님)
Lilian Weng — *LLM Powered Autonomous Agents* · Berkeley 에이전트 역사 강의

## 📄 발표 논문
#### 🟢 ReAct: Synergizing Reasoning and Acting in LLMs
- **출처:** Yao et al., ICLR 2023 · arXiv:2210.03629
- **발표 필수:** Think–Act–Observe 루프 구조와 추론·행동을 엮는 이유
- **선택 심화:** HotpotQA·ALFWorld 셋업
- **PDF:** [`W04_ReAct_2210.03629.pdf`](../papers/W04_ReAct_2210.03629.pdf)

#### 🟡 DeepSeek-R1: Incentivizing Reasoning via RL
- **출처:** DeepSeek-AI, 2025 · arXiv:2501.12948
- **발표 필수:** 순수 RL로 추론이 창발하는 큰 그림('aha moment')과 추론 모델이 루프 설계에 미치는 영향
- **선택 심화:** GRPO, cold-start 데이터
- **PDF:** [`W04_DeepSeek-R1_2501.12948.pdf`](../papers/W04_DeepSeek-R1_2501.12948.pdf)

#### 🟡 STaR: Self-Taught Reasoner (선택읽기·추론 학습 계보) *(선택읽기)*
- **출처:** Zelikman et al., NeurIPS 2022 · arXiv:2203.14465
- **발표 필수:** 스스로 만든 추론으로 추론을 부트스트랩하는 아이디어
- **선택 심화:** rationalization 트릭
- **PDF:** [`W04_opt-STaR_2203.14465.pdf`](../papers/W04_opt-STaR_2203.14465.pdf)

## 💬 토론 포인트 (교수 백업 질문)
CoT 없는 ReAct는 가능한가? 추론과 행동을 섞으면 왜 둘 다 좋아지나?

## 🛠 실습 — 누적 빌드 `docqa-agent`
**빌드 베이스:** from-scratch (내 모듈 직접 구현) · LLM 호출은 **aisuite** 래퍼(provider 무관)

*이번 주 주제:* ReAct(Thought→Action→Observation) while 루프 직접 구현 — W3 도구 레지스트리 위에서 + 미니 evalset

**추가 모듈:** `loop.py` — ReAct while 루프 골격. W3의 `tools.py` 레지스트리를 호출한다. + 미니 evalset 5문항.
> ✅ **완료:** 루프가 계산기 도구를 실제로 호출해 답하고, 미니 evalset 결과가 기록된다.

> 한 학기 하나의 앱을 쌓는다 · 스캐폴드 빈칸 채우기 + 주차별 체크포인트 → 상세는 [실습 가이드](../docs/practice-guide.md).

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
