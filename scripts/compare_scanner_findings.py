#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "results" / "raw"
OUT = ROOT / "results"

PAIRS = {
    "NC001_COMMENT_ONLY": "B001",
    "NC002_SEQUENCE_STYLE": "B002",
    "NC003_QUOTE_STYLE": "B003",
    "NC004_EVENT_KEY_ORDER": "B004",
    "NC005_EXPLICIT_SUCCESS": "B005",
}
TOOLS = ("actionlint", "zizmor", "poutine")

def load_json(path: Path):
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    if not text:
        return []
    return json.loads(text)

def normalize(tool: str, data):
    if tool == "poutine":
        findings = data.get("findings", []) if isinstance(data, dict) else []
    else:
        findings = data if isinstance(data, list) else data.get("findings", [])

    normalized = []
    for finding in findings:
        if not isinstance(finding, dict):
            normalized.append(str(finding))
            continue

        if tool == "actionlint":
            normalized.append({
                "kind": finding.get("kind"),
                "message": finding.get("message"),
            })
        elif tool == "zizmor":
            normalized.append({
                "audit": finding.get("audit") or finding.get("ident"),
                "description": finding.get("desc") or finding.get("description"),
                "severity": finding.get("severity"),
            })
        elif tool == "poutine":
            normalized.append({
                "rule_id": (
                    finding.get("rule_id")
                    or finding.get("rule")
                    or finding.get("id")
                ),
                "message": finding.get("message") or finding.get("description"),
                "level": finding.get("level") or finding.get("severity"),
            })

    return sorted(
        normalized,
        key=lambda item: json.dumps(item, sort_keys=True),
    )

comparisons = []
all_invariant = True

for control_id, baseline_id in PAIRS.items():
    for tool in TOOLS:
        base_path = RAW / baseline_id / f"{tool}.json"
        control_path = RAW / control_id / f"{tool}.json"
        base_norm = normalize(tool, load_json(base_path))
        control_norm = normalize(tool, load_json(control_path))
        invariant = base_norm == control_norm
        all_invariant = all_invariant and invariant
        comparisons.append({
            "control_id": control_id,
            "source_baseline": baseline_id,
            "tool": tool,
            "baseline_finding_count": len(base_norm),
            "control_finding_count": len(control_norm),
            "normalized_findings_invariant": invariant,
            "baseline_normalized_findings": base_norm,
            "control_normalized_findings": control_norm,
        })

result = {
    "rq6_oracle": "Semantics-preserving controls should retain identical normalized findings.",
    "all_pair_tool_comparisons_invariant": all_invariant,
    "comparison_count": len(comparisons),
    "comparisons": comparisons,
}
(OUT / "rq6_scanner_invariance.json").write_text(
    json.dumps(result, indent=2) + "\n",
    encoding="utf-8",
)
print(json.dumps(result, indent=2))
sys.exit(0 if all_invariant else 1)
