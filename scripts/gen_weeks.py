#!/usr/bin/env python3
import os

ROOT = "/workspace/BALAB_Prof/Lecture_STML_2026/weeks"

# 흐름: Microsoft ai-agents-for-beginners + Berkeley LLM Agents 재구성.
# week: (part, title, aux, practice, discussion, [papers])
# paper: (diff, title, cite, must, deep, pdf, optional)
W = {
1:("토대","강의소개 · 에이전트 개요 (What is an Agent?)",
 "Anthropic — *Building Effective Agents* (워크플로우 vs 에이전트) · MS01",
 "환경 세팅(Python 3.10+·aisuite·API 키/Ollama) → 원시 HTTP 호출로 API 내부 확인 → LLM 래퍼",
 "에이전트와 단순 워크플로우의 경계는? 챗봇은 에이전트의 전부인가(폼팩터)?",
 []),
2:("토대","CoT → ReAct — 추론과 행동의 결합",
 "Lilian Weng — *LLM Powered Autonomous Agents* · Berkeley 에이전트 역사 강의",
 "ReAct(Thought→Action→Observation) while 루프 직접 구현",
 "CoT 없는 ReAct는 가능한가? 추론과 행동을 섞으면 왜 둘 다 좋아지나?",
 [("🟢","ReAct: Synergizing Reasoning and Acting in LLMs","Yao et al., ICLR 2023 · arXiv:2210.03629",
   "Think–Act–Observe 루프 구조와 추론·행동을 엮는 이유","HotpotQA·ALFWorld 셋업","W02_ReAct_2210.03629.pdf",False),
  ("🟢","Chain-of-Thought Prompting Elicits Reasoning in LLMs","Wei et al., NeurIPS 2022 · arXiv:2201.11903",
   "CoT 핵심 아이디어와 추론 창발 조건","규모별 창발 곡선, self-consistency","W02_Chain-of-Thought_2201.11903.pdf",False)]),
3:("토대","추론 모델 (Reasoning / Test-time Compute)",
 "Lilian Weng — *Why We Think* — test-time compute 직관 · Berkeley 추론 강의",
 "self-consistency / 다중 샘플 추론 비교",
 "'더 오래 생각하기'는 왜 성능을 올리나? 언제 과한가?",
 [("🟡","STaR: Self-Taught Reasoner","Zelikman et al., NeurIPS 2022 · arXiv:2203.14465",
   "스스로 만든 추론으로 추론을 부트스트랩하는 아이디어","rationalization 트릭","W03_STaR_2203.14465.pdf",False),
  ("🟡","DeepSeek-R1: Incentivizing Reasoning via RL","DeepSeek-AI, 2025 · arXiv:2501.12948",
   "순수 RL로 추론이 창발하는 큰 그림('aha moment')","GRPO, cold-start 데이터","W03_DeepSeek-R1_2501.12948.pdf",False)]),
4:("핵심 디자인 패턴","도구 사용 (Tool Use)",
 "Anthropic — *Writing Effective Tools for Agents* · MS04",
 "도구 레지스트리·파싱·실행 직접 구현 (계산기·검색 함수)",
 "도구가 많아질수록 좋은가? 도구 절벽(tool cliff)이 생기는 이유는?",
 [("🟡","Toolformer: LMs Can Teach Themselves to Use Tools","Schick et al., NeurIPS 2023 · arXiv:2302.04761",
   "self-supervised로 API 호출 위치를 학습하는 방식","호출 필터링 손실, 데이터 파이프라인","W04_Toolformer_2302.04761.pdf",False),
  ("🟡","ToolLLM: Mastering 16000+ Real-world APIs","Qin et al., ICLR 2024 · arXiv:2307.16789",
   "대규모 실세계 API 학습 프레임과 DFSDT 탐색","ToolBench 구축, pass/win rate","W04_ToolLLM_2307.16789.pdf",False),
  ("🔴","ReTool: RL for Strategic Tool Use (선택읽기·RL 보강)","2025 · arXiv:2504.11536",
   "도구 사용 시점·방법을 RL로 최적화하는 핵심 직관","코드 인터프리터 통합, outcome 보상","W04_opt-ReTool_2504.11536.pdf",True)]),
5:("핵심 디자인 패턴","계획과 탐색 (Planning & Search)",
 "LangChain — *Plan-and-Execute Agents* · MS07",
 "탐색 기반 추론(트리 분기) 미니 구현, 계획–실행 분리",
 "탐색 비용 대비 성능 이득은 언제 정당한가?",
 [("🟡","Tree of Thoughts: Deliberate Problem Solving with LLMs","Yao et al., NeurIPS 2023 · arXiv:2305.10601",
   "사고를 트리로 분기·탐색(BFS/DFS)하는 발상","상태 평가 함수, Game of 24","W05_Tree-of-Thoughts_2305.10601.pdf",False),
  ("🟡","ReWOO: Decoupling Reasoning from Observations","Xu et al., 2023 · arXiv:2305.18323",
   "계획을 관찰과 분리해 토큰·호출을 줄이는 구조","planner/worker/solver 모듈 분해","W05_ReWOO_2305.18323.pdf",False)]),
6:("핵심 디자인 패턴","자기반성·메타인지 (Reflection)",
 "Anthropic — *Demystifying Evals for AI Agents* · MS09",
 "실패→언어 피드백→재시도 루프를 ReAct에 추가",
 "자기반성은 진짜 개선인가, 아니면 같은 오류의 반복인가?",
 [("🟡","Reflexion: Language Agents with Verbal RL","Shinn et al., NeurIPS 2023 · arXiv:2303.11366",
   "언어 피드백이 gradient 없이 학습되는 메커니즘","actor-evaluator-reflection 구조","W06_Reflexion_2303.11366.pdf",False),
  ("🟢","Self-Refine: Iterative Refinement with Self-Feedback","Madaan et al., NeurIPS 2023 · arXiv:2303.17651",
   "단일 모델의 생성→비평→개선 반복","과제별 개선 폭, 피드백 프롬프트 설계","W06_Self-Refine_2303.17651.pdf",False)]),
7:("지식·컨텍스트·기억","검색 증강 (RAG) — 1부: 기초",
 "Anthropic — *Contextual Retrieval* / LlamaIndex RAG 가이드 · MS05",
 "임베딩→유사도→컨텍스트 주입 검색 직접 구현 *(최종 프로젝트 부품 1)*",
 "언제 검색해야 하는가? 항상 검색이 답인가?",
 [("🟡","Retrieval-Augmented Generation for Knowledge-Intensive NLP","Lewis et al., NeurIPS 2020 · arXiv:2005.11401",
   "파라메트릭 vs 비파라메트릭(검색) 지식 결합","RAG-Sequence vs Token, retriever 공동학습","W07_RAG-Lewis_2005.11401.pdf",False),
  ("🟡","HyDE: Precise Zero-Shot Dense Retrieval without Labels","Gao et al., ACL 2023 · arXiv:2212.10496",
   "가설 문서를 생성해 검색 품질을 올리는 발상","dense retriever와의 결합","W07_HyDE_2212.10496.pdf",False)]),
8:("지식·컨텍스트·기억","에이전틱 RAG + 프로토콜 (MCP)",
 "Anthropic — *Code Execution with MCP* · MS05·11",
 "검색을 '도구'로 노출하고 에이전트가 단계별로 호출하게 개조 *(최종 프로젝트 부품 2)*",
 "RAG를 도구로 만들면 무엇이 좋아지고 무엇이 어려워지나?",
 [("🟡🔴","Self-RAG: Learning to Retrieve, Generate, and Critique","Asai et al., ICLR 2024 · arXiv:2310.11511",
   "reflection token으로 검색 여부·품질을 스스로 판단","critic 학습, segment beam search","W08_Self-RAG_2310.11511.pdf",False),
  ("🟡","Adaptive-RAG: Adapting Retrieval to Query Complexity","Jeong et al., NAACL 2024 · arXiv:2403.14403",
   "질의 난이도에 따라 검색 전략을 바꾸는 에이전틱 구조","complexity classifier","W08_Adaptive-RAG_2403.14403.pdf",False)]),
9:("지식·컨텍스트·기억","컨텍스트 엔지니어링 (하네스) ⭐",
 "Anthropic — *Effective Context Engineering* + HumanLayer — *Skill Issue: Harness Engineering* · MS12",
 "컨텍스트 예산·압축·큐레이션을 하네스에 내장 (긴 컨텍스트 관리)",
 "컨텍스트는 왜 유한 자원인가? 무엇을 넣고 무엇을 버려야 하나?",
 [("🟡","Lost in the Middle: How LMs Use Long Contexts","Liu et al., TACL 2024 · arXiv:2307.03172",
   "LLM이 긴 컨텍스트의 중간 정보를 잘 못 쓰는 현상","위치별 성능 곡선, 검색 문서 수 효과","W09_Lost-in-the-Middle_2307.03172.pdf",False),
  ("🟡","LLMLingua: Compressing Prompts for Accelerated Inference","Jiang et al., EMNLP 2023 · arXiv:2310.05736",
   "프롬프트를 압축해 비용·지연을 줄이면서 성능 유지","예산 제어 압축, perplexity 기반 토큰 선택","W09_LLMLingua_2310.05736.pdf",False),
  ("🔴","Agentic Context Engineering (선택읽기·프런티어)","2025 · arXiv:2510.04618",
   "컨텍스트 자체를 진화시켜 자기개선","context 업데이트 정책","W09_opt-Agentic-Context-Engineering_2510.04618.pdf",True),
  ("🔴","ReasoningBank (선택읽기·프런티어)","2025 · arXiv:2509.25140",
   "추론 메모리를 쌓아 에이전트가 진화","메모리 항목 추출·재사용","W09_opt-ReasoningBank_2509.25140.pdf",True)]),
10:("지식·컨텍스트·기억","메모리 (Memory)",
 "Letta (MemGPT) — *Agent Memory Blog* (3계층 메모리) · MS13",
 "메모리 스트림 구현(저장·검색), 외부 메모리 통합 *(최종 프로젝트 부품 3)*",
 "무엇을 기억하고 무엇을 잊어야 하는가? 메모리 검색의 기준은?",
 [("🟡","MemGPT: Towards LLMs as Operating Systems","Packer et al., 2023 · arXiv:2310.08560",
   "가상메모리 비유의 계층적 메모리(core/archival)","function-call self-editing, 페이징","W10_MemGPT_2310.08560.pdf",False),
  ("🟡","Mem0: Production-Ready AI Agents with Long-Term Memory","2025 · arXiv:2504.19413",
   "장기메모리 파이프라인(추출·갱신·검색)의 실전 설계","확장성·지연 분석, 그래프 메모리","W10_Mem0_2504.19413.pdf",False),
  ("🟡","MemoryBank (선택읽기)","Zhong et al., AAAI 2024 · arXiv:2305.10250",
   "망각 곡선 기반 메모리 갱신·검색","사용자 페르소나 유지","W10_opt-MemoryBank_2305.10250.pdf",True),
  ("🟡","Generative Agents (선택읽기·메모리 측면)","Park et al., UIST 2023 · arXiv:2304.03442",
   "최신성·중요도·관련성으로 메모리를 점수화·검색","memory stream 구조","W10_opt-Generative-Agents_2304.03442.pdf",True)]),
11:("협업·환경","멀티에이전트 + LangGraph 전환점 ⭐",
 "LangChain — *Choosing the Right Multi-Agent Architecture* · MS02·08",
 "역할 분담 멀티에이전트를 **LangGraph로 재구현·비교** (직접 구현 대비)",
 "멀티에이전트가 단일 에이전트보다 정말 나은가? 언제 과한가?",
 [("🟡","AutoGen: Multi-Agent Conversation Framework","Wu et al., COLM 2024 · arXiv:2308.08155",
   "대화 기반 멀티에이전트 추상화와 역할 분담","conversable agent, human-in-the-loop","W11_AutoGen_2308.08155.pdf",False),
  ("🟡","MetaGPT: Meta Programming for Multi-Agent Collaboration","Hong et al., ICLR 2024 · arXiv:2308.00352",
   "SOP(표준운영절차)를 코드화한 협업 구조","역할별 산출물 스키마","W11_MetaGPT_2308.00352.pdf",False),
  ("🟡","Multiagent Debate (선택읽기)","Du et al., ICML 2024 · arXiv:2305.14325",
   "다중 에이전트 토론이 사실성·추론을 높이는 원리","수렴 동역학","W11_opt-Multiagent-Debate_2305.14325.pdf",True),
  ("🟡","CAMEL: Communicative Agents (선택읽기)","Li et al., NeurIPS 2023 · arXiv:2303.17760",
   "역할극 기반 자율 협력 프레임","inception prompting","W11_opt-CAMEL_2303.17760.pdf",True)]),
12:("협업·환경","컴퓨터/웹 사용 에이전트 (Computer Use)",
 "*OS Agents: A Survey on MLLM-based Agents* (ACL 2025) · MS15",
 "브라우저/OS 환경에서 관찰-행동 루프 (간단한 웹/데스크톱 태스크)",
 "텍스트 도구 호출 vs 화면 클릭 — 무엇이 언제 나은가?",
 [("🟡","WebArena: A Realistic Web Environment for Agents","Zhou et al., ICLR 2024 · arXiv:2307.13854",
   "실제 웹 태스크 벤치마크 구성과 왜 어려운가","4개 도메인, 성공률 격차","W12_WebArena_2307.13854.pdf",False),
  ("🟡","OSWorld: Benchmarking Multimodal Agents in Real Computer Environments","Xie et al., NeurIPS 2024 · arXiv:2404.07972",
   "실제 데스크톱 OS에서 멀티모달 에이전트를 실행 기반으로 평가","369 태스크, 스크린샷–행동 인터페이스","W12_OSWorld_2404.07972.pdf",False),
  ("🟡","Mind2Web (선택읽기)","Deng et al., NeurIPS 2023 · arXiv:2306.06070",
   "실세계 웹사이트 일반화 과제와 데이터","DOM 후보 선택","W12_opt-Mind2Web_2306.06070.pdf",True),
  ("🟡","Voyager (선택읽기·스킬 축적/자기개선)","Wang et al., 2023 · arXiv:2305.16291",
   "스킬 라이브러리를 누적하는 평생학습 메커니즘","automatic curriculum, 코드형 스킬","W12_opt-Voyager_2305.16291.pdf",True)]),
13:("학습·품질·운영","평가와 벤치마크 (Evaluation) — 비판적 시각",
 "LangChain — *Agent Evaluation Readiness Checklist* · Berkeley 평가 강의",
 "최종 프로젝트 설계 + 평가 하네스(정확도·비용·재현성) 골격",
 "무엇을 측정해야 하는가? 우리 RAG 에이전트의 성공 기준은?",
 [("🟢","AI Agents That Matter","Kapoor et al., 2024 · arXiv:2407.01502",
   "리더보드의 함정, 비용을 무시한 정확도의 문제","Pareto(정확도-비용), 재현성","W13_AI-Agents-That-Matter_2407.01502.pdf",False),
  ("🟡","τ-bench: Tool-Agent-User Interaction Benchmark","Yao et al., ICLR 2025 · arXiv:2406.12045",
   "실세계 도메인 도구-에이전트-사용자 상호작용 평가","pass^k, 일관성 측정","W13_tau-bench_2406.12045.pdf",False)]),
14:("학습·품질·운영","신뢰·보안 (Trustworthy & Security)",
 "*OWASP Top 10 for LLM Applications* · MS06·18",
 "내 에이전트에 가드레일 추가 + 인젝션 공격 테스트",
 "행동하는 에이전트의 가장 위험한 실패는? 어디까지 자동화를 믿을 수 있나?",
 [("🟡","Not What You've Signed Up For: Indirect Prompt Injection","Greshake et al., AISec 2023 · arXiv:2302.12173",
   "간접 프롬프트 인젝션이 왜 근본적 위협인가","실제 공격 시나리오 분류","W14_Indirect-Prompt-Injection_2302.12173.pdf",False),
  ("🟡","InjecAgent: Benchmarking Indirect Injection in Tool Agents","Zhan et al., ACL 2024 · arXiv:2403.02691",
   "도구 사용 에이전트의 인젝션 취약성 측정","공격 성공률, 방어 프롬프트 효과","W14_InjecAgent_2403.02691.pdf",False)]),
15:("학습·품질·운영","프로덕션·단순함 — 에이전트가 꼭 필요한가",
 "HumanLayer — *Skill Issue: Harness Engineering* · MS10",
 "최종 프로젝트 구현 집중 (검색·컨텍스트·메모리·평가 통합)",
 "복잡한 에이전트 vs 단순 파이프라인 — 우리 과제엔 무엇이 맞나?",
 [("🟢","Agentless: Demystifying LLM-based SE Agents","Xia et al., 2024 · arXiv:2407.01489",
   "복잡한 에이전트 없이 단순 파이프라인이 더 나을 수 있다는 반론","localize-repair-validate, SWE-bench","W15_Agentless_2407.01489.pdf",False),
  ("🟡","SWE-agent: Agent-Computer Interfaces Enable Automated SE","Yang et al., NeurIPS 2024 · arXiv:2405.15793",
   "에이전트-컴퓨터 인터페이스(ACI)가 성능을 가른다는 발견","명령·관찰 인터페이스 설계","W15_SWE-agent_2405.15793.pdf",False)]),
16:("마무리","최종 발표 — 자기 하네스 관점에서 방어",
 "Anthropic — *What is an Agent?* (1주차와 수미상관)",
 "최종 발표 + 동료 평가 + 평가 리포트 제출",
 "학기를 통해 '에이전트'의 정의는 어떻게 바뀌었는가?",
 [("🟢","(보조) The Rise and Potential of LLM Based Agents: A Survey","Xi et al., 2023 · arXiv:2309.07864",
   "학기 전체를 brain/perception/action으로 정리","미해결 과제(open problems)와 자기 연구 연결","W16_LLM-Agents-Survey-Xi_2309.07864.pdf",False)]),
}

