# Final theorem status

**Session 19 closure document, updated after public release.** This file is the
concise authoritative status for the theorem/proof/formalisation/reproducibility
boundary and records the later Palomar and arXiv public identifiers.

## Public records

The paper **A Fixed-Offset Transition for Random Stackability on Paths** by
John Fairfax-Ball is publicly posted as
[arXiv:2609.39633](https://arxiv.org/abs/2609.39633), version 1, submitted
30 September 2026. The primary category is `math.CO` and the cross-list is
`math.PR`. The arXiv-issued DOI is
[10.48550/arXiv.2609.39633](https://doi.org/10.48550/arXiv.2609.39633).
The article license is CC BY 4.0.

The finite deterministic P6 theorem and its exact fixed-total corollary are
registered separately as
[PALOMAR-2026-09-30-000023, version 1](https://palomar-registry.org/entry.html?id=PALOMAR-2026-09-30-000023&version=1).
That registration does not cover the full probabilistic theorem. Neither an
arXiv posting nor Palomar registration is represented here as peer review.

## Frozen theorem

For positive integer `mu_n`, let `C_n` be uniformly distributed over the
weak compositions of total `n*mu_n` on `P_n`. Put

```
c_n = sqrt(log_2 n)
      - (1/2) log_2 log_2 n
      + log_2(3e).
```

For every fixed `epsilon > 0`:

```
log_2 mu_n <= c_n - epsilon eventually
    => P(C_n is stackable) -> 0,

log_2 mu_n >= c_n + epsilon eventually
    => P(C_n is stackable) -> 1.
```

The half-log-log sign is **MINUS** and the additive constant is
`log_2(3e)`. There is no claim at `epsilon = 0`.

## What is fully proved mathematically

The rigorous paper proof includes:

- the exact TreeStack/path structural reduction and categorical EMPTY
  semantics;
- exact left/right path-message and deficit recurrences;
- finite irreversible-front and runaway machinery;
- the deterministic opposing-front obstruction;
- the Session 5 deep-message necessity with exact target `-(2*mu-1)`;
- the exact iid-geometric representation of uniform weak compositions by
  conditioning on the total;
- finite local conditioned/product likelihood ratios;
- finite dyadic/binary-partition reductions;
- the binary-partition asymptotic used in the required regimes;
- the Session 17 one-sided local excursion theorem, uniform over dyadic phase
  and all integer starts `m in [mu,2mu]`;
- Session 8 constant-cost regeneration;
- the Session 18 subcritical spatial-abundance argument;
- the Session 18 supercritical terminal-specific upper cover;
- the fixed-offset balance and therefore the frozen two-sided theorem.

The complete dependency map is `docs/PROOF_DEPENDENCY_MAP.md`.

## What is Lean-formalised

The pinned Lean layer formalises the exact finite interfaces useful at the
paper/Lean boundary:

- `ProbStack.empty_ne_some_zero`;
- `pathStep` and exact EMPTY behaviour in `PathMessage.lean`;
- actual left/right TreeStack branch-message recurrences in
  `PathBranch.lean` and `PathBridge.lean`;
- `activeStep`, `deficit`, `LowRun`, `dyadicInputCost`, and exact
  low-phase deficit identities in `Deficit.lean`;
- `F_le_half`, steering arithmetic, `F_mem_mu_two_mu`, and
  `regeneration_transfer_window` in `TransferBounds.lean`;
- left/right block scans, weighted consequences of a deep terminal message,
  and `leftBranch_regeneration_step` /
  `rightBranch_regeneration_step` in `PathDeep.lean`;
- `DeepSeed`, `UniformDeepSeedBlock`, `CertifiedFront`,
  `deepSeed_runaway_to_front`, `certifiedFront_dominates`, and the genuine
  left/right regeneration-seed-runaway-to-front theorems in
  `PathFront.lean`;
- explicit finite seed/cap/runaway support and mass lemmas plus genuine
  left/right capped-seed front corollaries in `FiniteProbability.lean`;
- exact geometric finite-mass definitions, `IsWeakComposition`,
  `weakCompositionCount`, matched product-vector mass, constant mass on a
  fixed-total fibre, conditioned local-vector mass, and local-likelihood-ratio
  definitions in `FiniteProbability.lean`;
- exact finite dyadic/binary-partition encodings, low-phase simplex facts,
  ordinary-mass bounds, and reversal invariance in `FiniteDyadic.lean`;
- the Session 5 global deep-message necessity in `PathNecessity.lean`:
  `nonstackable_exists_directedMessage_le` and the exact fixed-total
  corollary `nonstackable_total_mul_exists_directedMessage_le`, which forces
  an actual directed path message at most `-(2*mu-1)`.

The current ProbStack Lean source still does **not** package a single global
`opposing fronts => nonstackable` theorem. P5 remains rigorous deterministic
paper mathematics; Session 23 changed only the P6 side of this formalisation
boundary.

## What remains paper mathematics rather than Lean

The deliberate non-Lean layer is:

- the global deterministic implication `opposing fronts => nonstackable` (P5);
- the full normalised event-level conditioning/uniformity theorem for the
  weak-composition fibre (Lean already contains its constant-atom algebra);
- Robbins/Stirling asymptotics for the conditioning point mass;
- de Bruijn/binary-partition asymptotics;
- the Session 17 product-geometric local asymptotic theorem;
- the Session 18 spatial abundance/conditioning limit arguments;
- the final two-sided limit theorem.

No `sorry` and no new project axiom are used to hide these distinctions.

## What has been computationally validated

Exact or deterministic validation includes:

- exhaustive direct legal-move versus TreeStack agreement on the recorded
  finite ranges;
- exact path-message/deficit/front tests;
- exact weak-composition counts and local conditioned/product ratios;
- exact regeneration intervals and worst-case probability;
- exact finite dyadic/binary-partition counts;
- deterministic Session 16 binary-partition diagnostics;
- deterministic Session 17 product-geometric diagnostics;
- deterministic Session 18 global conditioning/fixed-offset diagnostics;
- the full Python regression suite.

Monte Carlo data remain exploratory historical evidence and are not part of
the final theorem proof validation.

## What is not claimed

The project makes no claim of:

- a theorem at zero offset;
- a critical limiting distribution or Poisson front law;
- finite-`n` monotonicity in total mass;
- an arbitrary-tree extension of the path threshold;
- unconditional historical novelty or priority;
- full Lean formalisation of the asymptotic theorem;
- peer review or journal acceptance merely from the arXiv posting or Palomar
  registration.

Sessions 20–21 completed the public-record prior-art audit. Session 23
formalised P6; the finite theorem and fixed-total corollary were subsequently
registered with Palomar. The standalone paper was then completed, packaged and
posted publicly as arXiv:2609.39633. These release stages do not alter the
frozen mathematical or formalisation boundary recorded above.
