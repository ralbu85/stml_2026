#!/usr/bin/env bash
# build.sh — render the STML course materials and website.
#
# Everything is HTML. No LaTeX, no fonts to install, no image conversion.
#
# Each week's folder holds its sources AND its rendered files side by side,
# so lectures/weekNN/ is browsable on its own — double-click to view:
#     notes.en.md    → notes.html     lecture notes
#     slides.qmd     → slides.html    lecture deck (present in a browser)
#     W*_lab_*.ipynb                  lab notebook (upload to Colab)
# Both HTML files embed their images, so either one opens or sends by itself.
#
# The website copies each published week's folder into _site/lectures/weekNN/,
# which is why the site links and the folder contents are always the same files.
#
# Release model: every week page is public and shows that week's topic and
# presentation papers from day one; the materials are released week by week.
# PUBLISH_WEEKS is the single switch — a week not listed there has nothing
# copied into _site, so its files are not reachable by guessing a URL.
# To open a week: add its number here, replace the "published before class"
# rows of site/weekNN.qmd with links, and re-run this script.
set -euo pipefail
cd "$(dirname "$0")"

PUBLISH_WEEKS="01"
published() { case " $PUBLISH_WEEKS " in *" $1 "*) return 0;; *) return 1;; esac; }

# Render each week's materials in place, next to their sources.
for d in ../lectures/week*/; do
  nn="$(basename "$d")"; nn="${nn#week}"
  published "$nn" || continue

  # Rendered from inside the week folder: quarto resolves --output and the
  # figure paths against the working directory, not against the input file.
  if [ -f "$d/notes.en.md" ]; then
    ( cd "$d" && quarto render notes.en.md --to html --output notes.html \
        -M "title:Week $nn — Lecture Notes" -M toc:true -M embed-resources:true )
  fi

  [ -f "$d/slides.qmd" ] && ( cd "$d" && quarto render slides.qmd --to revealjs )
done

# API guide: strip the H1 (the page adds its own title), fix the README link.
sed '1{/^# /d}' ../labs/API_SETUP.md \
  | sed 's|\[labs/README.md\](README.md)|the lab README in the course repo|' \
  > _api-setup-content.md

# Built from scratch: the gate is only trustworthy if a week dropped from
# PUBLISH_WEEKS also disappears from the output of the next build.
rm -rf _site
quarto render .

# Published weeks: the same files the folder holds, served by the site.
for d in ../lectures/week*/; do
  week="$(basename "$d")"
  published "${week#week}" || continue
  mkdir -p "_site/lectures/$week"
  cp "$d"/notes.html "$d"/slides.html "_site/lectures/$week/" 2>/dev/null || true
  cp "$d"/W*_lab_*.ipynb "$d"/W*_hw_*.ipynb "_site/lectures/$week/" 2>/dev/null || true
done

# Data files the notebooks fetch at runtime (e.g. coffee_sales.csv).
mkdir -p _site/labs/data
cp ../labs/data/*.csv _site/labs/data/ 2>/dev/null || true

# Sample paper presentation (6-slide template exemplar, linked from presentations.qmd).
quarto render ../lectures/presentation-sample/slides.qmd --to revealjs
mkdir -p _site/lectures/presentation-sample
cp -r ../lectures/presentation-sample/slides.html \
      ../lectures/presentation-sample/slides_files \
      _site/lectures/presentation-sample/ 2>/dev/null || true

echo "built: $(pwd)/_site  (weeks published: $PUBLISH_WEEKS)"
