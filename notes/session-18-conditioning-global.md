# Session 18 — conditioning transfer and global path asymptotics

## Frozen boundary

Session 18 starts from validated main HEAD

ed811d42ea789c13a14f0d7f3e91fdbaf48be7ea.

The TreeStack, Mathlib and Lean pins are unchanged. EMPTY remains categorical.
The frozen path theorem and its center are unchanged. In particular the center
has the MINUS sign

c_n = sqrt(log_2 n)
      - (1/2) log_2 log_2 n
      + log_2(3e).

Session 17's local theorem is used as a black box throughout this note.

Write

x = log_2 mu,

and, uniformly for integer starting messages m in [mu,2mu],

-log_2 q_mu(m)
=
R(x)+o(x),

R(x)
=
x^2 + 2x log_2 x - 2 log_2(3e)x.

No local coefficient is recomputed here.

## 1. Exact conditioning identity

Let X_1,...,X_n be iid geometric variables on the nonnegative integers with

p = 1/(1+mu),
r = mu/(1+mu),
P(X_i=a) = p r^a.

For a vector a=(a_1,...,a_n) of total t,

P_prod(X=a) = p^n r^t.

Hence all vectors in the fixed-total fibre have exactly the same product
probability. Conditioning on

T = sum_i X_i = t

therefore gives the uniform law on weak compositions of t into n parts.

For every event A on configurations, the exact event-level identity is

P_wc,t(A)
=
P_prod(A | T=t)
=
P_prod(A and T=t) / P_prod(T=t).

For the headline theorem t=n mu.

The exact conditioning point mass is the negative-binomial value

P_prod(T=n mu)
=
choose(n+n mu-1,n mu)
(1/(1+mu))^n
(mu/(1+mu))^(n mu).

The new Python function conditioning_point_probability evaluates this exact
quantity with Fraction arithmetic for feasible finite inputs.

## 2. Size of the conditioning cost

The cancellation-free Robbins/Stirling bounds already implemented in
prob_stack/product_spatial.py give, uniformly in the threshold regime,

-log_2 P_prod(T=n mu)
=
(1/2) log_2 n
+
(1/2) log_2(mu(mu+1))
+
O(1).

Since x=log_2 mu,

-log_2 P_prod(T=n mu)
=
(1/2) log_2 n + x + O(1)

when mu tends to infinity. At the frozen threshold x=O(sqrt(log_2 n)), so the
reciprocal conditioning cost has only O(log n) bits.

This is not small compared with one local rare event. The relevant
subcritical comparison is instead with the exponent in the product no-success
probability. That exponent is exponentially larger at every fixed negative
offset, as shown below.

## 3. Exact local product-to-conditioned transfer

For a fixed local k-vector of total mass s under the matched product law
p=n/(n+t), r=t/(n+t), the exact likelihood ratio is

R_{n,t,k}(s)
=
P_cond(local vector) / P_prod(local vector)

=
[(n-1)_k (t)_s / (n+t-1)_(k+s)]
/
[(n/(n+t))^k (t/(n+t))^s].

Equivalently it is the product

prod_{i=1}^k (1-i/n)
prod_{j=0}^{s-1} (1-j/t)
prod_{ell=1}^{k+s} (1-ell/(n+t))^(-1).

If k<=n/2, s<=t/2 and k+s<=(n+t)/2, then

|log R_{n,t,k}(s)|
<=
Delta(n,t,k,s),

where

Delta
=
k(k+1)/n
+
s(s-1)/t
+
(k+s)(k+s+1)/(n+t).

Therefore any event supported on k displayed coordinates and local mass at
most S has conditioned/product ratio between exp(-Delta) and exp(Delta), with
s replaced by S.

For two separated bounded blocks, concatenate their displayed coordinates.
If each block has support at most k and mass at most S, the same statement
applies with 2k and 2S. No conditional independence is asserted or used.

This is packaged by one_block_transfer_log_bound and
separated_blocks_transfer_log_bound.

### Scale check

The Session 7/17 optimized fixed-delay excursion lower events have support
2L+O_eta(1) and deterministic mass O_eta(mu). The steering coordinate is at
most 5mu-1.

The Session 6 local truncations for reset and runaway keep positive constant
probability and give a whole reserved superblock support O(log n) and mass
O(mu log n).

Thus for one or two such bounded superblocks,

Delta
=
O((log n)^2/n + mu (log n)^2/n)
=
o(1)

uniformly when

mu = 2^{O(sqrt(log_2 n))}.

So one-block and two-block conditioned probabilities agree with their product
probabilities up to exp(o(1)). This fact is useful for local comparisons, but
the subcritical global proof below deliberately does not assume independence
after conditioning.

## 4. Exact Session 8 regeneration

Let M be an integer message with

-mu < M <= 2mu.

Define the one-coordinate steering interval

I_mu(M)
=
[2mu+2-M, 4mu-M] intersect Z.

