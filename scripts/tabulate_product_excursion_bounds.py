#!/usr/bin/env python3
"""Tabulate rigorous finite-block product-law deep-deficit bounds."""
from __future__ import annotations

import argparse
import csv
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from prob_stack.product_chain import canonical_deep_deficit_witness, finite_block_upper_log2_bound


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
    parser.add_argument("--levels", default="8,10,12,16,20,30,40")
    parser.add_argument(
        "--output", type=Path, default=Path("data/product_excursion_rigorous_bounds.csv")
    )
    args = parser.parse_args()

    rows: list[dict[str, object]] = []
    for level in parse_ints(args.levels):
        mean = 2**level
        witness = canonical_deep_deficit_witness(mean)
        lower_log2 = witness.log2_probability
        upper_log2 = finite_block_upper_log2_bound(mean)
        rows.append(
            {
                "log2_mean": level,
                "mean": mean,
                "horizon": 4 * level,
                "witness_horizon": witness.horizon,
                "log2_lower_bound": f"{lower_log2:.17g}",
                "log2_upper_bound": f"{upper_log2:.17g}",
                "lower_cost_over_L2": f"{-lower_log2/(level*level):.17g}",
                "upper_cost_over_L2": f"{-upper_log2/(level*level):.17g}",
            }
        )
        print(
            f"L={level}: lower cost/L^2={-lower_log2/(level*level):.8g}; "
            f"upper cost/L^2={-upper_log2/(level*level):.8g}"
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
            "python scripts/tabulate_product_excursion_bounds.py "
            f"--levels {args.levels} --output {args.output}"
        ),
        "quantity": "q_mu = P_m(hit M<=-mu within 4L steps), uniformly for m in [mu,2mu], L=ceil(log2 mu)",
        "lower_bound": "explicit deterministic cap witness",
        "upper_bound": "first-entry plus final-negative-run union bound",
        "status": "rigorous finite-parameter bounds implemented from Session 3 proof",
    }
    args.output.with_suffix(args.output.suffix + ".meta.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
