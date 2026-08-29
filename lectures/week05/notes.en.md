# Chapter 5. Reflection & Evaluation

This chapter holds two subjects that are two halves of one thing. A finished output can be put to two uses: fed back into the attempt so that the next version is better — reflection — or scored against a fixed standard so that change itself becomes measurable — evaluation. Reflection is a device built into the system; evaluation is the discipline outside it that says whether any device, this one included, actually helped. Each is the other's missing half: reflection's condition of validity is an evaluation signal (5.5), and the claim that reflection helped is itself an evaluation (5.6, 5.7).

The starting point is a gap the loop left open. The loop of Chapter 4 commits its Final Answer and stops. Everything before that point is examined — every Thought reads the preceding observation, every failed call is reinjected and corrected — but the answer itself is examined by nothing: the run ends the moment it is written. The same is true of every method in Chapter 2: CoT, worked examples, and self-consistency all act before or during generation, and none of them reads the answer after it is written. Yet a model that has just committed a wrong answer will often find the error itself when asked to read that answer against the question — nothing in a single generation call, and nothing in the loop's termination turn, asks it to.

The remedy that feeds an output or an attempt back into the model's input to be fixed is reflection: the configuration that refines one output through critique is Self-Refine, and the configuration that injects a summary of a failed attempt's cause into the next attempt is Reflexion. Sections 5.1–5.6 build these; sections 5.7–5.11 build the measurement discipline that every claim about them — and about every later chapter — stands on.

## 5.1 The Problem — Commitment Without Verification

A generation call ends when its answer is written; no step examines the content of that answer. Chapter 2's measurements showed what this costs: on multi-step problems a single pass misses often, and the miss is committed as confidently as a hit. Chapter 4 showed the same shape at the scale of a whole run: the termination turn writes its grounds and stops, and a wrong Final Answer terminates the loop exactly as a right one does.

The model itself can perform the missing examination. Generation and critique are different tasks: generation constructs one answer anew out of the possible ones, while critique compares a finished candidate against criteria. The asymmetry that scoring answers is easier than producing them is the same premise that introduced a verifier (→ 2.6), and on tasks where this asymmetry holds, a model can find defects in its own output.

## 5.2 Generate–Critique–Improve — Self-Refine

**Self-Refine** = a configuration in which the same model alternates the roles of generator, critic, and improver through prompts, refining one output repeatedly (Madaan et al., 2023).

1. **Generate** — output a draft for the task.
2. **Critique** (same model, different prompt) — take the draft as input and generate concrete points of improvement. If the critique judges that nothing needs improving, terminate.
3. **Improve** — take the draft and the critique together as input, generate a revision, and return to the critique step. The iteration has a cap.

> **[Figure 5.1]** The generate–critique–improve cycle of Self-Refine. From one model icon, three prompts (generate, critique, improve) branch out; arrows form a ring from draft → critique (list of improvements) → revision → back to critique. From the critique node, a "nothing to improve" verdict exits the ring toward termination. The structure — one model cycling through roles — and the termination condition must be visible at a glance.

The requirement on the critique prompt is specificity. "Make it better" gives the improve step no information. The prompt must demand what is deficient, against which criterion, and why; in practice, the critique's criteria are stated per dimension (accuracy, constraint compliance, format, and so on). With dimensions stated, the critique becomes a checklist, and the "good enough" verdict (the termination condition) is made per dimension, with grounds.

The critique prompt used in this week's lab is one concrete instance — each requirement above appears as a line the model must obey:

```
You are a strict writing reviewer. Reflect critically on the essay draft
below. Do not rewrite it. Identify each concrete defect in structure,
clarity, strength of argument, or evidence, and for each defect state what
a revision would need to add or change.
```

The first constraint (criticize only, do not rewrite) keeps the roles separate; the dimension list makes the critique a checklist; the last clause forces each point to be actionable by the improve step.

