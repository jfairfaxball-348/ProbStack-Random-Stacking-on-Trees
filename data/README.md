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
