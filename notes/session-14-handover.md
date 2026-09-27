# Session 14 handover

## Validated starting state

- Starting main HEAD: `9dbac5201207be55b141ceddadb3d549d82dd9ca`
- TreeStack: `f4112f08d42a37c0941bf469ac124621b1f54f22`
- Mathlib: `065356127b1dc0016f66b7283ce0ce2c4055aa55`
- Lean: `leanprover/lean4:v4.35.0-rc2`

All dependency pins remain unchanged.

The frozen structural criterion remains exactly
`StackableAt(T,C,r) iff 0 < score(T,C,r)`.

`TreeStack.EMPTY = none` remains categorical and was never identified with
integer zero or `some 0`.

The frozen headline path theorem and the zero-offset/critical-window scope
boundary were untouched.

## Main implementation checkpoint

Session 14 was squash-merged to main as

`debd6650a630eeae7508ed934494f5eae11801a3`.

That exact implementation HEAD passed GitHub Actions run

`36324532201`

including:

- the pinned TreeStack dependency build;
- the full ProbStack `lake build`;
- the project grep rejecting local `sorry` and `axiom`.

Before the squash merge, the final branch implementation/documentation tree
was also Lean-CI validated at

`30dcd3ab5c8db7b83673004acc6cc457ba320ebe`

by run

`36324317146`.

Exact-arithmetic Python validation was run separately on the same Session-14
code through a temporary validation-only workflow.  Run

`36337534870`

passed `tests/test_finite_probability.py`.  The temporary workflow was then
removed and its validation-only PR was closed without merging, so the
permanent main workflow was not changed.

The handover file itself is a later documentation commit.  Its exact final
main SHA and exact final-head CI run are reported in the end-of-session
external report; a tracked file cannot contain its own Git commit SHA without
creating a subsequent commit.

## Files added/changed in the Session-14 implementation

Added:

- `ProbStack/FiniteProbability.lean`
- `prob_stack/finite_probability.py`
- `tests/test_finite_probability.py`
- `notes/session-14-finite-probability.md`

Changed:

- `ProbStack.lean` to import `ProbStack.FiniteProbability`.

## Main Lean interface

The new module `ProbStack/FiniteProbability.lean` contains the finite scalar
probability/certificate interface.

### Explicit seed event

Core definitions:

- `affineInputCost`
- `PositiveDescentEvent`
- `LowBudget`
- `lowBudgetFinal`
- `ExplicitDeepSeedEvent`
- `CoordwiseLe`

Main deterministic theorems:

- `two_mul_activeStep_le`
- `activeScan_affine_bound`
- `positiveDescentEvent_forces_nonpositive`
- `lowBudget_lowRun_and_deficit_ge`
- `explicitDeepSeedEvent_uniform`
- `coordwiseLe_length`
- `coordwiseLe_sum`
- `affineInputCost_mono`
- `positiveDescentEvent_of_coordwise`
- `lowBudget_mono`
- `lowBudgetFinal_mono`
- `lowBudget_of_coordwise`
- `cappedSeed_uniformDeepSeedBlock`
- `cappedSeed_support_length`
- `cappedSeed_mass_le`

Thus a syntactically visible finite coordinate-cap event implies

`UniformDeepSeedBlock mu (2*mu) D`

without introducing a hitting-time state predicate.

### Geometric law

The exact support convention is `{0,1,2,...}`, with positive integer mean
`mu`,

`p = 1/(mu+1)`, `r = mu/(mu+1)`,

`P(X=k)=p r^k`.

Lean definitions:

- `geometricP`
- `geometricR`
- `geometricPointMass`
- `geometricCDFMass`
- `geometricIntervalMass`
- `geometricVectorMass`
- `geometricCapProduct`
- `cappedSeedProductMass`

with exact finite product factorisation
`geometricCapProduct_append` and
`cappedSeedProductMass_factor`.

### Runaway block

Lean definitions/theorems:

- `runawayCaps`
- `runawayProductMass`
- `runawayCaps_length`
- `four_mul_le_of_le_runawayCap`
- `runawayBlock_of_coordwise_runawayCaps`

The probability caps are therefore exactly the Session-13 deterministic
constraints `4 X_j <= D_j`, with
`D_{j+1}=D_j+D_j/2`.

### Weak compositions and conditioning core

Lean definitions/theorems:

- `IsWeakComposition`
- `weakCompositionCount`
- `weakCompositionCount_of_pos`
- `weakCompositionCount_zero_zero`
- `weakCompositionCount_zero_succ`
- `matchedGeometricP`
- `matchedGeometricR`
- `matchedProductVectorMass`
- `matchedProductVectorMass_of_length_sum`
- `matchedProductVectorMass_constant_on_total`
- `matchedProductVectorMass_uniform_on_compositions`
- `conditionedLocalVectorMass`
- `matchedProductLocalVectorMass`
- `localLikelihoodRatio`
- `conditionedLocalVectorMass_of_supported`

