# Chapter 4. The Agent Loop (ReAct)

Chapter 3 ended on an admission: the email assistant completed multi-step work because tool-call round trips repeated, with the model choosing each call and the stopping point — and the loop that carried this repetition belonged to the lab's client library, not to us. A borrowed loop runs, but it cannot be shaped. Its record shows calls and results, never the judgment between them; its termination rule is fixed inside the library; when it ends in a wrong answer, there is nothing to read that says where the run went wrong.

There is also a class of tasks that makes the loop unavoidable rather than convenient. Bug fixing is one. Until the tests run, there is no way to know what is broken; only after the failing point is confirmed does the next edit become determined; and whether that edit passes can only be confirmed by running again. What to do next depends each time on the immediately preceding result, so no fixed sequence of round trips, written in advance, can cover the task. The decisions of how many times, in what order, and when to stop belong to the party that can read the results — the model.

This chapter therefore builds the loop by hand: its anatomy as a procedure (4.1), the measured failure of the obvious protocol (4.2), the convention that fixes it — ReAct (4.3) — its limits (4.4), why today's tool-calling models run it without being told (4.5), and how to read a finished run when it fails (4.6).

## 4.1 The Agent Loop

The **agent loop** = the iterative structure of tool-call round trips in which the next action and the termination are decided by the model's output. Where Chapter 3's procedure treated one round trip at a time, the loop parses every model output into a branch: another call request, or a final answer that ends the run.

Marking an output as final follows one of two conventions, and both are in use. Under **function calling**, a response that contains no tool call is the final answer — this implicit convention is what Chapter 3's client used, and why its loop could remain invisible. Under a **text protocol**, the model marks the answer explicitly with a designated form (Final Answer), and the code detects that form. This chapter's lab uses the explicit form, because the point here is to own every branch; the two conventions carry the same information.

The procedure is as follows. The input is the user question and a system prompt listing each tool's name, function, and input format, together with the output format to follow when calling. The state is the conversation record (initialized with the input) and the iteration count (initialized to 0). If the model never produces a final answer, the iteration does not end on its own, so an upper bound on iterations, **max_steps**, is fixed in advance and checked in the Call step — the same bound the client library exposed as `max_turns`, now ours to enforce and report. The only exit paths are the answer return in the Judge step and the bound being reached in the Call step.

1. **Call** (code) — Increment the iteration count by 1. If it exceeds max_steps, return an answer that states the failure explicitly and terminate. Otherwise, call the model with the entire conversation record as input and receive its output.
2. **Judge** (code) — Parse the output into three branches.
   - Termination: if it is in Final Answer format, return that answer and terminate.
   - Execution request: if it is in tool-call format, pass it to the Execute step.
   - Format error: if it is in neither format, construct a result string stating what is wrong and pass it to the Reinject step.
3. **Execute** (code) — Call the requested tool function and obtain a result string. An unregistered tool or an exception during execution does not abort the procedure; it, too, becomes a result string stating what went wrong (→ 3.5).
4. **Reinject** (code) — Append the model output and the result string to the conversation record and return to the Call step.

On the bug-fixing task, this procedure runs as follows. The model requests a test run; when the failure log is reinjected, the model reads the failing point in the log and requests an edit to the corresponding file. When the edit result is reinjected, it requests the test run again, and only after the passing log is reinjected does it finalize completion with a Final Answer. Which iteration the loop ends on is determined by the test results and is written nowhere in the code.

By Chapter 1's definition — a system whose control flow is decided by the LLM's output — the email assistant of 3.6 already qualified as an agent; what this procedure changes is ownership, not status. The loop is now our code, and with it three things become ours: the protocol, meaning what the model must write on each turn (4.2–4.3); the bound, meaning when the loop stops and how failure is reported (above, and the guards of 4.6); and the record, meaning what to read when a run goes wrong (4.6). The rest of the chapter takes these up in turn.

> **[Figure 4.1]** A cycle diagram connecting the four steps Call → Judge → Execute → Reinject. The Judge step branches three ways: Termination (Final Answer) exits the loop; an execution request passes through Execute and Reinject back to Call; a format error skips Execute and goes to Reinject. The Call step carries a separate failure-exit arrow for reaching the bound. Each step is annotated with its owner (code/model), and a dotted outline contrasts Chapter 3's single round trip as one revolution of this cycle.

## 4.2 The Failure of Act-Only

