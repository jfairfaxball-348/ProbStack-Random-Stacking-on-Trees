# ProbStack roadmap

## Stage 1 — current: conjecture discovery and proof

Maintain independent deterministic solvers, exact small-instance enumeration,
seeded uniform-composition sampling, and auditable experiment logs.  For paths,
identify the correct growing-regime probability statement and prove it before
expanding to secondary deterministic tree families.

Secondary families (stars, balanced binary trees, complete b-ary trees,
bounded-height trees) enter only after the path machinery is functioning.
Random trees and `G(n,p)` are successor projects unless they become essentially
free consequences.

## Stage 2 — formalization, only after a stable informal theorem

Pin a Lean and mathlib revision; formalize the finite combinatorial probability
space and the theorem's probabilistic ingredients; either import a clean
trusted TreeStack theorem boundary or restate it with explicit provenance;
formalize the finite identities and asymptotics needed by the final result;
expose one clear headline theorem; remove all admits/sorries from the trusted
path; and run complete Lean CI.

If the asymptotic probability theory is substantially harder to formalize than
the deterministic TreeStack result, record that honestly rather than weakening
the mathematics to fit the prover.

## Stage 3 — comprehensive public-record prior-art/originality audit

Only after the theorem and proof are mature, search well beyond arXiv:
MathSciNet/zbMATH references where accessible, journals, Scholar-style citation
trails, graph-pebbling bibliographies, author pages, proceedings, theses,
terminology variants, cited/citing papers, and equivalent formulations.  Log
search terms, dates, databases, and findings.  A negative public-record audit
cannot rule out private, unpublished, or unindexed work.

## Stage 4 — Palomar

Only after proof and formalization are complete: freeze the verified commit,
inspect the then-current Palomar specification, prepare Comparator/Challenge
packaging, run repository CI and official preflight, fix every blocker, and
register the immutable verified revision.  Do not reuse TreeStack's old schema
or toolchain without rechecking current requirements.

## Stage 5 — standalone paper

Write a self-contained article explaining the model, deterministic input,
probability space, theorem(s), proof, only mathematically useful experiments,
relation to probabilistic pebbling, formal-verification statement,
reproducibility, and—only if justified by the later audit—carefully qualified
prior-art language.  Do not oversell.

## Stage 6 — arXiv

Prepare canonical LaTeX and a separately tested arXiv source bundle; audit
metadata, references, category, MSC, and keywords; compile from the upload
bundle; then submit the final checked source.  Category choice should follow the
actual mathematics (likely `math.CO` only if the completed work remains
primarily probabilistic combinatorics).
