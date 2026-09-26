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
