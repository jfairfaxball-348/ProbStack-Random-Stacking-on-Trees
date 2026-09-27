# Session 14 — finite probability interface

## Frozen boundary

Session 14 starts from validated main HEAD
`9dbac5201207be55b141ceddadb3d549d82dd9ca`.

Dependency pins are unchanged:

- TreeStack: `f4112f08d42a37c0941bf469ac124621b1f54f22`
- Mathlib: `065356127b1dc0016f66b7283ce0ce2c4055aa55`
- Lean: `leanprover/lean4:v4.35.0-rc2`

The structural semantics are unchanged:
`StackableAt(T,C,r) iff 0 < score(T,C,r)`.
`TreeStack.EMPTY = none` remains categorical and is never identified with
integer zero.  The frozen headline path theorem was not changed.

## Exact geometric convention

For positive integer mean `mu` set

`p = 1/(mu+1)`,  `r = mu/(mu+1)`.

The product law is supported on `{0,1,2,...}` and

`P(X=k) = p r^k`.

The new Lean definitions are:

- `geometricP`
- `geometricR`
- `geometricPointMass`
- `geometricCDFMass`
- `geometricIntervalMass`
- `geometricVectorMass`
- `geometricCapProduct`

Thus

`P(X <= a) = 1-r^(a+1)`

and a visible coordinate-cap event with caps `a_1,...,a_k` has exact iid
probability

`prod_i (1-r^(a_i+1))`.

Theorem `geometricCapProduct_append` proves the finite product
factorisation.  `cappedSeedProductMass` packages the two-stage seed product
and `cappedSeedProductMass_factor` splits it into descent and amplification
factors.

The Python module `prob_stack/finite_probability.py` mirrors these formulas
with `Fraction` arithmetic.

## Explicit finite deep-seed event

The scalar event is deliberately not a hitting-time or Markov-state event.

### Positive descent

`affineInputCost [x_1,...,x_k]` is the reverse-dyadic cost

`x_1 + 2 x_2 + ... + 2^(k-1) x_k`.

The theorem `activeScan_affine_bound` proves

`2^k activeScan(m,xs) <= m + affineInputCost(xs)`.

The visible arithmetic predicate

`PositiveDescentEvent mu xs`

is

`2 mu + affineInputCost(xs) < 2^k`.

Therefore `positiveDescentEvent_forces_nonpositive` sends every
`m <= 2 mu` to a nonpositive message.

### Low-phase amplification

`LowBudget D xs` is the exact recursive finite constraint

- `x <= D-2`;
- replace the certified deficit by `2(D-x)`;
- continue on the next coordinate.

`lowBudgetFinal D xs` is the resulting deterministic final certified
deficit.  The theorem `lowBudget_lowRun_and_deficit_ge` proves both that the
whole block stays in the low phase and that its true final deficit dominates
the certified one.

The two-stage predicate is

`ExplicitDeepSeedEvent mu D descent amplification`

meaning positive descent, then a low-phase budget starting from the universal
deficit lower bound 3, ending at certified deficit at least `D`.

The theorem

`explicitDeepSeedEvent_uniform`

proves

`ExplicitDeepSeedEvent mu D descent amplification`
`=> UniformDeepSeedBlock mu (2*mu) D (descent ++ amplification)`.

### Coordinate-cap version used by probability

`CoordwiseLe xs caps` makes every constrained coordinate visible.
Theorems `coordwiseLe_length`, `coordwiseLe_sum`,
`affineInputCost_mono`, `positiveDescentEvent_of_coordwise`,
`lowBudget_mono`, `lowBudgetFinal_mono`, and
`lowBudget_of_coordwise` show that decreasing coordinates can only improve
the certificate.

The main finite seam is

`cappedSeed_uniformDeepSeedBlock`.

If the deterministic cap lists themselves satisfy
`ExplicitDeepSeedEvent mu D descentCaps amplificationCaps`, then every
actual vector lying coordinatewise below those caps is a
`UniformDeepSeedBlock mu (2*mu) D`.

The support and mass are syntactically readable:

- `cappedSeed_support_length`: support length is exactly
  `descentCaps.length + amplificationCaps.length`;
- `cappedSeed_mass_le`: local mass is at most
  `descentCaps.sum + amplificationCaps.sum`.

This is the finite object to be counted in the binary-partition stage.

## Canonical Session-3 cap witness retained

Python `explicit_seed_caps(mean)` recovers the pre-existing canonical witness
from `canonical_deep_deficit_witness`, rather than inventing a competing
construction.

For `L=ceil(log_2 mu)` and `mu>=16`:

- positive descent has `L+4` caps
  `floor(mu/(L 2^j))`, `j=1,...,L+4`;
- amplification starts at certified deficit 3 and repeatedly uses cap
  `floor(D/L)`, replacing `D` by `2(D-floor(D/L))`, until
  `D>=mu+3`;
- the total support is the exact length of the two stored cap tuples and is
  at most the existing `4L` horizon;
- the exact deterministic local mass bound is the sum of those stored caps.

At `mu=16` the exact cap vectors are

- descent: `(2,1,0,0,0,0,0,0)`;
- amplification: `(0,1,2,4)`.

Thus the seed support is 12 coordinates, the local mass bound is 10, and the
certified final deficit is 24.  The new exhaustive test checks all 180
cap-satisfying occupancy vectors and all 17 starts in `[16,32]`, i.e. 3060
exact trajectories, and verifies that the final message is at most `-16`.

## Runaway block probability

