# Session 18 handover — conditioning transfer and global closure

> **Historical handover, superseded only in project-status bookkeeping by
> Session 19.** Its mathematical Session 18 conclusions remain inputs to the
> final theorem. Current formalisation and reproducibility status is recorded in
> `docs/FINAL_THEOREM_STATUS.md` and `docs/PROOF_DEPENDENCY_MAP.md`.


## Starting validated state

Session 18 started from exact validated main HEAD

`ed811d42ea789c13a14f0d7f3e91fdbaf48be7ea`.

The authoritative dependency boundary remains:

- TreeStack: `f4112f08d42a37c0941bf469ac124621b1f54f22`;
- Mathlib: `065356127b1dc0016f66b7283ce0ce2c4055aa55`;
- Lean: `leanprover/lean4:v4.35.0-rc2`.

EMPTY remains categorical and distinct from integer zero. The frozen path
theorem is unchanged.

## Session 18 mathematical result

Session 18 closes the remaining global probabilistic gap. The Session 17 local
one-sided excursion theorem was treated as a black box:

[
-log_2 q_mu(m)
=
x^2+2xlog_2 x-2log_2(3e)x+o(x),
qquad x=log_2mu,
]

uniformly for integer (min[mu,2mu]) and over the dyadic phase.

The authoritative frozen center remains

[
c_n
=
sqrt{log_2 n}
-\frac12log_2log_2 n
+log_2(3e).
]

The MINUS sign is essential and was independently checked in the Session 18
balance calculation.

For every fixed (\varepsilon>0):

- if (log_2mu_nle c_n-\varepsilon) eventually, then the uniform
  weak-composition configuration on (P_n) is nonstackable with probability
  tending to one;
- if (log_2mu_nge c_n+\varepsilon) eventually, then it is stackable with
  probability tending to one.

No zero-offset assertion is added.

## Exact conditioning identity

For iid geometric coordinates with

[
p=\frac1{1+mu},qquad r=\frac{mu}{1+mu},
qquad P(X_i=a)=p r^a,
]

every vector of fixed total (t) has product mass (p^n r^t). Therefore
conditioning on (sum_iX_i=t) is exactly the uniform weak-composition law.

At (t=nmu),

[
P!left(sum_iX_i=nmuight)
=
\binom{n+nmu-1}{nmu}
(1+mu)^{-n}
left(\frac{mu}{1+mu}ight)^{nmu}.
]

The cancellation-free Robbins/Stirling bounds give

[
-log_2 P!left(sum_iX_i=nmuight)
=
\frac12log_2 n
+\frac12log_2(mu(mu+1))
+O(1).
]

Thus at the frozen threshold the conditioning cost has only (O(log n))
bits.

## Local product-to-conditioned transfer

For a local (k)-vector of mass (s), the exact likelihood ratio is

[
R_{n,t,k}(s)
=
\frac{(n-1)_k(t)_s}{(n+t-1)_{k+s}}
Big/
left[
left(\frac n{n+t}ight)^k
left(\frac t{n+t}ight)^s
ight].
]

Under the standard half-range hypotheses,

[
|log R_{n,t,k}(s)|
le
\frac{k(k+1)}n
+\frac{s(s-1)}t
+\frac{(k+s)(k+s+1)}{n+t}.
]

One bounded block therefore transfers with factor (exp(o(1))) in the
threshold regime. Two separated bounded blocks are treated as one displayed
vector with doubled support and mass; conditional independence is never
assumed.

## Session 8 regeneration recovered exactly

For (-mu<Mle2mu), one steering coordinate in

[
[2mu+2-M,,4mu-M]capmathbb Z
]

forces the next message into ([mu,2mu]). The occupancy is at most
(5mu-1).

With (r=mu/(mu+1)), the exact worst-case steering probability is

[
delta_mu
=
r^{3mu+1}(1-r^{2mu-1}),
]

and for every integer (muge16),

[
delta_muge \frac{8}{17e^3}>0.0234.
]

If the reset output is already at most (-mu), regeneration is skipped.

## Subcritical spatial proof

A reserved block contains the Session 4 reset, one steering coordinate, the
Session 17 local excursion support, and the Session 4 runaway buffer. Its
length is (O(log n)), so each half contains

[
B_n=Omega(n/log n)
]

disjoint candidates.

Under the product law, conditioned on all previous failed attempts, the next
unused coordinates are fresh geometrics. Hence the sequential success
probability is uniformly at least (p_{mu,n}), with

