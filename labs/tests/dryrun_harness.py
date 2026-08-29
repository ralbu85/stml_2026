"""Offline dry-run for lab notebooks: stub aisuite, skip pip cells, execute all cells.

Usage:
    .venv/bin/python tests/dryrun_harness.py <notebook.ipynb> <responder.py>

<responder.py> is a plain Python file defining `def responder(model=None, messages=None,
**kw) -> str`. Its full source is injected into the kernel together with the aisuite
stub, so it must be self-contained (stdlib only). The responder receives every
chat.completions.create call and returns the canned assistant content.

Exit code 0 = every cell executed without error.
"""

import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

STUB_SRC = '''
# MOCK: offline aisuite stub for instructor dry-runs. No real API call happens.
import sys as _sys, types as _types

def _install_aisuite_stub(_responder):
    _mod = _types.ModuleType("aisuite")

    class _Message:
        def __init__(self, content):
            self.content = content
            self.tool_calls = None

    class _Choice:
        def __init__(self, content):
            self.message = _Message(content)

    class _Usage:
        prompt_tokens = 100
        completion_tokens = 50
        total_tokens = 150

    class _Response:
        def __init__(self, content):
            self.choices = [_Choice(content)]
            self.usage = _Usage()

    class _Completions:
        def create(self, model=None, messages=None, **kw):
            return _Response(_responder(model=model, messages=messages, **kw))

    class _Chat:
        def __init__(self):
            self.completions = _Completions()

    class Client:
        def __init__(self, *a, **k):
            self.chat = _Chat()

    _mod.Client = Client
    _sys.modules["aisuite"] = _mod

_install_aisuite_stub(responder)
'''


def is_pip_cell(source: str) -> bool:
    stripped = source.lstrip()
    return stripped.startswith(("%pip", "!pip", "%%capture"))


def main(nb_path: str, responder_path: str) -> int:
    nb = nbformat.read(nb_path, as_version=4)

    for cell in nb.cells:
        if cell.cell_type == "code" and is_pip_cell(cell.source):
            cell.source = "pass  # pip install skipped in dry-run"

    responder_src = Path(responder_path).read_text()
    stub_cell = nbformat.v4.new_code_cell(responder_src + "\n" + STUB_SRC)
    stub_cell.pop("id", None)
    nb.cells.insert(0, stub_cell)

    client = NotebookClient(nb, timeout=180, kernel_name="python3",
                            allow_errors=False)
    try:
        client.execute()
    except Exception as exc:  # nbclient raises CellExecutionError with cell context
        print(f"DRY-RUN FAILED: {nb_path}\n{exc}")
        return 1

    print(f"DRY-RUN OK: {nb_path} ({len(nb.cells) - 1} cells)")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1], sys.argv[2]))
