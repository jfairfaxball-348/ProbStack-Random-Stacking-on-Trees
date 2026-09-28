# Data policy

This directory contains only outputs generated from committed ProbStack code.
No synthetic or placeholder result files should be added.

- `path_exact_atlas.csv`: exact integer counts and rational probabilities for a
  bounded path rectangle.  Its `.meta.json` sidecar records the command,
  revision, range, model, and runtime.
- `path_linear_density_mc.csv`: seeded Monte Carlo data at fixed linear densities `t=a*n`; used as a competing scaling check.
- `path_recovery_scaling_mc.csv`: seeded Monte Carlo orientation data for the
  candidate `a * n * log2(n)` recovery normalization.  Raw success counts and
  trial counts are retained; the estimates are not treated as proofs.
- `path_recovery_large_mc.csv`: lower-trial extension of the same normalization to `n=1280,2560`.
- `experiment_log.jsonl`: one JSON object per recorded experiment, including
  command, Git commit, parameters, seed (or null), output path, and a short
  interpretation.

The intended probability space is always the uniform law on weak compositions
of `t` into `n` nonnegative parts.  Do not substitute independent placement of
labeled pebbles.


## Session 4 additions

- `spatial_front_rigorous_bounds.csv`: rigorous formula table for the reset +
  canonical witness + runaway-buffer superblock at selected dyadic means.
- `seed_to_front_mc.csv`: seeded Monte Carlo diagnostic for conversion from
  `M=-mu` to a whole-path-strength deficit before low-phase rescue.
- `missed_front_small_exact.csv`: exact classification of bounded
  nonstackable path configurations missed by direct front overlap.

Each file has a metadata sidecar recording parameters, source commit, purpose,
and the fact that the final values were evaluated in the session harness after
GitHub Actions failed before job creation.


## Session 5 additions

- deep_message_necessity_exact.csv: exact bounded catalogue comparing the
  minimum directed message in every nonstackable path through n<=10,t<=10 with
  the Session 5 forced threshold. It contains 307646 nonstackable
  configurations in total and 47 exact-threshold cases.
- supercritical_bound_table.csv: finite evaluations of the proved
  supercritical local-cap/conditioning upper bound at selected dyadic means and
  coefficients above one. This is a formula table, not Monte Carlo.

Both files have metadata sidecars giving the generating command and the
Session 5 source commit.

## Session 6 additions

- second_order_local_bounds.csv: rigorous formula evaluations for the
  dyadic-simplex second-order bounds at selected dyadic means, together with
  exact rational dynamic-programming probabilities for the two witness
  components through L=10.
- second_order_local_bounds.csv.meta.json: command, source revision, exactness
  statement, parameters, and interpretation for that table.

The Session 6 table is diagnostic support for an analytic theorem. It is not
Monte Carlo and is not used to infer the L log L coefficient by fitting.

## Session 7 additions

- `linear_order_entry_counts.csv`: exact integer reverse-DP counts for
  positive-phase entry into terminal messages 0 and 1 at selected dyadic
  phases, plus exact colored-slack lower-subset counts.
- `linear_order_entry_counts.csv.meta.json`: command, source revision,
  exactness statement, and interpretation.

The Session 7 table is a validation diagnostic, not a fit. The linear local
coefficient is derived analytically from binary-partition asymptotics and the
exact positive-phase slack generating function. The table records the bounded
spatial gap that existed at the end of Session 7; Session 8 later closed that
gap by constant-cost regeneration. No Monte Carlo was used.


## Session 8 additions

- regeneration_exact.csv: exact Fraction probabilities for the worst
  one-step regeneration state at selected integer means.
- regeneration_exact.csv.meta.json: generating command, source revision,
  exactness statement, and interpretation.

The regeneration table validates an elementary exact lemma; it is not a fit and
contains no Monte Carlo output.


## Session 16 additions

- `session16_binary_partition_diagnostics.csv`: exact integer finite
  binary-partition/dyadic-simplex diagnostics across the documented levels and
  phases.
- `session16_binary_partition_diagnostics.csv.meta.json`: exact generating
  command, parameter grid, purpose and non-Monte-Carlo status.

The table checks finite indexing, cutoff/truncation handling and asymptotic
signs. It is not the proof of the de Bruijn asymptotic.

## Session 18 additions

- `session18_global_balance.csv`: deterministic fixed-offset balance and
  conditioning-cost diagnostics.
- `session18_global_balance.csv.meta.json`: exact generator, parameter grid,
  frozen center and purpose.

This table checks the MINUS half-log-log sign, `log_2(3e)`, the spatial
factor `n`, and the separation from the conditioning point-mass cost. It is
validation only, not the global proof.

Session 17 product-geometric diagnostics are regenerated on demand rather than
stored as a committed CSV; see `docs/REPRODUCIBILITY.md`.
