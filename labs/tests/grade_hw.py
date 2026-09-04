#!/usr/bin/env python3
"""Grade homework submissions: by default from their SAVED outputs; with --rerun, by
re-executing every submission with the grader's own API key first.

Students run the notebook top to bottom in Colab and upload the .ipynb to the LMS.
Download all submissions into one folder, then:

    python3 tests/grade_hw.py submissions/week02/ --out grades_w02.csv                  # saved outputs
    OPENAI_API_KEY=sk-... .venv/bin/python tests/grade_hw.py submissions/week02/ \
        --rerun --rerun-dir rerun_w02/ --out grades_w02.csv                             # re-executed

--rerun strips every output, replaces the student's key line with the grader's
environment key, skips the pip cell, runs the notebook top to bottom in a local
kernel (labs/.venv, which has aisuite installed), saves the executed copy under
--rerun-dir, and grades that copy. Saved outputs in the submission are ignored, so
an edited output cannot pass. --model forces one model for every submission.

Each submission is matched to its shipped notebook (collected lab or homework) by
the H1 title in its first cell (LMS-renamed files are fine). The completion cell's
saved PASS/FAIL rows and LAB COMPLETE / HOMEWORK COMPLETE line become the grade
row, together with the "submitted by:" identity line that collected labs print; cheap integrity flags mark notebooks
that need a manual look. Grading stays what the course promises: structural smoke
checks, never content quality.

Flags:
    NO_COMPLETION_CELL   no completion cell found (wrong/duplicated file)
    NO_OUTPUT            completion cell was never run
    FILLIN_UNCHANGED     every fill-in block is byte-identical to the starter
    FILLIN_MARKERS_GONE  fill-in markers missing (cannot compare to starter)
    COMPLETION_NOT_LAST  cells were run after the completion check
    PARSE_ERROR          file is not a readable notebook
    RERUN_FAILED:<err>   the notebook could not be re-executed (--rerun)
"""

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

KEY_LINE_RE = re.compile(r'^(\s*)os\.environ\["(OPENAI|ANTHROPIC)_API_KEY"\]\s*=\s*.*$', re.M)
MODEL_LINE_RE = re.compile(r'^MODEL\s*=\s*"[^"]*"', re.M)

FILLIN_RE = re.compile(r"### FILL IN \(START\) ###(.*?)### FILL IN \(END\) ###", re.S)
ROW_RE = re.compile(r"^(PASS|FAIL)\b\s*(.*)$", re.M)
IDENTITY_RE = re.compile(r"^submitted by:\s*(.+?)\s*$", re.M)
COMPLETE_WORDS = ("HOMEWORK COMPLETE", "LAB COMPLETE")
SCORE_RE = re.compile(r"^([A-Za-z][\w ./()-]{0,28}?):?\s+(\d+\s*/\s*\d+)\s*(?:\(.*\))?\s*$", re.M)


def cell_source(cell):
    return "".join(cell.get("source", []))


def cell_output_text(cell):
    parts = []
    for out in cell.get("outputs", []):
        if out.get("output_type") == "stream":
            parts.append("".join(out.get("text", [])))
        elif out.get("output_type") in ("execute_result", "display_data"):
            parts.append("".join(out.get("data", {}).get("text/plain", [])))
    return "\n".join(parts)


def h1_of(nb):
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "markdown":
            for line in cell_source(cell).splitlines():
                if line.startswith("# "):
                    return line.strip()
    return ""


def fillin_blocks(nb):
    src = "\n".join(cell_source(c) for c in nb.get("cells", []) if c.get("cell_type") == "code")
    return [re.sub(r"\s+", " ", b).strip() for b in FILLIN_RE.findall(src)]


def completion_cell(nb):
    found = None
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        src = cell_source(cell)
        if ("completion = {" in src or "checks = {" in src) and any(w in src for w in COMPLETE_WORDS):
            found = cell   # keep the last match
    return found


def rerun_notebook(path, rerun_dir, model=None, timeout=900):
    """Submission path -> executed copy (dict), run with the grader's environment key."""
    import nbformat
    from nbclient import NotebookClient

    nb = nbformat.read(path, as_version=4)
    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        cell.outputs = []
        cell.execution_count = None
        src = cell.source
        if src.lstrip().startswith(("%pip", "!pip")):
            src = "pass  # pip skipped: the grader's environment has the packages"
        src = KEY_LINE_RE.sub(r"\1pass  # key comes from the grader's environment", src)
        if model:
            src = MODEL_LINE_RE.sub(f'MODEL = "{model}"', src)
        cell.source = src
    NotebookClient(nb, timeout=timeout, kernel_name="python3", allow_errors=True).execute()
    rerun_dir.mkdir(parents=True, exist_ok=True)
    out = rerun_dir / path.name
    nbformat.write(nb, out)
    return json.loads(nbformat.writes(nb))


def load_refs(lectures_dir):
    refs = {}
    paths = sorted(Path(lectures_dir).glob("week*/W*_hw_*.ipynb")) + sorted(Path(lectures_dir).glob("week*/W*_lab_*.ipynb"))
    for path in paths:
        nb = json.load(open(path))
        refs[h1_of(nb)] = {"name": path.stem, "fillins": fillin_blocks(nb)}
    return refs


