# ProbStack standalone paper

This directory contains the standalone research manuscript for ProbStack.

## Build

The manuscript is intentionally self-contained and uses only standard LaTeX packages. The bibliography is typeset directly in `main.tex` so that the paper builds without a BibTeX dependency; `references.bib` is retained as version-controlled bibliographic source metadata for the later submission-preparation stage.

Build with:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The paper was audited against ProbStack `main` revision `3953c09c7ca0508a95721f60c59912ca9c917478`. The immutable source of the registered Palomar finite theorem is `1897a76956168fba047f5943fa7998601f4fe459` (`PALOMAR-2026-09-30-000023`, version 1). Paper-only changes do not alter that registered theorem.

No arXiv submission package is created in this directory at this stage.
