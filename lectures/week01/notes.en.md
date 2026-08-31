# Chapter 1. What is an Agent?

## 1.1 An Observation — Same Model, Different Work

Chatbots of around 2022 received a user's question, generated a single answer, and ended the interaction. Systems that appeared afterward behave differently. Deep Research, given a topic, searches and reads dozens of web pages on its own and produces a synthesized report. Claude Code, given a bug report, reads the code, edits it, runs the tests, and when they fail, analyzes the cause and edits again.

This difference did not come from changing the model. The same model serves on one side as a chatbot and on the other as a component of Deep Research or Claude Code. What separates the two is not the model but the program surrounding the model.

Andrew Ng's *Agentic AI* course states the contrast in a form worth holding onto. A single-shot prompt asks the model to do what a person would be doing if instructed: "type out an essay on topic X from start to finish in one go, without using backspace." The alternative is a process: write an outline, decide whether web research is needed, write a first draft, consider what needs revision, revise. Ng's definition follows from that picture — an **agentic AI workflow** is a process in which an LLM-based application executes multiple steps to complete a task. No human writes without backspace, and the second column is simply what writing normally looks like.

To determine what in that surrounding program separates a chatbot from an agent, the first step is to establish what an LLM call itself can and cannot do.

## 1.2 Definition — Where Control Flow Resides

An **LLM (large language model)** is an autoregressive generative model trained on large text corpora with the objective of next-token prediction. Autoregressive means that the model computes a probability distribution over the next token conditioned on the tokens generated so far, samples one token from it, and repeats this process to produce text. An LLM call therefore takes text in and returns text out, and has no other input or output channel. The model cannot open a file, cannot execute a search, and cannot verify whether its own output is factual. What it produces is a chain of tokens with high conditional probability, not an action on the external world.

![recursive token generation](figures/recursive-token-generation.png)

*Figure 1.1 — Autoregressive generation: each sampled token is appended to the input and fed back, one token per pass, until a stop token. Source: P.-M. Dartus, "How LLMs Generate Text for the Rest of Us" (2025), pm.dartus.fr.*

Consequently, everything the model cannot do by itself — opening files, executing searches, validating output — is handled by code outside the model. That code decides which action to execute next, when to repeat, and when to stop.

The word *agent* has no single accepted definition, and the disagreement is worth stating before a definition is chosen. Anthropic's *Building Effective Agents* (2024) records it: some practitioners use the term for fully autonomous systems that operate independently over extended periods, others for prescriptive implementations that follow predefined workflows. That article groups all such variations under **agentic systems** and draws one architectural distinction inside the group, which this course adopts.

- **Workflows** are systems where LLMs and tools are orchestrated through predefined code paths.
- **Agents** are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks.

OpenAI's *A Practical Guide to Building Agents* (2025) draws the same line from the other side. Its definition is that agents are systems which independently accomplish tasks on the user's behalf, and it excludes explicitly: applications that integrate an LLM but do not use it to control workflow execution — simple chatbots, single-turn LLM calls, sentiment classifiers — are not agents.

Both definitions turn on which party decides what happens next. The smolagents documentation states this as a property of the program itself — "AI agents are programs where LLM outputs control the workflow" — and grades systems by how far the model's output reaches into that flow. This course uses **control flow** for the totality of those decisions: which action to execute next, whether to repeat, and when to stop.

At this point the sources disagree, and the disagreement is the subject of this chapter rather than an inconvenience in it. Anthropic draws a line: a system is a workflow or it is an agent. The smolagents guide refuses the line in as many words — with its definition, "'agent' is not a discrete, 0 or 1 definition: instead, 'agency' evolves on a continuous spectrum, as you give more or less power to the LLM on your workflow." The disagreement has consequences: Anthropic files *routing* under workflows, while smolagents places a router on the agency scale as a system whose output already controls an if/else switch.

Ng settles the question by declining it: "Rather than arguing over which work to include or exclude as being a true agent, we can acknowledge that there are different degrees to which systems can be agentic." This course takes that position. The workflow/agent distinction of 1.2 is kept because it names the axis — where control flow resides — and 1.4 grades systems along that axis instead of sorting them into two boxes. When a single label is needed, a system is called an agent when its model's output decides some part of the path.

