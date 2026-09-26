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
