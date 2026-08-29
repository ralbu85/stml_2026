# 머신러닝 특론 — LLM 에이전트 (2026) · 강의계획서

> **부제:** 논문 읽기와 함께 만들기 — 15주, 매주 from-scratch 실습 + 논문 발표
> **대상:** 부산대/부경대 대학원 · **최종 산출물:** 연구보조 검색·종합 에이전트 (수업 논문 코퍼스 기반 RAG)
> **순서 원칙:** 개념 의존성 — 각 주는 직전 주까지 배운 것만으로 이해 가능해야 한다
> **난이도:** 🟢 기초 · 🟡 중급 · 🔴 심화

주차별 상세(보조읽기·실습·토론·발표논문·루브릭)는 [`weeks/weekNN.md`](../weeks/) 참고.
이론 전개용 참고자료·주차별 이론 플랜은 [`materials/README.md`](../materials/README.md).

## 설계 원칙

- **개념 의존성이 순서를 결정** — 에이전트를 이해하는 데 필요한 개념을 단계적으로 도입한다. 추론(W2–3)과 도구(W4)를 갖춘 뒤에 루프(W5)를 조립한다. 참고 커리큘럼(MS·Berkeley·HF·Anthropic)의 공통 순서와 일치한다.
- **논문 발표와 주차 주제의 디커플링** — 발표 논문은 해당 개념이 강의에 등장한 이후이면 배치가 자유롭다. 주차 설계가 먼저이고 논문 배치는 그 다음이다.
- **지난주 산출물의 한계가 이번 주를 동기화** — 매주 여는 5분은 우리 앱의 실패 사례에서 출발한다.
- **실습 누적 = 최종 산출물** — 매주 from-scratch로 부품을 쌓아 연구보조 에이전트를 완성. W5에 첫 완전한 에이전트가 돌고, 이후는 전부 그 개선이다.
- **from-scratch → 11주 LangGraph 전환점** — 먼저 직접 짜고, 이후 프레임워크로.
- **난이도-무관 4항목 루브릭** ([발표 가이드](presentation-guide.md)).
- **1주차 ↔ 15주차 수미상관** — "에이전트란?"로 열고 "What is an Agent?"로 닫는다.

15주 = 강의 12주(1–7, 9–13) + 전일 시험/발표 3주(8 중간고사 · 14 최종발표 · 15 기말고사). 이론 14개 장의 번호는 교수 주 순서를 따르며(v10.1 재배치, 2026-08-29 — 5장은 반성과 평가를 한 장으로 통합), 통합 주(10·12)는 두 장을 한 주에 다룬다. 아래 괄호의 "N·M장"이 그 주가 담는 이론 장이다.

| 주 | 주제 (이론 장) | 발표 논문 (난이도) | 실습(📦=최종 부품) | 대응 |
|---|---|---|---|---|
| **부품에서 루프까지** |
| 1 | 강의소개 · 에이전트 개요 (1장) | 발표 없음 (W2부터 시작) | 첫 호출 · JSON 강제 | MS01 |
| 2 | 프롬프팅과 추론 (2장) | CoT🟢 (1편 — 첫 발표 주) | CoT·예시·코드 채점 평가 (Anthropic 원본) | Bk 추론 |
| 3 | 도구 사용 (3장) | Toolformer🟡 · ToolLLM🟡 | tool use 랩 (Ng M3) + 과제(새 도구) | MS04 |
| 4 | 에이전트 루프·ReAct (4장) | ReAct🟢 | 손 루프 랩(자체 제작) — 미니 evalset 도입 + 과제(루프 가드) | HF u1 · Bk 역사 |
| 5 | 자기반성·평가 (5장) | Reflexion🟡 · LLM-as-a-Judge🟡 (+Self-Refine🟢 선택) | 반성+평가 병합 랩 (Ng M2+M4) + 차트 과제 | MS09 · Bk 평가 |
| 6 | 멀티에이전트 (6장) | AutoGen🟡 · MetaGPT🟡 | multi-agent 랩 (Ng M5) + 과제(새 의도) | MS02·08·11 |
| 7 | 계획과 탐색 (7장) | ReWOO🟡 · ToT🟡 | 연구 에이전트 (Ng GL-M5) + 과제(자기 주제) | MS07 |
| **중간고사** |
| 8 | 중간고사 (서술형·전일) | — | — | — |
| **지식·확장** |
| 9 | 검색 증강 (RAG) (8장) | RAG-Lewis🟡 · Self-RAG🟡🔴 | 리트리버 📦 | MS05 |
| 10 | 컨텍스트 엔지니어링 · 메모리 (9·10장) ⭐ | Lost-in-the-Middle🟡 · LLMLingua🟡 · MemGPT🟡 · Mem0🟡 | 메모리·그래프 📦 | MS12·13 |
| **훈련·운영** |
| 11 | 추론 모델과 강화학습 (11장) | STaR🟡 · DeepSeek-R1🟡 | thinking budget 측정 | Bk 추론 심화 |
| 12 | 추론 경제성 · 평가 벤치마크 (12·13장) | TTC-Scaling🟡 · FrugalGPT🟢 · AI Agents That Matter🟢 · τ-bench🟡 | 라우팅·비용 + 평가 하네스 | — |
| 13 | 신뢰·보안 · 학기 회고 (14장) | Indirect Injection🟡 · InjecAgent🟡 (+보조 Survey🟢) | 가드레일·인젝션 테스트 | MS06·18 |
| **마무리** |
| 14 | 최종 발표 (팀별·전일) | — | 최종 통합 발표 + 동료평가·리포트 | MS10 |
| 15 | 기말고사 (서술형·전일) | — | — | — |

