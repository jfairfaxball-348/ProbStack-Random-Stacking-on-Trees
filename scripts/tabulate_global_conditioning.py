#!/usr/bin/env python3
"""Tabulate Session 18 fixed-offset global balance diagnostics."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

from prob_stack.global_conditioning import global_balance_diagnostic


DEFAULT_LEVELS = "256,1024,4096,16384"
DEFAULT_OFFSETS = "-2,-1,-0.5,0.5,1,2"


def _parse_floats(spec: str) -> list[float]:
    return [float(part.strip()) for part in spec.split(",") if part.strip()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--levels", default=DEFAULT_LEVELS)
    parser.add_argument("--offsets", default=DEFAULT_OFFSETS)
    parser.add_argument(
        "--output",
        default="data/session18_global_balance.csv",
    )
    args = parser.parse_args()

    levels = _parse_floats(args.levels)
    offsets = _parse_floats(args.offsets)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for N in levels:
        for delta in offsets:
            d = global_balance_diagnostic(N, delta)
            rows.append(
                {
                    "log2_n": N,
                    "offset": delta,
                    "center": d.center,
                    "log2_mu": d.log2_mean,
                    "local_rate_main": d.local_rate_main,
                    "log2_n_times_local_hazard": d.log2_n_times_local_hazard,
                    "log2_spaced_block_hazard": d.log2_spaced_block_hazard,
                    "conditioning_cost_bits_main": d.conditioning_cost_bits_main,
                    "log2_spaced_hazard_to_conditioning_cost": (
                        d.log2_spaced_hazard_to_conditioning_cost
                    ),
                }
            )

    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
