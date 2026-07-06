# Week 10. 멀티에이전트 + LangGraph 전환점 ⭐

> **Part:** 협업과 환경 · 난이도: 🟢 기초 · 🟡 중급 · 🔴 심화 · [📋 발표 가이드](../docs/presentation-guide.md)

## 🧭 개요
⭐ **전환점.** 여러 에이전트의 협업과 프레임워크로의 전환. 이론에서 협업 아키텍처(핸드오프·라우터)와 **그래프 실행 모델**을 다루고, 실습에서 직접 짠 멀티에이전트를 **LangGraph로 재구현·비교**한다(from-scratch→프레임워크 분기점). AutoGen·MetaGPT.

## 📖 보조읽기 (발표 대상 아님)
LangChain — *Choosing the Right Multi-Agent Architecture* (서브에이전트·핸드오프·라우터 비교)

## 📄 발표 논문
#### 🟡 AutoGen: Multi-Agent Conversation Framework
- **출처:** Wu et al., COLM 2024 · arXiv:2308.08155
- **발표 필수:** 대화 기반 멀티에이전트 추상화와 역할 분담
- **선택 심화:** conversable agent, human-in-the-loop
- **PDF:** [`W10_AutoGen_2308.08155.pdf`](../papers/W10_AutoGen_2308.08155.pdf)

#### 🟡 MetaGPT: Meta Programming for Multi-Agent Collaboration
- **출처:** Hong et al., ICLR 2024 · arXiv:2308.00352
- **발표 필수:** SOP(표준운영절차)를 코드화한 협업 구조
- **선택 심화:** 역할별 산출물 스키마
- **PDF:** [`W10_MetaGPT_2308.00352.pdf`](../papers/W10_MetaGPT_2308.00352.pdf)

#### 🟡 Multiagent Debate (선택읽기) *(선택읽기)*
- **출처:** Du et al., ICML 2024 · arXiv:2305.14325
- **발표 필수:** 다중 에이전트 토론이 사실성·추론을 높이는 원리
- **선택 심화:** 수렴 동역학, 에이전트 수·라운드
- **PDF:** [`W10_opt-Multiagent-Debate_2305.14325.pdf`](../papers/W10_opt-Multiagent-Debate_2305.14325.pdf)

#### 🟡 CAMEL: Communicative Agents (선택읽기) *(선택읽기)*
- **출처:** Li et al., NeurIPS 2023 · arXiv:2303.17760
- **발표 필수:** 역할극 기반 자율 협력 프레임
- **선택 심화:** inception prompting, 과제 분해
- **PDF:** [`W10_opt-CAMEL_2303.17760.pdf`](../papers/W10_opt-CAMEL_2303.17760.pdf)

## 💬 토론 포인트 (교수 백업 질문)
멀티에이전트가 단일 에이전트보다 정말 나은가? 언제 과한가?

## 🛠 실습 (from-scratch)
역할 분담 멀티에이전트를 **LangGraph로 재구현·비교** (직접 구현 대비)

> 실습 코드·노트는 이 파일 아래에 이어 적거나, 분량이 커지면 `week10/` 폴더로 분리한다.

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
