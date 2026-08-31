# Week 1 — review copies

Everything here is a copy, generated so the deck and the rules behind it can be
read without a browser or a build. Nothing here is a source file: editing these
changes nothing. Regenerate them by re-running `site/build.sh` and the PDF export
below.

| File | What it is |
|---|---|
| `slides.pdf` | The deck, one slide per page (31 pages: 30 + a blank export artifact). Exported from `slides.html`. |
| `slides-overview-1..3.png` | Every slide as a thumbnail, 12 per sheet — for judging flow and spotting overflow at a glance. |
| `style-guide.md` | Copy of `docs/style-guide.md`, the writing rules the deck and notes are held to. §8 is the review checklist. |

## Sources the Week 1 deck was written from

The chapter's argument and its structure come from two files in this repository:

- `../notes.en.md` — Chapter 1 itself (§1.1 observation → §1.2 control flow →
  §1.3 components → §1.4 autonomy → §1.5 form factor → §1.6 adoption →
  §1.7 course map → §1.8 discussion). The deck follows this order; the notes are
  the authority when the two disagree.
- `../../../docs/style-guide.md` — copied here as `style-guide.md`.

Two conventions the deck inherits from the notes and should be checked against them:

- The workflow/agent distinction and the term *control flow* follow Anthropic's
  *Building Effective Agents* (2024), cited in `notes.en.md` §1.2.
- The five workflow patterns table and the four-band autonomy table are taken
  from `notes.en.md` §1.4, unchanged in substance.

The named products on the band slides (Otter.ai, Granola, Zoom AI Companion,
Notion AI, Intercom Fin, Sierra, Zendesk, Claude Code, Cursor, Devin, GitHub
Copilot, Deep Research, Operator) were written from the model's own knowledge,
not from a source document in this repository. `notes.en.md` §1.4 names a subset
of them; the rest are additions and are worth a check before class.

## Regenerating

```
site/build.sh                       # slides.html + notes.html, in ../
google-chrome --headless --no-pdf-header-footer \
  --print-to-pdf=slides.pdf "file://$PWD/../slides.html?print-pdf"
```

Page count must equal slide count plus one blank. More than that means a slide
overflowed its frame — reveal does not shrink content the way Beamer did.
