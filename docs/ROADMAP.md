# ProbStack roadmap

## Stage 1 — complete: conjecture discovery and mathematical proof

The frozen path theorem is

\[
c_n=\sqrt{\log_2 n}
-\frac12\log_2\log_2 n
+\log_2(3e).
\]

For every fixed \(\varepsilon>0\), the stackability probability tends to zero
when \(\log_2\mu_n\le c_n-\varepsilon\) eventually and tends to one when
\(\log_2\mu_n\ge c_n+\varepsilon\) eventually. There is no zero-offset claim.

Session 18 completed the global mathematical proof. Do not reopen this stage
for a critical-window law, finer \(o(1)\) centering, finite-\(n\) monotonicity,
Poisson front counts, limiting distributions, or arbitrary-tree extensions.

## Stage 2 — complete: finite formalisation boundary and reproducibility

Sessions 9--19 established and validated the exact finite Lean boundary used by
the proof: pinned TreeStack semantics, categorical EMPTY, left/right path
messages, low-phase deficit identities, regeneration, explicit finite
seed/runaway/front interfaces, finite geometric and weak-composition algebra,
and finite dyadic combinatorics.

The full analytic asymptotic theorem is deliberately paper mathematics rather
than a Lean limit theorem. In particular, Robbins/Stirling asymptotics,
de Bruijn binary-partition asymptotics, the Session 17 local probability
asymptotic, and the Session 18 global limiting argument are not hidden behind
`sorry` or new axioms.

The authoritative closure documents are:

- `docs/FINAL_THEOREM_STATUS.md`;
- `docs/PROOF_DEPENDENCY_MAP.md`;
- `docs/REPRODUCIBILITY.md`;
- `notes/session-19-closure.md`.

Historical formalisation plans such as `notes/session-9-formalisation-design.md`
remain records of the state at the time; they are not the current completion
checklist.

## Stage 3 — next: comprehensive public-record prior-art/originality audit

Search well beyond arXiv: journals, MathSciNet/zbMATH where accessible,
Scholar-style citation trails, graph-pebbling bibliographies, author pages,
proceedings, theses, terminology variants, cited/citing papers, and
mathematically equivalent formulations.

The audit should cover at least random weak compositions / conditioned
geometrics, pebbling or stacking on paths and trees, TreeStack-style structural
certificates, binary-partition asymptotics, random message/affine recurrences
and rare deficit fronts, and thresholds at stretched-logarithmic densities.

Log search terms, dates, databases and findings. A negative public-record audit
cannot establish novelty or rule out private, unpublished, or unindexed work.
Do not make novelty or priority claims during the audit.

## Stage 4 — standalone paper

Only after Stage 3, write a self-contained article explaining the model,
deterministic TreeStack input, uniform weak-composition probability space,
frozen theorem, rigorous paper proof, exact finite Lean boundary, reproducible
deterministic validation, and the literature audit. Do not oversell the degree
of formalisation or originality.

## Stage 5 — submission and packaging decisions

Only after the theorem is proved, the finite formalisation/reproducibility
boundary is stable, the public-record audit is complete, and the standalone
paper is written should the project decide on arXiv, Palomar, journal
submission, or other packaging. Inspect then-current specifications rather
than reusing historical assumptions.
