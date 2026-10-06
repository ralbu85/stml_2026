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

In Chapter 5, a reviewer model examined the result of a writer. That system already had two roles. This chapter uses several agents for one task. It explains how to divide the task and how to connect the results.

## Part 1. Multi-agent systems {#concepts}

### 1.1 Why use several agents {#introduction}

One agent can do a large task. But its instructions, tools, and history must then cover all parts of the task. An academic essay, for example, needs research on two questions, a draft, and a check of the sources. If one agent does all these parts, its instructions become long, and its history mixes all of them. We can divide the work among several agents instead.

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

A small essay team has four roles:

| Agent | Contribution |
|---|---|
| Researcher A | Searches for facts on the first question, and reports each fact with its source |
| Researcher B | Searches for facts on the second question, and reports each fact with its source |
| Writer | Combines the two sets of notes into an essay with citations |
| Reviewer | Checks each citation of the draft against the notes |

### 1.3 What a division gives {#purpose}

A division of the task gives three possible advantages:

1. **Specialization.** Each agent receives only the instructions and tools for its part.
2. **Parallel work.** Parts that do not depend on each other can run at the same time.
3. **Review.** Another agent can examine a result against the task, as the reviewer did in Chapter 5.

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

An agent knows only what is in its messages. For this reason, a handoff must carry the findings, not only a report that the work is done. "Research: done" does not help the writer. A note such as "Large language models are trained on vast amounts of text [Large language model]" gives the writer a fact and its source.

### 2.3 Coordination {#coordination}

::: {.callout-tip icon=false}
## Coordination

The decision of which agent works next and what it receives.
:::

**Integration** combines the results of the agents into one result.

The order of the work comes from the dependencies. An agent that needs the output of another agent must wait for it. Agents that do not need each other's output can work in parallel. In the essay team, the two researchers can start at the same time. The writer waits for both sets of notes, and the reviewer waits for the draft.

::: {.diagram-scroll tabindex="0" role="region" aria-label="Essay task dependencies"}
![The two researchers work in parallel. The writer needs both sets of notes.](figures/essay/dependencies.svg){fig-alt="The essay question goes to researcher A and researcher B. Their notes both go to the writer, and the draft goes to the reviewer."}
:::

Code can do the coordination with a fixed order. An agent can also do it: it reads each result and decides the next task. These two choices lead to different communication structures.

::: {.checkpoint}
### Check 1 · A handoff

The writer receives only this message: "Research: done." Which information is not in the message, and where must it come from?

<details class="answer">
<summary>Read the answer</summary>

The message gives no facts and no sources. They must come from the notes of the two researchers, in the message to the writer. Without them, the writer uses its own knowledge and can cite sources that no researcher found.

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

A system can combine these structures. For example, a manager can run two researchers in parallel. Select the structure that matches the dependencies of the task.

### 3.2 A coordinator agent {#manager}

In the manager structure, an agent is the coordinator. The coordinator uses the other agents as its tools. To make an agent into a tool, put it in a function. The argument of the function is the task. The function returns the answer of the agent. The loop of the coordinator then calls these functions, as the agent loop of Chapter 4 calls tools.

::: {.diagram-scroll tabindex="0" role="region" aria-label="Essay team with a coordinator"}
![The coordinator gives tasks to the four roles and receives their results.](figures/essay/system.svg){fig-alt="The user sends the essay question to the coordinator. The coordinator exchanges tasks and results with researcher A, researcher B, the writer, and the reviewer, then returns the final essay to the user."}
:::

Is a team better than one agent? To find out, use an evaluation from Chapter 5. Give both systems the same requests, and grade both with the same criteria. Also compare the model calls.

::: {.checkpoint}
### Check 2 · Choose a structure

The review changes the next task: if the reviewer finds a claim that no note supports, the writer must revise. Which structure fits, sequential or manager?

<details class="answer">
<summary>Read the answer</summary>

The manager structure. The coordinator reads the review and then decides the next task. A sequential structure has a fixed order before the run.

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
| Role | `researcher_a = Agent(RESEARCHER_SYSTEM, [wikipedia_search])` |
| Task for a role | `notes_a = researcher_a.ask(QUESTION_A)` |
| Handoff | `writer.ask(handoff)`: `handoff` contains the essay question and the notes of both researchers |
| Review | `reviewer.ask(review_request(notes_a + "\n" + notes_b, draft))` |
| Targeted revision | `writer.ask("A reviewer found:\n" + review + ...)`, only when the review lists a problem |
| Agent as a tool | `def ask_researcher_b(task: str): return researcher_b_team.ask(task)` |
| Coordinator agent | `Agent(COORDINATOR_SYSTEM, [ask_researcher_a, ask_researcher_b, ask_writer, ask_reviewer])` |
| Cost of the team | The sum of `total_tokens` of all objects |

## Lab {#lab-guide}

1. Make one `Agent` object for each role: two researchers with Wikipedia search, a writer, and a reviewer.
2. Compare a handoff that says only "Research: done" with a handoff that carries the notes. Check the citations with code.
3. Write the instructions of the reviewer. Revise only when the review lists a problem.
4. Let a coordinator agent assign the work, with the roles as its tools.
5. Check the final essay with code, and compare the cost of the two runs.

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
