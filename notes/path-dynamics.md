# Exact path dynamics and irreversible deficit fronts

Status: exact deterministic identities and proved lemmas, with computational
cross-checks described below. The asymptotic discussion at the end is
heuristic and is **not** a theorem or promoted conjecture.

## Exact one-dimensional recurrence

Let the path have vertices `0,...,n-1` and configuration
`C=(C_0,...,C_{n-1})`. Let `F` be the exact TreeStack transfer map from
`prob_stack/tree_score.py`. The categorical value `EMPTY` is never identified
with integer zero.

Define `L_i` to be the message from the component strictly to the left of `i`
into `i`, and `R_i` symmetrically from the right. Thus `L_0=EMPTY` and
`R_{n-1}=EMPTY`. For `i<n-1`, the message sent from vertex `i` to `i+1` is
`EMPTY` exactly while `C_0=...=C_i=0`; otherwise it is
`F(C_i + L_i)`, omitting the `L_i` summand when it is `EMPTY`.

Equivalently, after the first positive coordinate has appeared, the left scan
is the scalar recursion
[
M_i=F(C_i+M_{i-1}).
]
The right scan is the same recurrence in reverse. Every rooted score is
[
S_i=C_i+L_i+R_i,
]
again omitting an `EMPTY` summand. Hence stackability on the path is exactly
`max_i S_i > 0`.

`tests/test_path_score.py` exhaustively compares these path-specific messages,
scores, and decisions with the general tree evaluator for all weak
compositions with `n<=8,t<=8`, and compares the pruned decision through
`n<=9,t<=10`.

## Low-phase deficit identity

Suppose an active incoming message is the integer `m`, the current occupancy is
`c`, and `c+m<=1`. This is the low branch of the TreeStack transfer, so
[
m'=2(c+m)-3.
]
Set `Z=3-m`. Then
[
Z'=3-m'=2(Z-c). 	ag{1}
]
Thus while the process remains in the low phase, uncompensated deficit doubles
at every step.

For a block `c_1,...,c_k` that remains wholly in the low phase, iterating (1)
gives
[
Z_k=2^k Z_0-sum_{j=1}^k 2^{k-j+1}c_j. 	ag{2}
]
A bad interval is therefore weighted and adaptive; it is not determined by
the count of zeros alone.

## A message never exceeds branch mass

**Lemma.** If a nonempty path branch has total mass `M` and TreeStack message
`d`, then `d<=M`.

**Proof.** The transfer map satisfies `F(x)<=x` for every integer `x`. For a
one-vertex branch, `d=F(C)<=C=M`. Inductively, if the child branch has message
`d_child` and mass `M_child`, then
[
d=F(C+d_{child})le C+d_{child}le C+M_{child}=M.
]
Messages can nevertheless be arbitrarily negative.

## Irreversible deficit front

Consider a cut after vertex `i`. Let `m_i` be the active message sent by the
prefix `0,...,i` into `i+1`, and let
[
R_i=sum_{j=i+1}^{n-1}C_j
]
be all mass still to the right.

**Lemma (right exclusion).** If
[
m_i+R_ile0, 	ag{3}
]
then no vertex `j>i` can be a stacking target.

**Proof.** At the next vertex, with occupancy `c<=R_i`, the effective value is
`m_i+c<=m_i+R_i<=0`, so the transfer is in the low phase. Put
`m'=2(m_i+c)-3` and `R'=R_i-c`. Then
[
m'+R'=(m_i+R_i)+(m_i+c)-3<0.
]
Thus (3) propagates strictly through every subsequent vertex. At any proposed
root to the right, the message from the opposite branch is at most that
branch's total mass by the previous lemma, so the rooted score is at most the
left incoming message plus all mass still to its right, hence is nonpositive.
The left-exclusion statement is symmetric.

**Corollary.** If left-to-right and right-to-left irreversible exclusion
regions cover the whole path, the configuration is nonstackable.

The converse is false. For example, `(1,0,2)` on `P_3` is nonstackable but
the two front regions leave the middle root uncovered; its rooted score is
exactly zero.

## Exact front-pruned evaluator

