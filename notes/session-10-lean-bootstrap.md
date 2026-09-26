# Session 10 — Lean bootstrap and deterministic path core

Status: **PINNED LEAN PACKAGE COMPILES; HEADLINE THEOREM NOT FORMALLY VERIFIED.**

## 1. Scope

Session 10 was deliberately limited to the first implementation layer:

- bootstrap the exact Lean/TreeStack/Mathlib dependency boundary;
- wrap Mathlib's path graph as a `TreeStack.FiniteTree`;
- define the scalar categorical path-message step;
- formalise low-risk transfer, deficit and regeneration arithmetic;
- compile everything with no local `sorry` or `axiom`.

No probability layer, binary partitions, local excursion asymptotics, conditioning,
or final headline theorem was attempted.

The frozen Session 8 headline theorem is unchanged and remains the formalisation
target.

## 2. Verified starting state

The session verified the starting ProbStack `main` HEAD as

`595566b350a6a5b93dd6184dc3bbb99e162e9c7c`.

The authoritative external dependency is

`TreeStack-Structural-Certificates-for-Stacking-on-Trees`
at
`f4112f08d42a37c0941bf469ac124621b1f54f22`.

## 3. Exact toolchain and resolved dependency state

GitHub Actions supplied the compiler because the local execution shell had no
Lean/Lake/elan installation and could not resolve github.com directly.

Literal CI version output:

```text
Lean (version 4.35.0-rc2, x86_64-unknown-linux-gnu,
  commit 11acb17ec6b07a8f9e9173e6845197929540936b, Release)
Lake version 5.0.0-src+11acb17 (Lean version 4.35.0-rc2)
elan 4.2.4 (227caca13 2026-08-25)
```

The repository `lean-toolchain` is exactly:

```text
leanprover/lean4:v4.35.0-rc2
```

The resolved Lake manifest printed in CI confirms:

- TreeStack revision:
  `f4112f08d42a37c0941bf469ac124621b1f54f22`;
- inherited Mathlib revision:
  `065356127b1dc0016f66b7283ce0ce2c4055aa55`.

## 4. Exact Lake configuration

```lean
import Lake

open Lake DSL

package "probstack" where
  leanOptions := #[⟨`autoImplicit, false⟩]

require treestack from git
  "https://github.com/jfairfaxball-348/TreeStack-Structural-Certificates-for-Stacking-on-Trees.git" @
  "f4112f08d42a37c0941bf469ac124621b1f54f22"

@[default_target]
lean_lib ProbStack
```

ProbStack does not declare a competing Mathlib dependency. Mathlib is inherited
through the pinned TreeStack package.

## 5. Files added or changed

Lean/package infrastructure:

- `lean-toolchain`;
- `lakefile.lean`;
- `ProbStack.lean`;
- `ProbStack/TreeStackBoundary.lean`;
- `ProbStack/Path.lean`;
- `ProbStack/PathMessage.lean`;
- `ProbStack/TransferBounds.lean`;
- `ProbStack/Deficit.lean`;
- `.github/workflows/lean-bootstrap.yml`.

Session documentation:

- `notes/session-10-lean-bootstrap.md`;
- `notes/session-10-handover.md`.

## 6. TreeStack import boundary

`ProbStack/TreeStackBoundary.lean` imports exactly:

```lean
import TreeStack.Basic
import TreeStack.Transfer
import TreeStack.Branch
import TreeStack.Message
import TreeStack.PebblingMove
import TreeStack.RootScore
```

No TreeStack semantic definition is duplicated.

In particular ProbStack reuses:

- `TreeStack.Configuration`;
- `TreeStack.mass`;
- `TreeStack.FiniteTree`;
- `TreeStack.F`;
- `TreeStack.Message`;
- `TreeStack.EMPTY`;
- `TreeStack.OrientedBranch.branchMessage`;
- `TreeStack.OrientedBranch.messageContribution`;
- `TreeStack.OrientedBranch.effectiveInput`;
- `TreeStack.score`;
- `TreeStack.StackableAt`;
- `TreeStack.stackableAt_iff_score_pos`;
- `TreeStack.not_stackable_iff_all_scores_nonpos`.

The theorem `ProbStack.empty_ne_some_zero` is a direct wrapper around
`TreeStack.empty_ne_integer_zero`, preserving the categorical distinction
between `none` and `some 0`.

## 7. Path finite-tree wrapper

The graph is exactly Mathlib's

`SimpleGraph.pathGraph n : SimpleGraph (Fin n)`.

The wrapper is:

```lean
noncomputable def pathTree (n : ℕ) (hn : 0 < n) :
    TreeStack.FiniteTree (Fin n) where
  graph := SimpleGraph.pathGraph n
  isTree := ⟨pathGraph_connected_of_pos hn, pathGraph_isAcyclic n⟩
