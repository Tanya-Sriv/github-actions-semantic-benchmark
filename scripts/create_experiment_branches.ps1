$ErrorActionPreference = "Stop"

git rev-parse --verify HEAD | Out-Null
$root = git rev-parse --show-toplevel
Set-Location $root

function Create-ExperimentBranch {
    param(
        [string]$Branch,
        [string]$Source
    )

    git checkout -B $Branch

    if (Test-Path ".github/workflows") {
        Remove-Item ".github/workflows" -Recurse -Force
    }
    if (Test-Path "fixture") {
        Remove-Item "fixture" -Recurse -Force
    }

    New-Item ".github/workflows" -ItemType Directory -Force | Out-Null
    New-Item "fixture" -ItemType Directory -Force | Out-Null

    Copy-Item "$Source/.github/workflows/*" ".github/workflows/" -Recurse -Force

    if (Test-Path "$Source/fixture") {
        Copy-Item "$Source/fixture/*" "fixture/" -Recurse -Force
    } else {
        "No fixture required for this experiment." | Set-Content "fixture/README.md"
    }

    git add .github/workflows fixture
    git commit -m "Configure $Branch"
}

Create-ExperimentBranch "ce08-baseline" "experiments/CE08/baseline"
git checkout main
Create-ExperimentBranch "ce08-mutant" "experiments/CE08/mutant"
git checkout main
Create-ExperimentBranch "ce11-baseline" "experiments/CE11/baseline"
git checkout main
Create-ExperimentBranch "ce11-mutant" "experiments/CE11/mutant"
git checkout main

git branch --list "ce08-*" "ce11-*"