[
-log_2p_{mu,n}=R(log_2mu)+o(log_2mu).
]

Therefore

[
P_{m prod}(\text{no successful block and }Tle2nmu)
le
exp(-B_np_{mu,n}).
]

Only after this product-law bound is obtained do we condition on (T=nmu).
No conditioned block independence is used.

At (x=c_n-\varepsilon),

[
log_2(B_np_{mu,n})
=
(2\varepsilon+o(1))sqrt{log_2 n},
]

so the exponent (B_np_{mu,n}) overwhelms the merely (O(log n))
conditioning-log cost. Apply the same argument in reverse on the other half
and use a union bound. Opposing certified fronts give nonstackability.

## Supercritical spatial proof

The exact Session 5 deterministic necessity is retained:

[
\text{nonstackable}
Longrightarrow
\text{some directed message}le-(2mu-1).
]

The target is not replaced by (-mu).

The Session 7/17 terminal-specific cover has the same optimized phase-free
interior rate. The (0\to0) route is cheapest. A (1\to0) route requires an
exact-output-zero bridge and therefore one prescribed geometric occupancy,
costing (L+O(1)) bits; polynomially many bridge locations are lower order.

There are (O(n)) interior locations. Physical-boundary witnesses have only
(O(1)) locations and no factor (n). Each local upper-cover pattern has
support (O(L^2)) and mass (O(mu L^2)), so local conditioning transfer
costs only (exp(o(1))).

At (x=c_n+\varepsilon),

[
log_2!left(n,P(\text{one interior cover})ight)
=
-(2\varepsilon+o(1))sqrt{log_2 n},
]

and the conditioned deep-message union probability tends to zero. The exact
necessity theorem then gives stackability with probability tending to one.

## Fixed-offset balance

Putting (N=log_2n), (s=sqrt N), and
(x=s-log_2s+log_2(3e)+delta), Session 18 checks

[
R(x)=N+2delta s+o(s),
]

hence

[
N-R(x)=-2deltasqrt N+o(sqrt N).
]

This confirms both the MINUS half-log-log sign and the constant
(log_2(3e)).

## New Session 18 repository material

Added:

- `prob_stack/global_conditioning.py`;
- `tests/test_global_conditioning.py`;
- `scripts/tabulate_global_conditioning.py`;
- `data/session18_global_balance.csv`;
- `data/session18_global_balance.csv.meta.json`;
- `notes/session-18-conditioning-global.md`;
- this handover.

Updated:

- `README.md`;
- `docs/ROADMAP.md`;
- `docs/REPRODUCIBILITY.md`.

A temporary Python-validation workflow is used only on the Session 18 branch
and must not remain on final main.

## Lean status

No new Lean theorem was needed in Session 18. The existing finite Lean layer
already exposes the exact boundary used by the global paper proof:

- weak-composition count and matched product-vector mass;
- constant mass on a fixed-total fibre;
- conditioned local-vector mass and likelihood ratio definitions;
- exact left/right regeneration;
- explicit finite seed support and mass bounds;
- runaway support;
- genuine left/right seed-to-front composition;
- deterministic deep-message and opposing-front implications.

The analytic Robbins/Stirling estimate, the Session 17 asymptotic rate, and
the final global limiting argument remain paper mathematics. No attempt should
be made to formalise those merely for completeness.

## Exact Session 19 target

Session 19 is the final theorem/formalisation/reproducibility closure stage.
It should not discover a new probabilistic theorem.

Its tasks are:

1. align the repository's final mathematical theorem statement everywhere with
   the frozen center and fixed-offset quantifiers;
2. build a theorem/proof dependency map from TreeStack semantics through the
   finite Lean interfaces and the isolated analytic paper theorems to the
   headline path result;
3. close only genuinely useful tractable Lean interface gaps, especially any
   finite weak-composition/cardinality or finite-sum conditioning statement
   needed to make the boundary explicit;
4. remove or clearly label stale Session 6/7 intermediate bounded-gap claims
   so they cannot be mistaken for the final proof architecture;
5. ensure all scripts, tables, notes, README and reproducibility instructions
   agree with the final theorem;
6. run the complete Python suite and permanent Lean CI;
7. verify dependency pins, EMPTY semantics, and no-`sorry`/no-`axiom`
   guarantees one final time.

After Session 19, and only then, the project can move to the separate
prior-art/originality audit and paper-preparation stages.
