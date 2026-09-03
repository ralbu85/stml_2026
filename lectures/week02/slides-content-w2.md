# Week 02 — Slide content

Format: white background, section-divider slides, `Label: statement` bullets, verbatim prompts in
quote blocks. Source of truth is `notes.en.md` (Chapter 2). Theory slot 30 min → 30 slides.
Speaker cues are in `<!-- -->` comments and are not slide text.

Figures: `figures/fig-2-1-cot-workspace.svg` (slide 10), `figures/fig-2-2-self-consistency.svg` (slide 24).

---

## 1. Special Topics in ML
Week 02

## 2. Prompting & Reasoning
Week 02

<!-- 30 min theory, then two presentations (CoT, Self-Consistency), then the lab. -->

---

## 3. [divider] Prompt Dependence of Reasoning Accuracy

## 4. Reasoning accuracy and agent accuracy
- Premise: an agent is a system whose next action is decided by the model's output. Each such decision is an inference from the current state to an action.
- Bound: the accuracy of an agent is bounded above by the accuracy of the model's reasoning at each step. Tools, memory, and loops add components around the model; they do not raise the accuracy of a single call.
- Scope of this chapter: the accuracy of one model call as a function of the prompt.

## 5. Reasoning
- Definition: reasoning = deriving a conclusion from given premises through intermediate steps.
- Instances: an arithmetic word problem (intermediate results), combining several facts to narrow an answer (intermediate inferences), ordering the steps of a plan (intermediate states).
- Contrast with recall: "What is the capital of Korea?" has no intermediate step. Reasoning has steps that must be completed before the conclusion.
- Error propagation: if any intermediate step is wrong, the conclusion is wrong.

## 6. The same model, two prompts
- Problem: a cafeteria has 23 apples. They use 20 for lunch and buy 6 more. How many apples do they have?

> Prompt A: <problem> Reply with only the number.
> Output A: 27   (wrong)
>
> Prompt B: <problem> Write the solution step by step, then give the answer on the last line as ANSWER: <number>.
> Output B: 23 − 20 = 3. 3 + 6 = 9. ANSWER: 9   (correct)

- Evidence: measured on the large models of 2022; this pair of outputs is the observation that started chain-of-thought research.
- Current models: a problem of this size is solved under Prompt A as well. The same split reappears when the number of steps and digits grows: on six problems with a two-digit product and two further operations, gpt-4o-mini scores 0/6 under A and 6/6 under B.
- Conclusion: the weights are identical in A and B. The difference in correctness is caused by the computation the prompt permits before the answer token.

<!-- Live demo option: run the answer-only vs. worked-solution comparison in the notebook. -->

---

## 7. [divider] The Text as the Model's Only Workspace

## 8. Token prediction and intermediate values
- Mechanism: an LLM generates one token at a time; each prediction reads only the text so far. No state is carried between tokens outside the text.
- Consequence: an intermediate value exists for the model only if it has been written into the text.
- Contrast: a person can hold "3" in working memory while continuing a sentence. The model has no working memory apart from the text it writes.

## 9. The apple problem under this mechanism
- Requirement: compute 23 − 20 = 3, retain 3, then compute 3 + 6.
- Prompt B: once "23 − 20 = 3" is written, the value 3 is in the text. The prediction of "9" reads 3 and 6 and performs one operation.
- Prompt A: no intermediate text is permitted. The single prediction that emits the answer must perform both operations.
- Interpretation: the extra tokens of B are the storage of intermediate values. A is the condition in which that storage is forbidden.

## 10. Answer-only vs. worked solution (figure)
[Figure 2.1 — `figures/fig-2-1-cot-workspace.svg`]
Caption: Under A, no token stores the intermediate value, so one prediction must carry both calculations. Under B, the written "3" is read back from the text and each step is one operation.

## 11. Capacity of a single prediction
- Question: how many operations can one prediction complete when no intermediate value may be written?
- Measurement: the same two prompts on problems of increasing size (gpt-4o-mini).

> 23 − 20 + 6                          answer only: correct
> 47 × 38 − 519 + 284, six problems     answer only: 0 of 6      written solution first: 6 of 6

