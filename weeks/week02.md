# Week 02. CoT → ReAct — 추론과 행동의 결합

> **Part:** 토대 · 난이도: 🟢 기초 · 🟡 중급 · 🔴 심화 · [📋 발표 가이드](../docs/presentation-guide.md)

## 🧭 개요
**하네스(제어 루프)의 최소 형태**를 만드는 주. 이론에서 CoT(생각의 외부화)→Act-only→**ReAct의 추론–행동–관찰 루프** 계보를 다루고 트레이스를 라이브로 읽는다. 실습에서 그 루프를 while 문으로 직접 구현한다. **학생 발표 시작** — ReAct·CoT.

## 📖 보조읽기 (발표 대상 아님)
Lilian Weng — *LLM Powered Autonomous Agents* · Berkeley 에이전트 역사 강의

## 📄 발표 논문
#### 🟢 ReAct: Synergizing Reasoning and Acting in LLMs
- **출처:** Yao et al., ICLR 2023 · arXiv:2210.03629
- **발표 필수:** Think–Act–Observe 루프 구조와 추론·행동을 엮는 이유
- **선택 심화:** HotpotQA·ALFWorld 셋업
- **PDF:** [`W02_ReAct_2210.03629.pdf`](../papers/W02_ReAct_2210.03629.pdf)

#### 🟢 Chain-of-Thought Prompting Elicits Reasoning in LLMs
- **출처:** Wei et al., NeurIPS 2022 · arXiv:2201.11903
- **발표 필수:** CoT 핵심 아이디어와 추론 창발 조건
- **선택 심화:** 규모별 창발 곡선, self-consistency
- **PDF:** [`W02_Chain-of-Thought_2201.11903.pdf`](../papers/W02_Chain-of-Thought_2201.11903.pdf)

## 💬 토론 포인트 (교수 백업 질문)
CoT 없는 ReAct는 가능한가? 추론과 행동을 섞으면 왜 둘 다 좋아지나?

## 🛠 실습 — 누적 빌드 `docqa-agent`
**빌드 베이스:** from-scratch (내 모듈 직접 구현) · LLM 호출은 **aisuite** 래퍼(provider 무관)

*이번 주 주제:* ReAct(Thought→Action→Observation) while 루프 직접 구현

**추가 모듈:** `loop.py` — ReAct(Thought→Action→Observation) while 루프 골격. W1 이론에서 본 루프를 직접 짠다.
> ✅ **완료:** 간단한 질문에 루프가 한 바퀴 돌아 답을 낸다.

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
