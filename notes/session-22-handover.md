# Session 22 handover — Palomar preparation

Date: 2026-09-28

## Outcome

**PALOMAR PREPARATION INCOMPLETE**

The target gate was applied before any Palomar packaging or module-system
migration. No existing ProbStack Lean declaration or small existing theorem
family honestly clears Palomar's current research-interest floor as the
advertised ProbStack result.

The one blocking task is:

> Formalise the Session 5 global deep-message necessity theorem (P6) as one
> packaged finite-path Lean theorem, including the exact total
> `t = n * mu` corollary forcing a directed message
> `<= -(2 * mu - 1)`.

Do not begin paper preparation until this blocker is resolved and the Palomar
target gate is rerun.

## Repository state

Starting SHA:

`78bbdd58ca08c381af28d0b6149dfa4daf655b17`

Branch:

`session-22-palomar-preparation`

Merge status:

unmerged; main was not modified.

Files intentionally changed in Session 22:

- `notes/palomar-preparation.md`
- `notes/session-22-handover.md`

No Lean, Python, tests, data, dependency pins, Lake files, or workflows were
changed.

## Target audit result

Rejected as the advertised Palomar result:

- `ProbStack.empty_ne_some_zero`: semantically important but trivial;
- path recurrence/bridge declarations: useful infrastructure but largely a path
  exposure of the already-registered TreeStack structural certificate;
- deep-seed/runaway/front helpers: substantial proof machinery but no packaged
  global path-stackability conclusion;
- fixed-total matched-geometric mass identity: elementary/classical on its own;
- finite dyadic/binary-partition encoding: elementary/classical on its own.

The paper-level global deterministic gaps remain P5 and P6. P6 was selected as
the single next blocker because it is the narrowest global quantitative theorem
that directly connects operational nonstackability on paths to the rare
deep-message event used on the supercritical side.

Plain P6 statement:

For a positive-mass configuration of total `t` on `P_n`, if it is
nonstackable and `h >= 2` and

`t > (n - 1) * (floor(h / 2) + 1)`,

then some directed path message is at most `-h`.

Exact corollary:

if `t = n * mu` with `mu >= 1` and the configuration is nonstackable, then
some directed message is at most `-(2 * mu - 1)`.

No theorem at epsilon zero and no analytic asymptotic theorem is to be touched
while formalising this blocker.

## TreeStack relationship

ProbStack still pins TreeStack at:

`f4112f08d42a37c0941bf469ac124621b1f54f22`.

The current TreeStack repository reports that its main structural/tree theorem
is already publicly registered as
`PALOMAR-2026-09-25-000010` version 1, with the registered source revision
reported there as:

`4d4969703a9f0ca7a51cbe7edf0f0338cc95cafb`.

Therefore TreeStack is not an unregistered fallback target for this ProbStack
stage, and its result must not be repackaged as ProbStack's theorem.

## Current Palomar references used

Exact revisions inspected in Session 22:

- PalomarPolicy:
  `96b034cc31a72a63d4f4041911dce337a85c9a04`
- PalomarTemplate:
  `2891de4c48955af824969a263d31b25e7a9a1406`
- PalomarSubmission:
  `65f0154ed776cd26c224254aa57b379137f28b0d`

Current Palomar minimum Lean version from
`PalomarSubmission/toolchains.json`:

`v4.35.0-rc2`

Current ProbStack toolchain therefore meets the minimum:

`leanprover/lean4:v4.35.0-rc2`

Current Palomar policy still requires module-system-compatible regular Lean
sources, a small protected Challenge statement surface, exact Comparator
matching, approved Challenge dependency closure, structured v0.4 metadata,
full immutable dependency pins, and a full predictive preflight before claiming
mechanical readiness.

## Palomar files and preflight

Not created because the target gate failed:

- `Challenge.lean`
- `Solution.lean`
- `comparator.json`
- `formalization.yaml`
- Palomar reusable-preflight workflow