The exclusion lemma gives an exact optimized decision procedure: scan from
each end only until its first irreversible front, then evaluate exact rooted
scores only in the central interval not excluded by either front. After a
front, raw negative messages can grow exponentially in bit length but cannot
change the decision. The implementation
`path_structurally_stackable_pruned` therefore avoids enormous integers
without approximating stackability.

## What the targeted experiments rule out

Simple longest-run hypotheses are too crude. At fixed `(n,t)=(3,3)`,
`(2,1,0)` is stackable while `(2,0,1)` is nonstackable, although both have
longest zero run 1 and longest run with occupancy at most one of length 2.

In the 600-trial focused run at `n=10000` and
[
t=operatorname{round}(n(log_2 n-0.75log_2log_2 n))=104887,
]
the success estimate is `308/600=0.5133`. Mean longest zero run is 3.399
among successes and 3.538 among failures; mean longest run with `C_i<=1` is
4.724 versus 5.055. By contrast, overlapping irreversible deficit fronts
certify `178/292=0.6096` of failures. The data favor an adaptive weighted
deficit excursion over a single unweighted sparse-run statistic.

## Scale discrimination and current working hypothesis

A first correction test used
[
t=n(log_2 n-clog_2log_2 n).
]
For `c=0.75`, success estimates were 0.490, 0.520, 0.535, and 0.427 at
`n=640,2560,10000,40000`; at `n=160000` the lower-trial estimate was 0.275.
This is better aligned than a fixed coefficient of `n log n` over the first
four sizes but still drifts.

The deficit recurrence suggests another mechanism. Very heuristically, a
one-sided message collapse across `k` successive scales can have cost like
[
2^{-1}2^{-2}cdots2^{-k}=2^{-k(k+1)/2},
]
where `k` is of order `log_2 mu` and `mu=t/n`. If global failure requires
two opposing excursions, the local two-sided cost is then of rough order
`2^{-k^2}`. Balancing `n2^{-k^2}` at order one gives
[
kasympsqrt{log_2 n},qquad
muasymp2^{sqrt{log_2 n}}. 	ag{heuristic}
]
This derivation is schematic: the actual message chain is not a sequence of
independent dyadic tests, the conditioned composition model is not product
measure, and front overlap does not capture every failure.

Nevertheless, at
[
t=a n 2^{sqrt{log_2 n}},
]
`a=0.84` gives success estimates 0.560, 0.480, 0.540, 0.573, and 0.450 for
`n=640,2560,10000,40000,160000`, respectively. The last point uses 40 trials;
the first three use 200 and `n=40000` uses 150. Multipliers 0.75 and 0.95
remain on the lower and upper sides of the transition over the same range.

This is the strongest current **working scale hypothesis**, but it is not
promoted to a formal conjecture. The one-sided rare-excursion probability, the
need for two-sided interaction, and transfer through conditioning still need
proof.

## Product geometric representation

If `X_1,...,X_n` are independent geometric variables with
[
Pr[X_i=k]=p(1-p)^k,
]
then every vector of total mass `t` has the same product probability
`p^n(1-p)^t`. Consequently, conditioning on `sum X_i=t` is exactly uniform
over weak compositions of `t`. Choosing `p=1/(1+mu)` gives unconditioned
mean `mu`.

Under this product surrogate the path message recursion is a scalar Markov
chain. The next analytic target is to estimate the probability of a one-sided
multiscale deficit excursion to an irreversible front, then understand how two
opposing excursions create global failure, and finally transfer those estimates
through conditioning on the total mass.


## Session 3: product-law finite-block deep-deficit rate

The product-geometric analysis now uses a finite-block local event rather than
an infinite-horizon phrase such as “eventual collapse.” For fixed `mu`, an
eventual-hitting probability is not the right local hazard: rare attempts can
recur indefinitely. The quantity studied here has a meaningful large-`mu`
logarithmic rate.

Let `X_1,X_2,...` be iid geometric variables with integer mean `mu`,

`P[X=k]=p(1-p)^k`, `p=1/(1+mu)`,

and let `M_j=F(M_{j-1}+X_j)`. Put `L=ceil(log_2 mu)`. For an integer starting
message `m in [mu,2mu]`, define

`q_mu(m)=P_m[min_{1<=j<=4L} M_j <= -mu]`.

