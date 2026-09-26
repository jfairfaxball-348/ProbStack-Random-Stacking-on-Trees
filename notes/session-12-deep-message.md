# Session 12 — weighted deep-message necessity on genuine path branches

Status: **FORMAL for both path orientations; genuine regeneration step begun.**

## 1. Scope

Session 12 remained entirely in the deterministic/formal structural layer.

No probability estimates, stars-and-bars calculations, geometric
approximations, binary-partition asymptotics, conditioning, prior-art search,
or paper drafting were started. The frozen headline path theorem was not
changed.

Starting ProbStack `main`:

`df62bf4dc55ba4d6352562b93f06c60c60ffe282`.

Pinned dependencies remain:

- TreeStack: `f4112f08d42a37c0941bf469ac124621b1f54f22`;
- Mathlib: `065356127b1dc0016f66b7283ce0ce2c4055aa55`;
- Lean: `leanprover/lean4:v4.35.0-rc2`.

## 2. Important sign correction

The natural low-phase consequence of a deep negative terminal message is an
**upper bound** on the dyadically weighted occupancies, not a lower bound.

This follows from the already-formal identity

`deficit (activeScan m xs)
 = 2^(xs.length) * deficit m - dyadicInputCost xs`.

Occupancy offsets deficit growth. Therefore, if the terminal message is very
negative, the terminal deficit is large and the weighted occupancy cost must
be small enough.

This is the deterministic restriction needed later for a probability upper
bound.

## 3. New scalar consequences

New module: `ProbStack/PathDeep.lean`.

The scalar helper

- `activeScan_append`

makes finite block concatenation explicit.

The weighted necessity lemmas are:

- `dyadicInputCost_le_of_lowRun_deficit_ge`;
- `dyadicInputCost_le_of_lowRun_message_le`.

The second says that, under `LowRun m xs`, if

`activeScan m xs <= -H`,

then

`dyadicInputCost xs
 <= 2^(xs.length) * deficit m - (H + 3)`.

The term `H+3` is exact because `deficit z = 3-z`.

The explicit `LowRun` hypothesis has not been falsely removed.

## 4. Exact weighting convention

For a list

`xs = [X₁, ..., X_k]`,

the existing `dyadicInputCost` is

`2^k X₁ + 2^(k-1) X₂ + ... + 2 X_k`.

Thus the first occupancy encountered in the low run receives the largest
coefficient, and the last receives coefficient `2`.

There is no coefficient-`1` terminal term.

## 5. Genuine left-oriented branch block

`LeftPath.leftBlockValues C start len` records the occupancies encountered
after the genuine branch rooted at `start` while moving inward to the branch
rooted at `start+len`:

`[C(start+1), ..., C(start+len)]`.

Formal results:

- `LeftPath.leftBlockValues_length`;
- `LeftPath.leftBranch_branchMessage_eq_activeScan_block`;
- `LeftPath.leftBranch_dyadicInputCost_le_of_deep`.

The block-scan theorem is the unconditional structural reduction, conditional
only on the starting branch being active with message `some m`: the actual
TreeStack branch message at the end is exactly the corresponding
`activeScan`.

The deep theorem then adds the mathematically necessary `LowRun` hypothesis.
If the ending actual branch message is `some z` with `z <= -H`, the
explicit dyadic occupancy bound above follows.

## 6. Genuine right-oriented branch block

The symmetric development is formal in the existing reversed finite
coordinate.

`RightPath.rightBlockValues C start len` records

`[C((start+1).rev), ..., C((start+len).rev)]`.

Formal results:

- `RightPath.rightBlockValues_length`;
- `RightPath.rightBranch_branchMessage_eq_activeScan_block`;
- `RightPath.rightBranch_dyadicInputCost_le_of_deep`.

Thus both orientations of finite path edges now have the same exact
deep-low-run necessity theorem attached to genuine
`TreeStack.OrientedBranch.branchMessage` values.

## 7. Genuine regeneration step

The existing scalar interval theorem `regeneration_transfer_window` has now
been attached to actual branch messages.

Formal results:

- `LeftPath.leftBranch_regeneration_step`;
- `RightPath.rightBranch_regeneration_step`.

If an actual incoming branch message is `some M` with

`-mu < M <= 2*mu`, `1 <= mu`,

and the next genuine occupancy lies in

`2*mu + 2 - M <= X <= 4*mu - M`,

then the next genuine branch message is `some M'` with

`mu <= M' <= 2*mu`.

This is the first Session 12 reset/regeneration theorem on actual path
branches.

## 8. What has not yet been formalised

No explicit front/event structure was added in Session 12.

The remaining deterministic work before entering probability is to package
the genuine regeneration step together with deep-seed growth/runaway and an
irreversible-front certificate in explicit finite-block form suitable for
later counting.

## 9. EMPTY semantics

All new block theorems start from an actual active message `some m`; no
arithmetic surrogate for EMPTY was introduced.

`TreeStack.EMPTY = none` remains categorical and distinct from `some 0`.

## 10. Validation

The promoted source checkpoint

`c45929a59a85db49dcf15e22498105361819309b`

was built successfully by GitHub Actions run

`36275694471`.

That run used the exact pinned package workflow, including the full
`lake build` and the project grep rejecting `sorry` or `axiom`.

The exact documentation-inclusive final HEAD is validated separately after
these notes are committed; its SHA and exact-head Actions run are reported in
the end-of-session handover response so that the validated head is not changed
after validation.