The axis is the location of the decision, not the system's capability. Having a search feature does not by itself make a system agentic. A pipeline that translates, then summarizes, then stores, in a fixed order, sits at the bottom of the scale even if it contains a search step, because the model decides nothing about the path. The same search moves the system up the scale when the model's output decides whether to search and with what query.

Anthropic describes agents in execution as, typically, LLMs using tools based on environmental feedback in a loop. Written out as steps:

1. The model reads the input accumulated so far and generates an output.
2. Code interprets that output. If the output is an action directive, the code executes the action; if it is a final answer, the iteration terminates.
3. The execution result is appended to the model's input.
4. The model reads the updated input and generates the next output (return to step 1).

This iterative structure is called the **agent loop**, and it is implemented directly in Chapter 4. Two of its properties matter from the outset. The same article insists that the agent obtain ground truth from the environment at each step — a tool result, a code execution — rather than judging its progress from its own text. And termination is not guaranteed by the loop itself, so implementations add stopping conditions such as a maximum number of iterations.

![control flow in a workflow versus an agent](figures/fig-1-2-loop-vs-workflow.svg)

*Figure 1.2 — A workflow executes a path fixed in code; an agent's every next step is a branch taken by reading the model's output.*

## 1.3 Components

OpenAI's guide states that in its most fundamental form an agent consists of three core components.

| Component | Definition |
|---|---|
| Model | The LLM powering the agent's reasoning and decision-making |
| Tools | External functions or APIs the agent can use to take action |
| Instructions | Explicit guidelines and guardrails defining how the agent behaves |

*Table 1.1 — Source: OpenAI, "A Practical Guide to Building Agents" (2025).*

The same guide divides tools into three types according to what they are for. **Data** tools retrieve the context needed to execute the workflow: querying a transaction database or a CRM, reading a PDF, searching the web. **Action** tools change something outside the model: sending mail, updating a record, handing a support ticket to a human. **Orchestration** tools are other agents, used as tools by an agent (→ Ch. 6).

Anthropic describes the same building block as the **augmented LLM** — a model enhanced with retrieval, tools, and memory, able to generate its own search queries, select appropriate tools, and determine what information to retain. The difference between the two lists is memory, and the loop of 1.2 is what requires it: each iteration decides on top of the previous iteration's result, so the record of progress has to be held somewhere. This course therefore treats memory as a fourth component and gives it its own chapters (→ Ch. 9–10).

## 1.4 Degrees of Agency

Ng's course sorts systems into three bands by how much the application decides for itself.

| Band | What holds | 
|---|---|
| Less autonomous | All steps predetermined; all tool use hard-coded; the autonomy is in text generation alone |
| Semi-autonomous | The agent makes some decisions and chooses tools, but all tools are predefined |
| Highly autonomous | The agent makes many decisions on its own and can create new tools on the fly |

*Table 1.2 — Source: Andrew Ng, "Agentic AI" (DeepLearning.AI), Module 1.*

Three bands are enough to place a system in conversation and too coarse to design with. The smolagents documentation grades the same axis more finely, naming each level together with the code that implements it — which is the useful part, because it shows that the difference between two levels is a difference of one line of code.

| Agency | What the LLM output does | Name | Example code |
|---|---|---|---|
| ☆☆☆ | has no impact on program flow | Simple processor | `process_llm_output(llm_response)` |
| ★☆☆ | controls an if/else switch | Router | `if llm_decision(): path_a() else: path_b()` |
| ★★☆ | controls function execution | Tool call | `run_function(llm_chosen_tool, llm_chosen_args)` |
| ★★☆ | controls iteration and program continuation | Multi-step agent | `while llm_should_continue(): execute_next_step()` |
| ★★★ | starts another agentic workflow | Multi-agent | `if llm_trigger(): execute_agent()` |
| ★★★ | acts in code, defining its own tools | Code agent | `def custom_tool(args): ...` |

*Table 1.3 — Levels of agency. Source: Hugging Face, smolagents conceptual guide.*

![levels of agency](figures/fig-1-3-autonomy-spectrum.svg)