For certified threshold `D`, the Session-13 cap is exactly

`X <= floor(D/4)`

and the next threshold is

`runawayNext D = D + D/2`.

Lean `runawayCaps D k` lists these visible caps and
`runawayProductMass mu D k` is their exact geometric cap product.

Theorems:

- `runawayCaps_length`;
- `four_mul_le_of_le_runawayCap`;
- `runawayBlock_of_coordwise_runawayCaps`

prove that a vector below those probability caps is exactly a
`RunawayBlock` in the Session-13 deterministic sense.

Python `runaway_caps` and `runaway_product_probability` provide the same
finite exact calculation.

## Genuine left/right front interface

No branch recursion was reopened.

The thin corollaries

- `LeftPath.leftBranch_regeneration_cappedSeed_runaway_to_front`;
- `RightPath.rightBranch_regeneration_cappedSeed_runaway_to_front`

compose:

1. the existing genuine regeneration occupancy interval;
2. the explicit coordinate-capped seed event;
3. the explicit coordinate-capped runaway block;

with the Session-13 genuine path-front theorems.  Therefore the local
probability event now feeds directly into a genuine `CertifiedFront` on both
orientations.

## Weak compositions and exact conditioning

Lean defines

`IsWeakComposition n t xs := xs.length=n and xs.sum=t`.

`weakCompositionCount n t` uses the exact edge-aware stars-and-bars count:

- `n=0,t=0`: 1;
- `n=0,t>0`: 0;
- `n>0`: `choose(n+t-1,n-1)`.

The positive-coordinate simplification is
`weakCompositionCount_of_pos`.

For the matched geometric law

`p=n/(n+t)`, `r=t/(n+t)`,

Lean defines `matchedProductVectorMass` and proves

- `matchedProductVectorMass_of_length_sum`;
- `matchedProductVectorMass_constant_on_total`;
- `matchedProductVectorMass_uniform_on_compositions`.

This is the finite algebraic core of the exact conditioning identity: every
product atom in the fixed-total fibre has the same mass.

Lean also defines the exact completion-count probability of one fixed local
vector, `conditionedLocalVectorMass`, its matching product mass, and
`localLikelihoodRatio`.

A full Lean cardinality theorem identifying the Fintype cardinality of a
list-defined weak-composition subtype with `weakCompositionCount` is not yet
added; the exact count formula and edge cases are represented algebraically,
while the repository's existing Python weak-composition enumerator already
tests the same stars-and-bars count exhaustively on small instances.

## Exact local likelihood ratio and finite event comparison

The authoritative formula recovered from the existing Session-3 notes/code is

`R_{n,t,k}(s)`
`= [(n-1)_k (t)_s/(n+t-1)_(k+s)]`
`  / [(n/(n+t))^k (t/(n+t))^s]`,

equivalently

`prod_{i=1}^k (1-i/n)`
`prod_{j=0}^{s-1} (1-j/t)`
`prod_{ell=1}^{k+s} (1-ell/(n+t))^(-1)`.

Python `local_likelihood_ratio_falling_product` implements this exact
`Fraction` product and tests equality with the pre-existing exact binomial
ratio `local_conditioning_ratio`.

For a cap event, `cap_mass_counts(caps)` computes the exact number
`N_s` of local vectors of each mass `s`.  Therefore

`P_prod(E) = p^k sum_s N_s r^s`

and

`P_cond(E) = [sum_s N_s Comp(n-k,t-s)] / Comp(n,t)`.

These are implemented exactly by

- `product_cap_probability_from_counts`;
- `conditioned_cap_probability_from_counts`.

`exact_local_cap_comparison` computes the exact event ratio and the exact
minimum/maximum atom ratios over its support.  Since the event ratio is a
product-law weighted average of the atom ratios, it lies between those exact
extremes.

The existing elementary half-range bound remains

`Delta = k(k+1)/n + S(S-1)/t + (k+S)(k+S+1)/(n+t)`

under `k<=n/2`, `S<=t/2`, and `k+S<=(n+t)/2`.
The new test checks the event-level ratio against `exp(+-Delta)`.

For the small exact check `n=5,t=7,caps=(1,2)`, direct weak-composition
enumeration and the mass-profile completion formula both give
`149/330`.

The event-level exact comparison is currently executable exact Python rather
than a Lean finite-sum theorem.  This is the principal remaining
finite-probability formalisation gap; it does not require any new path
dynamics.

## Files added/changed

Added:

- `ProbStack/FiniteProbability.lean`
- `prob_stack/finite_probability.py`
- `tests/test_finite_probability.py`
- this note

Changed:

- `ProbStack.lean` to import `ProbStack.FiniteProbability`.

## Validation

The Lean development has been compiled repeatedly against the exact pinned
TreeStack/Mathlib/Lean boundary during Session 14.  The final exact main HEAD
and its final-head GitHub Actions run are reported in the Session-14 handover
and end-of-session report after promotion to `main`.

No `sorry` or project `axiom` is introduced.

## Next mathematical target

The finite probability interface is now sufficient to begin finite
dyadic/binary-partition combinatorics without reopening the deterministic path
layer.

Session 15 should take the visible descent/amplification cap/simplex events and
formalise the exact finite counting identities that lead to the
binary-partition generating functions.  The isolated binary-partition
asymptotic itself remains a later stage.  A useful secondary formalisation task
is to port the exact mass-profile conditioned/product comparison from Python
to a Lean finite-sum theorem while the combinatorial event representation is
being built.
