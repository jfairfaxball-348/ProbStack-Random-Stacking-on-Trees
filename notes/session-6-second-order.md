# Session 6: second-order dyadic-simplex theorem

Status: proved mathematics, with exact finite checks and executable rigorous
bounds.  This note sharpens the Session 3 one-sided theorem and transfers the
new rate through the Session 4/5 global arguments.  It does not resolve the
bounded-offset critical window.

Throughout, X is geometric on {0,1,...} with integer mean mu,

P(X=x)=p r^x,  p=1/(mu+1),  r=mu/(mu+1),

and L=ceil(log_2 mu).  The TreeStack transfer is unchanged and EMPTY remains
categorical.

## 1. Dyadic weighted-simplex lemma

For positive integer k and B, put

E_{k,B}={x in Z_{\ge0}^k : sum_{j=1}^k 2^{j-1} x_j <= B}.

Let N_{k,B}=|E_{k,B}|.  Unit-cube comparison with the continuous weighted
simplex gives exactly

B^k / (k! 2^{k(k-1)/2})
<=
N_{k,B}
<=
(B+2^k-1)^k / (k! 2^{k(k-1)/2}).

For the lower inequality, the unit cubes anchored at lattice points in
E_{k,B} cover the continuous simplex of budget B.  For the upper inequality,
their union lies inside the continuous simplex of budget B+sum_j 2^{j-1}.

On E_{k,B}, sum_j x_j <= B.  Therefore

p^k r^B N_{k,B}
<=
P(E_{k,B})
<=
p^k N_{k,B}.

Consequently, whenever

k=L+O(1),  B=Theta(mu),  2^k=Theta(mu),

Stirling gives the uniform estimate

log_2 P(E_{k,B})
=
-L^2/2 - L log_2 L + O(L).                           (1)

The same statement holds when the dyadic weights are reversed.  The
factorial k! is the term missed by the Session 5 coordinatewise cap upper
bound and is also the reason that the Session 3 rectangular witness paid an
L log L loss.

## 2. Sharpened lower bound for q_mu

Recall the finite-block quantity

q_mu(m)
=
P_m[min_{1<=j<=4L} M_j <= -mu],

uniformly for integer m in [mu,2mu].

### Positive descent simplex

Take N=L+2 and require

sum_{j=1}^N 2^{j-1} X_j
<=
2^N-2mu-1.                                             (2)

The global transfer inequality F(x)<=x/2 implies

M_N
<=
[m + sum_j 2^{j-1}X_j]/2^N
<
1.

Since M_N is an integer, (2) forces M_N<=0 for every m<=2mu.  Its budget is
Theta(mu), so by (1) its probability is

2^{-L^2/2-L log_2 L+O(L)}.                             (3)

### Low-phase amplification simplex

Starting from any M<=0, write Z=3-M, so Z>=3.  On the next L coordinates
require

sum_{j=1}^L 2^{L-j} X_j <= 2^{L-1}.                    (4)

Equivalently, sum_j 2^{1-j}X_j<=1.  Every prefix then has normalized deficit

W_j
=
Z_0-sum_{s=1}^j 2^{1-s}X_s
>=2,

so every update stays in the low phase.  At the end,

Z_L=2^L W_L >= 2^{L+1},

hence M_L<=-mu for mu>=16.  Again (1) gives probability

2^{-L^2/2-L log_2 L+O(L)}.                             (5)

The two blocks are independent and have total length 2L+2<=4L.  Therefore

q_mu(m)
>=
2^{-L^2-2L log_2 L+O(L)}.                             (6)

This lower event is a weighted simplex, not the old rectangular cap witness.

## 3. Matching upper bound for q_mu

Suppose a trajectory starting from m in [mu,2mu] hits M<=-mu by time 4L.

Let tau be its first visit to M<=1.  Before tau, every message is at least 2.
For effective value y>=2,

2F(y)=y-delta,  delta in {0,3},

and also

F(y)+3 >= (y+3)/2.

Thus M_tau+3 >= (m+3)/2^tau.  Since M_tau is 0 or 1, tau>=L-2.

Put k=L-2 and examine the last k positive-phase updates before tau.  Iterating
the exact parity formula gives

sum_{j=1}^k 2^{j-1}X_j
=
2^k M_tau-M_{tau-k}
+
sum_{j=1}^k 2^{j-1}delta_j
<=
4*2^k-5.                                               (7)

Hence every positive entry supplies a necessary dyadic simplex of the form
(1), with probability at most

2^{-L^2/2-L log_2 L+O(L)}.                             (8)

Now let T be the first hit of M<=-mu and let rho<T be the last time with
M_rho>=0.  Then M_rho is 0 or 1, and every later update through T is in the
low phase.  Starting deficit is at most 3.  The final low run has length at
least L-2, because without occupancies its deficit can grow by at most a
factor 2 per step.

For the first k=L-2 steps of this final run, Z_k>=4 and the exact low-phase
identity yields

sum_{j=1}^k 2^{k-j}X_j
<=
3*2^{k-1}-2.                                           (9)

This is a reversed dyadic simplex with the same upper probability as (8).
The entry block and final low block are disjoint.  There are at most (4L)^2
choices of their locations.  Therefore

q_mu(m)
<=
2^{-L^2-2L log_2 L+O(L)}.                             (10)

Combining (6) and (10) proves:

**Second-order one-sided theorem.** Uniformly for integer
m in [mu,2mu],

-log_2 q_mu(m)
=
L^2 + 2L log_2 L + O(L).                              (11)

Thus the Session 3 O(L log L) mismatch is closed at the coefficient level:
the explicit coefficient is

alpha = 2.

The beta coefficient in a possible expansion
L^2+2L log_2 L+beta L+o(L) remains open.

