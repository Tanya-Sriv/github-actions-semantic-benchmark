# GitHub Actions Controlled-Execution Pilot Repository

This repository is a synthetic, independently created test environment for controlled execution of two priority semantic-mutation cases:

- **CE08 / B003_RL02** — interaction among `continue-on-error`, step `outcome`, step `conclusion`, `failure()`, and failure-log artifact upload.
- **CE11 / B005_CC02** — cross-workflow concurrency interference when CI and release workflows resolve to the same concurrency group.

## Safety and confidentiality

This repository must contain only synthetic fixtures and public GitHub Actions syntax.

Do not add:

- employer workflows;
- proprietary code;
- internal metrics;
- logs from private systems;
- secrets;
- deployment credentials;
- package-publishing credentials;
- production endpoints;
- company names or affiliations.

## Repository setup

Read:

1. `docs/01_repository_setup.md`
2. `docs/02_ce08_execution.md`
3. `docs/03_ce11_execution.md`
4. `docs/04_evidence_and_adjudication.md`

## Quick start

```bash
git init
git add .
git commit -m "Initialize controlled execution pilot"
bash scripts/create_experiment_branches.sh
```

On Windows PowerShell:

```powershell
git init
git add .
git commit -m "Initialize controlled execution pilot"
powershell -ExecutionPolicy Bypass -File scripts/create_experiment_branches.ps1
```

## Important

The workflows under `experiments/` are source templates. The branch-creation scripts copy the correct files into the active root `.github/workflows/` and `fixture/` directories for each experiment branch.

Do not run baseline and mutant workflows from the same branch unless the experiment guide explicitly requires it.
