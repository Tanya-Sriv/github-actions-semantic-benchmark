#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from pathlib import Path
import yaml
PKG=Path(__file__).resolve().parent
FORBIDDEN=["expected_violation","ground_truth_rationale","target_path","fault_class:","mutant_id:","oracle:"]
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--repo-root");ap.add_argument("--config",default="providers.yaml");args=ap.parse_args()
    errors=[]
    for f in ["llm_evaluation_protocol.md","prompt_template.txt","case_manifest.json","run_llm_baseline.py","summarize_results.py"]:
        if not (PKG/f).exists():errors.append(f"missing {f}")
    prompt=(PKG/"prompt_template.txt").read_text()
    for token in ["{intended_behavior}","{workflow_bundle}"]:
        if token not in prompt:errors.append(f"prompt missing {token}")
    prepared=PKG/"private/prepared_cases_private.json"
    if prepared.exists():
        cases=json.loads(prepared.read_text())
        if len([c for c in cases if c.get("case_status")=="mutant" and c.get("set")=="public"])!=18:errors.append("prepared public mutant count != 18")
        for c in cases:
            model_input=c.get("intended_behavior","")+c.get("workflow_bundle","")
            for x in FORBIDDEN:
                if x.lower() in model_input.lower():errors.append(f"possible oracle leak {x} in {c.get('source_case_id')}")
    else: errors.append("prepared cases absent: run prepare_cases.py")
    cfg=PKG/args.config
    if cfg.exists():
        data=yaml.safe_load(cfg.read_text())
        enabled=[p for p in data.get("providers",[]) if p.get("enabled")]
        if len(enabled)<3:errors.append("fewer than three enabled model configurations")
        if len({p["provider"] for p in enabled})<2:errors.append("enabled models use fewer than two providers")
        for p in enabled:
            if "FILL_" in p.get("model",""):errors.append(f"placeholder model id: {p['provider']}")
    else: errors.append(f"missing {args.config}; copy providers.example.yaml")
    if errors:
        print("VALIDATION FAILED")
        for e in errors:print("-",e)
        raise SystemExit(1)
    print("VALIDATION PASSED")
if __name__=="__main__":main()
