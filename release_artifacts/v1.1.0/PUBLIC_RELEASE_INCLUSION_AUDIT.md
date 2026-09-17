# Public Release Inclusion Audit — v1.1.0 RC5

## Included and verified

- A–J analyzer recovery/freeze package and provenance note — **included**.
- K–T complete frozen supplementary extension package — **included**.
- Original historical Cases 1–5 package — **included and hash-recorded**.
- Original historical Case 6 package — **included and hash-recorded**.
- CE12–CE15 authoritative freeze evidence and run metadata — **included**.
- Independent-human evaluation public-sanitized derivative — **included and hash-mapped to frozen originals**.
- Final scientific consistency audit — **included**.
- Current manuscript support snapshot — **included for review; optional for final benchmark release**.

## Deliberately excluded from the public package

- Frozen-original independent-human workbooks containing evaluator-identifying Office metadata — preserved in the private/frozen master archive instead.
- Automated secondary-evaluation raw workbook/artifacts — private/preliminary and not independent human ratings.
- Blind-key mappings, model-identity mappings, retry internals, and preliminary rankings — not included.

## Closed provenance items

1. Independent human evaluation source workbooks — **CLOSED**.
2. Historical six-case raw evidence — **CLOSED**.
3. CE12–CE15 runtime evidence — **CLOSED**.
4. K–T supplementary extension — **CLOSED**.
5. A–J evidence recovery — **CLOSED WITH DISCLOSED LIMITATION** regarding the unrecovered original per-finding artifact and RW-0018 unavailability.

## Integrity

- RC manifest and SHA-256 manifest must validate with zero mismatches before publication.
- Public human-evaluation workbooks are linked to frozen originals through `FROZEN_TO_PUBLIC_HASH_MAPPING.csv`.
- Frozen originals remain unchanged in the long-term records archive.

## Release decision

**RC5 passes the evidence/provenance and public-safety release-readiness audit.**

It should not be called the published v1.1.0 release until the repository content is staged, validated, tagged, and archived. The DOI can only be inserted into the manuscript after the archival release identifier is known.
