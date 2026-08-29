"""Canned responder for the W3 reflection-lab dry-run (stdlib only).

Branches on the prompt text of each stubbed chat.completions.create call:
- verification ping        -> "ready"
- judge request            -> per-criterion JSON scored from the submitted code
- reflection request       -> feedback JSON line + improved tagged chart code
- generation request       -> plain tagged chart code (no title/legend, so the
                              judge scores V1 low and the reflected V2 high)
Save paths are parsed from the "Save the figure as '...'" contract line.
"""

import json
import re

V1_CODE_TEMPLATE = """\
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

q1 = df[df["quarter"] == 1]
totals = q1.groupby("year")["price"].sum()
plt.figure()
totals.plot(kind="bar")
plt.savefig('{path}', dpi=100)
plt.close('all')
"""

V2_CODE_TEMPLATE = """\
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

q1 = df[df["quarter"] == 1]
totals = q1.groupby("year")["price"].sum()
plt.figure()
totals.plot(kind="bar")
plt.title("Q1 coffee sales by year")
plt.xlabel("Year")
plt.ylabel("Sales (currency units)")
plt.legend(["Q1 sales"])
plt.savefig('{path}', dpi=100)
plt.close('all')
"""


def _prompt_text(messages):
    content = messages[-1]["content"]
    if isinstance(content, list):
        return " ".join(part.get("text", "") for part in content
                        if isinstance(part, dict))
    return content


def _save_path(text, default):
    match = re.search(r"Save the figure as '([^']+)'", text)
    return match.group(1) if match else default


def responder(model=None, messages=None, **kw):
    text = _prompt_text(messages)

    if "Reply with exactly" in text:
        return "ready"

    if "You grade matplotlib plotting code" in text:
        rich = "plt.title" in text and "plt.legend" in text
        scores = {
            "data_slice": 1,
            "title": 1 if rich else 0,
            "axis_labels": 1 if rich else 0,
            "legend_readability": 1 if rich else 0,
            "matches_instruction": 1,
        }
        return json.dumps(scores)

    if '"feedback"' in text:  # reflection contract present
        path = _save_path(text, "chart_v2.png")
        feedback = json.dumps({"feedback": "V1 lacks a title, axis labels, "
                                           "and a legend; add all three."})
        return feedback + "\n<execute_python>\n" \
            + V2_CODE_TEMPLATE.format(path=path) + "</execute_python>"

    # default: V1 chart-code generation
    path = _save_path(text, "chart_v1.png")
    return ("<execute_python>\n" + V1_CODE_TEMPLATE.format(path=path)
            + "</execute_python>")
