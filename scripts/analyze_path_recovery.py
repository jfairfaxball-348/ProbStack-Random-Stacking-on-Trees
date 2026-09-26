#!/usr/bin/env python3
"""Targeted path recovery experiments driven by the one-dimensional recursion.

Two experiment modes are run together:

1. corrected-scale grid: t = n(log2 n - c log2 log2 n), testing whether a
   log-log subtraction reduces the drift seen under a fixed multiple of n log n;
2. obstruction diagnostics: for the same trials, compare longest zero/low runs
   with the exact irreversible-deficit-front certificate.

All configurations are sampled uniformly from weak compositions by stars and
bars.  The stackability decision uses the exact front-pruned path evaluator,
which is exhaustively cross-checked against the general TreeStack evaluator in
``tests/test_path_score.py``.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from random import Random

from prob_stack.configurations import sample_uniform_weak_composition
from prob_stack.path_score import (
    fronts_certify_nonstackability,
    irreversible_deficit_fronts,
    path_structurally_stackable_pruned,
)


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "UNCOMMITTED"


def parse_ints(raw: str) -> list[int]:
    return [int(x) for x in raw.split(",") if x]


def parse_floats(raw: str) -> list[float]:
    return [float(x) for x in raw.split(",") if x]


def longest_run_at_most(configuration: tuple[int, ...], threshold: int) -> int:
    best = current = 0
    for value in configuration:
        if value <= threshold:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-values", default="640,2560,10000,40000")
    parser.add_argument("--corrections", default="0,0.5,0.75,1.0")
    parser.add_argument("--trials", type=int, default=200)
    parser.add_argument("--seed-base", type=int, default=2026092620)
    parser.add_argument(
        "--output", type=Path, default=Path("data/path_recovery_correction_mc.csv")
    )
    args = parser.parse_args()

    ns = parse_ints(args.n_values)
    corrections = parse_floats(args.corrections)
    rows: list[dict[str, object]] = []

    for n in ns:
        logn = math.log2(n)
        loglog = math.log2(logn)
        for correction in corrections:
            density = logn - correction * loglog
            t = round(n * density)
            seed = args.seed_base + n * 10_000 + round(correction * 1_000)
            rng = Random(seed)
            successes = certified_failures = failures = 0
            zero_sum_success = zero_sum_failure = 0
            low1_sum_success = low1_sum_failure = 0
            front_gap_sum_failure = 0
            front_gap_count_failure = 0

            for _ in range(args.trials):
                c = sample_uniform_weak_composition(t, n, rng)
                stackable = path_structurally_stackable_pruned(c)
                zero_run = longest_run_at_most(c, 0)
                low1_run = longest_run_at_most(c, 1)
                if stackable:
                    successes += 1
                    zero_sum_success += zero_run
                    low1_sum_success += low1_run
                else:
                    failures += 1
                    zero_sum_failure += zero_run
                    low1_sum_failure += low1_run
                    certified = fronts_certify_nonstackability(c)
                    certified_failures += certified
                    lf, rf = irreversible_deficit_fronts(c)
                    if lf is not None and rf is not None:
                        front_gap_sum_failure += max(0, lf - rf - 1)
                        front_gap_count_failure += 1

            row = {
                "family": "path",
                "n": n,
                "correction_c": f"{correction:.8g}",
                "scaling": "n*(log2(n)-c*log2(log2(n)))",
                "t": t,
                "mean_density": f"{t/n:.17g}",
                "trials": args.trials,
                "successes": successes,
                "estimate": f"{successes/args.trials:.17g}",
                "failures": failures,
                "front_certified_failures": certified_failures,
                "front_certificate_fraction_of_failures": (
                    f"{(certified_failures/failures if failures else 0):.17g}"
                ),
                "mean_longest_zero_run_success": (
                    f"{(zero_sum_success/successes if successes else 0):.17g}"
                ),
                "mean_longest_zero_run_failure": (
                    f"{(zero_sum_failure/failures if failures else 0):.17g}"
                ),
                "mean_longest_leq1_run_success": (
                    f"{(low1_sum_success/successes if successes else 0):.17g}"
                ),
                "mean_longest_leq1_run_failure": (
                    f"{(low1_sum_failure/failures if failures else 0):.17g}"
                ),
                "mean_uncovered_front_gap_failure": (
                    f"{(front_gap_sum_failure/front_gap_count_failure if front_gap_count_failure else 0):.17g}"
                ),
                "seed": seed,
            }
            rows.append(row)
            print(
                f"P_{n}: c={correction:g}, t={t}, "
                f"{successes}/{args.trials}={successes/args.trials:.4f}; "
                f"front-certified failures={certified_failures}/{failures}"
            )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    metadata = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_commit(),
        "command": (
            "python scripts/analyze_path_recovery.py "
            f"--n-values {args.n_values} --corrections {args.corrections} "
            f"--trials {args.trials} --seed-base {args.seed_base} "
            f"--output {args.output}"
        ),
        "model": "uniform weak compositions of t into n nonnegative parts",
        "predicate": "exact path TreeStack recurrence with irreversible-deficit pruning",
        "statistics": {
            "zero_run": "maximum consecutive vertices with C_i=0",
            "low1_run": "maximum consecutive vertices with C_i<=1",
            "front_certificate": "two irreversible one-sided exclusion fronts cover all roots",
        },
    }
    args.output.with_suffix(args.output.suffix + ".meta.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
