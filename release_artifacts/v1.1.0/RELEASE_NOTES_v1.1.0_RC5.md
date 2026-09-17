# GitHub Actions Semantic Benchmark v1.1.0 — Release Candidate 5

**Status: release-ready candidate; not yet tagged or published.**

This candidate extends public v1.0.1 (Zenodo DOI `10.5281/zenodo.21658780`) with the post-v1.0.1 evidence supporting the expanded manuscript.

## Major additions

1. **30-case structured real-world corpus support**
   - recorded 20-case A–J protocol phase;
   - separately frozen 10-case K–T continuation;
   - K–T repair-specific analyzer results and raw outputs;
   - A–J evidence-recovery package preserving the historical 557-finding record separately from the fresh 19-case recovery.

2. **Controlled runtime validation extension CE12–CE15**
   - matrix/coverage semantics;
   - trigger-intent semantics;
   - failure/dependency propagation;
   - artifact identity/dataflow;
   - authoritative freeze commit: `6a1d7249e7ea7b1d0457f4b945d07a1e7412aba8`.

3. **Independent human evaluation**
   - 315 blinded evaluations;
   - frozen originals verified and preserved in the long-term records archive;
   - public-sanitized workbooks included here with frozen-to-public SHA-256 mapping;
   - private automated secondary-evaluation raw artifacts excluded.

4. **Six historical real-world cases**
   - original Cases 1–5 validation package recovered and included;
   - original Case 6 `github/gh-aw` artifact-flow package recovered and included.

5. **Scientific audit/manuscript support**
   - final scientific consistency audit;
   - current manuscript support snapshot.

## Analyzer versions

- actionlint 1.7.12
- zizmor 1.28.0
- poutine 1.1.4

## Important provenance boundaries

- The consolidated A–J record reports **557 raw findings** (34 actionlint, 459 zizmor, 64 Poutine) with 0/20 strict repair-specific detections.
- The exact original per-finding artifact for 557 was not recoverable during finalization.
- The fresh 19-case A–J recovery is a separate evidence layer and is not an exact reproduction of 557.
- RW-0018 (`ListenCloser/listencloser#361`) was not publicly resolvable during recovery and was not replaced.
- K–T is a supplementary continuation beyond the recorded A–J stopping boundary; combined 30-case results are descriptive and not population-prevalence estimates.

## Public-release decision

All major evidence workstreams have frozen provenance. RC5 preserves the RC5 release-ready evidence set, corrects the stale RC1/RC2 documentation in RC3 and removes evaluator-identifying Office metadata from the public human-evaluation derivative.

The remaining steps are publication mechanics:
1. stage the v1.1.0 public artifacts in the benchmark repository;
2. validate the staged repository;
3. tag/publish GitHub release v1.1.0;
4. archive the release on Zenodo and record the resulting DOI;
5. update the manuscript with the final release/DOI.
