# Session 24 — Palomar packaging

Date: 2026-09-28

Status at note creation: packaging and module migration complete; final predictive
FULL preflight is the remaining gate.  This note does not register with Palomar
and does not begin paper or arXiv preparation.

## Starting point

- Session 23 start for this session:
  `6b58462042a41125bd8d113168bb51276b2940ef`
- branch:
  `session-24-palomar-packaging`
- branch remains unmerged; main was not modified.

## Current Palomar revisions inspected

Rechecked at the beginning of Session 24:

- PalomarPolicy:
  `96b034cc31a72a63d4f4041911dce337a85c9a04`
- PalomarTemplate:
  `2891de4c48955af824969a263d31b25e7a9a1406`
- PalomarSubmission:
  `65f0154ed776cd26c224254aa57b379137f28b0d`

The current minimum supported Lean toolchain is:

`leanprover/lean4:v4.35.0-rc2`

The current metadata schema remains:

`formalization.yaml v0.4`

The reusable predictive verifier is
`PalomarRegistry/PalomarSubmission/.github/workflows/submission.yml`, pinned
to the exact PalomarSubmission SHA above, with `mode: full`.

Current Comparator policy permits only:

- `propext`
- `Quot.sound`
- `Classical.choice`

The Challenge transitive source closure may use only canonical statement
dependencies.  The selected Challenge therefore imports Mathlib only.

## Challenge design

The protected Challenge is `Challenge.lean`.

Exact import:

`public import Mathlib`

The Challenge defines a finite path configuration directly as
`Fin n -> Nat`, defines ordinary legal path pebbling reachability and
support-collapse stackability, and defines the exact categorical path message
recursion using `Option Int`.

The transfer function is the exact five-case TreeStack transfer.

`none` is EMPTY and is not identified with `some 0`.

The directed-message function uses:

- the forward prefix scan for an edge whose tail is immediately left of its
  head;
- the prefix scan of the reversed configuration for the opposite orientation.

Thus both ordered path orientations are represented.

No score-nonpositivity surrogate is used as the Challenge event.

### Advertised theorem 1

`ProbStack.Palomar.nonstackable_exists_directedMessage_le`

```lean
theorem nonstackable_exists_directedMessage_le
    {n h : Nat} (hn2 : 2 <= n)
    (C : Configuration n)
    (hmassPos : 0 < mass C)
    (hnonstack : ¬ Stackable C)
    (hh : 2 <= h)
    (hlarge : (n - 1) * (h / 2 + 1) < mass C) :
    ∃ (r u : Fin n)
        (hu : (SimpleGraph.pathGraph n).Adj u r)
        (m : Int),
      directedMessage C u r = some m ∧
        m <= -(h : Int)
```

### Advertised theorem 2

`ProbStack.Palomar.nonstackable_total_mul_exists_directedMessage_le`

```lean
theorem nonstackable_total_mul_exists_directedMessage_le
    {n mu : Nat} (hn2 : 2 <= n)
    (C : Configuration n)
    (hmu : 1 <= mu)
    (hmass : mass C = n * mu)
    (hnonstack : ¬ Stackable C) :
    ∃ (r u : Fin n)
        (hu : (SimpleGraph.pathGraph n).Adj u r)
        (m : Int),
      directedMessage C u r = some m ∧
        m <= -(2 * (mu : Int) - 1)
```

The Challenge is 142 lines, below Palomar's 1,000-line / 100-KiB limit.

Its transitive submitted-source closure is just `Challenge.lean`; imported
statement dependencies are Mathlib.  It does not import ProbStack or TreeStack.

## Solution design

`Solution.lean` imports `ProbStack` and duplicates the protected definitions
under the same advertised namespace for Comparator.

It proves explicit bridge facts:

- Challenge mass = `TreeStack.mass`;
- Challenge operational stackability = `TreeStack.Stackable` on
  `SimpleGraph.pathGraph n`;
- Challenge prefix scan = `ProbStack.LeftPath.prefixScan`;
- Challenge directed message on each ordered adjacent pair = the actual
  TreeStack incident-branch message.

The two advertised theorems are then proved by reusing:

- `ProbStack.nonstackable_exists_directedMessage_le`;
- `ProbStack.nonstackable_total_mul_exists_directedMessage_le`.

No P6 theorem statement was changed.

## Comparator

`comparator.json` compares exactly the two advertised theorems:

- `ProbStack.Palomar.nonstackable_exists_directedMessage_le`;
- `ProbStack.Palomar.nonstackable_total_mul_exists_directedMessage_le`.

It also compares the concrete Challenge definitions needed by the theorem
types: configuration, mass, transfer, Message/EMPTY, path step/prefix/reversal,
directed message, legal move/reachability, and stackability.

Permitted axioms are exactly the three policy axioms above.

The local validation workflow runs Comparator with the submitted Lean
toolchain and registers the bundled NanoDa and con-ron kernels exactly as the
current PalomarTemplate verifier script does.

