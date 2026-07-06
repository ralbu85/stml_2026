# Week 07. 검색 증강 (RAG) — 2부: 에이전틱 RAG

> **Part:** 추론과 지식 · 난이도: 🟢 기초 · 🟡 중급 · 🔴 심화 · [📋 발표 가이드](../docs/presentation-guide.md)

## 🧭 개요
검색을 전처리가 아닌 **'도구'로 바꾸는 에이전틱 RAG**. 이론에서 능동 검색(adaptive/self)과 MCP를 다루고, 실습에서 검색을 도구로 노출해 에이전트가 단계별로 호출하게 개조한다 *(최종 프로젝트 부품 2)*. Self-RAG·Adaptive-RAG.

## 📖 보조읽기 (발표 대상 아님)
Anthropic — *Code Execution with MCP* (도구 호출 오버헤드를 코드 실행으로 줄이기)

## 📄 발표 논문
#### 🟡🔴 Self-RAG: Learning to Retrieve, Generate, and Critique
- **출처:** Asai et al., ICLR 2024 · arXiv:2310.11511
- **발표 필수:** reflection token으로 검색 여부·품질을 스스로 판단
- **선택 심화:** critic 학습, segment beam search
- **PDF:** [`W07_Self-RAG_2310.11511.pdf`](../papers/W07_Self-RAG_2310.11511.pdf)

#### 🟡 Adaptive-RAG: Adapting Retrieval to Query Complexity
- **출처:** Jeong et al., NAACL 2024 · arXiv:2403.14403
- **발표 필수:** 질의 난이도에 따라 검색 전략을 바꾸는 에이전틱 구조
- **선택 심화:** complexity classifier
- **PDF:** [`W07_Adaptive-RAG_2403.14403.pdf`](../papers/W07_Adaptive-RAG_2403.14403.pdf)

## 💬 토론 포인트 (교수 백업 질문)
RAG를 도구로 만들면 무엇이 좋아지고 무엇이 어려워지나?

## 🛠 실습 (from-scratch)
검색을 '도구'로 노출하고 에이전트가 단계별로 호출하게 개조

> 실습 코드·노트는 이 파일 아래에 이어 적거나, 분량이 커지면 `week07/` 폴더로 분리한다.

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
