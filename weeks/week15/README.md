# Week 15. 단순함의 힘 — 에이전트가 꼭 필요한가

> **Part:** 평가와 마무리 · **난이도 범례:** 🟢 기초 · 🟡 중급 · 🔴 심화

## 📖 보조읽기 (발표 대상 아님)
HumanLayer — *Skill Issue: Harness Engineering* (대부분의 실패는 모델이 아니라 설정)

## 🛠 실습 (from-scratch)
최종 프로젝트 구현 집중 (검색·메모리·평가 통합)

## 💬 토론 포인트 (교수용 백업 질문)
복잡한 에이전트 vs 단순 파이프라인 — 우리 과제엔 무엇이 맞나?

## 발표 논문
#### 🟢 Agentless: Demystifying LLM-based SE Agents
- **출처:** Xia et al., 2024 · arXiv:2407.01489
- **발표 필수:** 복잡한 에이전트 없이 단순 파이프라인이 더 나을 수 있다는 반론
- **선택 심화:** localize-repair-validate, SWE-bench
- **PDF:** [`W15_Agentless_2407.01489.pdf`](../../papers/W15_Agentless_2407.01489.pdf)

#### 🟡 SWE-agent: Agent-Computer Interfaces Enable Automated SE
- **출처:** Yang et al., NeurIPS 2024 · arXiv:2405.15793
- **발표 필수:** 에이전트-컴퓨터 인터페이스(ACI)가 성능을 가른다는 발견
- **선택 심화:** 명령·관찰 인터페이스 설계
- **PDF:** [`W15_SWE-agent_2405.15793.pdf`](../../papers/W15_SWE-agent_2405.15793.pdf)

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
