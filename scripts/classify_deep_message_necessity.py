#!/usr/bin/env python3
"""Exact bounded check of the Session 5 deep-message necessity theorem."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from prob_stack.configurations import weak_compositions
from prob_stack.path_score import (
    left_incoming_messages,
    path_scores,
    right_incoming_messages,
)
from prob_stack.soft_front import forced_message_threshold
from prob_stack.tree_score import EMPTY


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=10)
    parser.add_argument("--max-total", type=int, default=10)
    parser.add_argument(
        "--output",
        default="data/deep_message_necessity_exact.csv",
    )
    args = parser.parse_args()

    rows = []
    for n in range(2, args.max_order + 1):
        for t in range(1, args.max_total + 1):
            threshold = forced_message_threshold(n, t)
            nonstackable = 0
            tight = 0
            minimum_margin = None
            example = ""

            for configuration in weak_compositions(t, n):
                if max(path_scores(configuration)) > 0:
                    continue
                nonstackable += 1
                messages = (
                    left_incoming_messages(configuration)
                    + right_incoming_messages(configuration)
                )
                minimum = min(
                    message
                    for message in messages
                    if message is not EMPTY
                )
                margin = (-minimum) - threshold
                if minimum_margin is None or margin < minimum_margin:
                    minimum_margin = margin
                    example = repr(configuration)
                tight += margin == 0

            rows.append(
                {
                    "n": n,
                    "t": t,
                    "forced_threshold": threshold,
                    "nonstackable": nonstackable,
                    "tight_examples": tight,
                    "minimum_margin": (
                        minimum_margin if minimum_margin is not None else ""
                    ),
                    "example_at_minimum": example,
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
                "exact": True,
                "max_order": args.max_order,
                "max_total": args.max_total,
                "statistic": (
                    "minimum directed message among nonstackable paths "
                    "compared with the proved forced threshold"
                ),
                "purpose": (
                    "bounded exhaustive validation and tightness diagnostics "
                    "for the Session 5 deep-message necessity theorem"
                ),
            },
            indent=2,
        )
        + "\n"
    )


if __name__ == "__main__":
    main()
