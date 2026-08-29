# Week 03. 추론 모델과 강화학습 (Reasoning Models & RL)

> **Part:** 부품에서 루프까지 · 난이도: 🟢 기초 · 🟡 중급 · 🔴 심화 · [📋 발표 가이드](../docs/presentation-guide.md)

## 🧭 개요
추론 능력을 모델의 가중치에 넣는 주. 이론에서 W2 test-time compute의 내재화인 **추론 모델**(o1/R1, thinking budget), 훈련 데이터의 문제(과정 레이블 부재), **STaR**(자가 생성·정오 필터), **강화학습**(정책·보상, RLHF vs RLVR), **R1**(GRPO, 창발)과 보상 해킹·증류를 다룬다. **RL 사전 지식 없음 가정** — 정의부터 강의에서 세운다. 실습은 self-consistency 구현(호출자 쪽 반복 절차의 실물)과 N=1 대비 비교.

## 📖 보조읽기 (발표 대상 아님)
Lilian Weng — *Why We Think* · Berkeley `Jason-Weston-Reasoning.pdf`

## 📄 발표 논문
#### 🟡 STaR: Self-Taught Reasoner
- **출처:** Zelikman et al., NeurIPS 2022 · arXiv:2203.14465
- **발표 필수:** 스스로 만든 추론으로 추론을 부트스트랩하는 아이디어
- **선택 심화:** rationalization 트릭
- **PDF:** [`W03_STaR_2203.14465.pdf`](../papers/W03_STaR_2203.14465.pdf)

#### 🟡 DeepSeek-R1: Incentivizing Reasoning via RL
- **출처:** DeepSeek-AI, 2025 · arXiv:2501.12948
- **발표 필수:** 순수 RL로 추론이 창발하는 큰 그림('aha moment')
- **선택 심화:** GRPO, cold-start 데이터
- **PDF:** [`W03_DeepSeek-R1_2501.12948.pdf`](../papers/W03_DeepSeek-R1_2501.12948.pdf)

## 💬 토론 포인트 (교수 백업 질문)
'더 오래 생각하기'는 왜 성능을 올리나? 언제 과한가?

## 🛠 실습 — 누적 빌드 `docqa-agent`
**빌드 베이스:** from-scratch (내 모듈 직접 구현) · LLM 호출은 **aisuite** 래퍼(provider 무관)

*이번 주 주제:* self-consistency(N샘플 다수결) 구현 — 추론 모델이 내재화한 호출자 쪽 반복 절차의 실물, N=1 대비 정확도·비용 비교

**추가 모듈:** `reasoning.py` — 같은 질문을 N번 샘플→다수결(`majority_vote`·`self_consistency`).
진행: 실습 노트북(`lectures/week03/W3_lab_selfconsistency.ipynb`) → `pytest tests/test_week03.py` → `demos/week03_selfconsistency.py`
> ✅ **완료:** 애매한 질문에서 N=1보다 N=5의 정확도가 높고, 그 대가로 비용이 N배임을 함께 기록한다.

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
