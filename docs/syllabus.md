# 머신러닝 특론 — LLM 에이전트 (2026) · 강의계획서

> **부제:** 논문 읽기와 함께 만들기 — 16주, 주당 논문 2편 발표 + 매주 from-scratch 실습
> **대상:** 부산대/부경대 대학원 · **최종 산출물:** RAG 문서 QA 에이전트
> **흐름:** Microsoft *ai-agents-for-beginners* + UC Berkeley *LLM Agents* 재구성
> **난이도:** 🟢 기초 · 🟡 중급 · 🔴 심화

주차별 상세(보조읽기·실습·토론·발표논문·루브릭)는 [`weeks/weekNN.md`](../weeks/) 참고.
이론 전개용 참고자료·주차별 이론 플랜은 [`materials/README.md`](../materials/README.md).

## 설계 원칙

- **검증된 커리큘럼 흐름 계승** — MS 16레슨 커버리지 + Berkeley의 추론·RL·평가.
- **보조읽기 / 발표논문 분리** — 산업체 가이드·서베이는 '보조 읽기'(발표 대상 아님).
- **실습 누적 = 최종 산출물** — 매주 from-scratch로 부품을 쌓아 RAG QA 에이전트를 완성.
- **from-scratch → 10주 LangGraph 전환점** — 먼저 직접 짜고, 이후 프레임워크로.
- **난이도-무관 4항목 루브릭** ([발표 가이드](presentation-guide.md)).
- **1주차 ↔ 16주차 수미상관** — "에이전트란?"로 열고 "What is an Agent?"로 닫는다.

## 16주 구성

| 주 | 주제 | 발표 논문 (난이도) | 실습(📦=최종 부품) | 대응 |
|---|---|---|---|---|
| **토대** |
| 1 | 에이전트 개요 + ReAct | ReAct🟢 · CoT🟢 | ReAct 제어 루프 골격 | MS01 |
| 2 | 추론 모델(test-time) | STaR🟡 · DeepSeek-R1🟡 | self-consistency 비교 | Bk 추론 |
| **핵심 디자인 패턴** |
| 3 | 도구 사용 | Toolformer🟡 · ToolLLM🟡 | 도구 레지스트리·실행 | MS04 |
| 4 | 계획과 탐색 | Tree of Thoughts🟡 · ReWOO🟡 | 트리 분기 미니 | MS07 |
| 5 | 자기반성·메타인지 | Reflexion🟡 · Self-Refine🟢 | 피드백→재시도 루프 | MS09 |
| **지식·컨텍스트·기억** |
| 6 | RAG 1부: 기초 | RAG-Lewis🟡 · HyDE🟡 | 임베딩→검색 📦 | MS05 |
| 7 | 에이전틱 RAG + MCP | Self-RAG🟡🔴 · Adaptive-RAG🟡 | 검색을 도구로 📦 | MS05·11 |
| 8 | **컨텍스트 엔지니어링(하네스)** ⭐ | Lost-in-the-Middle🟡 · LLMLingua🟡 | 컨텍스트 예산·압축 | MS12 |
| 9 | 메모리 | MemGPT🟡 · **Mem0🟡(2025)** | 메모리 스트림 📦 | MS13 |
| **협업·환경** |
| 10 | 멀티에이전트 + LangGraph ⭐ | AutoGen🟡 · MetaGPT🟡 | LangGraph 재구현 | MS02·08 |
| 11 | 컴퓨터/웹 사용 | WebArena🟡 · **OSWorld🟡(2024)** | 관찰-행동 루프 | MS15 |
| **학습·품질·운영** |
| 12 | 에이전트 강화학습(개념) | ReTool🔴 *(수식 생략)* | 보상 기반 도구선택 시뮬 | Bk 후련 |
| 13 | 평가·벤치마크(비판) | AI Agents That Matter🟢 · τ-bench🟡 | 평가 하네스 골격 | Bk 평가 |
| 14 | 신뢰·보안 | Indirect Injection🟡 · InjecAgent🟡 | 가드레일·인젝션 테스트 | MS06·18 |
| 15 | 프로덕션·단순함 | Agentless🟢 · SWE-agent🟡 | 최종 통합 구현 | MS10 |
| **마무리** |
| 16 | 최종 발표 | (보조) Survey🟢 | 발표+동료평가+리포트 | — |

**선택읽기(프런티어/보강):** W8 ACE·ReasoningBank(자기진화) · W9 MemoryBank·Generative Agents · W10 Multiagent Debate·CAMEL · W11 Mind2Web · W12 Voyager.

## 난이도 곡선

심화 논문은 사실상 W12(ReTool, 직관만)와 W7 Self-RAG(중급~심화) 뿐. 나머지는 기초~중급으로 부산대/부경대 수준에 맞춤. 어떤 주도 '심화+심화'가 아니다.

## 이전 버전 대비 (v2 → 현행)

- **흐름 재편:** 임의 토픽 나열 → **MS/Berkeley 강의 흐름** 계승. 추론 모델을 앞(W2)으로, 반성을 계획 뒤(W5)로.
- **8·9주 문제 해결:** 옛 sim 주(Voyager·Generative Agents) 제거 → **컨텍스트 엔지니어링(하네스, W8)** 신설, 메모리는 **Mem0(2025)** 로 현대화.
- **W11 현대화:** Mind2Web → **OSWorld(2024)**.
- 삭제 논문은 선택읽기로 보존. 발표 논문 38편 전량 arXiv 검증([`papers/README.md`](../papers/README.md)).
