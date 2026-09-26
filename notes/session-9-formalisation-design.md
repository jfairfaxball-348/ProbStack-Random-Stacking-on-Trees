# Session 9 — formalisation architecture

Status: **DESIGN COMPLETE; FORMAL VERIFICATION NOT YET STARTED.**

This document fixes the proposed Lean architecture for the frozen ProbStack path
theorem. It does not claim that any new ProbStack Lean theorem has compiled.
The mathematical target remains the Session 8 frozen theorem.

## 1. Pinned starting boundary

Session 9 verified the following exact starting state before design work:

- ProbStack `main`: `26f15c1f24d65e5a3e9f4702448c70f43558f8b0`.
- authoritative TreeStack dependency:
  `f4112f08d42a37c0941bf469ac124621b1f54f22`.
- TreeStack's pinned Mathlib revision:
  `065356127b1dc0016f66b7283ce0ce2c4055aa55`.
- TreeStack toolchain:
  `leanprover/lean4:v4.35.0-rc2`.

The exact structural criterion remains

[
operatorname{StackableAt}(T,C,r)iff 0<operatorname{score}(T,C,r).
]

`EMPTY` remains categorical and is never identified with the integer message
zero.

## 2. Frozen formal target

For a positive integer sequence (mu_n), let (C_n) be uniform on weak
compositions of total (nmu_n) over the (n)-vertex path (P_n), and put

[
c_n=
sqrt{log_2 n}
-rac12log_2log_2 n
+log_2(3e).
]

For every fixed (arepsilon>0):

- if (log_2mu_nle c_n-arepsilon) eventually, then
  (Pr[C_n	ext{ stackable}]	o0);
- if (log_2mu_nge c_n+arepsilon) eventually, then
  (Pr[C_n	ext{ stackable}]	o1).

No assertion is made at zero offset. This mathematical content is frozen.

## 3. Exact TreeStack dependency map

The following names were read at the exact pinned TreeStack commit.

### `TreeStack/Basic.lean`

Reuse directly:

- `TreeStack.Configuration (V : Type*) := V → ℕ`;
- `TreeStack.mass`;
- `TreeStack.support`;
- `TreeStack.FiniteTree`.

### `TreeStack/PebblingMove.lean`

Reuse directly:

- `TreeStack.move`;
- `TreeStack.PebbleStep`;
- `TreeStack.Reach`;
- `TreeStack.StackedAt`;
- `TreeStack.StackableAt`;
- `TreeStack.Stackable`;
- `TreeStack.UniversalStackable`.

### `TreeStack/Transfer.lean`

Reuse directly:

- `TreeStack.F : ℤ → ℤ`, the exact five-case transfer;
- `TreeStack.Message := Option ℤ`;
- `TreeStack.EMPTY := none`;
- `TreeStack.empty_ne_integer_zero`;
- `F_of_le_one`, `F_two`, `F_three`;
- `F_of_ge_four_even`, `F_of_ge_five_odd`;
- `F_sub_three_le`;
- `F_neg_iff`;
- `F_eq_zero_iff`;
- `F_eq_neg_odd_iff`;
- `F_eq_nonneg_iff`.

ProbStack must not redefine `F`, `Message` or `EMPTY`.

### `TreeStack/Branch.lean`

Reuse the oriented-branch infrastructure:

- `TreeStack.OrientedBranch`;
- `OrientedBranch.vertices`, `card`;
- `OrientedBranch.Child`, `childBranch`;
- `childBranch_card_lt`;
- the existing branch decomposition/boundary lemmas as needed.

### `TreeStack/Message.lean`

Reuse directly:

- `OrientedBranch.Occupied`;
- `OrientedBranch.messageContribution`;
- `OrientedBranch.branchMessage`;
- `OrientedBranch.childMessageSum`;
- `OrientedBranch.effectiveInput`;
- `branchMessage_eq_empty_of_not_occupied`;
- `branchMessage_eq_some_of_occupied`;
- `branchMessage_eq_empty_iff`;
- `branchMessage_ne_empty_of_occupied`.

The arithmetic contribution of `EMPTY` to a score is zero, but the message
itself remains `none`, not `some 0`.

### `TreeStack/RootScore.lean`

Reuse directly:

