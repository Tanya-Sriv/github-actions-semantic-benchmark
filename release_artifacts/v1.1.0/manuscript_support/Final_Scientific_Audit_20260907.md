# Final Scientific Consistency Audit — 2026-09-07

## Audited manuscript
`Valid_Files_Broken_Pipelines_IEEE_Access_PreV1_1_6plus30_FinalAudit_20260907.docx`

## Outcome
**PASS as a scientifically bounded pre-release manuscript candidate.**

The document is internally consistent after the corrections below. It should not yet be described as a fully archived/release-ready research package because the post-v1.0.1 extension artifacts have not yet been assembled into the next public versioned release.

## Verified headline results
- Synthetic benchmark: 18 schema-valid mutants; analyzer union 1/18 (5.6%).
- Controlled runtime validation: 7 representative missed faults.
- Historical validation: 6 cases; 0/6 repair-specific detections by each evaluated analyzer.
- Structured real-world corpus: 30 recorded cases total.
  - Recorded A–J protocol phase: 20 cases; consolidated study record reports 0/20 strict detections by actionlint, zizmor, and poutine.
  - Separately frozen K–T continuation: 10 cases; actionlint 3/10, zizmor 1/10, poutine 0/10, union 4/10.
  - Descriptive combined 30-case coverage: actionlint 3/30 (10.0%), zizmor 1/30 (3.3%), poutine 0/30, union 4/30 (13.3%).
- Human evaluation: 315 responses; strict 205/315 (65.08%), lenient 226/315 (71.75%).
  - Claude 85/105 strict (80.95%).
  - GPT 81/105 strict (77.14%).
  - Gemini 39/105 strict (37.14%).
  - Human/secondary four-category agreement 303/315 (96.19%), kappa 0.929.
  - Claude-vs-GPT exact McNemar p = 0.625.

## Important provenance correction made
Earlier manuscript wording treated the A–J 20-case phase as if its complete ordered query-family execution, final freeze artifacts, and per-finding analyzer provenance were fully recoverable. The private finalization audit had explicitly marked those provenance items as blocked. A later consolidated A–T handoff, however, records the A–J family yields, all 20 retained case identities, the Family J stopping boundary, and the 0/20 analyzer outcome.

The manuscript now preserves the substantive A–J study record while explicitly disclosing that the primary ordered search/freeze and complete per-finding analyzer provenance were not fully recoverable during finalization. It therefore does **not** present the A–J phase or combined 30 cases as a probability sample or fully replayable live-ranking denominator.

The previously reported A–J raw total of 557 analyzer findings was removed from the headline/reproducibility claims because the finalization audit could not independently recover the complete per-finding artifact needed to substantiate that breakdown.

## 6 + 30 framing retained
The manuscript now uses two main real-world components:
1. Six purposefully selected historical cases.
2. A 30-case structured real-world corpus consisting of a recorded 20-case A–J protocol phase plus a separately frozen 10-case K–T continuation.

This keeps the presentation compact while preserving the construction-history distinction in Methods, Results, Threats to Validity, Reproducibility, Conclusion, and Appendix C.

## Appendix C check
The 20 A–J rows match the later consolidated handoff, including the recorded family yields:
A=1, B=1, C=2, D=0, E=3, F=7, G=2, H=2, I=0, J=2, cumulative 20 after J.
The 10 K–T continuation rows match the frozen continuation manifest.

## Mechanical and layout QA
- 22 pages rendered after final edits.
- All pages visually inspected.
- No clipping, overlap, broken columns, missing glyphs, or table overflow observed.
- Table and figure numbering is sequential: Tables 1–15, Figures 1–4, Appendices A–C.
- Heading audit completed.
- Stale-risk scan found no remaining 557-finding headline claim, “final systematic denominator,” or complete-provenance overstatement.

## Remaining work before journal submission
1. Assemble the post-v1.0.1 evidence into the next versioned public artifact release and update §9.5/§11 with the final release version/DOI.
2. Perform a final source-integrity/citation fact check if not already completed after the latest content edits.
3. Author performs a final line-by-line manual proofread of the rendered manuscript.

