# ProbStack arXiv preparation package

This directory records the exact source intended for a later arXiv submission.
Nothing in this workflow submits to arXiv.

## Upload artifact

The upload artifact is ProbStack-arxiv.tar.gz.

The archive intentionally contains exactly one file, main.tex. The paper's
bibliography is directly typeset in that file, so references.bib is
repository-side bibliographic metadata and is not a build input. The upload
archive contains no generated PDF, logs, auxiliary files, repository metadata,
Lean/Python sources, caches, or Git files.

main.tex here must be byte-for-byte identical to ../main.tex; the preflight
script rejects any divergence. The standalone source commit from which the
package is derived is f37d04ee93168b1f3ab1ff271fc850e8dad2955c.

## Build and validation

From the repository root run:

    python3 paper/build_arxiv.py

The script checks mathematical/package invariants and submission metadata,
compiles the canonical and packaged sources with PDFLaTeX, rejects unresolved
references/citations, TeX errors, missing glyphs and overfull boxes, creates a
deterministic tar.gz containing only main.tex, safely extracts the exact
archive, recompiles the extracted source without repository inputs, and
requires identical page count and extracted PDF text across all builds.

It writes paper/arxiv/archive.sha256 and
paper/.build/arxiv/preflight.json. The generated PDF is an inspection/build
artifact and is not committed as an arXiv source input.

## Submission metadata

See metadata.txt. Proposed primary category: math.CO; no cross-list.

The intended article license is CC BY 4.0, to be confirmed by the author in the
actual submission interface after checking any applicable future journal or
funder policy. The repository's Apache-2.0 license does not determine the
article license.

Palomar record PALOMAR-2026-09-30-000023, version 1, covers only the finite
deterministic deep-message necessity theorem and its exact fixed-total
corollary. It does not cover the full probabilistic fixed-offset theorem.

## Current arXiv technical basis

Packaging rules were rechecked against official arXiv documentation on
2026-09-30. PDFLaTeX is supported; TeX Live 2025 is the default and TeX Live
2023 is also supported. arXiv accepts tar.gz/zip collections, requires
portable case-correct filenames, and asks authors to omit extraneous files.

Official references:
- https://info.arxiv.org/help/submit/index.html
- https://info.arxiv.org/help/submit_tex.html
- https://info.arxiv.org/help/faq/texlive.html
- https://info.arxiv.org/help/prep.html
- https://info.arxiv.org/help/license/index.html
