#!/usr/bin/env python3
"""Generate an exact path probability atlas under the uniform multiset model."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

from prob_stack.exact_probability import exact_probability
from prob_stack.families import path_tree

TREE_SCORE_PROVENANCE = "TreeStack main f4112f08d42a37c0941bf469ac124621b1f54f22"


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "UNCOMMITTED"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-n", type=int, default=2)
    parser.add_argument("--max-n", type=int, default=9)
    parser.add_argument("--max-t", type=int, default=12)
    parser.add_argument("--output", type=Path, default=Path("data/path_exact_atlas.csv"))
    args = parser.parse_args()
    if args.min_n < 1 or args.max_n < args.min_n or args.max_t < 0:
        raise SystemExit("invalid range")

    start = perf_counter()
    rows: list[dict[str, object]] = []
    for n in range(args.min_n, args.max_n + 1):
        tree = path_tree(n)
        for t in range(args.max_t + 1):
            result = exact_probability(tree, t)
            rows.append(
                {
                    "family": "path",
                    "n": n,
                    "t": t,
                    "total_configurations": result.total_configurations,
                    "stackable_configurations": result.stackable_configurations,
                    "nonstackable_configurations": result.nonstackable_configurations,
                    "probability": str(result.probability),
                    "probability_float": f"{float(result.probability):.17g}",
                }
            )
    elapsed = perf_counter() - start
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0])
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    metadata = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "command": f"python scripts/enumerate_paths.py --min-n {args.min_n} --max-n {args.max_n} --max-t {args.max_t} --output {args.output}",
        "git_commit": git_commit(),
        "tree_score_provenance": TREE_SCORE_PROVENANCE,
        "model": "uniform weak compositions of t into n nonnegative parts",
        "range": {"min_n": args.min_n, "max_n": args.max_n, "min_t": 0, "max_t": args.max_t},
        "rows": len(rows),
        "elapsed_seconds": elapsed,
    }
    meta_path = args.output.with_suffix(args.output.suffix + ".meta.json")
    meta_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(rows)} rows to {args.output} in {elapsed:.3f}s")


if __name__ == "__main__":
    main()
