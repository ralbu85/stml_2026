"""Canned responder for the W3 new-tool homework dry-run (stdlib only).

The stub records no tool trace, so every reply carries the marker word the
scorer falls back to.
"""


def responder(model=None, messages=None, **kw):
    text = " ".join(str(m.get("content", "")) for m in (messages or []))
    if "Reply with exactly: ready" in text:
        return "ready"
    if "17 * 23" in text:
        return "17 * 23 = 391."
    if "(144 + 6) / 3" in text:
        return "(144 + 6) / 3 = 50."
    if "ReAct" in text:
        return "ReAct was published in 2022, per the course catalog."
    if "Toolformer" in text:
        return "The Toolformer authors are Schick et al., per the course catalog."
    if "function calling" in text:
        return "Function calling is the protocol by which a model emits a structured request that code executes."
    if "French" in text:
        return "Yes - 'agent' is a French word as well as an English one."
    if "Week 9" in text or "week 9" in text:
        return "Week 9 covers Retrieval-Augmented Generation."
    if "Week 8" in text or "week 8" in text:
        return "Week 8 is the midterm exam session."
    return "Canned reply for the offline dry-run."
