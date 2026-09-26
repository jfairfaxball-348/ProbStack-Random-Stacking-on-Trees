from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

from prob_stack.second_order import (
    amplification_witness_parameters,
    descent_witness_parameters,
    dyadic_small_ball_probability_exact,
    finite_block_second_order_bounds,
    second_order_deep_message_cover,
    second_order_rate,
)


def _log2_fraction(value):
    return (
        math.log2(value.numerator)
        - math.log2(value.denominator)
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--levels",
        default="6,8,10,12,16,20,30,40,50",
    )
    parser.add_argument(
        "--exact-through-level",
        type=int,
        default=10,
    )
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    levels = [
        int(item)
        for item in args.levels.split(",")
        if item
    ]

    rows = []
    for level in levels:
        mean = 2**level
        bounds = finite_block_second_order_bounds(mean)
        cover = second_order_deep_message_cover(mean)

        exact_descent = None
        exact_amplification = None
        exact_witness = None
        if level <= args.exact_through_level:
            descent_steps, descent_budget = (
                descent_witness_parameters(mean)
            )
            amplification_steps, amplification_budget = (
                amplification_witness_parameters(mean)
            )
            descent_probability = (
                dyadic_small_ball_probability_exact(
                    mean,
                    descent_steps,
                    descent_budget,
                )
            )
            amplification_probability = (
                dyadic_small_ball_probability_exact(
                    mean,
                    amplification_steps,
                    amplification_budget,
                )
            )
            exact_descent = _log2_fraction(
                descent_probability
            )
            exact_amplification = _log2_fraction(
                amplification_probability
            )
            exact_witness = (
                exact_descent + exact_amplification
            )

        rows.append(
            {
                "L": level,
                "mean": f"2^{level}",
                "rate_L2_plus_2Llog2L": (
                    second_order_rate(level)
                ),
                "q_log2_lower": (
                    bounds.lower_log2_probability
                ),
                "q_log2_upper": (
                    bounds.upper_log2_probability
                ),
                "lower_rate_residual_per_L": (
                    bounds.lower_residual_per_level
                ),
                "upper_rate_residual_per_L": (
                    bounds.upper_residual_per_level
                ),
                "exact_descent_simplex_log2": (
                    exact_descent
                ),
                "exact_amplification_simplex_log2": (
                    exact_amplification
                ),
                "exact_two_block_witness_log2": (
                    exact_witness
                ),
                "supercritical_entry_upper_log2": (
                    cover.entry_log2_probability_upper
                ),
                "supercritical_low_upper_log2": (
                    cover.low_log2_probability_upper
                ),
                "supercritical_interior_upper_log2": (
                    cover.interior_log2_probability_upper
                ),
                "cluster_steps": cover.cluster_steps,
            }
        )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=rows[0].keys(),
        )
        writer.writeheader()
        writer.writerows(rows)

    metadata = {
        "exact_component_dp_through_level": (
            args.exact_through_level
        ),
        "analytic_bounds_rigorous": True,
        "levels": levels,
        "statistic": (
            "rigorous second-order bounds for q_mu "
            "and exact probabilities of the two "
            "simplex witness components at feasible "
            "levels"
        ),
        "seed": None,
        "interpretation": (
            "The theorem is analytic. Exact DP "
            "columns validate the weighted-budget "
            "components; they are not curve fits and "
            "do not estimate q_mu itself."
        ),
    }
    output.with_suffix(
        output.suffix + ".meta.json"
    ).write_text(
        json.dumps(metadata, indent=2) + "\n"
    )


if __name__ == "__main__":
    main()
