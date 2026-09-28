# Final theorem status

**Session 19 closure document.** This file is the concise authoritative status
for the theorem/proof/formalisation/reproducibility stage.

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
  ordinary-mass bounds, and reversal invariance in `FiniteDyadic.lean`.

The current ProbStack Lean source does **not** package the full Session 5
global implication

```
nonstackable => some directed message <= -(2*mu-1),
```

nor a single global `opposing fronts => nonstackable` theorem. Those are
rigorous deterministic paper mathematics. Session 19 leaves them there rather
than adding nontrivial path/root-score infrastructure merely to increase
formal theorem count.

## What remains paper mathematics rather than Lean

The deliberate non-Lean layer is:

- the two global deterministic implications just identified;
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
- novelty, priority, publication, or submission status.

The next stage is a separate extensive public-record prior-art/originality
audit. It must not reopen the frozen theorem.
