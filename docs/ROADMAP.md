# ProbStack roadmap

The original ProbStack research-and-release roadmap is complete for the current
fixed-offset path theorem. The theorem remains frozen at the following
precision:

[
c_n=sqrt{\log_2 n}
-\frac12\log_2\log_2 n
+\log_2(3e).
]

For every fixed (arepsilon>0), the stackability probability tends to zero
when (log_2mu_nle c_n-arepsilon) eventually and tends to one when
(log_2mu_nge c_n+arepsilon) eventually. There is no zero-offset claim.

## Stage 1 — complete: conjecture discovery and mathematical proof

Sessions 1--18 developed and closed the rigorous paper proof of the fixed-offset
path theorem. The theorem is not to be reopened merely for a finer critical
window, zero-offset law, finite-(n) monotonicity, Poisson front process, or
arbitrary-tree extension.

## Stage 2 — complete: finite formalisation boundary and reproducibility

Sessions 9--19 established and validated the exact finite Lean interfaces used
at the paper/formalisation boundary. The full analytic asymptotic theorem
remains paper mathematics rather than a Lean limit theorem. No `sorry` or new
project axiom is used to hide that distinction.

Authoritative closure documents include
`docs/FINAL_THEOREM_STATUS.md`,
`docs/PROOF_DEPENDENCY_MAP.md`, and
`docs/REPRODUCIBILITY.md`.

## Stage 3 — complete: public-record prior-art/originality audit

Sessions 20--21 completed the documented public-record audit. The audit found
no exact match in the searched public record for the ProbStack random
fixed-total support-collapse stackability theorem on paths. This is an
originality finding for the searched record, not an unconditional historical
priority claim.

## Stage 4 — complete: Palomar registration

The finite deterministic deep-message necessity theorem and its exact
fixed-total corollary are registered as
[PALOMAR-2026-09-30-000023, version 1](https://palomar-registry.org/entry.html?id=PALOMAR-2026-09-30-000023&version=1).

The registered source commit is
`1897a76956168fba047f5943fa7998601f4fe459`. The registration does not cover
the full probabilistic fixed-offset transition theorem.

## Stage 5 — complete: standalone paper

The standalone manuscript
_A Fixed-Offset Transition for Random Stackability on Paths_
was completed at source commit
`f37d04ee93168b1f3ab1ff271fc850e8dad2955c`.

## Stage 6 — complete: arXiv packaging and public posting

The source package was independently validated on the
`arxiv-preparation` branch. The paper is publicly posted as
[arXiv:2609.39633](https://arxiv.org/abs/2609.39633), version 1, submitted
30 September 2026, with primary category `math.CO` and cross-list
`math.PR`.

The arXiv-issued DOI is
[10.48550/arXiv.2609.39633](https://doi.org/10.48550/arXiv.2609.39633).
The article license is CC BY 4.0.

## Current state

The current research-and-release programme is complete. Routine corrections,
metadata maintenance, citation updates, or later journal decisions may be made
without reopening the mathematics or rerunning Palomar. Any genuinely new
mathematical objective should be treated as a separate research stage with its
own scope and validation boundary.
