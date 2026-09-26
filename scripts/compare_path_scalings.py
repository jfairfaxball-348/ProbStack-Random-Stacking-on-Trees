#!/usr/bin/env python3
"""Monte Carlo grid for candidate path recovery scalings.

The default experiment samples at t = a n log_2 n for several n and a.  It
uses the uniform weak-composition sampler, not independent pebble placement.
The output records raw successes as well as estimates so uncertainty remains
auditable.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from prob_stack.families import path_tree
from prob_stack.sampling import sample_stackability


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
    parser.add_argument("--n-values", default="40,80,160,320,640")
    parser.add_argument("--scaling", choices=("nlog2", "linear"), default="nlog2")
    parser.add_argument("--multipliers", default="0.55,0.65,0.75,0.85,1.00")
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--seed-base", type=int, default=2026092600)
    parser.add_argument("--output", type=Path, default=Path("data/path_recovery_scaling_mc.csv"))
    args = parser.parse_args()
    ns = parse_ints(args.n_values)
    multipliers = parse_floats(args.multipliers)
    if not ns or not multipliers or min(ns) < 2 or args.trials <= 0:
        raise SystemExit("invalid experiment parameters")

    rows: list[dict[str, object]] = []
    for n in ns:
        tree = path_tree(n)
        for a in multipliers:
            if args.scaling == "nlog2":
                t = round(a * n * math.log2(n))
                scaling_label = "a*n*log2(n)"
            else:
                t = round(a * n)
                scaling_label = "a*n"
            # Stable deterministic seed for each grid point.
            seed = args.seed_base + n * 10_000 + round(a * 1_000)
            result = sample_stackability(tree, t, args.trials, seed)
            rows.append(
                {
                    "family": "path",
                    "n": n,
                    "scaling": scaling_label,
                    "multiplier": f"{a:.8g}",
                    "t": t,
                    "trials": result.trials,
                    "successes": result.successes,
                    "estimate": f"{result.estimate:.17g}",
                    "seed": seed,
                }
            )
            print(f"P_{n}: a={a:g}, t={t}, {result.successes}/{result.trials}={result.estimate:.4f}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    metadata = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_commit(),
        "command": (
            "python scripts/compare_path_scalings.py "
            f"--n-values {args.n_values} --scaling {args.scaling} --multipliers {args.multipliers} "
            f"--trials {args.trials} --seed-base {args.seed_base} --output {args.output}"
        ),
        "model": "uniform weak compositions of t into n nonnegative parts",
        "predicate": "TreeStack structural score evaluator, cross-validated against direct legal reachability on bounded cases",
        "parameters": {
            "n_values": ns,
            "scaling": args.scaling,
            "multipliers": multipliers,
            "trials": args.trials,
            "seed_base": args.seed_base,
        },
    }
    args.output.with_suffix(args.output.suffix + ".meta.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
