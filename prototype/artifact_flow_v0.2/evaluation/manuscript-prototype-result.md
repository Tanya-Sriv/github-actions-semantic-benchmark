# Initial Artifact-Flow Analysis Prototype

We implemented a narrow static prototype with two rules: AF001, Artifact Consumer Without Guaranteed Producer, and AF002, Artifact Consumer Without Declared Producer Dependency. The prototype extracts explicit `upload-artifact` and `download-artifact` names, constructs transitive job-dependency ancestry from `needs`, and applies conservative producer-condition reasoning.

The prototype was evaluated on 28 cases: 5 clean baselines, 18 schema-valid mutants, and 5 semantics-preserving negative controls. Four mutants were designated in-scope artifact-flow positives: two artifact-name mismatches, one conditionally non-guaranteed producer, and one missing producer-job dependency. The prototype detected all four, producing three AF001 findings and one AF002 finding. It produced no findings on the remaining 14 mutants, five clean baselines, or five negative controls.

At the case level, the in-sample confusion matrix was TP=4, FP=0, TN=24, and FN=0, corresponding to precision=1.00 and recall=1.00. These values describe performance on the known benchmark cases used to define the initial rules; they are not evidence of generalization to unseen workflows or mutation operators. Holdout evaluation is required before presenting the values as detector accuracy.
