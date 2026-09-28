# Palomar preparation — Session 22

Date: 2026-09-28

Status: **NOT YET PALOMAR-READY**

This note is the authoritative Session 22 Palomar target audit. It does not
register anything with Palomar, does not begin paper drafting, and does not
alter the frozen ProbStack theorem.

## Starting point

- repository start SHA: `78bbdd58ca08c381af28d0b6149dfa4daf655b17`
- branch: `session-22-palomar-preparation`
- validated Session 19 main remains
  `d03b8381eb1b4cc100146cadbed3035c31c7016d`
- Sessions 20–21 remain documentation-only relative to Session 19.

Frozen dependency pins remain unchanged:

- TreeStack: `f4112f08d42a37c0941bf469ac124621b1f54f22`
- Mathlib: `065356127b1dc0016f66b7283ce0ce2c4055aa55`
- Lean: `leanprover/lean4:v4.35.0-rc2`

## Current Palomar revisions inspected

The current public Palomar repositories were rechecked before any repository
edit.

- PalomarPolicy: `96b034cc31a72a63d4f4041911dce337a85c9a04`
- PalomarSubmission: `65f0154ed776cd26c224254aa57b379137f28b0d`
- PalomarTemplate: `2891de4c48955af824969a263d31b25e7a9a1406`

The current PalomarSubmission `toolchains.json` minimum is
`v4.35.0-rc2`, so the existing ProbStack toolchain meets the minimum.

The inspected current policy confirms, among other things, that:

- the Challenge theorem itself must plausibly warrant a research paper or
  serious research note and have a credible research audience;
- every regular submitted `.lean` file must use Lean's module system;
- the Challenge dependency closure may use only the approved canonical
  statement dependencies;
- Comparator requires a nonempty theorem list and permits only
  `propext`, `Quot.sound`, and `Classical.choice`;
- Palomar checks the selected proof with Lean's kernel and independent kernels;
- `formalization.yaml` should use the v0.4 form, human-only authors and
  maintainers, honest automation disclosure, and source-derived provenance;
- `type: original-proof` is appropriate only when the formalisation is the
  first presentation of the result, not merely because a literature search
  found no match.

The current submission instructions still require a public immutable full
commit SHA. The reusable full predictive workflow remains available from
PalomarSubmission and `mode: full` is the relevant final mechanical preflight,
not `mode: preflight`.

## Target audit

The existing Lean families required by the handover were inspected:
`TreeStackBoundary.lean`, `PathMessage.lean`, `PathBranch.lean`,
`PathBridge.lean`, `Deficit.lean`, `TransferBounds.lean`,
`PathDeep.lean`, `PathFront.lean`, `FiniteProbability.lean`, and
`FiniteDyadic.lean`.

### Rejected as advertised Palomar targets

1. `ProbStack.empty_ne_some_zero` is a categorical sanity theorem about
   `Option Int`. It is important for semantics but does not meet Palomar's
   research-interest floor.

2. The path-message bridge and recurrence theorems are mathematically useful
   infrastructure, but in their present form they expose the already-registered
   TreeStack structural certificate on a path. Advertising one of these helper
   declarations as the ProbStack result would overstate the distinct
   mathematical content.

3. The regeneration, deep-seed, runaway and certified-front declarations are a
   substantial finite proof interface, but the existing Lean surface stops
   before the global theorem that turns the front mechanism into a statement
   about path nonstackability. The current strongest declarations therefore
   still read as proof machinery rather than the project's advertised
   mathematical result.

4. The matched geometric mass on a fixed-total fibre is the exact finite
   conditioning algebra used by ProbStack, but by itself it is an elementary
   and classical identity. It is not an honest research-level ProbStack target.

5. The finite dyadic/binary-partition encodings are exact and useful, but their
   standalone content is elementary finite combinatorics and belongs to a
   classical analytic lineage. They are not an honest substitute for the
   random-stackability theorem.

### TreeStack is not a new fallback target

The current TreeStack repository reports that its structural/tree result is
already publicly registered with Palomar as
`PALOMAR-2026-09-25-000010` (version 1), after mechanical verification of
TreeStack revision
`4d4969703a9f0ca7a51cbe7edf0f0338cc95cafb`.