- Result: the number of operations one prediction can complete is bounded, and the bound is reached once a multiplication is involved.
- Failure form: prediction emits the most probable token whether or not the computation is complete. An unfinished computation therefore returns a number, not a refusal: expected 1551, returned 1516.
- Proposed causes: (i) the depth of computation within one forward pass is bounded by the number of layers; (ii) answer-only solution text is rare in training data. The two are compatible.

## 12. Hallucination
- Definition: hallucination = generation of content that is plausible but not factual.
- Mechanism: prediction does not stop when the required computation is unfinished, and it does not stop when the required fact is absent. In both cases the most probable continuation is emitted, and it has the form of an answer.

> unfinished computation → 1516 in place of 1551
> absent fact           → a plausible name in place of "I do not know"

- Consequence: the output carries no signal of which case produced it. A wrong number and an invented fact are equally fluent and equally confident.
- Scope: writing the solution raises the bound on the computation limit, as the next section shows. It gives the model no access to a fact it does not have, so hallucination is untouched by it.

---

## 13. [divider] Chain-of-Thought

## 14. Chain-of-thought prompting
- Definition: chain-of-thought (CoT) prompting = prompting that induces the model to generate its solution process before the final answer.
- Mechanism: each token of the solution reads the values already written and advances one operation; the answer token reads the last intermediate value.
- Two forms: an instruction (zero-shot CoT) or worked examples (few-shot CoT). Both are text in the prompt; nothing else changes.

## 15. Form 1 — Instruction (zero-shot CoT)
- Procedure: append one instruction after the question.

> There are 23 apples. 20 are used and 6 more are bought. How many are there?
> Write the solution step by step, then give the answer on the last line as ANSWER: <number>.
>
> Output: 23 − 20 = 3. 3 + 6 = 9. ANSWER: 9

- Property: the instruction elicits a solution but does not specify its granularity or the format of the final line. "Step by step" admits many layouts.

## 16. Form 2 — Worked examples (few-shot CoT)
- Procedure: prepend question–solution pairs before the question.

> Q: Roger has 5 tennis balls. He buys 2 more cans of 3 balls each. How many balls does he have?
> A: He starts with 5 balls. 2 cans of 3 balls is 3 × 2 = 6. 5 + 6 = 11. ANSWER: 11
>
> Q: There are 23 apples. 20 are used and 6 more are bought. How many are there?
> A:
>
> Output: 23 − 20 = 3. 3 + 6 = 9. ANSWER: 9

- Definition: in-context learning = the property that examples in the prompt determine the output's format and procedure with no weight update.
- Property: the example fixes what the instruction leaves open: the step granularity, the wording of each step, and the exact final line.

## 17. Instruction versus example
- Difference: an instruction names the requirement; an example exhibits it. The example therefore pins format and procedure that the instruction underspecifies.

> Instruction: "Answer with the date."      → "The final date is March 10th, 2026."
> Example:    "Note: … / DATE: 2026-06-09"  → "DATE: 2026-03-10"

- Emergence: the CoT effect appears only above a model-scale threshold; in small models it is absent or harmful.
- Bound: writing the solution moves the per-prediction bound outward, it does not remove it. Each written step is itself one prediction. With three-digit factors in the same six problems, the written solution scores 1 of 6.

---

## 18. [divider] The Limit of Chain-of-Thought

## 19. Coherent reasoning on a false premise
- Question: "Aside from the Apple Remote, what other device can control the program the Apple Remote was originally designed to interact with?"

> CoT output: The Apple Remote was originally designed to interact with Apple TV. Apple TV can be controlled by iPhone, iPad, and iPod Touch. So the answer is iPhone, iPad, and iPod Touch.

- Error: the first premise is false. The program was Front Row; the correct answer is keyboard function keys.
- Diagnosis: the reasoning is not grounded in external information, so a hallucinated premise propagates through a valid chain.

## 20. Why prompting cannot repair it
- Cause: CoT draws only on knowledge stored in the parameters. No prompt gives the model access to an external fact.
- Test: adding "Verify each step before continuing" produces a more elaborate chain on the same false premise.

> Prompt: <question> Verify each step before continuing.
> Output: Step 1: The Apple Remote was designed for Apple TV. Verified. Step 2: …

