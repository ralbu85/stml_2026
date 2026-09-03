# Week 02 — Slide content (paste-ready for Google Slides)

Format follows the professor's Week 01 deck: white background, section-divider slides, and
`Label: sentence` bullets. Source of truth is `notes.en.md` (Chapter 2); when the two
disagree, the notes win. Theory slot is 30 min → 30 slides (2 title + 6 dividers + 22 content).
Speaker cues are in `<!-- -->` comments and are not slide text.

Figures to place: `figures/fig-2-1-cot-workspace.svg` (slide 10), `figures/fig-2-2-self-consistency.svg` (slide 20).

---

## 1. Special Topics in ML
Week 02

## 2. Prompting & Reasoning
Week 02

<!-- 30 min theory, then two presentations (CoT, Self-Consistency), then the lab. -->

---

## 3. [divider] Same Model, Different Accuracy

## 4. Why prompting matters for an agent
- Recall from Week 01: an agent is a system whose next action is decided by the model's output. Every one of those decisions is an act of reasoning.
- The bound: an agent's accuracy is capped by the accuracy of the model's reasoning at each step. No architecture is accurate on top of a model that reasons inaccurately.
- Where Week 01 left the deficits: tools, memory, verification, iteration are all repaired by adding something around the model in later weeks.
- This week: the one thing that cannot be delegated outward — the quality of a single call. What can be gotten out of a bare call before anything is built around it.

## 5. What is Reasoning?
- Definition: deriving a conclusion from given premises through intermediate steps — arithmetic word problems, combining several facts to narrow an answer, ordering the steps of a plan.
- What separates it from recall: "What is the capital of Korea?" has no intermediate steps. Reasoning has steps that must be passed through on the way to the conclusion.
- The fragility: if any one intermediate step is wrong, the conclusion is wrong.

## 6. The observed split
- The problem: a cafeteria has 23 apples. They use 20 for lunch and buy 6 more. How many apples do they have?
  - Method A — demand only the answer: "Answer: 27" (wrong)
  - Method B — elicit the worked solution: "23 − 20 = 3, 3 + 6 = 9. Answer: 9" (correct)
- The source: a measured case from Figure 1 of the Chain-of-Thought paper (Wei et al., 2022), on the large models of that time.
- Today: a large model solves a problem of this size by direct answering, but the same failure reappears once the number of steps and digits grows. The lab reproduces it on harder items.
- The conclusion: the weights are identical, yet correctness splits. The cause lies in the computational process that produces the answer, not in the weights.

<!-- Live demo option: run the answer-only vs. worked-solution cells of the lab notebook §2.2 (six two-digit-multiplication problems: 0/6 vs. 6/6 on gpt-4o-mini). -->

---

## 7. [divider] A Workspace Made Only of Text

## 8. How an LLM computes an answer
- The constraint: an LLM has no workspace outside the text. Producing the next token, it reads only the text so far. Between one token and the next, no train of thought continues outside the text.
- The contrast: a person can pause mid-sentence and carry a value in their head. The only place a model can hold an intermediate result is the text it is writing.
- The consequence: whether intermediate values may be written into the output decides whether they exist at all.

## 9. The apple problem, read with this fact
- What the problem needs: compute 23 − 20 = 3, keep the 3 somewhere, then add 6 to it.
- Method B: the moment "23 − 20 = 3" is written, the 3 is stored in the text. Later tokens only read it and advance one step.
- Method A: only the answer is allowed, so there is nowhere to write. The single prediction that emits the answer digit must carry both calculations at once.
- The point: B's extra tokens are not decoration. They are the storage site of intermediate values, and A is the condition that forbids that storage.

## 10. Answer-only vs. worked solution (figure)
[Figure 2.1 — `figures/fig-2-1-cot-workspace.svg`]
Caption: In A, nothing stores the intermediate value, so one prediction must carry both calculations. In B, the written "3" is read back from the text and each step advances alone.

## 11. The limit, and its open cause
- Established fact: there is a limit on how many steps one prediction can carry. It is measured, and failure grows with steps and digits.
- The failure shape: prediction emits the most plausible token whether or not the computation finished. Where processing could not complete, an answer-shaped number assembled from 23 and 6 appears — the 27.
- Open question, why the limit exists: one analysis bounds a single prediction's internal computation by the layer count (Feng et al., 2023; Merrill & Sabharwal, 2023). Another: answer-only solution text is rare in training data. The two are not mutually exclusive.
- What follows needs only two facts: the limit is measured, and a place to write intermediate values circumvents it.

