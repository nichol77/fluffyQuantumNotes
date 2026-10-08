#!/bin/sh
# Build the ePub, LaTeX and PDF versions of the notes from week1.md.
# Needs pandoc (brew install pandoc) and, for the PDF, a TeX installation.
set -e
pandoc week1.md -o Week1_notes.epub -t epub3 --mathml --toc --toc-depth=2 \
  --number-sections --css style.css --epub-cover-image=fig/cover.png
pandoc week1.md -s -o Week1_notes.tex --lua-filter=boxes.lua --number-sections --toc \
  -H preamble.tex -V documentclass=article -V papersize=a4 -V geometry:margin=2.5cm \
  -V fontsize=11pt -V colorlinks=true -V linkcolor=navy -V urlcolor=navy -V toccolor=navy \
  -M date="Draft --- October 2026"
if command -v latexmk >/dev/null; then latexmk -pdf -quiet Week1_notes.tex; fi
