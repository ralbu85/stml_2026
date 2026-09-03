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
- Recall (Week 01): an agent is a system whose next action is decided by the model's output. Each such decision is an inference from the current state to an action.
- Bound: the accuracy of an agent is bounded above by the accuracy of the model's reasoning at each step. Tools, memory, and loops (Weeks 03–05) add components around the model; they do not raise the accuracy of a single call.
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

- Evidence: Figure 1 of Wei et al. (2022), measured on the large models of 2022.
- Current models: a problem of this size is solved under Prompt A as well; the same split reappears when the number of steps and digits grows (lab §2.2: two-digit products, 0/6 under A, 6/6 under B on gpt-4o-mini).
- Conclusion: the weights are identical in A and B. The difference in correctness is caused by the computation the prompt permits before the answer token.

<!-- Live demo option: run lab §2.2 (answer-only vs. worked solution). -->

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

## 11. The per-prediction limit
- Empirical fact: the number of sequential operations one prediction can perform is bounded. Failure frequency rises with the number of steps and digits.
- Failure form: prediction emits the most probable token whether or not the computation is complete. An incomplete computation yields an answer-shaped number built from the digits in the problem (27 from 23 and 6).
- Proposed causes: (i) the depth of computation within one forward pass is bounded by the layer count (Feng et al., 2023; Merrill & Sabharwal, 2023); (ii) answer-only solution text is rare in training data. The two are compatible.
- What the remainder requires: the limit is measured, and writing intermediate values circumvents it.

## 12. Hallucination
- Definition: hallucination = generation of content that is plausible but not factual.
- Mechanism: the same as the computation limit. When the required fact or computation is unavailable, prediction still emits the most probable continuation, and that continuation has the form of an answer.
- Two symptoms, one mechanism: a wrong number (27) and a confident false premise are both "most probable token, regardless of completion."
- Scope: prompting repairs the computation limit (next section). It does not repair hallucination (slides 19–20).

---

## 13. [divider] Chain-of-Thought

## 14. Chain-of-thought prompting
- Definition: chain-of-thought (CoT) prompting = prompting that induces the model to generate its solution process before the final answer (Wei et al., 2022).
- Mechanism: each token of the solution reads the values already written and advances one operation; the answer token reads the last intermediate value.
- Two forms: an instruction (zero-shot CoT) or worked examples (few-shot CoT). Both are text in the prompt; nothing else changes.

## 15. Form 1 — Instruction (zero-shot CoT)
- Procedure: append one instruction after the question (Kojima et al., 2022).

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

- Emergence: the CoT effect appears only above a model-scale threshold; in small models it is absent or harmful (Wei et al., 2022). Magnitudes and the scale curve: this week's first presentation.
- Lab: assignments 8.1 (instruction), 8.2 and 8.4 (examples) measure both forms on code-graded sets.

---

## 18. [divider] The Limit of Chain-of-Thought

## 19. Coherent reasoning on a false premise
- Question (HotpotQA; Figure 1 of Yao et al., 2022): "Aside from the Apple Remote, what other device can control the program the Apple Remote was originally designed to interact with?"

> CoT output: The Apple Remote was originally designed to interact with Apple TV. Apple TV can be controlled by iPhone, iPad, and iPod Touch. So the answer is iPhone, iPad, and iPod Touch.

- Error: the first premise is false. The program was Front Row; the correct answer is keyboard function keys.
- Diagnosis (same paper): the reasoning is not grounded in external information, so a hallucinated premise propagates through a valid chain.

## 20. Why prompting cannot repair it
- Cause: CoT draws only on knowledge stored in the parameters. No prompt gives the model access to an external fact.
- Test: adding "Verify each step before continuing" produces a more elaborate chain on the same false premise.

> Prompt: <question> Verify each step before continuing.
> Output: Step 1: The Apple Remote was designed for Apple TV. Verified. Step 2: …

- Repair: a step that checks facts against an external source. This requires tools (Week 03) and the agent loop (Week 04); Week 04 traces this question through a loop with a search tool.
- Remaining direction: CoT adds predictions within one response. Predictions can also be added by generating the response more than once.

---

## 21. [divider] Self-Consistency

