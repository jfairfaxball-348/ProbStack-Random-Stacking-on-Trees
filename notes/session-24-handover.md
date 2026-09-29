# Session 24 handover — Palomar packaging and preflight

Date: 2026-09-28

## Scope

This session is limited to Palomar packaging, required module migration, and
predictive mechanical preflight for the already-formalized P6 theorem.

No paper drafting, arXiv preparation, P5 formalization, random-theorem
formalization, or Palomar registration is performed.

## Repository state

Starting SHA:

`6b58462042a41125bd8d113168bb51276b2940ef`

Branch:

`session-24-palomar-packaging`

Merge status:

unmerged; main was not modified.

The exact final branch SHA and final FULL-preflight run are recorded in the
end-of-session report because a commit cannot self-contain its own SHA or a
future GitHub Actions run ID.

## Current Palomar baseline

- PalomarPolicy:
  `96b034cc31a72a63d4f4041911dce337a85c9a04`
- PalomarTemplate:
  `2891de4c48955af824969a263d31b25e7a9a1406`
- PalomarSubmission:
  `65f0154ed776cd26c224254aa57b379137f28b0d`
- minimum Lean:
  `v4.35.0-rc2`
- metadata:
  `formalization.yaml v0.4`
- full predictive workflow mode:
  `full`

## Palomar package

Added:

- `ProbStackPalomar/Challenge.lean`
- `ProbStackPalomar/Solution.lean`
- `comparator.json`
- `formalization.yaml`
- `.github/workflows/session-24-palomar-validation.yml`

Challenge imports only Mathlib and states operational finite-path stackability
and exact categorical two-orientation path messages.

Advertised declarations:

- `ProbStack.Palomar.nonstackable_exists_directedMessage_le`
- `ProbStack.Palomar.nonstackable_total_mul_exists_directedMessage_le`

Solution bridges these definitions exactly to the existing ProbStack/TreeStack
implementation and reuses the already-formalized P6 theorems.

Comparator compares the two advertised theorems and their concrete statement
definitions.  The allowed axiom list is exactly `propext`, `Quot.sound`,
and `Classical.choice`.

## Module migration

Every regular submitted Lean source now uses `module`.

No public declaration name or P6 theorem statement changed.

The frozen TreeStack revision `f4112...` could not be imported from a module
under Lean 4.35.  The exact build error was:

`cannot import non-module TreeStack.Basic from module`.

The minimum compatibility migration was therefore made in a dedicated
TreeStack branch based directly on `f4112...`.

New pinned TreeStack compatibility revision:

`8fc9fc37a200855ec22579beaeec8f12f94f0310`

Only seven imported TreeStack source files received module/public-visibility
changes.  The prior SHA remains the semantic base.

Mathlib and Lean pins remain unchanged.

## Mathematical boundary

Theorem statements changed: **no**.

P5 touched: **no**.

Frozen random theorem touched: **no**.

EMPTY semantics changed: **no**.

The exact fixed-total target remains `-(2*mu-1)`.

Both directed path orientations remain included.

## Validation before final freeze

The full Lean package, Challenge, and Solution have built successfully after
the module and bridge repairs.

The no-`sorry` / no-project-`axiom` check remains scoped to the actual
ProbStack proof development; Challenge's deliberate statement-only `sorry`
holes are expected and are judged by Comparator against Solution.

The remaining final gate is the exact-candidate run of the Session 24
validation workflow, including:

- full project build;
- pinned TreeStack target build;
- 122-test Python suite;
- v0.4 metadata validator;
- local Comparator with independent kernels;
- official Palomar reusable FULL predictive preflight.

No file may change after that final successful run.

## Registration boundary

No Palomar registration is performed in this session.

If and only if the exact final candidate SHA passes the official FULL
predictive preflight, the next task is:

**MANUAL PALOMAR REGISTRATION**

## Latest official diagnostic and correction

Official FULL run `36544012411` on
`93fdd4a02269f7b9e3c196bf77257333e9556b7c` reached the authoritative
Palomar execution but failed at protected Challenge export because the
verifier-owned module alias could not export the configured
`ProbStack.Palomar.nonstackable_exists_directedMessage_le` declaration.

The report's resolved source paths showed the exact cause:
`.lake/packages/treestack/Challenge.lean` and
`.lake/packages/treestack/Solution.lean`.  The generic module identities
collided with TreeStack's earlier Palomar package.

ProbStack's Palomar files were therefore moved to the unique modules
`ProbStackPalomar.Challenge` and `ProbStackPalomar.Solution`; Comparator,
Lake targets, validation workflow, and metadata were updated, and the old
colliding root files were deleted.  The advertised `ProbStack.Palomar.*`
declaration names and theorem types are unchanged.

A fresh FULL predictive run on the final commit is required.  If it passes,
there must be no further repository change before manual registration.