> **통합 주 발표 부담:** 통합 주는 발표가 겹친다 — 10주 4편, 12주 4편. 수강 인원·시간에 맞춰 일부(예: LLMLingua·Mem0, τ-bench)를 선택읽기로 돌리거나 세션 내에 분산한다. 전반부는 v10.1 재배치로 주당 1–2편으로 고르다.

**선택읽기(프런티어/보강):** W3 ReTool(도구 RL) · W5 Self-Refine · W6 Multiagent Debate·CAMEL · W9 HyDE·Adaptive-RAG(검색 고도화) · W10 ACE·ReasoningBank(자기진화)·MemoryBank·Generative Agents · W12 RouteLLM(라우팅)·Agentless·SWE-agent(단순함·ACI).

**평가 스레드:** W4(손 루프 랩이 5문항 미니 evalset을 도입)부터 매주 같은 셋을 재채점해 트레이스 기반 개선을 습관화하고, W5에서 구성요소 평가로 정식화, W12에서 평가 하네스로 확장한다. **과제 스레드:** W2부터 매주 소과제 1건(요구사항·힌트·PASS/FAIL 체크 포함) — evalset 제작(W2) · 새 도구(W3) · 루프 가드(W4) · 차트 반성(W5) · 새 의도(W6) · 자기 주제 워크플로(W7).

## 주차별 발표 논문 (상세)

> 아래 절은 **이론 장(chapter) 단위**로 발표 논문을 정리한 것이다. 각 장이 어느 주에 배치되는지는 위 구성표를 따른다(통합 주 10·12는 두 장을 한 주에 다룸: 10=컨텍스트+메모리(9·10장), 12=경제성+벤치마크(12·13장)).

각 논문의 정식 인용·발표 필수/선택 심화. 전량 arXiv 검증됨 → [`papers/README.md`](../papers/README.md).

발표 배치는 디커플링 원칙을 따른다: 아래 배치는 기본안이며, 해당 개념이 강의에 등장한 이후라면 수강 인원·발표 준비 사정에 따라 뒤 주차로 옮길 수 있다.

### Week 01. 강의소개 · 에이전트 개요 (What is an Agent?)
- **논문 발표 없음** (배정 전) — OT·발표 배정과 발표 형식 안내. (교수 시연 발표는 2026-08 폐지.)