## 12. Hallucination — the same cause, second symptom
- Definition: generating content that is not factual but plausible.
- The cause: prediction never waits. When the required fact or computation is not available, the most probable continuation is emitted anyway, and that continuation is shaped like an answer.
- Two defects, one mechanism: the computation limit (27) and hallucination (a confident false premise) are both "most plausible token, regardless of completion."
- Which one prompting can fix: this lecture repairs the computation limit. The hallucination defect returns on slide 19.

---

## 13. [divider] Chain-of-Thought

## 14. The remedy: give the model a place to write
- The principle: make the model write out the solution instead of jumping to the answer. Each token then only reads the written values and advances one step.
- ELI5: a person solving a hard calculation on paper instead of in their head. The paper is the text.
- The only lever: text placed in the prompt. It takes exactly two forms — an instruction, or worked examples.

## 15. Method 1 — Instruction (zero-shot CoT)
- The move: append one line after the question demanding a worked solution (Kojima et al., 2022).

> There are 23 apples. 20 are used and 6 more are bought. How many are there?
> Write the solution step by step, then give the answer on the last line as "ANSWER: <number>".

- The output flips to Method B: "23 − 20 = 3. 3 + 6 = 9. ANSWER: 9".
- The catch: convenient, but it underspecifies. "Step by step" fixes neither how fine the steps are nor how the final answer is written.

## 16. Method 2 — Worked examples (few-shot CoT)
- The move: prepend worked question–answer pairs before the question.

> Q: Roger has 5 tennis balls. He buys 2 more cans of 3 balls each. How many balls does he have?
> A: He starts with 5 balls. 2 cans of 3 balls is 3 × 2 = 6. 5 + 6 = 11. ANSWER: 11
>
> Q: There are 23 apples. 20 are used and 6 more are bought. How many are there?
> A:

- Why it works: in-context learning — examples in the prompt specify the output format and procedure with no weight update. When the examples contain worked solutions, the model generates a solution first.
- The original form: this is the form the Chain-of-Thought paper uses (Wei et al., 2022).

## 17. What examples fix that instructions cannot
- Definition: Chain-of-Thought (CoT) = the family of prompting techniques that induce the model to generate its solution process before the answer.
- Why both forms work: at the moment the final "9" is produced, the text already contains "23 − 20 = 3" and "3 + 6 =". The model finishes by reading written values, not by computing both steps from scratch.
- The division of labor: instruction for convenience, examples for control of procedure and format. A worked example pins down exactly what "solve step by step" leaves open — step granularity, answer line, units.
- Emergence: the effect appears only above a model-scale threshold. In small models CoT is ineffective or harmful. The magnitudes (GSM8K) and the scale curve are this week's first presentation.
- Why the lab measures exemplar writing: writing a good worked example is the specification skill this week trains (lab §4–5, assignments 8.2 and 8.4).

---

## 18. [divider] What CoT Cannot Fix

## 19. A flawless solution, a wrong answer
- The question (HotpotQA, Figure 1 of the ReAct paper, Yao et al., 2022): "Aside from the Apple Remote, what other device can control the program the Apple Remote was originally designed to interact with?"
- The CoT run: "The Apple Remote was originally designed to interact with Apple TV. Apple TV can be controlled by iPhone, iPad, and iPod Touch. So the answer is iPhone, iPad, and iPod Touch." — wrong.
- What went wrong: the form is impeccable, every step connects. The first premise is false. The program was Front Row, not Apple TV. Correct answer: keyboard function keys.
- The diagnosis in the paper: reasoning not grounded in the external world → fact hallucination and error propagation.

## 20. Why no prompt can fix this
- The root: CoT's reasoning draws only on knowledge stored in the parameters. There is no path for checking an external fact.
- The lesson: coherence of the reasoning structure does not guarantee factuality. Adding "verify each step before continuing" produces more coherent text, not a checked fact.
- The structural fix: a step that checks facts against the world. That requires tools (Week 03) and the agent loop (Week 04). The same question, solved by a loop with a search tool, is traced in Week 04.
- What is still open on the computation side: CoT added predictions inside one response. The other direction is to produce the response itself more than once.

---

## 21. [divider] Ask More Than Once