*Figure 1.3 — The same levels on one axis. Rightward, the model holds more of the program's flow; predictability and per-run cost control shrink.*

The two tables nest. Ng's *less autonomous* band is the simple processor, where the model writes text that the program then uses on a path it did not choose. His *semi-autonomous* band covers the router, the tool call, and the multi-step agent: the model decides, but only among tools the developer defined. His *highly autonomous* band is where a system creates new tools on the fly, which is the code agent, and where one agentic workflow starts another, which is the multi-agent row.

The code column carries the rest. A router is one `if` statement whose branch is chosen by the model; a multi-step agent is one `while` loop whose continuation is chosen by the model. Everything this course builds from Chapter 4 onward lives inside that `while`.

Every level is occupied by systems described in these sources.

- **Simple processor.** OpenAI's guide names the cases explicitly and excludes them from the category of agents: simple chatbots, single-turn LLM calls, and sentiment classifiers. The model produces text; the program's path is unaffected by it.
- **Router.** Anthropic's routing workflow classifies an input and directs it to a specialized followup task — general questions, refund requests, and technical support sent to different downstream processes, prompts, and tools; or easy questions routed to a small, cost-efficient model and hard ones to a more capable model.
- **Tool call.** Anthropic's augmented LLM is the building block at this level: a model that generates its own search queries, selects the appropriate tools, and determines what to retain. OpenAI's minimal example is an agent given a `get_weather` function alongside its instructions.
- **Multi-step agent.** Anthropic reports its own coding agent resolving real GitHub issues in SWE-bench Verified from the pull-request description alone. The smolagents guide writes out the loop that defines the level: a memory initialized with the task, and `while llm_should_continue(memory)` around get-next-action, execute, append.
- **Multi-agent.** OpenAI's manager pattern makes specialized agents into tools of a central agent — its worked example equips one agent with `translate_to_spanish`, `translate_to_french`, and `translate_to_italian`, each of which is itself an agent (→ Ch. 6).
- **Code agent.** The level at which the model writes code that defines its own tools, which is what places it in Ng's highly-autonomous band. The smolagents library exists to support it.

Moving down the table, the system becomes able to handle problems whose path cannot be fixed in advance, but its behaviour becomes harder to predict and the number of calls and the cost grow. Autonomy is a trade: flexibility is bought with predictability and cost. Anthropic states the same trade as working advice — find the simplest solution possible and increase complexity only when needed, which may mean not building an agentic system at all.

Anthropic reports two domains in which agents have demonstrated value with its customers, and what the two have in common is the more useful lesson: both require conversation and action together, have clear success criteria, admit feedback loops, and integrate meaningful human oversight.

Customer support satisfies these because tools can pull customer data, order history, and knowledge-base articles while actions such as issuing a refund or updating a ticket are handled programmatically, and because a resolution is defined by the user, which makes success measurable. The article notes that several companies price the product per successful resolution — a commercial statement of confidence in the loop.

Coding satisfies them because code is verifiable: solutions are checked by automated tests, the agent iterates using the test results as feedback, and output quality can be measured objectively. The article adds the limit in the same breath — human review remains necessary, because automated tests verify function but not alignment with broader system requirements.

Neither domain was chosen for its level on the scale. They were chosen because their outputs can be checked, which is the condition that makes iteration worth anything.

## 1.5 Adoption Criteria

Since autonomy is a trade, choosing between an agent and a workflow is the problem of identifying when the trade pays off. Anthropic's rule is to find the simplest solution possible and to increase complexity only when needed: agentic systems trade latency and cost for task performance, workflows offer predictability and consistency for well-defined tasks, agents are the better option when flexibility and model-driven decision-making are needed at scale, and for many applications optimizing single LLM calls with retrieval and in-context examples is enough.

OpenAI's guide gives three conditions that identify workflows worth handing to an agent, each of them a case where deterministic and rule-based approaches fall short.

| Condition | Description | Example |
|---|---|---|
| Complex decision-making | Nuanced judgment, exceptions, or context-sensitive decisions | Refund approval in customer service |
| Difficult-to-maintain rules | Rulesets grown so extensive and intricate that updates are costly or error-prone | Vendor security reviews |
| Heavy reliance on unstructured data | Interpreting natural language, extracting meaning from documents, conversing with users | Processing a home insurance claim |

