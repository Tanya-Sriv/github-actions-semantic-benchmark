# 2. CE08 Execution Guide

## Research question

Does adding `continue-on-error: true` to a failing test step change subsequent `failure()` behavior and failure-log artifact collection?

## Baseline branch

```bash
git checkout ce08-baseline
```

The baseline intentionally fails the test and does not use `continue-on-error`.

## Mutant branch

```bash
git checkout ce08-mutant
```

The mutant differs by one semantic mutation:

```yaml
continue-on-error: true
```

## Trigger baseline

In GitHub:

1. Open **Actions**.
2. Select **CE08 baseline failure handling**.
3. Select **Run workflow**.
4. Choose branch `ce08-baseline`.
5. Run it.

Record:

- run ID;
- commit SHA;
- `run-tests` outcome;
- `run-tests` conclusion;
- value printed for `failure()`;
- upload step outcome and conclusion;
- whether `failure-logs` exists;
- job conclusion;
- workflow conclusion.

## Trigger mutant

Repeat using:

- workflow: **CE08 mutant failure handling**
- branch: `ce08-mutant`

## GitHub CLI alternative

```bash
gh workflow run ce08.yml --ref ce08-baseline
gh run list --workflow ce08.yml --branch ce08-baseline --limit 1
```

Then repeat for `ce08-mutant`.

## Evidence destination

Store evidence under:

```text
results/pilot/controlled_execution/CE08/
├── baseline/
└── mutant/
```

Use the templates in `templates/`.

## Adjudication

Use:

- `confirmed`
- `contradicted`
- `inconclusive`
- `execution_failed`
- `not_run`

Do not assume in advance whether the artifact upload will run.
