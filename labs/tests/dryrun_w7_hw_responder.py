"""Canned responder for the W7 own-topic homework dry-run (stdlib only)."""

import json

REPORT = "\n".join([
    "## Overview",
    "Test-time compute buys accuracy with more predictions at answer time "
    "(https://arxiv.org/abs/2401.00001). Self-consistency samples several paths "
    "and votes; search methods branch and prune. Agent loops multiply these costs "
    "per step, so budget policies matter (https://arxiv.org/abs/2402.00002).",
    "## Evidence",
    "Benchmark studies report diminishing returns past moderate sample counts, "
    "and compute-optimal allocation beats fixed budgets on hard items "
    "(https://arxiv.org/abs/2403.00003). Cost grows linearly in samples while "
    "accuracy saturates, which argues for routing only hard questions to large "
    "budgets. Reported gains concentrate on multi-step reasoning benchmarks "
    "rather than single-fact recall, matching the mechanism: extra predictions "
    "help exactly where intermediate steps can go wrong and be caught.",
    "## Open Questions",
    "How should budgets adapt online per question? Which verifier signals are "
    "reliable enough to prune early? How do these trades change for tool-using "
    "agents whose steps have side effects?",
])


def responder(model=None, messages=None, **kw):
    text = " ".join(str(m.get("content", "")) for m in (messages or []))
    if "Reply with exactly: ready" in text:
        return "ready"
    if "Reply with a JSON list of step strings" in text or "JSON list of step" in text:
        return json.dumps(["research the topic", "draft the report", "edit the report"])
    if "SCORE:" in text:
        return "Well grounded and structured.\nSCORE: 4"
    if "Return numbered, actionable feedback" in text:
        return ("1. Tighten the overview paragraph. 2. Name the benchmarks "
                "explicitly. 3. Keep every URL in the revision.")
    if "Revise the report" in text:
        return REPORT + "\n\n(The revision names benchmarks explicitly and keeps all URLs.)"
    if "Write a research report" in text:
        return REPORT
    return "Canned reply for the offline dry-run."
