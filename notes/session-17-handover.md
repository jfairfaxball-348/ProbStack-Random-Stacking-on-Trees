# Session 17 handover

## Repository boundary

Session 17 starts from validated `main`

`9a36c61833b82f971201c70cc078dbe5b24f8c82`.

The authoritative dependency pins remain:

- TreeStack: `f4112f08d42a37c0941bf469ac124621b1f54f22`;
- Mathlib: `065356127b1dc0016f66b7283ce0ce2c4055aa55`;
- Lean: `leanprover/lean4:v4.35.0-rc2`.

The final Session-17 main SHA and successful Actions run are properties of the
merge containing this handover and are recorded in the external end-of-session
report.

## Important sign correction in the incoming prompt

The Session-17 prompt accidentally wrote the frozen center with
`+(1/2) log_2 log_2 n`.  The authoritative Session-8 theorem and current
README have the minus sign:

```
sqrt(log_2 n)
- (1/2) log_2 log_2 n
+ log_2(3e).
```

Session 17 does not modify the frozen theorem; it merely prevents that
transcription error from being propagated.

## General product-geometric simplex theorem

For fixed integer `s`, compact positive `lambda)-range, uniformly bounded
additive budget shift, and

```
mu=theta 2^L, theta in (1/2,1],
k=L+s,
B=lambda 2^L+O(1),
```

Session 17 proves

```
-log_2 P_mu(E_{k,B})
 = (1/2)L^2
   + L log_2 L
   + [s+log_2 theta-log_2 lambda-1/2-log_2 e]L
   + O((log L)^2).
```

The proof is the exact deterministic sandwich

```
p^k r^B N_{k,B}
 <= P_mu(E_{k,B})
 <= p^k N_{k,B}.
```

The ordinary-mass inequality `sum x_j <= B` handles the complete
geometric weighting, not merely typical vectors.

## Role of p^k and of the tilt

The atom normalization contributes

```
-k log_2 p
 = L^2+[s+log_2 theta]L+O(1).
```

This contribution is essential.

By contrast,

```
B log_2 r
 <= log_2(weighted count/raw count)
 <= 0,
```

and its magnitude is at most `B/(mu ln 2)=O(1)` in every frozen local
regime.  Thus the tilt changes none of the quadratic, `L log L), or linear
coefficients.

## Sharp positive descent

For

```
k=L+2,
B=(4-2theta)2^L-1,
```

```
-log_2 P
 = (1/2)L^2+L log_2 L
   +[3/2+log_2 theta-log_2(4-2theta)-log_2 e]L
   +O((log L)^2).
```

The strict `-1` is retained exactly and affects only lower-order terms.

## Sharp low amplification

For the reversed simplex

```
k=L,
B=2^(L-1),
```

```
-log_2 P
 = (1/2)L^2+L log_2 L
   +[log_2 theta+1/2-log_2 e]L
   +O((log L)^2).
```

Reversal preserves ordinary mass and hence the exact product probability.

## Sharp two-simplex seed

The frozen sharp seed has support exactly `2L+2` and

```
-log_2 P_seed
 = L^2+2L log_2 L+beta_seed(theta)L+O((log L)^2),
```

with

```
beta_seed(theta)
 = 2+2log_2 theta-log_2(4-2theta)-2log_2 e.
```

This is more expensive at linear order than the optimized Session-7 local
excursion.  The distinction is expected: the sharp finite seed is a convenient
witness, not the optimized terminal-specific delayed construction.

## Necessary positive-entry coefficients

For terminal `a in {0,1}`, the exact Session-7 necessary simplex is

```
k=L-2,
B=((a+3)/4)2^L-5.
```

Its coefficient is re-derived as

```
gamma_a^+(theta)
 = log_2 theta-log_2(a+3)-1/2-log_2 e.
```

This matches Session 7 exactly.

## Necessary low-phase coefficients

For start `a in {0,1}`,

```
k=L-2,
B=((3-a)/8)2^L-2,
```

and

```
gamma_a^-(theta)
 = log_2 theta-log_2(3-a)+1/2-log_2 e.
```

This also matches Session 7 exactly.

## Colored slack

The exact Session-15 colored-slack count remains the correct combinatorial
object.  For every colored path of slack budget `B`, the associated ordinary
occupancy mass is at most `B`.  Therefore its probability is squeezed
between `p^k r^B` and `p^k` times the colored count.  Combined with the
Session-16 `O(1)` colored-count comparison, this proves there is no new
linear probability coefficient and no parity constant.

