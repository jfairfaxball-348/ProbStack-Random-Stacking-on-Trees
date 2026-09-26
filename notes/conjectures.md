# Conjecture register

## Promotion rule

A conjecture is promoted here only after independent stackability checks agree,
exact enumeration covers a meaningful range, obvious competing scalings have
been tested, boundary cases are understood, and there is a plausible analytic
mechanism.  A plotted curve alone is not enough.

## Current status — no stable headline conjecture yet

The initial exact atlas and seeded Monte Carlo runs point toward a high-density
path recovery on a mixed scale near `n log n`, rather than at a fixed multiple
of `n`.  This is a **working scale hypothesis**, not yet promoted as the first
formal conjecture.

Evidence so far:

- the exact atlas `2 <= n <= 9`, `0 <= t <= 12` establishes the nonmonotone
  finite profile and a genuine recovery region;
- direct legal reachability and TreeStack scores agree on every labeled tree
  through order 5 and mass 5;
- for fixed `t/n` between roughly 2 and 10, sampled path recovery probabilities
  move downward as `n` grows from 20 to 160;
- sampling at `t = a n log_2 n` aligns the curves substantially better for
  `n=40,...,640`, and targeted checks through `n=2560` remain compatible with
  that order of growth;
- the path event has a one-dimensional message recursion, and the uniform
  weak-composition law is exactly an i.i.d. geometric vector conditioned on its
  sum, providing a plausible route to extreme-block analysis.

Reasons not to promote a formula yet:

- the apparent `1/2` crossing in units of `n log_2 n` still drifts with `n`;
- the present range cannot rule out logarithmic corrections such as
  `log log n`, nor identify a limiting constant or profile;
- no rigorous lower/upper comparison reducing stackability to a tractable
  extreme-value event has yet been proved;
- Monte Carlo uncertainty is non-negligible at the largest path orders.

Next promotion test: derive a deterministic path criterion in terms of a small
number of one-sided message/deficit statistics, then test `n log n` against
explicit log-corrected alternatives on larger seeded runs.  If that succeeds,
a precise growing-regime recovery conjecture can be entered with date and
commit.
