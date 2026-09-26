# Reproducibility

## Environment

The project has no runtime dependencies outside the Python standard library.
Python 3.11+ is supported.  Install pytest for tests:

```bash
python -m pip install -e '.[test]'
```

## Validation

```bash
pytest
python scripts/validate_small.py --max-order 5 --max-total 5
```

The second command stops immediately on the first disagreement between direct
legal-move reachability and TreeStack scores, including rooted decisions.

## Exact data

```bash
python scripts/enumerate_paths.py --min-n 2 --max-n 9 --max-t 12 \
  --output data/path_exact_atlas.csv
python scripts/scan_probability_profile.py data/path_exact_atlas.csv
```

CSV rows retain exact integer counts and rational probabilities.  The sidecar
metadata records the generator command, Git revision, range, model, and timing.

## Monte Carlo data

Fixed linear-density comparison:

```bash
python scripts/compare_path_scalings.py \
  --n-values 20,40,80,160 --scaling linear \
  --multipliers 2,3,4,5,6,8,10 --trials 1000 \
  --seed-base 2026092600 --output data/path_linear_density_mc.csv
```

Mixed-scale comparison:

```bash
python scripts/compare_path_scalings.py \
  --n-values 40,80,160,320,640 \
  --multipliers 0.55,0.65,0.75,0.85,1.00 \
  --trials 1000 --seed-base 2026092600 \
  --output data/path_recovery_scaling_mc.csv
```


Large-path extension (lower trial count):

```bash
python scripts/compare_path_scalings.py \
  --n-values 1280,2560 --scaling nlog2 \
  --multipliers 0.70,0.75,0.80,0.85 --trials 200 \
  --seed-base 2026092600 --output data/path_recovery_large_mc.csv
```

Every grid point uses a deterministic derived seed and records the seed, raw
success count, and trial count.  The sampler is exact stars-and-bars sampling
from uniform weak compositions; it is not multinomial pebble placement.

## Experiment ledger

`data/experiment_log.jsonl` is append-only research metadata.  Each line must
contain at least: `command`, `git_commit`, `parameters`, `seed`, `output`, and
`interpretation`.  The Git revision means the code revision that generated the
output, which may precede the later commit that adds the generated data itself.