The threshold is tied to the ambient occupancy scale: it asks for a negative
message whose magnitude is comparable with the mean occupancy. It is not a
threshold selected from the Monte Carlo data.

### Exact dyadic budget in the low phase

For `Z_j=3-M_j`, while every update remains in the low phase,

`Z_j=2(Z_{j-1}-X_j)`.

Writing `W_j=Z_j/2^j` gives the exact identity

`W_j=Z_0-sum_{r=1}^j 2^(1-r) X_r`.

Moreover the `j`-th update is in the low phase exactly when

`W_j >= 2^(2-j)`.

Thus a low-phase deficit excursion is exactly a nested dyadic-budget event,
not merely an interval with many small occupancies.

### Positive-phase affine companion

For every integer `y>=2`,

`2F(y)=y-3*1_{y odd}`.

Couple the message with the affine recursion

`Y_j=(Y_{j-1}+X_j)/2`, `Y_0=M_0`.

As long as the message before each update is at least `2`, induction gives

`0 <= Y_j-M_j < 3`.

The affine recursion has the stationary perpetuity

`Y=sum_{r>=1}2^{-r}X_r`,

with `E[Y]=mu` and `Var(Y)=mu(mu+1)/3`. This does not supply a stationary law
for the TreeStack message chain, but it identifies the natural positive-phase
scale and controls the nonlinear/parity correction before the low phase.

### Finite-block deep-deficit theorem

**Theorem.** Uniformly for integer starting messages `m in [mu,2mu]`, as
`mu -> infinity`,

`2^{-L^2-O(L log L)} <= q_mu(m) <= 2^{-L^2+O(L)}`.

Consequently

`-log_2 q_mu(m)/(log_2 mu)^2 -> 1`.

This proves the quadratic logarithmic cost, including the leading constant
`1`, for this precisely defined one-sided local event.

For the upper bound, let `sigma` be the first time `M_sigma<=1`. Before
`sigma`, messages are at least `2`. At the entry step the effective value can
only be `2,3,5`, so `M_sigma` is `0` or `1`. Working backwards, an output
`d>=2` has an effective preimage at most `2d+3`. Therefore the last
`L-O(1)` occupancies before `sigma` satisfy deterministic caps of dyadic size
`O(1),O(2),O(4),...,O(mu)`. Since, for `0<=a<=mu`,

`P[X<=a] <= (a+1)/(mu+1)`,

the cost of entering `{0,1}` in an `O(L)` window is
`2^{-L^2/2+O(L)}`.

Now take the last nonnegative message before a hit of `-mu`. It is necessarily
`0` or `1`, and every later update in that final run is low-phase. Starting
from deficit at most `3`, after `r` such updates the deficit is at most
`3*2^r`; hence a hit of order `mu` needs `L-O(1)` updates. Necessarily the
occupancies in the first `L-O(1)` of them obey

`X_r <= 3*2^(r-1)-2`.

Their geometric-CDF product contributes a second
`2^{-L^2/2+O(L)}` factor. There are only `O(L^2)` choices of the entry and
final-run locations inside the `4L` horizon, which proves the upper bound.

For the lower bound, use an explicit deterministic-cap witness. During the
first `N=L+4` steps impose

`X_j <= floor(mu/(L*2^j))`.

The global inequality `F(x)<=x/2` gives

`M_N <= M_0/2^N + sum_{j=1}^N X_j/2^(N-j+1) < 1`

for `M_0<=2mu`; since `M_N` is an integer, `M_N<=0`. Starting from the
certified deficit lower bound `z=3`, then impose recursively

`X_j <= floor(z/L)`,
`z <- 2(z-floor(z/L))`,

until `z>=mu+3`. This block stays in the low phase and has `O(L)` steps, so it
forces `M<=-mu`. For `0<=a<=mu`, an absolute `c>0` gives

`P[X<=a] >= c (a+1)/mu`.

Summing the logarithmic costs of the two cap blocks gives
`-L^2/2-O(L log L)` for each half and proves the lower bound.

The logarithmically optimal structure is therefore two-stage and multiscale:
a positive-scale descent followed by low-phase deficit amplification. Both
use roughly dyadic scales. The proof does not identify a unique most likely
coordinate sequence; many capped sequences have the same leading-order cost,
and the `1/L` slack in the lower witness is not claimed optimal at lower order.

