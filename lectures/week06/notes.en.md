# Chapter 6. Multi-Agent Systems

With measurement in hand (Chapter 5), the system itself can grow. So far every configuration has been one agent: one standing prompt, one accumulating context, one set of tools, one loop deciding call by call (Chapter 4). Some work outgrows that unit — not because the model is too weak, but because one context is being asked to hold too many roles at once. This chapter splits the work: several agents, each with its own instructions, context, and tools, cooperating through handoffs or a shared store.

In this chapter an **agent** is exactly the unit Chapter 4 built — a loop that receives a task, calls its tools as it judges, and returns a result, carrying its own prompt and its own context. At the orchestration level, that inner machinery is deliberately out of view: each agent is treated as a box with an input and an output, and this chapter arranges the boxes.

## 6.1 The Problem — One Agent, One Context

Three pressures push against the single-agent design as tasks grow.

**Role interference.** A prompt that says "research the topic, then criticize your research, then write the report" carries three roles whose instructions compete. The critic role is the clearest casualty: a critique generated in the same context that produced the draft inherits the draft's framing, and Chapter 5 established that critique works best when it stands apart from generation. Separate agents give each role a prompt that says one thing.

**Context growth.** One agent doing everything accumulates everything: every observation, every draft, every tool result lands in a single context that is re-sent on every call. Cost grows with the square of the accumulated length, and long contexts degrade retrieval of what matters (treated fully in Chapter 9). Splitting the work partitions the context: the researcher's sources never enter the writer's window — only the findings do.

**No independent perspective.** One agent is one sampling of one model conditioned one way. Several agents prompted differently produce genuinely different readings of the same task, and disagreement between them is signal — the same principle that made self-consistency work (→ 2.5), applied at the level of roles instead of samples.

A **multi-agent system** = a configuration of several agents whose cooperation is arranged by an orchestration layer — code or a designated agent — that routes tasks and results between them.

## 6.2 Division-of-Labor Patterns

The workflow patterns of Chapter 1 reappear here with agents as the parts. Four cover most systems in use.

| Pattern | Arrangement | Fits |
|---|---|---|
| Pipeline | A → B → C, each output the next input | stages with a natural order (research → write → edit) |
| Parallel + aggregate | A₁ … Aₙ work independently; an aggregator merges | divisible work (sections, files); independent votes |
| Orchestrator–workers | a lead agent decomposes the task at run time and dispatches workers | subtasks unknown until the input arrives |
| Evaluator–optimizer | a generator agent and a critic agent alternate | quality gates; Chapter 5's reflection with the critic externalized |

> **[Figure 6.1]** The four patterns as four small box-and-arrow diagrams in one row: a pipeline's straight chain; parallel branches converging on an aggregator; an orchestrator node fanning out to workers and collecting; a generator–critic pair joined by a two-way arrow with an exit on the critic's "pass" verdict. Under each, one line naming what the arrangement buys.

Two of these are old acquaintances in new form. Evaluator–optimizer is Self-Refine (→ 5.2) with generator and critic given separate contexts, which removes the shared-framing weakness of self-critique. Orchestrator–workers is planning (→ Ch. 7) with the plan's steps executed by dispatched agents instead of a single loop.

The choice among patterns follows the task's structure, and the fallback is always the simplest arrangement that fits: a fixed pipeline where stages are known, dynamic orchestration only where they are not.

## 6.3 Communication and Shared State

Agents cooperate through two channels, and the choice shapes the system's failure modes.

**Message passing** — one agent's output becomes another's input, usually as a structured handoff (the JSON discipline of Chapter 3 applied between agents). The properties: explicit, inspectable, and lossy by design — the receiver knows only what the message carries. A researcher-to-writer handoff in a report pipeline looks like this:

```
{ "topic":    "test-time compute",
  "findings": [
    "Self-consistency: N samples + majority vote (Wang et al., 2022)",
    "Snell et al. 2024: compute-optimal allocation beats fixed N"
  ],
  "sources":  ["arxiv.org/abs/2203.11171", "arxiv.org/abs/2408.03314"] }
```

The writer's context receives these three fields and nothing else. That is the point — and the risk. If the researcher also learned that the two papers disagree on when extra samples stop paying, but the schema has no field for caveats, the writer will present both results as if they compose cleanly. The message was well-formed; the omission is invisible; the report is confidently wrong. Whatever the researcher fails to put into the findings, the writer does not know.

**Shared store** — agents read and write a common substrate: files, a database, a scratch document. The properties are inverted: nothing is lost, but nothing is scoped either — every agent must know the store's conventions, and two agents writing the same record need coordination.

Both channels exist to buy **context isolation**, the central payoff of the split: each agent's window holds only its role's material, so prompts stay short, attention stays on-task, and cost stays linear. The price is that information no longer travels implicitly. In a single agent, everything seen is available; in a multi-agent system, an agent cannot use what no handoff gave it, and the characteristic failure is the one above — a downstream agent working confidently from an upstream omission. Debugging therefore starts from the handoffs: the messages and store records between agents are the trace to read (→ 5.10, error analysis applied per component; → 4.6, trace reading inside a single agent).