*Table 1.4 — Source: OpenAI, "A Practical Guide to Building Agents" (2025).*

The guide's instruction is to validate that a use case meets these conditions clearly before committing to an agent, since otherwise a deterministic solution suffices. Its illustration of the difference is payment fraud analysis: a traditional rules engine works like a checklist that flags transactions against preset criteria, whereas an agent functions like an investigator that weighs context and identifies suspicious activity even where no clear-cut rule is violated.

Ng's course grades the task itself rather than the system, along three dimensions that run from easier to harder: a clear step-by-step process against steps not known ahead of time; standard procedures to follow against planning and solving as the work proceeds; text assets only against multimodal input of sound and vision. A task on the left of all three is one an agent adds nothing to.

The smolagents guide supplies the test in the most usable form. Consider an application handling customer requests for a surfing-trip website. If requests fall into two known buckets — wanting information about trips, or wanting to talk to sales — then two predetermined paths handle everything, and the guide's advice is unambiguous: "by all means just code everything," since a deterministic workflow is a fully reliable system with no risk introduced by letting an unpredictable model into the flow. Its stated default is to regularize toward not using agentic behaviour at all. The case that breaks the deterministic version is a request like: "I can come on Monday, but I forgot my passport so risk being delayed to Wednesday, is it possible to take me and my stuff to surf on Tuesday morning, with a cancellation insurance?" No predetermined bucket holds it. The criterion follows: if the predetermined workflow falls short too often, that is what a need for flexibility looks like.

The instruction to build a workflow instead is not usable while the only workflow in view is a straight line of calls. The side that does not hand over control flow has a design vocabulary of its own. A **workflow pattern** is a named arrangement of LLM calls whose order is decided by the code rather than by the model; the patterns below are the ones Anthropic reports seeing in production, and later chapters of this course implement each of them.

| Pattern | Structure | Example | Appears in |
|---|---|---|---|
| Prompt chaining | A task is decomposed into a sequence of steps, each call processing the output of the previous one, with optional programmatic checks between steps | Write marketing copy, then translate it; write an outline, check it against criteria, then write the document | Ch. 7 planning |
| Routing | An input is classified and directed to a specialized followup task | General questions, refund requests, and technical support to different processes; easy questions to a small model, hard ones to a capable model | Ch. 8 adaptive retrieval |
| Parallelization — sectioning | A task is broken into independent subtasks run in parallel | One model instance answers the query while another screens it for inappropriate content; each call evaluates a different aspect in an automated eval | Ch. 5 evaluation |
| Parallelization — voting | The same task is run several times to obtain diverse outputs | Several prompts review the same code for vulnerabilities; several prompts judge content with different vote thresholds | Ch. 2 self-consistency |
| Orchestrator–workers | A central LLM dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their results | Coding products that change multiple files at once; search that gathers and analyzes across sources | Ch. 6 multi-agent |
| Evaluator–optimizer | One call generates a response while another evaluates it and gives feedback, in a loop | Literary translation where an evaluator supplies the critique the translator missed; multi-round search where the evaluator decides whether to search again | Ch. 5 reflection |

*Table 1.5 — Structures and examples from Anthropic, "Building Effective Agents" (2024); the chapter column is this course's.*

Two of these are not sequences at all, and orchestrator–workers is separated from parallelization precisely by flexibility: its subtasks are not predefined but determined by the orchestrator from the input. A fixed procedure is therefore not the same thing as a simple one.

## 1.6 Orchestration — One Agent or Several

Once the decision to build an agent is made, the next question is how many agents the program contains. OpenAI's guide warns against answering it too early: although it is tempting to build a fully autonomous agent with a complex architecture immediately, its customers typically achieve greater success with an incremental approach. It sorts orchestration into two categories.

A **single-agent system** is one model, equipped with appropriate tools and instructions, executing workflows in a loop. Capability is added by adding tools, which keeps complexity manageable and keeps evaluation and maintenance simple; each new tool extends the agent without forcing a premature split into several agents.

