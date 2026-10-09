#!/bin/sh
# Build the ePub, LaTeX and PDF versions of the notes from week2.md.
# Needs pandoc (brew install pandoc) and, for the PDF, a TeX installation.
set -e
pandoc week2.md -o Week2_notes.epub -t epub3 --mathml --toc --toc-depth=2 \
  --number-sections --css style.css --epub-cover-image=fig/cover.png
pandoc week2.md -s -o Week2_notes.tex --lua-filter=boxes.lua --number-sections --toc \
  -H preamble.tex -V documentclass=article -V papersize=a4 -V geometry:margin=2.5cm \
  -V fontsize=11pt -V colorlinks=true -V linkcolor=navy -V urlcolor=navy -V toccolor=navy \
  -M date="Draft --- October 2026"
if command -v latexmk >/dev/null; then latexmk -pdf -interaction=nonstopmode -quiet Week2_notes.tex; fi