- `TreeStack.incidentBranch`;
- `TreeStack.rootMessageTerm`;
- `TreeStack.rootMessageSum`;
- `TreeStack.score`;
- `TreeStack.stackableAt_of_score_pos`;
- `TreeStack.score_pos_of_stackableAt`;
- `TreeStack.stackableAt_iff_score_pos`;
- `TreeStack.not_stackable_iff_all_scores_nonpos`.

The exact formal structural theorem is

```lean
TreeStack.stackableAt_iff_score_pos
  (T : FiniteTree V) (C : Configuration V) (r : V) :
  StackableAt T.graph C r ↔ 0 < score T C r
```

subject to the file's existing typeclass hypotheses.

### `TreeStack/Boundary.lean`

This file supplies the constructive branch-clearing/signature machinery used
internally by `RootScore.lean`, including
`MoveSignature.boundaryFlux`, `signature_branchFlux_bounds`,
`ClearOutcome.boundary_le_message`, and related lemmas. ProbStack should not
depend on these implementation details unless a later path lemma genuinely
needs them.

### Results not already present in TreeStack

No path-specialised Lean module was found at the pinned commit. In particular,
the audit did not locate pre-existing formal statements for:

- the scalar left/right path recurrence;
- prefix/suffix message folds on `Fin n`;
- the global inequality `F x ≤ x / 2`;
- the low-phase deficit recurrence/closed form;
- the path message-versus-prefix-mass bound;
- irreversible path fronts;
- opposing-front nonstackability;
- Session 5 dissipation/deep-message necessity;
- Session 8 regeneration.

These are new ProbStack theorems.

## 4. Dependency/import boundary

ProbStack remains an independent repository, but its Lean package should pin
TreeStack as an external Git dependency at the exact commit above. The intended
Lake boundary is conceptually

```lean
require treestack from git
  "https://github.com/jfairfaxball-348/TreeStack-Structural-Certificates-for-Stacking-on-Trees.git" @
  "f4112f08d42a37c0941bf469ac124621b1f54f22"
```

and ProbStack should use the same Mathlib revision as TreeStack unless a
deliberate, separately validated dependency upgrade is made.

A small `ProbStack.TreeStackBoundary` module should import the exact TreeStack
modules and expose no replacement semantics. Most path work should depend on
that boundary rather than on TreeStack's later stacking-number development.

## 5. Mathlib APIs inspected at the pinned revision

The formalisation design read the following APIs at Mathlib
`065356127b1dc0016f66b7283ce0ce2c4055aa55`:

- `SimpleGraph.pathGraph n : SimpleGraph (Fin n)`;
- `SimpleGraph.pathGraph_adj`;
- `SimpleGraph.pathGraph_preconnected` and
  `SimpleGraph.pathGraph_connected`;
- `ProbabilityTheory.geometricMeasure` and
  `geometricMeasure_singleton`;
- `PMF.uniformOfFinset` / `PMF.uniformOfFintype`;
- `ProbabilityTheory.cond`;
- `Measure.infinitePi` and the finite-index atom identity
  `infinitePi_singleton_of_fintype`;
- `Asymptotics.IsLittleO` and eventual/filter formulations;
- `Real.logb`.

A direct `pathGraph_isTree` theorem was not located in the inspected path
module, so the finite-tree wrapper will need an acyclicity proof even though
the graph and connectedness facts already exist.

No dedicated formal binary-partition / A000123 asymptotic development was
located in the limited Mathlib/Lean search. General formal power series exist,
but the ProbStack finite coefficient identities should initially be proved
combinatorially rather than introducing a general generating-function
framework.

## 6. Formal representations

### Paths

Use Mathlib's `SimpleGraph.pathGraph n` on `Fin n`.

Define, for positive `n`, a wrapper

```lean
noncomputable def pathTree (n : ℕ) (hn : 0 < n) :
    TreeStack.FiniteTree (Fin n)
```

whose graph is `SimpleGraph.pathGraph n`. Prove connectedness from the Mathlib
path theorem and prove acyclicity once.

Do not build a second path graph.

For scan direction, prefer explicit `leftMessage` and `rightMessage`
wrappers over a needlessly abstract orientation type. A small direction enum
may be added later only if it removes duplicated proofs.

### Configurations

