---
title: "Chapter 6. Multi-Agent Systems"
subtitle: "Divide a task among agents · Connect their results"
---

<!-- course-navigation:start -->
<nav class="chapter-nav" aria-label="Course navigation">
<a href="../../index.html">Home</a>
<a href="../reading.html">All chapters</a>
<a href="../../week06.html">Week 6 materials</a>
</nav>
<!-- course-navigation:end -->
<div class="reading-tools" role="group" aria-label="Reading options">
<button id="classroom-toggle" type="button" aria-pressed="false">Larger text</button>
<button id="answers-toggle" type="button" aria-pressed="false">Show all answers</button>
</div>

::: {.callout-note appearance="minimal"}
## Learning objectives

- Explain what a multi-agent system is and why a task can use one.
- Define a role, a handoff, and coordination.
- Define a communication structure, and name the four structures and the situation for each.
- Build a team of `Agent` objects, with a coordinator agent.
:::

In Chapter 5, one agent wrote an essay, evaluated it, and improved it. This chapter divides one task among several agents, and each agent does its own part of the work. It explains how to divide the task and how to connect the results.

## Part 1. Multi-agent systems {#concepts}

### 1.1 Why use several agents {#introduction}

One agent can do a large task. But its instructions, tools, and history must then cover all parts of the task. The essay agent of Chapter 5 is an example. It searched for facts, wrote the essay, and evaluated the essay. Its one system message described all these parts, and its one history held each search result, each draft, and each evaluation. We can divide the work among several agents instead.

### 1.2 Multi-agent system {#definition}

::: {.callout-tip icon=false}
## Multi-agent system

A system in which several agents do parts of one task and exchange their results to complete the task.
:::

Each agent in the system has a role.

::: {.callout-tip icon=false}
## Role

The responsibility of one agent in a multi-agent system. An agent in a role has its own instructions, its own tools, and its own history.
:::

Two agents can use the same model. Their roles make them different.

A small essay team does the work of the Chapter 5 agent with three roles:

| Agent | Contribution |
|---|---|
| Writer | Searches for facts, and writes or improves the essay |
| Evaluator | Examines the essay against its own searches, and writes an evaluation |
| Coordinator | Decides which agent works next, and when the essay is finished (Section 3.2) |

### 1.3 What a division gives {#purpose}

A division of the task gives three possible advantages:

1. **Specialization.** Each agent receives only the instructions and tools for its part.
2. **Parallel work.** Parts that do not depend on each other can run at the same time.
3. **Review.** Another agent can examine a result with its own instructions and its own history. In Chapter 5, the agent that wrote the essay also evaluated it.

Each agent adds model calls. For this reason, use several agents when the division makes the task easier to do or to examine.

## Part 2. Collaboration {#collaboration}

### 2.1 Roles {#role-assignment}

A role has three parts:

1. **A task:** the part of the work that the agent does.
2. **Information and tools:** what the agent needs for that task.
3. **An output:** a result that another agent or the user uses.

In code, the system message gives the task, the tool list gives the tools, and the returned answer is the output.

### 2.2 Handoff {#information-exchange}

Agents exchange messages: tasks, findings, questions, and feedback.

::: {.callout-tip icon=false}
## Handoff

The transfer of a task and the information that is necessary to continue it.
:::

An agent knows only what is in its messages. For this reason, a handoff must carry the findings, not only a report that the work is done. "The essay is ready. Evaluate it." does not help the evaluator, because the message carries no essay. A message with the question and the essay gives the evaluator the text that it must examine.

### 2.3 Coordination {#coordination}

::: {.callout-tip icon=false}
## Coordination

The decision of which agent works next and what it receives.
:::

**Integration** combines the results of the agents into one result.

The order of the work comes from the dependencies. An agent that needs the output of another agent must wait for it. Agents that do not need each other's output can work in parallel. In the essay team, the evaluator needs the essay, so it waits for the writer. The writer needs the evaluation to improve the essay, so it then waits for the evaluator. No two steps of this team can run in parallel. Two evaluators that examine different points of the same essay could work in parallel.

::: {.diagram-scroll tabindex="0" role="region" aria-label="Essay task dependencies"}
![The evaluator needs the essay. The writer needs the evaluation.](figures/team/dependencies.svg){fig-alt="The essay question goes to the writer. The essay goes to the evaluator. The evaluation goes back to the writer."}
:::

Code can do the coordination with a fixed order. An agent can also do it: it reads each result and decides the next task. These two choices lead to different communication structures.

::: {.checkpoint}
### Check 1 · A handoff

The evaluator receives only this message: "The essay is ready. Evaluate it." Which information is not in the message, and where must it come from?

<details class="answer">
<summary>Read the answer</summary>

The message gives no essay and no question. The essay must come from the output of the writer, in the message to the evaluator. The evaluator has its own history, so it cannot read the list of the writer.

