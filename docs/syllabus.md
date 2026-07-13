# 머신러닝 특론 — LLM 에이전트 (2026) · 강의계획서

> **부제:** 논문 읽기와 함께 만들기 — 16주, 매주 from-scratch 실습 + 논문 발표
> **대상:** 부산대/부경대 대학원 · **최종 산출물:** 연구보조 검색·종합 에이전트 (수업 논문 코퍼스 기반 RAG)
> **순서 원칙:** 개념 의존성 — 각 주는 직전 주까지 배운 것만으로 이해 가능해야 한다
> **난이도:** 🟢 기초 · 🟡 중급 · 🔴 심화

주차별 상세(보조읽기·실습·토론·발표논문·루브릭)는 [`weeks/weekNN.md`](../weeks/) 참고.
이론 전개용 참고자료·주차별 이론 플랜은 [`materials/README.md`](../materials/README.md).

## 설계 원칙

- **개념 의존성이 순서를 결정** — 에이전트를 이해하는 데 필요한 개념을 단계적으로 도입한다. 두뇌 격인 추론(W2), 행동 수단인 도구(W3)를 갖춘 뒤에 루프(W4)를 조립한다. 참고 커리큘럼(MS·Berkeley·HF·Anthropic)의 공통 순서와 일치한다.
- **논문 발표와 주차 주제의 디커플링** — 발표 논문은 해당 개념이 강의에 등장한 이후이면 배치가 자유롭다. 주차 설계가 먼저이고 논문 배치는 그 다음이다.
- **지난주 산출물의 한계가 이번 주를 동기화** — 매주 여는 5분은 우리 앱의 실패 사례에서 출발한다.
- **실습 누적 = 최종 산출물** — 매주 from-scratch로 부품을 쌓아 연구보조 에이전트를 완성. W4에 첫 완전한 에이전트가 돌고, 이후는 전부 그 개선이다.
- **from-scratch → 11주 LangGraph 전환점** — 먼저 직접 짜고, 이후 프레임워크로.
- **난이도-무관 4항목 루브릭** ([발표 가이드](presentation-guide.md)).
- **1주차 ↔ 16주차 수미상관** — "에이전트란?"로 열고 "What is an Agent?"로 닫는다.

## 16주 구성

| 주 | 주제 | 발표 논문 (난이도) | 실습(📦=최종 부품) | 대응 |
|---|---|---|---|---|
| **부품에서 루프까지** |
| 1 | 강의소개 · 에이전트 개요 | 학생 발표 없음 (교수 시연: Self-Consistency🟢) | 환경 세팅 + LLM 래퍼 | MS01 |
| 2 | 프롬프팅과 추론 | CoT🟢 (1편 — 첫 발표 주) | CoT·self-consistency | Bk 추론 |
| 3 | 도구 사용 | Toolformer🟡 · ToolLLM🟡 | 도구 레지스트리·실행 | MS04 |
| 4 | 에이전트 루프 (ReAct) | ReAct🟢 · DeepSeek-R1🟡 | ReAct 루프 — 첫 완전한 에이전트 | Bk 역사 |
| **지식** |
| 5 | RAG 1부: 기초 | RAG-Lewis🟡 · HyDE🟡 | 임베딩→검색 📦 | MS05 |
| 6 | 에이전틱 RAG + MCP | Adaptive-RAG🟡 · Self-RAG🟡🔴 | 검색을 도구로 📦 | MS05·11 |
| **단일 에이전트 고도화** |
| 7 | 계획과 탐색 | Tree of Thoughts🟡 · ReWOO🟡 | 멀티홉 질문 분해 플래너 | MS07 |
| 8 | 자기반성·메타인지 | Reflexion🟡 · Self-Refine🟢 | 검색 실패→피드백→재시도 | MS09 |
| 9 | **컨텍스트 엔지니어링(하네스)** ⭐ | Lost-in-the-Middle🟡 · LLMLingua🟡 | 컨텍스트 예산·압축 + 🏁중간데모 | MS12 |
| 10 | 메모리 | MemGPT🟡 · **Mem0🟡(2025)** | 메모리 스트림 📦 | MS13 |
| **협업·환경** |
| 11 | 멀티에이전트 + LangGraph ⭐ | AutoGen🟡 · MetaGPT🟡 | LangGraph 재구현 | MS02·08 |
| 12 | 컴퓨터/웹 사용 | WebArena🟡 · **OSWorld🟡(2024)** | 웹 도구 | MS15 |
| **학습·품질·운영** |
| 13 | 평가·벤치마크(비판) | AI Agents That Matter🟢 · τ-bench🟡 | 평가 하네스 골격 | Bk 평가 |
| 14 | 신뢰·보안 | Indirect Injection🟡 · InjecAgent🟡 | 가드레일·인젝션 테스트 | MS06·18 |
| 15 | 프로덕션·단순함 | Agentless🟢 · SWE-agent🟡 | 최종 통합 구현 | MS10 |
| **마무리** |
| 16 | 최종 발표 | (보조) Survey🟢 | 발표+동료평가+리포트 | — |

