#!/usr/bin/env python3
"""Monte Carlo path estimates using *uniform weak-composition* sampling."""

from __future__ import annotations

import argparse

from prob_stack.families import path_tree
from prob_stack.sampling import sample_stackability


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int)
    parser.add_argument("t", type=int)
    parser.add_argument("--trials", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=20260926)
    args = parser.parse_args()
    result = sample_stackability(path_tree(args.n), args.t, args.trials, args.seed)
    print(
        f"P_{args.n}, t={args.t}: {result.successes}/{result.trials} "
        f"= {result.estimate:.8f} (seed={result.seed})"
    )


if __name__ == "__main__":
    main()