</details>
:::

## Part 3. Communication structures {#structures}

### 3.1 Four structures {#comparison}

::: {.callout-tip icon=false}
## Communication structure

The pattern of which agents send messages to which agents.
:::

| Structure | How work passes | Use it when |
|--|-----|----|
| Sequential | Each agent gives its output to the next agent, in a fixed order. | The order of the work is known before the run. |
| Manager | A coordinator gives tasks to agents and receives their results. | The next task depends on the results. |
| Hierarchical | A manager gives large parts to leads. Each lead manages its own agents. | Each large part needs its own team. |
| All-to-all | Each agent can send messages to each other agent. | Agents must frequently agree on details. |

A system can combine these structures. For example, a manager can run several writers in parallel, one for each part of a long report. Select the structure that matches the dependencies of the task.

### 3.2 A coordinator agent {#manager}

In the manager structure, an agent is the coordinator. The coordinator uses the other agents as its tools. To make an agent into a tool, put it in a function. The argument of the function is the task. The function returns the answer of the agent. The loop of the coordinator then calls these functions, as the agent loop of Chapter 4 calls tools.

::: {.diagram-scroll tabindex="0" role="region" aria-label="Essay team with a coordinator"}
![The coordinator gives tasks to the writer and the evaluator, and receives their results.](figures/team/system.svg){fig-alt="The user sends the question to the coordinator. The coordinator exchanges tasks and results with the writer and the evaluator, then returns the final essay to the user."}
:::

Is a team better than one agent? To find out, use an evaluation from Chapter 5. Give both systems the same requests, and grade both with the same criteria. Also compare the model calls.

::: {.checkpoint}
### Check 2 · Choose a structure

The number of revisions that an essay needs is not known before the run: the next step depends on what the evaluation finds. Which structure fits, sequential or manager?

<details class="answer">
<summary>Read the answer</summary>

The manager structure. The coordinator reads each evaluation and decides the next task: one more revision, or the final essay. A sequential structure has fixed tasks in a fixed order before the run. A coordinator agent adds model calls, and its handoffs can lose information, so measure the result.

</details>
:::

## Summary {#recap}

- A multi-agent system divides one task among agents and connects their results.
- A role has a task, information and tools, and an output.
- A handoff carries the task and the findings. An agent knows only what is in its messages.
- Coordination follows the dependencies. Code or a coordinator agent can do it.
- A communication structure is the pattern of messages between agents: sequential, manager, hierarchical, or all-to-all.

## Lab preparation: from concept to code {#implementation}

The lab uses the `Agent` class from the practice notebook. Each role is one `Agent` object. A handoff is a user message to the next object.

| Concept | Lab code (short form) |
|--|-------|
| One agent (Chapter 5) | `single = Agent(REFLECT_SYSTEM, [wikipedia_search])`: one object writes and evaluates |
| Role | `writer = Agent(WRITER_SYSTEM, [wikipedia_search])` and `evaluator = Agent(EVALUATOR_SYSTEM, [wikipedia_search])` |
| Handoff | `evaluator.ask(handoff)`: `handoff` holds the question and the essay; then `writer.ask(...)` with the evaluation |
| Agent as a tool | `def ask_evaluator(task: str): return evaluator_team.ask(task)` |
| Coordinator agent | `Agent(COORDINATOR_SYSTEM, [ask_writer, ask_evaluator])` |
| Compare the systems | `judge_essay(QUESTION, essay)` of Chapter 5, a code check of the citations, and the sum of `total_tokens` |

## Lab {#lab-guide}

1. Run the single agent of the Week 5 lab again: one object writes, evaluates, and improves the essay.
2. Divide the work between a writer and an evaluator, and write the handoff between them.
3. Let a coordinator agent run the two roles as its tools.
4. Compare the three systems on the same question: the scores of the judge, the citations, and the tokens.

[Lab notebook in Colab](https://colab.research.google.com/github/ralbu85/stml_2026/blob/main/lectures/week06/W6_lab_multiagent.ipynb) · [Download the lab](W6_lab_multiagent.ipynb) · [Homework notebook](W6_hw_new_intent.ipynb).

## Materials and sources {.unnumbered #sources}

- Wu et al., [AutoGen](https://arxiv.org/abs/2308.08155) (2023): agents that collaborate through conversations.
- Hong et al., [MetaGPT](https://arxiv.org/abs/2308.00352) (2023): roles that follow set procedures and exchange work products.
- Anthropic, [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) (2024): workflow patterns, such as orchestrator and workers.

<!-- course-pagination:start -->
<nav class="chapter-pagination" aria-label="Previous and next chapters">
<a href="../week05/notes.html" rel="prev">← Previous: 5 · Reflection &amp; Evaluation</a>
<a href="../week07/notes.html" rel="next">Next →: 7 · Planning &amp; Search</a>
</nav>
<!-- course-pagination:end -->
