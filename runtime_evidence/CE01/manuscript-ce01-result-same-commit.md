# CE01 Artifact-Flow Controlled Execution

CE01 evaluated mutant `B001_AR03_001`, in which the only artifact-producing step was made unreachable under `workflow_dispatch` while the downstream consumer continued to request the artifact unconditionally.

Both the baseline and mutant were executed from the same repository commit (`a09033845e777332340f52784f6cebbd02adc088`), providing strict version parity.

The baseline run (`30223029640`) completed successfully. Its build job succeeded, the `ce01-package` artifact was uploaded, the downstream job downloaded and verified the artifact, and the workflow concluded successfully.

The mutant run (`30223035306`) produced the expected contrasting behavior. The build job succeeded, but the artifact-upload step was skipped. The downstream `verify` job then failed because `ce01-package` did not exist, producing the error: “Unable to download artifact(s): Artifact not found for name: ce01-package.” The workflow concluded with failure and no `ce01-package` artifact was present.

This same-commit controlled comparison confirms the runtime consequence encoded by the CE01 oracle: a syntactically valid workflow can contain a conditionally unreachable artifact producer whose unconditional downstream consumer fails at runtime.
