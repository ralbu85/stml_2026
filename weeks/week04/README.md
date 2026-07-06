# Week 04. 계획과 탐색 (Planning & Search)

> **Part:** 에이전트 기초 · **난이도 범례:** 🟢 기초 · 🟡 중급 · 🔴 심화

## 📖 보조읽기 (발표 대상 아님)
LangChain — *Plan-and-Execute Agents* (계획·실행 분리 하네스 패턴)

## 🛠 실습 (from-scratch)
탐색 기반 추론(트리 분기) 미니 구현

## 💬 토론 포인트 (교수용 백업 질문)
탐색 비용 대비 성능 이득은 언제 정당한가?

## 발표 논문
#### 🟡 Tree of Thoughts: Deliberate Problem Solving with LLMs
- **출처:** Yao et al., NeurIPS 2023 · arXiv:2305.10601
- **발표 필수:** 사고를 트리로 분기·탐색(BFS/DFS)하는 발상
- **선택 심화:** 상태 평가 함수, Game of 24
- **PDF:** [`W04_Tree-of-Thoughts_2305.10601.pdf`](../../papers/W04_Tree-of-Thoughts_2305.10601.pdf)

#### 🟡 ReWOO: Decoupling Reasoning from Observations
- **출처:** Xu et al., 2023 · arXiv:2305.18323
- **발표 필수:** 계획을 관찰과 분리해 토큰·호출을 줄이는 구조
- **선택 심화:** planner/worker/solver 모듈 분해
- **PDF:** [`W04_ReWOO_2305.18323.pdf`](../../papers/W04_ReWOO_2305.18323.pdf)

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
