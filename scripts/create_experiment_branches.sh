#!/usr/bin/env bash
set -euo pipefail

if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
  echo "Create an initial commit before running this script."
  exit 1
fi

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

create_branch() {
  local branch="$1"
  local source="$2"

  git checkout -B "$branch"
  rm -rf .github/workflows fixture
  mkdir -p .github/workflows fixture

  cp -R "$source/.github/workflows/." .github/workflows/
  if [ -d "$source/fixture" ]; then
    cp -R "$source/fixture/." fixture/
  else
    printf '%s\n' "No fixture required for this experiment." > fixture/README.md
  fi

  git add .github/workflows fixture
  git commit -m "Configure $branch"
}

create_branch ce08-baseline experiments/CE08/baseline
git checkout main
create_branch ce08-mutant experiments/CE08/mutant
git checkout main
create_branch ce11-baseline experiments/CE11/baseline
git checkout main
create_branch ce11-mutant experiments/CE11/mutant
git checkout main

echo "Created branches:"
git branch --list "ce08-*" "ce11-*"
