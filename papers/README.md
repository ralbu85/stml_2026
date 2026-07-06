# 발표 논문 PDF — 검증 매니페스트

`syllabus-v2.md` 발표 논문 전체(필수 30 + 선택읽기 4 = **34편**)를 arXiv에서 다운로드.
**검증 방법:** 각 arXiv ID의 실제 초록 페이지 제목을 대조 → **34/34 일치, 다운로드 실패 0**.
재현: `python3 scripts/fetch_papers.py` (arXiv 접속 필요).

> PDF 파일 자체는 `.gitignore` 처리(용량 127MB, arXiv 재다운로드 가능). 이 목록과 스크립트만 버전관리.

| 주 | 파일 | 논문 (검증된 정식 제목) | arXiv |
|---|---|---|---|
| 1 | `W01_ReAct_2210.03629.pdf` | ReAct: Synergizing Reasoning and Acting in Language Models | [2210.03629](https://arxiv.org/abs/2210.03629) |
| 1 | `W01_Chain-of-Thought_2201.11903.pdf` | Chain-of-Thought Prompting Elicits Reasoning in Large Language Models | [2201.11903](https://arxiv.org/abs/2201.11903) |
| 2 | `W02_Toolformer_2302.04761.pdf` | Toolformer: Language Models Can Teach Themselves to Use Tools | [2302.04761](https://arxiv.org/abs/2302.04761) |
| 2 | `W02_ToolLLM_2307.16789.pdf` | ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs | [2307.16789](https://arxiv.org/abs/2307.16789) |
| 3 | `W03_Reflexion_2303.11366.pdf` | Reflexion: Language Agents with Verbal Reinforcement Learning | [2303.11366](https://arxiv.org/abs/2303.11366) |
| 3 | `W03_Self-Refine_2303.17651.pdf` | Self-Refine: Iterative Refinement with Self-Feedback | [2303.17651](https://arxiv.org/abs/2303.17651) |
| 4 | `W04_Tree-of-Thoughts_2305.10601.pdf` | Tree of Thoughts: Deliberate Problem Solving with Large Language Models | [2305.10601](https://arxiv.org/abs/2305.10601) |
| 4 | `W04_ReWOO_2305.18323.pdf` | ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models | [2305.18323](https://arxiv.org/abs/2305.18323) |
| 5 | `W05_STaR_2203.14465.pdf` | STaR: Bootstrapping Reasoning With Reasoning | [2203.14465](https://arxiv.org/abs/2203.14465) |
| 5 | `W05_DeepSeek-R1_2501.12948.pdf` | DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning | [2501.12948](https://arxiv.org/abs/2501.12948) |
| 6 | `W06_RAG-Lewis_2005.11401.pdf` | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | [2005.11401](https://arxiv.org/abs/2005.11401) |
| 6 | `W06_HyDE_2212.10496.pdf` | Precise Zero-Shot Dense Retrieval without Relevance Labels | [2212.10496](https://arxiv.org/abs/2212.10496) |
| 7 | `W07_Self-RAG_2310.11511.pdf` | Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection | [2310.11511](https://arxiv.org/abs/2310.11511) |
| 7 | `W07_Adaptive-RAG_2403.14403.pdf` | Adaptive-RAG: Learning to Adapt Retrieval-Augmented LLMs through Question Complexity | [2403.14403](https://arxiv.org/abs/2403.14403) |
| 8 | `W08_MemGPT_2310.08560.pdf` | MemGPT: Towards LLMs as Operating Systems | [2310.08560](https://arxiv.org/abs/2310.08560) |
| 8 | `W08_MemoryBank_2305.10250.pdf` | MemoryBank: Enhancing Large Language Models with Long-Term Memory | [2305.10250](https://arxiv.org/abs/2305.10250) |
| 9 | `W09_Voyager_2305.16291.pdf` | Voyager: An Open-Ended Embodied Agent with Large Language Models | [2305.16291](https://arxiv.org/abs/2305.16291) |
| 9 | `W09_Generative-Agents_2304.03442.pdf` | Generative Agents: Interactive Simulacra of Human Behavior | [2304.03442](https://arxiv.org/abs/2304.03442) |
| 10 | `W10_AutoGen_2308.08155.pdf` | AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation | [2308.08155](https://arxiv.org/abs/2308.08155) |
| 10 | `W10_MetaGPT_2308.00352.pdf` | MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework | [2308.00352](https://arxiv.org/abs/2308.00352) |
| 10 | `W10_opt-Multiagent-Debate_2305.14325.pdf` | *(선택)* Improving Factuality and Reasoning through Multiagent Debate | [2305.14325](https://arxiv.org/abs/2305.14325) |
| 10 | `W10_opt-CAMEL_2303.17760.pdf` | *(선택)* CAMEL: Communicative Agents for "Mind" Exploration of LLM Society | [2303.17760](https://arxiv.org/abs/2303.17760) |
| 11 | `W11_ReTool_2504.11536.pdf` | ReTool: Reinforcement Learning for Strategic Tool Use in LLMs | [2504.11536](https://arxiv.org/abs/2504.11536) |
| 11 | `W11_opt-Agentic-Context-Engineering_2510.04618.pdf` | *(선택)* Agentic Context Engineering: Evolving Contexts for Self-Improving LMs | [2510.04618](https://arxiv.org/abs/2510.04618) |
| 11 | `W11_opt-ReasoningBank_2509.25140.pdf` | *(선택)* ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory | [2509.25140](https://arxiv.org/abs/2509.25140) |
| 12 | `W12_WebArena_2307.13854.pdf` | WebArena: A Realistic Web Environment for Building Autonomous Agents | [2307.13854](https://arxiv.org/abs/2307.13854) |
| 12 | `W12_Mind2Web_2306.06070.pdf` | Mind2Web: Towards a Generalist Agent for the Web | [2306.06070](https://arxiv.org/abs/2306.06070) |
| 13 | `W13_Indirect-Prompt-Injection_2302.12173.pdf` | Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection | [2302.12173](https://arxiv.org/abs/2302.12173) |
| 13 | `W13_InjecAgent_2403.02691.pdf` | InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated LLM Agents | [2403.02691](https://arxiv.org/abs/2403.02691) |
| 14 | `W14_AI-Agents-That-Matter_2407.01502.pdf` | AI Agents That Matter | [2407.01502](https://arxiv.org/abs/2407.01502) |
| 14 | `W14_tau-bench_2406.12045.pdf` | τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains | [2406.12045](https://arxiv.org/abs/2406.12045) |
| 15 | `W15_Agentless_2407.01489.pdf` | Agentless: Demystifying LLM-based Software Engineering Agents | [2407.01489](https://arxiv.org/abs/2407.01489) |
| 15 | `W15_SWE-agent_2405.15793.pdf` | SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering | [2405.15793](https://arxiv.org/abs/2405.15793) |
| 16 | `W16_LLM-Agents-Survey-Xi_2309.07864.pdf` | The Rise and Potential of Large Language Model Based Agents: A Survey | [2309.07864](https://arxiv.org/abs/2309.07864) |
