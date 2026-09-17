# Historical Real-World Validation — Six Purposefully Selected Cases

This set remains separate from the 30-case structured real-world corpus. It is a purposefully selected external-grounding set and is not a probability sample.

| Case | Repository | Documented defect | Repair-specific result |
|---|---|---|---|
| 1 | Apache Airflow | Release/ref coupling | Miss by all 3 |
| 2 | FastAPI | Skipped-job acceptance mismatch | Miss by all 3 |
| 3 | op-succinct | Transitive skip propagation | Miss by all 3 |
| 4 | op-succinct | Required-check materialization | Miss by all 3 |
| 5 | Pydantic | Deployment-condition scope | Miss by all 3 |
| 6 | github/gh-aw | Artifact-flow hidden-file omission | Miss by all 3 |

Each evaluated analyzer—actionlint 1.7.12, zizmor 1.28.0, and poutine 1.1.4—recorded **0/6 repair-specific detections**. The original historical six-case evidence packages were recovered and verified during RC3 assembly: Cases 1–5 are preserved in `Real_World_Validation_v1_Case01_Case05.zip`, and Case 6 is preserved in `Case06_GH_AW_Artifact_Flow_Validation.zip`. These recovered packages are included in this release candidate and are hash-recorded in the release manifest.
