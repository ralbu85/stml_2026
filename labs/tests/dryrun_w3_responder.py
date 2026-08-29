"""Canned responder for the W3 tools-lab dry-run (stdlib only).

The stub never executes tools, so every reply carries the marker string the
notebook's routing scorer falls back to when no tool trace is recorded.
"""


def responder(model=None, messages=None, **kw):
    text = " ".join(str(m.get("content", "")) for m in (messages or [])
                    if isinstance(m, dict))
    if "Reply with exactly: ready" in text:
        return "ready"
    if "17 * 23" in text:
        return "17 * 23 = 391."
    if "(144 + 6) / 3" in text:
        return "(144 + 6) / 3 = 50."
    if "ReAct" in text:
        return "According to the course catalog, ReAct was published in 2022 by Yao et al."
    if "Toolformer" in text:
        return "The Toolformer authors are Schick et al. (2023), per the course catalog."
    if "todo.txt" in text:
        return "I saved the note to todo.txt."
    if "function calling" in text:
        return ("Function calling is the protocol by which a model emits a structured "
                "request that client code parses, executes, and reinjects.")
    if "French" in text:
        return "Yes — 'agent' is a French word as well as an English one."
    if "reminders.txt" in text:
        return "I created reminders.txt with the reminder to call Daniel at 7PM."
    if "QR code" in text or "weather" in text:
        return "Current: 61F, High: 68F, Low: 51F. Files were requested via tools."
    if "unread emails from boss@email.com" in text:
        return ("Found 1 unread email from boss@email.com, marked it as read, "
                "and sent a polite follow-up.")
    if "Happy Hour" in text:
        return "I attempted to handle the Happy Hour email with the available tools."
    if "time is it" in text or "What time" in text:
        return "The current time is 14:03:22."
    return "Canned reply for the offline dry-run."