Accordingly:

- exact Challenge theorem types: none;
- exact Solution theorem names: none;
- comparator declarations: none;
- Challenge transitive import closure: not applicable;
- official reusable Palomar FULL preflight run ID: none;
- preflight candidate SHA: none;
- mechanical-report artifact: none;
- profile id/digest: none.

A preparation-only run was not substituted for a full run.

## Module-system status

ProbStack source was **not** ported to the module system in Session 22.

Reason: current Palomar policy requires that migration for a submission, but the
research-level target gate failed first. Broadly rewriting every Lean source
before there is a theorem worth registering would not fix the actual blocker.

No theorem statement changed.

## Frozen mathematics and semantics

Unchanged.

The frozen headline theorem remains the two fixed-epsilon implications about

`c_n = sqrt(log_2 n) - (1/2) log_2 log_2 n + log_2(3e)`.

It remains paper mathematics, not a Lean limit theorem.

The exact structural criterion remains:

`StackableAt(T,C,r) iff 0 < score(T,C,r)`.

`TreeStack.Message = Option Int` and `TreeStack.EMPTY = none`.

`none`, `some 0`, positive integers, and negative integers remain distinct.

## Dependency pins

Unchanged:

- TreeStack:
  `f4112f08d42a37c0941bf469ac124621b1f54f22`
- Mathlib:
  `065356127b1dc0016f66b7283ce0ce2c4055aa55`
- Lean:
  `leanprover/lean4:v4.35.0-rc2`

Permanent CI semantics in
`.github/workflows/lean-bootstrap.yml` were not changed.

## Licence

The root `LICENSE` is the standard Apache License 2.0 text, consistent with
the intended SPDX value `Apache-2.0`.

Palomar's template-style `licensee` detector was not run because packaging
stopped at the target gate. Therefore Session 22 does not claim a mechanical
Palomar licence-detection result.

## Provenance / sources / review / automation

No `formalization.yaml` was created, so no final source-origin classification
was asserted.

The later metadata must use the Session 20–21 prior-art audit without converting
negative searches into novelty claims. It must distinguish:

- Csernák–Soukup: deterministic graph stackability;
- Bushaw–Kettle and the random-pebbling threshold literature: same/similar
  fixed-total random law and path scale, different solvability event;
- TreeStack: already-registered structural certificate;
- ProbStack: whichever exact theorem eventually passes the target gate.

AI involvement must be disclosed honestly under automation/process metadata.
Humans only may be listed as authors and responsible maintainers. No independent
peer review is claimed. The current review basis is self-assessment plus the
repository's documented validation/audit history; no Palomar review occurred in
Session 22.

## Validation

Because Session 22 changed documentation only:

- local `lake build`: not rerun;
- exact pinned TreeStack build: not rerun;
- no-sorry/no-project-axiom check: not rerun;
- Python suite: not rerun; last validated Session 19 count remains 122 tests.

No Palomar Comparator or independent kernel replay was run because there is no
honest Challenge/Solution target yet.

## What Palomar is NOT verifying

Nothing was submitted or preflighted in Session 22.

In particular Palomar is not verifying the full ProbStack random
high-density transition theorem, the Session 17 analytic local theorem,
Robbins/Stirling or de Bruijn asymptotics, event-level conditioning, the global
probability transfer, P5, or P6.

## Next session

The next session is not Palomar registration and not paper preparation.

It is a single formalisation session:

**PROBSTACK P6 FORMALISATION — GLOBAL DEEP-MESSAGE NECESSITY ON PATHS**

Required endpoint:

1. one packaged Lean theorem for the general `h` statement above;
2. its exact `t = n * mu`, `-(2 * mu - 1)` corollary;
3. no change to the headline asymptotic theorem, Session 17, EMPTY semantics,
   dependency pins, or permanent CI guarantees;
4. full project regression validation;
5. then rerun the Palomar target gate before any module migration or packaging.