### The full product message chain has no stationary probability law

The full integer-valued message chain should not be initialized from a claimed
stationary distribution. From any finite state, a sufficiently long finite
run of zero occupancies has positive probability and reaches an arbitrarily
deep negative state. Once `Z=3-M` is a sufficiently large multiple of
`mu+1`, require forever that `X_j<=Z_{j-1}/4`. On that event
`Z_j>=(3/2)Z_{j-1}`. The conditional failure probabilities are bounded by a
summable sequence of the form `exp(-c(3/2)^j)`, so this runaway event has
positive probability.

Thus every starting state has positive probability of `M_j -> -infinity`.
If a stationary probability law existed, averaging those positive escape
probabilities would give an escape event of positive stationary probability.
For every fixed `A`, the event would eventually imply `M_j<-A`, forcing the
stationary left tail below `-A` to be bounded away from zero uniformly in `A`,
contradicting tightness of a probability distribution on the integers.

The appropriate positive-phase objects are therefore the affine companion, or
possibly a killed/quasi-stationary chain, not a stationary law for `M`.

### Exact local equivalence of ensembles

Let the fixed-total model have `n` coordinates and total `t`, and compare it
with iid geometrics having `p=n/(n+t)`, hence mean `t/n`. For a fixed local
`k`-vector of total mass `s`, the exact likelihood ratio is

`R_{n,t,k}(s) = [(n-1)_k (t)_s/(n+t-1)_{k+s}] /
                [(n/(n+t))^k (t/(n+t))^s]`.

Equivalently,

`R = prod_{i=1}^k(1-i/n)
     prod_{j=0}^{s-1}(1-j/t)
     prod_{l=1}^{k+s}(1-l/(n+t))^{-1}`.

If `k<=n/2`, `s<=t/2`, and `k+s<=(n+t)/2`, then the elementary estimate
`|log(1-x)|<=2x` yields

`|log R| <= k(k+1)/n + s(s-1)/t
           + (k+s)(k+s+1)/(n+t)`.

Therefore any local event supported on block mass at most `S` has conditioned
and product probabilities within the exponential of the same bound with
`s=S`.

For the canonical deep-deficit witness, `k=O(L)` and the sum of its caps is
`S=O(mu/L)`. Hence its conditioned/product ratio tends to one whenever

`L^2/n + mu/(nL^2) -> 0`.

In particular this covers `mu=2^{c sqrt(log_2 n)}` for every fixed `c`. The
local lower-bound obstruction therefore transfers rigorously to the uniform
weak-composition model at stretched-log densities. This does not yet transfer
the complete global nonstackability event.

### Revised global interpretation

The one-sided theorem changes the Session 2 heuristic mechanism. A complete
order-`mu` one-sided catastrophe costs

`q_mu = 2^{-(1+o(1))L^2}`,

not `2^{-L^2/2}`: positive descent and negative amplification each contribute
half of the exponent.

The stretched-log scale nevertheless remains structurally plausible through a
spatial-hazard mechanism. A directional scan of length `n` has order `n`
possible locations for a one-sided rare seed. If a renewal/block argument can
show that the effective directional hazard is of order `q_mu`, the natural
balance is

`n q_mu ~ 1`,

which gives

`L~sqrt(log_2 n)`, `mu~2^{sqrt(log_2 n)}`.

This is not yet a theorem or promoted global conjecture. The needed renewal or
block comparison has not been proved, left/right front events have not been
shown independent, and irreversible-front overlap remains sufficient rather
than necessary for nonstackability.


## Session 4: spatial reset, true-front conversion, and a global subcritical theorem

Session 4 turns the Session 3 canonical deep-deficit witness into a spatial
certificate. This section concerns a **sufficient certified front event**; it
does not identify the complete law of all irreversible fronts.

### Global half-contraction and reset block

The exact transfer satisfies

`F(x) <= x/2`

for every integer `x`. Hence, after a block of length `r` with occupancies
`X_1,...,X_r`, any active incoming integer message `m` obeys

`M_r <= m/2^r + sum_{j=1}^r 2^{-(r-j+1)} X_j`.

