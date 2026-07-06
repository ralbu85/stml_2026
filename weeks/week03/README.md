# Week 03. 피드백·자기반성 (Reflection)

> **Part:** 에이전트 기초 · **난이도 범례:** 🟢 기초 · 🟡 중급 · 🔴 심화

## 📖 보조읽기 (발표 대상 아님)
Anthropic — *Demystifying Evals for AI Agents* (검증 루프를 하네스에 내장)

## 🛠 실습 (from-scratch)
실패→언어 피드백→재시도 루프를 ReAct에 추가

## 💬 토론 포인트 (교수용 백업 질문)
자기반성은 진짜 개선인가, 아니면 같은 오류의 반복인가?

## 발표 논문
#### 🟡 Reflexion: Language Agents with Verbal RL
- **출처:** Shinn et al., NeurIPS 2023 · arXiv:2303.11366
- **발표 필수:** 언어 피드백이 gradient 없이 학습되는 메커니즘
- **선택 심화:** actor-evaluator-reflection 구조, 메모리 버퍼
- **PDF:** [`W03_Reflexion_2303.11366.pdf`](../../papers/W03_Reflexion_2303.11366.pdf)

#### 🟢 Self-Refine: Iterative Refinement with Self-Feedback
- **출처:** Madaan et al., NeurIPS 2023 · arXiv:2303.17651
- **발표 필수:** 단일 모델의 생성→비평→개선 반복
- **선택 심화:** 과제별 개선 폭, 피드백 프롬프트 설계
- **PDF:** [`W03_Self-Refine_2303.17651.pdf`](../../papers/W03_Self-Refine_2303.17651.pdf)

## 폴더
- `theory/` — 이론 강의 자료 (슬라이드·노트)
- `practice/` — from-scratch 실습 코드
- `presentation/` — 학생 논문 발표 자료

## 발표 평가 루브릭
| 항목 | 배점 | 기준 |
|---|---|---|
| 핵심 기여 | 30% | 논문의 기여를 한 문장으로 정확히 압축했는가 |
| 방법 이해 | 25% | 핵심 아이디어·메커니즘을 정확히 설명했는가 (심화는 직관 허용, 수식 생략 가능) |
| 비판적 분석 | 25% | 가장 약한 가정·한계를 스스로 짚었는가 |
| 연결·확장 | 20% | 후속 논문 또는 본인/연구실 주제와 연결했는가 |
