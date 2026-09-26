#!/usr/bin/env python3
"""Exhaustively compare direct reachability with TreeStack scores on small trees."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from prob_stack.configurations import weak_compositions
from prob_stack.families import all_labeled_trees
from prob_stack.reachability import direct_stackability_oracle, direct_target_oracle
from prob_stack.tree_score import scores, structurally_stackable


@dataclass
class Counts:
    trees: int = 0
    configurations: int = 0
    rooted_cases: int = 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=5)
    parser.add_argument("--max-total", type=int, default=5)
    args = parser.parse_args()
    counts = Counts()
    for n in range(1, args.max_order + 1):
        for tree in all_labeled_trees(n):
            counts.trees += 1
            direct = direct_stackability_oracle(tree)
            rooted = [direct_target_oracle(tree, r) for r in range(n)]
            for t in range(args.max_total + 1):
                for c in weak_compositions(t, n):
                    counts.configurations += 1
                    score_values = scores(tree, c)
                    structural = any(x > 0 for x in score_values)
                    exact = direct(c)
                    if structural != exact:
                        raise SystemExit(
                            f"GLOBAL DISAGREEMENT tree={tree} t={t} c={c} "
                            f"direct={exact} structural={structural} scores={score_values}"
                        )
                    for r in range(n):
                        counts.rooted_cases += 1
                        exact_at = rooted[r](c)
                        structural_at = score_values[r] > 0
                        if exact_at != structural_at:
                            raise SystemExit(
                                f"ROOTED DISAGREEMENT tree={tree} t={t} c={c} root={r} "
                                f"direct={exact_at} structural={structural_at} score={score_values[r]}"
                            )
    print(
        f"validated {counts.trees} labeled trees, {counts.configurations} configurations, "
        f"{counts.rooted_cases} rooted cases; no disagreements"
    )


if __name__ == "__main__":
    main()
