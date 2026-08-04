#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, glob, hashlib, json, re
from pathlib import Path
import yaml

ALLOWED_INTENT_KEYS = ("intended_behavior", "baseline_intent", "operational_intent", "intent")
FORBIDDEN_LEAK_KEYS = {"mutant_id","baseline_id","operator_id","fault_class","target_path","expected_violation","observable_symptom","ground_truth_rationale","oracle","rationale"}

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def extract_intended_behavior(oracle_path: Path) -> str:
    data = load_yaml(oracle_path)
    if not isinstance(data, dict):
        raise ValueError(f"Oracle is not a mapping: {oracle_path}")
    for key in ALLOWED_INTENT_KEYS:
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    # Search one level down only; never infer from expected violation or rationale.
    for value in data.values():
        if isinstance(value, dict):
            for key in ALLOWED_INTENT_KEYS:
                text = value.get(key)
                if isinstance(text, str) and text.strip():
                    return text.strip()
    raise ValueError(f"No neutral intended-behavior field found in {oracle_path}. Add one manually to private/case_intents.yaml before execution; do not derive it from the fault description.")

def bundle_files(repo: Path, rel_paths: list[str]) -> tuple[str,list[dict]]:
    chunks=[]; meta=[]
    for rel in sorted(rel_paths):
        p=repo/rel
        raw=p.read_bytes()
        text=raw.decode("utf-8")
        chunks.append(f"File: {Path(rel).name}\n```yaml\n{text.rstrip()}\n```")
        meta.append({"path":rel,"sha256":sha256_bytes(raw),"bytes":len(raw)})
    return "\n\n".join(chunks), meta

def expand_globs(repo: Path, patterns: list[str]) -> list[str]:
    out=[]
    for pattern in patterns:
        out.extend(str(Path(p).relative_to(repo)) for p in glob.glob(str(repo/pattern)))
    return sorted(set(out))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--package-root", default=str(Path(__file__).resolve().parent))
    args=ap.parse_args()
    repo=Path(args.repo_root).resolve(); pkg=Path(args.package_root).resolve()
    manifest=json.loads((pkg/"case_manifest.json").read_text())
    mutant_rows={}
    with (repo/"benchmark/mutant_manifest.csv").open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f): mutant_rows[row["mutant_id"]]=row
    prepared=[]
    # Baselines
    for b in manifest["baselines"]:
        paths=expand_globs(repo,b["workflow_globs"])
        if not paths: raise FileNotFoundError(f"No baseline workflows for {b['case_id']}")
        oracle_candidates=glob.glob(str(repo/b["oracle_source_glob"]))
        if not oracle_candidates: raise FileNotFoundError(f"No oracle source for {b['case_id']}")
        intent=extract_intended_behavior(Path(oracle_candidates[0]))
        bundle,files=bundle_files(repo,paths)
        prepared.append({"anonymous_case_id":b["case_id"],"source_case_id":b["case_id"],"case_status":"baseline","baseline_id":b["baseline_id"],"set":b["set"],"fault_class":"none","intended_behavior":intent,"workflow_bundle":bundle,"files":files})
    # Mutants
    for mutant_id, baseline_id, fault_class in manifest["mutants"]:
        row=mutant_rows.get(mutant_id)
        if not row: raise KeyError(f"Missing mutant manifest row: {mutant_id}")
        primary=row["workflow_file"]
        paths=[primary]
        # Cross-workflow cases require the companion workflow from the same mutant case directory.
        case_dir=(repo/primary).parent
        for p in sorted(case_dir.glob("*.y*ml")):
            rel=str(p.relative_to(repo))
            if rel not in paths: paths.append(rel)
        oracle=repo/row["oracle_file"]
        intent=extract_intended_behavior(oracle)
        bundle,files=bundle_files(repo,paths)
        prepared.append({"anonymous_case_id":mutant_id,"source_case_id":mutant_id,"case_status":"mutant","baseline_id":baseline_id,"set":"public","fault_class":fault_class,"intended_behavior":intent,"workflow_bundle":bundle,"files":files,"oracle_file":row["oracle_file"]})
    out=pkg/"private/prepared_cases_private.json"
    out.write_text(json.dumps(prepared,indent=2)+"\n",encoding="utf-8")
    print(f"Prepared {len(prepared)} cases -> {out}")

if __name__=="__main__": main()
