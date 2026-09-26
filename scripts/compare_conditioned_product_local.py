#!/usr/bin/env python3
"""Exact conditioned-vs-product comparison for the canonical local witness."""
from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from prob_stack.product_chain import (
    canonical_deep_deficit_witness,
    conditioned_cap_event_probability,
    conditioning_log_ratio_bound,
    product_cap_event_probability_nt,
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mean", type=int, default=16)
    parser.add_argument("--n-values", default="100,500,2000,10000")
    parser.add_argument(
        "--output", type=Path, default=Path("data/conditioned_product_local_exact.csv")
    )
    args = parser.parse_args()

    witness = canonical_deep_deficit_witness(args.mean)
    caps = witness.all_caps
    block_size = len(caps)
    max_block_mass = sum(caps)
    rows: list[dict[str, object]] = []

    for n in parse_ints(args.n_values):
        t = n * args.mean
        conditioned = conditioned_cap_event_probability(n, t, caps)
        product_probability = product_cap_event_probability_nt(n, t, caps)
        ratio = conditioned / product_probability
        delta = conditioning_log_ratio_bound(n, t, block_size, max_block_mass)
        rows.append(
            {
                "mean": args.mean,
                "n": n,
                "t": t,
                "block_size": block_size,
                "max_block_mass": max_block_mass,
                "conditioned_probability": f"{float(conditioned):.17g}",
                "product_probability": f"{float(product_probability):.17g}",
                "ratio_conditioned_to_product": f"{float(ratio):.17g}",
                "log_ratio": f"{math.log(float(ratio)):.17g}",
                "rigorous_abs_log_ratio_bound": f"{delta:.17g}",
            }
        )
        print(
            f"n={n}: ratio={float(ratio):.8g}; "
            f"log ratio={math.log(float(ratio)):.8g}; bound={delta:.8g}"
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
            "python scripts/compare_conditioned_product_local.py "
            f"--mean {args.mean} --n-values {args.n_values} --output {args.output}"
        ),
        "conditioned_model": "uniform weak compositions of t=n*mean into n parts",
        "product_model": "iid geometric with mean t/n",
        "event": "canonical deterministic-cap deep-deficit witness on the first block",
        "exactness": "both event probabilities are exact rational calculations; CSV uses float presentation",
        "caps": list(caps),
    }
    args.output.with_suffix(args.output.suffix + ".meta.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
