# Experiments

## Validation baseline

The code has two independent stackability checks: exhaustive legal-move search
and TreeStack score evaluation.  The command

```text
python scripts/validate_small.py --max-order 5 --max-total 5
```

checks every labeled tree of orders 1 through 5, every configuration of total
mass 0 through 5, and every possible target root.  Current result:

```text
validated 146 labeled trees, 33711 configurations, 166116 rooted cases; no disagreements
```

The test suite also includes a path of length 1500 to ensure the structural
message implementation is iterative and does not silently fail on Python's
recursion limit.

## Exact path atlas

A timing probe found that the rectangle through `n=10,t=12` costs about 17
seconds for `n=10` alone in the initial implementation, whereas `n=9` costs
about 7 seconds.  The committed baseline therefore uses the conservative
rectangle `2<=n<=9, 0<=t<=12`; larger exact runs are opt-in.

Selected exact values:

| path | t | stackable / total | probability |
|---|---:|---:|---:|
| `P_2` | 2 | 2 / 3 | 2/3 |
| `P_3` | 5 | 19 / 21 | 19/21 |
| `P_3` | 6 | 25 / 28 | 25/28 |
| `P_6` | 4 | 33 / 126 | 11/42 |
| `P_7` | 5 | 87 / 462 | 29/154 |
| `P_8` | 6 | 220 / 1716 | 5/39 |
| `P_9` | 6 | 260 / 3003 | 20/231 |
| `P_9` | 12 | 23539 / 125970 | 23539/125970 |

The exact finite profile has several important features.  The forced `t=1`
spike is followed by a trough and then recovery.  For `P_3`, the aggregate
probability is itself nonmonotone inside the higher-mass region:
`19/21` at mass 5 falls to `25/28` at mass 6, then reaches 1 at mass 7.  No
clear parity/congruence pattern is visible in this first rectangle.

The nontrivial minima within the atlas occur at masses 2,2,2,2,4,5,6,6 for
`P_2,...,P_9`, respectively.  For `P_8` and `P_9`, recovery above `1/2` lies
outside the committed `t<=12` rectangle.

## Large-path orientation

Monte Carlo is used only after the exact validation above and samples **uniform
weak compositions** by stars and bars.  Fixed linear density does not align the
recovery curves well: for example, at `t=4n` the 1000-trial estimates are `0.853` (`n=20`), `0.634` (`n=40`), `0.310` (`n=80`), and `0.094` (`n=160`).  At `t=5n` they are `0.945`, `0.862`, `0.657`, and `0.437`.  This systematic drift makes a fixed linear recovery scale implausible.

In contrast, the normalization `t=a n log_2 n` aligns the curves much better.
With 1000 trials per grid point for `n=40,...,640`, values near `a=0.75` remain
in the broad transition region; a separate 200-trial grid at `n=1280,2560` gives estimates `0.515` and `0.510` at `a=0.75`, again placing the transition in the same order of growth.  The
crossing drifts, so no limiting constant is claimed.

The committed comparison grid at `t=a n log_2 n` gives, for `a=0.75`, estimates `0.634, 0.600, 0.591, 0.560, 0.530` for `n=40,80,160,320,640`; at `a=0.85` the corresponding estimates are `0.774, 0.771, 0.761, 0.778, 0.786`.  This supports the *order* `n log n` far more clearly than it supports any limiting constant.

All committed numerical output is accompanied by sidecar metadata and an entry
in `data/experiment_log.jsonl`.  Sampling estimates should always be read with
finite-trial uncertainty in mind.


## Session 2: path deficit dynamics and scale discrimination

A path-specific evaluator now implements the exact left/right scalar message
recurrences and is exhaustively cross-checked against the general tree
evaluator.  A proved irreversible-deficit lemma permits exact early stopping:
if an active one-sided message plus all mass remaining beyond the cut is
nonpositive, every root beyond that cut has nonpositive score.  The resulting
front-pruned decision procedure agrees with the full path recurrence on every
weak composition through `n<=9,t<=10`.

The longest-zero-run mechanism was tested directly and is too crude.  At
`(n,t)=(3,3)`, configurations `(2,1,0)` and `(2,0,1)` have the same
longest zero run and the same longest run with occupancy at most one, but only
the first is stackable.  In a 600-trial run at `n=10000,t=104887`, mean
longest zero runs were 3.399 for successes and 3.538 for failures, whereas
overlapping irreversible deficit fronts certified 178 of 292 failures.

