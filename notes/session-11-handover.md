# Session 11 handover

## Validated state

Session 11 started from ProbStack `main`:

`06d9f077e59c4e129a3628d40aadc2c378889a7f`.

Pinned dependencies remain unchanged:

- TreeStack: `f4112f08d42a37c0941bf469ac124621b1f54f22`;
- Mathlib: `065356127b1dc0016f66b7283ce0ce2c4055aa55`;
- Lean: `leanprover/lean4:v4.35.0-rc2`.

The complete Session 11 Lean source was CI-validated at

`626b73a3e4192eb55dd63f45a4a30f1ee5f33d1e`

by Actions run `36273215404`.

## What is now formal

### A2 — path recurrence

**FORMAL.**

New generic recursion bridge in `ProbStack/PathBranch.lean`:

- `PathBranch.branchMessage_eq_pathStep_empty_of_noChildren`;
- `PathBranch.branchMessage_eq_pathStep_of_uniqueChild`.

New path-specific bridge in `ProbStack/PathBridge.lean`:

- `LeftPath.leftBranch_branchMessage_eq_prefixScan`;
- `RightPath.rightBranch_branchMessage_eq_reversePrefixScan`.

Left orientation: root `k`, parent `k+1`, branch is the prefix
`0,...,k`.

Right orientation: reversed coordinate root `Fin.rev k`, parent
`Fin.rev (k+1)`, branch is the suffix from that root to the right endpoint.

Both are on the existing Mathlib `SimpleGraph.pathGraph n`.

### A3 — EMPTY behavior

**FORMAL.**

- `pathStep_eq_empty_iff`;
- `LeftPath.prefixScan_eq_empty_iff`;
- `LeftPath.leftBranch_branchMessage_eq_empty_iff`;
- `RightPath.rightBranch_branchMessage_eq_empty_iff`.

EMPTY remains exactly `none`; no theorem identifies it with `some 0`.

### A6 — low-phase deficit

**FORMAL and attached to actual TreeStack branch messages.**

- `LeftPath.leftBranch_deficit_succ_of_low`;
- `RightPath.rightBranch_deficit_succ_of_low`.

### A7 — finite closed form

**FORMAL.**

New definitions:

- `activeScan`;
- `LowRun`;
- `dyadicInputCost`.

Main theorem:

- `deficit_activeScan_of_lowRun`.

For `[X₁,...,X_k]`, this gives the dyadic weighting
`2^k X₁ + 2^(k-1) X₂ + ... + 2 X_k`.

## Other statuses

- A4: FORMAL, unchanged.
- A5: FORMAL, unchanged.
- B3: FORMAL, unchanged.
- B4: FORMAL, unchanged.

No new `sorry` or project-added `axiom` exists.

## Files added/changed by the validated source

Added:

- `ProbStack/PathBranch.lean`;
- `ProbStack/PathBridge.lean`.

Changed:

- `ProbStack.lean`;
- `ProbStack/PathMessage.lean`;
- `ProbStack/Deficit.lean`.

Session documentation adds this handover and
`notes/session-11-path-message-bridge.md`.

## Important implementation lessons

Use the generic no-child/unique-child bridge rather than repeatedly unfolding
TreeStack recursion.

For path `Fin` arithmetic, normalize explicit root/parent values before
calling `omega`.

Use `Fin.rev` as an indexing device for the right-hand orientation; do not
introduce a second path graph.

## Frozen theorem

The frozen headline theorem is unchanged. There is still no assertion at
`ε=0`, no critical-window theorem, and no alteration to
`StackableAt(T,C,r) iff 0 < score(T,C,r)`.

## Session 12

The next session should stay deterministic.

Best target:

**formalise weighted prefix/suffix mass bounds and deep-message necessity for
the genuine left/right TreeStack path messages, then begin the
reset/regeneration/front layer.**

Do not start the probability layer until those structural lemmas are in place.
