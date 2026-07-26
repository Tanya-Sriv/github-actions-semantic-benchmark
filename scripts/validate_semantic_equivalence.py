#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
BASELINES = ROOT / "benchmark" / "baselines"
CONTROLS = ROOT / "benchmark" / "negative_controls"

PAIRS = {
    "NC001_COMMENT_ONLY": "B001",
    "NC002_SEQUENCE_STYLE": "B002",
    "NC003_QUOTE_STYLE": "B003",
    "NC004_EVENT_KEY_ORDER": "B004",
    "NC005_EXPLICIT_SUCCESS": "B005",
}

def load_yaml(path: Path):
    # BaseLoader keeps values as strings while still normalizing YAML syntax,
    # comments, quote style, sequence style, and mapping order.
    return yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)

def normalize_explicit_success(obj):
    if isinstance(obj, dict):
        result = {}
        for key, value in obj.items():
            if key == "jobs" and isinstance(value, dict):
                jobs = {}
                for job_name, job in value.items():
                    if isinstance(job, dict):
                        job = dict(job)
                        condition = job.get("if")
                        if condition in ("${{ success() }}", "success()"):
                            job.pop("if", None)
                    jobs[job_name] = normalize_explicit_success(job)
                result[key] = jobs
            else:
                result[key] = normalize_explicit_success(value)
        return result
    if isinstance(obj, list):
        return [normalize_explicit_success(v) for v in obj]
    return obj

def workflows(root: Path):
    return sorted(
        p for p in (root / "workflows").glob("*.y*ml") if p.is_file()
    )

records = []
all_equal = True

for control_id, baseline_id in PAIRS.items():
    base_files = workflows(BASELINES / baseline_id)
    control_files = workflows(CONTROLS / control_id)
    if [p.name for p in base_files] != [p.name for p in control_files]:
        raise SystemExit(f"Workflow filename mismatch for {control_id}")

    for base_path, control_path in zip(base_files, control_files):
        base_obj = load_yaml(base_path)
        control_obj = load_yaml(control_path)

        if control_id == "NC005_EXPLICIT_SUCCESS":
            control_obj = normalize_explicit_success(control_obj)

        equal = base_obj == control_obj
        all_equal = all_equal and equal
        records.append({
            "control_id": control_id,
            "source_baseline": baseline_id,
            "workflow_file": base_path.name,
            "equivalent": equal,
            "comparison": (
                "normalized operational equality"
                if control_id == "NC005_EXPLICIT_SUCCESS"
                else "parsed-object equality"
            ),
        })

result = {
    "all_controls_equivalent": all_equal,
    "records": records,
}
output = ROOT / "results" / "semantic_equivalence_validation.json"
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
sys.exit(0 if all_equal else 1)