## 6.4 Frameworks and Protocols

The orchestration layer is ordinary code, and frameworks package its recurring shapes. Graph orchestrators (LangGraph is the current representative) express a system as a graph: nodes are agents or steps, edges are control flow, and a typed shared state moves along the edges — the patterns of 6.2 become graph topologies. The lab track uses plain code for orchestration — the patterns are visible without a framework — and the graph formulation returns with the final-project labs.

The seam between agents and their tools has a standard of its own. Function calling (→ 3.3) standardized the call format between one application and one model API; it did not standardize where tools come from. Every agent wires its own — a research agent, a coding agent, and a pipeline that each want GitHub access implement GitHub tools three times. M agents × N services = M×N private integrations, and the multiplication is felt precisely when a system grows to many agents.

**MCP (Model Context Protocol)** = an open protocol, released by Anthropic in November 2024, that standardizes how applications connect models to tools and data sources. An **MCP server** wraps one service and exposes its tools over the protocol; the application (the **host**) runs an **MCP client** per connection, discovers what a server offers at connection time (`tools/list`), and calls by name (`tools/call`). A service wrapped once serves every agent that speaks the protocol: M×N becomes M+N, and a server-side change reaches every connected agent without a code change. MCP does not replace function calling — at the model boundary schemas still travel in `tools` and calls return in `tool_calls`; what it standardizes is where the schemas come from. Prebuilt servers exist for common services (GitHub, Google Drive, Slack, PostgreSQL), clients ship in editors and chat applications, and major vendors beyond the protocol's origin announced support in 2025.

> **[Figure 6.2]** Left: M agents × N services drawn as a full bipartite tangle of private integrations. Right: the same agents and services joined through the protocol — each agent speaks MCP once, each service is wrapped by one MCP server — and the edge count collapses from M×N to M+N. Annotate one server box with `tools/list` / `tools/call` to show discovery and call.

The caution restates the capability boundary (→ 3.6): a server's tool list is capability granted to the agent, and its descriptions and results are third-party text entering the context — connect servers as deliberately as you register tools. In a multi-agent system the deliberation is per agent: the researcher may hold the search server, and the writer none at all.

## 6.5 Adoption Criteria

The split is not free, and its costs are the mirror of its benefits. Every handoff adds latency and tokens; total cost multiplies with agent count. Handoff schemas are interfaces that must be designed and kept stable. And errors propagate: one wrong handoff poisons every agent downstream, so a many-agent system without per-component evaluation (→ Ch. 5) fails as a whole with no indication of where.

The default is therefore one agent. The split is justified when a measured bottleneck names the seam: a role whose instructions conflict with another's, a context that a partition would keep small, a stage that needs an independent check. Splitting on architecture-diagram aesthetics, with no bottleneck in evidence, buys cost and debugging surface with no return.

## 6.6 Summary

One agent, one context reaches its limits by role interference, context growth, and the absence of independent perspective. The remedy arranges several agents — each with its own prompt, context, and tools, each a Chapter 4 loop inside — under an orchestration layer, in four recurring patterns: pipeline, parallel-aggregate, orchestrator–workers, evaluator–optimizer. Cooperation runs over explicit messages or a shared store, and both exist to buy context isolation, whose price is that nothing travels implicitly — the characteristic failure is a downstream agent confident on an upstream omission. Frameworks package the orchestration shapes as graphs, and MCP standardizes the agent–tool seam, turning M×N private integrations into M+N. The split is adopted against a measured bottleneck, never by default, and per-component evaluation is what keeps the assembled system debuggable.

Every arrangement in this chapter took its step sequence from somewhere: the pipeline's stages were fixed by us, and the orchestrator decomposed tasks at run time by judgment alone. What it means to produce that decomposition well — to draw the whole path before walking it, and to search among paths instead of committing to one — is planning, the subject of Chapter 7.

---

**Presentation.** AutoGen (Wu et al., 2023) — multi-agent cooperation as conversation, and what the conversation protocol buys; MetaGPT (Hong et al., 2023) — roles fixed by standard operating procedures, and structured handoffs as the error-control device. Both are heard through one question: what does the split cost, and what does each paper's coordination device buy back?

**Lab.** `W6_lab_multiagent.ipynb` — this chapter's patterns run end to end, from Andrew Ng's *Agentic AI* Module 5: a plan → reflect → execute → explain pipeline over an inventory store, with tool-only plans, a reflection review step, and a scored task set. Reference answers: `labs/checkpoints/week06/solution.py`.

**Homework.** `W6_hw_new_intent.ipynb` — push a new intent (an exchange) through a condensed pipeline end to end: the tool, its docstring, the planner extension, and a scored request, with the original three intents still passing (target 4/4). Due before W7.
