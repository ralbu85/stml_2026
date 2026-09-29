---
title: "Chapter 1. What is an Agent?"
subtitle: "From a model call to a system that acts"
lang: en
---

<!-- course-navigation:start -->
<nav class="chapter-nav" aria-label="Course navigation">
<a href="../../index.html">Home</a>
<a href="../reading.html">All chapters</a>
<a href="../../week01.html">Week 1 materials</a>
</nav>
<!-- course-navigation:end -->

<div class="reading-tools" role="group" aria-label="Reading options">
<button id="classroom-toggle" type="button" aria-pressed="false">Larger text</button>
<button id="answers-toggle" type="button" aria-pressed="false">Show all answers</button>
</div>

::: {.callout-note appearance="minimal"}
## Learning objectives

- Explain what one model call receives and returns.
- Define an agent, and explain the roles of the model and the program.
- Name the four components of an agent.
- Explain the difference between a workflow and an agent.
- Select an amount of autonomy for a task.
:::

A language model receives text and returns text. Many tasks need more than text. For example, "Reserve a study room" needs a change in a reservation system, and a written reply cannot make that change. This chapter explains how a system around the model can act and use the results.

## 1.1 One model call {#model-call}

A **large language model (LLM)** is a model that receives a sequence of tokens and generates more tokens. A **token** is a unit of text, such as a word or a part of a word.

The input to one call is the **prompt**. It can contain instructions, the request of the user, documents, and earlier messages. The information that one call receives is its **context**.

A model call has three properties:

1. **It writes text only.** The model can write an explanation, a plan, or a request for an operation. It cannot do the operation.
2. **It keeps no memory between calls.** A second call does not know the first call. To continue a conversation, the program sends the earlier messages again.
3. **Its output can vary.** An option called **temperature** controls how much the output changes from one call to the next.

For this reason, a model call alone cannot complete a task that needs actions. The next section adds the parts that do the actions.

## 1.2 Agent {#agent}

::: {.callout-tip icon=false}
## Agent

A system that uses the available information to select actions toward a goal. In an **LLM-based agent**, the model selects the actions, and the program runs them and returns the results.
:::

An agent works in four steps:

1. The program gives the task and the latest results to the model.
2. The model selects the next action, or it writes the final answer.
3. The program runs the selected action.
4. The result becomes part of the input for the next call.

These steps repeat. This repetition is the **agent loop**. The loop stops when the model writes the final answer, or when the number of steps gets to a limit.

The agent is the whole system. The model is one part of it. The model decides what to do. The program does the actions and keeps the results.

## 1.3 Components {#components}

To build an agent, you must know its parts. An agent has four components:

| Component | Role |
|--|------|
| Model | Reads the context, and writes a reply or a request for an action |
| Instructions | Tell the model how to do the task, for example "Report a reservation only after the service confirms it" |
| Tools | Functions or services that the program runs for the model, for example a room search or a reservation |
| Memory | Information that the program keeps between steps, for example the request and the results so far |

A tool is code that the program runs. An instruction cannot replace a tool. Memory helps a call only when the program puts it into the context of that call.

::: {.checkpoint}
### Check 1 · Instruction or tool?

A program has a room search tool but no reservation tool. Can the instruction "You can make reservations" make the agent book a room?

<details class="answer">
<summary>Read the answer</summary>

No. The program needs a reservation tool. An instruction changes what the model reads. It does not add an operation.

</details>
:::

## 1.4 Workflows and agents {#control-flow}

Many systems make several model calls. Not all of them are agents. The difference is the part that selects the next step.

**Control flow** is the order of the operations in a program, with its branches, repetitions, and stop conditions.

- In a **workflow**, code sets the control flow before the run. The model does fixed work at fixed points.
- In an **agent**, the output of the model selects the next step. The result of each step goes back into the input.