Reuse

```lean
TreeStack.Configuration (Fin n) = Fin n → ℕ
```

and `TreeStack.mass`.

Use the semantic weak-composition type

```lean
def WeakComposition (n t : ℕ) :=
  {C : TreeStack.Configuration (Fin n) // TreeStack.mass C = t}
```

and construct its finite instance by an equivalence with bounded coordinate
vectors `Fin n → Fin (t+1)` satisfying the same sum constraint. This keeps the
public object exactly a TreeStack configuration while giving a finite uniform
law.

### Messages

Use TreeStack's exact

```lean
TreeStack.Message = Option ℤ
TreeStack.EMPTY = none
```

throughout.

Define a path scan step with separate EMPTY activation logic and prove it
equivalent to `OrientedBranch.branchMessage` on the corresponding path
branch. The arithmetic helper `messageContribution` may be used only when a
score/sum needs an integer; it must not erase the categorical state at the
message level.

### Uniform weak-composition law

Use `PMF.uniformOfFintype (WeakComposition n t)` as the canonical finite law.

For asymptotic statements, expose a real-valued event-probability wrapper so
that the final target is a sequence in `ℝ`, while proving once that it agrees
with the PMF/measure value.

### Geometric product law

For integer mean (mu>0), take success parameter

[
p_mu=rac1{mu+1},
qquad
r_mu=rac{mu}{mu+1}.
]

Use `ProbabilityTheory.geometricMeasure` on (mathbb N). For a finite vector
indexed by `Fin n`, use `Measure.infinitePi` over the finite index set. The
singleton product theorem supplies the exact atom formula.

Define total mass as the finite sum of coordinates. Condition the product
measure on the event that the total equals (t), using
`ProbabilityTheory.cond`, and prove that the induced law is exactly the
uniform weak-composition law. Because every vector with the same total has the
same geometric atom, this proof is finite and elementary.

Do not build an infinite stochastic-process framework. Every event used in the
paper is a finite-vector or finite-block event.

### Asymptotic sequences

Use filters:

- `Filter.atTop` for (n	oinfty);
- `∀ᶠ n in atTop, ...` for “eventually”;
- `Tendsto p atTop (𝓝 0)` and `Tendsto p atTop (𝓝 1)`;
- `Asymptotics.IsLittleO` where an explicit error function is helpful.

Keep (mu : mathbb N	omathbb N) with an explicit positivity hypothesis.
The center may be globally defined using `Real.logb`; all analytic lemmas
will work under eventual lower bounds on (n), so small exceptional indices do
not alter the theorem.

## 7. Complete theorem dependency DAG

The labels below are the intended stable proof graph. “TS” means imported
TreeStack. Risk refers to expected formalisation cost, not mathematical doubt.

### Layer A — tree/message basics

| ID | Formal statement | Direct dependencies | Risk |
|---|---|---|---|
| A1 | Exact transfer/message boundary | TS `F`, `Message`, `EMPTY` | LOW |
| A2 | Path scalar left/right message recurrence | A1, TS branchMessage, pathTree | MODERATE |
| A3 | EMPTY persistence/activation on prefixes and suffixes | A2, TS empty classification | MODERATE |
| A4 | `F x ≤ x/2` for all integer `x` | A1 exact transfer cases | LOW |
| A5 | Positive-phase parity/transfer identities | A1 transfer case lemmas | LOW |
| A6 | Low-phase deficit recurrence | A1, A2, `F_of_le_one` | LOW |
| A7 | Exact low-phase closed form | A6, finite sums/powers of two | MODERATE |
| A8 | Message-versus-prefix/suffix-mass bound | A2–A4 | MODERATE |
| A9 | Irreversible-front criterion | A2, A7, A8, TS score | MODERATE |
| A10 | Opposing fronts imply nonstackability | A9, TS `not_stackable_iff_all_scores_nonpos` | MODERATE |

### Layer B — reset/regeneration/front conversion

