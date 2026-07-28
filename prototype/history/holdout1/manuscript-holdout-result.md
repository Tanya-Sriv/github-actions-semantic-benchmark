# Frozen Holdout Evaluation of AF001 and AF002

After completing rule development, we froze the v0.1 analyzer and evaluated it without modification on a separately constructed 14-case holdout set. The set contained six positive artifact-flow faults and eight clean workflows, including adversarial cases involving transitive dependencies, multiple producers, download-all behavior, same-job artifact reuse, shared producer-consumer conditions, and expression-valued artifact names.

The frozen prototype detected all six positive cases, yielding holdout recall of 1.000. It also produced findings in 2 of eight clean cases, yielding precision of 0.750 and specificity of 0.750. The false-positive cases were `H012_SAME_JOB_REUSE`, `H013_SHARED_CONDITION`.

These false positives expose two limitations of the initial abstraction. First, AF002 treats a same-job producer as lacking a `needs` dependency even though steps within a job execute sequentially. Second, AF001 evaluates producer conditionality without proving that the consumer is guarded by an equivalent condition. The holdout therefore supports the feasibility of targeted artifact-flow analysis while showing that context-sensitive handling of intra-job order and correlated conditions is necessary before broader accuracy claims.

Because these cases are now observed, they must not be reused as an unseen test set after refining the rules. Any revised analyzer should be evaluated on a newly generated second holdout.