An EMPTY branch is handled separately by requiring the first coordinate of the
reset block to be positive; after activation the same upper bound is valid with
initial contribution zero.

On a path of length `n` with total mass at most `2 n mu`, the
message-versus-mass lemma gives every incoming message the upper bound
`2 n mu`. Put

`r = ceil(log_2(4n))`.

Define the reset event by `X_1>0` and

`sum_{j=1}^r 2^{-(r-j+1)} X_j <= 3 mu/2`.

Then every incoming state, including EMPTY, exits the reset block with message
at most `2 mu`. Under iid geometric coordinates of mean `mu`, Markov's
inequality and a union bound give

`P(reset) >= 1/3 - 1/(mu+1)`.

Thus the spatial argument does not need a stationary law or a proof that the
uncontrolled scan frequently lands specifically in `[mu,2mu]`: a
constant-probability local reset forces the required upper starting control.

### Constant-cost conversion of a deep seed into a true front

Suppose the canonical Session 3 witness has ended with `M<=-mu`, so the
low-phase deficit `Z=3-M` satisfies `Z>=mu+3`. If `D` is a deterministic
lower bound on `Z` and the next occupancy obeys

`X <= floor(D/4)`,

then the update stays in the low phase and

`Z' = 2(Z-X) >= 3D/2`.

Iterate this until the certified deficit is at least `2 n mu+3`. This takes
`O(log n)` steps. The probability of the entire buffer is bounded below
uniformly in `mu` and `n` by the positive infinite product

`c_* = prod_{j>=0} (1-exp(-(3/2)^j/4))`.

The explicit rigorous truncation implemented in
`universal_runaway_probability_lower_bound` gives

`c_* > 0.0095991`.

Consequently converting the canonical `-mu` seed into a deficit large enough
to dominate the entire path costs only a constant factor, not another
quadratic logarithmic exponent.

### Certified one-sided spatial-front theorem

A superblock consists of:

1. the reset block above;
2. the canonical Session 3 deep-deficit witness;
3. the runaway buffer above.

Let `w_mu` be the exact product probability of the canonical witness and let
`p_{mu,n}` be the certified superblock probability lower bound. Then

`p_{mu,n} >= (1/3-1/(mu+1)) c_* w_mu`,

and therefore, for `L=ceil(log_2 mu)`,

`log_2 p_{mu,n} = -L^2 - O(L log L)`.

The superblock length is

`b_{mu,n}=O(log n + L)`.

Disjoint superblocks are independent under the product law. On the event that
the total path mass is at most `2 n mu`, every successful superblock forces a
genuine irreversible left-to-right front. Hence, with
`B=floor(n/b_{mu,n})`,

`P_product[no certified front]
 <= (1-p_{mu,n})^B + P[total mass > 2 n mu]`.

The last term has an exponential Chernoff bound. Thus the **certified true
front** retains the Session 3 leading exponent `1`. This is a lower bound on
the occurrence rate of true fronts, not a matching upper bound for the event
that any true front occurs.

### Conditioning and a rigorous global nonstackability regime

For fixed total `t=n mu`, split the path into two halves. Use disjoint
left-to-right certified superblocks in the left half and the reversed
right-to-left construction in the right half. Under the product law the two
families use disjoint coordinates. After conditioning on total mass `n mu`,
the reserve bound required by either certificate is automatic.

If `B` is the number of superblocks in one half, then

`P_conditioned[missing at least one half-certificate]
 <= 2 (1-p_{mu,n})^B / P_product[sum X_i=n mu]`.

The negative-binomial point probability in the denominator is of order
`1/(mu sqrt(n))`; the code uses cancellation-free Robbins/Stirling bounds
rather than subtracting enormous `lgamma` values.

Therefore, whenever

`log_2 n - L^2 - O(L log L) -> +infinity`,

both opposing certified fronts occur with conditioned probability tending to
one, and their exclusion regions cover the path. In particular:

**Theorem (global subcritical stretched-log bound).** If `mu=mu_n` is an
integer sequence satisfying

`log_2 mu = (c+o(1)) sqrt(log_2 n)`

for a fixed `c<1`, and `t=n mu`, then a uniformly random weak composition
of `t` on `P_n` is nonstackable with probability tending to one.