OVERVIEW = {
1:"**강의소개(OT·발표 배정)** 와 함께 에이전트의 정의를 잡는 첫 주. 이론에서 에이전트 vs 워크플로우, 자율성 스펙트럼, **폼팩터 4형태**(대화·위임·임베디드·헤드리스 — 챗봇은 껍데기일 뿐)를 다루고, 실습은 **환경 세팅 + LLM 호출 래퍼**. **학생 발표 없음** — 교수가 6장 템플릿 시연 발표(Self-Consistency)로 W2부터의 기대 수준을 보여준다.",
2:"**하네스(제어 루프)의 최소 형태**를 만드는 주. 이론에서 CoT(생각의 외부화)→Act-only→**ReAct의 추론–행동–관찰 루프** 계보를 다루고 트레이스를 라이브로 읽는다. 실습에서 그 루프를 while 문으로 직접 구현한다. **학생 발표 시작** — ReAct·CoT.",
3:"2025–26 에이전트의 토대인 **추론 모델**을 앞쪽에 배치(Berkeley 흐름). 이론에서 CoT→self-consistency→**test-time compute**와 RL로 추론이 창발하는 과정(DeepSeek-R1), STaR 부트스트랩을 다룬다. **RL은 사전 지식 없음을 가정** — R1 전에 보상 개념을 비유 수준으로 3분 입문(수식 0). 실습은 self-consistency 비교. 유명·readable해 동기부여가 좋다.",
4:"에이전트가 외부 세계와 만나는 통로인 **도구**. 이론에서 함수 호출·스키마·에러 설계와 **도구 절벽**을 다루고, 실습에서 도구 레지스트리·파싱·실행을 직접 만든다. Toolformer·ToolLLM.",
5:"복잡한 과제를 나누고 탐색하는 **계획**. 이론에서 과제 분해, 계획–실행 분리, **트리 탐색 직관**을 다루고, 실습에서 트리 분기 추론을 미니 구현한다. Tree of Thoughts·ReWOO.",
6:"자기 출력을 스스로 고치는 **반성·메타인지**. 이론에서 생성→비평→개선 루프와 **언어 피드백이 gradient 없이 작동하는 원리**를 다루고, 실습에서 실패→피드백→재시도를 루프에 붙인다. Reflexion·Self-Refine.",
7:"외부 지식을 끌어오는 **RAG 기초**. 이론에서 임베딩·벡터검색, retriever–reader 구조를 다루고, 실습에서 임베딩→유사도→주입 검색을 직접 만든다 *(최종 프로젝트 부품 1)*. RAG(Lewis)·HyDE. *(보안 복선: 오늘 만든 '문서 입구'가 W14 간접 인젝션의 공격 통로가 된다 — 예고만.)*",
8:"검색을 전처리가 아닌 **'도구'로 바꾸는 에이전틱 RAG**와 **MCP**. 이론에서 능동 검색(adaptive/self)과 프로토콜을 다루고, 실습에서 검색을 도구로 노출해 단계별 호출하게 개조한다 *(최종 프로젝트 부품 2)*. Self-RAG·Adaptive-RAG.",
9:"⭐ 컨텍스트를 유한 자원으로 다루는 **컨텍스트 엔지니어링 = 하네스**. 이론에서 LLM이 긴 컨텍스트를 어떻게(못) 쓰는지와 압축·큐레이션을 다루고, 실습에서 컨텍스트 예산·압축을 하네스에 넣는다. Lost-in-the-Middle·LLMLingua. **🏁 중간 데모 체크포인트:** 여기까지가 from-scratch 단일 에이전트의 완성형(루프+도구+계획+반성+RAG+컨텍스트) — 실습 말미에 각자 **'내 에이전트 중간 데모'**(문서 QA를 예산 내 수행)로 중간 점검을 대신한다.",
10:"대화·과제를 넘어 정보를 유지하는 **메모리**. 이론에서 단기/장기, **계층적 메모리(OS 비유)**, 검색 기준(최신성·중요도·관련성)을 다루고, 실습에서 메모리 스트림을 구현한다 *(최종 프로젝트 부품 3)*. MemGPT·Mem0(2025).",
11:"⭐ **전환점.** 여러 에이전트의 협업과 프레임워크로의 전환. 이론에서 협업 아키텍처(핸드오프·라우터)를 다루고, 실습에서 직접 짠 멀티에이전트를 **LangGraph로 재구현·비교**한다(from-scratch→프레임워크 분기점). AutoGen·MetaGPT.",
12:"화면을 보고 클릭하는 **컴퓨터·웹 에이전트**. 이론에서 관찰–행동 루프, **DOM vs 스크린샷**, 벤치마크(WebArena/OSWorld)를 다루고, 실습에서 간단한 웹/OS 태스크 루프를 돌린다. 시각적이라 흥미로운 주. WebArena·OSWorld(2024). *(보안 복선: 오늘 붙인 웹 도구가 W14 간접 인젝션의 주 통로다 — 예고만.)*",
13:"에이전트를 **어떻게 평가하나**(비판적 시각). 이론에서 능력 평가 vs 회귀 평가, **비용–정확도 Pareto**, 재현성을 다루고, 실습에서 최종 프로젝트 평가 하네스 골격을 만든다. AI Agents That Matter·τ-bench.",
14:"행동하는 에이전트의 **신뢰·보안**. 이론에서 **프롬프트 인젝션(직접/간접)**, 신뢰 경계·최소권한, 가드레일을 다루고, 실습에서 내 에이전트에 가드레일을 붙이고 인젝션을 테스트한다. 실전적이라 난이도 부담이 낮다. Indirect Injection·InjecAgent.",
15:"**'에이전트가 꼭 필요한가'** 라는 반문. 이론에서 언제 에이전트가 과한지, 프로덕션 하네스, **ACI(에이전트-컴퓨터 인터페이스) 설계**를 다루고, 실습은 최종 프로젝트 통합 구현에 집중. Agentless·SWE-agent.",
16:"학기 마무리와 **최종 발표**. 각자 만든 RAG QA 에이전트를 **하네스 설계 관점에서 방어**하고, brain/perception/action 프레임으로 학기를 회고하며 1주차의 '에이전트란 무엇인가'를 재정의한다(수미상관).",
}

