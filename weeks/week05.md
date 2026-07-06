# Week 05. 🆕 추론 모델 (Reasoning Models / Test-time Compute)

> **Part:** 추론과 지식 · 난이도: 🟢 기초 · 🟡 중급 · 🔴 심화 · [📋 발표 가이드](../docs/presentation-guide.md)

## 🧭 개요
2025–26 에이전트의 토대인 **추론 모델**. 이론에서 CoT→self-consistency→**test-time compute**의 흐름과, RL로 추론이 창발하는 과정(DeepSeek-R1), STaR 부트스트랩을 다룬다. 실습은 self-consistency 비교. 어렵지 않으면서 화제성이 높아 동기부여가 잘 되는 주.

## 📖 보조읽기 (발표 대상 아님)
Lilian Weng — *Why We Think* (또는 DeepSeek-R1 해설) — test-time compute 직관

## 📄 발표 논문
#### 🟡 STaR: Self-Taught Reasoner
- **출처:** Zelikman et al., NeurIPS 2022 · arXiv:2203.14465
- **발표 필수:** 스스로 만든 추론으로 추론을 부트스트랩하는 아이디어
- **선택 심화:** rationalization 트릭
- **PDF:** [`W05_STaR_2203.14465.pdf`](../papers/W05_STaR_2203.14465.pdf)

#### 🟡 DeepSeek-R1: Incentivizing Reasoning via RL
- **출처:** DeepSeek-AI, 2025 · arXiv:2501.12948
- **발표 필수:** 순수 RL로 추론이 창발하는 큰 그림('aha moment')
- **선택 심화:** GRPO, cold-start 데이터
- **PDF:** [`W05_DeepSeek-R1_2501.12948.pdf`](../papers/W05_DeepSeek-R1_2501.12948.pdf)

## 💬 토론 포인트 (교수 백업 질문)
'더 오래 생각하기'는 왜 성능을 올리나? 언제 과한가?

## 🛠 실습 (from-scratch)
self-consistency / 간단한 다중 샘플 추론 비교

> 실습 코드·노트는 이 파일 아래에 이어 적거나, 분량이 커지면 `week05/` 폴더로 분리한다.

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