**선택읽기(프런티어/보강):** W3 ReTool(도구 RL) · W4 STaR(추론 부트스트랩) · W9 ACE·ReasoningBank(자기진화) · W10 MemoryBank·Generative Agents · W11 Multiagent Debate·CAMEL · W12 Mind2Web·Voyager.

**평가 스레드:** W4(첫 에이전트 완성)부터 매주 실습에 5문항 미니 evalset을 포함해 트레이스 기반 개선을 습관화하고, W13에서 평가 하네스로 정식화한다.

## 주차별 발표 논문 (상세)

각 논문의 정식 인용·발표 필수/선택 심화. 전량 arXiv 검증됨 → [`papers/README.md`](../papers/README.md).

발표 배치는 디커플링 원칙을 따른다: 아래 배치는 기본안이며, 해당 개념이 강의에 등장한 이후라면 수강 인원·발표 준비 사정에 따라 뒤 주차로 옮길 수 있다.

### Week 01. 강의소개 · 에이전트 개요 (What is an Agent?)
- **학생 발표 없음** (배정 전) — OT·발표 배정 + **교수 시연 발표**: Self-Consistency (Wang et al., 2022 · [arXiv:2203.11171](https://arxiv.org/abs/2203.11171)) — W2(프롬프팅과 추론)의 예고편.

### Week 02. 프롬프팅과 추론 (Prompting & Reasoning)
- 🟢 **Chain-of-Thought Prompting Elicits Reasoning in LLMs** — Wei et al., NeurIPS 2022 · [arXiv:2201.11903](https://arxiv.org/abs/2201.11903)
  - 필수: CoT 핵심 아이디어와 추론 창발 조건 · 선택심화: 규모별 창발 곡선, self-consistency
- 첫 발표 주이므로 1편만 배정한다 (준비 기간 1주).

### Week 03. 도구 사용 (Tool Use)
- 🟡 **Toolformer: LMs Can Teach Themselves to Use Tools** — Schick et al., NeurIPS 2023 · [arXiv:2302.04761](https://arxiv.org/abs/2302.04761)
  - 필수: self-supervised로 API 호출 위치를 학습하는 방식 · 선택심화: 호출 필터링 손실, 데이터 파이프라인
- 🟡 **ToolLLM: Mastering 16000+ Real-world APIs** — Qin et al., ICLR 2024 · [arXiv:2307.16789](https://arxiv.org/abs/2307.16789)
  - 필수: 대규모 실세계 API 학습 프레임과 DFSDT 탐색 · 선택심화: ToolBench 구축, pass/win rate
- 🔴 **ReTool: RL for Strategic Tool Use (선택읽기·RL 보강)** — 2025 · [arXiv:2504.11536](https://arxiv.org/abs/2504.11536)
  - 필수: 도구 사용 시점·방법을 RL로 최적화하는 핵심 직관 · 선택심화: 코드 인터프리터 통합, outcome 보상

### Week 04. 에이전트 루프 (ReAct)
- 🟢 **ReAct: Synergizing Reasoning and Acting in LLMs** — Yao et al., ICLR 2023 · [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)
  - 필수: Think–Act–Observe 루프 구조와 추론·행동을 엮는 이유 · 선택심화: HotpotQA·ALFWorld 셋업
- 🟡 **DeepSeek-R1: Incentivizing Reasoning via RL** — DeepSeek-AI, 2025 · [arXiv:2501.12948](https://arxiv.org/abs/2501.12948)
  - 필수: 순수 RL로 추론이 창발하는 큰 그림('aha moment')과 추론 모델이 루프 설계에 미치는 영향 · 선택심화: GRPO, cold-start 데이터
- 🟡 **STaR: Self-Taught Reasoner (선택읽기·추론 학습 계보)** — Zelikman et al., NeurIPS 2022 · [arXiv:2203.14465](https://arxiv.org/abs/2203.14465)
  - 필수: 스스로 만든 추론으로 추론을 부트스트랩하는 아이디어 · 선택심화: rationalization 트릭

### Week 05. 검색 증강 (RAG) — 1부: 기초
- 🟡 **Retrieval-Augmented Generation for Knowledge-Intensive NLP** — Lewis et al., NeurIPS 2020 · [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)
  - 필수: 파라메트릭 vs 비파라메트릭(검색) 지식 결합 · 선택심화: RAG-Sequence vs Token, retriever 공동학습
- 🟡 **HyDE: Precise Zero-Shot Dense Retrieval without Labels** — Gao et al., ACL 2023 · [arXiv:2212.10496](https://arxiv.org/abs/2212.10496)
  - 필수: 가설 문서를 생성해 검색 품질을 올리는 발상 · 선택심화: dense retriever와의 결합

### Week 06. 에이전틱 RAG + 프로토콜 (MCP)
- 🟡 **Adaptive-RAG: Adapting Retrieval to Query Complexity** — Jeong et al., NAACL 2024 · [arXiv:2403.14403](https://arxiv.org/abs/2403.14403)
  - 필수: 질의 난이도에 따라 검색 전략을 바꾸는 에이전틱 구조 · 선택심화: complexity classifier
- 🟡🔴 **Self-RAG: Learning to Retrieve, Generate, and Critique** — Asai et al., ICLR 2024 · [arXiv:2310.11511](https://arxiv.org/abs/2310.11511)
  - 필수: reflection token으로 검색 여부·품질을 스스로 판단 · 선택심화: critic 학습, segment beam search
  - 학기 유일의 중급~심화 논문 — 발표자 사정에 따라 디커플링 원칙으로 W9 이후로 이동 가능.

### Week 07. 계획과 탐색 (Planning & Search)
- 🟡 **Tree of Thoughts: Deliberate Problem Solving with LLMs** — Yao et al., NeurIPS 2023 · [arXiv:2305.10601](https://arxiv.org/abs/2305.10601)
  - 필수: 사고를 트리로 분기·탐색(BFS/DFS)하는 발상 · 선택심화: 상태 평가 함수, Game of 24
- 🟡 **ReWOO: Decoupling Reasoning from Observations** — Xu et al., 2023 · [arXiv:2305.18323](https://arxiv.org/abs/2305.18323)
  - 필수: 계획을 관찰과 분리해 토큰·호출을 줄이는 구조 · 선택심화: planner/worker/solver 모듈 분해

### Week 08. 자기반성·메타인지 (Reflection)
- 🟡 **Reflexion: Language Agents with Verbal RL** — Shinn et al., NeurIPS 2023 · [arXiv:2303.11366](https://arxiv.org/abs/2303.11366)
  - 필수: 언어 피드백이 gradient 없이 학습되는 메커니즘 · 선택심화: actor-evaluator-reflection 구조
- 🟢 **Self-Refine: Iterative Refinement with Self-Feedback** — Madaan et al., NeurIPS 2023 · [arXiv:2303.17651](https://arxiv.org/abs/2303.17651)
  - 필수: 단일 모델의 생성→비평→개선 반복 · 선택심화: 과제별 개선 폭, 피드백 프롬프트 설계

### Week 09. 컨텍스트 엔지니어링 (하네스) ⭐
- 🟡 **Lost in the Middle: How LMs Use Long Contexts** — Liu et al., TACL 2024 · [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
  - 필수: LLM이 긴 컨텍스트의 중간 정보를 잘 못 쓰는 현상 · 선택심화: 위치별 성능 곡선, 검색 문서 수 효과
- 🟡 **LLMLingua: Compressing Prompts for Accelerated Inference** — Jiang et al., EMNLP 2023 · [arXiv:2310.05736](https://arxiv.org/abs/2310.05736)
  - 필수: 프롬프트를 압축해 비용·지연을 줄이면서 성능 유지 · 선택심화: 예산 제어 압축, perplexity 기반 토큰 선택
- 🔴 **Agentic Context Engineering (선택읽기·프런티어)** — 2025 · [arXiv:2510.04618](https://arxiv.org/abs/2510.04618)
  - 필수: 컨텍스트 자체를 진화시켜 자기개선 · 선택심화: context 업데이트 정책
- 🔴 **ReasoningBank (선택읽기·프런티어)** — 2025 · [arXiv:2509.25140](https://arxiv.org/abs/2509.25140)
  - 필수: 추론 메모리를 쌓아 에이전트가 진화 · 선택심화: 메모리 항목 추출·재사용

### Week 10. 메모리 (Memory)
- 🟡 **MemGPT: Towards LLMs as Operating Systems** — Packer et al., 2023 · [arXiv:2310.08560](https://arxiv.org/abs/2310.08560)
  - 필수: 가상메모리 비유의 계층적 메모리(core/archival) · 선택심화: function-call self-editing, 페이징
- 🟡 **Mem0: Production-Ready AI Agents with Long-Term Memory** — 2025 · [arXiv:2504.19413](https://arxiv.org/abs/2504.19413)
  - 필수: 장기메모리 파이프라인(추출·갱신·검색)의 실전 설계 · 선택심화: 확장성·지연 분석, 그래프 메모리
- 🟡 **MemoryBank (선택읽기)** — Zhong et al., AAAI 2024 · [arXiv:2305.10250](https://arxiv.org/abs/2305.10250)
  - 필수: 망각 곡선 기반 메모리 갱신·검색 · 선택심화: 사용자 페르소나 유지
- 🟡 **Generative Agents (선택읽기·메모리 측면)** — Park et al., UIST 2023 · [arXiv:2304.03442](https://arxiv.org/abs/2304.03442)
  - 필수: 최신성·중요도·관련성으로 메모리를 점수화·검색 · 선택심화: memory stream 구조

### Week 11. 멀티에이전트 + LangGraph 전환점 ⭐
- 🟡 **AutoGen: Multi-Agent Conversation Framework** — Wu et al., COLM 2024 · [arXiv:2308.08155](https://arxiv.org/abs/2308.08155)
  - 필수: 대화 기반 멀티에이전트 추상화와 역할 분담 · 선택심화: conversable agent, human-in-the-loop
- 🟡 **MetaGPT: Meta Programming for Multi-Agent Collaboration** — Hong et al., ICLR 2024 · [arXiv:2308.00352](https://arxiv.org/abs/2308.00352)
  - 필수: SOP(표준운영절차)를 코드화한 협업 구조 · 선택심화: 역할별 산출물 스키마
- 🟡 **Multiagent Debate (선택읽기)** — Du et al., ICML 2024 · [arXiv:2305.14325](https://arxiv.org/abs/2305.14325)
  - 필수: 다중 에이전트 토론이 사실성·추론을 높이는 원리 · 선택심화: 수렴 동역학
- 🟡 **CAMEL: Communicative Agents (선택읽기)** — Li et al., NeurIPS 2023 · [arXiv:2303.17760](https://arxiv.org/abs/2303.17760)
  - 필수: 역할극 기반 자율 협력 프레임 · 선택심화: inception prompting

### Week 12. 컴퓨터/웹 사용 에이전트 (Computer Use)
- 🟡 **WebArena: A Realistic Web Environment for Agents** — Zhou et al., ICLR 2024 · [arXiv:2307.13854](https://arxiv.org/abs/2307.13854)
  - 필수: 실제 웹 태스크 벤치마크 구성과 왜 어려운가 · 선택심화: 4개 도메인, 성공률 격차
- 🟡 **OSWorld: Benchmarking Multimodal Agents in Real Computer Environments** — Xie et al., NeurIPS 2024 · [arXiv:2404.07972](https://arxiv.org/abs/2404.07972)
  - 필수: 실제 데스크톱 OS에서 멀티모달 에이전트를 실행 기반으로 평가 · 선택심화: 369 태스크, 스크린샷–행동 인터페이스
- 🟡 **Mind2Web (선택읽기)** — Deng et al., NeurIPS 2023 · [arXiv:2306.06070](https://arxiv.org/abs/2306.06070)
  - 필수: 실세계 웹사이트 일반화 과제와 데이터 · 선택심화: DOM 후보 선택
- 🟡 **Voyager (선택읽기·스킬 축적/자기개선)** — Wang et al., 2023 · [arXiv:2305.16291](https://arxiv.org/abs/2305.16291)
  - 필수: 스킬 라이브러리를 누적하는 평생학습 메커니즘 · 선택심화: automatic curriculum, 코드형 스킬

### Week 13. 평가와 벤치마크 (Evaluation) — 비판적 시각
- 🟢 **AI Agents That Matter** — Kapoor et al., 2024 · [arXiv:2407.01502](https://arxiv.org/abs/2407.01502)
  - 필수: 리더보드의 함정, 비용을 무시한 정확도의 문제 · 선택심화: Pareto(정확도-비용), 재현성
- 🟡 **τ-bench: Tool-Agent-User Interaction Benchmark** — Yao et al., ICLR 2025 · [arXiv:2406.12045](https://arxiv.org/abs/2406.12045)
  - 필수: 실세계 도메인 도구-에이전트-사용자 상호작용 평가 · 선택심화: pass^k, 일관성 측정

### Week 14. 신뢰·보안 (Trustworthy & Security)
- 🟡 **Not What You've Signed Up For: Indirect Prompt Injection** — Greshake et al., AISec 2023 · [arXiv:2302.12173](https://arxiv.org/abs/2302.12173)
  - 필수: 간접 프롬프트 인젝션이 왜 근본적 위협인가 · 선택심화: 실제 공격 시나리오 분류
- 🟡 **InjecAgent: Benchmarking Indirect Injection in Tool Agents** — Zhan et al., ACL 2024 · [arXiv:2403.02691](https://arxiv.org/abs/2403.02691)
  - 필수: 도구 사용 에이전트의 인젝션 취약성 측정 · 선택심화: 공격 성공률, 방어 프롬프트 효과

### Week 15. 프로덕션·단순함 — 에이전트가 꼭 필요한가
- 🟢 **Agentless: Demystifying LLM-based SE Agents** — Xia et al., 2024 · [arXiv:2407.01489](https://arxiv.org/abs/2407.01489)
  - 필수: 복잡한 에이전트 없이 단순 파이프라인이 더 나을 수 있다는 반론 · 선택심화: localize-repair-validate, SWE-bench
- 🟡 **SWE-agent: Agent-Computer Interfaces Enable Automated SE** — Yang et al., NeurIPS 2024 · [arXiv:2405.15793](https://arxiv.org/abs/2405.15793)
  - 필수: 에이전트-컴퓨터 인터페이스(ACI)가 성능을 가른다는 발견 · 선택심화: 명령·관찰 인터페이스 설계

### Week 16. 최종 발표 — 자기 하네스 관점에서 방어
- 🟢 **(보조) The Rise and Potential of LLM Based Agents: A Survey** — Xi et al., 2023 · [arXiv:2309.07864](https://arxiv.org/abs/2309.07864)
  - 필수: 학기 전체를 brain/perception/action으로 정리 · 선택심화: 미해결 과제(open problems)와 자기 연구 연결

## 발표 슬롯 계산

학생 발표 슬롯 = W2(1편) + W3~W15(각 2편) = **27슬롯**. 수강 인원에 따라 1인 1~2회로 W1 배정 때 조정한다. STaR가 선택읽기로 내려가 필수 발표 논문은 27편이다.

## 난이도 곡선

심화 논문은 사실상 W6 Self-RAG(중급~심화) 뿐(ReTool·STaR는 선택읽기). 나머지는 기초~중급으로 부산대/부경대 수준에 맞춤. 어떤 주도 '심화+심화'가 아니다. Self-RAG는 W6 배치가 이르다고 판단되면 디커플링 원칙에 따라 후주로 옮긴다.

## 이전 버전 대비 (v3 → v4)

- **v4 (2026-07-13) — 개념 의존성 기준 전면 재조정:**
  - **도구를 루프 앞으로** — function calling(W3)을 배운 뒤 ReAct 루프(W4)를 조립한다. 구 버전은 루프(W2)가 도구(W4)를 전제하는 역전이 있었고, 실습 `loop.py`가 스텁 도구 위에서 돌았다.
  - **추론 모델 주 해체** — test-time compute(self-consistency, 추론 모델 사용 관점)는 W2로 흡수, 훈련 서사는 발표(R1, W4)·선택읽기(STaR)로 위임. 참고 커리큘럼 5종 모두 추론 모델 훈련을 기초 과정에서 다루지 않는다.
  - **RAG를 계획·반성 앞으로** — 최종 산출물이 검색 에이전트이므로 검색(W5–6)을 먼저 만들고, 계획(W7)·반성(W8)은 실제 검색 위에서 동기화한다(멀티홉 분해, 검색 실패 복구).
  - **논문–주차 디커플링 명문화** — 발표는 개념 등장 이후 배치 자유. W2는 1편(첫 발표 주 부담 완화).
  - **평가 스레드 신설** — W4부터 미니 evalset, W13에서 정식화.
- v3 (2026-07): W1=강의소개·개요·환경세팅(발표 없음, 교수 시연), 이론·발표·실습 주제 정렬(→v4에서 디커플링으로 대체). RL 주 흡수.
- v2: MS/Berkeley 흐름 계승, 컨텍스트 엔지니어링(W9) 신설, 메모리 Mem0 현대화, W12 OSWorld.
- 삭제 논문은 선택읽기로 보존. 필수 28(학생 발표 27 + 보조 Survey 1) + 선택읽기 10 = 38편 전량 arXiv 검증([`papers/README.md`](../papers/README.md)).
