# Session 11 — formal path-message bridge

Status: **A2/A3/A6/A7 FORMAL; BOTH PATH ORIENTATIONS COMPILE.**

## 1. Scope

Session 11 closed the deterministic gap between ProbStack's scalar `pathStep`
recurrence and TreeStack's actual recursive
`TreeStack.OrientedBranch.branchMessage` on `SimpleGraph.pathGraph n`.

No probability, weak-composition, binary-partition, asymptotic, prior-art, or
paper work was started. The frozen headline theorem was not changed.

## 2. Verified starting state

Starting ProbStack `main` HEAD:

`06d9f077e59c4e129a3628d40aadc2c378889a7f`.

Pinned TreeStack:

`f4112f08d42a37c0941bf469ac124621b1f54f22`.

Inherited Mathlib:

`065356127b1dc0016f66b7283ce0ce2c4055aa55`.

Lean toolchain:

`leanprover/lean4:v4.35.0-rc2`.

The exact TreeStack definitions inspected were the pinned
`OrientedBranch`, `Child`, `childBranch`, `vertices`,
`branchMessage`, `childMessageSum`, `effectiveInput`,
`messageContribution`, `Message = Option ℤ`, `EMPTY = none`, and `F`.

## 3. Generic unique-child bridge

A new module `ProbStack/PathBranch.lean` isolates the only TreeStack recursion
facts needed by a path.

Definitions:

- `PathBranch.NoChildren`;
- `PathBranch.UniqueChild`.

Main theorems:

- `occupied_iff_root_of_noChildren`;
- `childMessageSum_eq_zero_of_noChildren`;
- `branchMessage_eq_pathStep_empty_of_noChildren`;
- `occupied_iff_root_or_uniqueChild`;
- `childMessageSum_eq_uniqueChild`;
- `branchMessage_eq_pathStep_of_uniqueChild`.

The key result is the last theorem: if an oriented branch has one genuine
child, then its actual recursive `branchMessage` is exactly one
`pathStep` applied to the child branch's actual message and the root
configuration value. If it has no child, the actual message is exactly
`pathStep EMPTY` at the root.

This proof preserves categorical EMPTY throughout. `none` is never replaced
by `some 0`.

## 4. Scalar EMPTY theorem

`ProbStack/PathMessage.lean` now also contains:

- `pathStep_eq_empty_iff`.

It proves exactly

`pathStep m x = EMPTY ↔ m = EMPTY ∧ x = 0`.

Thus an active integer message can never become categorical EMPTY, while an
EMPTY state persists exactly across a zero input.

## 5. Left-oriented path bridge

`ProbStack/PathBridge.lean` defines the canonical left-oriented branch

`leftBranch n hn k hk`

with root index `k` and parent index `k+1`, under `k+1<n`. Its branch is
the path prefix from `0` through `k`.

The scalar scan is

`LeftPath.prefixScan C k hk`,

which starts with `pathStep EMPTY (C 0)` and then iterates `pathStep`
through the values at indices `1,...,k`.

Geometry/recursion lemmas:

- `leftBranch_zero_noChildren`;
- `leftChildSucc`;
- `leftBranch_succ_uniqueChild`;
- `childBranch_leftChildSucc`.

Main bridge:

- `leftBranch_branchMessage_eq_prefixScan`.

This is the requested general finite theorem: for every legal prefix index
`k`, the actual TreeStack recursive branch message equals the corresponding
finite scalar scan.

The exact one-step structural recurrence is also exposed as:

- `leftBranch_branchMessage_succ`;
- `leftBranch_branchMessage_succ_some`.

## 6. Right-oriented path bridge

The opposite orientation is formal too.

`RightPath.rightBranch n hn k hk` uses reversed path coordinates:
its root is `Fin.rev k` and its parent is `Fin.rev (k+1)`. Thus `k=0`
is the right endpoint and increasing `k` scans inward from the right.

`RightPath.reverseConfig C i := C i.rev`.

Geometry/recursion lemmas:

- `rightBranch_zero_noChildren`;
- `rightChildSucc`;
- `rightBranch_succ_uniqueChild`;
- `childBranch_rightChildSucc`.

Main bridge:

- `rightBranch_branchMessage_eq_reversePrefixScan`.

It identifies the actual right-oriented TreeStack branch message with
`LeftPath.prefixScan (reverseConfig C)`.

The exact right one-step recurrence is:

- `rightBranch_branchMessage_succ`.

No competing path graph was introduced; `Fin.rev` is only an indexing device
on the same Mathlib `SimpleGraph.pathGraph n`.

Together the left and right forms cover the two orientations of every edge of
a finite path.

## 7. Structural EMPTY behavior

The scalar scan classification is:

- `prefixScan_eq_empty_iff`.

