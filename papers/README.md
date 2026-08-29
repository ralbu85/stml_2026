# 발표 논문 PDF — 검증 매니페스트

`docs/syllabus.md`(개념 의존성 순서 v5) 발표 논문 전체 — 필수 27 + 선택읽기 11 = **38편**.
**검증:** 각 arXiv ID의 실제 초록 제목 대조 → **전량 일치, 다운로드 실패 0**. 재현: `python3 scripts/fetch_papers.py`.

> PDF는 `.gitignore`(용량 큼, arXiv 재다운로드 가능). 이 목록과 스크립트만 버전관리.

| 주 | 파일 | 논문 | arXiv |
|---|---|---|---|
| 2 | `W02_Chain-of-Thought_2201.11903.pdf` | Chain-of-Thought Prompting Elicits Reasoning in LLMs | [2201.11903](https://arxiv.org/abs/2201.11903) |
| 3 | `W03_STaR_2203.14465.pdf` | STaR: Bootstrapping Reasoning With Reasoning | [2203.14465](https://arxiv.org/abs/2203.14465) |
| 3 | `W03_DeepSeek-R1_2501.12948.pdf` | DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via RL | [2501.12948](https://arxiv.org/abs/2501.12948) |
| 4 | `W04_Toolformer_2302.04761.pdf` | Toolformer: Language Models Can Teach Themselves to Use Tools | [2302.04761](https://arxiv.org/abs/2302.04761) |
| 4 | `W04_ToolLLM_2307.16789.pdf` | ToolLLM: Facilitating LLMs to Master 16000+ Real-world APIs | [2307.16789](https://arxiv.org/abs/2307.16789) |
| 4 | `W04_opt-ReTool_2504.11536.pdf` | *(선택)* ReTool: RL for Strategic Tool Use in LLMs | [2504.11536](https://arxiv.org/abs/2504.11536) |
| 5 | `W05_ReAct_2210.03629.pdf` | ReAct: Synergizing Reasoning and Acting in Language Models | [2210.03629](https://arxiv.org/abs/2210.03629) |
| 6 | `W06_RAG-Lewis_2005.11401.pdf` | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | [2005.11401](https://arxiv.org/abs/2005.11401) |
| 6 | `W06_Self-RAG_2310.11511.pdf` | Self-RAG: Learning to Retrieve, Generate, and Critique | [2310.11511](https://arxiv.org/abs/2310.11511) |
| 6 | `W06_opt-HyDE_2212.10496.pdf` | *(선택)* HyDE: Precise Zero-Shot Dense Retrieval without Relevance Labels | [2212.10496](https://arxiv.org/abs/2212.10496) |
| 6 | `W06_opt-Adaptive-RAG_2403.14403.pdf` | *(선택)* Adaptive-RAG: Adapt Retrieval-Augmented LLMs by Query Complexity | [2403.14403](https://arxiv.org/abs/2403.14403) |
| 7 | `W07_Tree-of-Thoughts_2305.10601.pdf` | Tree of Thoughts: Deliberate Problem Solving with LLMs | [2305.10601](https://arxiv.org/abs/2305.10601) |
| 7 | `W07_ReWOO_2305.18323.pdf` | ReWOO: Decoupling Reasoning from Observations | [2305.18323](https://arxiv.org/abs/2305.18323) |
| 8 | `W08_Reflexion_2303.11366.pdf` | Reflexion: Language Agents with Verbal Reinforcement Learning | [2303.11366](https://arxiv.org/abs/2303.11366) |
| 8 | `W08_Self-Refine_2303.17651.pdf` | Self-Refine: Iterative Refinement with Self-Feedback | [2303.17651](https://arxiv.org/abs/2303.17651) |
| 9 | `W09_Lost-in-the-Middle_2307.03172.pdf` | Lost in the Middle: How Language Models Use Long Contexts | [2307.03172](https://arxiv.org/abs/2307.03172) |
| 9 | `W09_LLMLingua_2310.05736.pdf` | LLMLingua: Compressing Prompts for Accelerated Inference | [2310.05736](https://arxiv.org/abs/2310.05736) |
| 9 | `W09_opt-Agentic-Context-Engineering_2510.04618.pdf` | *(선택)* Agentic Context Engineering: Evolving Contexts for Self-Improving LMs | [2510.04618](https://arxiv.org/abs/2510.04618) |
| 9 | `W09_opt-ReasoningBank_2509.25140.pdf` | *(선택)* ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory | [2509.25140](https://arxiv.org/abs/2509.25140) |
| 10 | `W10_MemGPT_2310.08560.pdf` | MemGPT: Towards LLMs as Operating Systems | [2310.08560](https://arxiv.org/abs/2310.08560) |
| 10 | `W10_Mem0_2504.19413.pdf` | Mem0: Production-Ready AI Agents with Scalable Long-Term Memory | [2504.19413](https://arxiv.org/abs/2504.19413) |
| 10 | `W10_opt-MemoryBank_2305.10250.pdf` | *(선택)* MemoryBank: Enhancing LLMs with Long-Term Memory | [2305.10250](https://arxiv.org/abs/2305.10250) |
| 10 | `W10_opt-Generative-Agents_2304.03442.pdf` | *(선택)* Generative Agents: Interactive Simulacra of Human Behavior | [2304.03442](https://arxiv.org/abs/2304.03442) |
| 11 | `W11_AutoGen_2308.08155.pdf` | AutoGen: Next-Gen LLM Apps via Multi-Agent Conversation | [2308.08155](https://arxiv.org/abs/2308.08155) |
| 11 | `W11_MetaGPT_2308.00352.pdf` | MetaGPT: Meta Programming for Multi-Agent Collaboration | [2308.00352](https://arxiv.org/abs/2308.00352) |
| 11 | `W11_opt-Multiagent-Debate_2305.14325.pdf` | *(선택)* Improving Factuality and Reasoning via Multiagent Debate | [2305.14325](https://arxiv.org/abs/2305.14325) |
| 11 | `W11_opt-CAMEL_2303.17760.pdf` | *(선택)* CAMEL: Communicative Agents for "Mind" Exploration | [2303.17760](https://arxiv.org/abs/2303.17760) |
| 12 | `W12_WebArena_2307.13854.pdf` | WebArena: A Realistic Web Environment for Building Agents | [2307.13854](https://arxiv.org/abs/2307.13854) |
| 12 | `W12_OSWorld_2404.07972.pdf` | OSWorld: Benchmarking Multimodal Agents in Real Computer Environments | [2404.07972](https://arxiv.org/abs/2404.07972) |
| 12 | `W12_opt-Mind2Web_2306.06070.pdf` | *(선택)* Mind2Web: Towards a Generalist Agent for the Web | [2306.06070](https://arxiv.org/abs/2306.06070) |
| 12 | `W12_opt-Voyager_2305.16291.pdf` | *(선택)* Voyager: An Open-Ended Embodied Agent with LLMs | [2305.16291](https://arxiv.org/abs/2305.16291) |
| 13 | `W13_AI-Agents-That-Matter_2407.01502.pdf` | AI Agents That Matter | [2407.01502](https://arxiv.org/abs/2407.01502) |
| 13 | `W13_tau-bench_2406.12045.pdf` | τ-bench: Tool-Agent-User Interaction Benchmark | [2406.12045](https://arxiv.org/abs/2406.12045) |
| 14 | `W14_Indirect-Prompt-Injection_2302.12173.pdf` | Not What You've Signed Up For: Indirect Prompt Injection | [2302.12173](https://arxiv.org/abs/2302.12173) |
| 14 | `W14_InjecAgent_2403.02691.pdf` | InjecAgent: Benchmarking Indirect Injection in Tool Agents | [2403.02691](https://arxiv.org/abs/2403.02691) |
| 15 | `W15_Agentless_2407.01489.pdf` | Agentless: Demystifying LLM-based Software Engineering Agents | [2407.01489](https://arxiv.org/abs/2407.01489) |
| 15 | `W15_SWE-agent_2405.15793.pdf` | SWE-agent: Agent-Computer Interfaces Enable Automated SE | [2405.15793](https://arxiv.org/abs/2405.15793) |
| 16 | `W16_LLM-Agents-Survey-Xi_2309.07864.pdf` | The Rise and Potential of LLM Based Agents: A Survey | [2309.07864](https://arxiv.org/abs/2309.07864) |
