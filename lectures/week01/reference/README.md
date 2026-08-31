# Week 1 — original sources

Third-party material the Chapter 1 notes and deck are written from, copied here
so every claim can be checked without leaving the folder. None of it is
course-authored; each file carries a provenance header with its URL and the date
it was taken. Do not edit these — they are the record of what the originals say.

| File | Source | What Chapter 1 takes from it |
|---|---|---|
| `anthropic-building-effective-agents.md` | Anthropic, *Building Effective Agents* (Dec 2024) — [link](https://www.anthropic.com/engineering/building-effective-agents) | The *agentic systems* umbrella and the workflow/agent definitions, quoted (§1.2). The agent-loop properties: environmental ground truth, stopping conditions (§1.2). The "simplest solution possible" rule (§1.4, §1.5). The five workflow patterns with their structures and examples (§1.5). Appendix 1's two domains — customer support and coding agents — which are §1.4's two cases. |
| `openai-practical-guide-to-building-agents.txt` (+ `.pdf`) | OpenAI, *A Practical Guide to Building Agents* (2025), 34 pp. | The three core components — Model, Tools, Instructions — quoted (§1.3). The three tool types: data, action, orchestration (§1.3). The three adoption conditions and the fraud-analysis illustration (§1.5). Orchestration patterns: single-agent, manager, decentralized (§1.6). The exclusion of chatbots, single-turn calls, and sentiment classifiers (§1.2, §1.4, §1.5). |
| `ng-agentic-ai-M1-intro-slides.txt` (+ `.pdf`) | Andrew Ng, *Agentic AI* (DeepLearning.AI), Module 1 — learner slides, 39 pp., from `materials/repos/agentic_ai_andrew/` | The zero-shot vs. agentic contrast and the "without using backspace" image, and the definition of an *agentic AI workflow* as multi-step execution (§1.1). **The position this chapter takes on the definition dispute** — degrees of agenticness rather than a true-agent argument (§1.2). The three bands, less / semi / highly autonomous (§1.4, Table 1.2). The easier-vs-harder task dimensions (§1.5). The four agentic design patterns that are this course's chapter structure (§1.7). |
| `smolagents-intro-agents.md` | Hugging Face, smolagents conceptual guide — [link](https://huggingface.co/docs/smolagents/conceptual_guides/intro_agents) | The levels-of-agency table with its code column, reproduced (§1.4, Table 1.3, Figure 1.3). The framing of agency as how far model output controls program flow, which is where this course's use of *control flow* comes from (§1.2). |
| `hf-agents-course-unit1-what-are-agents.md` | Hugging Face Agents Course, unit 1 | Cross-check on the agent definition and the loop. Reproduces the smolagents table in a five-row form. |
| `hf-agents-course-unit1-what-are-llms.md` | Hugging Face Agents Course, unit 1 | Cross-check on the autoregressive-LLM definition (§1.2). |
| `msft-ai-agents-for-beginners-01-intro.md` | Microsoft, *AI Agents for Beginners*, lesson 1 | Cross-check: agent as a system of environment / sensors / actuators; when to use agents. Its Russell–Norvig agent-type taxonomy is not used. |
| `msft-ai-agents-for-beginners-03-design-patterns.md` | Microsoft, *AI Agents for Beginners*, lesson 3 | Cross-check on design-pattern vocabulary. |

The Figure 1.1 image is credited in the notes to P.-M. Dartus, *How LLMs Generate
Text for the Rest of Us* (2025), pm.dartus.fr. Only the image is used.

## What is still course-authored

Where the sources conflict, §1.2 says so rather than choosing silently: Anthropic
treats workflow/agent as a binary, smolagents explicitly denies that it is one, and
they disagree on where routing sits. Ng's "different degrees" position is what the
chapter adopts to resolve it, and it is quoted where it is used.

Chapter 1 is written to follow these sources, but three things in it are the
course's own and have no source in this folder:

- **§1.1's opening observation** (Deep Research and Claude Code doing different
  work with the same model) — the course's framing device.
- **§1.7's deficit list and course arc** — about this course, so necessarily ours.
- **The chapter pointers** in the tables ("Appears in Ch. 7", etc.) and the
  treatment of **memory as a fourth component**. OpenAI names three components;
  memory is added because Anthropic's augmented LLM includes it and the loop
  requires it. The notes say so where it happens.

Where a source is quoted or its structure reproduced, §1.2–§1.6 name the source
in the text. Earlier drafts of this chapter placed a four-band autonomy table and
a list of named consumer products (Otter.ai, Granola, Zoom AI Companion, Notion
AI, Zendesk, and others) in §1.4; none of that came from a source and all of it
has been replaced by the smolagents levels and Anthropic's two documented
domains.

## Refreshing

The Microsoft and Hugging Face course files are copies from `materials/repos/`,
which `materials/fetch_materials.sh` re-clones. The Anthropic article and the
smolagents guide were fetched with `curl` and converted with
`pandoc -f html -t gfm`, then trimmed to the article body. The OpenAI guide is
the published PDF plus a `pdftotext -layout` extraction of it.
