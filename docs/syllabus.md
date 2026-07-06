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

## 주차별 발표 논문 (상세)

각 논문의 정식 인용·발표 필수/선택 심화. 전량 arXiv 검증됨 → [`papers/README.md`](../papers/README.md).

### Week 01. 에이전트 개요 + ReAct
- 🟢 **ReAct: Synergizing Reasoning and Acting in LLMs** — Yao et al., ICLR 2023 · [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)
  - 필수: Think–Act–Observe 루프 구조와 추론·행동을 엮는 이유 · 선택심화: HotpotQA·ALFWorld 셋업
- 🟢 **Chain-of-Thought Prompting Elicits Reasoning in LLMs** — Wei et al., NeurIPS 2022 · [arXiv:2201.11903](https://arxiv.org/abs/2201.11903)
  - 필수: CoT 핵심 아이디어와 추론 창발 조건 · 선택심화: 규모별 창발 곡선, self-consistency

### Week 02. 추론 모델 (Reasoning / Test-time Compute)
- 🟡 **STaR: Self-Taught Reasoner** — Zelikman et al., NeurIPS 2022 · [arXiv:2203.14465](https://arxiv.org/abs/2203.14465)
  - 필수: 스스로 만든 추론으로 추론을 부트스트랩하는 아이디어 · 선택심화: rationalization 트릭
- 🟡 **DeepSeek-R1: Incentivizing Reasoning via RL** — DeepSeek-AI, 2025 · [arXiv:2501.12948](https://arxiv.org/abs/2501.12948)
  - 필수: 순수 RL로 추론이 창발하는 큰 그림('aha moment') · 선택심화: GRPO, cold-start 데이터

### Week 03. 도구 사용 (Tool Use)
- 🟡 **Toolformer: LMs Can Teach Themselves to Use Tools** — Schick et al., NeurIPS 2023 · [arXiv:2302.04761](https://arxiv.org/abs/2302.04761)
  - 필수: self-supervised로 API 호출 위치를 학습하는 방식 · 선택심화: 호출 필터링 손실, 데이터 파이프라인
- 🟡 **ToolLLM: Mastering 16000+ Real-world APIs** — Qin et al., ICLR 2024 · [arXiv:2307.16789](https://arxiv.org/abs/2307.16789)
  - 필수: 대규모 실세계 API 학습 프레임과 DFSDT 탐색 · 선택심화: ToolBench 구축, pass/win rate

### Week 04. 계획과 탐색 (Planning & Search)
- 🟡 **Tree of Thoughts: Deliberate Problem Solving with LLMs** — Yao et al., NeurIPS 2023 · [arXiv:2305.10601](https://arxiv.org/abs/2305.10601)
  - 필수: 사고를 트리로 분기·탐색(BFS/DFS)하는 발상 · 선택심화: 상태 평가 함수, Game of 24
- 🟡 **ReWOO: Decoupling Reasoning from Observations** — Xu et al., 2023 · [arXiv:2305.18323](https://arxiv.org/abs/2305.18323)
  - 필수: 계획을 관찰과 분리해 토큰·호출을 줄이는 구조 · 선택심화: planner/worker/solver 모듈 분해

### Week 05. 자기반성·메타인지 (Reflection)
- 🟡 **Reflexion: Language Agents with Verbal RL** — Shinn et al., NeurIPS 2023 · [arXiv:2303.11366](https://arxiv.org/abs/2303.11366)
  - 필수: 언어 피드백이 gradient 없이 학습되는 메커니즘 · 선택심화: actor-evaluator-reflection 구조
- 🟢 **Self-Refine: Iterative Refinement with Self-Feedback** — Madaan et al., NeurIPS 2023 · [arXiv:2303.17651](https://arxiv.org/abs/2303.17651)
  - 필수: 단일 모델의 생성→비평→개선 반복 · 선택심화: 과제별 개선 폭, 피드백 프롬프트 설계

### Week 06. 검색 증강 (RAG) — 1부: 기초
- 🟡 **Retrieval-Augmented Generation for Knowledge-Intensive NLP** — Lewis et al., NeurIPS 2020 · [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)
  - 필수: 파라메트릭 vs 비파라메트릭(검색) 지식 결합 · 선택심화: RAG-Sequence vs Token, retriever 공동학습
- 🟡 **HyDE: Precise Zero-Shot Dense Retrieval without Labels** — Gao et al., ACL 2023 · [arXiv:2212.10496](https://arxiv.org/abs/2212.10496)
  - 필수: 가설 문서를 생성해 검색 품질을 올리는 발상 · 선택심화: dense retriever와의 결합

### Week 07. 에이전틱 RAG + 프로토콜 (MCP)
- 🟡🔴 **Self-RAG: Learning to Retrieve, Generate, and Critique** — Asai et al., ICLR 2024 · [arXiv:2310.11511](https://arxiv.org/abs/2310.11511)
  - 필수: reflection token으로 검색 여부·품질을 스스로 판단 · 선택심화: critic 학습, segment beam search
- 🟡 **Adaptive-RAG: Adapting Retrieval to Query Complexity** — Jeong et al., NAACL 2024 · [arXiv:2403.14403](https://arxiv.org/abs/2403.14403)
  - 필수: 질의 난이도에 따라 검색 전략을 바꾸는 에이전틱 구조 · 선택심화: complexity classifier

### Week 08. 컨텍스트 엔지니어링 (하네스) ⭐
- 🟡 **Lost in the Middle: How LMs Use Long Contexts** — Liu et al., TACL 2024 · [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
  - 필수: LLM이 긴 컨텍스트의 중간 정보를 잘 못 쓰는 현상 · 선택심화: 위치별 성능 곡선, 검색 문서 수 효과
- 🟡 **LLMLingua: Compressing Prompts for Accelerated Inference** — Jiang et al., EMNLP 2023 · [arXiv:2310.05736](https://arxiv.org/abs/2310.05736)
  - 필수: 프롬프트를 압축해 비용·지연을 줄이면서 성능 유지 · 선택심화: 예산 제어 압축, perplexity 기반 토큰 선택
- 🔴 **Agentic Context Engineering (선택읽기·프런티어)** *(선택읽기)* — 2025 · [arXiv:2510.04618](https://arxiv.org/abs/2510.04618)
  - 필수: 컨텍스트 자체를 진화시켜 자기개선 · 선택심화: context 업데이트 정책
- 🔴 **ReasoningBank (선택읽기·프런티어)** *(선택읽기)* — 2025 · [arXiv:2509.25140](https://arxiv.org/abs/2509.25140)
  - 필수: 추론 메모리를 쌓아 에이전트가 진화 · 선택심화: 메모리 항목 추출·재사용

### Week 09. 메모리 (Memory)
- 🟡 **MemGPT: Towards LLMs as Operating Systems** — Packer et al., 2023 · [arXiv:2310.08560](https://arxiv.org/abs/2310.08560)
  - 필수: 가상메모리 비유의 계층적 메모리(core/archival) · 선택심화: function-call self-editing, 페이징
- 🟡 **Mem0: Production-Ready AI Agents with Long-Term Memory** — 2025 · [arXiv:2504.19413](https://arxiv.org/abs/2504.19413)
  - 필수: 장기메모리 파이프라인(추출·갱신·검색)의 실전 설계 · 선택심화: 확장성·지연 분석, 그래프 메모리
- 🟡 **MemoryBank (선택읽기)** *(선택읽기)* — Zhong et al., AAAI 2024 · [arXiv:2305.10250](https://arxiv.org/abs/2305.10250)
  - 필수: 망각 곡선 기반 메모리 갱신·검색 · 선택심화: 사용자 페르소나 유지
- 🟡 **Generative Agents (선택읽기·메모리 측면)** *(선택읽기)* — Park et al., UIST 2023 · [arXiv:2304.03442](https://arxiv.org/abs/2304.03442)
  - 필수: 최신성·중요도·관련성으로 메모리를 점수화·검색 · 선택심화: memory stream 구조

### Week 10. 멀티에이전트 + LangGraph 전환점 ⭐
- 🟡 **AutoGen: Multi-Agent Conversation Framework** — Wu et al., COLM 2024 · [arXiv:2308.08155](https://arxiv.org/abs/2308.08155)
  - 필수: 대화 기반 멀티에이전트 추상화와 역할 분담 · 선택심화: conversable agent, human-in-the-loop
- 🟡 **MetaGPT: Meta Programming for Multi-Agent Collaboration** — Hong et al., ICLR 2024 · [arXiv:2308.00352](https://arxiv.org/abs/2308.00352)
  - 필수: SOP(표준운영절차)를 코드화한 협업 구조 · 선택심화: 역할별 산출물 스키마
- 🟡 **Multiagent Debate (선택읽기)** *(선택읽기)* — Du et al., ICML 2024 · [arXiv:2305.14325](https://arxiv.org/abs/2305.14325)
  - 필수: 다중 에이전트 토론이 사실성·추론을 높이는 원리 · 선택심화: 수렴 동역학
- 🟡 **CAMEL: Communicative Agents (선택읽기)** *(선택읽기)* — Li et al., NeurIPS 2023 · [arXiv:2303.17760](https://arxiv.org/abs/2303.17760)
  - 필수: 역할극 기반 자율 협력 프레임 · 선택심화: inception prompting

### Week 11. 컴퓨터/웹 사용 에이전트 (Computer Use)
- 🟡 **WebArena: A Realistic Web Environment for Agents** — Zhou et al., ICLR 2024 · [arXiv:2307.13854](https://arxiv.org/abs/2307.13854)
  - 필수: 실제 웹 태스크 벤치마크 구성과 왜 어려운가 · 선택심화: 4개 도메인, 성공률 격차
- 🟡 **OSWorld: Benchmarking Multimodal Agents in Real Computer Environments** — Xie et al., NeurIPS 2024 · [arXiv:2404.07972](https://arxiv.org/abs/2404.07972)
  - 필수: 실제 데스크톱 OS에서 멀티모달 에이전트를 실행 기반으로 평가 · 선택심화: 369 태스크, 스크린샷–행동 인터페이스
- 🟡 **Mind2Web (선택읽기)** *(선택읽기)* — Deng et al., NeurIPS 2023 · [arXiv:2306.06070](https://arxiv.org/abs/2306.06070)
  - 필수: 실세계 웹사이트 일반화 과제와 데이터 · 선택심화: DOM 후보 선택

### Week 12. 에이전트 강화학습 (개념 1주 · 수식 생략)
- 🔴 **ReTool: RL for Strategic Tool Use in LLMs** — 2025 · *수식 유도 생략 가능* · [arXiv:2504.11536](https://arxiv.org/abs/2504.11536)
  - 필수: 도구 사용 시점·방법을 RL로 최적화하는 핵심 직관 · 선택심화: 코드 인터프리터 통합, outcome 보상
- 🟡 **Voyager (선택읽기·스킬 축적/자기개선)** *(선택읽기)* — Wang et al., 2023 · [arXiv:2305.16291](https://arxiv.org/abs/2305.16291)
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

## 난이도 곡선

심화 논문은 사실상 W12(ReTool, 직관만)와 W7 Self-RAG(중급~심화) 뿐. 나머지는 기초~중급으로 부산대/부경대 수준에 맞춤. 어떤 주도 '심화+심화'가 아니다.

## 이전 버전 대비 (v2 → 현행)

- **흐름 재편:** 임의 토픽 나열 → **MS/Berkeley 강의 흐름** 계승. 추론 모델을 앞(W2)으로, 반성을 계획 뒤(W5)로.
- **8·9주 문제 해결:** 옛 sim 주(Voyager·Generative Agents) 제거 → **컨텍스트 엔지니어링(하네스, W8)** 신설, 메모리는 **Mem0(2025)** 로 현대화.
- **W11 현대화:** Mind2Web → **OSWorld(2024)**.
- 삭제 논문은 선택읽기로 보존. 발표 논문 38편 전량 arXiv 검증([`papers/README.md`](../papers/README.md)).