The first question of ownership is the protocol: what must the model write on each turn? The round-trip convention of Chapter 3 demanded only the call-request JSON or the final answer; nothing asked the model to write judgments or reasons. Putting that convention unchanged into the loop, one turn's record consists of two elements: the action (Action) the model outputs and the observation (Observation) the system fills in with the execution result. This configuration is called **Act-only**, and the ReAct paper measured it as a contrast condition (Yao et al., 2022). One of the questions used in the measurement reads: "Aside from the Apple Remote, what other device can control the program Apple Remote was originally designed to interact with?" Answering requires first searching to find out what the Apple Remote controls, then searching that program again to find the other devices that control it. The following is the Act-only trace on this question (Figure 1 of the paper). Following the paper's experimental environment, an action is written as tool[input], and termination is likewise an action of the form finish[answer].

> Action 1: search[Apple Remote] → Observation: … designed to control the Front Row media center …
> Action 2: search[Front Row] → Observation: could not find. Similar: [Front Row (software), …]
> Action 3: search[Front Row (software)] → Observation: discontinued media center software …
> Action 4: finish[yes] (wrong)

The searches were performed in the correct order. Yet at the end, the model finalized an answer ("yes") whose form is unrelated to the question.

The basis of the diagnosis is the model's computational structure. The model has no workspace outside text, and what is not written in text does not exist for the next prediction (→ 2.2). In the record above, what is written is only the sequence of actions and observations. Under this condition, the three correct query choices and the collapsed termination come apart. The cue for the next query lies on the surface of the immediately preceding observation: the name Front Row appears in Observation 1 and the alternative title Front Row (software) in Observation 2, so reading only the preceding observation yields the next action. The termination judgment has no such cue. It must integrate what the question demanded, what has been confirmed so far, and whether that suffices for an answer — and none of those judgments is written in any observation. At the moment of termination, the model must reconstruct the state of the task from the bare sequence, and when that reconstruction fails, an answer unrelated to the question, like "yes," comes out. The structure is the same as a calculation collapsing when intermediate values are not written down; here, task execution collapses when intermediate judgments are not written down.

## 4.3 ReAct

To remove the failure of 4.2, the model is made to write its judgment before every action. The two Act-only elements, action and observation, remain; reasoning (Thought) is added.

**ReAct** = a prompt convention that structures each iteration as a bundle of Thought, Action, and Observation (Yao et al., 2022). The loop procedure of 4.1 is unchanged, and the three elements correspond to its steps: Action is the call request that the Judge step passes to Execute, and Observation is the result string that the Execute step constructs and reinjects. Both already existed in Act-only. Only Thought is new, added to the model's output as a record of judgment. What the convention specifies is the format of what the model outputs on each turn.

The principle of the convention is that reasoning and action support each other. In one direction, a Thought writes down the facts confirmed in the preceding Observation and the task remaining before an answer, and the next Action is decided on top of that text. In the other direction, the Observation an Action brings back supports the premises of the next Thought with externally confirmed fact rather than the model's internal knowledge. Making reasoning's premises rest on confirmed fact is called **grounding**.

Specified precisely, the model's output on every turn must be one of two formats.

1. **Action turn** — Output one Thought paragraph (facts confirmed, task remaining, reason for this action) and one Action line (tool-call JSON), then stop generating.
2. **Termination turn** — Output one Thought paragraph (grounds for the answer) and one Final Answer line.

The Observation is not written by the model. The Execute step attaches the result string as the Observation and reinjects it. If the model were allowed to generate an Observation following its Action, an unexecuted result — an unconfirmed fact — would enter the record and become a premise of later reasoning. The full system prompt used in the lab is an implementation of this specification.

```
You are an agent that thinks and acts step by step. On every turn, answer in exactly one of the two formats below.

When a tool is needed:
Thought: <your reasoning so far>
Action: {"tool": "<tool name>", "input": "<input>"}

When finalizing the answer:
Thought: <final reasoning>
Final Answer: <answer>

Observation: is filled in by the system — never write it yourself. Write nothing after Action.
```

The following is the measured ReAct trace on the same question (Yao et al., 2022, Figure 1). The notation is the paper's, as in the 4.2 trace: search[…] corresponds to the Action JSON of the prompt above, and finish[…] to the Final Answer.

