#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path

from prob_stack.regeneration import (
    absolute_regeneration_lower_bound,
    regeneration_interval,
    worst_case_regeneration_probability,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--means", default="16,17,24,32,48,64,96,128,256")
    parser.add_argument("--output", default="data/regeneration_exact.csv")
    args = parser.parse_args()
    means = [int(x) for x in args.means.split(",") if x]
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "mean",
                "worst_message",
                "occupancy_lower",
                "occupancy_upper",
                "probability_numerator",
                "probability_denominator",
                "probability_float",
                "absolute_lower_bound",
            ],
        )
        writer.writeheader()
        for mean in means:
            message = -mean + 1
            lower, upper = regeneration_interval(mean, message)
            probability = worst_case_regeneration_probability(mean)
            writer.writerow(
                {
                    "mean": mean,
                    "worst_message": message,
                    "occupancy_lower": lower,
                    "occupancy_upper": upper,
                    "probability_numerator": probability.numerator,
                    "probability_denominator": probability.denominator,
                    "probability_float": f"{float(probability):.15g}",
                    "absolute_lower_bound": f"{absolute_regeneration_lower_bound():.15g}",
                }
            )


if __name__ == "__main__":
    main()