# 누적 빌드: 매주 문서 QA 에이전트(docqa-agent)에 모듈 하나 추가. 상세: docs/practice-guide.md
PRACTICE = {
1:"**추가 모듈:** `llm.py` — (원시 API 1회 호출로 내부 확인 후) **aisuite**로 provider-무관 `chat()` 래퍼.\n> ✅ **완료:** 원시 HTTP와 내가 채운 `chat()` 양쪽으로 같은 질문에 답을 받는다.",
2:"**추가 모듈:** `loop.py` — ReAct(Thought→Action→Observation) while 루프 골격. W1 이론에서 본 루프를 직접 짠다.\n> ✅ **완료:** 간단한 질문에 루프가 한 바퀴 돌아 답을 낸다.",
3:"**추가 모듈:** `reasoning.py` — 같은 질문을 N번 샘플→다수결(self-consistency) 토글.\n> ✅ **완료:** 애매한 질문에서 단일 답보다 정확도가 오른다.",
4:"**추가 모듈:** `tools.py` — 도구 등록(dict)·JSON 액션 파싱·실행(계산기·문자열검색).\n> ✅ **완료:** 루프가 계산기 도구를 실제로 호출해 답한다.",
5:"**추가 모듈:** `planner.py` — 질문을 하위 단계 리스트로 분해→순차 실행.\n> ✅ **완료:** 2단계 질문을 계획대로 처리한다.",
6:"**추가 모듈:** `reflect.py` — 검증 실패 시 언어 피드백을 붙여 재시도(최대 k회).\n> ✅ **완료:** 처음 틀린 답을 재시도로 고친다.",
7:"**추가 모듈:** `retriever.py` + 샘플 문서 — 청킹→임베딩→코사인 top-k 검색. 📦 *최종 부품*\n> ✅ **완료:** 문서 속 사실을 물으면 관련 청크로 답한다.",
8:"**개조:** `retriever`를 `tools.py`에 **검색 도구**로 등록 → 필요할 때만 검색. 📦 *최종 부품*\n> ✅ **완료:** 상식 질문은 검색 안 하고 문서 질문만 검색한다.",
9:"**추가 모듈:** `context.py` — 토큰 예산 관리(자르기·중요도 정렬·간단 압축).\n> ✅ **완료:** 문서가 많아도 예산 내에서 답 품질을 유지한다.",
10:"**추가 모듈:** `memory.py` — 단기(대화 이력)+장기(파일 저장·검색). 📦 *최종 부품*\n> ✅ **완료:** 이전 세션에 말한 정보를 다음 세션에서 기억한다.",
11:"**개조:** `graph.py` — 지금까지의 루프를 **LangGraph로 재구현**(+선택 비평 노드).\n> ✅ **완료:** from-scratch 버전과 동일 동작을 그래프로 재현·비교한다.",
12:"**추가 모듈:** `tools_web.py` — URL fetch/간단 웹검색 도구(관찰-행동).\n> ✅ **완료:** 웹에서 정보를 가져와 답한다(간단 버전).",
13:"**추가 모듈:** `eval/harness.py`+`testset.jsonl` — QA 20문항 정확도·비용·지연·재현성 측정.\n> ✅ **완료:** 내 에이전트의 점수표를 출력한다.",
14:"**추가 모듈:** `guardrails.py` — 입출력 필터 + **오염 문서로 간접 인젝션 레드팀**.\n> ✅ **완료:** 문서에 심은 인젝션이 가드레일에 막힌다.",
15:"**통합:** `app.py` — 전체 통합 CLI + 단순 파이프라인 베이스라인과 비교.\n> ✅ **완료:** 문서 QA 앱을 완성하고 베이스라인 대비 평가한다.",
16:"**최종 발표:** eval 점수·하네스 설계 선택을 방어 + 동료 평가.\n> ✅ **완료:** 데모 + 평가 리포트를 제출한다.",
}