## Terminal-state comparison and zero bridge

Adding the positive-entry and low coefficients gives the four route scales.

The `0 -> 0` route has coefficient

```
2 log_2 theta - log_2 9 - 2 log_2 e
 = 2 log_2 theta - 2 log_2(3e).
```

The `1 -> 0` route requires an exact output-zero bridge.  The bridge fixes one
geometric occupancy once the incoming message is fixed and costs

```
L+O(1)
```

in the negative logarithm.  This adds one to its linear coefficient.
Polynomially many bridge positions do not affect the linear term.

## Local one-sided excursion theorem

Uniformly for integer `m in [mu,2mu]`,

```
-log_2 q_mu(m)
 = L^2
   +2L log_2 L
   +[2log_2 theta-2log_2(3e)]L
   +o(L).
```

The upper bound uses the necessary terminal/start blocks.  The lower bound
uses the fixed-delay Session-7 terminal-zero constructions, with the fixed
delay sent to infinity only after the `L -> infinity` estimate.  Hence the
fully optimized theorem is stated with `o(L)`, not an unjustified
`O((log L)^2)` remainder.

## Phase-free form

With `x=log_2 mu`,

```
-log_2 q_mu(m)
 = x^2
   +2x log_2 x
   -2log_2(3e)x
   +o(x),
```

uniformly for `m in [mu,2mu]`.

## Uniformity

The general simplex theorem is uniform over the full
`theta in (1/2,1]` range whenever the budget scale is in a fixed compact
subset of `(0,infinity)`.

All sharp and necessary frozen regimes satisfy that condition.

For the matching lower constructions, every fixed delay has compact-uniform
budget scales, and the convergence of the fixed-delay coefficients to the
terminal-specific coefficients is uniform over the allowed theta/start
windows.  This yields the stated uniform local theorem.

## Computation and tests

New code:

- `prob_stack/product_geometric_asymptotics.py`;
- `tests/test_product_geometric_asymptotics.py`;
- `scripts/tabulate_product_geometric_asymptotics.py`.

The default diagnostic range is

```
L=4,6,8,10,12
theta=9/16,3/4,1.
```

Exact integer counts are used throughout.  Exact Fraction product
probabilities are checked through `L=8` by default; larger displayed
logarithms use a deterministic one-dimensional weighted DP.

Tests explicitly detect:

- omission of the `p^k` factor;
- treating the geometric tilt as exactly one;
- wrong support offsets;
- wrong theta dependence;
- the wrong sign of `L log_2 L`;
- loss of the sharp positive-descent `-1`;
- confusion between sharp and necessary simplices;
- forward/reverse product-probability disagreement.

Numerics validate the theorem; they do not prove it.

## Lean additions

`ProbStack/FiniteDyadic.lean` adds finite lemmas for:

- ordinary mass bounded by forward dyadic cost;
- ordinary mass invariant under reversal;
- ordinary mass bounded by the reversed forward cost.

The analytic de Bruijn theorem and the real asymptotic probability argument
remain paper proofs rather than Lean formalizations.

## Scope confirmation

Session 17 does not start conditioning transfer or global path asymptotics.

It does not alter:

- the frozen path theorem;
- EMPTY semantics;
- the Session-14 canonical witness;
- TreeStack, Mathlib, or Lean pins;
- the permanent CI design.

No zero-offset theorem, limiting law, arbitrary-tree extension, or novelty
claim is introduced.

## Exact Session-18 target

Session 18 should take the local theorem above as a black box and prove the
conditioning/global transfer only.

The precise target is:

1. transfer one-block and two-block local excursion probabilities from the iid
   geometric law to the uniform weak-composition law at the precision needed
   for fixed offsets;
2. keep the transfer uniform through the frozen threshold window and for the
   spatial start states actually produced by the Session-8 regeneration
   mechanism;
3. prove the global necessity/cover bound on the stackable side;
4. prove the spatial abundance/second-moment bound on the nonstackable side,
   using separated candidate blocks and the already-proved regeneration;
5. combine the two directions at the already-frozen center
   `sqrt(log_2 n)-(1/2)log_2 log_2 n+log_2(3e)`;
6. make no claim at zero offset.

Session 18 should not recompute the local rare-event coefficient.
