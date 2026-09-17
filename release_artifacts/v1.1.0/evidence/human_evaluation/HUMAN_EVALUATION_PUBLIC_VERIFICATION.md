# Independent Human Evaluation — Frozen-to-Public Verification

Authoritative frozen originals are retained in the long-term frozen-records master archive and are not distributed in this public release candidate because Part B contains evaluator-identifying Office metadata.

## Evaluation chronology and independence

Pulkit Srivastava completed the blinded human evaluation before joining the broader research and manuscript-development process. His later participation as a co-author therefore postdates the blinded evaluation and does not alter the chronology under which those judgments were produced.

Public sanitized package SHA-256: `cca852f6c4b72d7cc4b8b93559aae95e6c681e4f677624ff0433fd9e5987bb1e`

| Workbook | Frozen original SHA-256 | Public sanitized SHA-256 |
|---|---|---|
| `Independent_Human_Evaluation_Part_A_Evaluated_Final.xlsx` | `e7d07f17df72cfa8c69f4eaecee1b0718b9845caeca9686a726a16d764f61000` | `8576282e0224b5806ea12e0effbcfd72d551dac5027db125a5fef74c29495aed` |
| `Independent_Human_Evaluation_Part_B_Evaluated_Final.xlsx` | `f14502447988e13c3f6c9edcad40329b44b540f1e2ad98d02a7f8d0b63f5529e` | `404bb87cf9a615098b665fa0ada488f9e9f2202ff414e94c2fb493d2a65a5de4` |
| `Independent_Human_Evaluation_Part_C_Evaluated_Final.xlsx` | `735406659c3b9f78a070262ef30adcc228bf7a8901a57d92602bc49ee35d883c` | `bc2a266aa47aad8020e4f8bbe0fb977b08fa3a292767e26ada5fadb1ecb07a01` |

Sanitization changes only `docProps/core.xml` author metadata. Every other XLSX member is byte-identical to the frozen original.

The public workbooks remain blinded: no model/provider identity or evaluator email address appears in scoring cells.