RUBRIC = ("| 핵심 기여 | 30% | 논문의 기여를 한 문장으로 정확히 압축했는가 |\n"
"| 방법 이해 | 25% | 핵심 아이디어·메커니즘을 정확히 설명했는가 (심화는 직관 허용, 수식 생략 가능) |\n"
"| 비판적 분석 | 25% | 가장 약한 가정·한계를 스스로 짚었는가 |\n"
"| 연결·확장 | 20% | 후속 논문 또는 본인/연구실 주제와 연결했는가 |")

os.makedirs(ROOT, exist_ok=True)
W1_PAPERS = ("**⚠️ 학생 발표 없음** — 발표 배정 전이다. 이 시간에 **W2~W15 발표자·지정 토론자를 일괄 배정**한다.\n"
 "- **교수 시연 발표:** Self-Consistency (Wang et al., 2022 · [arXiv:2203.11171](https://arxiv.org/abs/2203.11171)) — "
 "6장 템플릿·15분 하드 스톱 그대로 시연. 수업 발표 목록에 없는 논문이라 스포일러가 없고, W3 이론·실습의 예고편이 된다.\n"
 "- 다음 주 발표 논문(ReAct·CoT)은 **개강 전 주에 발표자에게 미리 공지**한다.\n")

W1_PRESENT = ("- **학생 발표 없음** — 교수 시연으로 발표 형식(6장·하드 스톱·콜드 질문·지정 토론자)을 보여준다.\n"
 "- 시간표는 [발표 가이드 §1의 1주차 예외](../docs/presentation-guide.md) 참고.")

