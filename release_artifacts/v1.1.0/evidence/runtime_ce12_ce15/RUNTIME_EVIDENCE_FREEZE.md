# Runtime Evidence Freeze - CE12-CE15

Date: 2026-09-04
Study: *Valid Files, Broken Pipelines*
Repository: `Tanya-Sriv/github-actions-controlled-execution-repository`

## Scope

This freeze records the completed four-case runtime-validation extension selected before execution:

- CE12 / B002_MX01_001 - matrix coverage intent
- CE13 / B004_TR02_001 - pull-request trigger path filtering
- CE14 / B003_CF02_001 - cross-job failure propagation
- CE15 / B001_AR01_001 - artifact identity

All four frozen runtime oracles were confirmed. No case was substituted based on outcome and no substantive retry was required.

## Controlled commit and amendment

CE12, CE14, and CE15 were executed against full commit SHA:

`c8fcd726ed5ccd64cc428fd663d24070766492f0`

The pre-execution amendment was committed before these runtime outcomes were observed. It removed missing fixture dependencies from CE12 and CE14 without changing case selection, semantic oracles, or expected outcomes.

## CE12

Baseline run: `33899463227`
Mutant run: `33899468216`

The baseline instantiated four successful matrix jobs spanning Ubuntu and Windows with Python 3.11 and 3.12. The mutant instantiated two successful Ubuntu-only jobs. The frozen matrix-coverage oracle was confirmed.

## CE13

Pull request: `#1`
PR head SHA: `12fc75c1047f8a72ad7e459de1013d66ee46f7b3`
Baseline run: `33900274485`

The tests-only PR triggered the baseline workflow successfully. No CE13 mutant run was observed for the same PR head SHA during the frozen observation window of at least 10 minutes; the threshold time was 2026-09-04T17:33:00Z. The frozen trigger-suppression oracle was confirmed.

## CE14

Baseline run: `33899873255`
Mutant run: `33899876229`

Both test jobs failed on the same deterministic failure probe. In the baseline, the downstream `summarize` job executed successfully under `always()`. In the mutant, `summarize` was skipped. The frozen failure-propagation oracle was confirmed.

## CE15

Baseline run: `33899610554`
Mutant run: `33899617923`

Both producer jobs succeeded. The baseline uploaded artifact `package-c8fcd726ed5ccd64cc428fd663d24070766492f0`, and its verifier succeeded. The mutant uploaded `package-mutated-c8fcd726ed5ccd64cc428fd663d24070766492f0`; its verifier failed at `actions/download-artifact@v4` while requesting the original artifact identity. The frozen artifact-identity oracle was confirmed.

## Result

**4/4 selected extension cases confirmed.**

Together with the previously controlled CE01, CE08, and CE11 cases, the manuscript has runtime confirmation for seven benchmark mutants spanning artifact reachability and identity, matrix coverage, trigger filtering, failure handling/propagation, and cross-workflow concurrency.

## Authoritative freeze commit

`6a1d7249e7ea7b1d0457f4b945d07a1e7412aba8`
Commit message: `Freeze CE12-CE15 runtime validation evidence`
