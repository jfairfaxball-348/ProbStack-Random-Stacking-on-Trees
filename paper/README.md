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

## arXiv package and public record

The validated arXiv-preparation material is under arxiv/. The exact upload
archive is paper/arxiv/ProbStack-arxiv.tar.gz and its checksum is recorded in
paper/arxiv/archive.sha256. The generated PDF was an inspection artifact and
was not an upload input.

That validated source was subsequently posted publicly as
arXiv:2609.39633, version 1, on 30 September 2026:
https://arxiv.org/abs/2609.39633

The final public classification is primary math.CO with a math.PR cross-list.
The arXiv-issued DOI is https://doi.org/10.48550/arXiv.2609.39633 and the
article license is CC BY 4.0.

paper/arxiv/metadata.txt is retained as the pre-submission metadata snapshot
used during packaging. The final submission interface required an ASCII-only
abstract and added the math.PR cross-list, so the public arXiv record is
authoritative for final metadata.

## Verification boundary

The immutable source of the registered Palomar finite theorem is
1897a76956168fba047f5943fa7998601f4fe459
(PALOMAR-2026-09-30-000023, version 1). That registration covers the
deterministic finite-path deep-message necessity theorem and its exact
fixed-total corollary; it does not cover the full probabilistic fixed-offset
transition theorem. Paper/arXiv packaging changes do not alter the registered
Lean theorem and do not require a new Palomar run.