> Thought 1: I need to search Apple Remote and find the program it was originally designed to control.
> Action 1: search[Apple Remote]
> Observation 1: The Apple Remote is a remote control introduced by Apple in October 2005 … designed to control the Front Row media center program …
>
> Thought 2: Apple Remote was designed to control Front Row. I need to search Front Row next and find the other devices that control it.
> Action 2: search[Front Row]
> Observation 2: Could not find [Front Row]. Similar: ['Front Row Seat to Earth', 'Front Row Motorsports', 'Front Row (software)', …]
>
> Thought 3: Front Row is not found. I need to search Front Row (software).
> Action 3: search[Front Row (software)]
> Observation 3: Front Row is a discontinued media center software … controlled by an Apple Remote or the keyboard function keys …
>
> Thought 4: Front Row (software) is controlled by an Apple Remote or the keyboard function keys. So the answer is keyboard function keys.
> Action 4: finish[keyboard function keys] (correct)

The difference from Act-only is the Thought before each action, and this resolves the diagnosis of 4.2. Thought 2 wrote down the fact confirmed from the observation ("designed to control Front Row") and the remaining task ("the other devices that control it"), and the second query was decided on top of that text. Thought 4 restated the confirmed facts immediately before termination, and as a result the termination became a conclusion from fact rather than a formulaic answer like Act-only's "yes."

This trace also resolves the failure of CoT. CoT, which makes the model write out its solution, fabricated the premise "Apple TV" from internal knowledge on this same question (→ 2.4). Here the premise in the same position came from a search result — Observation 1. Failed actions contribute in the same way: the "could not find" of Observation 2 led to the query correction of Thought 3. This is why failures are designed to be reinjected as result strings rather than raised as exceptions (→ 3.5).

ReAct predates function calling, and the two are the same skeleton in different notation. The Action line and the Final Answer marker are the Judge step's two branches carried in plain text; function calling carries the same two branches in structured fields (`tool_calls` present, or absent). What ReAct adds beyond notation is the content requirement — a written judgment before every action — and that requirement is what the measurement above shows to matter.

> **[Figure 4.2]** A side-by-side contrast of the two traces on the same question. On the left, Act-only alternates only actions and observations and ends in an unrelated answer ("yes"); on the right, ReAct inserts one Thought line before each action, leaving the facts obtained from observations and the remaining task in text. Only the inserted Thought lines are marked in an accent color, and the two termination points are labeled wrong/correct.

## 4.4 Limits

ReAct is not uniformly superior. In the same paper's measurements, on question types answerable from internal knowledge alone, CoT beats ReAct: for that type, search results act as noise instead. The paper reports the best results from a configuration that combines the two methods and selects by question. Per-task outcomes and figures are examined in the presentation.

The structural limits that remain in the agent loop are treated in turn in later chapters. It commits its Final Answer without verifying it — every Thought looks forward to the next action, and nothing reads the finished answer (→ Ch. 5, reflection; how that reading differs from the Thought is drawn precisely in 5.4). The loop picks one action per turn and only moves forward; it cannot compare multiple paths or backtrack (→ Ch. 7, planning and search). Knowledge is locked in the model's parameters, so every knowledge question depends on search (→ Ch. 8, retrieval augmentation). As iterations lengthen, observations accumulate and the input grows (→ Ch. 9, context).

## 4.5 The Protocol, Internalized

A fair question at this point: the loop of Chapter 3's lab ran without any ReAct prompt — no Thought was demanded, yet the email assistant chose sensible calls and stopped correctly. Did the protocol not matter there?

It mattered — but it had already been paid for, during training. Models offered behind a function-calling API are trained on tool-use episodes of exactly this shape — reason, call, read the result, continue — so the convention that ReAct imposed by prompt in 2022 now sits, in tool-calling models, in the weights. Reasoning models go one step further and internalize the Thought itself: the deliberation ReAct forced into the visible record runs as **thinking tokens** before the answer, budgeted and billed but not prompted (→ Ch. 11). The migration is the same one Chapter 2 flagged for test-time compute: a procedure the caller once orchestrated — write your reasoning, then act — moves into the model, and the caller's protocol survives as the model's habit.

The practical consequence runs in both directions. Because the protocol is internalized, production systems mostly run function-calling loops and get grounded, interleaved reasoning without a ReAct prompt. But internalized does not mean guaranteed: the habit falls short on smaller models, unfamiliar tools, and long horizons, and then the remedy is the 2022 one — put the requirement back into the prompt and read what the model writes. The lab does both on the same questions and measures the difference.

