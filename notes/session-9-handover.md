# Session 9 handover

## Starting state

Session 9 began from ProbStack

`26f15c1f24d65e5a3e9f4702448c70f43558f8b0`

and verified that `main` matched that SHA.

The authoritative TreeStack dependency remains

`f4112f08d42a37c0941bf469ac124621b1f54f22`.

TreeStack at that commit pins Mathlib

`065356127b1dc0016f66b7283ce0ce2c4055aa55`

and Lean

`leanprover/lean4:v4.35.0-rc2`.

## Session 9 result

Session 9 was a design session. The theorem was not reopened.

The full architecture is recorded in
`notes/session-9-formalisation-design.md`.

The main decisions are:

1. import TreeStack's exact `F`, categorical `Message = Option ℤ`,
   `EMPTY`, branch messages, rooted score, and
   `stackableAt_iff_score_pos`;
2. use Mathlib's `SimpleGraph.pathGraph n` on `Fin n`;
3. reuse `TreeStack.Configuration` and `TreeStack.mass`;
4. define weak compositions as exact-mass TreeStack configurations and obtain
   finiteness via bounded-coordinate vectors;
5. use Mathlib's geometric measure, finite-index product measure, conditional
   measure, and uniform PMF rather than building a general probability stack;
6. isolate the binary-partition analytic input in one module;
7. require only compact-uniform (o(L)) precision for the cumulative
   binary-partition logarithm;
8. first attempt a direct recurrence/saddle-point proof of that weaker estimate
   instead of formalising de Bruijn's full historical periodic expansion;
9. keep all final trusted files free of axioms/sorries;
10. split the final frozen theorem into subcritical and supercritical Lean
    theorems and combine them only in `Main.lean`.

## Exact TreeStack formal reuse

The audit located the exact formal names:

- `TreeStack.F`;
- `TreeStack.Message`;
- `TreeStack.EMPTY`;
- `TreeStack.empty_ne_integer_zero`;
- `TreeStack.OrientedBranch.branchMessage`;
- `TreeStack.OrientedBranch.messageContribution`;
- `TreeStack.OrientedBranch.effectiveInput`;
- `TreeStack.score`;
- `TreeStack.StackableAt`;
- `TreeStack.Stackable`;
- `TreeStack.stackableAt_iff_score_pos`;
- `TreeStack.not_stackable_iff_all_scores_nonpos`.

No path-specialised TreeStack formal module was found, so the path scalar
recurrence and all probabilistic/path-asymptotic lemmas are new ProbStack
obligations.

## Binary-partition bottleneck

The minimal analytic input is the compact-uniform estimate

[
log_2 A(B)
=
rac12L^2
-Llog_2L
+
left(log_2(B/2^L)+rac12+log_2eight)L
+o(L)
]

uniformly when (B/2^L) stays in a fixed compact subinterval of
((0,infty)).

Only (o(L)) is needed. The stronger periodic/full de Bruijn expansion is not
required.

The minus sign in the cumulative-count (Llog L) term is deliberate and
matches the Session 7 proof. It yields the plus (Llog L) term in each rare
probability cost.

## Lean/code validation

No Lean source was added because the current execution environment has neither
`lean` nor `lake` installed. Therefore no Lean compilation is claimed.

No Python code was changed and no Python tests were run.

Recorded validation remains:

- Session 8 targeted regeneration: 5 passed;
- last literal full pytest suite: 54 passed (Session 5);
- exhaustive independent validator:
  146 labelled trees,
  33,711 configurations,
  166,116 rooted cases,
  zero disagreements.

## Frozen theorem status

**YES — the frozen Session 8 headline theorem remains the correct
formalisation target.**

No assertion at zero offset has been added. No finite-(n) monotonicity,
critical-window distribution, Poisson-process statement, or arbitrary-tree
extension has been introduced.

## Dependency-driven next stages

The next implementation sequence is:

- bootstrap pinned Lean/TreeStack/Mathlib and compile the import boundary;
- formalise the deterministic path recurrence and low-risk transfer/deficit
  lemmas;
- formalise fronts/reset/regeneration;
- formalise finite weak-composition/geometric conditioning;
- formalise structural deep-message necessity;
- formalise finite dyadic/binary-partition combinatorics;
- attack the isolated binary-partition (o(L)) asymptotic;
- assemble local excursion asymptotics;
- finish conditioning/hazard estimates;
- prove the global fixed-offset theorem.

The binary-partition analytic theorem may consume multiple sessions; session
numbers should follow dependencies rather than deadlines.

## Single best next step

Configure the exact Lean package boundary and make a minimal compiling
`ProbStack/TreeStackBoundary.lean` plus the `SimpleGraph.pathGraph`
finite-tree wrapper. Do not proceed to probability or binary partitions until
that foundation compiles.