### Week 02. 프롬프팅과 추론 (Prompting & Reasoning)
- 🟢 **Chain-of-Thought Prompting Elicits Reasoning in LLMs** — Wei et al., NeurIPS 2022 · [arXiv:2201.11903](https://arxiv.org/abs/2201.11903)
  - 필수: CoT 핵심 아이디어와 추론 창발 조건 · 선택심화: 규모별 창발 곡선
- 첫 발표 주이므로 1편만 배정한다 (준비 기간 1주).

### Week 03 · 3장. 도구 사용 (Tool Use)
- 🟡 **Toolformer: LMs Can Teach Themselves to Use Tools** — Schick et al., NeurIPS 2023 · [arXiv:2302.04761](https://arxiv.org/abs/2302.04761)
  - 필수: self-supervised로 API 호출 위치를 학습하는 방식 · 선택심화: 호출 필터링 손실, 데이터 파이프라인
- 🟡 **ToolLLM: Mastering 16000+ Real-world APIs** — Qin et al., ICLR 2024 · [arXiv:2307.16789](https://arxiv.org/abs/2307.16789)
  - 필수: 대규모 실세계 API 학습 프레임과 DFSDT 탐색 · 선택심화: ToolBench 구축, pass/win rate
- 🔴 **ReTool: RL for Strategic Tool Use (선택읽기·RL 보강)** — 2025 · [arXiv:2504.11536](https://arxiv.org/abs/2504.11536)
  - 필수: 도구 사용 시점·방법을 RL로 최적화하는 핵심 직관 · 선택심화: 코드 인터프리터 통합, outcome 보상

### Week 04 · 4장. 에이전트 루프 (ReAct)
- 🟢 **ReAct: Synergizing Reasoning and Acting in LLMs** — Yao et al., ICLR 2023 · [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)
  - 필수: Think–Act–Observe 루프 구조와 추론·행동을 엮는 이유 · 선택심화: HotpotQA·ALFWorld 셋업
- 루프를 손으로 짓는 주로 실습 비중이 크다 — 발표는 1편.

### Week 05 · 5장. 자기반성·평가 (Reflection & Evaluation)
- 🟡 **Reflexion: Language Agents with Verbal RL** — Shinn et al., NeurIPS 2023 · [arXiv:2303.11366](https://arxiv.org/abs/2303.11366)
  - 필수: 언어 피드백이 gradient 없이 학습되는 메커니즘 · 선택심화: actor-evaluator-reflection 구조
- 🟡 **Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena** — Zheng et al., NeurIPS 2023 · [arXiv:2306.05685](https://arxiv.org/abs/2306.05685)
  - 필수: 판정자–사람 일치도의 측정과 위치·장황함·자기 선호 편향 · 선택심화: MT-Bench 설계, Arena Elo
- 🟢 **Self-Refine: Iterative Refinement with Self-Feedback (선택읽기)** — Madaan et al., NeurIPS 2023 · [arXiv:2303.17651](https://arxiv.org/abs/2303.17651)
  - 필수: 단일 모델의 생성→비평→개선 반복 · 선택심화: 과제별 개선 폭, 피드백 프롬프트 설계

### Week 06 · 6장. 멀티에이전트 (Multi-Agent) ⭐
- 🟡 **AutoGen: Multi-Agent Conversation Framework** — Wu et al., COLM 2024 · [arXiv:2308.08155](https://arxiv.org/abs/2308.08155)
  - 필수: 대화 기반 멀티에이전트 추상화와 역할 분담 · 선택심화: conversable agent, human-in-the-loop
- 🟡 **MetaGPT: Meta Programming for Multi-Agent Collaboration** — Hong et al., ICLR 2024 · [arXiv:2308.00352](https://arxiv.org/abs/2308.00352)
  - 필수: SOP(표준운영절차)를 코드화한 협업 구조 · 선택심화: 역할별 산출물 스키마
- 🟡 **Multiagent Debate (선택읽기)** — Du et al., ICML 2024 · [arXiv:2305.14325](https://arxiv.org/abs/2305.14325)
  - 필수: 다중 에이전트 토론이 사실성·추론을 높이는 원리 · 선택심화: 수렴 동역학
- 🟡 **CAMEL: Communicative Agents (선택읽기)** — Li et al., NeurIPS 2023 · [arXiv:2303.17760](https://arxiv.org/abs/2303.17760)
  - 필수: 역할극 기반 자율 협력 프레임 · 선택심화: inception prompting

### Week 07 · 7장. 계획과 탐색 (Planning & Search)
- 🟡 **Tree of Thoughts: Deliberate Problem Solving with LLMs** — Yao et al., NeurIPS 2023 · [arXiv:2305.10601](https://arxiv.org/abs/2305.10601)
  - 필수: 사고를 트리로 분기·탐색(BFS/DFS)하는 발상 · 선택심화: 상태 평가 함수, Game of 24
- 🟡 **ReWOO: Decoupling Reasoning from Observations** — Xu et al., 2023 · [arXiv:2305.18323](https://arxiv.org/abs/2305.18323)
  - 필수: 계획을 관찰과 분리해 토큰·호출을 줄이는 구조 · 선택심화: planner/worker/solver 모듈 분해

### Week 09 · 8장. 검색 증강 (RAG) — 기초와 에이전틱
- 🟡 **Retrieval-Augmented Generation for Knowledge-Intensive NLP** — Lewis et al., NeurIPS 2020 · [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)
  - 필수: 파라메트릭 vs 비파라메트릭(검색) 지식 결합 · 선택심화: RAG-Sequence vs Token, retriever 공동학습
- 🟡🔴 **Self-RAG: Learning to Retrieve, Generate, and Critique** — Asai et al., ICLR 2024 · [arXiv:2310.11511](https://arxiv.org/abs/2310.11511)
  - 필수: reflection token으로 검색 여부·품질을 스스로 판단 · 선택심화: critic 학습, segment beam search
- 🟡 **HyDE (선택읽기)** — Gao et al., ACL 2023 · [arXiv:2212.10496](https://arxiv.org/abs/2212.10496)
  - 필수: 가설 문서를 생성해 검색 품질을 올리는 발상 · 선택심화: dense retriever와의 결합
- 🟡 **Adaptive-RAG (선택읽기)** — Jeong et al., NAACL 2024 · [arXiv:2403.14403](https://arxiv.org/abs/2403.14403)
  - 필수: 질의 난이도에 따라 검색 전략을 바꾸는 에이전틱 구조 · 선택심화: complexity classifier

### Week 10 · 9장. 컨텍스트 엔지니어링 (하네스) ⭐
- 🟡 **Lost in the Middle: How LMs Use Long Contexts** — Liu et al., TACL 2024 · [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
  - 필수: LLM이 긴 컨텍스트의 중간 정보를 잘 못 쓰는 현상 · 선택심화: 위치별 성능 곡선, 검색 문서 수 효과
- 🟡 **LLMLingua: Compressing Prompts for Accelerated Inference** — Jiang et al., EMNLP 2023 · [arXiv:2310.05736](https://arxiv.org/abs/2310.05736)
  - 필수: 프롬프트를 압축해 비용·지연을 줄이면서 성능 유지 · 선택심화: 예산 제어 압축, perplexity 기반 토큰 선택
- 🔴 **Agentic Context Engineering (선택읽기·프런티어)** — 2025 · [arXiv:2510.04618](https://arxiv.org/abs/2510.04618)
  - 필수: 컨텍스트 자체를 진화시켜 자기개선 · 선택심화: context 업데이트 정책
- 🔴 **ReasoningBank (선택읽기·프런티어)** — 2025 · [arXiv:2509.25140](https://arxiv.org/abs/2509.25140)
  - 필수: 추론 메모리를 쌓아 에이전트가 진화 · 선택심화: 메모리 항목 추출·재사용

### Week 10 · 10장. 메모리 (Memory)
- 🟡 **MemGPT: Towards LLMs as Operating Systems** — Packer et al., 2023 · [arXiv:2310.08560](https://arxiv.org/abs/2310.08560)
  - 필수: 가상메모리 비유의 계층적 메모리(core/archival) · 선택심화: function-call self-editing, 페이징
- 🟡 **Mem0: Production-Ready AI Agents with Long-Term Memory** — 2025 · [arXiv:2504.19413](https://arxiv.org/abs/2504.19413)
  - 필수: 장기메모리 파이프라인(추출·갱신·검색)의 실전 설계 · 선택심화: 확장성·지연 분석, 그래프 메모리
- 🟡 **MemoryBank (선택읽기)** — Zhong et al., AAAI 2024 · [arXiv:2305.10250](https://arxiv.org/abs/2305.10250)
  - 필수: 망각 곡선 기반 메모리 갱신·검색 · 선택심화: 사용자 페르소나 유지
- 🟡 **Generative Agents (선택읽기·메모리 측면)** — Park et al., UIST 2023 · [arXiv:2304.03442](https://arxiv.org/abs/2304.03442)
  - 필수: 최신성·중요도·관련성으로 메모리를 점수화·검색 · 선택심화: memory stream 구조

### Week 11 · 11장. 추론 모델과 강화학습 (Reasoning Models & RL)
- 🟡 **STaR: Self-Taught Reasoner** — Zelikman et al., NeurIPS 2022 · [arXiv:2203.14465](https://arxiv.org/abs/2203.14465)
  - 필수: 스스로 만든 추론으로 추론을 부트스트랩하는 아이디어 · 선택심화: rationalization 트릭
- 🟡 **DeepSeek-R1: Incentivizing Reasoning via RL** — DeepSeek-AI, 2025 · [arXiv:2501.12948](https://arxiv.org/abs/2501.12948)
  - 필수: 순수 RL로 추론이 창발하는 큰 그림('aha moment') · 선택심화: GRPO, cold-start 데이터
  - RL 사전 지식을 가정하지 않는다 — 강의에서 정의 수준의 최소 개념을 제공한다.

### Week 12 · 12장. 추론 경제성 (Inference Economics)
- 🟡 **Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters** — Snell et al., 2024 · [arXiv:2408.03314](https://arxiv.org/abs/2408.03314)
  - 필수: 추론을 늘릴 때의 정확도 곡선과 과제 난이도별 compute-optimal 배분 · 선택심화: 작은 모델+테스트타임이 큰 모델을 앞서는 조건, FLOPs-matched 비교
- 🟢 **FrugalGPT: How to Use LLMs While Reducing Cost and Improving Performance** — Chen et al., 2023 · [arXiv:2305.05176](https://arxiv.org/abs/2305.05176)
  - 필수: 캐스케이드·프롬프트 적응·근사로 비용을 낮추는 세 전략 · 선택심화: 최상위 모델 성능을 유지하며 비용을 대폭 줄이는 수치
- 🟡 **RouteLLM (선택읽기·모델 라우팅)** — Ong et al., 2024 · [arXiv:2406.18665](https://arxiv.org/abs/2406.18665)
  - 필수: 강·약 모델 사이 라우터를 선호 데이터로 학습해 비용을 낮추는 발상 · 선택심화: 품질을 유지하며 비용 절반 이하
- 🟢🟡 **Agentless / SWE-agent (선택읽기·단순함 반론)** — Xia et al., 2024 · [arXiv:2407.01489](https://arxiv.org/abs/2407.01489) / Yang et al., NeurIPS 2024 · [arXiv:2405.15793](https://arxiv.org/abs/2405.15793)
  - 필수: 복잡한 에이전트 없이 단순 파이프라인이 나을 수 있다(Agentless), ACI 설계가 성능을 가른다(SWE-agent) · 12.6의 워크플로우–에이전트 비용 교환과 연결(→ W15 종합 토론)

### Week 12 · 13장. 평가와 벤치마크 (Benchmarks) — 비판적 시각
- 🟢 **AI Agents That Matter** — Kapoor et al., 2024 · [arXiv:2407.01502](https://arxiv.org/abs/2407.01502)
  - 필수: 리더보드의 함정, 비용을 무시한 정확도의 문제 · 선택심화: Pareto(정확도-비용), 재현성
- 🟡 **τ-bench: Tool-Agent-User Interaction Benchmark** — Yao et al., ICLR 2025 · [arXiv:2406.12045](https://arxiv.org/abs/2406.12045)
  - 필수: 실세계 도메인 도구-에이전트-사용자 상호작용 평가 · 선택심화: pass^k, 일관성 측정

### Week 13 · 14장. 신뢰·보안 (Trustworthy & Security)
- 🟡 **Not What You've Signed Up For: Indirect Prompt Injection** — Greshake et al., AISec 2023 · [arXiv:2302.12173](https://arxiv.org/abs/2302.12173)
  - 필수: 간접 프롬프트 인젝션이 왜 근본적 위협인가 · 선택심화: 실제 공격 시나리오 분류
- 🟡 **InjecAgent: Benchmarking Indirect Injection in Tool Agents** — Zhan et al., ACL 2024 · [arXiv:2403.02691](https://arxiv.org/abs/2403.02691)
  - 필수: 도구 사용 에이전트의 인젝션 취약성 측정 · 선택심화: 공격 성공률, 방어 프롬프트 효과

### Week 15. 최종 발표 · 종합 — 자기 하네스 관점에서 방어
- 🟢 **(보조) The Rise and Potential of LLM Based Agents: A Survey** — Xi et al., 2023 · [arXiv:2309.07864](https://arxiv.org/abs/2309.07864)
  - 필수: 학기 전체를 brain/perception/action으로 정리 · 선택심화: 미해결 과제(open problems)와 자기 연구 연결
- **종합 토론 — 에이전트가 꼭 필요한가:** 구 프로덕션·단순함 주가 이 종합으로 흡수됐다. 단순 파이프라인 대 복잡한 에이전트, 단순함과 비용의 균형을 W12(추론 경제성)의 워크플로우–에이전트 비용 교환 위에서 토론한다. 근거 논문 Agentless·SWE-agent는 W12 선택읽기.
- 최종 통합 산출물 발표 + 동료평가 + 리포트.

## 발표 슬롯 계산

학생 발표 슬롯 = W2·W5(각 1편) + W3·W4·W6·W9·W11·W13(각 2편) + W7(3편) + W10·W12(각 4편) = **25슬롯**. 수강 인원에 따라 1인 1~2회로 W1 배정 때 조정하며, 통합 주의 3~4편은 필요 시 일부를 선택읽기로 돌린다. 필수 발표 논문 25편 + 보조(Survey) 1편.

## 난이도 곡선

심화 논문은 사실상 W6 Self-RAG(중급~심화) 뿐(ReTool은 선택읽기). 나머지는 기초~중급으로 부산대/부경대 수준에 맞춤. 어떤 주도 '심화+심화'가 아니다. Self-RAG는 필요시 디커플링 원칙에 따라 후주로 옮긴다.

## 이전 버전 대비 (v8 → v9)

- **v9 (2026-08-28) — 이론–실습 정렬 재배치 (안 A):**
  - **실습 열 고정 원칙:** W3부터 Ng *Agentic AI* 모듈을 순서대로 연속 실행(M2→M3→M4→M5→GL-M5)하고, 이론 주차를 실습에 맞춰 재배열. 12개 교수 주 전부 이론–실습 일치.
  - 이동: 자기반성 8장→3장(W3) · 평가를 구성요소 수준(신설 5장, W5)과 벤치마크(14장, W12)로 분리 · 멀티에이전트 11장→6장(W6) · 루프 5장→7장, 계획 7장→8장(W7 통합) · RAG 6장→9장(W9) · 컨텍스트 9장→10장, 메모리 10장→11장(W10 통합) · 추론 모델·RL 3장→12장(W11) · 경제성 12장→13장(W12 통합) · 보안·회고 14·15장→15장(W13).
  - 발표 이동: Self-Refine·Reflexion→W3 · LLM-as-a-Judge(Zheng, 신규)→W5 · AutoGen·MetaGPT→W6 · ReAct→W7 · RAG·Self-RAG→W9 · STaR·R1→W11 · Snell·FrugalGPT→W12. 슬롯 24→25.
  - 신규 실습: W11 thinking budget 측정(`anthropic-cookbook/extended_thinking` 원본). 상세 근거: [`lab-theory-realignment.md`](lab-theory-realignment.md).

## 이전 버전 대비 (v7 → v8)

- **v8 (2026-07-21) — 15주 시험일 구조:**
  - **8주 중간고사 · 14주 최종발표 · 15주 기말고사**를 전일 시험/발표 주로 지정(강의 없음). 시험은 서술형(시스템 이해 중심), 발표는 팀별 구술.
  - 강의 12주 확보를 위해 인접 두 장을 한 주에 통합: **7주 계획+반성(7·8장) · 9주 컨텍스트+메모리(9·10장) · 13주 보안+회고(14·15장)**. 이론 15개 장은 파일·번호 그대로이며 주차 배치만 변경.
  - 이후 주차 순연: 멀티(11장)→10주 · 경제성(12장)→11주 · 평가(13장)→12주. 발표 슬롯 24 유지(통합 주는 4편 배정, 초과 시 선택읽기로).

## 이전 버전 대비 (v6 → v7)

- **v7 (2026-07-21) — 15주로 축소 + 추론 경제성 도입:**
  - **W12 컴퓨터·웹 사용 → 추론 경제성으로 교체.** 컴퓨터 사용은 "같은 루프, 새 도메인"이라 이론 밀도가 낮고 실질(WebArena/OSWorld 수치)은 발표 위임이었다. 대신 W2·3·7·8·9에 흩어진 test-time compute의 비용–정확도 교환을 한 주로 통합(비용 구조·compute-optimal·라우팅/캐싱/예산·측정). 발표 Snell·FrugalGPT.
  - **프로덕션·단순함 주(구 W15) 해체.** 단순함·워크플로우 대 에이전트 비용 교환은 W12(추론 경제성)와 W15 최종 종합으로 흡수, Agentless·SWE-agent는 W12 선택읽기로. 최종 발표가 W15.
  - 발표 슬롯 26 → 24. WebArena·OSWorld·Mind2Web·Voyager(컴퓨터 사용)는 목록에서 제외. 컴퓨터 사용의 행동 grounding 개념은 삭제(13장 흡수 안 함).

## 이전 버전 대비 (v5 → v6)

- **v6 (2026-07-13) — W3 재편: 추론 모델과 강화학습:**
  - W3을 **추론 모델과 강화학습**으로 재편 — 추론 모델(내재화·thinking budget), 훈련 데이터 문제, STaR, 강화학습 정의(정책·보상, RLHF vs RLVR), R1(GRPO·창발), 보상 해킹·증류.
  - **self-consistency·test-time compute를 W2로 이관** — 개념 의존상 CoT의 직접 연장이며, W1 교수 시연(Self-Consistency)의 예고 대상도 W2로 일치.
  - W3 실습(self-consistency 구현)은 유지하되 "추론 모델이 내재화한 호출자 쪽 반복 절차의 실물"로 재정위. 주차 구성·발표 슬롯 불변.

## 이전 버전 대비 (v4 → v5)

- **v5 (2026-07-13) — 추론 모델 주 복원:**
  - v4에서 해체했던 추론 모델을 **W3 독립 주로 복원** (test-time compute·self-consistency·내재화·STaR·R1). 2025–26 에이전트의 토대 주제를 한 주에 압축·산개시킨 것이 오류였다.
  - 자리 확보를 위해 **RAG 두 주를 W6 한 주로 통합**(기초+에이전틱). HyDE·Adaptive-RAG는 선택읽기로. **MCP는 W11**(프레임워크·생태계 주)로 이동.
  - 도구 W4, 에이전트 루프 W5로 순연. 발표 슬롯 26.

## 이전 버전 대비 (v3 → v4)

- **v4 (2026-07-13) — 개념 의존성 기준 전면 재조정:**
  - **도구를 루프 앞으로** — function calling(W3)을 배운 뒤 ReAct 루프(W4)를 조립한다. 구 버전은 루프(W2)가 도구(W4)를 전제하는 역전이 있었고, 실습 `loop.py`가 스텁 도구 위에서 돌았다.
  - **추론 모델 주 해체** — test-time compute(self-consistency, 추론 모델 사용 관점)는 W2로 흡수, 훈련 서사는 발표(R1, W4)·선택읽기(STaR)로 위임. 참고 커리큘럼 5종 모두 추론 모델 훈련을 기초 과정에서 다루지 않는다.
  - **RAG를 계획·반성 앞으로** — 최종 산출물이 검색 에이전트이므로 검색(W5–6)을 먼저 만들고, 계획(W7)·반성(W8)은 실제 검색 위에서 동기화한다(멀티홉 분해, 검색 실패 복구).
  - **논문–주차 디커플링 명문화** — 발표는 개념 등장 이후 배치 자유. W2는 1편(첫 발표 주 부담 완화).
  - **평가 스레드 신설** — W4부터 미니 evalset, W13에서 정식화.
- v3 (2026-07): W1=강의소개·개요·환경세팅(발표 없음, 교수 시연), 이론·발표·실습 주제 정렬(→v4에서 디커플링으로 대체). RL 주 흡수.
- v2: MS/Berkeley 흐름 계승, 컨텍스트 엔지니어링(W9) 신설, 메모리 Mem0 현대화, W12 OSWorld.
- 삭제 논문은 선택읽기로 보존. 필수 25(학생 발표 24 + 보조 Survey 1) + 선택읽기 12 = 37편 전량 arXiv 검증([`papers/README.md`](../papers/README.md)).
