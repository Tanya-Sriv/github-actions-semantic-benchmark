# 1. Repository Setup

## Prerequisites

Install:

- Git
- A GitHub account
- Python 3.11 or later for local fixture checks
- Optional: GitHub CLI (`gh`) for downloading logs and triggering workflows

## Create the GitHub repository

Create a new empty repository named:

`github-actions-semantic-benchmark`

Recommended settings:

- Visibility: private during pilot execution
- Initialize with README: no
- Add `.gitignore`: no
- Add license: no

This package already includes those files.

## Extract and initialize locally

```bash
unzip github-actions-controlled-execution-repository.zip
cd github-actions-controlled-execution-repository
git init
git branch -M main
git add .
git commit -m "Initialize controlled execution"
```

## Connect the GitHub remote

Replace `YOUR-ACCOUNT`:

```bash
git remote add origin https://github.com/YOUR-ACCOUNT/github-actions-semantic-benchmark.git
git push -u origin main
```

## Create experiment branches

macOS/Linux:

```bash
bash scripts/create_experiment_branches.sh
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/create_experiment_branches.ps1
```

Push all branches:

```bash
git push -u origin ce08-baseline
git push -u origin ce08-mutant
git push -u origin ce11-baseline
git push -u origin ce11-mutant
```

## Verify each branch

```bash
git checkout ce08-baseline
python scripts/verify_branch_contents.py

git checkout ce08-mutant
python scripts/verify_branch_contents.py

git checkout ce11-baseline
python scripts/verify_branch_contents.py

git checkout ce11-mutant
python scripts/verify_branch_contents.py
```

## Repository permissions

The included workflows declare:

```yaml
permissions:
  contents: read
```

Do not add secrets or broader permissions for these experiments.
