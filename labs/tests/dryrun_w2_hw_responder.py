"""Canned responder for the W2 evalset homework dry-run (stdlib only)."""


def responder(model=None, messages=None, **kw):
    text = " ".join(str(m.get("content", "")) for m in (messages or []))
    cot = "step" in text.lower()
    if "Reply with exactly: ready" in text:
        return "ready"
    if "in 2 days" in text and "Wednesday" in text:
        return "ANSWER: Friday"
    if "3 days ago" in text and "Saturday" in text:
        return "ANSWER: Wednesday"
    if "45 days" in text and "Monday" in text:
        if cot:
            return "45 days is 6 weeks and 3 days. Monday + 3 = Thursday.\nANSWER: Thursday"
        return "ANSWER: Sunday"
    return "ANSWER: unknown"
