#!/usr/bin/env python3
"""Test the recurrence-motivated stretched-log path recovery scale.

The candidate density is

    mu_n = a * 2**sqrt(log2(n)),

motivated by a two-sided rare deficit-excursion heuristic.  This is an
experiment, not a theorem or promoted conjecture.
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-values", default="640,2560,10000,40000")
    parser.add_argument("--multipliers", default="0.75,0.84,0.95")
    parser.add_argument("--trials", type=int, default=200)
    parser.add_argument("--seed-base", type=int, default=2026092640)
    parser.add_argument(
        "--output", type=Path, default=Path("data/path_stretched_scale_mc.csv")
    )
    args = parser.parse_args()

    rows: list[dict[str, object]] = []
    for n in parse_ints(args.n_values):
        base_density = 2 ** math.sqrt(math.log2(n))
        for multiplier in parse_floats(args.multipliers):
            t = round(multiplier * n * base_density)
            seed = args.seed_base + n * 10_000 + round(multiplier * 1_000)
            rng = Random(seed)
            successes = failures = certified_failures = 0
            for _ in range(args.trials):
                c = sample_uniform_weak_composition(t, n, rng)
                stackable = path_structurally_stackable_pruned(c)
                successes += stackable
                if not stackable:
                    failures += 1
                    certified_failures += fronts_certify_nonstackability(c)

            rows.append(
                {
                    "family": "path",
                    "n": n,
                    "scaling": "a*n*2^sqrt(log2(n))",
                    "multiplier": f"{multiplier:.8g}",
                    "base_density": f"{base_density:.17g}",
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
                    "seed": seed,
                }
            )
            print(
                f"P_{n}: a={multiplier:g}, density={t/n:.4f}, "
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
            "python scripts/compare_path_stretched_scale.py "
            f"--n-values {args.n_values} --multipliers {args.multipliers} "
            f"--trials {args.trials} --seed-base {args.seed_base} "
            f"--output {args.output}"
        ),
        "model": "uniform weak compositions of t into n nonnegative parts",
        "predicate": "exact front-pruned path TreeStack recurrence",
        "status": "scale-discrimination experiment; not a theorem or promoted conjecture",
    }
    args.output.with_suffix(args.output.suffix + ".meta.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