A correction grid at
`t=n(log2(n)-c log2(log2(n)))` improved alignment over a fixed coefficient of
`n log n` through `n=40000`, but the best apparent `c` moved by
`n=160000`.  More importantly, the exact deficit recurrence motivated a
competing stretched-log density
`mu=t/n = a*2^sqrt(log2(n))`.  At `a=0.84` the seeded estimates were
0.560, 0.480, 0.540, 0.573 and 0.450 for
`n=640,2560,10000,40000,160000`, respectively (40 trials at the last size,
150 at `n=40000`, 200 otherwise).  Multipliers 0.75 and 0.95 stayed on the
lower and upper sides of the transition over the same range.

This materially weakens the interpretation of the earlier `n log n`
alignment as asymptotic evidence.  The strongest current numerical signal is
the recurrence-motivated stretched-log scale, but it is not yet promoted to a
conjecture.  See `notes/path-dynamics.md` for the exact lemmas and heuristic.


## Session 3: product-law excursion and conditioning experiments

The Session 3 computations were designed only to test consequences of the
analytic finite-block event; no generic larger path grid was generated.

The product-law Monte Carlo command was

```text
python scripts/analyze_product_excursion.py --means 4,8,16 --trials 200000 --seed-base 2026092660 --output data/product_deep_excursion_mc.csv
```

For `q_mu=P_{M_0=mu}[min_{j<=4 ceil(log2 mu)} M_j<=-mu]`, the seeded estimates
were:

| `mu` | hits / trials | estimate | Wilson 95% interval | `-log2(qhat)/L^2` |
|---:|---:|---:|---:|---:|
| 4 | 28161 / 200000 | 0.140805 | [0.139288, 0.142336] | 0.7071 |
| 8 | 2031 / 200000 | 0.010155 | [0.009725, 0.010604] | 0.7357 |
| 16 | 22 / 200000 | 0.000110 | [0.0000726, 0.0001666] | 0.8219 |

The statistic was defined before running the experiment. Its purpose was to
check whether finite means move in the direction of the proved limiting
constant `1`, not to estimate that constant from a fit. The rare `mu=16` row
has only 22 hits and should be read with its interval.

The rigorous finite-parameter bounds were tabulated with

```text
python scripts/tabulate_product_excursion_bounds.py --levels 8,10,12,16,20,30,40 --output data/product_excursion_rigorous_bounds.csv
```

At `L=8,10,12,16,20,30,40`, the normalized cost of the explicit lower-bound
witness decreases from `2.048` to `1.348`, while the normalized cost associated
with the rigorous upper probability bound increases from `0.466` to `0.904`.
The bounds converge slowly but squeeze toward the analytic exponent `1` from
opposite sides; this table is a computation of proved formulas, not simulation.

The exact conditioned-versus-product comparison used

```text
python scripts/compare_conditioned_product_local.py --mean 16 --n-values 100,500,2000,10000 --output data/conditioned_product_local_exact.csv
```

The canonical `mu=16` witness has 12 coordinates, caps
`(2,1,0,0,0,0,0,0,0,1,2,4)`, and total cap mass 10. Its matching product
probability is `2.2977271062e-13`. The exact conditioned/product ratios are
`0.4808, 0.8686, 0.9656, 0.9930` at `n=100,500,2000,10000`. At `n=10000`,
`log R=-0.006984`, while the elementary rigorous bound gives
`|log R|<=0.019139`. This directly sanity-checks the local equivalence-of-
ensembles estimate on the witness used in the proof.

All three outputs record the code commit, exact command, parameters, and seeds
where applicable in sidecar metadata and `data/experiment_log.jsonl`.


## Session 4: spatial-front diagnostics

Session 4 used computation only for the two structural questions left open by
the new proof.

### Exact missed-front catalogue

The exact command represented by
`scripts/classify_missed_front_failures.py` uses all weak compositions with
`2<=n<=10` and `1<=t<=8`. Across the grid, 20,429 nonstackable
configurations are missed by direct overlap of the two irreversible fronts.
All 20,429 nevertheless possess both one-sided fronts. Their failure of the
certificate is a central gap, not absence of a front.

Among the missed cases, 5,579 have `max_i S_i=0` and 14,850 have
`max_i S_i<0`. Hence the finite counterexample `(1,0,2)` is not merely
representative of an equality-score exception. The maximum uncovered gap in
the tested rectangle is 4. Full counts are in
`data/missed_front_small_exact.csv`.

### Seed-to-front conversion

The statistic was fixed before sampling: start from `M_0=-mu`, take
`n=2^{ceil(log_2 mu)^2}`, and record whether the exact product-geometric
chain reaches `Z>=2nmu+3` before its first exit from the low phase.

With 20,000 trials per mean and seed `2026092700+mu`:

