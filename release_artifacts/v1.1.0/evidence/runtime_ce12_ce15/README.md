# Controlled Runtime Extension CE12–CE15

Repository: `Tanya-Sriv/github-actions-controlled-execution-repository`

The workflow definitions in `workflows/` were recovered from immutable GitHub refs used by the controlled experiment. The execution summary records the preserved run IDs and job-level behavior.

## Results

- **CE12 / B002_MX01_001 — matrix coverage:** baseline executed four OS/Python cells; mutant executed only the two Ubuntu cells. Both workflows can be green while coverage is semantically reduced.
- **CE13 / B004_TR02_001 — trigger intent:** on the tests-only pull request, the baseline ran successfully because `tests/**` is in the path filter. The mutant omits `tests/**`; the defect is an absence-of-run behavior rather than a failed job.
- **CE14 / B003_CF02_001 — failure propagation:** both variants contain the same deterministic failing test. In the baseline, `summarize` uses `if: ${{ always() }}` and runs successfully after the failed upstream job. In the mutant, the downstream summary is skipped.
- **CE15 / B001_AR01_001 — artifact identity:** baseline upload/download names agree and verification succeeds; mutant uploads under a different name and fails during artifact download.

These four cases extend the earlier CE01/CE08/CE11 controlled executions, yielding seven representative runtime-validated missed faults in the current manuscript.
