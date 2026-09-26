#!/usr/bin/env python3
"""Tabulate rigorous Session-4 spatial certificate parameters."""
from __future__ import annotations
import argparse,csv,json,math
from pathlib import Path
from prob_stack.product_spatial import spatial_front_certificate_in_segment,universal_runaway_probability_lower_bound

def main()->None:
    ap=argparse.ArgumentParser(); ap.add_argument('--levels',default='4,5,6,8,10,12,16'); ap.add_argument('--coefficient',type=float,default=1.0); ap.add_argument('--output',default='data/spatial_front_rigorous_bounds.csv'); args=ap.parse_args()
    rows=[]
    for L in [int(x) for x in args.levels.split(',') if x]:
      mean=2**L; log2n=(L/args.coefficient)**2; n=2**math.ceil(log2n)
      cert=spatial_front_certificate_in_segment(mean,n,n//2)
      log2N=math.log2(cert.disjoint_blocks) if cert.disjoint_blocks else -math.inf
      rows.append({
       'L':L,'mean':mean,'coefficient_c':args.coefficient,'log2_path_length':math.log2(n),
       'reset_steps':cert.reset_steps,'witness_steps':cert.witness_steps,'buffer_steps':cert.buffer_steps,
       'block_length':cert.block_length,'half_path_blocks':cert.disjoint_blocks,
       'witness_log2_probability':cert.witness_log2_probability,'buffer_log2_probability':cert.buffer_log2_probability,
       'per_block_log2_probability_lower':cert.per_block_log2_probability_lower,
       'log2_N_times_per_block_lower':log2N+cert.per_block_log2_probability_lower,
       'universal_buffer_constant_lower':universal_runaway_probability_lower_bound(),
      })
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('w',newline='') as f:
      w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    Path(str(out)+'.meta.json').write_text(json.dumps({'rigorous_formula_table':True,'levels':[r['L'] for r in rows],'coefficient_c':args.coefficient,'path_rule':'n=2^ceil((L/c)^2)'},indent=2)+"\n")
if __name__=='__main__':main()
