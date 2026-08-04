#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
PKG=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--scoring",default="scoring_blinded.csv");args=ap.parse_args()
    df=pd.read_csv(PKG/args.scoring)
    required={"provider","model","case_id","case_status","set","trial","full_oracle_match","baseline_equivalent_finding","unsupported_finding_count","adjudicated"}
    miss=required-set(df.columns)
    if miss:raise ValueError(f"Missing columns: {sorted(miss)}")
    d=df[df["adjudicated"].astype(str).str.lower().isin(["1","true","yes"])].copy()
    d["effective_tp"]=(d["full_oracle_match"]==1)&(d["baseline_equivalent_finding"]!=1)&(d["case_status"]=="mutant")
    mutants=d[d.case_status=="mutant"].groupby(["provider","model","set","case_id"])["effective_tp"].agg(["sum","count"]).reset_index()
    mutants["any_trial"]=(mutants["sum"]>=1).astype(int);mutants["majority"]=(mutants["sum"]>=2).astype(int);mutants["stable"]=(mutants["sum"]==mutants["count"]).astype(int)
    summary=mutants.groupby(["provider","model","set"])[["any_trial","majority","stable"]].agg(["sum","count"])
    summary.to_csv(PKG/"outputs/model_detection_summary.csv")
    baselines=d[d.case_status=="baseline"].groupby(["provider","model","set"])["unsupported_finding_count"].agg(["sum","mean","count"])
    baselines.to_csv(PKG/"outputs/baseline_false_positive_summary.csv")
    mutants.to_csv(PKG/"results_llm_baseline.csv",index=False)
    print(summary)
if __name__=="__main__":main()
