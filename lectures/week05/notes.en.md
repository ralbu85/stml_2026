---
title: "Chapter 5. Reflection & Evaluation"
subtitle: "Correct a result with feedback · Measure a system on fixed cases"
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

::: {.callout-note appearance="minimal"}
## Learning objectives

- Name the three steps of reflection (draft, critique, revision) and the input of each step.
- Explain why a query can run without an error and still give a wrong answer. Name the feedback that finds this error.
- Measure the accuracy of a system on an evaluation set with a code check.
- Compare two versions of a system on the same cases, and find the causes of the failed cases.
- Use an LLM judge with a rubric. Compare its scores with human labels before you use it.
:::

## Part 1. Reflection {#reflection}

### Draft, critique, revision {#reflection-def}

In Chapter 4, the agent loop stopped when the model wrote a final answer. No step examined that answer. A first answer can look correct and still contain an error. Reflection adds a step that examines the answer before the system returns it.

::: {.callout-tip icon=false}
## Reflection

A workflow in which an LLM examines a result, writes feedback about it, and then uses that feedback to change the result. The result can be an answer, a query, a plan, or code.
:::

::: {.diagram-scroll .comparison-scroll tabindex="0" role="region" aria-label="Comparison of direct generation and reflection; scroll horizontally on small screens"}

