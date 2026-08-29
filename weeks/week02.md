# Week 02. 프롬프팅과 추론 (Prompting & Reasoning)

> **Part:** 부품에서 루프까지 · 난이도: 🟢 기초 · 🟡 중급 · 🔴 심화 · [📋 발표 가이드](../docs/presentation-guide.md)

## 🧭 개요
에이전트의 추론 능력을 프롬프트와 계산으로 끌어내는 주. 이론에서 추론의 정의, 직접 질의가 실패하는 원인(글밖에 없는 작업 공간), **CoT**(중간 단계의 외부화 — 지시와 풀이 예시), 그 확장인 **self-consistency**(표집과 다수결)와 **test-time compute**(예측 횟수·정확도의 교환)를 다룬다. 실습은 직접 질의 vs CoT 정답률 측정과 few-shot exemplar 작성(다수결 구현은 W3 실습). **첫 학생 발표 주 — 부담 완화를 위해 1편만.**

## 📖 보조읽기 (발표 대상 아님)
Anthropic — *Prompt Engineering Interactive Tutorial* · Berkeley `llm-reasoning.pdf`

## 📄 발표 논문
#### 🟢 Chain-of-Thought Prompting Elicits Reasoning in LLMs
- **출처:** Wei et al., NeurIPS 2022 · arXiv:2201.11903
- **발표 필수:** CoT 핵심 아이디어와 추론 창발 조건
- **선택 심화:** 규모별 창발 곡선
- **PDF:** [`W02_Chain-of-Thought_2201.11903.pdf`](../papers/W02_Chain-of-Thought_2201.11903.pdf)

## 💬 토론 포인트 (교수 백업 질문)
풀이를 쓰게 하면 왜 정답률이 오르나? 어떤 문제에서는 안 오르나?

## 🛠 실습 — 누적 빌드 `docqa-agent`
**빌드 베이스:** from-scratch (내 모듈 직접 구현) · LLM 호출은 **aisuite** 래퍼(provider 무관)

*이번 주 주제:* 직접 질의 vs CoT 정답률 측정 + few-shot exemplar 작성으로 정답률 개선

**실험:** `reasoning.py`의 `COT_PROMPT`로 직접 질의 vs CoT 정답률을 측정하고, few-shot exemplar를 직접 작성해 정답률을 올린다.
진행: 실습 노트북(`lectures/week02/W2_lab_prompting.ipynb`) → `demos/week02_cot.py`
> ✅ **완료:** 직접 질의 대비 CoT, zero-shot 대비 exemplar의 정답률 표를 기록한다.

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
