# Week 09. 체화·평생학습 (Embodied / Lifelong)

> **Part:** 협업과 환경 · 난이도: 🟢 기초 · 🟡 중급 · 🔴 심화 · [📋 발표 가이드](../docs/presentation-guide.md)

## 📖 보조읽기 (발표 대상 아님)
Anthropic — *Effective Harnesses for Long-Running Agents* (장기 과제 패턴)

## 📄 발표 논문
#### 🟡 Voyager: An Open-Ended Embodied Agent with LLMs
- **출처:** Wang et al., 2023 · arXiv:2305.16291
- **발표 필수:** 스킬 라이브러리를 누적하는 평생학습 메커니즘
- **선택 심화:** automatic curriculum, 코드형 스킬
- **PDF:** [`W09_Voyager_2305.16291.pdf`](../papers/W09_Voyager_2305.16291.pdf)

#### 🟡 Generative Agents: Interactive Simulacra of Human Behavior
- **출처:** Park et al., UIST 2023 · arXiv:2304.03442
- **발표 필수:** 메모리·반성·계획을 한 시스템에 통합
- **선택 심화:** 최신성·중요도·관련성 점수화
- **PDF:** [`W09_Generative-Agents_2304.03442.pdf`](../papers/W09_Generative-Agents_2304.03442.pdf)

## 💬 토론 포인트 (교수 백업 질문)
누적된 스킬이 항상 도움이 되는가? 망각이 필요한 순간은?

## 🛠 실습 (from-scratch)
재사용 가능한 스킬 라이브러리(도구 누적) 구현

> 실습 코드·노트는 이 파일 아래에 이어 적거나, 분량이 커지면 `week09/` 폴더로 분리한다.

## 🎤 발표 진행 (요약 · 상세는 [발표 가이드](../docs/presentation-guide.md))
- 편당 **20분**: 발표 12분(슬라이드 6장 상한·하드 스톱) + 이해검증 6분 + 정리 2분
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
