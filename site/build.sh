#!/usr/bin/env bash
# build.sh — render the STML course website into site/_site.
#
# Release model: every week page is public and shows that week's topic and
# presentation papers from the day the site goes up; the materials themselves
# (lecture notes, slides, lab notebook) are released week by week. PUBLISH_WEEKS
# below is the single switch — a week not listed there has no material file
# copied into _site at all, so nothing is reachable by guessing a URL.
#
# To open a week: add its number to PUBLISH_WEEKS, move its weekNN-notes.qmd
# page out of _unpublished/ into this directory, replace the "published before
# class" rows of weekNN.qmd with links, and re-run this script.
#
# Notebooks are published as downloadable .ipynb only. Students upload them to
# Colab themselves, so no notebook link depends on a hosted copy of this repo.
set -euo pipefail
cd "$(dirname "$0")"

PUBLISH_WEEKS="01"
published() { case " $PUBLISH_WEEKS " in *" $1 "*) return 0;; *) return 1;; esac; }

# Built from scratch: the gate is only trustworthy if a week dropped from
# PUBLISH_WEEKS also disappears from the output of the next build.
rm -rf _site
rm -f _week*-notes-en.md

# API guide: strip the H1 (the page adds its own title), fix the README link.
sed '1{/^# /d}' ../labs/API_SETUP.md \
  | sed 's|\[labs/README.md\](README.md)|the lab README in the course repo|' \
  > _api-setup-content.md

# Lecture notes (English) → included by weekNN-notes.qmd pages.
for d in ../lectures/week*/; do
  nn="$(basename "$d")"; nn="${nn#week}"
  published "$nn" || continue
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
mkdir -p _site/figures
for d in ../lectures/week*/figures; do
  [ -d "$d" ] || continue
  nn="$(basename "$(dirname "$d")")"; nn="${nn#week}"
  published "$nn" || continue
  cp "$d"/* _site/figures/
done

# Lab and homework notebooks: downloadable .ipynb, plus the data files the
# notebooks fetch at runtime.
mkdir -p _site/labs/data
for d in ../lectures/week*/; do
  nn="$(basename "$d")"; nn="${nn#week}"
  published "$nn" || continue
  cp "$d"/W*_lab_*.ipynb "$d"/W*_hw_*.ipynb _site/labs/ 2>/dev/null || true
done
cp ../labs/data/*.csv _site/labs/data/ 2>/dev/null || true

# Lecture notes → downloadable PDF. LaTeX cannot read SVG, so figures are
# converted to PNG in a scratch copy of each note first.
PYBIN="$(cd .. && pwd)/labs/.venv/bin/python"
mkdir -p _site/notes
for d in ../lectures/week*/; do
  nn="$(basename "$d")"; nn="${nn#week}"
  published "$nn" || continue
  [ -f "$d/notes.en.md" ] || continue
  tmp="$(mktemp -d)"
  # drop image alt text: pandoc would turn it into a second, duplicate caption
  sed -e 's/^!\[[^]]*\](/![](/' -e 's/\.svg)/.png)/g' "$d/notes.en.md" > "$tmp/week$nn-notes.md"
  if [ -d "$d/figures" ]; then
    mkdir -p "$tmp/figures"
    cp "$d"/figures/*.png "$tmp/figures/" 2>/dev/null || true
    for f in "$d"/figures/*.svg; do
      [ -e "$f" ] || continue
      "$PYBIN" -c "import cairosvg,sys; cairosvg.svg2png(url=sys.argv[1], write_to=sys.argv[2], output_width=1600)" \
        "$f" "$tmp/figures/$(basename "$f" .svg).png"
    done
  fi
  quarto render "$tmp/week$nn-notes.md" --to pdf \
    -M pdf-engine:xelatex -M mainfont:"DejaVu Serif" -M sansfont:"DejaVu Sans" \
    -M monofont:"DejaVu Sans Mono" -M geometry:margin=25mm -M colorlinks:true \
    -M fontsize:11pt >/dev/null
  mv "$tmp/week$nn-notes.pdf" "_site/notes/"
  rm -rf "$tmp"
done

# Lecture decks (Beamer PDF), for every published week that has a slides.qmd.
for d in ../lectures/week*/; do
  week="$(basename "$d")"
  published "${week#week}" || continue
  [ -f "$d/slides.qmd" ] || continue
  quarto render "$d/slides.qmd" --to beamer
  mkdir -p "_site/lectures/$week"
  mv "$d/slides.pdf" "_site/lectures/$week/"
done

echo "built: $(pwd)/_site  (weeks published: $PUBLISH_WEEKS)"