![Both workflows start with the same task. Reflection adds a critique and a revision before the system submits the result. Select the figure to make it larger. On a small screen, scroll across it.](figures/ng/reflection.svg){#fig-reflection-flow fig-alt="Direct generation: Task, Generate, Submit. With reflection: Task, Generate, Critique, Revise, Submit."}

:::

Reflection has three steps:

1. **Draft.** The model does the task and gives a first result.
2. **Critique.** A model examines the draft against the task. It lists each problem that it finds, or it writes that there is no problem. This text is the **critique**.
3. **Revision.** The model that wrote the draft receives the critique. It changes the draft to correct the problems.

The same model can do all three steps. Each step is a different prompt, and no step changes the model. In this chapter, two `Agent` objects do the work. The **writer** makes the draft and the revision. The **reviewer** writes the critique.

**Feedback** is information about a result that the next step uses. A critique is feedback that a model writes. **External feedback** comes from outside the model. Examples are the rows that a query returns and an error message from a program.

### Example: a query that runs but gives a wrong answer {#sql-example}

The example uses the Week 4 shop database. It has four tables: customers, products, orders, and order items. Each order has the status `completed` or `cancelled`. The data is from January to March 2025.

The question is:

> Which product's units sold in completed orders fell the most from February 2025 to March 2025? Return the product name and the drop.

A person wrote a reference query. Its result is `[('Keyboard', 46)]`. The program uses this result only to measure the answer. The model never receives it.

The outputs below come from one recorded run of the lab with `gpt-4.1` at temperature 0. Your run can give a different draft.

#### Step 1. The writer drafts a query

The writer's system message asks for one SQL query in JSON and lists the tables. The user message is the question. The draft makes one subquery for February and one for March. Then it joins the two subqueries:

```sql
... ) feb
JOIN ( ... ) mar ON feb.product_id = mar.product_id
JOIN products p ON p.product_id = feb.product_id
ORDER BY drop_in_units DESC
LIMIT 1;
```

The program runs the draft. The result is `[('Notebook', 17)]`. The query ran without an error, and the row has the correct form. The row alone does not show a problem.

The data shows the problem. The table gives the units sold in completed orders for four of the twelve products:

| Product | February | March | Drop |
|---|---|---|---|
| Keyboard | 46 | no sales | 46 |
| Headphones | 30 | no sales | 30 |
| Mouse | 26 | no sales | 26 |
| Notebook | 37 | 20 | 17 |

The March subquery has no row for Keyboard, Headphones, or Mouse. `JOIN` keeps only the products that have a row in both subqueries. Because of this, the draft removed the three products with the largest drops.

Other runs give a different form of the same error. The draft uses `LEFT JOIN`, but it does not replace an empty March total with 0. February units minus an empty value (`NULL`) is `NULL`. SQLite puts `NULL` values last in a `DESC` sort, so the result is the same wrong row.

#### Step 2. The reviewer writes a critique

The reviewer is a second `Agent` object. Its system message starts with these lines, and the table list follows them:

```text
You review a SQL query. You receive the question, the query, and the rows it returned.
You can run your own queries with run_sql to check the data.
Check that the query answers exactly the question and that the result matches the data.
List each problem, or reply exactly: No problems.
```

The user message contains the question, the draft query, and its rows. The reviewer receives the rows only because the program writes them into this message. The rows are external feedback. They show what the query did. The query text alone does not show this.

The recorded critique listed three problems. Its last line was:

> Summary: The query does not account for products that had sales in February but none in March, so it may miss the true largest drop.

The reviewer had the tool `run_sql`, but it did not use the tool in this run. The query and the row were enough for this critique.

#### Step 3. The writer revises the query

The program sends the critique to the writer as a new user message: `"A reviewer wrote:\n" + feedback + "\nRevise the query if needed."` The program does not send the question or the draft again. The writer's message list already contains them:

| # | Role | Content |
|---|---|---|
| 0 | system | Write one SQL query as JSON; the table list |
| 1 | user | The question |
| 2 | assistant | The draft (`JOIN` of `feb` and `mar`) |
| 3 | user | "A reviewer wrote: … Revise the query if needed." |
| 4 | assistant | The revised query |

The revised query starts from all products. It gives the value 0 to a month with no sales:

```sql
SELECT p.name, (COALESCE(feb.units_sold,0) - COALESCE(mar.units_sold,0)) AS drop_in_units
FROM products p
LEFT JOIN feb ON p.product_id = feb.product_id
LEFT JOIN mar ON p.product_id = mar.product_id
...
```

The program runs the revised query. The result is `[('Keyboard', 46)]`. This result is equal to the reference.

The critique was useful because it named the cause of the error. The query removed the products with no March sales, and the writer could correct this. The rows let the reviewer compare the result with the question.

### External feedback: an error message {#error-feedback}

A program can also give feedback. For this feedback, a reviewer model is not necessary. The second lab question is: *What was the median value of a completed order in January 2025?* The reference answer is 60.0.

The writer's system message does not name the database program. The recorded draft used the function `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total_value)`. SQLite does not have this function. The database returned this error:

```text
error: near "(": syntax error
```

The program sent the error to the writer as the next user message: `"The database returned: " + rows + "\nFix the query."` Here, `rows` contains the error text. The writer then gave each order total a number with `ROW_NUMBER()` and took the average of the middle value or values. The new query ran and returned `[(60.0,)]`. This answer is correct.

The loop has two stop conditions: the query runs, or three rounds are complete. In the recorded run, one round was enough.

An error message and a critique find different problems:

| Feedback | Source | It can find | It cannot find |
|---|---|---|---|
| Error message | The database | A query that does not run | A query that runs and gives a wrong answer |
| Critique with the rows | The reviewer model | A logic error in a query that runs, such as the removed products | An error that the reviewer does not see |

The Notebook query ran without an error. For this reason, no error message could show its problem. Only an examination of the logic, with the rows, found it.

### Limits and stop conditions {#reflection-limits}

Reflection does not make a result correct automatically. The result of a revision depends on the critique.

- **The reviewer can miss an error.** In one recorded run of the lab exercise, the draft had the `NULL` form of the error. The reviewer replied `No problems.` The writer changed the query anyway, and the new result was correct. The final result was correct, but the critique was wrong. Examine the critique, not only the final result.
- **The reviewer can report a problem that does not exist.** Then the revision can change a correct result into a wrong one. Give the reviewer the evidence that it needs, such as the rows and the task. Tell it to reply `No problems.` if it finds no problem.
- **Each round adds model calls and tokens.** A critique and a revision add up to two calls to each case. In Part 2, reflection increased the calls for ten invoices from 10 to 22.

Stop the loop when one of these conditions occurs:

1. The reviewer replies `No problems.`
2. An external check passes. For example, the query runs.
3. The loop gets to a set number of rounds.

If the loop stops at the limit, report the problems that remain.

::: {.checkpoint}
### Check 1 · Which feedback finds the error?

A writer drafts two queries. Query A uses a function that SQLite does not have. Query B runs and returns `[('Notebook', 17)]`, but the correct answer is `[('Keyboard', 46)]`. Which feedback can find each problem?

<details class="answer">
<summary>Read the answer</summary>

Query A: the database error message. The query does not run, so the database tells the writer. A reviewer model is not necessary.

Query B: a critique that uses the question, the query, and the rows. The query runs without an error, so the database gives no feedback. The reviewer must compare the result with the question and the data.

</details>
:::

## Part 2. Evaluation {#evaluation}

### Why one correct run is not enough {#why-evaluate}

In Part 1, one question gave one correct result. That result does not show how frequently the system is correct on other questions. Evaluation measures this.

::: {.callout-tip icon=false}
## Evaluation

A measurement of the outputs of a system against written criteria on a fixed set of cases. It gives pass or fail results, scores, and the reasons for them.
:::

Evaluation uses four more terms:

- **Criterion:** a written rule that an output must obey. Example: "The output is the payment due date, in the form `YYYY/MM/DD`."
- **Evaluation set:** the cases on which you measure the system. Each case has an input and the information that is necessary to judge the output.
- **Reference answer** (also *ground truth*): the correct output for one case. A person finds it. The model never receives it.
- **Accuracy:** the number of correct cases divided by the number of cases.

### Example: due dates on ten invoices {#invoice-set}

The task is: return the **payment due date** of an invoice as `YYYY/MM/DD`. The lab evaluation set has ten fictional invoices, A to J. Some invoices give the due date directly. Other invoices give a rule, and the model must calculate the date. The table gives four invoices in a short form:

| Invoice | Invoice text (short form) | Reference |
|---|---|---|
| A | Issued: 2026/10/01. Due: 2026/10/15. | 2026/10/15 |
| G | Issued 2026/10/15. Net 30 days. If the due date is a Saturday or Sunday, pay on the next Monday. | 2026/11/16 |
| I | Delivered 2026/12/22. Due 10 business days after delivery. Holidays: 2026/12/25 and 2027/01/01. | 2027/01/07 |
| J | Issued 2026/09/14. Due on the first Friday at least 60 days after the issue date. | 2026/11/13 |

Invoice A has two dates. The output `2026/10/01` has the correct form, but it is the issue date. For this reason, a check of the form alone is not enough.

### A code check {#code-check}

The criterion is an exact match with the reference text. Code can apply this rule:

```python
def date_matches(pred, ref):
    return pred == ref

print(date_matches("2026/10/01", "2026/10/15"))   # the issue date, not the due date
# False
```

The function receives a prediction and a reference. It returns `True` only if the two texts are the same. A correct date in a different form, such as `2026-10-15`, also fails. The output form is part of the task.

Use code when the rule is exact. Other examples are a necessary field in the output, valid JSON, and a word limit.

### Compare two versions on the same cases {#compare}

To compare two system messages, use the same cases and the same check. Change only the system message. Give each case a new `Agent` object. Then no case receives the messages of an earlier case.

The lab compares three versions. These are the recorded results with `gpt-4.1` at temperature 0:

| Version | System message | Correct | Model calls |
|---|---|---|---|
| 1 | `You answer questions about invoices.` | 0/10 | 10 |
| 2 | `Return the payment due date of the invoice you receive as YYYY/MM/DD. Return only the date.` | 9/10 | 10 |
| 3 | Version 2, then a reviewer and a revision | 10/10 | 22 |

Version 3 adds reflection. A reviewer examines each draft. If the reviewer replies `No problems.`, the draft is the final answer. If not, the model revises the draft. The reviewer found problems in two drafts, so the total was 20 + 2 = 22 calls.

Ten cases show how the measurement works. They do not measure the system on all invoices. A difference of one case in ten can come from the variation between runs.

### Find the causes of the failed cases {#error-analysis}

An accuracy value does not show the cause of a failure. Read each failed output.

**Version 1 (0/10).** Nine of the ten outputs had the correct date, but not in the necessary form. Three examples:

| Invoice | Output (part) | Problem |
|---|---|---|
| A | `The invoice is due on 2026/10/15.` | A sentence, not only the date |
| B | `So, the invoice is due on **3 December 2026**.` | A different date form |
| C | `This invoice is due on **2026-12-04**.` | Hyphens, not slashes |

Only invoice I had a wrong date: `2027/01/08`. The model made an error when it counted the business days. The 0/10 is correct for this criterion, but the cause is the output form, not the date. The correction is an output rule in the system message.

**Version 2 (9/10).** The output rule corrected the form. Invoice J failed with `2026/11/20`. The issue date plus 60 days is 2026/11/13, and that day is a Friday. The rule says "at least 60 days", so 2026/11/13 is the due date. The model selected the next Friday.

In version 1, the model wrote its calculation step by step and gave 2026/11/13 for J. Version 2 tells the model to return only the date, so the model writes no calculation. This can be the cause. Ten cases cannot show that it is the cause.

**Version 3 (10/10).** The reviewer's system message contains this instruction: `If the date must be computed from the terms, recompute it step by step.` The reviewer found the error in J, and the revision gave 2026/11/13.

In the version 3 run, the draft for invoice I was `2027/01/08`. In the version 2 run, the same system message gave `2027/01/07` for the same invoice. The reviewer also found this error. The input, the system message, and the temperature were the same, but the answers were different. For this reason, one run of ten cases is a small sample.

### An LLM judge for criteria that need interpretation {#llm-judge}

Some criteria have no exact rule. Example task: summarize this fictional announcement and keep its three facts.

> The library building closes on Monday for repairs. Online services remain available. The building reopens on Tuesday.

A summary can say "shuts for repair work" and not "closes for repairs". The meaning is the same, but an exact text comparison gives `False`. For this criterion, use an LLM judge.

- **LLM judge:** a model that examines an output against written criteria and gives a score.
- **Rubric:** the criteria and the rules for the score that the judge uses.

The lab rubric gives one point for each fact that the summary states correctly. The judge is an `Agent` object, and the rubric is its system message:

```text
You grade summaries of an announcement against required facts.
Score each fact 0 or 1. Accept equivalent wording. Quote the supporting phrase, or explain what is missing
or incorrect. Judge what the summary actually says; do not fill its omissions from the facts.
Return JSON: {"scores": [{"fact": 1, "score": 0 or 1, "evidence": "..."}, ...]}
```

The user message contains the announcement, the three facts, and this summary:

> The library building shuts on Monday for repair work and opens again on Tuesday.

The recorded judge reply was:

```json
{
  "scores": [
    {"fact": 1, "score": 1, "evidence": "The library building shuts on Monday for repair work"},
    {"fact": 2, "score": 0, "evidence": "No mention of online services remaining available"},
    {"fact": 3, "score": 1, "evidence": "opens again on Tuesday"}
  ]
}
```

Code reads the JSON and adds the scores. The result is 2 of 3 facts. This score counts the facts in one output. It is not an accuracy over a set of cases. It measures only the three facts, not all qualities of the summary.

The rubric asks for evidence. With the evidence, a person can quickly find the reason for each score.

### Compare the judge with human labels {#judge-validation}

An LLM judge is a model, so it can make errors. Before you use a judge, compare its scores with the scores of a person on some cases. A **human label** is the score that a person gives to one fact in one summary.

The lab uses five summaries with three facts each, so there are 15 decisions. Each summary gets a new judge object. In the recorded run, the judge agreed with the person on 15 of 15 decisions. One summary was a difficult case:

> The library, including its online services, closes on Monday for repairs and reopens on Tuesday.

This summary says that the online services close. That is incorrect, so the person gave fact 2 a score of 0. The judge also gave 0.

Agreement on 15 decisions does not prove that the judge is correct on all summaries. If the judge and the person do not agree, read the evidence of the judge. Find the cause: an unclear rubric, or an error of the judge. Correct the rubric, and then compare again.

### Choose a method for each criterion {#two-axes}

Write the criterion first. Then select the method. Two questions help you select:

1. Can code apply the rule exactly? If yes, use code. If the rule needs an interpretation of meaning, use an LLM judge.
2. Does each case have a reference answer? A reference can be a value or a list of facts.

| Method | Each case has a reference | No reference for each case |
|---|---|---|
| Code | Compare an extracted due date with the reference date. | Count the words of a summary (limit: 20 words). |
| LLM judge | Score a summary against its three facts. | Score how easy a chart is to read, with a rubric. |

One output can have criteria of both types. In the lab, code counts the words of the five summaries. All five have 20 words or fewer. One of them says that the building reopens on Wednesday. It passes the word limit, but it fails fact 3. A pass on the word limit gives no information about the facts.

::: {.checkpoint}
### Check 2 · Choose a method for each criterion

A system writes summaries of at most 40 words. Each summary must keep three facts from its source. Which method do you use for each criterion? What does each method receive?

<details class="answer">
<summary>Read the answer</summary>

Length: code. It receives the summary and the limit, and it counts the words.

Facts: an LLM judge. It receives the source, the three facts, the summary, and the rubric. Before you use the judge, compare its scores with human labels on some summaries.

A pass on the length does not show that the facts are in the summary.

</details>
:::

For regressions, traces, and component tests, read the [optional evaluation supplement](evaluation-supplement.html).

## Chapter summary {#recap}

| Term | Meaning | Example in this chapter |
|---|---|---|
| Reflection | Draft, critique, and revision of one result | `('Notebook', 17)` → critique → `('Keyboard', 46)` |
| External feedback | Evidence from outside the model | The rows of a query; `near "(": syntax error` |
| Evaluation set | Fixed cases with reference answers | Ten invoices, A to J |
| Accuracy | Correct cases ÷ all cases | 0/10, 9/10, and 10/10 for three versions |
| Failure analysis | Read each failed output and find its cause | Version 1: correct dates in the wrong form |
| LLM judge | A model that gives scores with a rubric | Library summary: 2 of 3 facts |
| Judge validation | Compare the judge with human labels | 15 of 15 decisions agreed |

## Lab preparation: reflection and evaluation in code {#implementation}

The lab uses the `Agent` class from the practice notebook. An `Agent` object has its own message list. The list starts with one **system** message. Each call to `ask` adds a **user** message and the **assistant** reply of the model. This pseudocode shows reflection with two objects:

```text
writer   ← Agent(system: "Write one SQL query for the question" + the table list)
reviewer ← Agent(system: "Check a query and the rows it returned against the question")

query    ← writer.ask(question)
rows     ← run the query on the database
feedback ← reviewer.ask(question + query + rows)
revised  ← writer.ask("A reviewer wrote: " + feedback + " Revise the query if needed.")
```

The reviewer receives the rows only because the program adds them to its user message. The writer can revise "the query" because its message list already contains the question and the draft.

An evaluation runs the same system on each case and compares each output with its reference:

```text
correct ← 0
for each (invoice, reference) in the evaluation set:
    extractor  ← a new Agent(system: "Return the payment due date as YYYY/MM/DD")
    prediction ← extractor.ask(invoice)
    if prediction equals reference: correct ← correct + 1
accuracy ← correct ÷ number of cases
```

A new object for each case gives each invoice the same empty history.

::: {.checkpoint}
### Check 3 · One object for all cases?

A program makes one extractor before the loop and uses it for all ten invoices. What does the tenth call receive? Why is this a problem for the accuracy?

<details class="answer">
<summary>Read the answer</summary>

The tenth call also receives the nine earlier invoices and answers, because the object keeps its history. The cases are not independent: an earlier answer can change a later answer. The accuracy then does not measure the system on one invoice. Each call also costs more, because the input becomes longer with each case. A new object for each case gives each case the same start.

</details>
:::

## Lab: reflection on SQL queries, evaluation on invoices {#lab-guide}

**Goal:** correct a SQL query with feedback from its result. Then measure if a change makes the system better.

1. Do the practice notebook first. It shows the message kinds, tool calls, the agent loop, and the `Agent` class.
2. Part 1: make a writer and a reviewer on the Week 4 shop database. Draft, run, critique, and revise a query.
3. Part 1: use the error message of the database as feedback.
4. Part 2: measure the accuracy on ten invoices with code. Compare two system messages and reflection on the same cases.
5. Part 3: give scores to summaries with a judge object. Compare the judge with human labels.

[Practice notebook in Colab](https://colab.research.google.com/github/ralbu85/stml_2026/blob/main/lectures/week05/W5_practice_core_patterns.ipynb) · [Lab notebook in Colab](https://colab.research.google.com/github/ralbu85/stml_2026/blob/main/lectures/week05/W5_lab_reflection_evals.ipynb) · [Homework notebook in Colab](https://colab.research.google.com/github/ralbu85/stml_2026/blob/main/lectures/week05/W5_hw_chart_reflection.ipynb): reflection on a rendered chart. Submit the homework on the LMS.

## Materials and sources {.unnumbered #sources}

- Practice: [Core code patterns in Colab](https://colab.research.google.com/github/ralbu85/stml_2026/blob/main/lectures/week05/W5_practice_core_patterns.ipynb) · [Lab notebook in Colab](https://colab.research.google.com/github/ralbu85/stml_2026/blob/main/lectures/week05/W5_lab_reflection_evals.ipynb) · [Homework notebook in Colab](https://colab.research.google.com/github/ralbu85/stml_2026/blob/main/lectures/week05/W5_hw_chart_reflection.ipynb).
- Recorded outputs: the model outputs in this chapter come from one run of the lab notebook with `gpt-4.1` at temperature 0 (2026-09-29). The shop database is the fictional Week 4 data. The invoices and the library announcement are fictional examples for this course.
- Andrew Ng, [Agentic AI](https://www.deeplearning.ai/courses/agentic-ai): Module 2 is the source of the reflection pattern and the adapted workflow diagram. Module 4 is the source of the evaluation framework.
- Madaan et al., [Self-Refine](https://arxiv.org/abs/2303.17651): generation, feedback, and revision with one LLM.
- Zheng et al., [Judging LLM-as-a-Judge](https://arxiv.org/abs/2306.05685): the capabilities and biases of model judges.

<!-- course-pagination:start -->
<nav class="chapter-pagination" aria-label="Previous and next chapters">
<a href="../week04/notes.html" rel="prev">← Previous: 4 · The Agent Loop and ReAct</a>
<a href="../week06/notes.html" rel="next">Next →: 6 · Multi-Agent Systems</a>
</nav>
<!-- course-pagination:end -->