## Required module-system migration

Current Palomar policy requires every regular submitted `.lean` file to use
Lean's module system.

All regular ProbStack Lean files were migrated with:

- a `module` header;
- `public import` for their existing imports;
- exposed public sections needed to preserve prior cross-module definitional
  use.

No namespace or public declaration was renamed.

The files migrated are:

- `ProbStack.lean`
- `ProbStack/TreeStackBoundary.lean`
- `ProbStack/Path.lean`
- `ProbStack/PathMessage.lean`
- `ProbStack/PathBranch.lean`
- `ProbStack/TransferBounds.lean`
- `ProbStack/Deficit.lean`
- `ProbStack/PathBridge.lean`
- `ProbStack/PathDeep.lean`
- `ProbStack/PathFront.lean`
- `ProbStack/PathNecessity.lean`
- `ProbStack/FiniteProbability.lean`
- `ProbStack/FiniteDyadic.lean`

The new `Challenge.lean` and `Solution.lean` are modules from creation.

### TreeStack compatibility exception

The frozen Session 23 TreeStack pin was:

`f4112f08d42a37c0941bf469ac124621b1f54f22`.

After the ProbStack module migration, Lean 4.35 produced the exact error:

`cannot import non-module TreeStack.Basic from module`.

Therefore Palomar compatibility is technically impossible with the frozen
TreeStack source revision.

A dedicated unmerged TreeStack compatibility branch was created directly from
that exact semantic base.  Only the seven transitive TreeStack source files
imported by ProbStack were migrated to module headers/public visibility:

- `TreeStack/Basic.lean`
- `TreeStack/Transfer.lean`
- `TreeStack/Branch.lean`
- `TreeStack/Message.lean`
- `TreeStack/PebblingMove.lean`
- `TreeStack/Boundary.lean`
- `TreeStack/RootScore.lean`

The exact compatibility revision is:

`8fc9fc37a200855ec22579beaeec8f12f94f0310`.

It is seven commits ahead of the semantic base and changes only those seven
files by module/import/visibility syntax.  No TreeStack theorem statement or
mathematical definition was intentionally changed.

ProbStack is pinned to this immutable compatibility revision.

Mathlib remains exactly:

`065356127b1dc0016f66b7283ce0ce2c4055aa55`.

Lean remains exactly:

`leanprover/lean4:v4.35.0-rc2`.

The permanent workflow remains
`.github/workflows/lean-bootstrap.yml`; its validation commands were not
weakened.  Only the TreeStack cache key was updated to the compatibility pin.

## Metadata / provenance

`formalization.yaml` uses v0.4.

Humans only are listed as authors and responsible maintainers.

Substantial AI assistance is disclosed under `automation`, including the
model/framework and the human-directed workflow.

No independent peer review is claimed.

No novelty, priority, first-proof, or publication-acceptance claim is made.

The source description distinguishes:

- Csernák-Soukup: exact deterministic support-collapse stackability event and
  worst-case stacking context;
- Bushaw-Kettle: same fixed-total weak-composition law and close path
  asymptotics for a different event, solvability;
- TreeStack: earlier structural root-score certificate and Palomar entry
  `PALOMAR-2026-09-25-000010`;
- ProbStack P6: deterministic quantitative necessity theorem forcing a deep
  actual directed message.

The project root licence is Apache-2.0.

## Validation chronology

Mechanical diagnostic run `36485272916` failed before the module-compatible
TreeStack pin, with the exact non-module import error above.

Diagnostic run `36485944085` passed the module-compatible ProbStack build
through P6 and exposed only `Solution.lean` bridge-proof errors.

Those bridge proofs were repaired without changing the advertised theorem
types.

Diagnostic run `36486967431` then passed:

- the module-header check;
- the exact pinned TreeStack target build;
- full `lake build`;
- `lake build Challenge Solution`;
- the no-`sorry` / no-project-`axiom` check over `ProbStack/` and
  `ProbStack.lean`.

Its Python suite reached 121/122 tests and failed only because the old Session
19 invariant still demanded the pre-module TreeStack SHA.  That test was
updated to retain `f4112...` as the semantic base while requiring the
documented compatibility pin.

The final candidate workflow additionally runs:

- `PYTHONPATH=. pytest -q`;
- the current PalomarTemplate v0.4 metadata validator;
- local `lake comparator` with Lean kernel, NanoDa, and con-ron;
- the official PalomarSubmission reusable workflow in `mode: full`.

## Immutable final-preflight record

The registration candidate must be the exact final commit after this note and
the handover note are committed.

A Git commit cannot contain its own SHA, and a workflow run ID does not exist
until after that commit is created.  Therefore the exact final candidate SHA,
final FULL-preflight run ID, mechanical-report artifact id/name, profile
id/digest, licence result, Comparator result, allowed-axiom report, and
independent-kernel results are recorded in the external end-of-session report
after the final immutable run.  No repository file is changed after that final
preflight.

No Palomar registration is performed automatically.
