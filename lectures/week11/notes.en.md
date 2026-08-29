# Chapter 11. Reasoning Models & Reinforcement Learning

Chapter 2 raised the quality of reasoning while leaving the weights untouched, and everything it did lived on the caller's side: an instruction elicited a written solution (CoT), worked examples pinned down its format, and the caller's code sampled N responses and took a majority vote (self-consistency). The common shape was a procedure wrapped around the model — the model itself never changed.

This chapter starts from what happened when that investment moved inside. Models of the o1 and DeepSeek-R1 family answer a hard question by thinking at length on their own — no instruction demands it, no caller code samples or votes — and answer better the longer they think. Two questions organize the chapter. The user's question: what is such a reasoning model, and when is it worth its cost (11.1)? The builder's question: how does the ability to write a long, correct solution get into the weights (11.2–11.6)? The answer runs from the absence of training data (11.2), through learning from the model's own filtered solutions (STaR, 11.3), to reinforcement learning on outcome rewards (11.4), its public extreme case R1 (11.5), and the limits of what a reward can buy (11.6).

## 11.1 Internalization — Reasoning Models

The methods of test-time compute work only if the caller implements a procedure. Using self-consistency means our code must call the model N times on the same question, parse the answers, and tally a majority vote (→ 2.5); using Best-of-N additionally requires a verifier that ranks candidate answers. The limits of this approach come from the procedure itself. Majority voting holds only for problems whose final answer is discrete enough to collect votes; the procedure must be redesigned for every task; and the cost is a uniform N-fold multiple whether the problem is easy or hard.

A **reasoning model** is a model trained to move this investment of computation inside itself — to think at length on its own before answering (the o1 and DeepSeek-R1 family; OpenAI, 2024; DeepSeek-AI, 2025). It works in a single call with no caller-side procedure, and the model itself adjusts how long it thinks to the problem at hand.

In a reasoning model, the amount of thinking is controlled by the **thinking budget**, a parameter capping the number of thinking tokens. Token count is prediction count and is what is billed — thinking tokens are charged like output tokens — so this one parameter sets the exchange rate between accuracy and cost. Vendors use different names (reasoning effort, thinking budget), but the concept is one: the amount of thinking is an adjustable, billable resource.

The two kinds of model divide labor as follows.

| | General model | Reasoning model |
|---|---|---|
| Strengths | tool calls, well-structured tasks | mathematics, planning, hard judgment |
| Cost · latency | low | high (proportional to thinking tokens) |

The default choice is the cheap general model; the reasoning model is deployed only at bottleneck steps. The basis for the choice is measurement, not impression (→ Ch. 5, evaluation).

Up to this point the perspective has been that of selecting a finished reasoning model. The remaining question is how such a model is made — how the ability to generate a long, correct solution before the answer is put into the weights.

## 11.2 The Training Problem — Data and Labels

From the standpoint of supervised learning the answer looks obvious: collect a large corpus of texts containing long worked solutions and train on it. The problem is that this data does not exist. The two contemporary ways of obtaining it each ran into a different limit (Zelikman et al., 2022, §1 states this as the training motivation). Having humans hand-write a solution dataset is expensive, and building one for every problem domain of interest is infeasible. Putting a few worked examples into the prompt (few-shot) needs no dataset but does not reach the accuracy of **fine-tuning** — continued training that updates the weights on a prepared dataset.

The labeling situation contains one asymmetry. Process labels — which step is right, where the solution went wrong — must be annotated by hand and are therefore hard to produce. Outcome labels, by contrast, are decided automatically in verifiable domains: comparing against the answer key in mathematics, passing the tests in code. Process labels are absent, but outcome labels come at no extra cost. This asymmetry is the common foundation of the two methods that follow.

## 11.3 Self-Generation and Filtering — STaR

**STaR (Self-Taught Reasoner)** is a method that obtains solution data from the model itself instead of from humans (Zelikman et al., 2022). A few worked examples are given as a seed; the model generates solutions to many problems; only the solutions whose final answer is correct are kept; and the model is fine-tuned on those. Repeating the process with the improved model, generation, filtering, and fine-tuning interlock and the quality of the solutions rises on its own.

> **[Figure 11.1]** The STaR bootstrap loop. Seed examples → the model generates solutions to many problems → a filter passes only solutions with a correct final answer → fine-tune on what remains → return to the loop with the improved model. At the filter, mark "outcome correctness stands in for process labels"; on a branch leaving the loop, mark "problems the model never solves leave no surviving solutions — no training signal", foreshadowing the limit treated in 11.4.