```
[Task]     Summarize the passage in exactly two sentences, mentioning the
           term "chunking".
[Draft]    RAG systems couple a model with a document index so that answers
           can cite current sources.
[Critique] Two defects. (1) Length: the summary is one sentence; the task
           demands exactly two. (2) Required content: the term "chunking"
           does not appear.
[Revision] RAG couples a model with a document index, so answers can cite
           current sources. Retrieval quality depends on chunking, the
           embedding model, and how many passages are injected.
```

The size of the improvement depends on whether the critique step can actually detect defects. It is large where the model can name concrete defects — multi-aspect preference tasks, compliance with stated constraints — and small where error detection itself is hard: in mathematical reasoning a wrong chain reads as plausible, and gains return only when an external signal identifies the error. Per-task improvement margins are covered in the presentation.

## 5.3 Reflection at the Level of Attempts — Reflexion

What Self-Refine fixes is a single output. But failures often occur at the level of a whole attempt — a loop run that ends in a wrong Final Answer, a solution that fails its tests — and what is then needed is not revision of an answer but a retry of the task. The problem is that a bare retry learns nothing: rerunning the same input may happen to take a different path through sampling randomness (→ 2.5), but the information from the previous failure exists nowhere, so the same failure tends to repeat.

**Reflexion** = a configuration that produces a linguistic summary of the failure's cause (a reflection) from the failed attempt's record and injects it, cumulatively, into the next attempt's prompt (Shinn et al., 2023). A **trial** here is one complete run of the unit doing the work — for tool tasks, one run of a Chapter 4 loop from question to Final Answer, whose record is the trace.

1. **Attempt** (actor) — perform the task once and keep the record: the input, the generated output, and what happened when it was checked.
2. **Evaluate** (evaluator) — judge the attempt's success or failure; on success, terminate. The signal comes in three types: rule-based (answer matching, test execution), heuristic (the same action repeating, an attempt running over-long), and model judgment (a separate LLM call scores success). The earlier types are more reliable; the later types apply more broadly.
3. **Reflect** (self-reflection, model) — from the record and the failure signal, summarize what failed, why, and what to do differently in the next attempt.
4. **Retry** — append the reflection summary to the prompt and return to the attempt step. The iteration has a cap. Reflections are themselves context-consuming text, so they are not accumulated without bound; the paper keeps a fixed-size window of the most recent reflections.

> **[Figure 5.2]** The attempt–evaluate–reflect–retry cycle of Reflexion and the accumulation of reflection memos. On the left, three blocks — actor, evaluator, reflection — stacked vertically; from the evaluator, a branch to termination on success and to reflection on failure. The reflection block's output (a linguistic summary) stacks line by line into an episodic-memory box on the right, and an arrow feeds that memory back into the next attempt's prompt. The drawing must show that what is updated is the context, not the weights.

On a code-generation task checked by unit tests, the reflect step's output takes this form.

```
Reflection: The attempt failed test 3 (empty input list). The function
assumes at least one element and reads index [0] unconditionally. In the
next attempt, handle the empty list before any indexing.
```

Why the retry improves without any training is the property from Chapter 2: text placed in the prompt conditions the next generation (in-context learning, → 2.3). The reflection memos accumulating in the prompt change how the next attempt is generated. The paper calls this verbal reinforcement learning, and the name is precise: reinforcement learning corrects a model by updating its weights with the same kind of success/failure signal; Reflexion receives a signal in the same position but moves the target of the update from the weights to the context. The price is persistence: the lesson applies immediately, at no training cost, and disappears with the context.

The paper's measured domains show where the structure applies: multi-step question answering over documents (HotpotQA — answer matching as the signal), sequential decision-making in a text environment (ALFWorld — task success as the signal), and code generation (HumanEval — execution of self-written unit tests as the signal). In the first two, the actor is literally a ReAct agent (→ 4.3): the loop of Chapter 4 is the inner machinery of each trial, and Reflexion wraps it from outside. All three are domains where the evaluation signal is obtained automatically; the improvement numbers are covered in the presentation.