def grade_one(path, refs, rerun_dir=None, model=None):
    row = {"file": path.name, "homework": "?", "student": "", "complete": "?", "rows": "",
           "failed": "", "scores": "", "flags": []}
    try:
        nb = json.load(open(path))
        assert isinstance(nb.get("cells"), list)
    except Exception:
        row["flags"] = ["PARSE_ERROR"]
        return row
    if rerun_dir is not None:
        try:
            nb = rerun_notebook(path, rerun_dir, model=model)
        except Exception as exc:
            row["flags"] = [f"RERUN_FAILED:{type(exc).__name__}"]
            return row

    ref = refs.get(h1_of(nb))
    if ref is None:   # fallback: match shipped notebook name inside the LMS filename
        ref = next((r for r in refs.values() if r["name"] in path.name), None)
    row["homework"] = ref["name"] if ref else "UNKNOWN"

    comp = completion_cell(nb)
    if comp is None:
        row["flags"].append("NO_COMPLETION_CELL")
        return row

    text = cell_output_text(comp)
    if not text.strip():
        row["flags"].append("NO_OUTPUT")
    else:
        rows = ROW_RE.findall(text)
        n_pass = sum(1 for status, _ in rows if status == "PASS")
        row["rows"] = f"{n_pass}/{len(rows)}"
        row["failed"] = "; ".join(label.strip() for status, label in rows if status == "FAIL")[:120]
        row["complete"] = "NO" if "NOT COMPLETE YET" in text else (
            "YES" if any(w in text for w in COMPLETE_WORDS) else "?")
        identity = IDENTITY_RE.search(text)
        row["student"] = identity.group(1)[:60] if identity else ""

    # score lines ("improved score: 7/8", "core: 4/5") from every cell's saved output
    scores = []
    for cell in nb.get("cells", []):
        for label, frac in SCORE_RE.findall(cell_output_text(cell)):
            entry = f"{label.strip()} {frac.replace(' ', '')}"
            if not label.startswith(("PASS", "FAIL")) and entry not in scores:
                scores.append(entry)
    row["scores"] = "; ".join(scores[:6])

    if ref and ref["fillins"]:
        student = fillin_blocks(nb)
        if len(student) != len(ref["fillins"]):
            row["flags"].append("FILLIN_MARKERS_GONE")
        elif student == ref["fillins"]:
            row["flags"].append("FILLIN_UNCHANGED")

    counts = [c.get("execution_count") for c in nb["cells"]
              if c.get("cell_type") == "code" and c.get("execution_count")]
    if counts and comp.get("execution_count") and comp["execution_count"] < max(counts):
        row["flags"].append("COMPLETION_NOT_LAST")
    return row


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("paths", nargs="+", help="submission .ipynb files or folders of them")
    ap.add_argument("--refs", default=None, help="lectures/ dir with the shipped lab/homework notebooks")
    ap.add_argument("--out", default=None, help="write the result as CSV to this path")
    ap.add_argument("--rerun", action="store_true",
                    help="re-execute each submission with the key in OPENAI_API_KEY / ANTHROPIC_API_KEY before grading")
    ap.add_argument("--rerun-dir", default="rerun", help="where the executed copies are written (with --rerun)")
    ap.add_argument("--model", default=None, help='with --rerun: force this MODEL string, e.g. "openai:gpt-4o-mini"')
    args = ap.parse_args()
    rerun_dir = None
    if args.rerun:
        if not (os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")):
            sys.exit("--rerun needs OPENAI_API_KEY or ANTHROPIC_API_KEY in the environment")
        rerun_dir = Path(args.rerun_dir)

    repo = Path(__file__).resolve().parent.parent.parent
    refs = load_refs(Path(args.refs) if args.refs else repo / "lectures")
    if not refs:
        sys.exit("no reference notebooks found — pass --refs <repo>/lectures")

    files = []
    for p in map(Path, args.paths):
        files += sorted(p.glob("*.ipynb")) if p.is_dir() else [p]
    if not files:
        sys.exit("no .ipynb submissions found")

    rows = [grade_one(f, refs, rerun_dir=rerun_dir, model=args.model) for f in files]

    widths = {k: max(len(k), *(len(str(r[k] if k != "flags" else ",".join(r[k]))) for r in rows))
              for k in ("file", "homework", "student", "complete", "rows", "flags")}
    header = "  ".join(k.upper().ljust(widths[k]) for k in widths)
    print(header + "\n" + "-" * len(header))
    for r in rows:
        print("  ".join(str(r[k] if k != "flags" else ",".join(r[k]) or "-").ljust(widths[k])
                        for k in widths))
    n_ok = sum(1 for r in rows if r["complete"] == "YES" and not r["flags"])
    print(f"\n{len(rows)} submissions — {n_ok} complete and unflagged")

    if args.out:
        with open(args.out, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["file", "homework", "student", "complete", "rows", "failed", "scores", "flags"])
            for r in rows:
                w.writerow([r["file"], r["homework"], r["student"], r["complete"], r["rows"],
                            r["failed"], r["scores"], ",".join(r["flags"])])
        print(f"CSV written: {args.out}")


if __name__ == "__main__":
    main()
