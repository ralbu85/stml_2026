# Week 2 — original sources

Third-party material the Chapter 2 notes are written from, copied here so
every claim can be checked without leaving the folder. None of it is
course-authored; each entry below names the source and what Chapter 2 takes
from it. Do not edit these — they are the record of what the originals say.

Andrew Ng's *Agentic AI* course (`materials/repos/agentic_ai_andrew/`), used
as a source for Week 1 and as this course's Week 3+ lab backbone, is not
listed here: none of its five modules (planning/research agent, reflection,
tool use, evals, multi-agent) covers prompting or reasoning technique, and
Chapter 2's notes cite it nowhere. Its own material starts at Week 3
(`docs/syllabus.md`, "Ng *Agentic AI* 모듈을 순서대로 연속 실행").

## Papers

| File | Source | What Chapter 2 takes from it |
|---|---|---|
| `wei-chain-of-thought_2201.11903.pdf` (+ `.txt`) | Wei et al., *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*, NeurIPS 2022 — arXiv:2201.11903 (also `papers/W02_Chain-of-Thought_2201.11903.pdf`, this week's presented paper) | The apples word-problem measurement, Figure 1 (§2.1–2.3, quoted almost verbatim). The definition and example form of CoT (§2.3). The emergence-with-scale claim (§2.3) — magnitudes and the scale curve are left to the student presentation. |
| `kojima-zeroshot-cot_2205.11916.pdf` (+ `.txt`) | Kojima et al., *Large Language Models are Zero-Shot Reasoners*, NeurIPS 2022 — arXiv:2205.11916 | Zero-shot CoT: the single added instruction ("Let's think step by step") as Method 1 of §2.3, contrasted with Wei et al.'s worked-example form. |
| `feng-cot-theory_2305.15408.pdf` (+ `.txt`) | Feng et al., *Towards Revealing the Mystery behind Chain of Thought: A Theoretical Perspective*, NeurIPS 2023 — arXiv:2305.15408 | One of the two candidate explanations in §2.2 for why a single prediction has a step ceiling: bounded-depth Transformers provably cannot solve certain sequential tasks without CoT (their circuit-complexity impossibility result). |
| `merrill-sabharwal-cot-expressive-power_2310.07923.pdf` (+ `.txt`) | Merrill & Sabharwal, *The Expressive Power of Transformers with Chain of Thought* — arXiv:2310.07923 | The same §2.2 claim from the complementary direction: a transformer's per-step computation is bounded by its depth (log-precision transformer / constant-depth results), so chaining steps requires writing them out rather than computing them in one pass. |
| `wang-self-consistency_2203.11171.pdf` (+ `.txt`) | Wang et al., *Self-Consistency Improves Chain of Thought Reasoning in Language Models*, ICLR 2023 — arXiv:2203.11171 | The definition of Self-Consistency and the "sample-and-marginalize" procedure, quoted (§2.5). The marginalization identity $P(a\mid q) = \sum_r P(a\mid r,q)P(r\mid q)$ is this paper's framing of why majority voting approximates the true answer distribution. |
| `yao-react_2210.03629.pdf` (+ `.txt`) | Yao et al., *ReAct: Synergizing Reasoning and Acting in Language Models*, ICLR 2023 — arXiv:2210.03629 (also `papers/W05_ReAct_2210.03629.pdf`, Week 5's presented paper) | The Apple Remote / HotpotQA failure case in Figure 1(1b) — CoT reasoning coherently from a hallucinated premise (§2.4). Note: the example dialogue is set inside the Figure 1 image, so it does not appear in the `.txt` text-layer extraction; it is legible in the PDF itself. |

## Course material (background reading and lab source)

| File | Source | What Chapter 2 / the lab takes from it |
|---|---|---|
| `anthropic-prompt-tutorial-06-precognition.ipynb` | Anthropic, *Prompt Engineering Interactive Tutorial*, ch. 6 "Precognition (Thinking Step by Step)" — `materials/repos/courses/prompt_engineering_interactive_tutorial/Anthropic 1P/` | Listed as this week's 보조읽기 (background reading, not a presentation source). The lab (`W2_lab_prompting.ipynb`) is adapted from this chapter's exercises for the zero-shot "think step by step" section. |
| `anthropic-prompt-tutorial-07-few-shot-examples.ipynb` | Anthropic, *Prompt Engineering Interactive Tutorial*, ch. 7 "Using Examples (Few-Shot Prompting)" | Same tutorial, following chapter. Source of the lab's few-shot exemplar exercise and the email-classification task cited in notes §2.8 (Lab). |
| `anthropic-prompt-tutorial-08-avoiding-hallucinations.ipynb` | Anthropic, *Prompt Engineering Interactive Tutorial*, ch. 8 "Avoiding Hallucinations" | Source of the lab's Section 7 (the "heaviest hippo" question, chain-of-thought run, and "giving an out"), which shows the hallucination limit of notes §2.4. |
| `anthropic-prompt-evaluations-03-code-graded.ipynb` | Anthropic, *Prompt Evaluations* course, lesson 3 "Code-Graded Evals" — `materials/repos/courses/prompt_evaluations/03_code_graded_evals/` | Source of the lab's code-graded eval structure (baseline → format fix → CoT prompt, target ≥ 11/12), referenced in notes §2.8 (Lab). |
| `berkeley-llm-reasoning.pdf` (+ `.txt`) | UC Berkeley CS294 (LLM Agents MOOC), `llm-reasoning.pdf` — `materials/repos/llm-agents-mooc/slides/` | Listed as this week's 보조읽기 (`weeks/week02.md`, `docs/lecture-outlines.md`). Not quoted in the notes; background depth on reasoning research beyond what the chapter covers. |
| `berkeley-inference-time-techniques.pdf` (+ `.txt`) | UC Berkeley CS294 (LLM Agents MOOC), `inference_time_techniques_lecture_sp25.pdf` — same repo | Background for §2.6 (test-time compute / inference-time scaling table): Best-of-N, tree search, and the verifier concept beyond what majority voting needs. |

## What is still course-authored

Chapter 2 is written to follow the papers above, but these parts are the
course's own and have no source in this folder:

- **§2.1's framing** — casting the chapter as repairing the one deficit from
  Chapter 1 that cannot be delegated outward (decision quality itself), and
  the "same model, different accuracy" framing device.
- **§2.6's product mapping** — connecting test-time compute to current chat
  products' "thinking" toggles and subscription tiers (OpenAI o-series,
  Claude extended thinking, Gemini thinking models, o1 pro / Gemini Deep
  Think / Grok Heavy). No single source states this mapping; it is the
  course's own reading of public vendor documentation.
- **The chapter pointers** ("→ Ch. 3", "→ Ch. 11", etc.) and **§2.7's
  summary** connecting this chapter's open threads (hallucination, reasoning
  moved into the weights) to where later chapters close them.
- **§2.8's discussion questions** — course-authored exercises applying the
  chapter's concepts to new scenarios.

Where a source is quoted or its structure reproduced, §2.1–§2.6 name the
source in the text (Wei et al., Kojima et al., Feng et al., Merrill &
Sabharwal, Wang et al., Yao et al.).

## Refreshing

The papers were fetched from arXiv (`arxiv.org/pdf/<id>`); the Anthropic
notebooks and Berkeley PDFs are copies from `materials/repos/`, which
`materials/fetch_materials.sh` re-clones. Each PDF's `.txt` sidecar is a
`pdftotext -layout` extraction, kept for grep-ability — the PDF is the
authoritative copy.