```

and `pathTree_graph` is a simp lemma proving the graph field is definitionally
the Mathlib path graph.

### Acyclicity proof

No second path graph was introduced.

For a hypothetical cycle in `pathGraph n`, the proof:

1. takes the maximum vertex in the finite support of the cycle;
2. rotates the cycle to start/end at that maximum;
3. uses `SimpleGraph.pathGraph_adj` plus maximality to show both the second
   and penultimate vertices are the unique predecessor of the maximum;
4. concludes those two vertices are equal;
5. contradicts `IsCycle.snd_ne_penultimate`.

Connectedness uses Mathlib's `SimpleGraph.pathGraph_connected k` after
splitting a positive `n` as a successor.

## 8. Scalar categorical path recurrence

The new wrapper is:

```lean
def pathStep (m : TreeStack.Message) (x : Nat) : TreeStack.Message :=
  match m with
  | none =>
      if x = 0 then TreeStack.EMPTY
      else some (TreeStack.F (x : Int))
  | some z => some (TreeStack.F (z + (x : Int)))
```

This preserves EMPTY categorically.

Compiled local behavior:

- `pathStep_empty_zero`;
- `pathStep_empty_pos`;
- `pathStep_some`.

**Important limitation:** Session 10 did not prove the general prefix theorem
identifying this scalar scan with
`TreeStack.OrientedBranch.branchMessage` on Mathlib path prefixes. Therefore
the scalar recurrence is not yet claimed as a formally connected replacement
for TreeStack branch messages. That equivalence is the first Session 11 target.

## 9. New theorem inventory

### Boundary / path

- `empty_ne_some_zero`: `TreeStack.EMPTY ≠ some 0`.
- `pathGraph_isAcyclic`: every Mathlib path graph is acyclic.
- `pathGraph_connected_of_pos`: positive-size Mathlib path graphs are connected.
- `pathTree_graph`: the wrapper graph is exactly `SimpleGraph.pathGraph n`.

### Scalar messages

- `pathStep_empty_zero`;
- `pathStep_empty_pos`;
- `pathStep_some`.

### Transfer bounds

- `F_le_half`: for every integer `x`,
  `TreeStack.F x ≤ x / 2` with Lean integer division.
- `F_eq_half_of_ge_four_even`;
- `F_eq_shifted_half_of_ge_five_odd`;
- `steering_input_window`;
- `F_mem_mu_two_mu`;
- `regeneration_transfer_window`.

The transfer-window proof handles Lean integer division explicitly through
`Int.le_ediv_iff_mul_le` and `Int.ediv_le_of_le_mul`.

### Low phase

Definitions:

- `activeStep`;
- `deficit`.

Theorems:

- `deficit_activeStep_of_low`:
  if `m + x ≤ 1`, then
  `deficit (activeStep m x) = 2 * (deficit m - x)`;
- `deficit_two_steps_of_low`:
  the exact two-step dyadic sanity identity.

## 10. A/B layer status

- **A2 path recurrence:** PARTIAL. Scalar recurrence is defined and compiled;
  the general branch-message equivalence is not yet proved.
- **A3 EMPTY behavior:** PARTIAL. Local EMPTY persistence/activation for
  `pathStep` is formal; prefix/suffix statements await A2.
- **A4 global half-bound:** FORMAL.
- **A5 positive-phase identities:** FORMAL path-friendly wrappers around the
  TreeStack parity theorems.
- **A6 low-phase deficit recurrence:** FORMAL.
- **A7 low-phase closed form:** PARTIAL. Exact two-step theorem is formal; the
  general finite iterated sum remains.
- **B3 regeneration interval arithmetic:** FORMAL via
  `steering_input_window`.
- **B4 transfer-window lemma:** FORMAL via `F_mem_mu_two_mu` and
  `regeneration_transfer_window`.

## 11. Exact Lean commands used in CI

The validating workflow ran:

```text
lean --version
lake --version
elan --version
lake update
cat lake-manifest.json
lake build @treestack/+TreeStack.RootScore
lake build
```

During isolated source development it additionally used:

```text
lake env lean /tmp/ProbStackScratch.lean
```

Scratch commits were used only to obtain compiler feedback before promoting
source into repository files.

## 12. Build result

Validated source/audit commit before this documentation commit:

`4631e822ee7707c0f7ec89b239e5991dd6dfdec1`.

Literal final source build result at that commit:

```text
Build completed successfully (8937 jobs).
...
Built ProbStack.TreeStackBoundary
Built ProbStack.Path
Built ProbStack.PathMessage
Built ProbStack.TransferBounds
Built ProbStack.Deficit
Built ProbStack
Build completed successfully (8945 jobs).
```

The CI placeholder audit also completed successfully: no local ProbStack Lean
source matched `sorry` or `axiom`.

## 13. Python status

No Python mathematics was changed.

No Python tests, Monte Carlo runs or large experiments were run in Session 10,
because the work was confined to Lean/package infrastructure and exact
deterministic formalisation.

Mathematical theorem status, prior Python validation status and Lean compilation
status remain separate.

## 14. Documentation/source files inspected

ProbStack:

- `notes/session-9-formalisation-design.md`;
- `notes/session-9-handover.md`.

Pinned TreeStack:

- `lakefile.lean`;
- `lean-toolchain`;
- `TreeStack/Basic.lean`;
- `TreeStack/Transfer.lean`;
- `TreeStack/Branch.lean`;
- `TreeStack/Message.lean`;
- `TreeStack/RootScore.lean`.

Pinned Mathlib:

- `Mathlib/Combinatorics/SimpleGraph/Hasse.lean`;
- `Mathlib/Combinatorics/SimpleGraph/Acyclic.lean`;
- `Mathlib/Combinatorics/SimpleGraph/Walk/Traversal.lean`;
- `Mathlib/Combinatorics/SimpleGraph/Walk/Decomp.lean`;
- `Mathlib/Combinatorics/SimpleGraph/Paths.lean`;
- `Mathlib/Data/Finset/Max.lean`.

Tooling documentation:

- `leanprover/lean-action` README was checked while designing the CI route,
  although the final workflow uses direct elan installation.

No mathematical literature/prior-art search was conducted.

## 15. Unexpected Lean-semantic findings

There was no mathematical mismatch with the informal deterministic proof.

Two implementation details mattered:

1. `F_le_half` compiles exactly with Lean's integer division semantics, so no
   replacement by real division is needed.
2. The regeneration transfer-window bounds were made explicit through the
   integer-division lemmas rather than leaving the division step implicit.

The only substantive uncompleted connection is structural rather than
arithmetic: the scalar `pathStep` still needs a theorem identifying it with
TreeStack's recursive `branchMessage` on oriented Mathlib path prefixes.

## 16. Theorem status

The frozen headline theorem remains mathematically unchanged.

It is **not** formally verified by Session 10.

Session 10 verifies only the package boundary and the deterministic lemmas
listed above.

## 17. Decision and next step

**YES — the frozen headline theorem is still the correct formalisation target.**

The single best next step is to prove the general path-prefix equivalence
between the scalar `pathStep` scan and
`TreeStack.OrientedBranch.branchMessage`. Once that theorem compiles, use it
to lift EMPTY behavior and the low-phase recurrence from the scalar layer to
actual TreeStack path branches before proceeding to fronts/regeneration.
