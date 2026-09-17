# GitHub Actions Semantic Benchmark

This repository contains the canonical research artifact associated with the study:

> **Valid Files, Broken Pipelines: A Mutation-Based Benchmark for Operational-Semantic Error Detection in GitHub Actions Workflows**

The benchmark evaluates whether GitHub Actions analysis tools detect operational-semantic faults that remain syntactically valid and schema-valid while violating intended relationships across steps, jobs, triggers, artifacts, failure states, or workflows.

## Associated Paper

**Valid Files, Broken Pipelines: A Mutation-Based Benchmark for Operational-Semantic Error Detection in GitHub Actions Workflows**

**Authors:** Tanya Srivastava and Pulkit Srivastava  
**Tanya Srivastava ORCID:** https://orcid.org/0009-0000-5222-2076  
**Correspondence:** tanya.1108srivastava@gmail.com

## Author Contributions

**Tanya Srivastava:** Conceptualization, methodology, benchmark design, software and artifact development, investigation, experimentation, data curation, formal analysis, validation, visualization, reproducibility and artifact preparation, and writing—original draft and revision.

**Pulkit Srivastava:** Blinded independent human evaluation completed before joining the research team, followed by validation and review of study results, interpretation of findings, and writing—review and editing.

**Both authors** reviewed and approved the final manuscript and associated v1.1.0 research artifact.

Pulkit Srivastava completed the blinded human evaluation before becoming involved in the broader research and manuscript-development process. His subsequent co-authorship therefore does not alter the chronology of the blinded evaluation. The contribution statement above describes the current manuscript and v1.1.0 research artifact and does not retroactively redefine authorship or provenance of previously frozen v1.0.0/v1.0.1 artifacts.

## Release and Archival Record

- **Current public release:** [`v1.0.1`](https://github.com/Tanya-Sriv/github-actions-semantic-benchmark/releases/tag/v1.0.1)
- **v1.1.0 status:** release preparation in progress
- **Source repository:** [Tanya-Sriv/github-actions-semantic-benchmark](https://github.com/Tanya-Sriv/github-actions-semantic-benchmark)
- **Existing Zenodo record:** [10.5281/zenodo.21658780](https://doi.org/10.5281/zenodo.21658780)
- **License:** MIT

The v1.1.0 release extends the public research package with additional validation and evaluation materials while preserving the provenance of previously frozen artifacts. Final v1.1.0 release metadata and the archival DOI/version record will be inserted after release finalization.

## Benchmark Contents

The repository includes:

- five canonical synthetic workflow baselines;
- eighteen schema-valid semantic mutants;
- five semantics-preserving negative controls;
- benchmark manifests and per-case metadata;
- automated clean-baseline and mutant scanner workflows;
- pinned-action sensitivity analysis;
- semantic-equivalence validation for negative controls;
- controlled runtime-validation evidence for CE01, CE08, and CE11;
- comparison and validation scripts;
- execution and adjudication documentation;
- the canonical Artifact-Flow Analysis prototype, version 0.2;
- development and holdout evaluation artifacts; and
- consolidated result tables and release-validation summaries.

## Release Validation Summary

The released v1.0.1 artifacts report:

- **18** semantic mutants;
- **1 of 18** mutants detected by the union of the evaluated existing tools;
- **1 of 18** mutants detected by the pinned-tool union;
- **3** mutants supported by controlled runtime evidence;
- **4** known artifact-flow-positive mutants detected by Artifact-Flow Analysis in the benchmark corpus; and
- exact oracle agreement for all **16** workflows in the designed second holdout for the frozen Artifact-Flow Analysis v0.2.

The Artifact-Flow Analysis results are specific to the released benchmark and designed holdout. They should not be interpreted as population-level detector-accuracy estimates.

## Research Scope

The benchmark focuses on operational relationships that may not be captured by file-local syntax, schema validation, or security-oriented checks.

Representative fault categories include:

- producer-consumer artifact mismatches;
- incorrect matrix or expression references;
- failure-handling changes;
- conditional-execution faults;
- cross-job and cross-workflow dependencies;
- concurrency-group interference; and
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
```

## Reproducibility

The repository provides workflows and scripts for:

- running clean-baseline scans;
- running mutant scans;
- evaluating pinned-action sensitivity;
- validating semantics-preserving negative controls;
- validating the Artifact-Flow Analysis prototype;
- comparing normalized scanner findings; and
- checking release artifacts and result consistency.

See the `docs/` directory, workflow documentation under `.github/workflows/`, and the prototype-specific instructions under `prototype/artifact_flow_v0.2/`.

## Artifact Boundaries

All workflows and evaluation artifacts were independently created for this study. The repository contains no employer workflow data, proprietary source code, internal logs, confidential metrics, credentials, or private production-system information.

## Citation

Citation metadata is provided in [`CITATION.cff`](CITATION.cff). The final v1.1.0 citation and Zenodo archival identifier will be updated after the release is frozen and archived.

## License

This project is released under the [MIT License](LICENSE).
