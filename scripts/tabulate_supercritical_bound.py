#!/usr/bin/env python3
"""Evaluate the Session 5 conditioned supercritical union bound."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from prob_stack.supercritical import (
    conditioned_nonstackable_log2_upper,
    deep_message_cover,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--levels", default="20,30,40,50")
    parser.add_argument("--coefficients", default="1.05,1.10,1.25,1.50")
    parser.add_argument(
        "--output",
        default="data/supercritical_bound_table.csv",
    )
    args = parser.parse_args()

    levels = [int(value) for value in args.levels.split(",")]
    coefficients = [float(value) for value in args.coefficients.split(",")]
    rows = []

    for coefficient in coefficients:
        for level in levels:
            mean = 2**level
            log2_n = round((level / coefficient) ** 2)
            n = 2**log2_n
            cover = deep_message_cover(mean)
            rows.append(
                {
                    "coefficient": coefficient,
                    "L": level,
                    "mean": f"2^{level}",
                    "log2_n": log2_n,
                    "entry_log2_probability": cover.entry_log2_probability,
                    "low_log2_probability": cover.low_log2_probability,
                    "interior_log2_probability": (
                        cover.interior_log2_probability
                    ),
                    "cluster_steps": cover.cluster_steps,
                    "max_window_length": cover.max_window_length,
                    "conditioned_nonstackable_log2_upper": (
                        conditioned_nonstackable_log2_upper(mean, n)
                    ),
                }
            )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    Path(str(output) + ".meta.json").write_text(
        json.dumps(
            {
                "exact_formula_evaluation": True,
                "levels": levels,
                "coefficients": coefficients,
                "scale": "mean=2^L, log2(n)=round((L/c)^2)",
                "purpose": (
                    "finite evaluation of the proved Session 5 local-cap and "
                    "conditioning upper bound; floating values are diagnostics, "
                    "not the asymptotic proof"
                ),
            },
            indent=2,
        )
        + "\n"
    )


if __name__ == "__main__":
    main()