## 5.4 Thought versus Reflection

Both ReAct's Thought (→ 4.3) and this chapter's reflection make the model write about its own work, and the two are easily conflated. One question separates them every time: *when is it written, and what does it read?* A Thought is written during the attempt, before each action, and reads the observation that just arrived. A reflection is written after something is finished — a draft, a whole trial — and reads that finished thing together with its failure signal.

The difference is visible in a single failing run and its retry.

```
Trial 1 — one Chapter 4 loop:
  Thought 1:  I need the paper's publication year first.        ← inside the trial:
  Action 1:   search_papers["Reflexion publication year"]          chooses the next action
  Observation 1: (a chunk about Reflexion's memory design; no year)
  Thought 2:  No year in the result. I will answer from memory. ← inside: a judgment — here a bad one
  Final Answer: 2022                                              (wrong)

Evaluator:   answer does not match the golden year → trial failed.

Reflection — written after the trial, reading its whole record:
  "The query asked for a 'publication year', but corpus chunks rarely
   contain bare years. Next trial: search for the paper's title and venue
   line, and do not answer until a year string appears in an observation."

Trial 2 — the reflection sits in the prompt; the first query is already different.
```

Every Thought above serves the current attempt: it reads one observation and chooses one action. The reflection serves the next attempt: it reads the failed record end to end and turns the failure signal into an instruction. Neither can do the other's job — a Thought cannot know the trial will fail, and a reflection cannot choose the next query mid-run.

| | Thought (ReAct) | Reflection |
|---|---|---|
| written when | during the attempt, before each action | after a draft or a trial is finished |
| reads | the observation just returned | the finished record, plus its failure signal |
| serves | this attempt — choosing the next action | the next version, or the next attempt |
| requires | nothing extra — observations arrive every turn | an evaluation signal (→ 5.5) |

The two therefore stack rather than compete. In the Reflexion paper the actor is itself a ReAct agent: the inner loop acts within the trial, writing Thoughts; the outer loop learns across trials, writing reflections.

Placed next to Chapter 2, the course so far has applied one principle three times. The model's only workspace is text (→ 2.2), so whatever must survive to the next prediction must be written down:

- inside one response — CoT writes the intermediate values of a calculation (→ 2.3);
- inside one attempt — the Thought writes the judgment before each action (→ 4.3);
- between attempts — the reflection writes the lesson of a failure (this chapter).

Three names, one mechanism; what changes is only where the writing sits.

## 5.5 The Condition of Validity — the Source of Feedback

The quality of reflection cannot exceed the quality of the signal the evaluation step receives. The extreme is the case with no external signal at all. If the only basis for judging an attempt is the model's own opinion, there is no information by which the model, rereading an answer it generated as correct, could judge it wrong. Self-correction under this condition either finds no errors or, conversely, "corrects" right answers into wrong ones. Controlled measurements with external signals blocked report that self-correction fails to improve reasoning accuracy or actively lowers it (Huang et al., 2024, *Large Language Models Cannot Self-Correct Reasoning Yet*), and the fact that the success stories of the reflection line are all in domains with automatic evaluation signals (5.3 above) points to the same conclusion.

The condition under which reflection holds, therefore, is the existence of an evaluation signal from outside the attempt: a test passing, an answer matching, an execution error, a rendered result that can be inspected. Given such a signal, reflection converts it into causal analysis; without one, it becomes groundless rewriting. The character of the cost is also fixed: a retry is a multiple of an attempt's cost, so these methods belong to test-time compute (→ 2.6) — accuracy bought with more predictions.

## 5.6 Practical Guide — Adding a Reflection Step

The working rules below are the operational side of 5.1–5.5, adapted from the lecture notes of the source course of this week's lab (Ng, *Agentic AI*, Module 2).

**Which tasks benefit.** Reflection pays where the defect is checkable in the output: the first pass tends to produce it, and a reader armed with the right question can catch it by reading alone. It pays little where no one can state what a defect would look like. The source course's examples:

