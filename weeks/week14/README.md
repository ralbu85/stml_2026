# Week 14. 평가와 벤치마크 (Evaluation) — 비판적 시각

> **Part:** 평가와 마무리 · **난이도 범례:** 🟢 기초 · 🟡 중급 · 🔴 심화

## 📖 보조읽기 (발표 대상 아님)
LangChain — *Agent Evaluation Readiness Checklist* (능력 평가 vs 회귀 평가 · 최종프로젝트 직결)

## 🛠 실습 (from-scratch)
최종 프로젝트 설계 + 평가 하네스(정확도·비용·재현성) 골격

## 💬 토론 포인트 (교수용 백업 질문)
무엇을 측정해야 하는가? 우리 RAG 에이전트의 성공 기준은?

## 발표 논문
#### 🟢 AI Agents That Matter
- **출처:** Kapoor et al., 2024 · arXiv:2407.01502
- **발표 필수:** 리더보드의 함정, 비용을 무시한 정확도의 문제
- **선택 심화:** Pareto(정확도-비용), 재현성
- **PDF:** [`W14_AI-Agents-That-Matter_2407.01502.pdf`](../../papers/W14_AI-Agents-That-Matter_2407.01502.pdf)

#### 🟡 τ-bench: Tool-Agent-User Interaction Benchmark
- **출처:** Yao et al., ICLR 2025 · arXiv:2406.12045
- **발표 필수:** 실세계 도메인 도구-에이전트-사용자 상호작용 평가
- **선택 심화:** pass^k, 일관성 측정
- **PDF:** [`W14_tau-bench_2406.12045.pdf`](../../papers/W14_tau-bench_2406.12045.pdf)

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
