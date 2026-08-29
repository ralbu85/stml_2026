# Labs — Colab-native, self-contained, Ng-core (v10.1, 2026-08)

Every first-half lab and homework (W1–W7) follows a single standard:

1. **Runtime = Google Colab, one self-contained notebook per week.** A student opens the
   notebook straight from the course site's **Open in Colab** link, pastes their API key
   into the setup cell (plain string, replacing `PASTE-YOUR-KEY-HERE`; the key is the
   student's own responsibility), and runs top to bottom. No repo clone, no shared
   library import, no local files, no Colab Secrets. When a later week genuinely needs
   data or a package, the notebook fetches it in its own setup cell.
2. **Core material = Andrew Ng, *Agentic AI* (DeepLearning.AI)** —
   `materials/repos/agentic_ai_andrew`. Weeks 1–2 are prompting practice matched to
   those weeks' theory; from W3 the Ng module labs are used nearly as given, adapted
   only for Colab (aisuite setup, inlined helpers, GitHub-raw data URLs) with prose
   rewritten to course register and a measured improvement layer added. The W4 loop lab
   is course-built (Hugging Face Agents Course unit 1 pattern). The source is credited
   in each notebook header.
3. **Standard shape (80 minutes of real work):** learning outcome → setup (install +
   paste key + helpers, ~3 cells) → observation cells (reproduce the failure that
   motivates the build) → fill-ins between `### FILL IN (START/END) ###` markers →
   **measured improvement task with a numeric target** → exercises in
   predict → run → check form, including one trade-off exercise → print-only PASS/FAIL
   completion checklist. Grading checks structure (prompts written, shapes returned,
   target reached), never content quality.
   Scoring/judge plumbing that is not itself the week's lesson is hidden in collapsed
   Colab form cells (`#@title … { display-mode: "form" }`); kept visible where
   evaluation IS the lesson (W2 measurement loop, W5 evals part).
4. **API access:** `aisuite` only, model selected by one `MODEL` string
   (`openai:gpt-4o-mini` default, `anthropic:claude-haiku-4-5` alternative). Key issuing
   and safety: [`API_SETUP.md`](API_SETUP.md).
5. **Homework thread (W2–W7):** each week ships a small graded homework in the same
   format — Goal header, requirements, numbered hints, runnable starter fill-ins,
   PASS/FAIL completion cell — due before the next class.
6. **Reference answers:** `checkpoints/weekNN/solution.py` (labs and homework),
   published after each week. Falling behind means pasting the reference prompts and
   continuing.

## Status

| Week | Lab · Homework | Core source | State |
|---|---|---|---|
| 1 | [`W1_lab_setup.ipynb`](../lectures/week01/W1_lab_setup.ipynb) — first calls; roles, statelessness, temperature; core task: a system prompt that forces clean JSON answers (PASS/FAIL) | prompting practice | ✅ |
| 2 | [`W2_lab_prompting.ipynb`](../lectures/week02/W2_lab_prompting.ipynb) — step-by-step thinking + few-shot exemplars + a code-graded eval (CoT ≥ 11/12, email classification 4/4), self-consistency · hw [`W2_hw_build_evalset.ipynb`](../lectures/week02/W2_hw_build_evalset.ipynb) — own 8-item evalset, CoT beats answer-only ≥ 7/8 | Anthropic *Prompt Eng. Interactive Tutorial* ch. 6–7 + *Prompt Evaluations* lesson 3 (near-verbatim) | ✅ |
| 3 | [`W3_lab_tools.ipynb`](../lectures/week03/W3_lab_tools.ipynb) — functions into tools, docstring schemas, routing taskset ≥ 6/8, email assistant · hw [`W3_hw_new_tool.ipynb`](../lectures/week03/W3_hw_new_tool.ipynb) — schedule-lookup tool + 2 routing tasks ≥ 7/8 | Ng M3 (near-verbatim) | ✅ |
| 4 | [`W4_lab_loop.ipynb`](../lectures/week04/W4_lab_loop.ipynb) — the agent loop by hand, Judge parser fill-in, Act-only vs ReAct on a 5-item mini evalset, trace reading, step bound · hw [`W4_hw_loop_guard.ipynb`](../lectures/week04/W4_hw_loop_guard.ipynb) — repetition guard + 2 own multi-hop questions | course-built (HF Agents Course unit 1 pattern) | ✅ |
| 5 | [`W5_lab_reflection_evals.ipynb`](../lectures/week05/W5_lab_reflection_evals.ipynb) — draft → critique → revise on an essay, then evalsets, LLM-judge, error analysis, prompt iteration to a numeric target · hw [`W5_hw_chart_reflection.ipynb`](../lectures/week05/W5_hw_chart_reflection.ipynb) — reflection where the critique reads a rendered chart image | Ng M2 + M4 (merged, near-verbatim) | ✅ |
| 6 | [`W6_lab_multiagent.ipynb`](../lectures/week06/W6_lab_multiagent.ipynb) — plan → reflect → execute → explain over a DuckDB store, tool-only plans, 6-request taskset ≥ 5/6 · hw [`W6_hw_new_intent.ipynb`](../lectures/week06/W6_hw_new_intent.ipynb) — a new exchange intent end to end, 4/4 | Ng M5 (near-verbatim) | ✅ |
| 7 | [`W7_lab_research_agent.ipynb`](../lectures/week07/W7_lab_research_agent.ipynb) — planner → research → writer → editor, arXiv/Wikipedia keyless tools, checklist + judge ≥ 4/5 · hw [`W7_hw_own_topic.ipynb`](../lectures/week07/W7_hw_own_topic.ipynb) — own research topic + 2 self-designed checks | Ng final project (GL-M5) | ✅ |
| 9–10 | retriever · memory · graph integration (course-specific, final project) | — | pending |
| 11–13 | routing + cost logging · eval harness · guardrails + red team | — | pending |

`tests/` holds the offline validation harness (below). `docqa/`, `utils.py`, and the
`data/` evalsets are infrastructure for the second-half labs (W9–13); notebooks load
data by URL, never from a local checkout.

## Grading homework submissions (instructors)

Students submit the executed `.ipynb` (outputs saved) through the LMS. Download all
submissions into one folder and run:

```bash
python3 tests/grade_hw.py submissions/week03/ --out grades_w03.csv
```

No API key, no re-execution: the script reads each notebook's saved completion-cell
output (PASS/FAIL rows, HOMEWORK COMPLETE line, score lines) and writes one CSV row
per submission. Submissions are matched to their homework by the notebook's H1 title,
so LMS-renamed files are fine. Integrity flags mark what to open by hand:
`NO_OUTPUT` (never run), `FILLIN_UNCHANGED` (starter untouched — pasted outputs),
`COMPLETION_NOT_LAST` (edited after the check), `NO_COMPLETION_CELL`, `PARSE_ERROR`.
Flags are smoke-level by design; spot-check flagged files only.

## Authoring environment (instructors)

Notebooks are authored in this repo and validated without a key by stubbing the
`aisuite` client in-kernel. Full sweep (all 13 first-half notebooks):

```bash
cd labs && bash tests/dryrun_all.sh
```

Single notebook: `cd labs && .venv/bin/python tests/dryrun_harness.py
../lectures/weekNN/<notebook>.ipynb tests/dryrun_wN_responder.py`. For weeks that need
real execution, `labs/.venv` (Python 3.12) exists for local runs:

```bash
cd labs && uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python aisuite langgraph numpy requests pytest
```
