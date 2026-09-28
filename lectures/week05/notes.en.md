---
title: "Chapter 5. Reflection & Evaluation"
subtitle: "Reviewing work · Measuring quality"
---

<!-- course-navigation:start -->
<nav class="chapter-nav" aria-label="Course navigation">
<a href="../../index.html">Home</a>
<a href="../reading.html">All chapters</a>
<a href="../../week05.html">Week 5 materials</a>
</nav>
<!-- course-navigation:end -->
<div class="reading-tools" role="group" aria-label="Reading options">
<button id="classroom-toggle" type="button" aria-pressed="false">Larger text</button>
<button id="answers-toggle" type="button" aria-pressed="false">Show all answers</button>
</div>

## Part 1. Reflection {#reflection}

### Why review an existing result? {#why-reflect}

A first response can look complete while missing a requirement or containing an error. Once a draft exists, the model can inspect it with a more focused question: **what needs to change for this result to satisfy the task?** This gives the next attempt a specific direction.

### Reflection adds review and revision {#workflow-comparison}

**Reflection is a workflow pattern in which an LLM reviews existing work and uses the resulting feedback to revise it.** The work can be an answer, a plan, or code.

::: {.diagram-scroll .comparison-scroll tabindex="0" role="region" aria-label="Comparison of direct generation and reflection; scroll horizontally on small screens"}

