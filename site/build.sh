#!/usr/bin/env bash
# build.sh — render the STML course website into site/_site.
# Everything is published; each week page shows the same four rows
# (lecture notes · slides · lab · papers) and links whatever exists in
# lectures/weekNN/: notes.en.md, slides.qmd (→ Beamer PDF), figures/.
# Lab and homework notebooks are NOT copied here — the week pages link them
# on GitHub (public repo), which is also what the Colab links open.
set -euo pipefail
cd "$(dirname "$0")"

# API guide: strip the H1 (the page adds its own title), fix the README link.
sed '1{/^# /d}' ../labs/API_SETUP.md \
  | sed 's|\[labs/README.md\](README.md)|the lab README in the course repo|' \
  > _api-setup-content.md

# Lecture notes (English) → included by weekNN-notes.qmd pages.
for d in ../lectures/week*/; do
  nn="$(basename "$d")"; nn="${nn#week}"
  [ -f "$d/notes.en.md" ] && cp "$d/notes.en.md" "_week${nn}-notes-en.md"
done

quarto render .

# Sample paper presentation (6-slide template exemplar, linked from presentations.qmd).
quarto render ../lectures/presentation-sample/slides.qmd --to revealjs
mkdir -p _site/lectures/presentation-sample
cp -r ../lectures/presentation-sample/slides.html \
      ../lectures/presentation-sample/slides_files \
      _site/lectures/presentation-sample/

# Figures referenced by the notes (lectures/weekNN/figures/).
rm -rf _site/figures
mkdir -p _site/figures
for d in ../lectures/week*/figures; do
  [ -d "$d" ] && cp "$d"/* _site/figures/
done

# Artifacts of retired formats left in _site by earlier builds.
rm -rf _site/lectures/week0? _site/lectures/week1? _site/labs
rm -f _site/week*-notes-ko.html

# Lecture decks (Beamer PDF), for every week that has a slides.qmd.
for d in ../lectures/week*/; do
  week="$(basename "$d")"
  [ -f "$d/slides.qmd" ] || continue
  quarto render "$d/slides.qmd" --to beamer
  mkdir -p "_site/lectures/$week"
  mv "$d/slides.pdf" "_site/lectures/$week/"
done

echo "built: $(pwd)/_site"
