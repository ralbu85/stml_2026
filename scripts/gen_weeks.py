#!/usr/bin/env python3
import os

ROOT = "/workspace/BALAB_Prof/Lecture_STML_2026/weeks"

# 흐름: Microsoft ai-agents-for-beginners + Berkeley LLM Agents 재구성.
# week: (part, title, aux, practice, discussion, [papers])
# paper: (diff, title, cite, must, deep, pdf, optional)
W = {
1:("토대","에이전트 개요 + ReAct",
 "Anthropic — *Building Effective Agents* (워크플로우 vs 에이전트) · MS01",
 "환경 세팅, LLM API 단일 호출 → ReAct 제어 루프 골격(while 루프)",
 "에이전트와 단순 워크플로우의 경계는? CoT 없는 ReAct는 가능한가?",
 [("🟢","ReAct: Synergizing Reasoning and Acting in LLMs","Yao et al., ICLR 2023 · arXiv:2210.03629",
   "Think–Act–Observe 루프 구조와 추론·행동을 엮는 이유","HotpotQA·ALFWorld 셋업","W01_ReAct_2210.03629.pdf",False),
  ("🟢","Chain-of-Thought Prompting Elicits Reasoning in LLMs","Wei et al., NeurIPS 2022 · arXiv:2201.11903",
   "CoT 핵심 아이디어와 추론 창발 조건","규모별 창발 곡선, self-consistency","W01_Chain-of-Thought_2201.11903.pdf",False)]),
2:("토대","추론 모델 (Reasoning / Test-time Compute)",
 "Lilian Weng — *Why We Think* — test-time compute 직관 · Berkeley 추론 강의",
 "self-consistency / 다중 샘플 추론 비교",
 "'더 오래 생각하기'는 왜 성능을 올리나? 언제 과한가?",
 [("🟡","STaR: Self-Taught Reasoner","Zelikman et al., NeurIPS 2022 · arXiv:2203.14465",
   "스스로 만든 추론으로 추론을 부트스트랩하는 아이디어","rationalization 트릭","W02_STaR_2203.14465.pdf",False),
  ("🟡","DeepSeek-R1: Incentivizing Reasoning via RL","DeepSeek-AI, 2025 · arXiv:2501.12948",
   "순수 RL로 추론이 창발하는 큰 그림('aha moment')","GRPO, cold-start 데이터","W02_DeepSeek-R1_2501.12948.pdf",False)]),
3:("핵심 디자인 패턴","도구 사용 (Tool Use)",
 "Anthropic — *Writing Effective Tools for Agents* · MS04",
 "도구 레지스트리·파싱·실행 직접 구현 (계산기·검색 함수)",
 "도구가 많아질수록 좋은가? 도구 절벽(tool cliff)이 생기는 이유는?",
 [("🟡","Toolformer: LMs Can Teach Themselves to Use Tools","Schick et al., NeurIPS 2023 · arXiv:2302.04761",
   "self-supervised로 API 호출 위치를 학습하는 방식","호출 필터링 손실, 데이터 파이프라인","W03_Toolformer_2302.04761.pdf",False),
  ("🟡","ToolLLM: Mastering 16000+ Real-world APIs","Qin et al., ICLR 2024 · arXiv:2307.16789",
   "대규모 실세계 API 학습 프레임과 DFSDT 탐색","ToolBench 구축, pass/win rate","W03_ToolLLM_2307.16789.pdf",False)]),
4:("핵심 디자인 패턴","계획과 탐색 (Planning & Search)",
 "LangChain — *Plan-and-Execute Agents* · MS07",
 "탐색 기반 추론(트리 분기) 미니 구현, 계획–실행 분리",
 "탐색 비용 대비 성능 이득은 언제 정당한가?",
 [("🟡","Tree of Thoughts: Deliberate Problem Solving with LLMs","Yao et al., NeurIPS 2023 · arXiv:2305.10601",
   "사고를 트리로 분기·탐색(BFS/DFS)하는 발상","상태 평가 함수, Game of 24","W04_Tree-of-Thoughts_2305.10601.pdf",False),
  ("🟡","ReWOO: Decoupling Reasoning from Observations","Xu et al., 2023 · arXiv:2305.18323",
   "계획을 관찰과 분리해 토큰·호출을 줄이는 구조","planner/worker/solver 모듈 분해","W04_ReWOO_2305.18323.pdf",False)]),
5:("핵심 디자인 패턴","자기반성·메타인지 (Reflection)",
 "Anthropic — *Demystifying Evals for AI Agents* · MS09",
 "실패→언어 피드백→재시도 루프를 ReAct에 추가",
 "자기반성은 진짜 개선인가, 아니면 같은 오류의 반복인가?",
 [("🟡","Reflexion: Language Agents with Verbal RL","Shinn et al., NeurIPS 2023 · arXiv:2303.11366",
   "언어 피드백이 gradient 없이 학습되는 메커니즘","actor-evaluator-reflection 구조","W05_Reflexion_2303.11366.pdf",False),
  ("🟢","Self-Refine: Iterative Refinement with Self-Feedback","Madaan et al., NeurIPS 2023 · arXiv:2303.17651",
   "단일 모델의 생성→비평→개선 반복","과제별 개선 폭, 피드백 프롬프트 설계","W05_Self-Refine_2303.17651.pdf",False)]),
6:("지식·컨텍스트·기억","검색 증강 (RAG) — 1부: 기초",
 "Anthropic — *Contextual Retrieval* / LlamaIndex RAG 가이드 · MS05",
 "임베딩→유사도→컨텍스트 주입 검색 직접 구현 *(최종 프로젝트 부품 1)*",
 "언제 검색해야 하는가? 항상 검색이 답인가?",
 [("🟡","Retrieval-Augmented Generation for Knowledge-Intensive NLP","Lewis et al., NeurIPS 2020 · arXiv:2005.11401",
   "파라메트릭 vs 비파라메트릭(검색) 지식 결합","RAG-Sequence vs Token, retriever 공동학습","W06_RAG-Lewis_2005.11401.pdf",False),
  ("🟡","HyDE: Precise Zero-Shot Dense Retrieval without Labels","Gao et al., ACL 2023 · arXiv:2212.10496",
   "가설 문서를 생성해 검색 품질을 올리는 발상","dense retriever와의 결합","W06_HyDE_2212.10496.pdf",False)]),
7:("지식·컨텍스트·기억","에이전틱 RAG + 프로토콜 (MCP)",
 "Anthropic — *Code Execution with MCP* · MS05·11",
 "검색을 '도구'로 노출하고 에이전트가 단계별로 호출하게 개조 *(최종 프로젝트 부품 2)*",
 "RAG를 도구로 만들면 무엇이 좋아지고 무엇이 어려워지나?",
 [("🟡🔴","Self-RAG: Learning to Retrieve, Generate, and Critique","Asai et al., ICLR 2024 · arXiv:2310.11511",
   "reflection token으로 검색 여부·품질을 스스로 판단","critic 학습, segment beam search","W07_Self-RAG_2310.11511.pdf",False),
  ("🟡","Adaptive-RAG: Adapting Retrieval to Query Complexity","Jeong et al., NAACL 2024 · arXiv:2403.14403",
   "질의 난이도에 따라 검색 전략을 바꾸는 에이전틱 구조","complexity classifier","W07_Adaptive-RAG_2403.14403.pdf",False)]),
8:("지식·컨텍스트·기억","컨텍스트 엔지니어링 (하네스) ⭐",
 "Anthropic — *Effective Context Engineering* + HumanLayer — *Skill Issue: Harness Engineering* · MS12",
 "컨텍스트 예산·압축·큐레이션을 하네스에 내장 (긴 컨텍스트 관리)",
 "컨텍스트는 왜 유한 자원인가? 무엇을 넣고 무엇을 버려야 하나?",
 [("🟡","Lost in the Middle: How LMs Use Long Contexts","Liu et al., TACL 2024 · arXiv:2307.03172",
   "LLM이 긴 컨텍스트의 중간 정보를 잘 못 쓰는 현상","위치별 성능 곡선, 검색 문서 수 효과","W08_Lost-in-the-Middle_2307.03172.pdf",False),
  ("🟡","LLMLingua: Compressing Prompts for Accelerated Inference","Jiang et al., EMNLP 2023 · arXiv:2310.05736",
   "프롬프트를 압축해 비용·지연을 줄이면서 성능 유지","예산 제어 압축, perplexity 기반 토큰 선택","W08_LLMLingua_2310.05736.pdf",False),
  ("🔴","Agentic Context Engineering (선택읽기·프런티어)","2025 · arXiv:2510.04618",
   "컨텍스트 자체를 진화시켜 자기개선","context 업데이트 정책","W08_opt-Agentic-Context-Engineering_2510.04618.pdf",True),
  ("🔴","ReasoningBank (선택읽기·프런티어)","2025 · arXiv:2509.25140",
   "추론 메모리를 쌓아 에이전트가 진화","메모리 항목 추출·재사용","W08_opt-ReasoningBank_2509.25140.pdf",True)]),
9:("지식·컨텍스트·기억","메모리 (Memory)",
 "Letta (MemGPT) — *Agent Memory Blog* (3계층 메모리) · MS13",
 "메모리 스트림 구현(저장·검색), 외부 메모리 통합 *(최종 프로젝트 부품 3)*",
 "무엇을 기억하고 무엇을 잊어야 하는가? 메모리 검색의 기준은?",
 [("🟡","MemGPT: Towards LLMs as Operating Systems","Packer et al., 2023 · arXiv:2310.08560",
   "가상메모리 비유의 계층적 메모리(core/archival)","function-call self-editing, 페이징","W09_MemGPT_2310.08560.pdf",False),
  ("🟡","Mem0: Production-Ready AI Agents with Long-Term Memory","2025 · arXiv:2504.19413",
   "장기메모리 파이프라인(추출·갱신·검색)의 실전 설계","확장성·지연 분석, 그래프 메모리","W09_Mem0_2504.19413.pdf",False),
  ("🟡","MemoryBank (선택읽기)","Zhong et al., AAAI 2024 · arXiv:2305.10250",
   "망각 곡선 기반 메모리 갱신·검색","사용자 페르소나 유지","W09_opt-MemoryBank_2305.10250.pdf",True),
  ("🟡","Generative Agents (선택읽기·메모리 측면)","Park et al., UIST 2023 · arXiv:2304.03442",
   "최신성·중요도·관련성으로 메모리를 점수화·검색","memory stream 구조","W09_opt-Generative-Agents_2304.03442.pdf",True)]),
10:("협업·환경","멀티에이전트 + LangGraph 전환점 ⭐",
 "LangChain — *Choosing the Right Multi-Agent Architecture* · MS02·08",
 "역할 분담 멀티에이전트를 **LangGraph로 재구현·비교** (직접 구현 대비)",
 "멀티에이전트가 단일 에이전트보다 정말 나은가? 언제 과한가?",
 [("🟡","AutoGen: Multi-Agent Conversation Framework","Wu et al., COLM 2024 · arXiv:2308.08155",
   "대화 기반 멀티에이전트 추상화와 역할 분담","conversable agent, human-in-the-loop","W10_AutoGen_2308.08155.pdf",False),
  ("🟡","MetaGPT: Meta Programming for Multi-Agent Collaboration","Hong et al., ICLR 2024 · arXiv:2308.00352",
   "SOP(표준운영절차)를 코드화한 협업 구조","역할별 산출물 스키마","W10_MetaGPT_2308.00352.pdf",False),
  ("🟡","Multiagent Debate (선택읽기)","Du et al., ICML 2024 · arXiv:2305.14325",
   "다중 에이전트 토론이 사실성·추론을 높이는 원리","수렴 동역학","W10_opt-Multiagent-Debate_2305.14325.pdf",True),
  ("🟡","CAMEL: Communicative Agents (선택읽기)","Li et al., NeurIPS 2023 · arXiv:2303.17760",
   "역할극 기반 자율 협력 프레임","inception prompting","W10_opt-CAMEL_2303.17760.pdf",True)]),
11:("협업·환경","컴퓨터/웹 사용 에이전트 (Computer Use)",
 "*OS Agents: A Survey on MLLM-based Agents* (ACL 2025) · MS15",
 "브라우저/OS 환경에서 관찰-행동 루프 (간단한 웹/데스크톱 태스크)",
 "텍스트 도구 호출 vs 화면 클릭 — 무엇이 언제 나은가?",
 [("🟡","WebArena: A Realistic Web Environment for Agents","Zhou et al., ICLR 2024 · arXiv:2307.13854",
   "실제 웹 태스크 벤치마크 구성과 왜 어려운가","4개 도메인, 성공률 격차","W11_WebArena_2307.13854.pdf",False),
  ("🟡","OSWorld: Benchmarking Multimodal Agents in Real Computer Environments","Xie et al., NeurIPS 2024 · arXiv:2404.07972",
   "실제 데스크톱 OS에서 멀티모달 에이전트를 실행 기반으로 평가","369 태스크, 스크린샷–행동 인터페이스","W11_OSWorld_2404.07972.pdf",False),
  ("🟡","Mind2Web (선택읽기)","Deng et al., NeurIPS 2023 · arXiv:2306.06070",
   "실세계 웹사이트 일반화 과제와 데이터","DOM 후보 선택","W11_opt-Mind2Web_2306.06070.pdf",True)]),
12:("학습·품질·운영","에이전트 강화학습 (개념 1주 · 수식 생략)",
 "Lilian Weng — *Reward Hacking in RL* · Berkeley 후련 강의",
 "간단한 보상 기반 도구 선택 시뮬레이션",
 "도구 사용을 왜 RL로 배워야 하나? RL 에이전트 vs 프롬프트 에이전트?",
 [("🔴","ReTool: RL for Strategic Tool Use in LLMs","2025 · arXiv:2504.11536 · *수식 유도 생략 가능*",
   "도구 사용 시점·방법을 RL로 최적화하는 핵심 직관","코드 인터프리터 통합, outcome 보상","W12_ReTool_2504.11536.pdf",False),
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
1:"에이전트의 정의를 잡고 **하네스(제어 루프)의 최소 형태**를 만드는 첫 주. 이론에서 에이전트 vs 워크플로우, 자율성 스펙트럼, ReAct의 **추론–행동–관찰 루프**를 다루고, 실습에서 그 루프를 while 문으로 직접 구현한다. ReAct·CoT.",
2:"2025–26 에이전트의 토대인 **추론 모델**을 앞쪽에 배치(Berkeley 흐름). 이론에서 CoT→self-consistency→**test-time compute**와 RL로 추론이 창발하는 과정(DeepSeek-R1), STaR 부트스트랩을 다룬다. 실습은 self-consistency 비교. 유명·readable해 동기부여가 좋다.",
3:"에이전트가 외부 세계와 만나는 통로인 **도구**. 이론에서 함수 호출·스키마·에러 설계와 **도구 절벽**을 다루고, 실습에서 도구 레지스트리·파싱·실행을 직접 만든다. Toolformer·ToolLLM.",
4:"복잡한 과제를 나누고 탐색하는 **계획**. 이론에서 과제 분해, 계획–실행 분리, **트리 탐색 직관**을 다루고, 실습에서 트리 분기 추론을 미니 구현한다. Tree of Thoughts·ReWOO.",
5:"자기 출력을 스스로 고치는 **반성·메타인지**. 이론에서 생성→비평→개선 루프와 **언어 피드백이 gradient 없이 작동하는 원리**를 다루고, 실습에서 실패→피드백→재시도를 루프에 붙인다. Reflexion·Self-Refine.",
6:"외부 지식을 끌어오는 **RAG 기초**. 이론에서 임베딩·벡터검색, retriever–reader 구조를 다루고, 실습에서 임베딩→유사도→주입 검색을 직접 만든다 *(최종 프로젝트 부품 1)*. RAG(Lewis)·HyDE.",
7:"검색을 전처리가 아닌 **'도구'로 바꾸는 에이전틱 RAG**와 **MCP**. 이론에서 능동 검색(adaptive/self)과 프로토콜을 다루고, 실습에서 검색을 도구로 노출해 단계별 호출하게 개조한다 *(최종 프로젝트 부품 2)*. Self-RAG·Adaptive-RAG.",
8:"⭐ 컨텍스트를 유한 자원으로 다루는 **컨텍스트 엔지니어링 = 하네스**. 이론에서 LLM이 긴 컨텍스트를 어떻게(못) 쓰는지와 압축·큐레이션을 다루고, 실습에서 컨텍스트 예산·압축을 하네스에 넣는다. Lost-in-the-Middle·LLMLingua.",
9:"대화·과제를 넘어 정보를 유지하는 **메모리**. 이론에서 단기/장기, **계층적 메모리(OS 비유)**, 검색 기준(최신성·중요도·관련성)을 다루고, 실습에서 메모리 스트림을 구현한다 *(최종 프로젝트 부품 3)*. MemGPT·Mem0(2025).",
10:"⭐ **전환점.** 여러 에이전트의 협업과 프레임워크로의 전환. 이론에서 협업 아키텍처(핸드오프·라우터)를 다루고, 실습에서 직접 짠 멀티에이전트를 **LangGraph로 재구현·비교**한다(from-scratch→프레임워크 분기점). AutoGen·MetaGPT.",
11:"화면을 보고 클릭하는 **컴퓨터·웹 에이전트**. 이론에서 관찰–행동 루프, **DOM vs 스크린샷**, 벤치마크(WebArena/OSWorld)를 다루고, 실습에서 간단한 웹/OS 태스크 루프를 돌린다. 시각적이라 흥미로운 주. WebArena·OSWorld(2024).",
12:"에이전트를 **RL로 학습**시키는 관점(1주·수식 생략). 이론에서 보상 설계 직관, RLHF→RLVR, 도구학습 보상을 **직관 수준**으로만 다루고, 실습은 보상 기반 도구선택 시뮬레이션. ReTool. *(Voyager는 스킬 축적 선택읽기)*",
13:"에이전트를 **어떻게 평가하나**(비판적 시각). 이론에서 능력 평가 vs 회귀 평가, **비용–정확도 Pareto**, 재현성을 다루고, 실습에서 최종 프로젝트 평가 하네스 골격을 만든다. AI Agents That Matter·τ-bench.",
14:"행동하는 에이전트의 **신뢰·보안**. 이론에서 **프롬프트 인젝션(직접/간접)**, 신뢰 경계·최소권한, 가드레일을 다루고, 실습에서 내 에이전트에 가드레일을 붙이고 인젝션을 테스트한다. 실전적이라 난이도 부담이 낮다. Indirect Injection·InjecAgent.",
15:"**'에이전트가 꼭 필요한가'** 라는 반문. 이론에서 언제 에이전트가 과한지, 프로덕션 하네스, **ACI(에이전트-컴퓨터 인터페이스) 설계**를 다루고, 실습은 최종 프로젝트 통합 구현에 집중. Agentless·SWE-agent.",
16:"학기 마무리와 **최종 발표**. 각자 만든 RAG QA 에이전트를 **하네스 설계 관점에서 방어**하고, brain/perception/action 프레임으로 학기를 회고하며 1주차의 '에이전트란 무엇인가'를 재정의한다(수미상관).",
}

RUBRIC = ("| 핵심 기여 | 30% | 논문의 기여를 한 문장으로 정확히 압축했는가 |\n"
"| 방법 이해 | 25% | 핵심 아이디어·메커니즘을 정확히 설명했는가 (심화는 직관 허용, 수식 생략 가능) |\n"
"| 비판적 분석 | 25% | 가장 약한 가정·한계를 스스로 짚었는가 |\n"
"| 연결·확장 | 20% | 후속 논문 또는 본인/연구실 주제와 연결했는가 |")

os.makedirs(ROOT, exist_ok=True)
for wk,(part,title,aux,practice,disc,papers) in W.items():
    plines=[]
    for diff,pt,cite,must,deep,pdf,opt in papers:
        tag=" *(선택읽기)*" if opt else ""
        plines.append(f"#### {diff} {pt}{tag}\n"
            f"- **출처:** {cite}\n"
            f"- **발표 필수:** {must}\n"
            f"- **선택 심화:** {deep}\n"
            f"- **PDF:** [`{pdf}`](../papers/{pdf})\n")
    papers_md="\n".join(plines)
    md=f"""# Week {wk:02d}. {title}

> **Part:** {part} · 난이도: 🟢 기초 · 🟡 중급 · 🔴 심화 · [📋 발표 가이드](../docs/presentation-guide.md)

## 🧭 개요
{OVERVIEW[wk]}

## 📖 보조읽기 (발표 대상 아님)
{aux}

## 📄 발표 논문
{papers_md}
## 💬 토론 포인트 (교수 백업 질문)
{disc}

## 🛠 실습 (from-scratch)
{practice}

> 실습 코드·노트는 이 파일 아래에 이어 적거나, 분량이 커지면 `week{wk:02d}/` 폴더로 분리한다.

## 🎤 발표 진행 (요약 · 상세는 [발표 가이드](../docs/presentation-guide.md))
- 편당 **25분**: 발표 15분(슬라이드 6장 상한·하드 스톱) + 이해검증 8분 + 정리 2분
- 발표 템플릿 6장: ①한 문장 기여 ②문제·동기 ③핵심 메커니즘(직접 그린 그림) ④결과 1개 ⑤약한 가정·한계 ⑥연결
- 교수 콜드 질문(슬라이드 끄고): *X 단계 빼면? / 처음부터 구현 첫 3단계? / 실패하는 입력?*
- 지정 토론자 1명 사전 배정 → 발표 후 2분 반박·보완

## 📊 평가 루브릭
| 항목 | 배점 | 기준 |
|---|---|---|
{RUBRIC}
"""
    open(os.path.join(ROOT, f"week{wk:02d}.md"),"w").write(md)
    print(f"week{wk:02d}.md: {title}")

print("\nDONE ->", ROOT)
