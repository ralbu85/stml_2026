# Week 1 — original sources

Third-party material the Chapter 1 notes and deck were written against, copied
here so the claims can be checked without leaving the folder. None of it is
course-authored; each file carries a provenance header with its URL and the date
it was taken. Do not edit these — they are the record of what the originals say.

| File | Source | What Chapter 1 takes from it |
|---|---|---|
| `anthropic-building-effective-agents.md` | Anthropic, *Building Effective Agents* (Dec 2024) — [anthropic.com/engineering/building-effective-agents](https://www.anthropic.com/engineering/building-effective-agents) | The workflow/agent distinction and the term *control flow* (§1.2); the five workflow patterns table, verbatim in structure (§1.6). Its "When (and when not) to use agents" section is the basis of §1.6. |
| `msft-ai-agents-for-beginners-01-intro.md` | Microsoft, *AI Agents for Beginners*, lesson 1 | Cross-check on the agent definition and the components list (§1.2–1.3). |
| `msft-ai-agents-for-beginners-03-design-patterns.md` | Microsoft, *AI Agents for Beginners*, lesson 3 | Cross-check on the design-pattern vocabulary (§1.6). |
| `hf-agents-course-unit1-what-are-agents.md` | Hugging Face Agents Course, unit 1 | Cross-check on the agent definition and the loop (§1.2). |
| `hf-agents-course-unit1-what-are-llms.md` | Hugging Face Agents Course, unit 1 | Cross-check on the autoregressive-LLM definition (§1.2). |

The Figure 1.1 image is credited in the notes to P.-M. Dartus, *How LLMs Generate
Text for the Rest of Us* (2025), pm.dartus.fr. Only the image is used; the article
itself is not copied here.

## What has no source in this folder

The chapter's four-band autonomy table (§1.4) is course-authored — Anthropic's
article does not use these bands. So are the product placements on the band
walk: Otter.ai, Granola, Zoom AI Companion, Notion AI, Intercom Fin, Sierra,
Zendesk, Claude Code, Cursor, Devin, GitHub Copilot, Deep Research, Operator.
Those were written from the model's general knowledge, not from any document
here, and their product details are the part of Chapter 1 most likely to drift
or to be wrong. Check them before class.

## Refreshing

The Microsoft and Hugging Face files are copies from `materials/repos/`, which
`materials/fetch_materials.sh` re-clones. The Anthropic article was fetched with
`curl` and converted with `pandoc -f html -t gfm`, then trimmed to the article
body.
