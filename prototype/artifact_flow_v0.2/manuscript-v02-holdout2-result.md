# Artifact-Flow Analysis v0.2 and Second Holdout

Holdout 1 exposed two false-positive modes in v0.1: same-job artifact reuse and equivalent producer-consumer conditions. Version 0.2 introduced only two corresponding refinements. It accepts a matching upload that occurs earlier in the same job and recognizes exactly equivalent normalized producer and consumer conditions.

Version 0.2 retained all expected results on the 28-case development corpus and corrected both Holdout 1 false positives during regression testing. The analyzer was then frozen with SHA-256 `12d22382838e10ae5616fb2b5946b284ed1966145e818d81573cfee9d642eedf` before a second holdout was created.

Holdout 2 contained 16 unseen cases: 7 positive artifact-flow faults and 9 clean cases, including adversarial same-job, transitive-dependency, multiple-producer, condition-equivalence, expression-name, and download-all scenarios. The frozen analyzer produced 7 true positives, 0 false positives, 9 true negatives, and 0 false negatives. Precision was 1.00, recall was 1.00, and specificity was 1.00. Exact rule-level oracle agreement was 16/16.

These results support the feasibility of narrow, explainable artifact-flow checks for the evaluated cases. They do not establish population-level accuracy or support unrestricted GitHub Actions expressions and inter-workflow artifact transfer.
