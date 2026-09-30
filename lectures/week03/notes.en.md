---
title: "Chapter 3. Tool Use"
subtitle: "Describe a function to the model, run it, and return its result"
lang: en
---

<!-- course-navigation:start -->
<nav class="chapter-nav" aria-label="Course navigation">
<a href="../../index.html">Home</a>
<a href="../reading.html">All chapters</a>
<a href="../../week03.html">Week 3 materials</a>
</nav>
<!-- course-navigation:end -->

<div class="reading-tools" role="group" aria-label="Reading options">
<button id="classroom-toggle" type="button" aria-pressed="false">Larger text</button>
<button id="answers-toggle" type="button" aria-pressed="false">Show all answers</button>
</div>

::: {.callout-note appearance="minimal"}
## Learning objectives

- Define a tool, and explain why a model needs tools.
- Define a tool definition, and name its three parts.
- Explain the four steps of a tool call.
- Define function calling, and explain what it changes.
- Explain how one tool result can give the input of the next request.
:::

In Chapter 2, a prompt guided the text that the model writes. Some tasks need information that text generation cannot produce. For example, a model cannot read a clock. This chapter shows how a model uses a **tool** to get this information.

## 3.1 Tool {#why-tools}

A model generates text from its input. It cannot read a clock, search the web, or query a database by itself. For the question "What time is it in Seoul?", a model can only write a guess. To get the real time, a program must run code that reads a clock.

::: {.callout-tip icon=false}
## Tool

A function that an LLM can ask a program to run. The program runs the function and gives the result back to the model.
:::

The tools set what an agent can do. A prompt cannot add a new capability. A new capability needs a new tool.

## 3.2 Tool definition {#tool-definition}

The model must know which tools exist and what input each tool needs.

::: {.callout-tip icon=false}
## Tool definition

The description of a tool that the model receives. It has a name, a description, and parameters.
:::

1. **Name:** for example `get_current_time`.
2. **Description:** what the tool does and what it returns.
3. **Parameters:** the inputs, with a type and a description for each input.

In Python, the function name, the docstring, and the type annotations contain these three parts. The model receives only the definition. The program keeps the function and runs it.

A **parameter** is a named input, for example `timezone_name`. An **argument** is the value for that input in one call, for example `"Asia/Seoul"`.

## 3.3 Tool call {#clock-exchange}

::: {.callout-tip icon=false}
## Tool call

One exchange in which the model requests a tool, the program runs the tool, and the model receives the result. It is also called a **round trip**.
:::

A tool call has four steps:

1. **Request.** The model receives the task and the tool definitions. It writes a request: the tool name and the arguments.
2. **Execute.** The program runs the function with these arguments.
3. **Return.** The program adds the result to the conversation and calls the model again.
4. **Answer.** The model writes the answer from the result.

