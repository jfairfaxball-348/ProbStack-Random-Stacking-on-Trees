# Session 12 handover

## Validated starting state

Session 12 started from ProbStack `main`:

`df62bf4dc55ba4d6352562b93f06c60c60ffe282`.

Dependencies were not changed:

- TreeStack: `f4112f08d42a37c0941bf469ac124621b1f54f22`;
- Mathlib: `065356127b1dc0016f66b7283ce0ce2c4055aa55`;
- Lean: `leanprover/lean4:v4.35.0-rc2`.

## Session 12 result

The deterministic deep-message layer is now formal for genuine TreeStack path
branches in both orientations.

New module:

- `ProbStack/PathDeep.lean`.

New scalar results:

- `activeScan_append`;
- `dyadicInputCost_le_of_lowRun_deficit_ge`;
- `dyadicInputCost_le_of_lowRun_message_le`.

New left-oriented results:

- `LeftPath.leftBlockValues`;
- `LeftPath.leftBlockValues_length`;
- `LeftPath.leftBranch_branchMessage_eq_activeScan_block`;
- `LeftPath.leftBranch_dyadicInputCost_le_of_deep`;
- `LeftPath.leftBranch_regeneration_step`.

New right-oriented results:

- `RightPath.rightBlockValues`;
- `RightPath.rightBlockValues_length`;
- `RightPath.rightBranch_branchMessage_eq_activeScan_block`;
- `RightPath.rightBranch_dyadicInputCost_le_of_deep`;
- `RightPath.rightBranch_regeneration_step`.

`ProbStack.lean` now imports `ProbStack.PathDeep`.

## Weighted necessity statement

For `xs=[X₁,...,X_k]` the weighting is

`2^k X₁ + 2^(k-1) X₂ + ... + 2 X_k`.

If an active low run begins at message `m`, ends at a genuine branch message
at most `-H`, and the corresponding block satisfies the explicit `LowRun`
hypothesis, then

`dyadicInputCost xs <= 2^k * deficit m - (H+3)`.

The direction is an upper bound on weighted occupancy. This is intentional:
occupancy subtracts from deficit in the low-phase identity.

The exact branch-message scan theorem is also formal without a low-run
hypothesis, so the structural reduction and the low-phase arithmetic are kept
separate.

## Regeneration status

The exact one-coordinate regeneration window is now connected to genuine
left and right branch messages.

For `1 <= mu`, `-mu < M <= 2mu`, and

`2mu+2-M <= X <= 4mu-M`,

the next actual branch message lies in `[mu,2mu]`.

No explicit irreversible-front/event definition was added yet.

## Verification discipline

The final theorem was not changed.

EMPTY remains categorical:

- `TreeStack.Message = Option ℤ`;
- `TreeStack.EMPTY = none`;
- no new theorem identifies EMPTY with integer zero or `some 0`.

The promoted source checkpoint
`c45929a59a85db49dcf15e22498105361819309b`
passed GitHub Actions run `36275694471`, including full package build and the
project no-`sorry`/no-`axiom` audit.

The exact final documentation-inclusive HEAD and its exact-head CI run are
reported after the final validation pass in the Session 12 completion response.

## Recommended Session 13 objective

Stay deterministic for one more session.

Formalise a genuine path **seed-to-front interface**:

1. attach a finite deep-deficit growth/runaway lemma to actual left/right
   branch messages;
2. define explicit left/right finite-block deep-seed/front predicates suitable
   for later probability events;
3. prove that the existing genuine regeneration step followed by the
   appropriate low-phase block produces the corresponding certified front;
4. expose the resulting certificate using only explicit vertex occupancies and
   integer inequalities.

Only after that interface is stable should the weak-composition/geometric
probability layer begin.
