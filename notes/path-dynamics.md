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