| ID | Formal statement | Direct dependencies | Risk |
|---|---|---|---|
| B1 | Reset affine upper bound | A2–A4 | LOW |
| B2 | Reset-event product-law lower bound | B1, F1 | MODERATE |
| B3 | Session 8 regeneration interval arithmetic | integer arithmetic | LOW |
| B4 | ([2mu+2,4mu]) transfers into ([mu,2mu]) | A1, parity cases | LOW |
| B5 | Exact geometric probability of the steering interval | B3, F1 | MODERATE |
| B6 | (delta_muge8/(17e^3)) for (muge16) | B5, elementary real inequalities | MODERATE |
| B7 | Deep seed gives deficit at least (mu+3) | A6 | LOW |
| B8 | Runaway (3/2) deficit growth | A6, integer floors | LOW |
| B9 | Positive uniform runaway probability | B8, F1, finite/infinite product bounds | HIGH |
| B10 | Deep seed to true irreversible front using mass reserve | A8–A9, B7–B9 | MODERATE |

For B9, prefer a finite explicit lower-bound lemma sufficient for the paper
over developing general infinite-product theory unless the latter becomes
simpler.

### Layer C — structural necessity / supercritical cover

| ID | Formal statement | Direct dependencies | Risk |
|---|---|---|---|
| C1 | Prefix/suffix dissipation definitions and exact score identity | A2–A3, TS score | MODERATE |
| C2 | Dissipation increment identity and one-step bound | A1, C1 | MODERATE |
| C3 | Deep-message necessity theorem | C1–C2, TS rooted criterion | MODERATE |
| C4 | First-entry decomposition into positive/middle/low phases | A2, A5–A7 | MODERATE |
| C5 | Boundary versus interior witness split | C3–C4 | MODERATE |
| C6 | Finite local cover for a deep message | C4–C5, D7–D8 | HIGH |

C6 should first be a finite structural union/decomposition. Its sharp
probability rate belongs downstream in E/F.

### Layer D — dyadic simplex / binary partitions

| ID | Formal statement | Direct dependencies | Risk |
|---|---|---|---|
| D1 | Finite dyadic simplex count | finite sums/Finsets | MODERATE |
| D2 | Equivalence with cumulative binary partitions | D1, finite partition encoding | HIGH |
| D3 | Reverse positive slack encoding | A5 | MODERATE |
| D4 | Slack multiplicity 1 for 0,1,2 and 2 for ≥3 | D3, parity | LOW |
| D5 | Coefficient identity corresponding to ((1+z^3)/(1-z)) | D4 | MODERATE |
| D6 | Finite telescoping across dyadic scales | D5 | MODERATE |
| D7 | Terminal-specific positive-entry budgets | D3–D6 | HIGH |
| D8 | Terminal-specific low-phase budgets | A7, D1 | MODERATE |
| D9 | Truncated/unrestricted binary-partition comparison | D1–D2 | HIGH |
| D10 | Uniform binary-partition linear-scale asymptotic | binary-partition recurrence + real asymptotics | RESEARCH-LEVEL FORMAL ANALYSIS |

D5–D6 should be stated as finite coefficient/counting identities; general
formal power series are not required for the theorem.

### Layer E — local excursion asymptotics

| ID | Formal statement | Direct dependencies | Risk |
|---|---|---|---|
| E1 | Positive-entry asymptotic for terminal (ain{0,1}) | D7, D9–D10, F1 | HIGH |
| E2 | Low-phase asymptotic for start (ain{0,1}) | D8–D10, F1 | HIGH |
| E3 | Exact bridge atom penalty | A1, F1 | MODERATE |
| E4 | Compare the four terminal routes | E1–E3 | MODERATE |
| E5 | Prove (0	o0) is uniquely cheapest at linear order | E4, real inequalities | LOW |
| E6 | Uniform local (q_mu(m)) theorem in (L,	heta) | E1–E5 | HIGH |
| E7 | Phase cancellation in (x=log_2mu) | E6, log algebra | HIGH |

### Layer F — finite probability and conditioning

| ID | Formal statement | Direct dependencies | Risk |
|---|---|---|---|
| F1 | Integer-mean geometric law and finite products | pinned Mathlib geometric/product APIs | MODERATE |
| F2 | Conditioning on total (t) gives exact uniform weak compositions | F1, uniform PMF | MODERATE |
| F3 | Exact local block likelihood ratio | F1–F2, binomial/falling-product algebra | HIGH |
| F4 | Exact point probability for the total (negative binomial) | F1, stars-and-bars | MODERATE |
| F5 | Required lower/asymptotic bound for that point probability | F4, factorial/Stirling inequalities | HIGH |
| F6 | Adaptive sequential-hazard lemma for disjoint product blocks | F1, finite conditional probability | HIGH |
| F7 | Subcritical failure estimate transferred through total conditioning | F2, F5–F6, B10, E6 | HIGH |
| F8 | Local conditioned/product transfer for supercritical union bound | F2–F3, C6, E1–E2 | HIGH |

