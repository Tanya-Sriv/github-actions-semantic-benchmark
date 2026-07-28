# GitHub Actions Semantic Benchmark

This repository contains the research artifact for:

> **Valid Files, Broken Pipelines: A Mutation-Based Evaluation of Semantic Error Detection in GitHub Actions Workflows**

The benchmark evaluates whether GitHub Actions analysis tools detect operational-semantic faults that remain syntactically valid and schema-valid while violating intended relationships across steps, jobs, triggers, artifacts, failure states, or workflows.

## Repository Status

This repository is being prepared for the initial public research-artifact release, `v1.0.0`.

The release corresponding to the paper will be archived through Zenodo and assigned a version-specific DOI.

## Benchmark Contents

The repository currently includes:

- five canonical synthetic workflow baselines;
- eighteen schema-valid semantic mutants;
- five semantics-preserving negative controls;
- benchmark manifests and per-case metadata;
- automated clean-baseline and mutant scanner workflows;
- pinned-action sensitivity analysis;
- semantic-equivalence validation for negative controls;
- controlled-execution cases for CE08 and CE11;
- comparison and validation scripts;
- execution and adjudication documentation.

The repository includes the canonical Artifact-Flow Analysis prototype, consolidated result artifacts, and controlled runtime-validation evidence corresponding to the study.

## Research Scope

The benchmark focuses on operational relationships that may not be captured by file-local syntax, schema validation, or security-oriented checks.

Representative fault categories include:

- producer-consumer artifact mismatches;
- incorrect matrix or expression references;
- failure-handling changes;
- conditional-execution faults;
- cross-job and cross-workflow dependencies;
- concurrency-group interference;
- operational changes that preserve local validity.

The benchmark is intentionally bounded. It does not claim to represent every GitHub Actions construct, every workflow failure mode, or the prevalence of these faults in public repositories.

## Repository Structure

```text
.github/workflows/          GitHub Actions automation
benchmark/baselines/        Canonical clean workflow baselines
benchmark/mutants/          Schema-valid semantic mutants
benchmark/negative_controls/
                            Semantics-preserving controls
benchmark/*.csv             Benchmark and control manifests
experiments/CE08/           Failure-handling controlled-execution case
experiments/CE11/           Cross-workflow concurrency case
scripts/                    Validation and comparison utilities
templates/                  Evidence and adjudication templates
docs/                       Setup, execution, and troubleshooting guidance
fixture/                    Active controlled-execution fixture location
prototype/                  Artifact-Flow Analysis v0.2, tests, and holdouts
results/                    Canonical result tables and validation summaries
runtime_evidence/           CE01, CE08, and CE11 execution evidence