A **multi-agent system** distributes workflow execution across several coordinated agents. The guide names two broadly applicable patterns. In the **manager** pattern, a central agent coordinates specialized agents through tool calls, each handling one task or domain. In the **decentralized** pattern, agents operate as peers and hand tasks off to one another according to their specializations. Modeled as a graph with agents as nodes, the edges in the manager pattern are tool calls, and in the decentralized pattern they are handoffs that transfer execution from one agent to another.

Anthropic's orchestrator–workers workflow has the shape of the manager pattern: a central LLM breaks a task down, delegates the pieces to worker LLMs, and synthesizes their results. Both sources make the same recommendation regardless of pattern — keep the components composable and driven by clear instructions — and this course returns to the subject in Chapter 6.

## 1.7 Organization of the Course

As established in 1.2, an LLM call takes text in and returns text out, and nothing more. From this follow the deficits that must be filled to build an agent, and those deficits form the organization of this course.

- The model cannot act → tools (Ch. 3), the agent loop (Ch. 4)
- The model does not know when it is wrong → reflection and evaluation (Ch. 5), planning and search (Ch. 7)
- Tasks too large for a single agent are divided among several → multi-agent systems (Ch. 6)
- The model knows nothing after its training cutoff and nothing inside an organization → retrieval augmentation (Ch. 8), memory (Ch. 10)
- Iteration accumulates input without bound → context management (Ch. 9)
- The caller's procedures migrate into the model's weights → reasoning models (Ch. 11)
- Accumulated capability multiplies inference cost → inference economics (Ch. 12); capability must be measured against that cost → benchmarks (Ch. 13)
- A system that acts becomes an attack surface → security (Ch. 14)

The order of the chapters is the arc of the course. The first half builds one complete agent and disciplines it: reasoning as the raw material (Ch. 2), tools as its hands (Ch. 3), the loop that assembles the first agent (Ch. 4), then the feedback and measurement that make its improvement claimable (Ch. 5), and finally scale — several agents (Ch. 6) and paths planned rather than stumbled into (Ch. 7) — before the midterm. The second half grounds the agent in knowledge it does not have (Ch. 8–10) and turns it into an operated system (Ch. 11–14).

The same arc can be read off Ng's course, which closes its introductory module with four agentic design patterns: reflection, tool use, planning, and multi-agent collaboration. Each is a chapter here — tool use in Chapter 3, reflection in Chapter 5, multi-agent collaboration in Chapter 6, planning in Chapter 7 — and this is not a coincidence, because from week 3 the labs adapt Ng's modules.

Labs run as one self-contained Colab notebook per week, with one course-built lab (week 4, the loop built by hand); weeks 1–2 cover prompting practice. This chapter's lab is the first API call and prompting fundamentals.

## 1.8 Discussion

Each question is answerable with this chapter's definitions; several return as design decisions in later chapters.

1. A nightly job sends every new arXiv abstract in your field to an LLM, stores the summaries, and mails a digest. A support bot reads each incoming ticket and decides whether to answer, refund, or escalate to a human. Classify each as workflow or agent by the criterion of 1.2, and name the single decision that settles the classification.
2. A RAG chatbot always retrieves the top five passages for the user's question and answers from them, in a fixed sequence. Is it an agent under 1.2? State the smallest change that would flip your answer.
3. Place a system you have used on each row of Table 1.2 that it occupies, and write the line of code from the table's last column that its program would contain. Which row is the highest it reaches, and what would have to change for it to reach the next one?
4. OpenAI's guide excludes sentiment classifiers from the category of agents, while Anthropic's routing workflow classifies a support ticket and dispatches it. Both classify; explain why one is an agent under 1.2 and the other is not.
5. The same model serves as a chatbot and as a component of Deep Research (1.1). If the weights are identical, where does the added capability come from — and which of the components of 1.3 supply it?

**Presentation.** There is no paper presentation this week. Presentations begin in week 2; presenter assignment and format guidance take place during orientation.

**Lab.** `W1_lab_setup.ipynb` — a Colab notebook: paste an API key into the setup cell and make first model calls through aisuite; examine message roles, statelessness, and temperature; then write a system prompt that forces every answer into clean JSON (checked PASS/FAIL by the notebook). Reference answers: `labs/checkpoints/week01/solution.py`.
