#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

import yaml

UPLOAD_RE = re.compile(r"^actions/upload-artifact(?:@|$)")
DOWNLOAD_RE = re.compile(r"^actions/download-artifact(?:@|$)")
STATUS_FUNCS = ("success()", "failure()", "always()", "cancelled()")


@dataclass(frozen=True)
class ArtifactEndpoint:
    workflow: str
    job: str
    step_index: int
    step_id: str | None
    action: str
    artifact_name: str | None
    condition: str | None


@dataclass(frozen=True)
class Finding:
    rule_id: str
    message: str
    workflow: str
    consumer_job: str
    consumer_step_index: int
    artifact_name: str | None
    producer_jobs: list[str]
    confidence: str
    evidence: dict[str, Any]


def load_workflow(path: Path) -> dict[str, Any]:
    data = yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    if not isinstance(data, dict):
        raise ValueError(f"Workflow root must be a mapping: {path}")
    return data


def normalize_condition(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if text.startswith("${{") and text.endswith("}}"):
        text = text[3:-2].strip()
    return text


def explicit_artifact_name(step: dict[str, Any]) -> str | None:
    with_block = step.get("with")
    if not isinstance(with_block, dict):
        return None
    value = with_block.get("name")
    return str(value) if value is not None else None


def get_triggers(workflow: dict[str, Any]) -> set[str]:
    on_value = workflow.get("on")
    if on_value is None:
        # PyYAML 1.1 compatibility if a non-BaseLoader caller generated Boolean True.
        on_value = workflow.get(True)
    if isinstance(on_value, str):
        return {on_value}
    if isinstance(on_value, list):
        return {str(v) for v in on_value}
    if isinstance(on_value, dict):
        return {str(k) for k in on_value}
    return set()


def extract_endpoints(path: Path, workflow: dict[str, Any]):
    producers: list[ArtifactEndpoint] = []
    consumers: list[ArtifactEndpoint] = []
    jobs = workflow.get("jobs") or {}
    if not isinstance(jobs, dict):
        return producers, consumers
    for job_name, job in jobs.items():
        if not isinstance(job, dict):
            continue
        job_if = normalize_condition(job.get("if"))
        steps = job.get("steps") or []
        if not isinstance(steps, list):
            continue
        for index, step in enumerate(steps):
            if not isinstance(step, dict):
                continue
            action = str(step.get("uses") or "")
            endpoint = ArtifactEndpoint(
                workflow=str(path),
                job=str(job_name),
                step_index=index,
                step_id=str(step.get("id")) if step.get("id") is not None else None,
                action=action,
                artifact_name=explicit_artifact_name(step),
                condition=normalize_condition(step.get("if")) or job_if,
            )
            if UPLOAD_RE.match(action):
                producers.append(endpoint)
            elif DOWNLOAD_RE.match(action):
                consumers.append(endpoint)
    return producers, consumers


def normalize_needs(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    return [str(value)]


def needs_ancestors(workflow: dict[str, Any], job_name: str) -> set[str]:
    jobs = workflow.get("jobs") or {}
    if not isinstance(jobs, dict):
        return set()
    visited: set[str] = set()
    stack = list(normalize_needs((jobs.get(job_name) or {}).get("needs")))
    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        current_job = jobs.get(current)
        if isinstance(current_job, dict):
            stack.extend(normalize_needs(current_job.get("needs")))
    return visited


def producer_is_conditionally_non_guaranteed(producer: ArtifactEndpoint, triggers: set[str]) -> tuple[bool, str]:
    condition = producer.condition
    if not condition:
        return False, "unconditional producer"
    compact = re.sub(r"\s+", " ", condition.strip())
    if compact in STATUS_FUNCS or compact == "true":
        return False, "default/status condition"
    if compact == "false":
        return True, "producer condition is false"

    # Narrow, explainable contradictions and conditionality checks.
    ref_eq = re.fullmatch(r"github\.ref\s*==\s*['\"]refs/heads/([^'\"]+)['\"]", compact)
    if ref_eq and "push" not in triggers:
        return True, "producer requires a branch ref but workflow has no push trigger"

    event_eq = re.fullmatch(r"github\.event_name\s*==\s*['\"]([^'\"]+)['\"]", compact)
    if event_eq and event_eq.group(1) not in triggers:
        return True, f"producer requires event {event_eq.group(1)!r}, absent from workflow triggers"

    # An unconditional consumer cannot rely on an arbitrary conditional producer.
    return True, "producer has an additional condition not shared by the consumer"


def analyze_workflow(path: Path) -> dict[str, Any]:
    workflow = load_workflow(path)
    producers, consumers = extract_endpoints(path, workflow)
    triggers = get_triggers(workflow)
    findings: list[Finding] = []

    producers_by_name: dict[str, list[ArtifactEndpoint]] = {}
    for producer in producers:
        if producer.artifact_name is not None:
            producers_by_name.setdefault(producer.artifact_name, []).append(producer)

    for consumer in consumers:
        name = consumer.artifact_name
        matching = producers_by_name.get(name or "", []) if name is not None else []

        if name is None:
            # Download-all semantics are intentionally outside v0.1's AF001 oracle.
            continue

        if not matching:
            findings.append(Finding(
                rule_id="AF001",
                message=(
                    f'Job {consumer.job!r} consumes artifact {name!r}, but this workflow '
                    "contains no producer with the same explicit artifact name."
                ),
                workflow=str(path),
                consumer_job=consumer.job,
                consumer_step_index=consumer.step_index,
                artifact_name=name,
                producer_jobs=[],
                confidence="high",
                evidence={"reason": "no_exact_name_match"},
            ))
            continue

        ancestors = needs_ancestors(workflow, consumer.job)
        dependency_matching = [p for p in matching if p.job in ancestors]
        if not dependency_matching:
            findings.append(Finding(
                rule_id="AF002",
                message=(
                    f'Job {consumer.job!r} consumes artifact {name!r} produced by '
                    f"{sorted({p.job for p in matching})}, but none of those producer jobs "
                    "is in the consumer job's declared needs ancestry."
                ),
                workflow=str(path),
                consumer_job=consumer.job,
                consumer_step_index=consumer.step_index,
                artifact_name=name,
                producer_jobs=sorted({p.job for p in matching}),
                confidence="high",
                evidence={
                    "reason": "missing_declared_dependency",
                    "consumer_needs_ancestors": sorted(ancestors),
                },
            ))
            continue

        unavailable = []
        for producer in dependency_matching:
            non_guaranteed, reason = producer_is_conditionally_non_guaranteed(producer, triggers)
            if non_guaranteed:
                unavailable.append({"job": producer.job, "step_index": producer.step_index, "condition": producer.condition, "reason": reason})

        if unavailable and len(unavailable) == len(dependency_matching):
            findings.append(Finding(
                rule_id="AF001",
                message=(
                    f'Job {consumer.job!r} consumes artifact {name!r}, but every matching '
                    "producer in its dependency ancestry is conditionally non-guaranteed."
                ),
                workflow=str(path),
                consumer_job=consumer.job,
                consumer_step_index=consumer.step_index,
                artifact_name=name,
                producer_jobs=sorted({p.job for p in dependency_matching}),
                confidence="high",
                evidence={"reason": "all_matching_producers_conditionally_non_guaranteed", "producers": unavailable},
            ))

    return {
        "schema_version": "0.1",
        "workflow": str(path),
        "rules": {
            "AF001": "Artifact Consumer Without Guaranteed Producer",
            "AF002": "Artifact Consumer Without Declared Producer Dependency",
        },
        "producers": [asdict(p) for p in producers],
        "consumers": [asdict(c) for c in consumers],
        "findings": [asdict(f) for f in findings],
    }


def workflow_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    candidates = []
    for pattern in ("*.yml", "*.yaml"):
        candidates.extend(path.rglob(pattern))
    return sorted(set(candidates))


def main() -> int:
    parser = argparse.ArgumentParser(description="Artifact-Flow Analysis prototype")
    parser.add_argument("path", type=Path, help="Workflow file or directory")
    parser.add_argument("--format", choices=("json", "text"), default="text")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    reports = [analyze_workflow(path) for path in workflow_files(args.path)]
    result = {
        "schema_version": "0.1",
        "analyzed_workflows": len(reports),
        "finding_count": sum(len(r["findings"]) for r in reports),
        "reports": reports,
    }
    if args.format == "json":
        rendered = json.dumps(result, indent=2)
    else:
        lines = []
        for report in reports:
            for finding in report["findings"]:
                lines.append(f"{finding['rule_id']}: {finding['message']} ({finding['workflow']})")
        rendered = "\n".join(lines) if lines else "No findings."

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 1 if result["finding_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