| Task | Typical first-pass defect | Critique question |
|---|---|---|
| generating an HTML table | a broken tag (missing `>`) | validate the HTML |
| writing step-by-step instructions | a missing step | check coherence and completeness |
| brainstorming product names | unintended meaning, hard to pronounce | negative connotations? hard to pronounce? |

Each row's critique question is answerable from the output itself — that is what qualifies the task.

**Writing the critique prompt.** Two rules: state the reflection action explicitly, and specify the criteria to check. The source course's reflection prompt for improving an e-mail draft:

```
Review the email first draft.
Check that the tone is professional and look for phrases that could be
considered rude or insensitive.
Verify all facts, dates, and promises are accurate.
Then write the next draft of the email.
```

The actions (review, check, verify) and the criteria (tone, rude phrasing, factual accuracy) are both explicit. This prompt folds critique and revision into one call; the lab separates them into two calls, which costs one call and buys the ability to give the two steps different prompts, different context, or different models. Both shapes are in use.

**Choosing the critic.** The default is the same model under a critique prompt. A second option is a different model, which reads the draft without the framing that produced it. In the source course's own reflection lab the two are combined: a general-purpose model writes the draft and a model trained for long verification chains (a reasoning model) critiques it — checking is the part of the work such models are trained on.

**Sourcing feedback beyond the model.** 5.5 fixed the condition — the critique is only as good as its signal. In practice the signal is often a cheap program or a tool from Chapter 3, not a second opinion:

| Failure to catch | Feedback source |
|---|---|
| output mentions a competitor's name | pattern matching against a name list |
| a factual claim in an essay | web search results |
| output exceeds a length limit | a word counter |
| generated code is wrong | executing it against tests |

The rule: use the cheapest source that can actually catch the failure, and where a program can check, let the program's verdict outrank the model's opinion.

**Where the ceiling sits.** With enough prompt polishing every configuration plateaus, and the plateaus are ordered: direct generation lowest, reflection above it, reflection with external feedback highest. Reflection alone saturates once the critique has consumed the defects it can see without new information — the lab's second-round exercise reproduces exactly this — and past that point the gain comes from a better signal, not a better prompt.

**Measuring whether reflection helped.** The claim "V2 is better" is tested, not assumed — a fixed set of inputs, scored with and without the reflection step, re-run on every prompt change. Stating that procedure precisely — what is fixed, what grades, how the failures are read — is no longer a side note of reflection but a subject of its own, and it is the second half of this chapter.

## 5.7 The Second Problem — Judging by Impression

Every improvement so far was claimed with a number. Chapter 2 scored prompts on a fixed problem set; Chapter 3 checked tool calls against expected routes; Chapter 4 scored its loop against a five-question set; and this chapter's first half accepts a revision only when a judge score rises. What follows turns that recurring practice into its own subject: how to know whether a change helped. The question sounds administrative and is not — for systems built on a stochastic model, evaluation is the only substitute for the compiler and the type checker that ordinary software leans on.

The default way people check a prompt change is to run one or two inputs and read the outputs. This check fails for reasons that are structural, not sloppy. The sample is one; a stochastic model passes and fails the same input on different runs (→ 2.5). The reader is the author; an author reads their own change charitably. And the check looks only at the case being fixed, so a change that fixes one input and silently breaks three others reads as a success — the regression is invisible by construction.

**Evaluation** = scoring a system against a fixed dataset with a fixed metric by a fixed procedure, so that two runs produce comparable numbers. The three fixings are the content of the definition: change any of them between runs and the numbers no longer compare.

## 5.8 The Evalset and Code-Graded Metrics

An **evalset** = a fixed list of inputs with expected outcomes (golden answers) against which every version of the system is scored. Design rules follow from its purpose.

