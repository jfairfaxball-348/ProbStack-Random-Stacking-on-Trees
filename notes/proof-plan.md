# Proof plan — stage 1

The current goal is not to formalize an unproved guess.  It is to turn the path
score theorem into a tractable probabilistic event and identify the correct
asymptotic statement.

## Deterministic reduction on a path

For vertices `1,...,n`, define one-sided messages by the TreeStack recurrence.
The first task is to derive equivalent descriptions of a message in terms of
local deficits/surpluses or a transformed partial-sum process.  Useful targets
include:

- an explicit formula or monotone envelope for the iterates of `F`;
- a characterization of when a one-sided message is very negative;
- a decomposition of `max_r S_r` into extreme one-sided obstructions;
- a finite-state / transfer-matrix representation after suitable truncation;
- exact dynamic programming for path counts that extends beyond brute-force
  weak-composition enumeration.

## Probabilistic reduction

Use the exact identity

\[
(C_1,\ldots,C_n)\stackrel d=(X_1,\ldots,X_n)\mid\sum X_i=t,
\]

where the `X_i` are i.i.d. geometric.  Product-measure arguments can first be
proved for the `X_i`, but deconditioning back to fixed total must be justified;
independence must never be silently assumed under `D_{P_n,t}`.

Potential tools include generating functions, local limit estimates for the
conditioning event, Poissonisation/de-Poissonisation, first/second moments for
extreme bad blocks, and concentration only after the correct statistic is
identified.

## Current scale question

Experiments make `n log n` a serious working hypothesis for the recovery order,
but not yet a theorem or stable conjecture.  A proof programme should seek
matching lower and upper mechanisms rather than fit a constant first.  In
particular, determine which rare path patterns force all rooted scores to be
nonpositive, and which density prevents such patterns with high probability.

Any eventual theorem statement must explicitly exclude or otherwise account
for the trivial `t=1` regime and must not infer monotonicity that has not been
proved.


## Session 2 proof progress

The deterministic path reduction is now substantially sharper.

1. Exact one-sided messages are scalar recurrences `M_i=F(C_i+M_{i-1})`
   after the first occupied vertex.
2. In the low phase `C_i+M_{i-1}<=1`, the transformed deficit
   `Z=3-M` satisfies `Z_i=2(Z_{i-1}-C_i)`, with an exact dyadically weighted
   closed form over any block that stays in this phase.
3. Every nonempty branch message is at most its branch mass.
4. If a prefix message plus all remaining mass is nonpositive, every target to
   its right is impossible; symmetrically from the other side.  This gives a
   rigorous sufficient nonstackability certificate and an exact front-pruned
   evaluator.

The next proof target is no longer a generic interval bound.  Work under the
i.i.d. geometric product law with mean `mu` and estimate the probability
`q(mu)` that a one-sided scalar message chain undergoes a multiscale descent
from its typical positive scale to an irreversible negative deficit.  The
recurrence suggests a sequence of progressively rarer replenishment failures,
with a heuristic logarithmic cost quadratic in `log mu`.

After obtaining upper and lower bounds on `q(mu)`, determine whether global
failure genuinely requires two suitably independent/opposed excursions.  A
relation of the form
[
Pr(\text{local two-sided obstruction}) \approx q(\mu)^2
]
would naturally lead to the observed stretched-log candidate scale when
balanced over `n` possible locations.  Only after this product-law step should
conditioning on `sum X_i=t` be handled, via a local-limit or
de-Poissonisation argument that preserves the rare-event scale.


## Session 3 proof progress

The one-sided product-law problem now has a rigorous logarithmic-rate answer.
For integer mean `mu`, `L=ceil(log_2 mu)`, and initial message
`m in [mu,2mu]`, define

`q_mu(m)=P_m[min_{1<=j<=4L} M_j <= -mu]`.

The proved bounds are

`2^{-L^2-O(L log L)} <= q_mu(m) <= 2^{-L^2+O(L)}`,

uniformly in that starting window. Thus
`-log_2 q_mu(m)~(log_2 mu)^2`. The proof decomposes the excursion into a
positive-phase descent to `{0,1}` and a low-phase amplification from deficit
`O(1)` to deficit `Theta(mu)`. Each phase contributes half of the quadratic
logarithmic cost.

Three exact reductions now accompany this estimate:

- in the low phase, `W_j=Z_j/2^j` is a dyadic weighted budget with an exact
  nested inequality for remaining low-phase;
- before the low phase, `2F(y)=y-3*1_{y odd}` couples the message within an
  additive constant of `Y_j=(Y_{j-1}+X_j)/2`;
- for a fixed local block under the conditioned composition model, the exact
  conditioned/product likelihood ratio depends only on the block mass and is
  uniformly `1+o(1)` for the canonical witness at every stretched-log density.

The full product message chain has no stationary probability distribution:
from every state there is positive probability of runaway to `-infinity`.
Accordingly, future starting-state work should use a killed/quasi-stationary
positive phase or regeneration description rather than assume a stationary
message law.

The leading remaining proof target is global. Prove a renewal/block theorem
that turns the finite-block hazard `q_mu` into the probability and spatial
location of an irreversible one-sided front over a path of length `n`, with
matching bounds up to `2^{o(L^2)}` factors. Then combine the two directions
without assuming independence and quantify the failures not captured by front
overlap. The exact local equivalence-of-ensembles bound can then transfer the
result to fixed total.


## Session 4 proof progress

The Session 3 local witness now has a rigorous spatial implementation.

The key deterministic/probabilistic chain is:

1. `F(x)<=x/2` globally.
2. On total mass at most `2nmu`, an `O(log n)` reset block has probability
   bounded below by a positive constant and sends every incoming state to
   message at most `2mu`.
3. The canonical Session 3 cap witness then forces message at most `-mu`
   with probability `2^{-L^2-O(L log L)}`.
4. A further `O(log n)` low-phase buffer grows the deficit by factor at least
   `3/2` per step and has probability bounded below by the universal
   constant `c_*>0.0095991`.
5. The resulting deficit exceeds `2nmu`, so on the reserve event it is a
   genuine irreversible front.
6. Disjoint superblocks give `Theta(n/polylog n)` independent opportunities
   under the product law.
7. Conditioning on total `nmu` is handled globally by division by the exact
   negative-binomial point probability, not by pretending many local blocks
   remain independent after conditioning.
8. Putting one directional certificate in each half proves nonstackability
   with probability tending to one for
   `mu=2^{(c+o(1))sqrt(log_2 n)}` for every fixed `c<1`.

This gives a rigorous global **lower side** of the stretched-log recovery
picture. It does not prove that the actual front hazard is no larger than the
certified hazard, and it does not prove stackability for `c>1`.

### Highest-priority next proof target

Prove a structural necessity or near-necessity theorem for nonstackability.
A useful target is a “soft-front” statement saying that every nonstackable
configuration, except perhaps for a controlled exceptional event, contains a
local one-sided deep-deficit seed in one of `n polylog(n)` candidate windows.
Combined with the Session 3 upper bound
`q_mu<=2^{-L^2+O(L)}`, such a theorem could yield stackability for `c>1`
and close the leading coefficient.

The exact missed-front catalogue suggests looking first at the central gap
between the two irreversible fronts: every missed failure through
`n<=10,t<=8` has both fronts, but with an uncovered gap of length 1--4.
The correct refinement may be a finite-reserve or soft-front bridge rather than
a new rare-event mechanism.

Secondary targets are to sharpen the `O(L log L)` loss in the explicit lower
witness, characterize the unrestricted true-front hazard from above, and only
then study the critical `c=1` window.
