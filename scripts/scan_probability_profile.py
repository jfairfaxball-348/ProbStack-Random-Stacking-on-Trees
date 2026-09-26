#!/usr/bin/env python3
"""Summarize exact path profiles without fitting or promoting a conjecture."""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", nargs="?", type=Path, default=Path("data/path_exact_atlas.csv"))
    args = parser.parse_args()
    by_n: dict[int, list[tuple[int, Fraction]]] = {}
    with args.csv_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            by_n.setdefault(int(row["n"]), []).append((int(row["t"]), Fraction(row["probability"])))

    print("n  nontrivial minimum (t,p)   first recovery >=1/2   drops for t>=2")
    for n in sorted(by_n):
        profile = sorted(by_n[n])
        nontrivial = [(t, p) for t, p in profile if t >= 2]
        min_p = min(p for _, p in nontrivial)
        min_ts = [t for t, p in nontrivial if p == min_p]
        last_min_t = max(min_ts)
        recovery = next(((t, p) for t, p in nontrivial if t > last_min_t and p >= Fraction(1, 2)), None)
        drops = [
            (t0, t1)
            for (t0, p0), (t1, p1) in zip(nontrivial, nontrivial[1:])
            if p1 < p0
        ]
        print(
            f"{n:<2} ({min_ts[0]:>2},{float(min_p):.6f})"
            f"              {str(recovery):<20} {drops or '-'}"
        )


if __name__ == "__main__":
    main()