This is the first rigorous global stretched-log result in ProbStack. It is
one-sided: no theorem yet proves stackability for `c>1`.

As direct corollaries of the same certificate criterion, densities
`mu=Theta(log n)` and more generally
`mu=exp(O((log n)^alpha))` with `alpha<1/2` are still nonstackable with
probability tending to one. No monotonicity in total mass is used for these
claims.

### Small failures missed by front overlap

Exact enumeration through `n<=10,t<=8` found 20,429 nonstackable
configurations missed by the existing front-overlap certificate. Every one of
these missed cases still had both one-sided irreversible fronts; the fronts
simply left a central uncovered gap. Of the missed cases, 5,579 had maximum
root score exactly zero and 14,850 had maximum root score strictly negative.
Thus an equality-only explanation is false.

The largest uncovered gap in this rectangle is 4. The observed maximum grows
from 1 to 4 across the small grid, so no universal bounded-gap claim is made.

### Seed-to-front diagnostic

A seeded product-law diagnostic started exactly from `M_0=-mu` and asked
whether the process reached deficit `2 n mu+3`, with
`n=2^{ceil(log_2 mu)^2}`, before ever leaving the low phase. With 20,000
trials per mean, the estimates were 0.2634, 0.2159, 0.19845, and 0.18615 for
`mu=16,32,64,128`, respectively. The Wilson intervals are recorded in
`data/seed_to_front_mc.csv`.

These values are far above the universal rigorous lower constant
`0.0095991`, supporting the interpretation that seed-to-front conversion is
order one. They are not used in the proof.

### What remains open

The exponent `1` is proved for the certified front witness, but not as a
matching logarithmic rate for **all** irreversible fronts. More importantly,
nonstackability is not yet shown to require one of these deep local witnesses.
Therefore Session 4 does not prove the supercritical statement for `c>1`,
does not prove a full threshold, and does not determine a critical window.


## Session 5: deep-message necessity and the supercritical theorem

Session 5 closes the leading-order structural gap left by Session 4. The key
new fact is that nonstackability itself forces a genuinely deep one-sided
message. No front-overlap converse is needed.

### Exact dissipation identity

Use zero only as the arithmetic contribution of an EMPTY branch inside a
score; EMPTY remains a distinct categorical message. Let

A_i = sum_{j<i} C_j,    B_i = sum_{j>i} C_j,

and let ell_i and r_i be the numerical contributions of the left and right
incoming messages at root i. Define

D_i^L = A_i - ell_i,    D_i^R = B_i - r_i.

Then exactly

S_i = t - D_i^L - D_i^R.                                           (4)

For an active left transfer with effective value x=C_i+ell_i, prefix
dissipation increments by

D_{i+1}^L - D_i^L = x - F(x).                                      (5)

If the prefix through i is still empty, the increment is zero.

### Sharp one-step dissipation bound

Lemma. Let h>=2. If x<=h-1 and F(x)>=1-h, then

x - F(x) <= floor(h/2)+1.                                           (6)

For x<=1, the low branch F(x)=2x-3 and F(x)>=1-h imply
x>=ceil((4-h)/2), which gives (6). For x>=2, the exact parity formulas for F
give the same inequality directly from x<=h-1.

### Deep-message necessity theorem

Theorem. Let C be a positive-mass configuration of total t on P_n. If C is
nonstackable and h>=2 satisfies

t > (n-1)(floor(h/2)+1),                                            (7)

then at least one directed TreeStack message is at most -h.

Proof. Suppose instead that every nonempty directed message is at least 1-h.
At any vertex i<n-1, nonstackability gives C_i+ell_i+r_i<=0. The opposite
incoming contribution is either zero (EMPTY) or at least 1-h, so the active
left effective value x=C_i+ell_i is at most h-1. The outgoing message is also
at least 1-h. By (6), every active prefix dissipation increment is at most
floor(h/2)+1, while inactive empty-prefix steps contribute zero. Hence

D_{n-1}^L <= (n-1)(floor(h/2)+1) < t.

But the last rooted score is S_{n-1}=t-D_{n-1}^L, contradicting
nonstackability. For h=1, if all directed messages were nonnegative then every
occupied root would have positive score, so a positive-mass nonstackable
configuration must contain a negative message.

