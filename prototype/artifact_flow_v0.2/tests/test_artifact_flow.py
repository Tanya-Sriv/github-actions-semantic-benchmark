import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from artifact_flow.analyzer import analyze_workflow

FIXTURES = Path(__file__).resolve().parent / "fixtures"

def rules(filename):
    return [f["rule_id"] for f in analyze_workflow(FIXTURES / filename)["findings"]]

def test_clean_baseline():
    assert rules("baseline.yml") == []

def test_name_mismatch_producer():
    assert rules("B001_AR01_001.yml") == ["AF001"]

def test_name_mismatch_consumer():
    assert rules("B001_AR02_001.yml") == ["AF001"]

def test_conditional_producer():
    assert rules("B001_AR03_001.yml") == ["AF001"]

def test_missing_needs():
    assert rules("B001_CF01_001.yml") == ["AF002"]
