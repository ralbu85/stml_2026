# Week 07. 검색 증강 (RAG) — 2부: 에이전틱 RAG

> **Part:** 추론과 지식 · **난이도 범례:** 🟢 기초 · 🟡 중급 · 🔴 심화

## 📖 보조읽기 (발표 대상 아님)
Anthropic — *Code Execution with MCP* (도구 호출 오버헤드를 코드 실행으로 줄이기)

## 🛠 실습 (from-scratch)
검색을 '도구'로 노출하고 에이전트가 단계별로 호출하게 개조

## 💬 토론 포인트 (교수용 백업 질문)
RAG를 도구로 만들면 무엇이 좋아지고 무엇이 어려워지나?

## 발표 논문
#### 🟡🔴 Self-RAG: Learning to Retrieve, Generate, and Critique
- **출처:** Asai et al., ICLR 2024 · arXiv:2310.11511
- **발표 필수:** reflection token으로 검색 여부·품질을 스스로 판단
- **선택 심화:** critic 학습, segment beam search
- **PDF:** [`W07_Self-RAG_2310.11511.pdf`](../../papers/W07_Self-RAG_2310.11511.pdf)

#### 🟡 Adaptive-RAG: Adapting Retrieval to Query Complexity
- **출처:** Jeong et al., NAACL 2024 · arXiv:2403.14403
- **발표 필수:** 질의 난이도에 따라 검색 전략을 바꾸는 에이전틱 구조
- **선택 심화:** complexity classifier
- **PDF:** [`W07_Adaptive-RAG_2403.14403.pdf`](../../papers/W07_Adaptive-RAG_2403.14403.pdf)

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
