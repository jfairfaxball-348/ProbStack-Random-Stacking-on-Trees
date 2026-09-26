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
