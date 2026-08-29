# Week 06. 검색 증강 (RAG) — 기초와 에이전틱

> **Part:** 지식 · 난이도: 🟢 기초 · 🟡 중급 · 🔴 심화 · [📋 발표 가이드](../docs/presentation-guide.md)

## 🧭 개요
외부 지식을 끌어오는 **검색 증강(RAG)** 을 기초부터 에이전틱까지 한 주에 다룬다. W5의 에이전트는 돌지만 아는 것이 없다 — 이론에서 임베딩·코사인 유사도(이 과목 유일의 수식), 청킹→인덱스→top-k 파이프라인, 그리고 고정 파이프라인의 낭비에서 **검색=도구**(에이전틱 RAG)로의 전환을 다룬다. 실습에서 retriever를 만들고 곧바로 도구로 등록한다 *(최종 프로젝트 부품 1·2)*. RAG(Lewis)·Self-RAG. *(보안 복선: 오늘 만든 '문서 입구'가 W14 간접 인젝션의 공격 통로가 된다 — 예고만.)*

## 📖 보조읽기 (발표 대상 아님)
Anthropic — *Contextual Retrieval* · MS05 · `RAG_Techniques`(기초 노트북)

## 📄 발표 논문
#### 🟡 Retrieval-Augmented Generation for Knowledge-Intensive NLP
- **출처:** Lewis et al., NeurIPS 2020 · arXiv:2005.11401
- **발표 필수:** 파라메트릭 vs 비파라메트릭(검색) 지식 결합
- **선택 심화:** RAG-Sequence vs Token, retriever 공동학습
- **PDF:** [`W06_RAG-Lewis_2005.11401.pdf`](../papers/W06_RAG-Lewis_2005.11401.pdf)

#### 🟡🔴 Self-RAG: Learning to Retrieve, Generate, and Critique
- **출처:** Asai et al., ICLR 2024 · arXiv:2310.11511
- **발표 필수:** reflection token으로 검색 여부·품질을 스스로 판단
- **선택 심화:** critic 학습, segment beam search
- **PDF:** [`W06_Self-RAG_2310.11511.pdf`](../papers/W06_Self-RAG_2310.11511.pdf)

#### 🟡 HyDE: Precise Zero-Shot Dense Retrieval (선택읽기) *(선택읽기)*
- **출처:** Gao et al., ACL 2023 · arXiv:2212.10496
- **발표 필수:** 가설 문서를 생성해 검색 품질을 올리는 발상
- **선택 심화:** dense retriever와의 결합
- **PDF:** [`W06_opt-HyDE_2212.10496.pdf`](../papers/W06_opt-HyDE_2212.10496.pdf)

#### 🟡 Adaptive-RAG (선택읽기) *(선택읽기)*
- **출처:** Jeong et al., NAACL 2024 · arXiv:2403.14403
- **발표 필수:** 질의 난이도에 따라 검색 전략을 바꾸는 에이전틱 구조
- **선택 심화:** complexity classifier
- **PDF:** [`W06_opt-Adaptive-RAG_2403.14403.pdf`](../papers/W06_opt-Adaptive-RAG_2403.14403.pdf)

## 💬 토론 포인트 (교수 백업 질문)
언제 검색해야 하는가? 항상 검색이 답인가?

## 🛠 실습 — 누적 빌드 `docqa-agent`
**빌드 베이스:** from-scratch (내 모듈 직접 구현) · LLM 호출은 **aisuite** 래퍼(provider 무관)

*이번 주 주제:* 임베딩→코사인 top-k 검색 구현 + 검색을 도구로 등록 *(최종 프로젝트 부품 1·2)*

**추가 모듈:** `retriever.py` — 청킹→임베딩→코사인 top-k 검색, 그리고 `tools.py`에 검색 도구로 등록. 📦 *최종 부품*
> ✅ **완료:** 문서 속 사실을 물으면 관련 청크로 답하고, 상식 질문은 검색하지 않는다.

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
