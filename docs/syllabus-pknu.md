# 강의계획서 (부경대 시스템 입력용) · Course Syllabus for PKNU System

> 과목명: 머신러닝 특론 — LLM 에이전트 (Special Topics in Machine Learning: LLM Agents) · 15주
> 대학원 · 발표+실습 병행 · 최종 산출물: 연구보조 검색·종합 에이전트

---

# [국문] 한글

## 강의목표

대규모 언어모델(LLM) 기반 에이전트의 핵심 원리를 개념 의존성 순서로 학습하고, 매주 핵심 부품을 직접 구현(from-scratch)하여 학기말에 하나의 연구보조 에이전트로 완성한다. 도구 사용·에이전트 루프·검색 증강·계획·자기반성·컨텍스트 관리·메모리·멀티에이전트·추론 경제성·평가·보안의 원리를 이해하고, 분야의 핵심 논문을 읽고 발표하며, 에이전트 시스템을 정확도와 비용의 관점에서 비판적으로 평가하는 능력을 기른다.

## 주요내용

- 추론과 프롬프팅(Chain-of-Thought, self-consistency), 추론 모델과 강화학습
- 도구 사용과 function calling, ReAct 에이전트 루프
- 검색 증강 생성(RAG), 계획과 탐색, 자기반성
- 컨텍스트 엔지니어링과 하네스(harness), 장기 메모리
- 멀티에이전트·프레임워크(LangGraph)·모델 컨텍스트 프로토콜(MCP)
- 추론 경제성(비용–정확도 교환, 라우팅·캐싱·예산)
- 평가·벤치마크, 신뢰·보안

## 강의진행방법

매주 개념 강의, 이론을 코드로 구현하는 실습(Jupyter 노트북), 팀별 논문 구술 발표로 진행한다. 실습 부품을 누적해 학기말에 하나의 연구보조 에이전트로 완성한다.

## 교재

지정 단일 교재는 없다. 주 교재는 분야의 핵심 논문(주차별 발표 논문, 전량 arXiv 공개)이며, 보조 참고자료로 다음을 사용한다.

- Microsoft, "AI Agents for Beginners"
- UC Berkeley, "Large Language Model Agents (MOOC)"
- Hugging Face, "Agents Course"
- Anthropic, "Building Effective Agents"

## 평가방법

중간고사(8주차)와 기말고사(15주차)는 서술형으로, 에이전트 시스템의 구성과 원리에 대한 이해를 중심으로 출제한다. 논문 발표는 팀별 구술로 진행하며, 매주 실습(과제)과 수업 참여를 함께 평가한다.

| 항목 | 비중 | 내용 |
|---|---|---|
| 중간고사 | 20% | 8주차 서술형 — 시스템 구성·원리 이해 |
| 기말고사 | 30% | 15주차 서술형 — 학기 전체 개념 통합 이해 |
| 과제 | 30% | 주차별 실습(구현) 노트북 — 완료 자동 점검 및 코드 정확성 채점, 프롬프트·수치 목표 검토 |
| 퀴즈 | 0% | 미실시 |
| 기타 | 20% | 팀별 논문 구술 발표 및 수업 참여 |

## 주차별 강의주제 및 상세 강의내용

| 주차 | 강의주제 | 상세 강의내용 |
|---|---|---|
| 1 | 강의소개·에이전트 개요 | 에이전트의 정의(제어 흐름을 LLM 출력이 결정하는 시스템), 구성요소(Model·Instructions·Tools·Memory), 자율성 스펙트럼. 개발환경 세팅과 LLM 호출 래퍼 실습 |
| 2 | 프롬프팅과 추론 | Chain-of-Thought로 추론을 글로 외부화하는 원리, self-consistency(다수결)와 test-time compute의 개념 |
| 3 | 자기반성 (Reflection) | 검증 없는 확정의 문제, 생성–비평–개선(Self-Refine), 시도 단위 반성(Reflexion), 외부 피드백의 성립 조건 |
| 4 | 도구 사용 | 판단(모델)과 실행(코드)의 분업, function calling, 도구 스키마 작성과 실패의 재주입 |
| 5 | 평가 (Evaluation) | 인상 판단의 구조적 실패, 평가셋과 코드 채점 지표, LLM 심판(LLM-as-a-judge)과 편향, 오류 분석, 회귀 검사 |
| 6 | 멀티에이전트 | 분업의 근거(역할 간섭·컨텍스트 성장·독립 관점), 분업 패턴, 메시지·공유 저장소와 컨텍스트 격리, 프레임워크(LangGraph)·MCP 개관, 채택 기준 |
| 7 | 에이전트 루프 · 계획과 탐색 | 결정권의 코드→모델 이양, Thought·Action·Observation 규약(ReAct), 트레이스 리딩; 과제 분해와 계획, 계획–실행 분리(ReWOO), Tree of Thoughts 탐색 |
| 8 | 중간고사 | 서술형 시험(전일) — 1~7주차 에이전트 시스템의 구성·원리 이해 |
| 9 | 검색 증강 (RAG) | 임베딩과 코사인 유사도, 색인·질의 파이프라인, 청킹과 top-k, 검색의 도구화(에이전틱 RAG) |
| 10 | 컨텍스트 엔지니어링 · 메모리 | 유한·유료·불균등한 컨텍스트, Lost in the Middle, 선별·정렬·압축, 하네스의 정의; 컨텍스트와 메모리의 구분, 장기 메모리 저장·반입(MemGPT)·갱신(Mem0) |
| 11 | 추론 모델과 강화학습 | 추론 모델(o1/R1)과 thinking budget, STaR 부트스트랩, 강화학습(정책·보상, RLHF와 RLVR의 구분), GRPO |
| 12 | 추론 경제성 · 평가 벤치마크 | 비용 구조(호출 수·토큰·모델 티어), 비용–정확도 교환, 라우팅·캐싱·예산; 에이전트 수준 벤치마크와 리더보드의 함정, pass^k, 평가 하네스 |
| 13 | 신뢰·보안 · 학기 회고 | 에이전트의 새 공격면(시스템에 대한 공격), 간접 프롬프트 인젝션, 가드레일과 다층 방어; 학기 종합(brain·perception·action 지도)과 남은 연구 문제 |
| 14 | 최종 발표 | 팀별 최종 산출물(연구보조 에이전트) 구술 발표 및 상호 평가 (전일 발표) |
| 15 | 기말고사 | 서술형 시험(전일) — 학기 전체 개념 통합 이해 |

