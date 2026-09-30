# ProbStack paper

This directory contains the standalone research manuscript and the separately
validated arXiv-preparation package.

## Standalone manuscript

main.tex is the canonical manuscript source. It is intentionally self-contained
and uses only standard LaTeX packages. The bibliography is typeset directly in
main.tex; references.bib is retained as version-controlled bibliographic source
metadata.

Build the standalone manuscript with:

    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex

The completed standalone-paper source commit is
f37d04ee93168b1f3ab1ff271fc850e8dad2955c.

## arXiv preparation

The arXiv-preparation material is under arxiv/. Run the complete clean-package
preflight from the repository root with:

    python3 paper/build_arxiv.py

The exact upload archive is paper/arxiv/ProbStack-arxiv.tar.gz. Its checksum is
written to paper/arxiv/archive.sha256; the generated PDF is not an upload input
and is not committed. See arxiv/README.md and arxiv/metadata.txt for the package
record and proposed submission metadata.

This workflow prepares and validates source only. It does not submit anything
to arXiv.

## Verification boundary

The immutable source of the registered Palomar finite theorem is
1897a76956168fba047f5943fa7998601f4fe459
(PALOMAR-2026-09-30-000023, version 1). That registration covers the
deterministic finite-path deep-message necessity theorem and its exact
fixed-total corollary; it does not cover the full probabilistic fixed-offset
transition theorem. Paper/arXiv packaging changes do not alter the registered
Lean theorem and do not require a new Palomar run.