1. **Fixed** — the same items every run; an item is changed only deliberately, never per-run.
2. **Covering** — items span the input kinds the system must handle, including the known-hard ones. A set of only easy cases measures nothing (the tricky animal statements of the W2 lab existed for exactly this reason).
3. **Separate** — no evalset item or its answer may appear in the prompt. Worked examples are drawn from a disjoint pool; otherwise the measurement measures leakage, not ability (→ 2.3, the exemplar-separation rule).

A **code-graded metric** = a scoring rule computed by a program from the output alone: exact match against the golden answer, presence of a required term, format validity, a numeric tolerance. Code grading is the most reliable instrument available — deterministic, free, and incapable of charity — and the narrowest: it applies only where correctness is checkable by rule. The measurements of this course stand on it wherever they can (answer keys in Chapter 2, routing checks in Chapter 3, answer matching on the mini evalset in Chapter 4).

## 5.9 LLM-as-a-Judge

Many outputs that matter have no rule-checkable golden answer: a summary's faithfulness, a critique's usefulness, a report's coverage. **LLM-as-a-judge** = using a model call as the grader: the judge receives the input, the output under test, and explicit criteria, and returns a score or verdict per criterion.

The device works because of the same asymmetry as reflection: comparing an output against stated criteria is easier than producing the output (→ 5.1). Its reliability, however, is not free. Two biases are measured in the judge literature (Zheng et al., 2023). **Position bias** — in pairwise comparison the judge favors one position; the paper's remedy is judging both orders and accepting only a verdict that survives the swap (otherwise a tie). This is the instability the reflection guide already warned about in open "which is better" comparisons (→ 5.6). **Verbosity bias** — longer answers score higher at equal quality; as a countermeasure, criteria should name substance, not length. The same work raises a third, **self-enhancement bias** — a judge favoring answers it generated itself — but leaves it unconfirmed for lack of data. The measurements are covered in the presentation.

Two design rules follow. First, criteria are stated per dimension — the judge receives a checklist, not "is this good?" — so that scores decompose into named causes, and binary items beat scales because 1-or-0 forces a verdict a human can audit. The judge used on this week's essays is this rule in concrete form:

```
Score the essay on each criterion. Answer 1 or 0 per line, then one line of JSON.
1. thesis: states a clear position on the question.
2. structure: has a recognizable introduction, body, and conclusion.
3. evidence: supports claims with concrete examples or reasons.
4. counterargument: addresses at least one opposing view.
```

A score of 2/4 under this rubric is not "the judge felt 2-ish"; it names which two properties are absent, and the revision targets them. Second, the judge is itself evaluated: on a sample of items, judge verdicts are compared with human labels, and the judge is trusted only as far as that agreement. A judge that has never been checked against a human is an unread instrument.

## 5.10 Error Analysis

A score says how much fails; it does not say why. **Error analysis** = reading the failed items and grouping them by cause, so that the next change targets the largest group. The procedure is a loop.

