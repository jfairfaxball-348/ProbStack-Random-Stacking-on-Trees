# Final theorem / proof dependency map

**Authoritative from Session 19 onward.** Historical dependency plans,
especially `notes/session-9-formalisation-design.md`, remain records of what
was proposed at the time. This file is the current map of what the repository
actually proves, formalises, and validates.

## Frozen headline theorem

Let `C_n` be uniform over the weak compositions of total `n*mu_n` on the
path `P_n`, with positive integer `mu_n`, and define

```
c_n = sqrt(log_2 n)
      - (1/2) log_2 log_2 n
      + log_2(3e).
```

For every fixed `epsilon > 0`:

- if `log_2 mu_n <= c_n - epsilon` eventually, then
  `P(C_n is stackable) -> 0`;
- if `log_2 mu_n >= c_n + epsilon` eventually, then
  `P(C_n is stackable) -> 1`.

There is no claim at `epsilon = 0`.

## Dependency DAG

| ID | Proof node | Authoritative repository anchor | Lean status | Exact computation / validation | Depends on |
|---|---|---|---|---|---|
| P1 | TreeStack structural criterion `StackableAt(T,C,r) iff 0 < score(T,C,r)`; categorical `EMPTY` | pinned TreeStack `TreeStack.RootScore`; `ProbStack/TreeStackBoundary.lean`; `notes/session-9-formalisation-design.md` | Imported/formal; `empty_ne_some_zero` is formal | exhaustive TreeStack/direct-reachability tests | — |
| P2 | Exact path message recurrence in both orientations | `ProbStack/PathMessage.lean`, `PathBranch.lean`, `PathBridge.lean` | Formal | `tests/test_path_score.py` | P1 |
| P3 | Low-phase deficit recurrence and dyadic closed form | `ProbStack/Deficit.lean`, `PathBridge.lean` | Formal | exact recurrence tests | P2 |
| P4 | Deep seed, runaway growth, irreversible certified front; left/right seed-to-front composition | `ProbStack/PathFront.lean`, `FiniteProbability.lean`; `notes/session-13-front.md` | Formal finite interface | exact cap/front tests | P2, P3 |
| P5 | Opposing irreversible fronts imply path nonstackability | Sessions 4/8 proof architecture; `notes/path-dynamics.md`, `notes/session-18-conditioning-global.md` | **Paper deterministic theorem; no single ProbStack Lean theorem currently packages this global implication** | small exact path validation | P1, P4 |
| P6 | Session 5 deep-message necessity: nonstackability at total `n*mu` forces a directed message `<= -(2*mu-1)` | `ProbStack/PathNecessity.lean`; `notes/proof-plan.md` Session 5; `prob_stack/supercritical.py` | **Formal.** `nonstackable_exists_directedMessage_le` proves the general `h` statement and `nonstackable_total_mul_exists_directedMessage_le` proves the exact fixed-total corollary | full Lean build + exact finite P6 regression | P1, P2 |
| P7 | Exact iid-geometric / weak-composition conditioning identity | `notes/session-18-conditioning-global.md`; `ProbStack/FiniteProbability.lean` matched masses | Lean formalises constant product mass on a fixed-total fibre and finite local mass definitions; full normalised event-level conditioning identity remains paper/finite combinatorics | exact Fraction tests | — |
| P8 | Exact finite local conditioned/product likelihood ratio and bounded-support transfer | `prob_stack/product_chain.py`, `finite_probability.py`, `global_conditioning.py`; `ProbStack/FiniteProbability.lean` | Definitions and fixed-vector algebra formal; logarithmic transfer inequality is paper/Python | exact formula cross-checks and brute force | P7 |
| P9 | Finite dyadic simplex and binary-partition encoding | `ProbStack/FiniteDyadic.lean`, `prob_stack/finite_dyadic.py`; Sessions 15–16 notes | Formal finite combinatorics | exact integer diagnostics | P3 |
| P10 | Binary-partition asymptotic used at the required compact-uniform scales | `notes/session-16-binary-partition-asymptotics.md`, `prob_stack/binary_partition_asymptotics.py` | Paper analysis | deterministic exact-count table | P9 |
| P11 | Session 17 one-sided product-geometric local excursion theorem, uniform in dyadic phase and `m in [mu,2mu]` | `notes/session-17-product-geometric-local-asymptotics.md` | Paper analysis | deterministic weighted-simplex diagnostics/tests | P10 |
| P12 | Session 8 one-coordinate regeneration from `-mu < M <= 2mu` into `[mu,2mu]`, with cap `5mu-1` and constant minorisation | `ProbStack/TransferBounds.lean`, `PathDeep.lean`, `prob_stack/regeneration.py`, `notes/session-8-regeneration.md` | Formal deterministic transfer; probability lower bound paper/Python | exact exhaustive regeneration tests | P2 |
| P13 | Product-law spatial abundance of reserved superblocks below the center | `notes/session-18-conditioning-global.md` sections 5–6 | Paper global probability | deterministic support/hazard diagnostics | P4, P11, P12 |
| P14 | Transfer from product law to fixed total without conditioned independence | `notes/session-18-conditioning-global.md` sections 1–3,6; `global_conditioning.py` | Paper analytic transfer; exact finite algebra partially formal | exact one/two-block ratio tests | P7, P8, P13 |
| P15 | Supercritical terminal-specific local upper cover, bridge treatment, interior `O(n)` versus physical-boundary `O(1)` locations | `notes/session-17-product-geometric-local-asymptotics.md`; `notes/session-18-conditioning-global.md` section 7; `prob_stack/supercritical.py` | Paper probability/deterministic cover | exact cover tests | P6, P8, P11 |
| P16 | Fixed-offset balance `R(c_n+delta) = log_2 n + 2*delta*sqrt(log_2 n) + o(sqrt(log_2 n))` | `notes/session-18-conditioning-global.md` section 8; `global_conditioning.py` | Paper asymptotic algebra | Session 18 deterministic table/tests | P11 |
| P17 | Two-sided frozen headline theorem | `notes/session-18-conditioning-global.md`; `docs/FINAL_THEOREM_STATUS.md` | **Paper theorem, not a Lean limit theorem** | full exact deterministic/Python regression + permanent Lean finite-interface CI | P5, P6, P14, P15, P16 |

