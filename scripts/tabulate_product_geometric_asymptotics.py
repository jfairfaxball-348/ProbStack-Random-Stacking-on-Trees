#!/usr/bin/env python3
"""Emit Session 17 product-geometric dyadic-simplex diagnostics as CSV."""
from __future__ import annotations

import argparse
import csv
from fractions import Fraction
from pathlib import Path
import sys

from prob_stack.binary_partition_asymptotics import (
    low_amplification_regime,
    necessary_low_phase_regime,
    necessary_positive_entry_regime,
    positive_descent_regime,
)
from prob_stack.product_geometric_asymptotics import (
    local_excursion_beta,
    probability_diagnostic,
    sharp_seed_beta,
)


def parse_levels(raw: str) -> list[int]:
    levels = [int(piece.strip()) for piece in raw.split(",") if piece.strip()]
    if not levels or any(level < 4 for level in levels):
        raise ValueError("levels must be comma-separated integers >=4")
    return levels


def parse_phases(raw: str) -> list[Fraction]:
    phases = [Fraction(piece.strip()) for piece in raw.split(",") if piece.strip()]
    if not phases or any(not (Fraction(1, 2) < phase <= 1) for phase in phases):
        raise ValueError("phases must lie in (1/2,1]")
    return phases


def mean_at(level: int, phase: Fraction) -> int:
    numerator = phase.numerator * (1 << level)
    if numerator % phase.denominator:
        raise ValueError(f"phase {phase} is not integral at L={level}")
    return numerator // phase.denominator


def block_rows(levels: list[int], phases: list[Fraction], exact_through: int):
    for level in levels:
        for phase in phases:
            mean = mean_at(level, phase)
            exact = level <= exact_through
            regimes = [
                (positive_descent_regime(mean), False),
                (low_amplification_regime(mean), True),
                (necessary_positive_entry_regime(mean, 0), False),
                (necessary_positive_entry_regime(mean, 1), False),
                (necessary_low_phase_regime(mean, 0), True),
                (necessary_low_phase_regime(mean, 1), True),
            ]
            diagnostics = {}
            for regime, reverse in regimes:
                diagnostic = probability_diagnostic(
                    mean,
                    regime,
                    reverse=reverse,
                    exact_fraction=exact,
                )
                diagnostics[regime.family] = diagnostic
                yield {
                    "family": regime.family,
                    "L": level,
                    "theta": float(phase),
                    "mean": mean,
                    "k": regime.steps,
                    "B": regime.budget,
                    "lambda": regime.scale,
                    "count": diagnostic.count,
                    "log2_count": diagnostic.log2_count,
                    "log2_p_factor": diagnostic.log2_p_factor,
                    "tilt_log2": diagnostic.tilt_log2,
                    "tilt_lower_bound": diagnostic.tilt_lower_bound,
                    "neg_log2_probability": -diagnostic.log2_probability,
                    "linear_coefficient": diagnostic.linear_coefficient,
                    "residual_after_linear": (
                        diagnostic.residual_after_probability_linear_term
                    ),
                    "exact_fraction_checked": int(
                        diagnostic.exact_fraction_checked
                    ),
                    "exact_neg_log2_probability": (
                        ""
                        if diagnostic.exact_log2_probability is None
                        else -diagnostic.exact_log2_probability
                    ),
                    "optimized_local_beta": local_excursion_beta(float(phase)),
                }

            positive = diagnostics["positive_descent"]
            low = diagnostics["low_amplification"]
            beta = sharp_seed_beta(float(phase))
            seed_cost = -positive.log2_probability - low.log2_probability
            seed_unweighted_cost = -(
                positive.log2_p_factor
                + positive.log2_count
                + low.log2_p_factor
                + low.log2_count
            )
            seed_tilt = positive.tilt_log2 + low.tilt_log2
            leading = (
                level**2
                + 2 * level * __import__("math").log2(level)
                + beta * level
            )
            exact_seed = ""
            if (
                positive.exact_log2_probability is not None
                and low.exact_log2_probability is not None
            ):
                exact_seed = -(
                    positive.exact_log2_probability
                    + low.exact_log2_probability
                )
            yield {
                "family": "sharp_seed",
                "L": level,
                "theta": float(phase),
                "mean": mean,
                "k": 2 * level + 2,
                "B": positive.budget + low.budget,
                "lambda": "",
                "count": positive.count * low.count,
                "log2_count": positive.log2_count + low.log2_count,
                "log2_p_factor": positive.log2_p_factor + low.log2_p_factor,
                "tilt_log2": seed_tilt,
                "tilt_lower_bound": (
                    positive.tilt_lower_bound + low.tilt_lower_bound
                ),
                "neg_log2_probability": seed_cost,
                "linear_coefficient": beta,
                "residual_after_linear": seed_cost - leading,
                "exact_fraction_checked": int(bool(exact_seed != "")),
                "exact_neg_log2_probability": exact_seed,
                "optimized_local_beta": local_excursion_beta(float(phase)),
                "unweighted_neg_log2_probability": seed_unweighted_cost,
            }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--levels", default="4,6,8,10,12")
    parser.add_argument("--phases", default="9/16,3/4,1")
    parser.add_argument("--exact-through-level", type=int, default=8)
    parser.add_argument("--output")
    args = parser.parse_args()

    levels = parse_levels(args.levels)
    phases = parse_phases(args.phases)
    rows = list(block_rows(levels, phases, args.exact_through_level))

    fields = [
        "family",
        "L",
        "theta",
        "mean",
        "k",
        "B",
        "lambda",
        "count",
        "log2_count",
        "log2_p_factor",
        "tilt_log2",
        "tilt_lower_bound",
        "neg_log2_probability",
        "linear_coefficient",
        "residual_after_linear",
        "exact_fraction_checked",
        "exact_neg_log2_probability",
        "optimized_local_beta",
        "unweighted_neg_log2_probability",
    ]

    destination = Path(args.output) if args.output else None
    handle = destination.open("w", newline="") if destination else sys.stdout
    try:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    finally:
        if destination:
            handle.close()


if __name__ == "__main__":
    main()
