import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from artifact_flow.analyzer import analyze_workflow

FIXTURES = Path(__file__).resolve().parent / "fixtures_v02"

def rules(name):
    return [f["rule_id"] for f in analyze_workflow(FIXTURES / name)["findings"]]

def test_same_job_upload_before_download_is_safe():
    assert rules("same_job_safe.yml") == []

def test_same_job_download_before_upload_is_af002():
    assert rules("same_job_late.yml") == ["AF002"]

def test_shared_condition_is_safe():
    assert rules("shared_condition.yml") == []

def test_different_conditions_still_af001():
    assert rules("different_conditions.yml") == ["AF001"]