This formalises the finite algebraic core of the exact conditioning identity:
all matched-geometric atoms in one fixed-total weak-composition fibre have the
same mass.

The full Lean Fintype/cardinality theorem equating an explicit subtype of weak
compositions with `weakCompositionCount` is not yet present.  The exact
stars-and-bars formula and zero-coordinate edge cases are represented
algebraically, while Python exhaustively checks the corresponding finite
counting formulas.

### Genuine path-front corollaries

The probability-facing cap certificate is composed with the already-proved
Session-13 branch theorems through:

- `LeftPath.leftBranch_regeneration_cappedSeed_runaway_to_front`
- `RightPath.rightBranch_regeneration_cappedSeed_runaway_to_front`

No path recursion, branch indexing, or EMPTY semantics were reopened.

## Exact Python finite probability layer

`prob_stack/finite_probability.py` adds exact `Fraction` routines for:

- geometric point and interval probabilities;
- weak-composition counts including `n=0` edge cases;
- cap-vector counts by exact local mass;
- exact iid cap-event probabilities;
- exact conditioned weak-composition cap-event probabilities;
- exact falling-product likelihood ratios;
- exact event-level conditioned/product comparison;
- canonical Session-3 seed caps;
- exact seed support length and local mass bound;
- exact finite runaway caps and probabilities.

The authoritative local likelihood ratio retained from Session 3 is

`R_{n,t,k}(s)`
`= [(n-1)_k (t)_s/(n+t-1)_(k+s)]`
`  / [(n/(n+t))^k (t/(n+t))^s]`,

equivalently the three finite products documented in
`notes/session-14-finite-probability.md`.

For any cap event, the exact conditioned/product event ratio is a
product-law-weighted average of the atom ratios, and therefore lies between
their exact minimum and maximum.  The existing half-range logarithmic error

`Delta = k(k+1)/n + S(S-1)/t + (k+S)(k+S+1)/(n+t)`

is cross-checked against the exact event ratio.

## Canonical seed check

The existing Session-3 canonical cap witness is retained, not replaced.

For `mu=16`:

- descent caps: `(2,1,0,0,0,0,0,0)`;
- amplification caps: `(0,1,2,4)`;
- seed support length: 12;
- deterministic local mass bound: 10;
- certified final deficit: 24.

The exact test exhausts all 180 cap-satisfying vectors and all 17 initial
messages in `[16,32]`, checking 3060 exact trajectories and verifying final
message at most `-16`.

## Status against the Session-14 objectives

- Exact product geometric convention: COMPLETE.
- Basic finite geometric formulas: COMPLETE at the finite algebraic level.
- Explicit finite deep-seed coordinate event: COMPLETE.
- Deterministic implication to `UniformDeepSeedBlock`: FORMAL.
- Exact product-law cap/seed probability: FORMAL algebraic product; canonical
  executable exact probability also implemented.
- Exact finite runaway probability: FORMAL algebraic product plus deterministic
  implication.
- Weak-composition stars-and-bars count: algebraically represented in Lean and
  exhaustively checked in Python; explicit Lean subtype-cardinality theorem
  remains.
- Exact geometric-conditioning representation: finite equal-atom core FORMAL;
  full conditional-probability packaging remains.
- Local likelihood ratio: exact finite Lean definition; authoritative
  falling-product identity executable and exact in Python.
- Finite conditioned/product local-event comparison: exact `Fraction`
  implementation and tests COMPLETE; porting the mass-profile finite-sum
  theorem to Lean remains.
- Genuine left-front probability interface: FORMAL.
- Genuine right-front probability interface: FORMAL.

The finite probability layer is complete enough to begin finite
dyadic/binary-partition combinatorics.  The remaining items are formalisation
depth at the finite counting/conditioning boundary, not a missing
mathematical probability mechanism.

## Session 15 recommended objective

Begin the finite dyadic/binary-partition combinatorics.

The primary target should be an exact finite counting theorem for the
reverse-dyadic descent and low-phase amplification/simplex events, preserving
the explicit support and mass bounds from Session 14.  Recover the existing
binary-partition generating-function identities from the Session-6/7 notes,
verify all indexing and finite endpoints, and formalise the finite identities
before any asymptotic analysis.

In parallel, where it composes naturally with those counts, port the exact
Python mass-profile formula

`sum_s N_s Comp(n-k,t-s) / Comp(n,t)`

and its conditioned/product comparison to a Lean finite-sum theorem.

Do not begin the isolated binary-partition asymptotic until the exact finite
combinatorial identities are stable.  Do not reopen the frozen headline
theorem, critical window, path recursion, or EMPTY semantics.
