# Week 02. 프롬프팅과 추론 (Prompting & Reasoning)

> **Part:** 부품에서 루프까지 · 난이도: 🟢 기초 · 🟡 중급 · 🔴 심화 · [📋 발표 가이드](../docs/presentation-guide.md)

## 🧭 개요
에이전트의 추론 능력을 프롬프트로 끌어내는 주. 이론에서 messages·역할 구조와 few-shot(in-context learning), **CoT**(생각의 외부화), **test-time compute**(self-consistency 다수결), 추론 모델(o1/R1)의 사용 관점(thinking budget·비용)을 다룬다. 실습은 CoT·self-consistency 비교 실험. 추론 모델의 훈련 원리(STaR·RLVR)는 W4 발표·선택읽기로 위임한다. **첫 학생 발표 주 — 부담 완화를 위해 1편만.**

## 📖 보조읽기 (발표 대상 아님)
Anthropic — *Prompt Engineering Interactive Tutorial* · Lilian Weng — *Why We Think* (test-time compute 직관)

## 📄 발표 논문
#### 🟢 Chain-of-Thought Prompting Elicits Reasoning in LLMs
- **출처:** Wei et al., NeurIPS 2022 · arXiv:2201.11903
- **발표 필수:** CoT 핵심 아이디어와 추론 창발 조건
- **선택 심화:** 규모별 창발 곡선, self-consistency
- **PDF:** [`W02_Chain-of-Thought_2201.11903.pdf`](../papers/W02_Chain-of-Thought_2201.11903.pdf)

## 💬 토론 포인트 (교수 백업 질문)
'더 오래 생각하기'는 왜 성능을 올리나? 언제 과한가?

## 🛠 실습 — 누적 빌드 `docqa-agent`
**빌드 베이스:** from-scratch (내 모듈 직접 구현) · LLM 호출은 **aisuite** 래퍼(provider 무관)

*이번 주 주제:* CoT 프롬프트 작성 + self-consistency(N샘플 다수결) 비교 실험

**추가 모듈:** `reasoning.py` — CoT 프롬프트 토글 + 같은 질문을 N번 샘플→다수결(self-consistency).
> ✅ **완료:** 애매한 질문에서 단일 답보다 정확도가 오른다.

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
