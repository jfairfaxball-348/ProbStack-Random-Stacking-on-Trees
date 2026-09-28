# Session 19 — theorem / formalisation / reproducibility closure

## Starting boundary

Session 19 starts from validated `main`

`28d4dbf0e4692e544324fa7810c90791de4cd648`.

Frozen dependencies:

- TreeStack: `f4112f08d42a37c0941bf469ac124621b1f54f22`;
- Mathlib: `065356127b1dc0016f66b7283ce0ce2c4055aa55`;
- Lean: `leanprover/lean4:v4.35.0-rc2`.

EMPTY remains categorical: `TreeStack.EMPTY = none` and is not `some 0`.

## Audit conclusions

The frozen theorem is internally consistent across the current mathematical
sources. The authoritative center remains

```
sqrt(log_2 n)
- (1/2) log_2 log_2 n
+ log_2(3e).
```

Session 19 does not change the theorem, the Session 17 local rate, the exact
deep target `-(2*mu-1)`, or any dependency pin.

The principal documentation issue was historical status drift. Several notes
still used language that was accurate at the end of Sessions 1, 6, or 7 but
could be mistaken for current status. Those records are preserved and marked
as historical/superseded; current-facing documentation now points to the
Session 18 proof and the final Session 19 dependency map.

## Formalisation audit

The Lean repository contains the finite/deterministic interfaces listed in
`docs/FINAL_THEOREM_STATUS.md`: exact path recursion, deficit identities,
regeneration, deep-block consequences, explicit seed/runaway support and mass,
genuine left/right seed-to-front composition, finite geometric masses,
fixed-total atom equality, local conditioning definitions, and finite dyadic
combinatorics.

Two claims that had sometimes been described too broadly are **not** packaged
as ProbStack Lean theorems:

1. the full Session 5 global necessity
   `nonstackable => some directed message <= -(2*mu-1)`;
2. a single path-level theorem packaging opposing certified fronts into
   nonstackability.

The existing `PathDeep.lean` theorem is a weighted necessity consequence of
an already-deep message, not the Session 5 global implication. Both global
facts remain rigorous paper mathematics. They are not small interface seams,
so Session 19 does not attempt risky root-score/path infrastructure merely for
formalisation quantity.

The weak-composition `Fintype.card` theorem and a finite-sum normalisation
theorem likewise remain optional finite seams. They are not required by any
current Lean theorem and would not remove the genuinely analytic boundary, so
they are deliberately left out.

## Conditioning audit

The Python/Lean finite conventions agree:

- `p = 1/(1+mu)`;
- `r = mu/(1+mu)`;
- `weak_composition_count(0,0) = 1`;
- `weak_composition_count(0,t) = 0` for `t > 0`;
- matched local product law uses `p=n/(n+t)`, `r=t/(n+t)`;
- exact local likelihood-ratio implementations agree;
- separated bounded blocks are concatenated into one displayed vector;
- conditioned independence is nowhere required.

The exact total point mass is the negative-binomial/stars-and-bars value
recorded in Session 18.

## Spatial audit

The final proof continues to use:

- Session 4 reset;
- Session 8 regeneration for `-mu < M <= 2mu`;
- steering interval `[2mu+2-M, 4mu-M]`;
- steering occupancy cap `5mu-1`;
- worst-case probability
  `r^(3mu+1) * (1-r^(2mu-1)) >= 8/(17e^3)` for `mu >= 16`;
- Session 17 start window `[mu,2mu]`;
- an `O(log n)`-support reserved superblock;
- reversed construction in the other half;
- exact supercritical target `-(2mu-1)`;
- `O(n)` interior locations but only `O(1)` physical-boundary locations;
- one prescribed occupancy for the exact-output-zero bridge.

No conditioned independence is introduced.

## Reproducibility closure

`docs/REPRODUCIBILITY.md` is the single entry point for final exact
validation commands. Session 19 adds regression tests for:

- the exact `-(2mu-1)` deep target;
- the explicit spatial factor `n` in the global balance;
- concatenation rather than independence for separated conditioned blocks;
- the frozen TreeStack/Mathlib/Lean pins and permanent workflow cache key.

A temporary Session 19 Python workflow is used only on the Session 19 branch
to run the full suite and regenerate/check the deterministic Session 16–18
diagnostics. It must be deleted before merging final work to `main`.

## Boundary after Session 19

After final Python and permanent Lean CI validation, the
theorem/proof/formalisation/reproducibility stage is closed. The next stage is
an extensive public-record prior-art/originality audit. No novelty or priority
claim is made here.