The largest threshold obtained directly from (7) is

h_*(n,t) = max(1, 2 floor((t-1)/(n-1)) - 1).

In particular, for integer mean t=n mu,

nonstackable  ==>  some directed message <= -(2 mu - 1).            (8)

This is stronger than the order-mu necessity originally targeted for
Session 5.

### Local cap cover for a deep message

Work under iid geometric occupancies of integer mean mu and put
L=ceil(log_2 mu). A directional scan starts from EMPTY.

For an interior descent from a state at least mu to its first state at most 1,
backward TreeStack preimages force L-O(1) occupancies to obey the cap sequence

5, 13, 29, ...

when read backwards from the entry. Let a_mu be the product probability of
these entry caps. The Session 3 small-deviation estimate gives

log_2 a_mu = -L^2/2 + O(L).                                        (9)

For the final uninterrupted low-phase run to a message at most -(2 mu - 1),
the last nonnegative state is 0 or 1; the only boundary exception starts from
-1. In all cases the initial deficit is at most 4. Therefore the first
L-O(1) occupancies of the final run obey

X_j <= 4*2^(j-1)-2.

Let b_mu be this cap probability. Then

log_2 b_mu = -L^2/2 + O(L).                                       (10)

A state M>-(2 mu-1) is sent to M'>=mu whenever X>=4 mu+1. Thus, while
a scan has neither returned to height mu nor hit the deep threshold, every
intervening coordinate must satisfy X<=4 mu. Put c_mu=P[X<=4 mu] and choose
the least R with c_mu^R<=b_mu. Since P[X>=4 mu+1] is bounded below by an
absolute positive constant and b_mu=2^{-O(L^2)},

R = O(L^2).                                                        (11)

Every deep-message occurrence is therefore covered as follows.

- A boundary-origin witness has one of R+1 cap patterns, each of product
  probability at most b_mu.
- An interior witness has an entry block, at most R middle coordinates capped
  by 4 mu, and a final low-run block, or else an entry block followed by R
  middle caps. There are at most R+2 such patterns per possible entry
  location, each of product probability at most a_mu b_mu.

Consequently, for a one-direction scan with N transfers,

P_prod[some message <= -(2 mu-1)]
 <= (R+1)b_mu + N(R+2)a_mu b_mu.                                  (12)

The boundary contribution has exponent 1/2 but only O(L^2) opportunities. The
spatial interior contribution satisfies

a_mu b_mu = 2^{-L^2+O(L)}.                                        (13)

### Conditioning without the global point-probability loss

Every cap pattern in (12) is supported on O(L^2) consecutive coordinates and
has total capped block mass O(mu L^2). The exact Session 3 local
likelihood-ratio bound therefore gives, uniformly over all these witness
events,

P_cond(E) <= exp(Delta_n) P_prod(E),

where

Delta_n = O(L^4/n + mu L^4/n) = o(1)

throughout the stretched-log regime. This avoids dividing by
P(sum X_i=n mu), and hence avoids the square-root-n loss that a global
conditioning inequality would introduce.

Combining (8), the two scan directions, and the local cap cover gives

P_cond[nonstackable]
 <= 2 exp(o(1)) ((R+1)b_mu + n(R+2)a_mu b_mu).                     (14)

### Global supercritical theorem

Theorem. Let mu=mu_n be integer, t=n mu, and

log_2 mu = (c+o(1)) sqrt(log_2 n)

for a fixed c>1. Then a uniformly random weak composition of total t on P_n
is stackable with probability tending to one.

The boundary term in (14) tends to zero, while the interior term has

log_2(n poly(L) a_mu b_mu)
 = (1-c^2+o(1)) log_2 n -> -infinity.

Together with the Session 4 theorem for every fixed c<1, this proves the
leading stretched-log separation coefficient 1. It does not prove a critical
window at c=1, a finite-n monotonicity statement in total mass, or a
second-order threshold correction.

## Session 6: second-order dyadic-simplex asymptotics

Session 6 replaces the coordinatewise cap approximation by the exact geometry
of a dyadic weighted simplex. For

