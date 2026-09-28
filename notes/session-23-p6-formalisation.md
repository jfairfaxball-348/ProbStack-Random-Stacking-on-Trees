# Session 23 — P6 formalisation

Date: 2026-09-28

Status: **P6 FORMALISED — PALOMAR TARGET GATE PASSES**

This session is limited to the deterministic finite-path P6 theorem selected
by Session 22.  It does not draft the paper, prepare arXiv material, register
with Palomar, or create Palomar Challenge/Solution packaging.

## Starting point

- starting SHA: `694caef022936d69cbe16b415222c30c34db97d1`
- branch: `session-23-p6-formalisation`
- branch remains unmerged
- validated Session 19 main remains
  `d03b8381eb1b4cc100146cadbed3035c31c7016d`

Frozen pins remain unchanged:

- TreeStack: `f4112f08d42a37c0941bf469ac124621b1f54f22`
- Mathlib: `065356127b1dc0016f66b7283ce0ce2c4055aa55`
- Lean: `leanprover/lean4:v4.35.0-rc2`

## Formal surface

The new module is:

`ProbStack/PathNecessity.lean`

and is exported by `ProbStack.lean`.

The readable directed-message predicate is:

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

Thus a "directed path message" is an actual TreeStack incident-branch message
on an oriented edge `u -> r` of the path.  The existential ranges over all
adjacent ordered pairs, hence both left-to-right and right-to-left
orientations.  The witness is explicitly `some m`; `EMPTY = none` is never
identified with integer zero.

The general P6 theorem is:

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

For natural `h`, `h / 2` is exactly `floor(h/2)`.  This is the Session 5
paper statement with the path-size convention `n >= 2` made explicit.

The exact fixed-total corollary is:

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

The target is exactly `-(2*mu-1)`; it is not weakened to `-mu`,
`-2*mu`, or a surrogate event.

## Proof architecture

The formal proof follows the Session 5 dissipation argument.

1. Use TreeStack's exact
   `not_stackable_iff_all_scores_nonpos` theorem, so operational
   nonstackability gives every rooted score at most zero.

2. Define finite prefix mass and
   `leftPrefixDissipation = prefix mass - genuine left branch message
   contribution`.

3. Negate the desired conclusion, so every actual directed integer message is
   strictly greater than `-h`.  EMPTY branches remain categorical and
   contribute zero only through TreeStack's existing
   `messageContribution` operation.

4. At each path root, combine score nonpositivity with the opposite directed
   branch message being greater than `-h`.  This bounds the active effective
   input by `h-1`.

5. Prove directly from the exact TreeStack transfer function that, under those
   two bounds, one dissipation increment is at most
   `floor(h/2)+1`.

6. Telescope the prefix dissipation along the path.

7. At the terminal root, score nonpositivity forces total mass to be at most
   the final prefix dissipation.

8. Conclude
   `mass C <= (n-1)*(floor(h/2)+1)`, contradicting the P6 mass hypothesis.

No front theorem, probability theorem, P5 statement, or assumed deep seed is
used.

## Arithmetic and the fixed-total corollary

For the fixed-total theorem set

`h = 2*mu - 1`.

The proof establishes algebraically:

`h / 2 + 1 = mu`

and then

`(n-1)*mu < n*mu = mass C`

from `mu >= 1`.

For `mu = 1`, this gives `h = 1`.  The public Session 5 theorem is
intentionally stated only for `h >= 2`, but the internal dissipation bound is
proved for `h >= 1`, so the exact `-1` corollary is obtained without
weakening its target or changing the paper theorem.

## Edge cases and paper fidelity

- `n >= 2` is explicit because the conclusion concerns an oriented path
  edge.  The positive-mass `P_1` case is trivially stackable and has no
  directed edge.
- positive total mass is retained in the general public theorem exactly as in
  the Session 5 paper statement, although the strict mass inequality already
  implies it.
- `mu >= 1` is handled including `mu = 1`.
- endpoint root-score decompositions are proved explicitly.
- EMPTY is never coerced to an integer message.
- no paper theorem needed correction.

## Validation

Permanent workflow:

- GitHub Actions run: `36476902728`
- result: success
- exact pinned TreeStack target build:
  `lake build @treestack/+TreeStack.RootScore`
- full ProbStack build: `lake build`
- no-`sorry` / no-project-`axiom` check over `ProbStack/` and
  `ProbStack.lean`: success

Temporary Session 23 validation workflow:

- GitHub Actions run: `36476902781`
- result: success
- `PYTHONPATH=. pytest -q`: **122 tests passed**
- exhaustive direct P6 check:
  - 38,111 nonstackable small configurations checked for the general
    dissipation implication over `2 <= n <= 7`, totals `1..12`, and tested
    thresholds;
  - 4,001 nonstackable fixed-total cases checked for the exact
    `-(2*mu-1)` corollary over `2 <= n <= 6`, `1 <= mu <= 3`.
- no counterexample was found.

The temporary validation workflow is session infrastructure only and is to be
removed before final session closure.  Its successful Python result remains
valid because no Python source or tests are changed afterward.

## Formalisation boundary

P5 was not touched.

No theorem statement outside P6 was changed.  The only Lean integration change
outside the new module is the import of `ProbStack.PathNecessity` from
`ProbStack.lean`.

The frozen random theorem, Session 17 local rate, binary-partition
asymptotics, probability transfer, dependency pins, EMPTY semantics, and
permanent CI semantics remain unchanged.

## Palomar target-gate reassessment

The Session 22 target gate now passes for P6.

1. The statement is understandable independently of its proof machinery:
   global nonstackability plus a mass inequality forces a quantitatively deep
   directed message.

2. It directly concerns graph pebbling/stackability on finite paths.

3. It is distinct from TreeStack's already-registered structural certificate:
   TreeStack characterises rooted stackability by score, while P6 derives a
   global quantitative deep-message consequence from nonstackability and
   total mass.

4. It is quantitatively substantive: the exact coefficient is
   `floor(h/2)+1`, and the fixed-total consequence is exactly
   `-(2*mu-1)`.

5. Its role in ProbStack is clear: it is the deterministic reduction used on
   the supercritical side to cover nonstackability by rare deep-message
   events.

6. The prior-art relationship remains describable without novelty claims:
   Csernák-Soukup supplies the exact stackability event and deterministic
   stacking context; Bushaw-Kettle supplies the closest same-law/path
   random-pebbling asymptotic analogue for a different solvability event;
   TreeStack supplies the already-registered structural score certificate.

7. A finite quantitative necessity theorem of this kind plausibly supports a
   serious research note for graph-pebbling/probabilistic-combinatorics
   readers.  This is a Palomar target-floor assessment, not a novelty,
   priority, publication, or acceptance claim.

8. A small Mathlib-only Challenge surface is plausible: the path-only
   transfer/message recursion and standard legal pebbling stackability can be
   stated canonically without importing the TreeStack proof development.
   Building and mechanically verifying that surface is deliberately deferred
   to the next session.

No Palomar packaging files were created in this session, and no module-system
migration was performed.

## Outcome

**P6 FORMALISED — PALOMAR TARGET GATE PASSES**

Exactly one next task:

**PALOMAR PACKAGING + MODULE-SYSTEM MIGRATION + FULL PREFLIGHT**