For the left branch:

- `leftBranch_branchMessage_eq_empty_iff`.

It states that the actual branch message is EMPTY exactly when every path
vertex with index at most `k` has configuration value zero.

For the right branch:

- `rightBranch_branchMessage_eq_empty_iff`.

It states the same fact in reversed coordinates: every vertex whose reversed
index is at most `k` has value zero.

These are structural TreeStack theorems derived through the bridge, not merely
facts about the scalar model.

## 8. Genuine-message low-phase recurrence

The existing scalar theorem

- `deficit_activeStep_of_low`

has now been attached to actual path branch messages.

Left:

- `leftBranch_deficit_succ_of_low`.

Right:

- `rightBranch_deficit_succ_of_low`.

If the previous actual branch message is `some m` and the next effective
input remains in the low phase, the next actual branch message is an integer
message whose deficit satisfies

`Z' = 2 * (Z - X)`.

Thus A6 is no longer only an isolated scalar calculation.

## 9. General finite low-phase closed form

`ProbStack/Deficit.lean` now defines:

- `activeScan`;
- `LowRun`;
- `dyadicInputCost`.

The theorem

- `deficit_activeScan_of_lowRun`

proves the finite iterated identity

`deficit (activeScan m xs)
 = 2^(length xs) * deficit m - dyadicInputCost xs`

for every low-phase run.

For inputs `[X₁,...,X_k]`, the recursive `dyadicInputCost` is exactly the
weighted sum with coefficients

`2^k, 2^(k-1), ..., 2`.

The indexing was checked at the first two lengths:

- `k=1`: `Z₁ = 2 Z₀ - 2 X₁`;
- `k=2`: `Z₂ = 4 Z₀ - 4 X₁ - 2 X₂`.

The latter agrees with the pre-existing theorem
`deficit_two_steps_of_low`.

## 10. Lean/API facts worth retaining

1. The cleanest bridge is not to unfold TreeStack's recursive definition on
   every path index. Prove generic no-child/unique-child lemmas once, then
   prove path geometry separately.

2. `Fintype.sum_eq_single` is cleaner than a dependent `Finset.sum_eq_single`
   proof for `childMessageSum`, because child records contain proof fields.

3. `omega` does not always unfold `Fin` structure projections automatically.
   Explicit `change` or simplification of root/parent values is more robust.

4. The right orientation is substantially cleaner when indexed with
   `Fin.rev` rather than repeated natural-number subtraction.

5. In the right base case, `reverseConfig C 0` needed an explicit
   definitional reduction before rewriting by root equality.

6. An early long base64 scratch-CI attempt failed before Lean because the
   payload transport was invalid. Subsequent validation used real branch
   source files; that transport failure has no mathematical significance.

## 11. Validation

The complete source tree containing both path orientations, A3, A6, and A7 was
validated at branch commit

`626b73a3e4192eb55dd63f45a4a30f1ee5f33d1e`.

GitHub Actions run:

`36273215404`.

The workflow completed successfully, including:

- exact Lean/TreeStack/Mathlib resolution;
- `lake build @treestack/+TreeStack.RootScore`;
- full `lake build`;
- project grep rejecting any ProbStack `sorry` or `axiom`.

There is no new `sorry` and no project-added `axiom`.

The temporary Session 11 branch-only CI modifications and scratch files were
removed after source validation.

## 12. A/B layer status after Session 11

- **A2 path recurrence: FORMAL.** Both left-prefix and right-suffix actual
  TreeStack branch messages are identified with finite scalar scans.
- **A3 EMPTY behavior: FORMAL.** Actual branch EMPTY is classified exactly by
  zero occupation of the corresponding path side.
- **A4 global half-bound: FORMAL.** Unchanged from Session 10.
- **A5 positive-phase identities: FORMAL.** Unchanged from Session 10.
- **A6 low-phase deficit recurrence: FORMAL and structurally connected.**
- **A7 general low-phase closed form: FORMAL.**
- **B3 regeneration interval arithmetic: FORMAL.** Unchanged.
- **B4 transfer-window lemma: FORMAL.** Unchanged.

## 13. What was deliberately not started

No probability-space formalisation, weak-composition measures, conditioning,
geometric approximation, binary partitions, asymptotics, final headline
theorem assembly, prior-art audit, or paper drafting was started.

The frozen headline theorem and its `ε>0` formulation remain unchanged.

## 14. Recommended Session 12 target

The single best next target is the remaining deterministic prefix/suffix mass
and deep-message layer:

1. derive a reusable weighted-mass bound from a sufficiently negative actual
   left/right path branch message;
2. formalise the corresponding deep-message necessity statement;
3. use those results to begin the reset/regeneration/front layer.

Do not enter probability until those deterministic structural lemmas are
stable.
