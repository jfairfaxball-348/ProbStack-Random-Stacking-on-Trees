# Session 13 — deterministic seed-to-front interface

Status: **FORMAL and CI-validated on both path orientations.**

Session 13 remained entirely deterministic/formal. No probability estimates,
stars-and-bars calculations, iid geometric estimates, binary-partition
asymptotics, conditioning, prior-art search, or paper drafting were started.
The frozen headline theorem was untouched.

Starting ProbStack `main`:
`84e16f3cc4678d5a95ad3c116b6c91112e1672f0`.

Pinned dependencies remain unchanged:

- TreeStack: `f4112f08d42a37c0941bf469ac124621b1f54f22`;
- Mathlib: `065356127b1dc0016f66b7283ce0ce2c4055aa55`;
- Lean: `leanprover/lean4:v4.35.0-rc2`.

## New module

`ProbStack/PathFront.lean`, imported by `ProbStack.lean`.

## Scalar runaway convention

The exact cap is `4 * X <= D`, equivalent for the positive thresholds here
to `X <= floor(D/4)`.

The next certified threshold is

`runawayNext D = D + D / 2`,

i.e. `floor(3D/2)` for nonnegative integer `D`.

Formal scalar objects/results:

- `RunawayBlock`;
- `runawayThreshold`;
- `DeepSeed`;
- `UniformDeepSeedBlock`;
- `CertifiedFront`;
- `four_le_runawayNext`;
- `runaway_step`;
- `runawayBlock_lowRun_and_deficit_ge`;
- `deepSeed_runaway_to_front`.

Thus a finite recursive list of explicit occupancy caps propagates a deep seed
with certified geometric deficit growth.

`UniformDeepSeedBlock lo hi D xs` is deliberately the scalar seam for the
later sharp local excursion: every starting message in `[lo,hi]` is sent by
the explicit finite occupancy list `xs` to deficit at least `D`.

## Irreversibility / domination

Formal results:

- `lowRun_of_message_add_sum_le_one`;
- `certifiedFront_lowRun`;
- `activeScan_le_neg_one_of_lowRun_nonempty`;
- `certifiedFront_dominates`.

`CertifiedFront budget m` means `budget + 2 <= deficit m`. If a future
finite occupancy list has total mass at most `budget`, the entire
continuation stays in the low phase. Any nonempty such continuation ends at a
message at most `-1`.

This is the reusable front-domination statement; no hard-coded `n` or
`mu` is needed.

## Genuine left path

Formal results:

- `LeftPath.leftBranch_runaway_to_front`;
- `LeftPath.leftBranch_certifiedFront_irreversible`;
- `LeftPath.leftBranch_seed_runaway_to_front`;
- `LeftPath.leftBranch_regeneration_seed_runaway_to_front`.

The last theorem formalises:

genuine incoming reset-window state
+ one valid regeneration occupancy
+ a finite `UniformDeepSeedBlock`
+ an explicit `RunawayBlock`
=> a genuine left branch message satisfying `CertifiedFront`.

All occupancies are exposed through the existing
`LeftPath.leftBlockValues`.

## Genuine right path

Symmetric formal results:

- `RightPath.rightBranch_runaway_to_front`;
- `RightPath.rightBranch_certifiedFront_irreversible`;
- `RightPath.rightBranch_seed_runaway_to_front`;
- `RightPath.rightBranch_regeneration_seed_runaway_to_front`.

The existing `Fin.rev` right orientation is preserved exactly.

## EMPTY semantics

EMPTY remains categorical:

- `TreeStack.Message = Option Int`;
- `TreeStack.EMPTY = none`;
- no theorem identifies EMPTY with integer zero or `some 0`.

The new interface begins only from an actual active message `some m`, or
after the existing genuine regeneration theorem has produced one.

## Probability-readiness

The branch recursion, path indexing, runaway growth, and irreversible-front
domination layers no longer need to be reopened for probability.

Session 14 can work with explicit finite occupancy lists: prove/count a chosen
local seed event as an instance of
`UniformDeepSeedBlock mu (2*mu) D xs`, append the explicit
`RunawayBlock` caps, then invoke the genuine left/right concatenation
theorems.

## Validation checkpoint

Lean-source checkpoint:
`9a38019a9a9d269846ae223d6665431b7418d307`.

GitHub Actions run `36301866410` completed successfully using the pinned
TreeStack dependency, full `lake build`, and the project grep rejecting
local `sorry` and `axiom`.

The exact documentation-inclusive final `main` HEAD and exact-head CI run
are reported in the completion response after promotion. A file cannot
reliably contain its own final commit SHA without changing that SHA.