![The application sends the task and the tool definition. The model writes a request. The application runs the function and returns the result. The model then answers or writes another request.](figures/fig-3-1-round-trip-swimlane.svg){#fig-round-trip fig-alt="Application and model lanes: 1. task and tool schema go to the model; 2. the model requests get_current_time; 3–4. the application parses, validates, and executes it; 5. the result goes back to the model, which answers or writes another request."}

The result of a tool is an **observation**. The model writes the request, but the program runs the function. The model decides if it needs a tool. If it does not need a tool, it writes the answer directly.

::: {.checkpoint}
### Check 1 · Who runs the tool?

The model writes `get_current_time("Asia/Seoul")`. What must the program do before the model can answer?

<details class="answer">
<summary>Read the answer</summary>

Run the function to read the clock. Then send the result to the model in the next call.

</details>
:::

## 3.4 Function calling {#function-calling}

A tool call can work with plain text. The system message lists the tool definitions, and the model writes the request as text. Then the program must find the function name and the arguments in that text.

::: {.callout-tip icon=false}
## Function calling

An API feature for tool calls. The program sends the tool definitions in a separate field, and the model returns each request as a tool name and arguments in separate fields.
:::

1. The program sends each tool definition as a JSON object, called a **schema**.
2. The model returns a request with the tool name, the arguments, and an id.
3. The program runs the function.
4. The program returns the result in a message with the role `tool` and the same id.

Function calling changes the form of the request and the result. It does not change who runs the tool: the program still runs it.

## 3.5 Dependent requests {#dependent-calls}

Sometimes the input of a tool is not in the question. Then an earlier tool result must give it.

::: {.callout-tip icon=false}
## Dependent request

A tool request whose arguments come from the result of an earlier tool call.
:::

For example, a forecast tool needs a city, but the question names only a palace. The model first requests a search for the location of the palace. Then it requests the forecast for the city in the search result.

A dependent request is possible because each result goes back to the model before the next request. Chapter 4 repeats these tool calls in a loop.

::: {.checkpoint}
### Check 2 · Why return the result first?

Why must the search result go back to the model before the forecast request?

<details class="answer">
<summary>Read the answer</summary>

The model writes the forecast request from the search result. Without the result, the model does not know the city.

</details>
:::

## 3.6 Learning to use tools {#toolformer}

In this chapter, the tool definitions in the input tell the model which tools exist. Training can also teach a model when to call a tool.

**Toolformer** trains a model on text that contains useful tool calls. The method keeps a call only when its result helps the model predict the next words (Schick et al., 2023). Training teaches the model when to request a tool. The program still runs the tool.

## Summary {#recap}

- A tool is a function that an LLM can ask a program to run.
- A tool definition has a name, a description, and parameters. The model receives the definition, and the program keeps the function.
- A tool call has four steps: request, execute, return, and answer.
- Function calling puts the definitions and the requests in separate API fields. The program still runs the tool.
- In a dependent request, the arguments come from an earlier tool result.

## Lab preparation: from concept to code {#implementation}

The lab first does the tool call by hand. Then it uses function calling in the `aisuite` library. `tools=[...]` sends the definitions, and `max_turns` sets the number of model calls. The library then does all four steps.

| Concept | Lab code (short form) |
|--|-------|
| Tool function | `def get_current_time(timezone_name: str = ""):` with a docstring |
| Tool definition in the system prompt | `TOOL_LIST_SYSTEM = """Available tools: - get_current_time(timezone_name: str): ..."""` |
| Request | `call_text = response.choices[0].message.content` |
| Execute | `result = eval(call_text)` |
| Return | `messages.append({"role": "user", "content": f"Tool result: {result}"})` |
| Answer | `client.chat.completions.create(model=MODEL, messages=messages)` |
| Function calling | `client.chat.completions.create(model=MODEL, messages=messages, tools=[get_current_time], max_turns=2)` |
| Dependent requests | `tools=[web_search, get_forecast], max_turns=3` |

## Lab {#lab-connection}

1. Ask the model for the time without a tool.
2. Do the clock tool call by hand: request, execute, return, and answer.
3. Do the same tool call with `tools=[get_current_time]`.
4. Add weather tools, and add a forecast tool.
5. Ask about a place. Find how the search result gives the input of the forecast request.

[Lab notebook in Colab](https://colab.research.google.com/github/ralbu85/stml_2026/blob/main/lectures/week03/W3_lab_tools.ipynb) · [Homework notebook in Colab](https://colab.research.google.com/github/ralbu85/stml_2026/blob/main/lectures/week03/W3_hw_new_tool.ipynb) · [Week 3 materials](../../week03.html)

## Materials and sources {.unnumbered #sources}

- [Anthropic — Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview): tool definitions, requests, and execution.
- Schick et al., [Toolformer](https://arxiv.org/abs/2302.04761) (2023): a model learns tool calls from text with useful calls.
- Qin et al., [ToolLLM](https://arxiv.org/abs/2307.16789) (2023): a model learns to use a large set of APIs.

<!-- course-pagination:start -->
<nav class="chapter-pagination" aria-label="Previous and next chapters">
<a href="../week02/notes.html" rel="prev">← Previous: 2 · Prompting &amp; Reasoning</a>
<a href="../week04/notes.html" rel="next">Next →: 4 · The Agent Loop and ReAct</a>
</nav>
<!-- course-pagination:end -->