The proof should exploit finite atomic measures aggressively; sigma-algebra
generality is unnecessary.

### Layer G — global asymptotics

Define

[
R(x)=x^2+2xlog_2x-2log_2(3e)x
]

and the frozen (c_n).

| ID | Formal statement | Direct dependencies | Risk |
|---|---|---|---|
| G1 | Define and basic-domain lemmas for (R) | real log | LOW |
| G2 | Define and basic-domain lemmas for (c_n) | real sqrt/log | LOW |
| G3 | Fixed-offset expansion of (R(c_npmarepsilon)) | G1–G2 | HIGH |
| G4 | Negative offset gives exponentially many certified front opportunities | G3, B10, E6, F6–F7 | HIGH |
| G5 | Nonstackability below the center | G4, A10, F2 | HIGH |
| G6 | Positive offset kills the deep-message cover | G3, C3–C6, E1–E2, F8 | HIGH |
| G7 | Stackability above the center | G6, F2, complement of nonstackability | MODERATE |
| G8 | Combine both implications into the frozen headline theorem | G5, G7 | MODERATE |

The graph is acyclic: TreeStack/Mathlib foundations feed A/F/D; A feeds
B/C/D; D and F feed E; B/C/E/F feed G.

## 8. Minimal binary-partition analytic interface

Let (A(B)) be the cumulative number of partitions of integers at most (B)
into powers of two, equivalently the Session 7 cumulative binary-partition
count with recurrence

[
A(0)=1,qquad A(B)=A(B-1)+A(lfloor B/2floor)quad(Bge1).
]

The full historical de Bruijn expansion is stronger than ProbStack needs. The
smallest convenient interface is a compact-uniform **linear-scale error**
statement.

For every fixed (0<ale b<infty) and every (eta>0), for all sufficiently
large integers (L), every integer (B) with
(a2^Lle Ble b2^L) satisfies

[
left|
log_2 A(B)
-
left[
rac12L^2
-Llog_2L
+
left(
log_2rac{B}{2^L}
+rac12+log_2 e
ight)L
ight]
ight|
le eta L.
]

This is equivalent to the (o(L)) precision actually consumed downstream and
is enough for every fixed-offset global theorem. It deliberately omits the
periodic (O(1)) term and the stronger (O((log L)^2)) historical remainder.

**Sign consistency.** The cumulative-count asymptotic has
(-Llog_2L). This is the sign used in Session 7 and is what produces
(+Llog_2L) in each negative logarithmic probability cost. The illustrative
formula in the Session 9 prompt displayed the opposite sign for the count;
that display is not adopted because it would contradict the already-frozen
Session 7 local theorem.

### Recommendation

Use a two-stage strategy:

1. **Architecturally isolate D10 now.** Put it in
   `BinaryPartitionAsymptotic.lean` behind the compact-uniform statement
   above. Do not introduce an `axiom`, `sorry`, or an unproved imported
   historical theorem into the final trusted path.
2. **Target a weaker direct proof, not full historical de Bruijn.** First try
   to prove the two-sided (eta L) estimate from the recurrence using
   elementary recurrence/saddle-point bounds. This is materially weaker than
   formalising de Bruijn's complete periodic expansion and is all the frozen
   theorem needs.
3. If that replacement remains research-level, keep D10 as the sole deferred
   analytic bottleneck while fully formalising D1–D9 and all deterministic/
   finite-probability layers that do not depend on it. Intermediate theorems
   may take the D10 statement as an explicit hypothesis; `Main.lean` may not.

Thus the recommended outcome is: **isolate now (C), attempt the simpler
replacement proof (B), and avoid full-strength historical formalisation (A)
unless B fails.**

## 9. Lean-facing headline statement

The final implementation should split the two directions and then package
them.

Schematic interface:

