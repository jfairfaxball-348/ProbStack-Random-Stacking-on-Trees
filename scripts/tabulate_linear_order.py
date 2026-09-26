from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

from prob_stack.linear_order import (
    certified_front_beta,
    colored_slack_count_exact,
    dyadic_phase,
    low_phase_linear_coefficient,
    one_sided_beta,
    positive_entry_count_exact,
    positive_entry_linear_coefficient,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--levels", default="6,8,10,12")
    parser.add_argument("--phase-numerators", default="9,12,14,16")
    parser.add_argument("--phase-denominator", type=int, default=16)
    parser.add_argument("--entry-step-offset", type=int, default=0)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    levels = [int(item) for item in args.levels.split(",") if item]
    numerators = [
        int(item) for item in args.phase_numerators.split(",") if item
    ]
    rows = []
    for level in levels:
        scale = 2**level
        for numerator in numerators:
            mean = max(
                2 ** (level - 1) + 1,
                numerator * scale // args.phase_denominator,
            )
            actual_level, theta = dyadic_phase(mean)
            if actual_level != level:
                continue
            steps = level + args.entry_step_offset
            for terminal in (0, 1):
                count = positive_entry_count_exact(mean, steps, terminal)
                lower_count = None
                lower_ratio = None
                if args.entry_step_offset == 0 and level >= 4:
                    active_steps = level - 2
                    slack_budget = (terminal + 3) * (2**level) - 3 - mean
                    lower_count = colored_slack_count_exact(
                        active_steps, slack_budget
                    )
                    lower_ratio = lower_count / count if count else None
                rows.append(
                    {
                        "L": level,
                        "mean": mean,
                        "theta": theta,
                        "entry_steps": steps,
                        "terminal": terminal,
                        "exact_positive_entry_count": str(count),
                        "log2_exact_positive_entry_count": (
                            math.log2(count) if count else float("-inf")
                        ),
                        "exact_s0_colored_lower_count": (
                            str(lower_count)
                            if lower_count is not None
                            else None
                        ),
                        "s0_colored_lower_fraction": lower_ratio,
                        "positive_linear_coefficient": (
                            positive_entry_linear_coefficient(theta, terminal)
                        ),
                        "matching_low_linear_coefficient": (
                            low_phase_linear_coefficient(theta, terminal)
                        ),
                        "q_beta_theta": one_sided_beta(theta),
                        "certified_front_beta_theta": (
                            certified_front_beta(theta)
                        ),
                        "local_to_certificate_beta_gap": math.log2(3.0),
                        "global_center_gap": 0.5 * math.log2(3.0),
                    }
                )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
