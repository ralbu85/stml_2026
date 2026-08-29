"""Canned responder for the W1 notebook dry-run (stdlib only)."""

ANSWER_JSON = (
    '{"topic": "LLM agent methods", '
    '"answer": "A short single-sentence answer to the research question.", '
    '"difficulty": "intro"}'
)

JSON_TASK_MARKERS = (
    "PDF reports",
    "step by step",
)


def responder(model=None, messages=None, **kw):
    text = " ".join(m.get("content", "") for m in (messages or []))

    if "Reply with exactly: ready" in text:
        return "ready"
    if "Chain-of-Thought paper as JSON" in text:
        return '```json\n{"title": "Chain-of-Thought Prompting", "year": 2022}\n```'

    # §4 example — sentiment classifier
    if "Classify the sentiment" in text:
        return '{"label": "positive", "confidence": 0.93}'

    # §4 task / exercises — research questions under JSON_SYSTEM
    if any(marker in text for marker in JSON_TASK_MARKERS):
        return ANSWER_JSON

    # §2.2 statelessness
    if "What is my research topic?" in text and "maritime" not in text:
        return "I do not have that information from this conversation."

    return "A single-sentence canned reply for the offline dry-run."
