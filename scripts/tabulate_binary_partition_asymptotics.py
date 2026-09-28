#!/usr/bin/env python3
"""Emit exact Session 16 binary-partition asymptotic diagnostics as CSV."""
from __future__ import annotations

import argparse
import csv
from fractions import Fraction
from pathlib import Path
import sys

from prob_stack.binary_partition_asymptotics import (
    exact_diagnostic,
    low_amplification_regime,
    necessary_low_phase_regime,
    necessary_positive_entry_regime,
    positive_descent_regime,
)


def parse_levels(raw: str) -> list[int]:
    levels = [int(piece) for piece in raw.split(",") if piece.strip()]
    if not levels or any(level < 4 for level in levels):
        raise ValueError("levels must be comma-separated integers >=4")
    return levels


def parse_phases(raw: str) -> list[Fraction]:
    phases = [Fraction(piece.strip()) for piece in raw.split(",") if piece.strip()]
    if not phases or any(not (Fraction(1, 2) < phase <= 1) for phase in phases):
        raise ValueError("phases must lie in (1/2,1]")
    return phases


def rows(levels: list[int], phases: list[Fraction]):
    for level in levels:
        for phase in phases:
            mean = phase.numerator * (1 << level) // phase.denominator
            regime = positive_descent_regime(mean)
            if regime.level != level:
                raise ValueError(
                    f"phase {phase} at L={level} does not give exact requested level"
                )
            yield exact_diagnostic(regime)

        mean = 1 << level
        yield exact_diagnostic(low_amplification_regime(mean))
        for terminal in (0, 1):
            yield exact_diagnostic(
                necessary_positive_entry_regime(mean, terminal)
            )
        for start in (0, 1):
            yield exact_diagnostic(necessary_low_phase_regime(mean, start))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--levels", default="6,8,10,12,14")
    parser.add_argument("--phases", default="9/16,3/4,1")
    parser.add_argument("--output")
    args = parser.parse_args()

    levels = parse_levels(args.levels)
    phases = parse_phases(args.phases)
    destination = Path(args.output) if args.output else None
    handle = destination.open("w", newline="") if destination else sys.stdout
    try:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "family",
                "L",
                "theta",
                "k",
                "B",
                "lambda",
                "cutoff_exact",
                "tail_factor_bound",
                "exact_count",
                "unrestricted_count",
                "log2_count",
                "residual_after_half_L2_minus_LlogL",
                "linear_coefficient",
                "residual_after_linear",
            ]
        )
        for diagnostic in rows(levels, phases):
            regime = diagnostic.regime
            writer.writerow(
                [
                    regime.family,
                    regime.level,
                    "" if regime.theta is None else f"{regime.theta:.12g}",
                    regime.steps,
                    regime.budget,
                    f"{regime.scale:.12g}",
                    int(regime.cutoff_is_exact),
                    regime.tail_factor_bound,
                    diagnostic.exact_count,
                    diagnostic.unrestricted_count,
                    f"{diagnostic.log2_count:.12f}",
                    f"{diagnostic.residual_after_quadratic_and_llogl:.12f}",
                    f"{diagnostic.linear_coefficient:.12f}",
                    f"{diagnostic.residual_after_linear_term:.12f}",
                ]
            )
    finally:
        if destination:
            handle.close()


if __name__ == "__main__":
    main()