```lean
noncomputable def frozenCenter (n : ℕ) : ℝ :=
  Real.sqrt (Real.logb 2 (n : ℝ))
    - (1 / 2 : ℝ) * Real.logb 2 (Real.logb 2 (n : ℝ))
    + Real.logb 2 (3 * Real.exp 1)

noncomputable def pathStackableProb (n μ : ℕ) : ℝ := ...
-- uniform law on WeakComposition n (n * μ),
-- event TreeStack.Stackable (SimpleGraph.pathGraph n) C

theorem frozen_path_subcritical
    (μ : ℕ → ℕ) (hμ : ∀ n, 0 < μ n)
    (ε : ℝ) (hε : 0 < ε)
    (hbelow :
      ∀ᶠ n in Filter.atTop,
        Real.logb 2 (μ n : ℝ) ≤ frozenCenter n - ε) :
    Tendsto (fun n => pathStackableProb n (μ n))
      Filter.atTop (𝓝 0) := ...

theorem frozen_path_supercritical
    (μ : ℕ → ℕ) (hμ : ∀ n, 0 < μ n)
    (ε : ℝ) (hε : 0 < ε)
    (habove :
      ∀ᶠ n in Filter.atTop,
        frozenCenter n + ε ≤ Real.logb 2 (μ n : ℝ)) :
    Tendsto (fun n => pathStackableProb n (μ n))
      Filter.atTop (𝓝 1) := ...
```

A final theorem may return the conjunction of these two implications. Splitting
them during development is preferable because the proof dependencies are
different.

This statement keeps:

- quantification over positive integer sequences;
- total mass exactly (nmu_n);
- (P_n) as the (n)-vertex Mathlib path on `Fin n`;
- the exact uniform weak-composition law;
- fixed (arepsilon>0);
- eventual inequalities;
- limits (0) and (1).

Small values of (n) are harmless because all hypotheses/conclusions are
filter statements at infinity. Any alternative shifted indexing convention
must first be proved equivalent rather than silently replacing (P_n).

## 10. Proposed Lean source layout

```text
ProbStack/
  TreeStackBoundary.lean
  Path.lean
  PathMessage.lean
  Front.lean
  Regeneration.lean
  Necessity.lean
  FiniteProbability.lean
  Geometric.lean
  Conditioning.lean
  DyadicSimplex.lean
  BinaryPartition.lean
  BinaryPartitionAsymptotic.lean
  LocalExcursion.lean
  DeepMessageCover.lean
  GlobalAsymptotic.lean
  Main.lean
```

Intended imports:

```text
TreeStackBoundary
  ↓
Path → PathMessage → Front → Regeneration
                 ↘ Necessity
FiniteProbability → Geometric → Conditioning
DyadicSimplex → BinaryPartition → BinaryPartitionAsymptotic
PathMessage + Geometric + BinaryPartitionAsymptotic → LocalExcursion
Necessity + LocalExcursion + Conditioning → DeepMessageCover
Front + Regeneration + LocalExcursion + DeepMessageCover + Conditioning
  → GlobalAsymptotic → Main
```

Keep `Main.lean` very small: definitions, the two frozen directions, and the
combined theorem.

## 11. Implementation order

The dependency-driven order is:

1. **Toolchain/bootstrap.** Pin Lean, TreeStack and Mathlib; make
   `TreeStackBoundary.lean` compile.
2. **Deterministic path core.** Path finite-tree wrapper, scalar recurrence,
   EMPTY activation, transfer inequalities, low-phase recurrence/closed form,
   message-versus-mass.
3. **Front/reset/regeneration.** Formalise A9–A10 and B1, B3–B4, B7–B8, then
   the finite geometric pieces B2/B5/B6 and true-front conversion.
4. **Finite probability foundation.** Weak compositions, uniform PMF,
   geometric product law, exact conditioning identity, total point
   probability.
5. **Structural necessity.** C1–C5 and the finite witness-cover skeleton.
6. **Finite binary-partition combinatorics.** D1–D9, including colored slack
   and telescoping, with no asymptotics yet.
7. **Binary-partition analytic bottleneck.** Prove D10 at exactly the
   compact-uniform (o(L)) scale above. This may require multiple sessions.