![In a workflow, code fixes the path. In an agent, the output of the model selects an action or the final answer, and each result goes back into the input.](figures/fig-1-2-loop-vs-workflow.svg){#fig-workflow-agent width="100%" fig-alt="Workflow: Input, LLM call, LLM call, Output, with a fixed path. Agent: the model reads the input, then selects an action or a final answer; tool execution appends the result to the input."}

**Autonomy** is the set of decisions that a system makes without a new instruction from a person. A workflow gives the model few decisions. An agent gives the model more decisions.

Five workflow patterns are common:

| Pattern | Organization |
|--|------|
| Prompt chaining | Each step uses the output of the step before it. |
| Routing | A first step classifies the input and selects a path. |
| Parallelization | Independent calls run at the same time, and a last step combines the results. |
| Orchestrator–workers | One model divides the task and gives the parts to other calls. |
| Evaluator–optimizer | One call examines a result, and another call revises it. |

This course studies four capabilities of agentic systems: tool use, reflection, planning, and multi-agent collaboration.

## 1.5 How much autonomy {#autonomy-and-completion}

More autonomy gives more flexibility, and it also gives more points where the model can make a wrong decision. Select the autonomy that the task needs:

- If you know the steps before the run, use a workflow.
- If the results of a step change what to do next, give that decision to the model.

In both cases, the program sets the limits. It sets the tools that the model can use, and it sets a **stop condition**: a rule that ends the run. A task is complete only when a result from a tool shows it, for example a reservation confirmation.

::: {.checkpoint}
### Check 2 · Workflow or agent?

Code tries room R12. If the reservation fails, code tries room R18. Then a model writes the confirmation message. Is this a workflow or an agent?

<details class="answer">
<summary>Read the answer</summary>

A workflow. Code selects each step. The model only writes the message at a fixed point.

</details>
:::

## Summary {#recap}

- One model call receives a prompt and returns text. It keeps no memory between calls.
- An agent is a system in which the model selects actions and the program runs them and returns the results.
- An agent has four components: a model, instructions, tools, and memory.
- In a workflow, code selects the next step. In an agent, the model selects it.
- Give the model only the decisions that the task needs, and let a tool result show completion.

## Lab preparation: from concept to code {#implementation}

The lab uses the `aisuite` client. One call sends a list of messages and returns a reply.

| Concept | Lab code (short form) |
|--|-------|
| One model call | `client.chat.completions.create(model=MODEL, messages=messages)` |
| Reply text | `response.choices[0].message.content` |
| Instructions | `{"role": "system", "content": "Answer in one sentence, for a graduate ML audience."}` |
| Request of the user | `{"role": "user", "content": QUESTION}` |
| Memory of a conversation | `conversation.append({"role": "assistant", "content": reply})`, then send the whole list again |
| Temperature | `temperature=0.0` and `temperature=1`: the same prompt five times |
| Output format | `response_format={"type": "json_object"}`, then `json.loads` |
| Tokens and cost | `response.usage.prompt_tokens`, `response.usage.completion_tokens` |

## Lab {#lab-guide}

1. Make one model call, and read the reply.
2. Add a system message, and compare the two replies.
3. Send a second call without the history, and then with the history.
4. Send the same prompt five times at two temperatures.
5. Ask for JSON, and parse the reply with code.

[Lab notebook in Colab](https://colab.research.google.com/github/ralbu85/stml_2026/blob/main/lectures/week01/W1_lab_setup.ipynb)

## Materials and sources {#readings}

- [Anthropic — Building effective agents](https://www.anthropic.com/engineering/building-effective-agents): workflows, agents, and the five workflow patterns.
- [Hugging Face — What are agents?](https://huggingface.co/docs/smolagents/conceptual_guides/intro_agents): degrees of model control over the program flow.
- [Andrew Ng — Agentic AI](https://www.deeplearning.ai/courses/agentic-ai): tool use, reflection, planning, and multi-agent collaboration.

<!-- course-pagination:start -->
<nav class="chapter-pagination" aria-label="Previous and next chapters">
<a href="../week02/notes.html" rel="next">Next →: 2 · Prompting &amp; Reasoning</a>
</nav>
<!-- course-pagination:end -->
