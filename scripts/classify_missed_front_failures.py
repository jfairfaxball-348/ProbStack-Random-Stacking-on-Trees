#!/usr/bin/env python3
"""Exact catalogue of nonstackable paths missed by front overlap."""
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
from prob_stack.configurations import weak_compositions
from prob_stack.path_score import fronts_certify_nonstackability,irreversible_deficit_fronts,path_scores,path_structurally_stackable

def main()->None:
    ap=argparse.ArgumentParser(); ap.add_argument('--max-order',type=int,default=10); ap.add_argument('--max-total',type=int,default=8); ap.add_argument('--output',default='data/missed_front_small_exact.csv'); args=ap.parse_args()
    rows=[]
    for n in range(2,args.max_order+1):
      for t in range(1,args.max_total+1):
        total_fail=missed=max_zero=max_negative=missing_front=0; gap_counts={}
        max_gap=-1; max_gap_example=None
        for c in weak_compositions(t,n):
          if path_structurally_stackable(c): continue
          total_fail+=1
          if fronts_certify_nonstackability(c): continue
          missed+=1; mx=max(path_scores(c)); max_zero += mx==0; max_negative += mx<0
          lf,rf=irreversible_deficit_fronts(c)
          if lf is None or rf is None:
            missing_front+=1; continue
          gap=lf-rf-1; gap_counts[gap]=gap_counts.get(gap,0)+1
          if gap>max_gap: max_gap=gap; max_gap_example=c
        rows.append({
          'n':n,'t':t,'nonstackable':total_fail,'missed_by_front_overlap':missed,
          'missed_max_score_zero':max_zero,'missed_max_score_negative':max_negative,
          'missed_missing_one_sided_front':missing_front,'max_uncovered_gap':max_gap,
          'max_gap_example':repr(max_gap_example) if max_gap_example is not None else '',
          'gap_histogram':json.dumps(gap_counts, sort_keys=True),
        })
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('w',newline='') as f:
      w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    Path(str(out)+'.meta.json').write_text(json.dumps({
      'exact':True,'max_order':args.max_order,'max_total':args.max_total,
      'classification':'nonstackable but not certified by overlap of irreversible one-sided fronts',
      'purpose':'test equality-only and bounded-gap explanations of missed failures'
    },indent=2)+"\n")
if __name__=='__main__': main()
