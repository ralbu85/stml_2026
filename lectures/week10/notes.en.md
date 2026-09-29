---
title: "Chapter 9. Context Engineering"
subtitle: "Build the input of each model call within its limits"
---

<!-- course-navigation:start -->
<nav class="chapter-nav" aria-label="Course navigation">
<a href="../../index.html">Home</a>
<a href="../reading.html">All chapters</a>
<a href="../../week10.html">Week 10 materials</a>
</nav>
<!-- course-navigation:end -->
<div class="reading-tools" role="group" aria-label="Reading options">
<button id="classroom-toggle" type="button" aria-pressed="false">Larger text</button>
<button id="answers-toggle" type="button" aria-pressed="false">Show all answers</button>
</div>

::: {.callout-note appearance="minimal"}
## Learning objectives

- Explain what the context of a model call contains.
- Explain the difference between stored information and the current context.
- Explain the two limits of context: capacity and use.
- Explain the three operations that manage context: select, structure, and compress.
- Explain how an agent builds the input again for each call.
:::

In Chapter 8, retrieval added document text to the input of the model. An agent adds more: conversation, tool descriptions, and tool results. The input has a limit, and the records of an agent grow with each step. This chapter explains how to build the input for each model call.

## Part 1. Context {#context}

### 1.1 Context and context engineering {#definition}

The answer of a model depends on the model and on its input. The model sees only the information in the input of the current call.

::: {.callout-tip icon=false}
## Context

The complete input that a model receives for one call.
:::

::: {.callout-tip icon=false}
## Context engineering

The work to select and organize the information for a task, keep it within the input limit, and update it for each call.
:::

A context has these parts:

| Part | Role |
|---|---|
| Instructions | What to do, and which rules to obey |
| Current request | The question or task for this call |
| Conversation history | Earlier requirements, and what the model and the user said |
| Tool descriptions | The available operations, and how to request them |
| Retrieved text and tool results | External information for the answer or the next action |

Two familiar methods are parts of context engineering. **Prompt engineering** writes the instructions. **RAG** retrieves the external text.

### 1.2 Stored information and context {#stored}

Chapter 1 called the information that a program keeps between steps its **memory**. An application can store a full conversation or many documents. It sends only some parts of them in each model call. A stored record is not part of the context. The model can use a record only if the application puts it into the input of the current call.

::: {.checkpoint}
### Check 1 · Stored but not sent

An application stores a requirement of the user, but it does not send the requirement in the next call. Can the model obey the requirement?

<details class="answer">
<summary>Read the answer</summary>

No. The model sees only the input of the current call. Put the requirement into the input.

</details>
:::

## Part 2. The limits of context {#limits}

### 2.1 Context window and token budget {#window}

As in Chapter 1, a **token** is a unit of text that a model processes. A token can be a word, a part of a word, or a punctuation mark.

The **context window** is the maximum number of tokens that a model can process in one call. A **token budget** is the number of tokens that the application gives to a call or to one part of it. The instructions, the tool descriptions, the conversation, and the retrieved text share this budget. For many models, the window also contains the output, so keep space for the answer.

### 2.2 Capacity and use {#lost-in-the-middle}

Context has two different limits:

1. **Capacity.** The input does not fit in the window. Reduce the input.
2. **Use.** The input fits and contains the necessary information, but the model does not use it correctly.

Liu et al. (2023) showed the second limit. In their experiment, models used information at the start or the end of a long input better than information in the middle. This result is **Lost in the Middle**. An input that fits is not always an input that works. Examine the answer as well as the size of the input.

## Part 3. Select, structure, and compress {#management}

Three operations manage the context. Each operation changes a different property of the input.

| Operation | What it does | Change to the input |
|---|---|---|
| **Select** | Keep the information that the current task needs | Unrelated and duplicate records go out |
| **Structure** | Make the role of each part clear | Instructions, requirements, and evidence are separate, and each claim keeps its source and conditions |
| **Compress** | Make the input shorter and keep its necessary meaning | Long records become a short summary |

### 3.1 Select {#selection}

