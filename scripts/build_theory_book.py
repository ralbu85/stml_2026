#!/usr/bin/env python3
"""이론 노트 16장을 한 파일로 합쳐 lectures/이론_전체.md 를 생성한다.

- 각 장 제목(H1)을 H2로 내려 문서 전체가 하나의 H1을 갖게 한다.
- 상단에 장별 점프 링크(문서 내 앵커)와 원본 notes.md·slides.md 링크를 단다.
- 원본은 lectures/weekNN/notes.md 이며, 이 파일은 재생성 산출물이다.

실행: python scripts/build_theory_book.py
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LECT = ROOT / "lectures"
OUT = LECT / "이론_전체.md"
WEEKS = [f"{i:02d}" for i in range(1, 17)]


def demote_headings(text: str) -> str:
    """마크다운 헤딩을 한 단계 내린다(# → ##). 코드펜스 안은 건드리지 않는다."""
    lines, in_fence, out = text.splitlines(), False, []
    for ln in lines:
        if ln.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append(ln)
            continue
        if not in_fence and re.match(r"^#{1,5} ", ln):
            out.append("#" + ln)
        else:
            out.append(ln)
    return "\n".join(out)


def h1_title(text: str) -> str:
    for ln in text.splitlines():
        if ln.startswith("# "):
            return ln[2:].strip()
    return "(제목 없음)"


def main() -> None:
    chapters = []
    for w in WEEKS:
        note = LECT / f"week{w}" / "notes.md"
        if not note.exists():
            continue
        raw = note.read_text(encoding="utf-8")
        chapters.append((w, h1_title(raw), raw))

    parts = []
    parts.append("# 이론 강의 전체 — LLM 에이전트 특론 (2026)\n")
    parts.append(
        "> 16개 장 이론 노트를 한 파일로 모은 합본이다. 원본은 각 `lectures/weekNN/notes.md`이며,\n"
        "> 이 파일은 `scripts/build_theory_book.py`로 재생성한다(원본을 고치면 다시 실행).\n"
    )

    # 목차
    parts.append("## 목차\n")
    parts.append("| 장 | 제목 | 원본 | 슬라이드 |")
    parts.append("|---|---|---|---|")
    for w, title, _ in chapters:
        num = title.split(".", 1)[0]
        parts.append(
            f"| {num} | [{title}](#ch{w}) | "
            f"[notes](week{w}/notes.md) | [slides](week{w}/slides.md) |"
        )
    parts.append("")

    # 본문
    for w, title, raw in chapters:
        parts.append(f'<a id="ch{w}"></a>\n')
        parts.append(f"> 원본: [`lectures/week{w}/notes.md`](week{w}/notes.md) · "
                     f"슬라이드: [`week{w}/slides.md`](week{w}/slides.md) · "
                     "[▲ 목차](#목차)\n")
        parts.append(demote_headings(raw).strip())
        parts.append("\n---\n")

    OUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"wrote {OUT}  ({len(chapters)}장, {OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
