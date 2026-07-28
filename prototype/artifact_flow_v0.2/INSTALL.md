# Repository Installation

Copy this directory into the benchmark repository as `artifact-flow-prototype/`.
Copy `.github/workflows/validate_artifact_flow_prototype.yml` to the repository's
`.github/workflows/` directory. The validation workflow expects these existing
paths:

- `benchmark/baselines/`
- `benchmark/mutants/`
- `benchmark/mutant_manifest.csv`
- `benchmark/negative_controls/`