E_{k,B}={x>=0: sum_{j=1}^k 2^{j-1}x_j<=B},

unit-cube comparison gives

B^k/(k! 2^{k(k-1)/2})
<= |E_{k,B}|
<= (B+2^k-1)^k/(k! 2^{k(k-1)/2}).

For iid geometric occupancies of mean mu, whenever
k=L+O(1), B=Theta(mu), and L=ceil(log_2 mu), this yields

log_2 P(E_{k,B})
=
-L^2/2-L log_2 L+O(L).

The same estimate holds for reversed dyadic weights.

Applying this to a positive descent simplex and then to the exact low-phase
deficit budget gives a new lower witness for the Session 3 finite-block
probability q_mu(m). Conversely, every hit within 4L steps contains a
necessary positive-entry simplex and a disjoint necessary final-low-run
simplex. Hence, uniformly for integer m in [mu,2mu],

-log_2 q_mu(m)
=
L^2+2L log_2 L+O(L).

Thus the coefficient of L log_2 L is proved to be 2. The former
O(L log L) lower/upper mismatch is closed at this order; the coefficient of
the remaining linear term is not determined.

The same two necessary simplices sharpen the Session 5 first-deep-message
cover at threshold -(2mu-1). Its interior probability is

2^{-L^2-2L log_2 L+O(L)},

while the physical-boundary term has half this exponent and no spatial n
factor. The middle cluster remains O(L^2).

Combining the sharpened local bounds with local equivalence of ensembles and
a conditioned second-moment argument for disjoint spatial certificates gives
the following second-order centering. Write N=log_2 n and

a_n=sqrt(N)-log_2 sqrt(N)
   =sqrt(log_2 n)-(1/2)log_2 log_2 n.

For L_n=ceil(log_2 mu_n), integer mu_n, and total t=n mu_n:

- if L_n-a_n -> -infinity, nonstackability holds with probability tending to 1;
- if L_n-a_n -> +infinity, stackability holds with probability tending to 1.

The bounded-offset regime L_n-a_n=O(1) remains open. In particular Session 6
does not determine a limiting critical-window law, a beta coefficient in a
linear-in-L refinement, or finite-n monotonicity in total mass.

Full derivation and validation details are in notes/session-6-second-order.md.

## Session 7: exact linear rare-excursion term

The one-sided finite-block probability now has a full linear
asymptotic.  For `L=ceil(log_2 mu)`,
`theta=mu/2^L`, and `m in [mu,2mu]`,

`-log_2 q_mu(m)
 = L^2+2L log_2 L
   +[2 log_2 theta-2 log_2(3e)]L+o(L)`.

The positive phase admits an exact reverse-slack representation.  If the
terminal state is `a in {0,1}`, each reverse slack `y` has multiplicity
one for `y=0,1,2` and two for `y>=3`.  Its generating factor is
`(1+z^3)/(1-z)`, and across dyadic weights the numerator telescopes.
Combined with binary-partition asymptotics, this shows that parity contributes
no additional unknown linear constant.

In the natural variable `x=log_2 mu` the dyadic phase cancels:

`-log_2 q_mu(m)
 = x^2+2x log_2 x-2 log_2(3e)x+o(x)`.

The global translation is not yet a single center: the refined upper cover and
the best current state-independent lower certificate leave an explicit
`0.5 log_2 3` gap in `log_2 mu`.  See
`notes/session-7-linear-order.md` for the proof and validation details.


## Session 8/17/18 supersession — final path theorem

The Session 7 bounded spatial gap displayed immediately above is historical.
Session 8 introduced the exact one-coordinate regeneration

`-mu < M <= 2mu,quad 2mu+2-M <= X <= 4mu-M`,

which sends the next message into `[mu,2mu]` at constant probability. Session
17 then stabilised the one-sided local rate, uniformly over dyadic phase and
starting messages, as

`-log_2 q_mu(m) = x^2 + 2x log_2 x - 2log_2(3e)x + o(x)`.

Session 18 transferred the resulting product-law argument to the fixed-total
weak-composition model without conditioned independence and completed both
global directions. The final frozen center is

`sqrt(log_2 n) - 0.5 log_2 log_2 n + log_2(3e)`,

with fixed nonzero offsets only.
