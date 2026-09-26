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
