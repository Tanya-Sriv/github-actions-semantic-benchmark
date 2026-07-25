# 3. CE11 Execution Guide

## Research question

Do CI and release workflows interfere when both resolve to the same concurrency group?

## Baseline branch

```bash
git checkout ce11-baseline
```

Groups:

- CI: `ci-main`
- Release: `release-main`

They should run independently.

## Mutant branch

```bash
git checkout ce11-mutant
```

Groups:

- CI: `ci-main`
- Release: `ci-main`

This creates the intended cross-workflow collision.

## Baseline trial

1. Trigger **CE11 baseline CI** on `ce11-baseline`.
2. Within 10 seconds, trigger **CE11 baseline release**.
3. Record both run IDs and conclusions.
4. Repeat in the opposite order.
5. Repeat at least three times per order.

Minimum recommended baseline trials: six.

## Mutant trial

Repeat the same sequence using `ce11-mutant`.

Minimum recommended mutant trials: six.

## Expected evidence

Record:

- first workflow triggered;
- second workflow triggered;
- trigger-time difference;
- CI run ID;
- release run ID;
- queue behavior;
- cancellation behavior;
- final conclusions;
- raw logs.

## GitHub CLI examples

```bash
gh workflow run ci.yml --ref ce11-mutant
sleep 5
gh workflow run release.yml --ref ce11-mutant
```

Reverse order:

```bash
gh workflow run release.yml --ref ce11-mutant
sleep 5
gh workflow run ci.yml --ref ce11-mutant
```

## Evidence destination

```text
results/pilot/controlled_execution/CE11/
├── baseline-trial-01/
├── baseline-trial-02/
├── mutant-trial-01/
└── ...
```
