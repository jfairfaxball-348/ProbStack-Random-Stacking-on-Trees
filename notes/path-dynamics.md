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
