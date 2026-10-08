# Week 2 notes: source files

- `week2.md` is the master copy of the notes. Edit this file.
- `build.sh` makes the ePub, the `.tex` file and the PDF from `week2.md` (needs pandoc; the PDF also needs LaTeX).
- `style.css` styles the ePub. `preamble.tex` and `boxes.lua` style the LaTeX and PDF.
- `fig/` holds the figures. `make_figures.py` redraws them (needs Python with numpy and matplotlib).

Coloured boxes are written as fenced divs, for example:

    ::: keyresult
    **Key result.** $E = hf$
    :::

The box types are `keyresult`, `example`, `further`, `aside`, `reading` and `problem`.