- Repair: a step that checks facts against an external source, that is, a tool call (for this question, a search) inserted between the premise and the next step.
- Remaining direction: CoT adds predictions within one response. Predictions can also be added by generating the response more than once.

---

## 21. [divider] Self-Consistency

## 22. One response as one sample
- Sampling: an LLM draws each token from a probability distribution. Temperature = the parameter controlling the randomness of that draw; at temperature 0 the most probable token is taken.
- Consequence: at temperature > 0, repeated runs of the same prompt follow different solution paths and may reach different answers.
- Interpretation: one response is one sample from the set of possible reasoning paths. A wrong sample does not imply that the next sample is wrong.

> Same CoT prompt, temperature 1.0, five runs → final answers: 9, 27, 9, 8, 9

## 23. Majority voting — Self-Consistency
- Definition: self-consistency = sample N solutions at temperature > 0, extract the final answer of each, and return the majority answer.
- Justification: P(a | q) = Σ_r P(a | r, q) P(r | q). A single response evaluates one term (one path r). The vote over samples estimates the sum over paths.
- Empirical pattern: correct answers are reached by different paths that converge on one value; wrong answers scatter across distinct values.

## 24. Self-consistency (figure)
[Figure 2.2 — `figures/fig-2-2-self-consistency.svg`]
Caption: Paths sampled from the same question. Correct paths converge on one value, wrong paths scatter, and the vote returns the convergent value.

## 25. Precondition of the vote
- Requirement: the final answer must be discrete and extractable (a number, a choice, a short string) so that equal answers can be counted.
- Failure case: free-form text. Two 200-word abstracts are never identical; the vote has nothing to count.
- Replacement: selection among non-discrete outputs requires a scoring function, a verifier.

---

## 26. [divider] Test-Time Compute

## 27. Accounting in predictions
- Count: CoT lengthens one response by one prediction per solution token. Self-consistency multiplies the number of responses by N.
- Cost: the cost of one prediction is approximately constant, so cost is proportional to the number of predictions.
- Definition: test-time compute = accuracy obtained by increasing the number of predictions at inference time, with the weights unchanged. The general principle is inference-time scaling.

> One question, gpt-4o-mini: answer-only = 1 completion token; chain-of-thought = 75; five CoT samples = 375.

## 28. Methods
| Method | Additional predictions |
|---|---|
| Chain-of-thought | one longer response: one prediction per solution token |
| Self-consistency | N responses; majority vote over discrete answers |
| Best-of-N | N responses; a verifier selects one (replaces the vote for non-discrete outputs) |
| Tree search | branch, evaluate, backtrack |

- Common principle: inference computation is exchanged for accuracy. Best-of-N and tree search additionally require a verifier.

## 29. Test-time compute in deployed systems
- Reasoning modes (OpenAI o-series, Claude extended thinking, Gemini thinking): the written solution of this chapter generated inside the model and billed per token.
- Parallel-reasoning tiers (o1 pro, Gemini Deep Think, Grok Heavy): several reasoning lines generated in parallel and one selected, that is, self-consistency or best-of-N.
- Cost: N samples multiply cost and latency by N. The design variable is which queries receive N > 1.

---

## 30. Summary
- Observation: the same model answers the same problem correctly or incorrectly depending on whether the prompt permits a written solution before the answer.
- Cause: the model's only workspace is the text it generates; an intermediate value exists only once written. Answer-only prompting forces every operation into one prediction, whose capacity is bounded.
- Chain-of-thought: an instruction or worked examples induce the written solution. Examples additionally fix the granularity and format that an instruction leaves open.
- Limit: chain-of-thought draws only on parametric knowledge. A false premise propagates through a valid chain; repair requires an external check, not a prompt.
- Self-consistency: one response is one sampled path. Sampling N paths and taking the majority of discrete answers estimates the answer probability summed over paths.
- Test-time compute: chain-of-thought and self-consistency both buy accuracy with additional predictions at inference time, with the weights unchanged.

<!-- Timing: slides 3–12 ≈ 10 min, 13–20 ≈ 10 min, 21–30 ≈ 10 min. Slide 12 must be kept even if time runs short: tools repair hallucination, prompting does not. -->
