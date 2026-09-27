# Session 13 handover

Session 13 starts from validated `main`
`84e16f3cc4678d5a95ad3c116b6c91112e1672f0` and keeps all dependency pins
unchanged.

## Deterministic result

New module: `ProbStack/PathFront.lean`.

Core scalar interface:

- `runawayNext`;
- `RunawayBlock`;
- `runawayThreshold`;
- `DeepSeed`;
- `UniformDeepSeedBlock`;
- `CertifiedFront`;
- `runaway_step`;
- `runawayBlock_lowRun_and_deficit_ge`;
- `deepSeed_runaway_to_front`;
- `certifiedFront_dominates`.

Exact runaway convention:

- occupancy cap: `4 * X <= D`;
- next threshold: `D + D/2 = floor(3D/2)` for the positive thresholds used.

Genuine left results:

- `LeftPath.leftBranch_runaway_to_front`;
- `LeftPath.leftBranch_certifiedFront_irreversible`;
- `LeftPath.leftBranch_seed_runaway_to_front`;
- `LeftPath.leftBranch_regeneration_seed_runaway_to_front`.

Genuine right results:

- `RightPath.rightBranch_runaway_to_front`;
- `RightPath.rightBranch_certifiedFront_irreversible`;
- `RightPath.rightBranch_seed_runaway_to_front`;
- `RightPath.rightBranch_regeneration_seed_runaway_to_front`.

The deterministic concatenation is formal in both orientations:

genuine regeneration
+ finite seed block valid uniformly for regenerated states
+ explicit finite runaway caps
=> genuine certified front.

A certified front with budget `T` dominates every subsequent finite
occupancy block of total mass at most `T`: the continuation stays low-phase,
and every nonempty continuation ends at a negative active message.

## Session 14 boundary

The remaining sharp seed event is exposed as
`UniformDeepSeedBlock mu (2*mu) D xs`, a scalar predicate on an explicit
finite occupancy list. Session 14 may begin finite weak-composition/geometric
probability and instantiate/count sharp seed events without reopening genuine
TreeStack branch recursion or left/right path indexing.

No probability work was started in Session 13.

The frozen headline theorem was untouched. EMPTY remains categorical.

## Validation

Lean-source checkpoint:
`9a38019a9a9d269846ae223d6665431b7418d307`.

PR-head GitHub Actions run `36301866410` passed the pinned TreeStack build,
full ProbStack build, and local no-`sorry`/no-`axiom` grep.

The exact documentation-inclusive final `main` HEAD and exact-head Actions
run are reported after the final promotion/validation pass.
