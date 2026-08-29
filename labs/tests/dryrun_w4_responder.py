"""Canned responder for the W4 loop-lab dry-run (stdlib only).

Plays a scripted ReAct/Act-only agent: branches on the question in the first
user message, the protocol in the system message, and the number of
Observation turns so far.
"""


def _texts(messages):
    sys_txt = " ".join(m["content"] for m in (messages or []) if m.get("role") == "system")
    user0 = next((m["content"] for m in (messages or []) if m.get("role") == "user"), "")
    n_obs = sum(1 for m in (messages or [])
                if m.get("role") == "user" and str(m.get("content", "")).startswith("Observation:"))
    return sys_txt, user0, n_obs


def responder(model=None, messages=None, **kw):
    sys_txt, question, n_obs = _texts(messages)
    if "Reply with exactly: ready" in question:
        return "ready"
    if kw.get("tools"):   # section 2: the client's hidden loop; stub returns the final text
        return ("chain-of-thought (2022) was published earlier than Toolformer (2023), "
                "according to the catalog.")

    react = "Thought" in sys_txt
    guarded = "do not guess from memory" in sys_txt

    def turn(thought, rest):
        return (f"Thought: {thought}\n{rest}") if react else rest

    if "How many years passed" in question:
        script = [
            turn("I need chain-of-thought's year first.",
                 'Action: {"tool": "paper_lookup", "input": "chain-of-thought"}'),
            turn("Chain-of-thought is 2022. Now Toolformer's year.",
                 'Action: {"tool": "paper_lookup", "input": "toolformer"}'),
            turn("2023 and 2022; subtract.",
                 'Action: {"tool": "calculator", "input": "2023 - 2022"}'),
            turn("The difference is 1 year.",
                 "Final Answer: 1 year passed (2022 to 2023)."
                 if react else "Final Answer: yes"),
        ]
        return script[min(n_obs, len(script) - 1)]

    if "Which was published earlier" in question:
        script = [
            turn("Look up Toolformer.",
                 'Action: {"tool": "paper_lookup", "input": "toolformer"}'),
            turn("Toolformer is 2023. Now chain-of-thought.",
                 'Action: {"tool": "paper_lookup", "input": "chain-of-thought"}'),
            turn("2022 is earlier than 2023.",
                 "Final Answer: chain-of-thought (2022) came earlier than Toolformer (2023)."
                 if react else "Final Answer: yes"),
        ]
        return script[min(n_obs, len(script) - 1)]

    if "Reflexion" in question:
        if n_obs == 0:
            return turn("Try the catalog first.",
                        'Action: {"tool": "paper_lookup", "input": "reflexion"}')
        if guarded:
            return turn("The catalog does not contain it; say so.",
                        "Final Answer: the catalog does not contain Reflexion.")
        return turn("Not in the catalog, but I recall the paper.",
                    "Final Answer: 2021.")

    if "year was ReAct published" in question:
        return turn("The catalog gives ReAct's year.", "Final Answer: ReAct was published in 2022.")
    if "authors of Toolformer" in question:
        return turn("The catalog lists the authors.", "Final Answer: Schick et al. (2023).")
    if "self-consistency" in question:
        return turn("Look up self-consistency.",
                    "Final Answer: Wang et al., published in 2022.")

    return turn("Proceeding.", "Final Answer: done.")