## 4.6 Operations — Trace Reading

A **trace** = the complete execution record of the loop, the sequence of Thoughts, Actions, and Observations. In practitioner vocabulary, the accumulated record that the model reads and extends each turn is also called the scratchpad. Debugging an agent starts from the trace, not from the code — owning the loop means the full record of every run is ours to read. The procedure is as follows. The input is the trace of a run that ended in a wrong answer or a failure; the output is the location of what to fix.

1. **Locate the first error** — Read the trace from the beginning and find the first point that conflicts with fact or with the task. Do not search backward from the final answer: later errors are mostly propagations of the first one.
2. **Classify the error** — Determine which element the first error lies in. The branch determines what to fix.
   - An error in a Thought (wrong judgment) → fix the prompt.
   - An error in an Action (wrong call) → fix the tool's schema — its name, function description, and input format.
   - An error in an Observation (wrong or corrupted result) → fix the tool implementation.
3. **Reproduce and verify** — Rerun with the conversation record up to just before the first error point as input, and confirm that the fix actually removes the error.

Applying this procedure to the Act-only trace of 4.2: the first error point is the termination at Action 4. The call formats and the tool results are all normal, so the error class is judgment, and the fix target is the prompt. That fix is the convention of 4.3.

Two loop guards belong in the same operational kit. A **repetition guard** detects the loop's characteristic stall — the same Action with the same input recurring turn after turn, each reinjection returning the same Observation — and interrupts it (or injects a notice that the action was already tried), because a model that ignored the first identical result will ignore the fifth. And the **bound report**: when max_steps is exhausted, the returned answer must say so and carry the trace, never a fabricated best guess — a run that failed by budget is diagnosable, a disguised one is not.

The effect of a fix is confirmed by measurement, not by a single reproduction. A small evaluation set of fixed questions is kept, and every change to prompts or code is scored against the same set — the lab introduces a five-question set this week, and the homework re-scores it after the guard is added. Chapter 5's second half turns this practice into its own subject, and Chapter 13 extends it into a full benchmark harness.

## 4.7 Summary

Chapter 3's client repeated round trips under a hidden bound; this chapter took the loop into our own code, and with it the protocol, the bound, and the record. The protocol is ours to set: repeating actions without any requirement to write judgments (Act-only) fails in measurement, because for a model whose only workspace is text, the record retains no judgments — the prescription is ReAct, a written judgment before every action, under which the next query is decided on facts confirmed in the preceding observation (grounding) and even failed actions become input for course correction. The bound is ours to enforce: max_steps with an explicit failure report, plus a guard against repeated actions. The record is ours to read: trace reading locates the first error and classifies it into prompt, schema, or tool. Today's tool-calling models carry the ReAct convention in their weights, which is why the borrowed loop worked without it and why the explicit form returns when the internalized habit falls short.

The loop commits its Final Answer and stops; nothing reads the answer after it is written, and every fix so far was justified by a score we have not yet examined critically. Chapter 5 takes up both halves of that gap in one week: feeding outputs and attempts back to be improved (reflection), and making "it improved" a measured claim (evaluation).

---

**Presentation.** ReAct (Yao et al., 2022) — why reasoning and acting are interleaved, the Act-only and CoT contrast conditions, and per-task outcomes. Listen with the question: what exactly does the written Thought buy, and on which tasks does it buy nothing?

**Lab.** `W4_lab_loop.ipynb` — the loop built by hand, self-contained. First, rerun one Week-3 tool chain and read the client's trace — the hidden loop made visible. Then implement the loop of 4.1 in about twenty-five lines: the ReAct system prompt of 4.3, the Judge parser as the fill-in, execution, reinjection, max_steps with an explicit failure report. Act-only and ReAct run on the same five multi-hop questions over a course-paper catalog tool — the mini evalset (`labs/data/mini_evalset.jsonl`), re-scored in this week's homework — and the lab closes with trace reading on a failing run and the step bound as an honest exit. The from-scratch construction follows the pattern of Hugging Face's *Agents Course* unit 1 (the dummy-agent notebook). Reference answers: `labs/checkpoints/week04/solution.py`.

**Homework.** `W4_hw_loop_guard.ipynb` — add the repetition guard of 4.6 to the hand-built loop, show it converting a spinning run into a finished answer, and grow the mini evalset with two multi-hop questions of your own. Due before W5.
