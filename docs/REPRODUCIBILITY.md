# Reproducibility

This is the authoritative entry point for final theorem verification. The
frozen theorem is rigorous paper mathematics supported by exact finite Lean
interfaces and deterministic computation; Monte Carlo is not part of the
proof validation.

## Environment

Python 3.11+ is supported. The project has no runtime dependencies outside the
standard library; pytest is required for the regression suite.

```bash
python -m pip install pytest
```

The final validation is intentionally run with `PYTHONPATH=.`; no packaging
change or editable installation is required.

## Full Python regression suite

```bash
PYTHONPATH=. pytest -q
```

The Session 19 invariant tests explicitly freeze the exact deep target
`-(2*mu-1)`, the spatial factor `n`, concatenation rather than conditioned
independence for separated local blocks, and the TreeStack/Mathlib/Lean pins.

## Independent finite structural validation

```bash
PYTHONPATH=. python scripts/validate_small.py --max-order 5 --max-total 5
```

This stops on the first disagreement between direct legal-move reachability
and TreeStack scores, including rooted decisions.

## Deterministic Session 16 binary-partition diagnostics

Regenerate the committed table with:

```bash
PYTHONPATH=. python scripts/tabulate_binary_partition_asymptotics.py \
  --levels 6,8,10,12,14 \
  --phases 9/16,3/4,1 \
  --output /tmp/session16_binary_partition_diagnostics.csv
cmp /tmp/session16_binary_partition_diagnostics.csv \
  data/session16_binary_partition_diagnostics.csv
```

The exact generating command and purpose are recorded in
`data/session16_binary_partition_diagnostics.csv.meta.json`. This table
checks finite counts, truncation/cutoff handling, the negative
`L log_2 L` sign and the derived linear coefficients. It is validation, not
the proof of the binary-partition asymptotic.

## Deterministic Session 17 product-geometric diagnostics

Session 17 intentionally has no committed CSV table; regenerate the diagnostic
directly from the authoritative script:

```bash
PYTHONPATH=. python scripts/tabulate_product_geometric_asymptotics.py \
  --levels 4,6,8,10,12 \
  --phases 9/16,3/4,1 \
  --exact-through-level 8 \
  --output /tmp/session17_product_geometric.csv
```

For a byte-level determinism check, run the same command to a second path and
`cmp` the two outputs. The table separates exact counts, the geometric
`p^k` atom factor, tilt, total probability, sharp-seed coefficient and
optimized local coefficient. It validates the implementation; the Session 17
local asymptotic theorem is paper mathematics.

## Deterministic Session 18 global conditioning diagnostics

Regenerate the committed table with:

```bash
PYTHONPATH=. python scripts/tabulate_global_conditioning.py \
  --levels 256,1024,4096,16384 \
  --offsets=-2,-1,-0.5,0.5,1,2 \
  --output /tmp/session18_global_balance.csv
cmp /tmp/session18_global_balance.csv data/session18_global_balance.csv
```

The sidecar `data/session18_global_balance.csv.meta.json` records the exact
parameters. The table checks the frozen MINUS half-log-log sign,
`log_2(3e)`, the factor `n` in the spatial hazard, and the scale separation
between the product no-success exponent and the conditioning cost.

## Permanent Lean validation

The pinned environment is:

- TreeStack `f4112f08d42a37c0941bf469ac124621b1f54f22`;
- Mathlib `065356127b1dc0016f66b7283ce0ce2c4055aa55`;
- Lean `leanprover/lean4:v4.35.0-rc2`.

The permanent workflow is `.github/workflows/lean-bootstrap.yml`. Its core
local commands are:

```bash
lake update
lake build @treestack/+TreeStack.RootScore
lake build
if grep -R -n -E '(^|[^A-Za-z])(sorry|axiom)([^A-Za-z]|$)' \
    --include='*.lean' ProbStack ProbStack.lean; then
  exit 1
fi
```

A successful permanent workflow therefore validates the exact pinned TreeStack
dependency build, the complete ProbStack Lean build, and the no-`sorry` /
no-project-`axiom` condition.

## Exact historical data

The exact path atlas can be regenerated with:

```bash
PYTHONPATH=. python scripts/enumerate_paths.py --min-n 2 --max-n 9 --max-t 12 \
  --output data/path_exact_atlas.csv
PYTHONPATH=. python scripts/scan_probability_profile.py data/path_exact_atlas.csv
```

CSV rows retain exact integer counts and rational probabilities. Sidecar
metadata records generators and parameters.

## Historical Monte Carlo data

Monte Carlo datasets in `data/` are retained as discovery history. They use
fixed/derived seeds and exact stars-and-bars sampling from uniform weak
compositions, not multinomial pebble placement. They are not needed to verify
the final theorem and should not be substituted for the deterministic
Session 16--18 diagnostics.

## Status documents

For the meaning of each validation layer, see:

- `docs/FINAL_THEOREM_STATUS.md`;
- `docs/PROOF_DEPENDENCY_MAP.md`;
- `notes/session-19-closure.md`.

These documents distinguish rigorous paper mathematics, exact finite Lean
formalisation, and deterministic computational validation.