If X lies in this interval, then

2mu+2 <= M+X <= 4mu,

and the exact TreeStack transfer satisfies

mu <= F(M+X) <= 2mu.

The largest possible steering occupancy is 5mu-1.

Writing r=mu/(mu+1), the exact steering probability is

r^(2mu+2-M) [1-r^(2mu-1)].

It is minimized at M=-mu+1, so

delta_mu
=
r^(3mu+1)[1-r^(2mu-1)].

For every integer mu>=16,

delta_mu >= 8/(17 e^3) = 0.0234292086....

If the reset output already satisfies M<=-mu, steering is skipped and the
deep seed has already been obtained.

Thus reset plus regeneration enters the Session 17 starting window at constant
cost and loses no linear-in-x exponent.

## 5. Product-law reserved superblocks

The Session 8 reserved superblock consists of

1. the Session 4 reset block;
2. one reserved regeneration coordinate;
3. at most 4L local-excursion coordinates;
4. the Session 4 runaway buffer.

The reset length is ceil(log_2(4n)). The runaway deficit grows by at least a
factor 3/2 until it dominates 2nmu+3, so its length is O(log n). Hence the
whole reserved superblock length is

b_n = O(log n).

On the product event T<=2nmu, every incoming message is at most the available
prefix mass and hence at most 2nmu. The reset therefore supplies the exact
incoming upper bound required by Session 8.

Conditional on any preceding product-law history with no earlier successful
block, the next unused block contains fresh iid geometric coordinates. The
reset, regeneration, Session 17 excursion and runaway pieces therefore give a
uniform sequential success probability p_{mu,n} satisfying

-log_2 p_{mu,n}
=
R(x)+o(x),

uniformly over the dyadic phase and over all admissible incoming states.

This sequential hazard statement is enough. The block indicators do not need
to be identically defined functions of isolated blocks, and no conditioned
independence is claimed.

## 6. Subcritical side under exact conditioning

Use disjoint reserved superblocks in the left half of the path. If B_n denotes
their number, then

B_n = Omega(n/log n).

The sequential product-law hazard gives

P_prod(no successful left front and T<=2nmu)
<=
(1-p_{mu,n})^{B_n}
<=
exp(-B_n p_{mu,n}).

Exactly the same construction, reversed, is used in the right half.

Now condition on T=nmu. Since T=nmu implies T<=2nmu,

P_cond(no left front)
<=
exp(-B_n p_{mu,n}) / P_prod(T=nmu).

The same inequality holds on the right. A union bound, not conditioned
independence, gives the probability that at least one of the two opposing
fronts is missing.

Put

N = log_2 n,
s = sqrt(N),
a = log_2(3e),

and

c_n = s - log_2 s + a.

Section 8 below proves, for every fixed epsilon>0,

N - R(c_n-epsilon)
=
(2epsilon+o(1))s.

The O(log n) block spacing subtracts only O(log N) from log_2(B_n p_{mu,n}).
Therefore

log_2(B_n p_{mu,n})
=
(2epsilon+o(1))s.

In particular B_n p_{mu,n} itself is

2^{(2epsilon+o(1))s},

whereas

-log P_prod(T=nmu) = O(N).

Hence

exp(-B_n p_{mu,n}) / P_prod(T=nmu) -> 0.

The product no-success exponent overwhelms the reciprocal conditioning point
mass by a large margin.

When the two opposing certified fronts occur, the deterministic TreeStack path
front theorem excludes all possible roots, so the configuration is
nonstackable.

Therefore, for every fixed epsilon>0, if

log_2 mu_n <= c_n-epsilon

eventually, then

P(C_n is stackable) -> 0.

If mu_n does not tend to infinity, the finitely many small-mean regimes are
handled by the earlier finite superblock construction; the Session 17
asymptotic is needed only on subsequences with mu_n tending to infinity.

## 7. Supercritical side

For total t=nmu, Session 5 proved the exact deterministic necessity

nonstackable
implies
some directed message <= -(2mu-1).

The target is exactly -(2mu-1); it is not replaced by -mu.

The Session 7/17 terminal-specific cover gives the following product-law
structure for an interior first deep hit.

- The positive-entry and final-low blocks are disjoint.
- The 0 to 0 terminal route has the largest probability at linear order.
- The 1 to 0 route needs an exact-output-zero bridge. Since F(y)=0 only at
  y=3, one geometric occupancy is fixed once the incoming message is fixed,
  and this bridge costs L+O(1) bits.
- Polynomially many entry, bridge and cluster locations contribute only
  o(x) to the logarithm.
- The bounded middle cluster contributes only o(x).
- Reversal preserves the same estimates.

Thus the interior one-location cover has the same phase-free rate

2^{-R(x)+o(x)}.

There are O(n) spatial locations and only polynomially many local variants, so

P_prod(interior deep hit in either direction)
<=
2^{N-R(x)+o(x)}.