![Both workflows begin with the same task. Reflection adds critique and revision before returning the result. Select the figure to enlarge it, or scroll across it on a small screen.](figures/ng/reflection.svg){#fig-reflection-flow fig-alt="Direct generation: Task, Generate, Submit. With reflection: Task, Generate, Critique, Revise, Submit. The additional steps inspect the draft and use the feedback to change it."}

:::

A **critique** identifies a weakness relative to the task and proposes a correction. A **revision** applies that feedback to the existing work. The critique becomes input to the revision.

### How feedback guides the next version {#reflection-workflow}

1. **Review:** Give the model the original task and the draft. Ask it to identify specific problems, explain why they matter, and suggest changes.
2. **Revise:** Supply the task, draft, and feedback so the model can make the corresponding changes. Then check the revised result against the task.

The same model can generate, review, and revise; these steps use additional prompts and require no retraining. Review and revision can also share one model call.

A model can review the draft alone. It can also use **external feedback**—evidence from outside its own judgment, such as a program's error message or rendered output—to guide a correction.

::: {.example-note #reflection-example}
**Brief example — chart revision**

**Task:** Compare each drink's sales in two years.  
**Critique:** “The two years' bars for each drink are far apart. Place them side by side to make the comparison easier.”  
**Revision:** Regroup the same data accordingly and render the chart again.
:::

### When it helps, and when to stop {#reflection-usage}

Use reflection when reviewing a draft can reveal a correctable weakness. It depends on the quality of the feedback: the reviewer may miss an error or suggest a harmful change. Check whether the revision resolves the identified problem while still meeting the original requirements.

Additional calls cost time and tokens. Stop when the requirements are met or a preset iteration limit is reached, and report unresolved issues.

::: {#reflection-conclusion .outcome}
**Reflection uses feedback on existing work to guide the next version.** Its value comes from identifying a problem, making a justified correction, and checking the result. Repetition alone does not guarantee improvement.
:::

::: {.checkpoint}
### Check 1 · What makes this reflection?

A system generates three independent answers to the same request and returns the last one. Has it used reflection? What would it need to add?

<details class="answer">
<summary>Read the answer</summary>

No. It needs to review an existing answer against the task and use that feedback to revise the answer. Making additional attempts alone does not establish this connection.

</details>
:::

## Part 2. Evaluation {#evaluation}

### Why a successful run is not enough {#why-evaluate}

An invoice-processing system must return the **payment due date** as `YYYY/MM/DD`. Consider this fictional case:

| Invoice A contains | System returns |
|---|---|
| Issued: 2026/10/01 · Due: 2026/10/15 | `2026/10/01` |

The system returned a date in the requested format, but selected the issue date. The output can be processed by software and still fail the task. Before relying on this system, we need to know how often it extracts the right field.

**Evaluation assesses an output or a system's performance against explicit criteria.** It produces evidence such as pass/fail judgments, scores, and reasons. Here, “uses the required format” and “gives the correct due date” are different criteria. We must decide what to check before choosing how to check it.

### Use code when the rule can be executed precisely {#code-check}

For each test invoice, a person checks the document and records its correct due date. This is the case's **reference answer**, also called *ground truth*. A collection of test inputs and the information needed to judge their outputs is an **evaluation set**.

Our output contract requires a single date in `YYYY/MM/DD`. With references written in that same format, code can compare the returned string directly:

```python
def date_matches(pred, ref):
    return pred == ref

pred = "2026/10/01"
ref = "2026/10/15"
print(date_matches(pred, ref))
# False
```

The function receives a prediction and its reference, and returns whether they match. Invoice A fails even though its output has a valid date format. Under this contract, equivalent dates written in a different format also fail; the required representation is part of the task.

Apply the same check to four invoices:

| Invoice | Reference due date | System output | Correct? |
|---|---|---|---|
| A | 2026/10/15 | 2026/10/01 | No |
| B | 2026/11/03 | 2026/11/03 | Yes |
| C | 2026/12/01 | 2026/11/20 | No |
| D | 2026/12/20 | 2026/12/20 | Yes |

**Accuracy** is the number of correct cases divided by the number tested: **2/4 = 50%** here. The outputs are constructed examples, and the judgments follow from executing the code; this is not a measured model benchmark. Four cases explain the calculation but do not establish performance on all invoices. To compare two prompts, run both on the same cases using the same criteria.

Code fits this check because the expected value and comparison rule are explicit. Other suitable checks include required fields, valid JSON, and word limits. A format check alone would miss the error in Invoice A.

### Use an LLM judge when the check needs interpretation {#llm-judge}

Now consider a different task: determine whether a summary includes the required information. Exact wording can differ while the meaning stays the same. A string comparison cannot reliably decide whether “shuts for repair work” expresses “closes for repairs.”

An **LLM judge** is a model asked to assess a candidate output against supplied criteria. A **rubric** specifies those criteria and how to assign judgments. For this example, award one point for each required fact accurately expressed in the summary; award zero if it is missing or incorrect.

**Task:** Summarize this fictional library announcement, preserving its three key facts.

> The library building closes on Monday for repairs. Online services remain available. The building reopens on Tuesday.

**Candidate summary**

> The library building shuts on Monday for repair work and opens again on Tuesday.

The judge receives **the task, candidate summary, reference facts, and rubric**, with an instruction such as:

> Score each fact 0 or 1. Accept equivalent wording. Quote the supporting phrase, or explain what is missing or incorrect. Judge what the summary actually says; do not fill its omissions from the reference.

Applying that rubric gives the following **manual illustration**, not a recorded LLM response:

| Required fact | Score | Evidence in the summary |
|---|---|---|
| Building closes Monday for repairs | 1 | “shuts on Monday for repair work” |
| Online services remain available | 0 | Missing |
| Building reopens Tuesday | 1 | “opens again on Tuesday” |

The total is **2/3 facts covered**. Unlike the invoice accuracy, this score counts satisfied items within one output. It measures coverage of these facts, not every aspect of writing quality.

An LLM judge makes a model judgment, so it can be wrong. Compare a sample of its item-level decisions with human judgments and inspect disagreements. Asking for evidence makes those decisions easier to check.

### Two axes: method and reference availability {#two-axes}

An evaluation can be described along two independent axes: **the evaluation method** and **whether each case has a reference answer**. A reference can be a known value or a set of expected facts; it need not be an exact model response.

| Method | Per-case reference available | No per-case reference answer |
|---|---|---|
| Code | Compare an extracted invoice date with its correct date. | Check whether a text stays within a word limit. |
| LLM judge | Check whether a summary covers its required facts. | Judge a chart's readability using a rubric. |

A reference does not automatically make the check suitable for code: interpreting equivalent meanings may require an LLM judge. Having no reference does not mean having no criteria or evidence. A word limit still defines a rule, and a chart judge still needs the actual image and a readability rubric.

Choose the **criterion first**, then the evidence and method needed to judge it. Different criteria for the same output can use different methods—for example, code for a summary's length and an LLM judge for its coverage of required facts.

::: {.checkpoint}
### Check 2 · Choose a method for each requirement

A system writes summaries of at most 40 words. You need to check both the length and whether each summary preserves its source's three key facts. Which method and evidence would you use for each check?

<details class="answer">
<summary>Read the answer</summary>

Use code to count words under an explicit counting rule; it needs the summary and the limit. Use an LLM judge for meaning-based coverage, supplying the summary, source-specific key facts, and scoring rubric. A length pass provides no evidence that the facts are present.

</details>
:::

For regressions, failure traces, and component tests, see the [optional evaluation reading](evaluation-supplement.html).

## Lab preparation: reflection and evaluation in code {#implementation}

The lab builds both parts with a small class from the practice notebook. A `Chat` object stores its own message list: a **system** message fixed when the object is created, then every **user** message it receives and every **assistant** reply it gives. This **conceptual pseudocode** shows reflection with two such objects:

```text
extractor ← Chat(system: "Return the payment due date as YYYY/MM/DD")
reviewer  ← Chat(system: "Check a draft against the task and the invoice")

draft    ← extractor.ask(invoice)
feedback ← reviewer.ask(invoice + draft)
revised  ← extractor.ask("Revise your answer: " + feedback)
```

Each `ask` adds a user message and stores the assistant reply. The reviewer sees the draft only because the draft is written into the reviewer's user message. The extractor can revise "your answer" because its history already holds the invoice and the draft.

Evaluation runs the same system on every case and compares each output with its reference:

```text
correct ← 0
for each (invoice, reference) in the evaluation set:
    extractor ← a new Chat(system as above)
    prediction ← extractor.ask(invoice)
    if prediction equals reference: correct ← correct + 1
accuracy ← correct ÷ number of cases
```

A new object for every case starts each invoice from the same empty history.

::: {.callout-note icon=false}
## Check: one object for every case?

Suppose the loop creates one extractor before the loop and reuses it for all ten invoices. What does the tenth call receive, and why does that matter for the accuracy?

<details class="answer">
<summary>Read the answer</summary>

The tenth call also receives the nine earlier invoices and answers, because the object keeps its history. The cases are no longer independent: an earlier answer can influence a later one, so the accuracy no longer describes the system on a single invoice. Each call also costs more, because the input grows with every case. A new object for each case, or a reset, gives every case the same starting input.

</details>
:::

## Lab: reflection and evaluation on invoices {#lab-guide}

**Goal:** improve an extraction with feedback, then measure whether a change helped.

1. Work through the practice notebook first. It introduces the message kinds, tool calls, the agent loop, and the `Chat` and `Agent` classes used from this chapter on.
2. Give each role its own `Chat` object: an extractor drafts an invoice due date, a reviewer checks it, and the extractor revises. Use a program's error message as feedback, and see feedback change a correct answer.
3. Measure accuracy on ten invoices with code, giving every case a new object, and compare two system messages on the same cases.
4. Grade summaries with a judge object and check it against human labels.

[Practice notebook in Colab](https://colab.research.google.com/github/ralbu85/stml_2026/blob/main/lectures/week05/W5_practice_core_patterns.ipynb) · [Lab notebook in Colab](https://colab.research.google.com/github/ralbu85/stml_2026/blob/main/lectures/week05/W5_lab_reflection_evals.ipynb) · [Homework notebook](W5_hw_chart_reflection.ipynb): reflection on a rendered chart, submitted on the LMS.

## Materials and sources {.unnumbered #sources}

- Practice: [Core code patterns](W5_practice_core_patterns.ipynb) · [Lab notebook](W5_lab_reflection_evals.ipynb) · [Homework notebook](W5_hw_chart_reflection.ipynb).
- Andrew Ng, [Agentic AI](https://www.deeplearning.ai/courses/agentic-ai): Module 2 informs Part 1's reflection pattern and adapted workflow diagram. The brief chart example paraphrases a critique and revision from its Chart Generation lab. Module 4 informs Part 2's evaluation framework. The invoices and library announcement are fictional teaching examples.
- Madaan et al., [Self-Refine](https://arxiv.org/abs/2303.17651): generation, feedback, and revision using one LLM.
- Zheng et al., [Judging LLM-as-a-Judge](https://arxiv.org/abs/2306.05685): capabilities and biases of model judges.

<!-- course-pagination:start -->
<nav class="chapter-pagination" aria-label="Previous and next chapters">
<a href="../week04/notes.html" rel="prev">← Previous: 4 · The Agent Loop and ReAct</a>
<a href="../week06/notes.html" rel="next">Next →: 6 · Multi-Agent Systems</a>
</nav>
<!-- course-pagination:end -->
