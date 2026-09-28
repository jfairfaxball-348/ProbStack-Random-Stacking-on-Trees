# Session 23 handover — P6 formalisation

Date: 2026-09-28

## Outcome

**P6 FORMALISED — PALOMAR TARGET GATE PASSES**

The Session 22 blocker is resolved.

ProbStack now contains one coherent finite-path Lean theorem for the Session 5
global deep-message necessity statement and an exact fixed-total corollary
forcing a directed message at most `-(2*mu-1)`.

No Palomar package was created.  No registration was attempted.  No paper or
arXiv material was prepared.

## Repository state

Starting SHA:

`694caef022936d69cbe16b415222c30c34db97d1`

Branch:

`session-23-p6-formalisation`

Merge status:

unmerged; `main` was not modified.

The exact final branch SHA is to be taken from the session-closing report after
temporary validation-workflow cleanup.  No mathematical source change is
planned after the successful P6 validation recorded below.

## New Lean declarations

New module:

`ProbStack/PathNecessity.lean`

Public declaration:

```lean
def HasDirectedPathMessageAtMost {n : Nat} (hn : 0 < n)
    (C : TreeStack.Configuration (Fin n)) (h : Nat) : Prop :=
  ∃ (r u : Fin n)
      (hu : (pathTree n hn).graph.Adj u r)
      (m : Int),
    (TreeStack.incidentBranch (pathTree n hn) r u hu).branchMessage C =
        some m ∧
      m <= -(h : Int)
```

General P6 theorem:

```lean
theorem nonstackable_exists_directedMessage_le
    {n h : Nat} (hn2 : 2 <= n)
    (C : TreeStack.Configuration (Fin n))
    (hmassPos : 0 < TreeStack.mass C)
    (hnonstack :
      ¬ TreeStack.Stackable (pathTree n (by omega)).graph C)
    (hh : 2 <= h)
    (hlarge :
      (n - 1) * (h / 2 + 1) < TreeStack.mass C) :
    HasDirectedPathMessageAtMost (n := n) (by omega) C h
```

Exact fixed-total corollary:

```lean
theorem nonstackable_total_mul_exists_directedMessage_le
    {n mu : Nat} (hn2 : 2 <= n)
    (C : TreeStack.Configuration (Fin n))
    (hmu : 1 <= mu)
    (hmass : TreeStack.mass C = n * mu)
    (hnonstack :
      ¬ TreeStack.Stackable (pathTree n (by omega)).graph C) :
    ∃ (r u : Fin n)
        (hu : (pathTree n (by omega)).graph.Adj u r)
        (m : Int),
      (TreeStack.incidentBranch (pathTree n (by omega)) r u hu).branchMessage C =
          some m ∧
        m <= -(2 * (mu : Int) - 1)
```

## Directed-message convention

The witness is an actual integer-valued TreeStack branch message on an
oriented path edge `u -> r`.

Because `u` and `r` range over every ordered adjacent pair, both path
orientations are included.

The theorem does not identify `EMPTY = none` with `some 0` or with any
integer.

## Proof architecture

The proof is the Session 5 prefix-dissipation proof:

- nonstackability gives all rooted scores `<= 0`;
- negate the existence of a message `<= -h`;
- use the opposite directed message at each root to bound the active effective
  input by `h-1`;
- use the exact TreeStack transfer to bound each prefix-dissipation increment
  by `floor(h/2)+1`;
- telescope along the path;
- use the last rooted score to force total mass below the resulting
  dissipation cap;
- contradict the strict total-mass hypothesis.

The fixed-total corollary sets `h=2*mu-1` and proves
`h/2+1=mu` algebraically.

For `mu=1`, the exact target is `-1`; the internal dissipation lemma is
valid for `h>=1`, so this edge case is covered directly without changing the
public `h>=2` theorem.

## Added hypothesis relative to paper prose

The formal theorem states `n >= 2` explicitly.

This is the natural finite-path domain for a conclusion asserting existence of
a directed edge message.  The positive-mass `P_1` case is trivially
stackable and has no directed path edge.

No mathematical correction to the Session 5 theorem was required.

## Files changed for Session 23

Substantive/session files relative to the Session 22 starting SHA:

- `ProbStack/PathNecessity.lean` — new P6 formalisation;
- `ProbStack.lean` — exports the new module;
- `docs/PROOF_DEPENDENCY_MAP.md` — records P6 as formal;
- `docs/FINAL_THEOREM_STATUS.md` — records the new formalisation boundary;
- `notes/session-23-p6-formalisation.md` — proof/validation record;
- `notes/session-23-handover.md` — this handover.

A temporary `.github/workflows/session-23-validation.yml` was used only to
run the Python suite and exhaustive finite checks.  It is to be deleted before
session closure and is not a permanent workflow change.

Session 20–22 documentation already present in the starting history is not a
Session 23 change.

## Validation

Permanent Lean workflow run:

`36476902728`

Result: success.

That run executed the permanent workflow's:

- exact pinned TreeStack build
  `lake build @treestack/+TreeStack.RootScore`;
- full `lake build`;
- no-`sorry` / no-project-`axiom` grep over `ProbStack/` and
  `ProbStack.lean`.

Temporary Session 23 validation run:

`36476902781`

Result: success.

It executed:

- `PYTHONPATH=. pytest -q`: **122 tests passed**;
- exhaustive general P6 finite check:
  **38,111 nonstackable configurations**;
- exhaustive exact fixed-total check:
  **4,001 nonstackable configurations**;
- no counterexample.

## Frozen items

Unchanged:

- TreeStack:
  `f4112f08d42a37c0941bf469ac124621b1f54f22`;
- Mathlib:
  `065356127b1dc0016f66b7283ce0ce2c4055aa55`;
- Lean:
  `leanprover/lean4:v4.35.0-rc2`;
- permanent workflow:
  `.github/workflows/lean-bootstrap.yml`;
- EMPTY semantics;
- Session 17;
- local asymptotics;
- binary-partition asymptotics;
- fixed-offset center;
- zero-offset status;
- full random theorem.

P5 was not touched.

No theorem statement outside P6 changed.

## Palomar target gate

The gate now passes for the formalised P6 target.

The theorem is a readable global quantitative statement about path
stackability, distinct from TreeStack's already-registered structural score
certificate, and it is the deterministic supercritical reduction used by the
ProbStack random threshold argument.

The relationship to earlier work remains descriptive rather than a novelty
claim:

- Csernák-Soukup: exact stackability event and deterministic graph-stacking
  context;
- Bushaw-Kettle: closest same-law/path sharp random-pebbling analogue for a
  different solvability event;
- TreeStack: already-registered structural certificate used as an input here.

A small Mathlib-only Challenge surface is plausibly achievable by restating the
path-only transfer/message recursion and ordinary legal path stackability, but
that work belongs to the next session.

No Palomar files were created and no module-system migration was performed.

## Exactly one next task

**PALOMAR PACKAGING + MODULE-SYSTEM MIGRATION + FULL PREFLIGHT**