The physical-boundary mechanism has only O(1) locations. It uses one
half-rate low simplex and tends to zero on its own; it does not receive a
factor n.

Every local upper-cover pattern has support O(L^2) and mass O(mu L^2), so the
exact local likelihood-ratio bound gives a conditioned/product factor
exp(o(1)) uniformly in the frozen threshold region. This avoids division by
the global conditioning point probability on the supercritical side.

Section 8 gives, for fixed epsilon>0,

N-R(c_n+epsilon)
=
-(2epsilon+o(1))s.

Consequently the conditioned union-cover probability tends to zero. By the
deep-message necessity theorem,

P(C_n is nonstackable) -> 0,

or equivalently

P(C_n is stackable) -> 1

whenever

log_2 mu_n >= c_n+epsilon

eventually.

## 8. Fixed-offset algebra at the frozen center

Let

x = c_n + delta
  = s - log_2 s + a + delta,

where delta is fixed.

Write u=-log_2 s+a+delta, so x=s+u and u=O(log s). Expanding

log_2(s+u)
=
log_2 s + u/(s ln 2) + O(u^2/s^2)

gives

R(c_n+delta)
=
N + 2delta s + O((log s)^2).

The stabilized local theorem has an additional o(x)=o(s) remainder, uniformly
over the allowed dyadic phase. Therefore

N-R(c_n+delta)
=
-2delta s + o(s).

In particular:

- for delta=-epsilon, the spatial hazard exponent is
  +(2epsilon+o(1))sqrt(N);
- for delta=+epsilon, the O(n) union-cover exponent is
  -(2epsilon+o(1))sqrt(N).

This checks both the MINUS half-log-log term and the constant log_2(3e).
Changing either destroys the cancellation of the order s log s or order s
terms.

The function fixed_offset_scaled_residual evaluates the main-rate ratio

[N-R(c_n+delta)]/sqrt(N),

which tends to -2delta.

## 9. Uniformity

The final argument is uniform over arbitrary integer sequences mu_n in the
fixed-offset regimes.

The imported Session 17 local theorem is uniform over

theta = mu/2^ceil(log_2 mu) in (1/2,1]

and over starting messages m in [mu,2mu].

The regeneration lower bound is uniform for all integer mu>=16.

The local conditioning bounds are deterministic and depend only on support and
mass caps. In the frozen threshold region their error is o(1) uniformly in
the dyadic phase.

The phase-free rate removes the artificial ceiling-phase dependence at linear
order. No powers-of-two restriction is used.

## 10. Computational diagnostics

The new module prob_stack/global_conditioning.py contains:

- the exact negative-binomial conditioning point probability;
- rigorous log2 Robbins/Stirling bounds through the existing implementation;
- one-block and separated-block likelihood-ratio transfer bounds;
- the frozen center;
- the Session 17 phase-free main rate;
- fixed-offset balance diagnostics.

The script scripts/tabulate_global_conditioning.py writes deterministic
diagnostics. The committed table data/session18_global_balance.csv covers

N = 256, 1024, 4096, 16384

and offsets

-2, -1, -1/2, +1/2, +1, +2.

The table records the main local rate, N-R(x), the O(log n)-spacing-adjusted
hazard exponent, the Stirling main conditioning cost, and the logarithmic
ratio between the spaced product hazard and conditioning cost.

The tests explicitly guard against:

- the wrong sign of the half-log-log term;
- the wrong log_2(3e) constant;
- forgetting the factor n;
- treating two conditioned blocks as independent;
- losing a linear term to conditioning.

No Monte Carlo is used.

## 11. Lean boundary

The existing finite Lean layer already contains the exact algebraic core
needed here:

- weakCompositionCount;
- matchedProductVectorMass;
- constant product mass on the fixed-total fibre;
- conditionedLocalVectorMass;
- localLikelihoodRatio;
- exact left/right regeneration;
- capped finite seed support and mass bounds;
- genuine left/right seed-plus-runaway-to-front theorems;
- deep-message and front deterministic interfaces.

Session 18 does not attempt to formalise Robbins/Stirling, de Bruijn
asymptotics, the Session 17 real asymptotic rate, or the global analytic limit.
Those remain paper mathematics.

No sorry and no new axioms are introduced.

## 12. Session 18 conclusion

The last global probabilistic gap is closed at the mathematical level.

The frozen theorem follows from:

1. exact TreeStack path semantics and front/deep-message theorems;
2. the Session 17 local excursion theorem as a black box;
3. the exact geometric conditioning identity;
4. Robbins/Stirling control of the conditioning point mass;
5. Session 8 constant-cost regeneration;
6. sequential product-law spatial abundance below the center;
7. local likelihood-ratio upper-cover transfer above the center;
8. the fixed-offset expansion around the frozen center.

Session 19 should be theorem/formalisation/reproducibility closure, not new
probabilistic discovery.