---

# [English] 영문

## Course Objectives

Students learn the core principles of Large Language Model (LLM) agents in concept-dependency order, implementing each key component from scratch every week to build a complete research-assistant agent by the end of the term. The course covers tool use, the agent loop, retrieval augmentation, planning, self-reflection, context management, memory, multi-agent systems, inference economics, evaluation, and security. Students read and present foundational papers and develop the ability to critically evaluate agent systems in terms of both accuracy and cost.

## Main Content

- Reasoning and prompting (Chain-of-Thought, self-consistency); reasoning models and reinforcement learning
- Tool use and function calling; the ReAct agent loop
- Retrieval-Augmented Generation (RAG); planning and search; self-reflection
- Context engineering and the harness; long-term memory
- Multi-agent systems, frameworks (LangGraph), and the Model Context Protocol (MCP)
- Inference economics (cost–accuracy trade-off; routing, caching, budgeting)
- Evaluation and benchmarking; trustworthiness and security

## Teaching Methods

Each week combines a concept lecture, a hands-on implementation lab (Jupyter notebooks), and a team-based oral paper presentation. The weekly lab components accumulate into a complete research-assistant agent by the end of the term.

## Textbooks

There is no single required textbook. The primary readings are the field's foundational papers (the weekly presentation papers, all publicly available on arXiv). Supplementary references are:

- Microsoft, "AI Agents for Beginners"
- UC Berkeley, "Large Language Model Agents (MOOC)"
- Hugging Face, "Agents Course"
- Anthropic, "Building Effective Agents"

## Assessment

The midterm (Week 8) and final (Week 15) are written exams focused on understanding the structure and principles of agent systems. Paper presentations are given by teams orally, and weekly labs (assignments) and class participation are also assessed.

| Component | Weight | Description |
|---|---|---|
| Midterm | 20% | Week 8 written exam — structure and principles of the system |
| Final | 30% | Week 15 written exam — integrated understanding of the whole semester |
| Assignments | 30% | Weekly implementation labs (notebooks) — automated completion and code-correctness checks, plus review of prompts and target metrics |
| Quizzes | 0% | Not used |
| Other | 20% | Team oral paper presentations and class participation |

## Weekly Topics and Detailed Content

| Week | Topic | Detailed Content |
|---|---|---|
| 1 | Introduction & Agent Overview | Definition of an agent (a system whose control flow is determined by LLM output), components (Model, Instructions, Tools, Memory), the autonomy spectrum; environment setup and an LLM call wrapper |
| 2 | Prompting & Reasoning | Externalizing reasoning as text with Chain-of-Thought; self-consistency (majority voting) and the notion of test-time compute |
| 3 | Reasoning Models & RL | Reasoning models (o1/R1) and the thinking budget; STaR bootstrapping; reinforcement learning (policy and reward, RLHF vs. RLVR); GRPO |
| 4 | Tool Use | Division of labor between judgment (model) and execution (code); function calling; writing tool schemas and re-injecting failures |
| 5 | Agent Loop (ReAct) | Handing control from code to the model; the failure of action-only loops and its diagnosis; the Thought–Action–Observation protocol; trace reading |
| 6 | Retrieval-Augmented Generation (RAG) | Embeddings and cosine similarity; indexing and query pipelines; chunking and top-k; turning retrieval into a tool (agentic RAG) |
| 7 | Planning & Search · Self-Reflection | Task decomposition and planning; decoupling plan and execution (ReWOO); Tree of Thoughts search; the generate–critique–refine loop (Self-Refine) and attempt-level reflection (Reflexion) |
| 8 | Midterm Exam | Written exam (full session) — structure and principles of agent systems (Weeks 1–7) |
| 9 | Context Engineering · Memory | The finite, paid, and uneven context; Lost-in-the-Middle; selection, ordering, compression; the harness; distinguishing context from memory; long-term memory storage/recall (MemGPT) and update (Mem0) |
| 10 | Multi-Agent, Frameworks & MCP | Rationale and architectures for division of labor (supervisor, handoff, etc.); the graph execution model (LangGraph); the Model Context Protocol (MCP) |
| 11 | Inference Economics | Cost structure (number of calls, tokens, model tier); the cost–accuracy trade-off and compute-optimal allocation; routing, caching, budgeting; measuring cost |
| 12 | Evaluation & Benchmarking | Pitfalls of leaderboards and cost-aware evaluation; reproducibility; LLM-as-a-judge; the evaluation harness |
| 13 | Trustworthiness & Security · Retrospective | The new attack surface of agents; indirect prompt injection; guardrails and layered defense; semester synthesis (the brain–perception–action map) and open research problems |
| 14 | Final Presentations | Team oral presentations of the final project (research-assistant agent) and peer assessment (full session) |
| 15 | Final Exam | Written exam (full session) — integrated understanding of the whole semester |