STD_PRESENT = ("- 편당 **25분**: 발표 15분(슬라이드 6장 상한·하드 스톱) + 이해검증 8분 + 정리 2분\n"
 "- 발표 템플릿 6장: ①한 문장 기여 ②문제·동기 ③핵심 메커니즘(직접 그린 그림) ④결과 1개 ⑤약한 가정·한계 ⑥연결\n"
 "- 교수 콜드 질문(슬라이드 끄고): *X 단계 빼면? / 처음부터 구현 첫 3단계? / 실패하는 입력?*\n"
 "- 지정 토론자 1명 사전 배정 → 발표 후 2분 반박·보완")

for wk,(part,title,aux,practice,disc,papers) in W.items():
    plines=[]
    for diff,pt,cite,must,deep,pdf,opt in papers:
        tag=" *(선택읽기)*" if opt else ""
        plines.append(f"#### {diff} {pt}{tag}\n"
            f"- **출처:** {cite}\n"
            f"- **발표 필수:** {must}\n"
            f"- **선택 심화:** {deep}\n"
            f"- **PDF:** [`{pdf}`](../papers/{pdf})\n")
    papers_md="\n".join(plines) if papers else W1_PAPERS
    present_md = W1_PRESENT if wk==1 else STD_PRESENT
    papers_head = "## 📄 발표 논문" if papers else "## 📄 이번 주 논문 운영"
    if wk<=10:     base_note="**빌드 베이스:** from-scratch (내 모듈 직접 구현) · LLM 호출은 **aisuite** 래퍼(provider 무관)"
    elif wk==11:   base_note="**빌드 베이스:** 🔄 **전환점** — from-scratch 모듈을 **LangGraph 노드로 감싼다**(로직 재사용, 오케스트레이션만 위임)"
    elif wk==16:   base_note="**빌드 베이스:** 최종 통합·발표"
    else:          base_note="**빌드 베이스:** **LangGraph** 위에서 확장 (W1–10 from-scratch 모듈 재사용)"
    md=f"""# Week {wk:02d}. {title}

> **Part:** {part} · 난이도: 🟢 기초 · 🟡 중급 · 🔴 심화 · [📋 발표 가이드](../docs/presentation-guide.md)

## 🧭 개요
{OVERVIEW[wk]}

## 📖 보조읽기 (발표 대상 아님)
{aux}

{papers_head}
{papers_md}
## 💬 토론 포인트 (교수 백업 질문)
{disc}

## 🛠 실습 — 누적 빌드 `docqa-agent`
{base_note}

*이번 주 주제:* {practice}

{PRACTICE[wk]}

> 한 학기 하나의 앱을 쌓는다 · 스캐폴드 빈칸 채우기 + 주차별 체크포인트 → 상세는 [실습 가이드](../docs/practice-guide.md).

## 🎤 발표 진행 (요약 · 상세는 [발표 가이드](../docs/presentation-guide.md))
{present_md}

## 📊 평가 루브릭
| 항목 | 배점 | 기준 |
|---|---|---|
{RUBRIC}
"""
    open(os.path.join(ROOT, f"week{wk:02d}.md"),"w").write(md)
    print(f"week{wk:02d}.md: {title}")

print("\nDONE ->", ROOT)
