#!/usr/bin/env python3
"""Targeted iid-geometric deep-deficit experiment for the path message chain.

For integer mean mu, start M_0=mu and run K=4*ceil(log2(mu)) exact TreeStack
updates with iid geometric occupancies of mean mu.  The recorded rare event is

    min_{1<=j<=K} M_j <= -mu.

This is a finite-block local hazard, not an eventual-hitting probability.
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

from prob_stack.tree_score import transfer


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "UNCOMMITTED"


def parse_ints(raw: str) -> list[int]:
    return [int(x) for x in raw.split(",") if x]


def wilson_interval(successes: int, trials: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if trials <= 0:
        return 0.0, 1.0
    phat = successes / trials
    denominator = 1 + z * z / trials
    center = (phat + z * z / (2 * trials)) / denominator
    half_width = z * math.sqrt(
        phat * (1 - phat) / trials + z * z / (4 * trials * trials)
    ) / denominator
    return center - half_width, center + half_width


def sample_geometric_integer_mean(mean: int, rng: Random) -> int:
    """Sample P[X=k]=(1/(1+mean))*(mean/(1+mean))^k."""
    log_ratio = math.log(mean / (mean + 1))
    return int(math.log1p(-rng.random()) / log_ratio)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--means", default="4,8,16")
    parser.add_argument("--trials", type=int, default=200000)
    parser.add_argument("--seed-base", type=int, default=2026092660)
    parser.add_argument(
        "--output", type=Path, default=Path("data/product_deep_excursion_mc.csv")
    )
    args = parser.parse_args()

    if args.trials <= 0:
        raise SystemExit("trials must be positive")

    rows: list[dict[str, object]] = []
    for mean in parse_ints(args.means):
        if mean <= 1:
            raise SystemExit("means must exceed 1")
        level = math.ceil(math.log2(mean))
        horizon = 4 * level
        seed = args.seed_base + mean * 1000
        rng = Random(seed)
        hits = entries = hit_step_sum = 0

        for _ in range(args.trials):
            message = mean
            entered_low = False
            for step in range(1, horizon + 1):
                occupancy = sample_geometric_integer_mean(mean, rng)
                message = transfer(message + occupancy)
                if message <= 1:
                    entered_low = True
                if message <= -mean:
                    hits += 1
                    hit_step_sum += step
                    break
            entries += entered_low

        low, high = wilson_interval(hits, args.trials)
        estimate = hits / args.trials
        normalized = -math.log2(estimate) / (level * level) if hits else math.inf
        rows.append(
            {
                "mean": mean,
                "log_level": level,
                "horizon": horizon,
                "trials": args.trials,
                "deep_hits": hits,
                "estimate": f"{estimate:.17g}",
                "wilson95_low": f"{low:.17g}",
                "wilson95_high": f"{high:.17g}",
                "entered_leq1": entries,
                "entry_estimate": f"{entries/args.trials:.17g}",
                "mean_hit_step": f"{(hit_step_sum/hits if hits else 0):.17g}",
                "normalized_cost_minus_log2_q_over_L2": (
                    f"{normalized:.17g}" if math.isfinite(normalized) else "inf"
                ),
                "seed": seed,
            }
        )
        print(
            f"mu={mean}: {hits}/{args.trials}={estimate:.6g}; "
            f"Wilson95=[{low:.6g},{high:.6g}]; normalized cost={normalized:.6g}"
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
            "python scripts/analyze_product_excursion.py "
            f"--means {args.means} --trials {args.trials} "
            f"--seed-base {args.seed_base} --output {args.output}"
        ),
        "model": "iid geometric occupancies with P[X=k]=p(1-p)^k and p=1/(1+mu)",
        "start_state": "M_0=mu",
        "event": "hit M_j <= -mu within 4*ceil(log2(mu)) steps",
        "purpose": "finite-block sanity check of the proved quadratic logarithmic rare-event rate; not used to fit an asymptotic constant",
        "uncertainty": "Wilson 95% binomial interval",
    }
    args.output.with_suffix(args.output.suffix + ".meta.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
