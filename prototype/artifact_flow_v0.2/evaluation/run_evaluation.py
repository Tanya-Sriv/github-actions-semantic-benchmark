#!/usr/bin/env python3
from pathlib import Path
import argparse, csv, json, sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from artifact_flow.analyzer import analyze_workflow

EXPECTED = {
    "B001_AR01_001": {"AF001"},
    "B001_AR02_001": {"AF001"},
    "B001_AR03_001": {"AF001"},
    "B001_CF01_001": {"AF002"},
}

def workflow_files(directory: Path):
    return sorted(list(directory.glob("*.yml")) + list(directory.glob("*.yaml")))

def scan_case(files):
    findings=[]
    for path in files:
        report=analyze_workflow(path)
        for finding in report["findings"]:
            findings.append({**finding, "workflow_file": path.name})
    return findings

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--baselines", type=Path, default=Path("benchmark/baselines"))
    parser.add_argument("--mutants", type=Path, default=Path("benchmark/mutants"))
    parser.add_argument("--manifest", type=Path, default=Path("benchmark/mutant_manifest.csv"))
    parser.add_argument("--controls", type=Path, default=Path("benchmark/negative_controls"))
    parser.add_argument("--output-dir", type=Path, default=Path("artifact-flow-prototype/evaluation/results"))
    args=parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    cases=[]
    for baseline in sorted(args.baselines.glob("B*")):
        cases.append(("baseline", baseline.name, workflow_files(baseline/"workflows"), set()))

    manifest=list(csv.DictReader(args.manifest.open(encoding="utf-8")))
    for row in manifest:
        # Support both corpus layouts: manifest path relative to repo root, or nested mutant layout.
        declared=Path(row.get("workflow_file", ""))
        candidates=[declared, args.mutants/row["baseline_id"]/row["operator_id"]/row["mutant_id"] / "workflows" / Path(row["target_file"]).name]
        workflow=next((p for p in candidates if p.exists()), None)
        if workflow is None:
            raise FileNotFoundError(f"Could not locate workflow for {row['mutant_id']}: {candidates}")
        cases.append(("mutant", row["mutant_id"], [workflow], EXPECTED.get(row["mutant_id"], set())))

    for control in sorted(args.controls.glob("NC*")):
        cases.append(("negative_control", control.name, workflow_files(control/"workflows"), set()))

    rows=[]; all_findings=[]
    for case_type,case_id,files,oracle in cases:
        findings=scan_case(files)
        observed={f["rule_id"] for f in findings}
        rows.append({
            "case_type":case_type,
            "case_id":case_id,
            "workflow_files":";".join(str(p) for p in files),
            "expected_rules":";".join(sorted(oracle)),
            "observed_rules":";".join(sorted(observed)),
            "finding_count":len(findings),
            "oracle_match":observed==oracle,
        })
        for finding in findings:
            all_findings.append({"case_type":case_type,"case_id":case_id,**finding})

    tp=sum(r["case_type"]=="mutant" and bool(r["expected_rules"]) and bool(r["observed_rules"]) for r in rows)
    fn=sum(r["case_type"]=="mutant" and bool(r["expected_rules"]) and not bool(r["observed_rules"]) for r in rows)
    fp=sum(not bool(r["expected_rules"]) and bool(r["observed_rules"]) for r in rows)
    tn=sum(not bool(r["expected_rules"]) and not bool(r["observed_rules"]) for r in rows)
    summary={
        "prototype_version":"0.2",
        "corpus":{
            "baselines":sum(r["case_type"]=="baseline" for r in rows),
            "mutants":sum(r["case_type"]=="mutant" for r in rows),
            "negative_controls":sum(r["case_type"]=="negative_control" for r in rows),
            "total_cases":len(rows),
        },
        "artifact_flow_positive_mutants":4,
        "case_level_confusion_matrix":{"tp":tp,"fp":fp,"tn":tn,"fn":fn},
        "case_level_precision":tp/(tp+fp) if tp+fp else None,
        "case_level_recall":tp/(tp+fn) if tp+fn else None,
        "all_oracles_matched":all(r["oracle_match"] for r in rows),
        "rule_findings":{
            "AF001":sum(f["rule_id"]=="AF001" for f in all_findings),
            "AF002":sum(f["rule_id"]=="AF002" for f in all_findings),
        },
        "claim_boundary":"In-sample results on known artifact-flow mutants, clean baselines, and semantics-preserving controls; unseen holdout evaluation is required before general detector-accuracy claims."
    }
    with (args.output_dir/"evaluation-matrix.csv").open("w",newline="",encoding="utf-8") as handle:
        writer=csv.DictWriter(handle,fieldnames=rows[0].keys()); writer.writeheader(); writer.writerows(rows)
    (args.output_dir/"evaluation-summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    (args.output_dir/"findings.json").write_text(json.dumps(all_findings,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))
    return 0 if summary["all_oracles_matched"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
