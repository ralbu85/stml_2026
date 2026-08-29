"""Canned responder for the W4 loop-guard homework dry-run (stdlib only)."""


def _state(messages):
    user0 = next((m["content"] for m in (messages or []) if m.get("role") == "user"), "")
    obs = [str(m.get("content", "")) for m in (messages or [])
           if m.get("role") == "user" and str(m.get("content", "")).startswith("Observation:")]
    return user0, obs


def responder(model=None, messages=None, **kw):
    question, obs = _state(messages)
    if "Reply with exactly: ready" in question:
        return "ready"

    if "Verify very carefully" in question:
        # spinner: repeats the same lookup until a guard notice appears
        if any("guard" in o.lower() for o in obs):
            return ("Thought: The result is already above; ReAct is 2022.\n"
                    "Final Answer: 2022.")
        return ('Thought: I should verify the year again.\n'
                'Action: {"tool": "paper_lookup", "input": "react"}')

    if "How many years passed" in question:
        script = [
            'Thought: chain-of-thought first.\nAction: {"tool": "paper_lookup", "input": "chain-of-thought"}',
            'Thought: now Toolformer.\nAction: {"tool": "paper_lookup", "input": "toolformer"}',
            'Thought: subtract.\nAction: {"tool": "calculator", "input": "2023 - 2022"}',
            "Thought: one year.\nFinal Answer: 1 year (2022 to 2023).",
        ]
        return script[min(len(obs), len(script) - 1)]

    if "Which was published earlier" in question:
        script = [
            'Thought: Toolformer first.\nAction: {"tool": "paper_lookup", "input": "toolformer"}',
            'Thought: now chain-of-thought.\nAction: {"tool": "paper_lookup", "input": "chain-of-thought"}',
            "Thought: 2022 < 2023.\nFinal Answer: chain-of-thought (2022) came earlier.",
        ]
        return script[min(len(obs), len(script) - 1)]

    if "year was ReAct published" in question:
        return "Thought: catalog.\nFinal Answer: ReAct was published in 2022."
    if "authors of Toolformer" in question:
        return "Thought: catalog.\nFinal Answer: Schick et al. (2023)."
    if "self-consistency" in question:
        return "Thought: catalog.\nFinal Answer: Wang et al., published in 2022."
    return "Thought: proceeding.\nFinal Answer: done."