## 4. Session 5 deep-message upper cover at second order

For the Session 5 threshold -(2mu-1), the same positive-entry simplex applies.
The final low run may begin from message -1, so its initial deficit is at most
4.  Its first L-2 updates therefore satisfy a reversed dyadic simplex with
budget

2^{L-1}-2 = Theta(mu).

Let a_mu and b_mu now denote rigorous upper probabilities for these entry and
low simplices.  Then

log_2 a_mu
=
-L^2/2-L log_2 L+O(L),

log_2 b_mu
=
-L^2/2-L log_2 L+O(L).                                (12)

The Session 5 middle-gap mechanism is unchanged.  While there is neither a
return to height at least mu nor a deep hit, every intervening occupancy is
at most 4mu.  Since P[X<=4mu] is bounded strictly below one, choosing
R=Theta(L^2) makes the probability of R consecutive middle caps at most
b_mu.

Hence a one-direction scan with N transfers obeys

P_prod[some message <= -(2mu-1)]
<=
poly(L) b_mu
+
N poly(L) a_mu b_mu,                                  (13)

so the boundary term has exponent

-L^2/2-L log_2 L+O(L),

while the interior term has exponent

-L^2-2L log_2 L+O(L).                                 (14)

There are only two physical boundaries, so the half-rate boundary mechanism
cannot determine the global second-order recovery scale.

## 5. Conditioning precision

The sharpened upper-cover atoms have window length O(L^2) and mass
O(mu L^2): the two simplex blocks each have total mass O(mu), and the middle
cluster contributes O(mu L^2).

The exact Session 3 likelihood-ratio estimate therefore gives

Delta_n
=
O(L^4/n + mu L^4/n)
=
o(1)

throughout the stretched-log regime, including the second-order scale below.
Thus the supercritical union bound transfers with multiplicative
exp(o(1)) error.

For the subcritical spatial certificate, use the Session 4 reset and runaway
blocks but intersect them with local mass truncations.

- The reset event has probability at least 1/3-1/(mu+1).  Its block has
  expected mass mu r, so intersecting with total reset mass at most
  12 mu r leaves a positive absolute probability by Markov.
- The runaway cap event has the universal probability lower bound
  c_*>0.009599.  Its block has expected mass mu u, so intersecting with total
  runaway mass at most 256 mu u still leaves a positive absolute probability.
- The new two-simplex deep witness itself has deterministic mass O(mu).

The resulting certified-front superblock still has probability

2^{-L^2-2L log_2 L+O(L)},                             (15)

length O(log n), and deterministic local mass O(mu log n).

At the critical scale log_2 n=Theta(L^2), both a single superblock and the
union of two disjoint superblocks have conditioned/product likelihood ratio
exp(o(1)).  If Y counts disjoint certified blocks in one half of the path,
then

E_cond Y = (1+o(1)) E_prod Y,

and for distinct blocks i,j,

P_cond(E_i cap E_j)
=
(1+o(1)) P_prod(E_i)P_prod(E_j).

Therefore the elementary second-moment bound gives
P_cond[Y=0]->0 whenever the product expectation tends to infinity.  Applying
the same argument to the reversed blocks in the other half produces opposing
irreversible fronts with high probability, hence nonstackability.

This replaces the Session 4 division by
P_prod[sum X_i=nmu] and its unwanted sqrt(n) loss.

## 6. Second-order global recovery scale

Let

N=log_2 n,
s=sqrt(N),
a_n=s-log_2 s
   =sqrt(log_2 n)-0.5 log_2 log_2 n.

Let L_n=ceil(log_2 mu_n), with integer mu_n and total t=n mu_n.

From (13)-(15), the controlling interior exponent is

N - [L^2+2L log_2 L] + O(L).                          (16)

If L=a_n+d_n with d_n=o(s), direct expansion gives

L^2+2L log_2 L-N
=
2s d_n + O(s)                                         (17)

uniformly whenever |d_n| is at most o(s); the weaker O(s) form is enough for
the following dichotomy.

**Second-order global theorem.**

If

L_n-a_n -> -infinity,

then a uniformly random weak composition of total n mu_n on P_n is
nonstackable with probability tending to one.

If

L_n-a_n -> +infinity,

then it is stackable with probability tending to one.

Equivalently, the proved second-order centering is

log_2(t/n)
=
sqrt(log_2 n)
-
0.5 log_2 log_2 n
+
bounded-order unresolved terms.

This is a second-order centering theorem, not a resolved critical window.
The regime L_n-a_n=O(1) remains open.

## 7. Exact finite computation

The companion script

python scripts/tabulate_second_order_bounds.py \
  --levels 6,8,10,12,16,20,30,40,50 \
  --exact-through-level 10 \
  --output data/second_order_local_bounds.csv

evaluates the rigorous analytic bounds.  For L<=10 it also computes the two
weighted-simplex witness probabilities exactly by a rational dynamic
programme.  Those exact columns validate the new small-deviation objects; they
are not estimates of q_mu itself and are not used to infer the theorem.

The deterministic sharpened first-deep-hit cover was also checked exhaustively
on all 7^6 occupancy strings in {0,...,6}^6 at mu=16.

No Monte Carlo was used in Session 6.

## 8. What remains open

Session 6 does not determine beta in

-log_2 q_mu
=
L^2+2L log_2 L+beta L+o(L),

does not identify a limiting law in the bounded-offset regime, does not prove
finite-n monotonicity in total mass, and does not establish a Poisson-clumping
description of rare front locations.

The conditioning error is already o(1) on the relevant local and pair events,
so it is not the apparent obstruction to a beta calculation.  The next
mathematical target is the linear-in-L term in the dyadic weighted-simplex
excursion probability, including the exact interaction of the positive parity
penalties and the final low-phase budget.