This structure solves the problem of 11.2 as follows. Instead of humans producing process labels, the outcome verdict serves as the selection criterion for solutions. There is no guarantee that every solution reaching the correct answer is a good solution, but that filter alone collects enough data for training to work. The paper reports that fine-tuning this way approached the fine-tuned performance of a model 30× larger. The device of not discarding failed problems but regenerating solutions after revealing the answer as a hint (rationalization) is left to the presentation as optional depth.

STaR's limit also comes from its structure. Because the final step is supervised learning, the model learns only to imitate its own filtered solutions. On problems the current model never answers correctly, no solutions survive and there is no training signal at all; nor is there any pressure toward solutions better than the surviving ones.

## 11.4 Reinforcement Learning

STaR's limit came from its final step being supervised learning — imitation of demonstrations. In a situation where no demonstration of the desired behavior exists and only the outcome's correctness can be judged, what is needed is a framework that uses that outcome signal directly as the training signal, without passing through demonstrations. That framework is reinforcement learning.

**Reinforcement learning (RL)** is learning that improves a behavior rule from a reward signal alone, without demonstrations of the correct answer.

The rule that generates behavior is called the **policy**, and the score assigned to the result of behavior is called the **reward**. In the context of LLM training, the policy is the model's generation distribution, the behavior is the generation of a response, and the reward is a score assigned to the completed response. Where supervised learning imitates demonstrations, reinforcement learning finds the direction that raises reward through exploration. Because it does not imitate, it is not bounded by the ceiling of demonstration data, and on a previously unsolved problem a single success during exploration reinforces that direction.

Written as an equation, the objective of reinforcement learning is the maximization of expected reward when the policy $\pi_\theta$ with parameters $\theta$ generates a response $o$ to a question $q$:

$$J(\theta) = \mathbb{E}_{o \sim \pi_\theta(\cdot \mid q)}\big[\, r(q, o) \,\big]$$

Read in words: $q$ is the question, $o$ is a response sampled from the model, $\pi_\theta(\cdot \mid q)$ is the model's distribution over responses, $r(q,o)$ is the scalar reward assigned to that response, and $J(\theta)$ is the reward expected on average when the current parameters generate responses. The gradient of this objective is given by the policy gradient theorem:

$$\nabla_\theta J(\theta) = \mathbb{E}_{o \sim \pi_\theta}\big[\, r(q, o)\, \nabla_\theta \log \pi_\theta(o \mid q) \,\big]$$

The update rule this equation dictates is simple: sample responses, score them, and move the parameters in the direction that raises the log-probability of high-reward responses. The form of the update is the same as supervised learning, which raises the log-probability of demonstration data; the difference is that reward, not a demonstration set, chooses whose probability is raised. In practice, using the raw reward $r$ makes the gradient estimate high-variance, so $r - b$ with a baseline $b$ is used instead: the signal is not absolute reward but how much better a response is than an average one, and the choice of baseline is one of the forks between algorithms (→ GRPO in 11.5).

The crux is where the reward comes from. Reward sources divide into human preference and rule-based verification. **RLHF (reinforcement learning from human feedback)** uses as reward a reward model trained on human preference judgments. It is used to improve properties with no right answer — helpfulness, safety — and is the standard procedure of chatbot alignment today (InstructGPT; Ouyang et al., 2022). But a learned reward model is an approximation: it cannot accurately judge the mathematical correctness of a long solution, and the approximation's loopholes can be exploited during optimization. **RLVR (reinforcement learning with verifiable rewards)** uses as reward a signal verified by rules — answer-key comparison, test passing. The asymmetry established in 11.2 — process labels absent, outcome correctness decided automatically — here takes the position of the reward. Training reasoning ability is a problem of verifiable domains (mathematics, code), so RLVR applies; the public case that carried it to the extreme is R1, next.

## 11.5 Learning from Verifiable Reward — R1

DeepSeek-R1 is the public case that carried RLVR to the extreme (DeepSeek-AI, 2025). R1-Zero skipped the supervised stage and began reinforcement learning directly from a pretrained base model; the reward was only the rule-based signals of final-answer correctness and format compliance, with no constraint placed on the solution process. The authors' stated design rationale interlocks with STaR's limit: human-defined reasoning patterns can restrict the model's exploration, so unconstrained reinforcement learning better induces the emergence of new reasoning ability (§1).

For the policy update they used **GRPO (Group Relative Policy Optimization)**. GRPO's answer to the baseline problem of 11.4 is relative comparison within a group. For the same question $q$, sample $G$ responses $o_1, \dots, o_G$, score each with reward $r_i$, and compute each response's relative standing against the group mean as the baseline:

$$\hat{A}_i = \frac{r_i - \operatorname{mean}(r_1, \dots, r_G)}{\operatorname{std}(r_1, \dots, r_G)}$$

This $\hat{A}_i$ is called the **advantage** — the value of how much better this response was than the other attempts at the same question.

> **[Figure 11.2]** GRPO's group-relative advantage. Bars for the rewards $r_i$ of $G$ responses sampled on the same question, with the group mean drawn as a horizontal baseline. Responses above the line have positive advantage (generation probability ↑), those below negative (probability ↓), colored differently — showing how relative standing is obtained from the group mean alone, with no separate value model.

The objective raises the generation probability of responses with positive advantage and lowers that of negative ones:

$$J_{\text{GRPO}}(\theta) = \mathbb{E}\left[ \frac{1}{G} \sum_{i=1}^{G} \frac{\pi_\theta(o_i \mid q)}{\pi_{\theta_\text{old}}(o_i \mid q)}\, \hat{A}_i \right] - \beta\, D_{\text{KL}}\big(\pi_\theta \,\big\|\, \pi_\text{ref}\big)$$

The probability ratio in the first term corrects for updating the current policy $\pi_\theta$ with data generated by the sampling-time policy $\pi_{\theta_\text{old}}$; the full objective clips this ratio to a fixed range so that one update cannot move the policy abruptly. The second term is a regularizer keeping the policy from drifting too far from a reference model $\pi_\text{ref}$ (usually the model at the start of reinforcement learning), weighted by $\beta$. Because the group mean serves as the baseline, no separate value model of the kind required by other policy-gradient algorithms (PPO) is needed, and training cost drops accordingly. The structure of sampling several responses to one question is the same as self-consistency (→ 2.5) with a different use: at inference time the bundle yields an answer by majority vote, at training time the bundle's reward differences become the learning signal. The derivation of the objective and the training details are left to the presentation.

In the reported results the model exhibited behavior it was never taught: responses grew longer, and verification, reflection, and the exploration of alternatives appeared inside them. This is emergence (→ 2.3) — an absent ability appearing past a threshold of scale and conditions — observed here along the training axis. The released R1 combined a small supervised stage to remedy R1-Zero's poor readability.

## 11.6 The Limits of Reward, and Distillation

What reinforcement learning delivers extends exactly as far as what is written in the reward.

First, properties not put into the reward are not obtained, and loopholes in the reward that is put in are exploited. The former is illustrated by R1-Zero's poor readability: readability was not in the reward, so it was not obtained. The latter is called **reward hacking** — optimizing the loopholes of the reward function instead of the intended ability, raising the score alone. A concrete example: a coding agent rewarded for test passage that special-cases the test inputs in its code passes the tests without solving the task. The design of rewards and measurements is treated in Chapter 13 (evaluation & benchmarks).

Second, the ability of a trained reasoning model can be transferred by supervised learning. **Distillation** is supervised fine-tuning of a small model on data generated by a large model. The R1 paper reports that fine-tuning small open models on reasoning text generated by R1 transfers a substantial part of the reasoning ability without any reinforcement learning. The structure — a model produces the data, supervised learning consumes it — is the same as STaR, with the generator changed from the model itself to a stronger model.

## 11.7 Summary

The methods of Chapter 2 held the weights fixed and had the caller invest computation. This chapter put that capability into the weights. From the user's perspective, a reasoning model is a model that has internalized the procedure of repetition and selection, and the amount of thinking is a billable resource adjusted by the thinking budget. From the builder's perspective, the starting point is the absence of data: demonstrations of long solutions do not exist, while outcome correctness is judged automatically. STaR therefore filters self-generated solutions by the outcome verdict and trains on them by supervised learning; to pass beyond that ceiling of imitation, reinforcement learning optimizes the outcome reward directly. On verifiable rewards (RLVR), R1 obtained the emergence of long reasoning through unconstrained exploration, and the obtained ability transfers to small models by distillation. The limit — properties not written into the reward are not obtained — leads into the problem of evaluation and reward design (→ Ch. 13).

**Presentation.** STaR (Zelikman et al., 2022) — bootstrapping from self-generated solutions, rationalization. DeepSeek-R1 (DeepSeek-AI, 2025) — long reasoning emerging from pure reinforcement learning, GRPO. Both are heard through one question: what stands in for the label or the reward, and what collapses without it.

**Lab.** Thinking-budget measurement (planned): vary a reasoning model's thinking budget on a fixed evalset and measure the accuracy–cost curve of 11.1 directly; source material `anthropic-cookbook/extended_thinking`. Details are finalized in the post-midterm lab rework.
