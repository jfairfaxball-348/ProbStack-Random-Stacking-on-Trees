#!/usr/bin/env python3
"""Monte Carlo for immediate conversion of M=-mu into a whole-path-strength deficit.

Statistic is defined before sampling: starting at integer message M_0=-mu,
run the exact product-geometric chain until either (i) Z=3-M reaches
2*n*mu+3, or (ii) an update has M+X>1 and therefore exits the low phase.
"""
from __future__ import annotations
import argparse, csv, json, math, random
from pathlib import Path
from prob_stack.tree_score import transfer


def geometric_sample(mean: int, rng: random.Random) -> int:
    ratio = mean / (mean + 1.0)
    return int(math.log1p(-rng.random()) / math.log(ratio))


def wilson(successes: int, trials: int, z: float = 1.959963984540054) -> tuple[float,float]:
    phat=successes/trials; den=1+z*z/trials
    ctr=(phat+z*z/(2*trials))/den
    rad=z*math.sqrt(phat*(1-phat)/trials+z*z/(4*trials*trials))/den
    return ctr-rad,ctr+rad


def simulate(mean: int, path_length: int, trials: int, seed: int) -> dict[str,object]:
    rng=random.Random(seed); target=2*path_length*mean+3
    reached=rescued=total_steps=0
    for _ in range(trials):
        message=-mean
        for step in range(100000):
            if 3-message >= target:
                reached += 1; total_steps += step; break
            occupancy=geometric_sample(mean,rng)
            if message+occupancy > 1:
                rescued += 1; break
            message=transfer(message+occupancy)
        else:
            raise RuntimeError("simulation step limit exceeded")
    lo,hi=wilson(reached,trials)
    return {
        "mean":mean,"log2_mean_level":math.ceil(math.log2(mean)),"path_length":path_length,
        "trials":trials,"seed":seed,"front_strength_hits":reached,"rescues":rescued,
        "estimate":reached/trials,"wilson95_low":lo,"wilson95_high":hi,
        "mean_steps_given_hit":total_steps/reached if reached else math.nan,
    }


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--means",default="16,32,64,128,256")
    ap.add_argument("--trials",type=int,default=100000)
    ap.add_argument("--seed-base",type=int,default=2026092700)
    ap.add_argument("--output",default="data/seed_to_front_mc.csv")
    args=ap.parse_args()
    means=[int(x) for x in args.means.split(',') if x]
    rows=[]
    for mean in means:
        L=math.ceil(math.log2(mean)); n=2**(L*L); seed=args.seed_base+mean
        rows.append(simulate(mean,n,args.trials,seed))
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    meta={
        "statistic":"P_{M0=-mu}[reach deficit Z>=2*n*mu+3 before first exit from low phase]",
        "path_length":"n=2^(ceil(log2(mu))^2)","means":means,"trials":args.trials,
        "seed_base":args.seed_base,"seed_rule":"seed_base+mean",
        "purpose":"discriminate order-one seed-to-front conversion from an additional rare-event cost",
    }
    Path(str(out)+'.meta.json').write_text(json.dumps(meta,indent=2)+"\n")

if __name__=='__main__': main()