Therefore Option 3 does not supply a new ProbStack registration target.
ProbStack must stand on a distinct theorem rather than repackaging TreeStack's
registered certificate.

## Formalisation boundary

The frozen two-sided random threshold theorem is still **not** a Lean theorem.
Nothing in Session 22 changes that fact. In particular, Palomar is not being
asked to verify:

- the Session 17 analytic local theorem;
- Robbins/Stirling or de Bruijn asymptotics;
- event-level conditioning and global probability transfer;
- the final two-sided fixed-offset asymptotic theorem.

The full ProbStack random high-density transition theorem is not the
declaration registered here; in fact, no ProbStack declaration is being
registered in Session 22.

## Single blocker

The one blocking formalisation task selected by this audit is:

> **Formalise the Session 5 global deep-message necessity theorem (P6) as one
> packaged Lean theorem over a finite path, including its exact
> `t = n * mu` corollary with target `-(2 * mu - 1)`.**

The mathematical statement to package is:

For a positive-mass configuration of total `t` on `P_n`, if the
configuration is nonstackable and `h >= 2` with

`t > (n - 1) * (floor(h / 2) + 1)`,

then at least one directed path message is at most `-h`.

Consequently, for total `t = n * mu` with `mu >= 1`, nonstackability
forces some directed message to be at most `-(2 * mu - 1)`.

This is the narrowest current paper-only deterministic statement that is both
global and quantitatively tied to the random-threshold argument. Unlike the
existing helper lemmas, it directly constrains the operational stackability
event on paths. It can be formalised without reopening the Session 17 analytic
rate, the fixed-offset centre, zero-offset behaviour, or the probability
arguments.

After P6 is formalised, the Palomar target gate must be run again before any
Challenge/Solution packaging. No claim is made here that merely formalising P6
automatically guarantees editorial acceptance.

## Why no Palomar packaging was created

Because the target gate failed at the current SHA, this session deliberately
did **not** create:

- `Challenge.lean`;
- `Solution.lean`;
- `comparator.json`;
- `formalization.yaml`;
- a Palomar predictive-preflight workflow.

For the same reason, the repository-wide module-system migration was not
started. That migration is a compatibility refactor required for an actual
ProbStack submission, but doing it before there is an honest registrable theorem
would create broad source churn without resolving the substantive blocker.

## Licence and source checks

The repository has one root `LICENSE` containing the standard Apache License
2.0 text. A template-style `licensee` detector was not run because the target
gate failed before packaging; therefore this session records the source licence
as Apache-2.0 but does not claim a Palomar mechanical licence-detection result.

No theorem source, Python, test, data, dependency, workflow, or frozen
mathematical statement was changed in this session.

## Validation / preflight status

No substantive Lean source was changed, so the Session 19 validated Lean/Python
state remains the relevant computational baseline. Session 22 did not rerun
`lake build`, the pinned TreeStack build, the no-sorry/no-project-axiom check,
or the 122-test Python suite because the only intended repository changes are
documentation.

No Palomar local Comparator run or official reusable full preflight was run:
there is intentionally no Challenge/Solution package to verify.

## Provenance and AI metadata status

No `formalization.yaml` was created, so no final Palomar provenance
classification has been asserted. The Session 20–21 prior-art audit remains the
source record for a later target decision; its negative searches are not treated
as novelty proof.

Any later submission must disclose the substantial AI-assisted research, proof
engineering, repository work and literature auditing under automation/process
metadata, while keeping `project.authors` and
`project.responsible_maintainers` human-only. No independent peer review is
claimed.

## Editorial self-audit

At the current SHA, Questions 1–4 of the Palomar readiness review fail for the
available ProbStack Challenge candidates: the existing Lean declarations do not
yet package a distinct, globally meaningful ProbStack theorem at the level that
should be advertised to an external research mathematician. Questions about
Comparator, protected Challenge closure, kernel replay and immutable candidate
SHA are therefore not reached.

Final decision: **PALOMAR PREPARATION INCOMPLETE**.

Single blocker: formalise P6 exactly as specified above.
