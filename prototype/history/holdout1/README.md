# AF001/AF002 Frozen Holdout Evaluation

This package evaluates the unchanged v0.1 Artifact-Flow Analysis rules on 14 cases created after rule development:

- 6 positive artifact-flow faults
- 8 clean cases, including adversarial clean workflows

The analyzer source is copied under `frozen_prototype/`, and its SHA-256 is recorded in `FROZEN_RULES_LOCK.json`.

## Result

- TP: 6
- FP: 2
- TN: 6
- FN: 0
- Precision: 0.750
- Recall: 1.000
- Specificity: 0.750

The adversarial clean cases reveal where the narrow v0.1 rules require refinement. Do not modify the frozen analyzer and rerun this same holdout as though it remained unseen; any refinement should be evaluated on a new second holdout.