8. **Local excursion theorem.** E1–E7.
9. **Conditioning/hazard estimates.** F3/F5–F8 as needed by the global proof.
10. **Global assembly.** G1–G8 and the no-sorry `Main.lean`.

This ordering is based on mathematical dependencies, not a fixed number of
sessions.

## 12. Formalisation risk summary

- **LOW RISK:** transfer case arithmetic, EMPTY/nonzero distinction, global
  half-bound, low-phase recurrence, Session 8 interval arithmetic, transfer
  window, deep-seed arithmetic, (3/2) growth, route-coefficient comparison.
- **MODERATE:** path/tree wrapper, scalar recurrence from branch messages,
  prefix/suffix induction, finite dyadic sums, exact geometric interval
  probabilities, uniform weak-composition finite type, conditioned-uniform
  identity.
- **HIGH:** message-versus-mass at path boundaries, finite local witness cover,
  exact likelihood-ratio algebra, negative-binomial/Stirling bounds, adaptive
  conditional-hazard induction, uniform terminal excursion assembly, real-log
  change of variables.
- **RESEARCH-LEVEL FORMAL ANALYSIS:** D10, the compact-uniform binary-partition
  asymptotic. This is the principal formal bottleneck.
- **Global real asymptotics:** technically HIGH but conceptually standard once
  D10/E6 are available; the fixed-offset expansion around (c_n) should use
  existing Mathlib limit/asymptotic lemmas rather than hand epsilon algebra
  everywhere.

Integer parity is LOW/MODERATE because TreeStack already exposes the exact
even/odd transfer lemmas. General generating functions would raise risk
unnecessarily; finite coefficient identities avoid that.

## 13. Session 9 validation status

### Mathematical theorem status

The frozen Session 8 theorem remains the correct formalisation target. No
mathematical change was made in Session 9.

### Python status

No Python code changed and no Python tests were run. Existing recorded status
therefore remains:

- Session 8 targeted regeneration tests: 5 passed;
- last literal full-suite run: 54 tests passed (Session 5);
- exhaustive TreeStack/direct validator:
  146 labelled trees, 33,711 configurations, 166,116 rooted cases,
  zero disagreements.

### Lean status

No ProbStack Lean file was added.

The literal local environment probes were:

```text
command -v lean
# NOT FOUND

command -v lake
# NOT FOUND
```

Accordingly no `lake build` was claimed. The local shell also lacked network
DNS access for a direct Git clone, while the authenticated GitHub connector
remained available for repository inspection. Session 9 therefore obeyed the
rule “if Lean is not configured, document the missing setup rather than
pretending code was checked.”

## 14. Documentation/literature read in Session 9

This was a formalisation-design search only, not a prior-art audit.

Read at the exact TreeStack commit:

- `TreeStack/Basic.lean`;
- `TreeStack/PebblingMove.lean`;
- `TreeStack/Transfer.lean`;
- `TreeStack/Branch.lean`;
- `TreeStack/Message.lean`;
- `TreeStack/Boundary.lean`;
- `TreeStack/RootScore.lean`;
- `TreeStack/Stacking.lean`;
- `TreeStack.lean`;
- `lakefile.lean`;
- `lean-toolchain`.

Read at the exact TreeStack-pinned Mathlib revision:

- `Mathlib/Probability/Distributions/Geometric.lean`;
- `Mathlib/Probability/Distributions/Uniform.lean`;
- `Mathlib/Probability/ConditionalProbability.lean`;
- `Mathlib/Probability/ProductMeasure.lean`;
- `Mathlib/Analysis/Asymptotics/Defs.lean`;
- `Mathlib/Combinatorics/SimpleGraph/Hasse.lean`;
- `Mathlib/Analysis/SpecialFunctions/Log/Base.lean`.

A limited web/GitHub search was also made for Lean formalisation of binary
partitions/A000123/de Bruijn and for Mathlib generating-function/multichoose
support. No dedicated binary-partition asymptotic formalisation was located in
that limited search. This is not a novelty or completeness claim.

## Decision

**YES: the frozen headline theorem is still the correct formalisation target.**

The single best next step is to configure the pinned Lean/Lake dependency
boundary in ProbStack and make the smallest `TreeStackBoundary.lean` plus
path wrapper compile before proving any substantive new mathematics.