## Below the center

Reset + Session 8 regeneration + the Session 17 local excursion + runaway
conversion form an `O(log n)`-support reserved superblock. Each half-path
contains `Omega(n/log n)` disjoint candidates. Under the iid product law,
unused coordinates remain fresh after previous failures, so a sequential
hazard argument gives the product no-success bound first. Only then is the law
conditioned on total `n*mu`. The reciprocal conditioning cost has only
`O(log n)` bits and is overwhelmed at every fixed negative offset. The
construction is repeated in the reversed half; a union bound supplies opposing
fronts. **No conditioned-block independence is used.**

## Above the center

The exact deterministic target is `-(2*mu-1)`. Interior first-hit covers
have the Session 17 optimized phase-free rate and `O(n)` possible locations.
A `1 -> 0` route needs one exact-output-zero bridge; because `F(y)=0` only
for `y=3`, one geometric occupancy is fixed once the incoming message is
known, at cost `L+O(1)` bits. Physical-boundary witnesses have only `O(1)`
locations and receive no factor `n`. Bounded support/mass permits local
conditioned/product transfer.

## Formalisation boundary

Session 19 deliberately did not attempt Stirling/Robbins asymptotics,
de Bruijn binary-partition asymptotics, the Session 17 real asymptotic local
rate, or the final limit theorem in Lean. Session 23 subsequently formalised
the Session 5 global deep-message necessity in `PathNecessity.lean`, without
reopening any analytic layer. The global opposing-front implication P5 remains
paper-level deterministic mathematics. The Lean development therefore now
contains P6 together with the finite path-message, deep-block, regeneration,
seed, runaway and front interfaces that feed the frozen paper theorem.

This distinction is authoritative and should not be blurred in future stages.