## 22. One path is one sample
- What CoT commits to: a single written path. If any step on it is wrong the conclusion is wrong, and the model does not know.
- The stochastic fact: an LLM samples tokens from a probability distribution. Raise the temperature (the sampling-randomness parameter) and ask again, and each run follows a different solution path to a possibly different answer.
- The reframe: one response is one draw from the set of possible paths. A wrong draw does not mean the next draw is wrong.

## 23. Majority voting — Self-Consistency
- The procedure (Wang et al., 2022): sample N solutions at high temperature, extract each final answer, take the majority vote.
- Why it works: the answer probability sums over all reasoning paths, P(a | q) = Σ_r P(a | r, q) P(r | q). One ask shows only the single most plausible path's term. Voting over samples estimates the whole sum.
- The mechanism in practice: correct answers are reached by different paths converging on one value. Wrong answers scatter, each wrong in its own way. Counting brings the convergent answer to the front.
- The numbers: measured gains and the cost of N samples are this week's second presentation.

## 24. Self-consistency in one picture (figure)
[Figure 2.2 — `figures/fig-2-2-self-consistency.svg`]
Caption: sampled paths from the same question. Correct paths converge on one value, wrong paths scatter, and the vote surfaces the convergent answer.

## 25. When the vote cannot be tallied
- The precondition: answers must be discrete and extractable — a number, a choice, a short string — so that equal answers can be counted.
- Where it breaks: free-form prose. No two 200-word abstracts are literally equal, so there is nothing to count.
- The replacement: selecting among such outputs needs a scoring device — a verifier. Named on the next slide, built in Week 05.

---

## 26. [divider] Test-Time Compute

## 27. The bill is the number of predictions
- The accounting: CoT lengthens one response (one extra prediction per solution token). Self-consistency produces N responses (N× predictions).
- The unit price: one prediction costs roughly the same everywhere, so the number of predictions is the bill.
- Definition: test-time compute = leaving the weights untouched and buying accuracy by spending more predictions at answer time. The principle behind every method in the family is inference-time scaling.

## 28. The method family
| Method | How predictions are increased |
|---|---|
| CoT | one response made longer — predictions added per solution token |
| Self-consistency | N responses → majority vote over discrete answers |
| Best-of-N | N responses → a verifier selects the best (replaces the vote when answers are not discrete) |
| Tree search | branch, evaluate, backtrack (Week 07, planning & search) |

- The shared principle: exchange inference computation for accuracy. Best-of-N and tree search additionally require a verifier — a device that scores answers against each other.

## 29. Already on the price list
- Thinking modes (OpenAI o-series, Claude extended thinking, Gemini thinking): the written solution of this lecture moved inside the model, billed by the token (Week 11).
- The tiers above (o1 pro, Gemini Deep Think, Grok Heavy): documented by their vendors as exploring several reasoning lines in parallel — the sampling-and-selection of this lecture, sold as a subscription level.
- Not free: N samples multiply cost and latency by N. The practical decision variable is not the size of N but which questions deserve N > 1 (Week 12, routing).

---

## 30. This week
- The arc: same model, different accuracy → no workspace but text → CoT writes the workspace → CoT cannot check facts (tools, Week 03) → sample and vote → test-time compute.
- Presentations (first student week): Chain-of-Thought (Wei et al., 2022) — prompting-only gains and the emergence curve. Self-Consistency (Wang et al., 2022) — sample-and-vote, its measured gains, the cost of N.
- Lab (`W2_lab_prompting.ipynb`): answer-only vs. worked solution on the apple problem and six code-graded arithmetic items → the silent-thinking and answer-first controls → a code-graded eval improved from baseline to a format fix to your own CoT prompt (target ≥ 11/12) → few-shot email classification (4/4) → self-consistency on the hardest item → the hallucination limit. Four graded assignments close it.
- Homework (`W2_hw_build_evalset.ipynb`): an eight-item code-graded evalset in your own domain, and a CoT template that beats answer-only on it (≥ 7/8). Due before Week 03.
- Next week: tools — the external checking step that this week's failure on slide 19 requires.

<!-- Timing: slides 3–12 ≈ 10 min, 13–20 ≈ 10 min, 21–30 ≈ 10 min. Slide 12 is the one to keep even if time runs short: it is what makes the Week 03 hand-off (tools fix hallucination, prompting does not) land. -->
