# ProbStack paper

This directory contains the canonical standalone research manuscript for
ProbStack.

## Public preprint

The paper is publicly posted as:

- **John Fairfax-Ball, _A Fixed-Offset Transition for Random Stackability on Paths_**
- arXiv:2609.39633 — https://arxiv.org/abs/2609.39633
- version 1, submitted 30 September 2026
- primary category: `math.CO` (Combinatorics)
- cross-list: `math.PR` (Probability)
- DOI: https://doi.org/10.48550/arXiv.2609.39633
- 16 pages, 0 figures
- article license: CC BY 4.0

The public arXiv metadata correctly states that the Palomar registration covers
only the finite deterministic deep-message necessity theorem and its exact
fixed-total corollary, not the full probabilistic asymptotic theorem.

## Standalone manuscript

`main.tex` is the canonical manuscript source. It is intentionally
self-contained and uses only standard LaTeX packages. The bibliography is
typeset directly in `main.tex`; `references.bib` is retained as
version-controlled bibliographic source metadata.

Build with:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The completed standalone-paper source commit is
`f37d04ee93168b1f3ab1ff271fc850e8dad2955c`. The validated arXiv-preparation
history is retained on the `arxiv-preparation` branch; its final validated
pre-submission package commit is
`9d2a1f71e713cabbeaaa480c7dfac8019d716610`.

## Verification boundary

The immutable source of the registered Palomar finite theorem is
`1897a76956168fba047f5943fa7998601f4fe459`
(`PALOMAR-2026-09-30-000023`, version 1). That registration covers the
deterministic finite-path deep-message necessity theorem and its exact
fixed-total corollary; it does not cover the full probabilistic fixed-offset
transition theorem.

Paper, arXiv metadata and post-publication documentation changes do not alter
that registered Lean theorem and do not require a new Palomar run.