1. **Run** the evalset and collect the failures.
2. **Read and label** each failure with its apparent cause — wrong retrieval, format violation, missed constraint, arithmetic slip. Labels are invented from the failures, not fixed in advance.
3. **Count** the labels. The distribution, not intuition, chooses what to fix: the largest group first.
4. **Fix one thing and re-run.** One change per measurement; a run that changes two things cannot attribute its delta (→ the W2 lab's revision discipline).

A worked instance, in the shape the lab produces. Forty items, eleven failures; reading each failure and writing one label per item yields:

| Label (invented while reading) | Count |
|---|---|
| search query too literal — right passage never retrieved | 5 |
| answer correct, required format violated | 3 |
| constraint in the question ignored ("...before 2023") | 2 |
| golden answer itself ambiguous (item defect) | 1 |

The vivid failure in this run was the ignored constraint — it produced a confidently wrong paragraph — but the count says the next change is the query prompt, worth five items, and the format fix is worth three more before the vivid one is worth touching. One item goes back to the evalset for repair, not to the system. The counting step is what separates this procedure from debugging by anecdote: a failure that is vivid but rare loses to a failure that is dull but frequent, and only the count reveals which is which.

> **[Figure 5.3]** The error-analysis loop as a cycle: run → read & label → count → fix one thing → re-run, drawn as a ring with the label-count bar chart at the "count" node feeding the choice at "fix one thing." A dashed shortcut arrow from "run" directly to "fix," bypassing read/count, is struck through and labeled "debugging by anecdote" — the anti-pattern the loop replaces.

## 5.11 Operations — Regression and Growth

The evalset earns its cost when it runs on every change, not once. **Regression testing** = re-scoring the same set after each modification, so that a fix which breaks something else is caught by the score, not by a user. Two operational rules complete the practice. A numeric **target** is fixed before iterating (the labs' "≥ 11/12" lines), because a target chosen after seeing the score will drift to meet it. And the set **grows from failures**: an error found in real use becomes a new item, so coverage tracks the system's actual failure surface rather than its designer's imagination.

What this half measures is components: one prompt, one tool router, one retrieval step. Whole-agent measurement — multi-step tasks, success rates over repeated trials (pass^k), cost-aware comparison — layers on top of it and is treated with benchmarks in Chapter 13.

## 5.12 Summary

The loop commits its answer without verifying it; the remedy feeds the output or the attempt back into the input. Refining one output is Self-Refine (generate–critique–improve); redoing a whole attempt is Reflexion (attempt–evaluate–reflect–retry), whose actor in the source measurements is a Chapter 4 loop. Both operate on the asymmetry that critique is easier than generation. Thought and reflection are different writings — one during the attempt to choose the next action, one after it to improve the next attempt — and with CoT they are one principle at three ranges: what must survive must be written. The condition of validity is external feedback; self-critique without a signal guarantees no improvement.

The claim that any of this helped is settled by the chapter's second half. Impression-based checking fails structurally — sample of one, charitable reader, invisible regressions — so dataset, metric, and procedure are fixed to make numbers comparable. Code grading is the most reliable instrument and the narrowest; the LLM judge extends measurement to unruled outputs at the price of documented biases, and is trusted only as far as its agreement with human labels. Error analysis converts scores into causes by reading and counting failures; regression runs convert the evalset into a standing safety net that grows from real failures. Operationally, the two halves close into one loop: reflect where defects are checkable, ground the critique in the cheapest reliable signal, and prove the gain on a fixed set before keeping it.

The next chapter begins to scale the system itself — from one agent to several — and per-component measurement is what keeps a many-part system debuggable: when the pipeline's score drops, component scores say where.

---

**Presentation.** Two papers this week. Reflexion (Shinn et al., 2023) — the mechanism by which verbal feedback works like learning without weight updates; listen for where the feedback signal comes from and what breaks without it. Judging LLM-as-a-Judge (Zheng et al., 2023) — MT-Bench and Chatbot Arena: how judge agreement with humans is measured, and the position and verbosity biases with their mitigations; listen for when a model is allowed to grade a model. Optional reading: Self-Refine (Madaan et al., 2023) — the generate–critique–improve iteration and per-task margins.

**Lab.** `W5_lab_reflection_evals.ipynb` — the chapter's two halves run as one experiment, adapted from Andrew Ng's *Agentic AI* Modules 2 and 4. First the reflection cycle on an essay task: draft (V1), critique with the prompt of 5.2, revise (V2). Then the claim "V2 beats V1" is put through the second half: the four-criterion binary judge of 5.9 scores both versions over a fixed topic set, error analysis labels and counts the remaining failures, and the critique prompt is iterated against a numeric target with the same set re-scored each round. Reference answers: `labs/checkpoints/week05/solution.py`.

**Homework.** `W5_hw_chart_reflection.ipynb` — the reflection loop where the output is a rendered matplotlib chart and the critique reads the image itself: an external signal in exactly the sense of 5.5, produced by the code-execution convention of 3.7. Due before W6.