Select the records that help with the current request. An old requirement can still apply, and a recent message can be unrelated. **Trimming** removes records from the input by a rule, for example "keep only the last five messages". Trimming does not delete the stored records. It only keeps them out of this call.

### 3.2 Structure {#structure}

Give each part of the input a clear role. Put the instructions together, mark the requirements of the user, and label each piece of evidence with its source. Keep a rule next to its exception. Write instructions that state the necessary behavior: "Answer from the supplied passages, and cite the source."

### 3.3 Compress {#compression}

**Summarization** writes a shorter version of the records. Trimming keeps the original words. Summarization writes new words. A summary must keep the requirements, the numbers, and the conditions of the original. Compare the summary with the original before you use it.

::: {.checkpoint}
### Check 2 · Trimming or summarization?

One program keeps only the last two messages. Another program writes a short paragraph from the full conversation. Which program trims, and which program summarizes?

<details class="answer">
<summary>Read the answer</summary>

The first program trims: it removes earlier messages and keeps the original words. The second program summarizes: it writes new, shorter text.

</details>
:::

## Part 4. Build the input for each call {#updates}

### 4.1 The context loop {#loop}

An agent calls the model many times. After each call, new information arrives: a reply, a tool result, or a new message from the user. For this reason, the application builds the input again before each call:

1. Collect the available information: the request, the instructions, the stored records, and the new results.
2. Build the input. Select, structure, and compress. Make sure that the input fits the budget.
3. Call the model.
4. Store the reply or the tool result. Go back to step 1 for the next call.

![Before each call, the application selects from the available information and puts it into the context window. A tool result goes into the message history and becomes available for the next input.](figures/context/anthropic-prompt-vs-context.png){#fig-context-loop fig-alt="Anthropic diagram: possible context is curated into the context window of the model. The model requests a tool, and the tool result returns to the message history before the next curation step."}

### 4.2 Evaluate the input and the answer {#evaluation}

To compare two methods that build the input, keep the task, the stored records, and the model the same. Then examine three things:

1. **The input.** Does it still contain the necessary requirements, evidence, and conditions?
2. **The answer.** Does it answer the request, obey the requirements, and agree with the evidence?
3. **The cost.** How many tokens and calls did it use? Count the calls that write a summary too.

The best input is not the shortest input. It is the input that gives a correct answer within the budget.

## Summary {#recap}

- Context is the complete input of one model call. The model sees only this input.
- A stored record helps the model only if the application puts it into the input.
- Context has two limits: capacity (the input must fit) and use (the model must use the information).
- Three operations manage context: select, structure, and compress.
- An agent builds the input again before each call, and you evaluate the input and the answer together.

## Lab {#lab}

1. Continue a conversation. Compare the stored messages with the input that the model receives.
2. Keep a message out of the input, and do not delete it from storage.
3. Summarize earlier messages, and use the summary in the next call.
4. Answer questions about a document with three inputs: the full conversation, the recent messages, and a summary with the recent messages. Compare the inputs, the answers, and the token use.

[Lab page](lab.html) · [Download the notebook](W10_lab_context.ipynb). Upload the notebook to [Google Colab](https://colab.research.google.com/) to run it.

## Materials and sources {.unnumbered #sources}

- Anthropic, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents): the definition of context engineering and the context loop diagram.
- Liu et al., [Lost in the Middle](https://arxiv.org/abs/2307.03172) (2023): how the position of information in a long input changes its use.
- Jiang et al., [LLMLingua](https://arxiv.org/abs/2310.05736) (2023): prompt compression with a small language model.
- LangChain, [Context engineering for agents](https://www.langchain.com/blog/context-engineering-for-agents): trimming and summarization.
- [Source notes](sources.md): definitions, original figures, and adaptations for this course.

<!-- course-pagination:start -->
<nav class="chapter-pagination" aria-label="Previous and next chapters">
<a href="../week09/notes.html" rel="prev">← Previous: 8 · Retrieval-Augmented Generation</a>
</nav>
<!-- course-pagination:end -->