| mu | hits | estimate | Wilson 95% interval | mean steps given hit |
|---:|---:|---:|---:|---:|
| 16 | 5268 | 0.2634 | [0.25734, 0.26955] | 19.52 |
| 32 | 4318 | 0.2159 | [0.21025, 0.22166] | 28.75 |
| 64 | 3969 | 0.19845 | [0.19298, 0.20404] | 39.88 |
| 128 | 3723 | 0.18615 | [0.18082, 0.19160] | 52.92 |

The purpose was only to discriminate an order-one conversion probability from
a second rare-event exponent. The rigorous proof uses the much smaller
universal lower bound `0.0095991`; these estimates do not enter any theorem.

### Rigorous finite-parameter spatial table

`data/spatial_front_rigorous_bounds.csv` records the exact formula values for
the canonical superblock at `mu=2^L` and `n=2^{L^2}`. At the exact
coefficient-one scale the explicit lower witness remains far too conservative
at finite `L`: `log_2(Bp)` is negative throughout the tabulated
`L=4,5,6,8,10,12,16` range. This is expected from the
`O(L log L)` subleading loss and is not evidence against the asymptotic
`c<1` theorem.

### Validation note

GitHub-hosted Actions was attempted for a literal final `pytest` run but the
run failed before job creation (`jobs=0`), so that failed run is not counted
as code validation and the temporary workflow was removed.

The original 34 Session 3 tests concern files unchanged in Session 4. In the
session harness, the following exact checks were rerun against the committed
formulas:

- all 146 labeled trees through order 5, 33,711 configurations through mass 5,
  and 166,116 rooted direct-vs-structural cases, with zero disagreements;
- 24,309 path message/score comparisons against the general evaluator;
- 167,959 exact pruned-path decisions;
- the Session 3 product-chain test identities and finite bounds;
- all current Session 4 spatial deterministic/numerical assertions, including
  the stable Robbins conditioning bounds and the stretched-log two-sided bound.

Thus the mathematical checks underlying the new commit were independently
reproduced, but a literal `pytest` invocation at the final HEAD was not
available in this execution environment. This limitation is recorded rather
than reported as a passing pytest run.


## Session 5: necessity and supercritical validation

Session 5 began by closing the Session 4 validation caveat. In the local
execution environment, the literal full test suite was run successfully after
the new Session 5 code was added. The suite contains 54 tests, all passing.
The independent exact validator was also rerun and returned:

validated 146 labeled trees, 33711 configurations, 166116 rooted cases; no disagreements

The Session 5 deterministic necessity theorem is checked exhaustively by
tests/test_soft_front.py, while tests/test_supercritical.py checks the local
cap-cover implication, finite probability ordering, and conditioned bound
behavior. The cap-cover test includes all 7^6=117649 occupancy strings in the
bounded alphabet 0,...,6 at mu=16, plus targeted boundary and interior
deep-excursion examples.

### Exact deep-message catalogue

Command:

python scripts/classify_deep_message_necessity.py --max-order 10 --max-total 10 --output data/deep_message_necessity_exact.csv

The script enumerates every weak composition in the displayed rectangle,
filters the nonstackable configurations, and compares the minimum directed
message with the proved forced threshold

h_*(n,t)=max(1, 2 floor((t-1)/(n-1))-1).

Across the rectangle there are 307646 nonstackable configurations. No
counterexample to the theorem occurs. Forty-seven configurations attain the
forced threshold exactly, so the deterministic estimate is genuinely tight on
bounded instances rather than merely qualitative. Examples include (1,1) at
(n,t)=(2,2), (3,0,3) at (3,6), and (1,0,4,5) at (4,10).

### Finite supercritical bound table

Command:

python scripts/tabulate_supercritical_bound.py --levels 20,30,40,50 --coefficients 1.05,1.10,1.25,1.50 --output data/supercritical_bound_table.csv

This evaluates the proved local-cap plus conditioning formula at mu=2^L and
log2(n)=round((L/c)^2). It is not Monte Carlo.

For c=1.10, the log2 upper bounds on fixed-total nonstackability are
approximately 17.67, -28.09, -109.22, and -224.56 at L=20,30,40,50. For
c=1.25 they are approximately -57.33, -196.09, -407.22, and -690.56. The slow
finite convergence at c=1.05 is expected from lower-order terms: the bound
becomes negative by L=50.

These finite values are diagnostics of the proved formula, not the proof of
the asymptotic theorem. The proof uses
log2 a_mu=-L^2/2+O(L), log2 b_mu=-L^2/2+O(L), R=O(L^2), and local conditioning
error o(1).
