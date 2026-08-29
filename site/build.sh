#!/usr/bin/env bash
# build.sh — render the STML course website into site/_site.
# Single-source layout per teaching week (lectures/weekNN/):
#   notes.en.md (THE lecture material — English only, no slides)
#   WN_lab_*.ipynb / WN_hw_*.ipynb (lab and homework notebooks)
# The site pulls everything from those files; run this after editing any of them.
set -euo pipefail
cd "$(dirname "$0")"

# Weeks whose materials (notes, lab, homework) are published. To open a new week:
# add its number here, move its weekNN-notes.qmd page back from _unpublished/,
# and restore the material links in weekNN.qmd ("published before class" rows).
PUBLISH_WEEKS="01 02 03 04 05 06 07"
published() { case " $PUBLISH_WEEKS " in *" $1 "*) return 0;; *) return 1;; esac; }

# API guide: strip the H1 (the page adds its own title), fix the README link.
sed '1{/^# /d}' ../labs/API_SETUP.md \
  | sed 's|\[labs/README.md\](README.md)|the lab README in the course repo|' \
  > _api-setup-content.md

# Lecture notes (English) → included by weekNN-notes.qmd pages.
for d in ../lectures/week*/; do
  week="$(basename "$d")"          # week01 …
  nn="${week#week}"
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

# Lab and homework notebooks: downloadable .ipynb + read-only HTML view
# (rendered from stored outputs only, never executed).
mkdir -p _site/labs
for nb in ../lectures/week*/W*_lab_*.ipynb ../lectures/week*/W*_hw_*.ipynb; do
  [ -e "$nb" ] || continue
  nbweek="$(basename "$(dirname "$nb")")"
  published "${nbweek#week}" || continue
  cp "$nb" _site/labs/
  quarto render "$nb" --to html --no-execute
  base="$(basename "$nb" .ipynb)"
  dir="$(dirname "$nb")"
  mv "$dir/$base.html" _site/labs/
  if [ -d "$dir/${base}_files" ]; then
    rm -rf "_site/labs/${base}_files"
    mv "$dir/${base}_files" _site/labs/
  fi
done

# Lab data files, fetched by notebooks at runtime (e.g. coffee_sales.csv).
mkdir -p _site/labs/data
cp ../labs/data/*.csv _site/labs/data/ 2>/dev/null || true

# Purge artifacts of unpublished weeks and retired formats (slides, Korean pages)
# left in _site by earlier builds.
rm -rf _site/lectures/week0? _site/lectures/week1?
rm -f _site/week*-notes-ko.html
for d in ../lectures/week*/; do
  nn="$(basename "$d")"; nn="${nn#week}"
  published "$nn" && continue
  rm -rf _site/labs/W$((10#$nn))_lab_* _site/labs/W$((10#$nn))_hw_*
  rm -f "_site/week$nn-notes.html"
done

echo "built: $(pwd)/_site"