## 22. One response as one sample
- Sampling: an LLM draws each token from a probability distribution. Temperature = the parameter controlling the randomness of that draw; at temperature 0 the most probable token is taken.
- Consequence: at temperature > 0, repeated runs of the same prompt follow different solution paths and may reach different answers.
- Interpretation: one response is one sample from the set of possible reasoning paths. A wrong sample does not imply that the next sample is wrong.

> Same CoT prompt, temperature 1.0, five runs → final answers: 9, 27, 9, 8, 9

## 23. Majority voting — Self-Consistency
- Definition: self-consistency = sample N solutions at temperature > 0, extract the final answer of each, and return the majority answer (Wang et al., 2022).
- Justification: P(a | q) = Σ_r P(a | r, q) P(r | q). A single response evaluates one term (one path r). The vote over samples estimates the sum over paths.
- Empirical pattern: correct answers are reached by different paths that converge on one value; wrong answers scatter across distinct values.
- Magnitudes and the cost of N: this week's second presentation.

## 24. Self-consistency (figure)
[Figure 2.2 — `figures/fig-2-2-self-consistency.svg`]
Caption: Paths sampled from the same question. Correct paths converge on one value, wrong paths scatter, and the vote returns the convergent value.

## 25. Precondition of the vote
- Requirement: the final answer must be discrete and extractable (a number, a choice, a short string) so that equal answers can be counted.
- Failure case: free-form text. Two 200-word abstracts are never identical; the vote has nothing to count.
- Replacement: selection among non-discrete outputs requires a scoring function, a verifier (Week 05).

---

## 26. [divider] Test-Time Compute

## 27. Accounting in predictions
- Count: CoT lengthens one response by one prediction per solution token. Self-consistency multiplies the number of responses by N.
- Cost: the cost of one prediction is approximately constant, so cost is proportional to the number of predictions.
- Definition: test-time compute = accuracy obtained by increasing the number of predictions at inference time, with the weights unchanged. The general principle is inference-time scaling.

> Lab §4.6, one eval item (gpt-4o-mini): answer-only = 1 completion token; chain-of-thought = 75; five CoT samples = 375.

## 28. Methods
| Method | Additional predictions |
|---|---|
| Chain-of-thought | one longer response: one prediction per solution token |
| Self-consistency | N responses; majority vote over discrete answers |
| Best-of-N | N responses; a verifier selects one (replaces the vote for non-discrete outputs) |
| Tree search | branch, evaluate, backtrack (Week 07) |

- Common principle: inference computation is exchanged for accuracy. Best-of-N and tree search additionally require a verifier.

## 29. Test-time compute in deployed systems
- Reasoning modes (OpenAI o-series, Claude extended thinking, Gemini thinking): the written solution of this chapter generated inside the model and billed per token (Week 11).
- Parallel-reasoning tiers (o1 pro, Gemini Deep Think, Grok Heavy): several reasoning lines generated in parallel and selected, the procedure of slides 22–25.
- Cost: N samples multiply cost and latency by N. The design variable is which queries receive N > 1 (Week 12, routing).

---

## 30. This week
- Chapter: prompt dependence of accuracy → the text as the only workspace → chain-of-thought → its limit (ungrounded premises) → self-consistency → test-time compute.
- Presentations: Chain-of-Thought (Wei et al., 2022) — accuracy gains from prompting and the emergence curve. Self-Consistency (Wang et al., 2022) — sample-and-vote, measured gains, cost of N.
- Lab (`W2_lab_prompting.ipynb`): answer-only vs. worked solution on code-graded arithmetic → silent-thinking and answer-first controls → a code-graded eval improved from baseline to format fix to your own CoT prompt (≥ 11/12) → few-shot email classification (4/4) → self-consistency on the hardest item → the hallucination limit. Four graded assignments.
- Homework (`W2_hw_build_evalset.ipynb`): an eight-item code-graded evalset in your own domain and a CoT template that beats answer-only on it (≥ 7/8). Due before Week 03.
- Next week: tools, the external checking step required by slide 20.

<!-- Timing: slides 3–12 ≈ 10 min, 13–20 ≈ 10 min, 21–30 ≈ 10 min. Slide 12 must be kept even if time runs short: it sets up the Week 03 hand-off (tools repair hallucination, prompting does not). -->
