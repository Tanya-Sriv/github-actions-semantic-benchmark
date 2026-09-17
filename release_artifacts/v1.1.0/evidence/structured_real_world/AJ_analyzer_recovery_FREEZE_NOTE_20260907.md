# A–J Analyzer Evidence Recovery and Freeze Note

Freeze date: 2026-09-07 / controlled run completed 2026-09-08 UTC
Study: *Valid Files, Broken Pipelines*
Scope: recorded 20-case A–J structured real-world phase only.

## Purpose
This package preserves the final evidence-recovery work undertaken after the original per-finding A–J analyzer artifact could no longer be located during manuscript finalization. It prevents later work from conflating the historically recorded aggregate with a newly reproduced result.

## Historical study record
The later consolidated A–J study record preserves the following analyzer totals for the 20-case phase:

- actionlint 1.7.12: 34 raw findings across 4/20 cases
- zizmor 1.28.0: 459 raw findings across 19/20 cases
- poutine 1.1.4: 64 raw findings across 14/20 cases
- total raw findings: 557
- strict repair-specific detections: 0/20 for each analyzer in the recorded A–J study result

These values are retained as **historically recorded results**. The original complete per-finding artifact that produced 557 was not recoverable during the later finalization audit.

## Fresh controlled recovery
A new controlled reconstruction was performed from public repair-PR identities using immutable PR base SHAs and pinned analyzer versions. Nineteen of the twenty recorded cases were recoverable. RW-0018 (`ListenCloser/listencloser#361`) was not publicly resolvable at recovery time and was not replaced by another case.

The final archival run reconstructed the documented defect-target workflow(s), preserved the actual YAML bytes (including hidden `.github` paths), calculated SHA-256 hashes, and stored raw analyzer outputs.

Controlled run ID: `34177365064`
Harness commit: `ac521ba912b738fe763154995dc31658fccc3b76`
GitHub artifact ID: `10037715335`
GitHub artifact digest: `sha256:3acabc18286cc893204131d2ef0c78d80a7f437245c44c4326315c27c6944636`

Pinned analyzers:
- actionlint 1.7.12
- zizmor 1.28.0
- poutine 1.1.4

Final controlled recovery counts under the explicitly documented recovery configuration:

actionlint_no_shellcheck=0 cases=
zizmor=464 cases=18
poutine=65 cases=13
historical_recorded_actionlint=34 cases=4
historical_recorded_zizmor=459 cases=19
historical_recorded_poutine=64 cases=14
historical_recorded_total=557
unresolved_case=RW-0018 ListenCloser/listencloser#361 repository/PR unavailable at recovery time

Thus, under this recovery configuration, the fresh raw-finding total is **529** (0 actionlint with ShellCheck integration disabled + 464 zizmor + 65 Poutine) across the 19 publicly recoverable cases. This is **not** presented as a replacement estimate for the missing twentieth case and is **not** a reproduction of 557.

## Reconciliation conclusion
1. **557 is a genuine historical study result** preserved in later consolidated study records with a stable per-tool breakdown (34 + 459 + 64).
2. **557 has not been independently reproduced exactly** because the original invocation/counting environment and the complete original raw-output artifact are unavailable, and one recorded repository/PR (RW-0018) is no longer publicly resolvable.
3. The fresh replay demonstrates that large numbers of analyzer warnings are readily reproduced on the recorded real-world workflows, but exact raw-warning totals are sensitive to target-file selection and analyzer integration/configuration (especially actionlint's external ShellCheck integration).
4. Therefore, manuscript use should distinguish the two layers:
   - safe: “The consolidated A–J study record reported 557 raw findings (34 actionlint, 459 zizmor, 64 Poutine) while recording 0/20 strict repair-specific detections; the original per-finding artifact was not recoverable during finalization.”
   - stronger reproducibility claim such as “we independently reproduced exactly 557 findings” is **not supported** and should not be made.
5. The scientifically valuable conclusion is the contrast between **high raw-warning volume** and **low/zero repair-specific semantic detection**, not the exact integer 557 itself.

## Archival contents
- `aj-final-reconciliation-freeze-hidden-included.zip`: GitHub Actions artifact containing raw outputs, 19-case immutable pre-fix workflow snapshots, manifest, counts, run metadata, and SHA-256 sums.
- `final_reconciliation_evidence/`: extracted copy of the same evidence for convenient inspection.
- `aj-target-workflow-reproduction.zip` (when present): earlier target-workflow recovery run retained as research history.
- `FREEZE_NOTE.md`: this interpretation and provenance boundary.
- `PACKAGE_SHA256.txt`: package-level hash record.

## Recovered immutable target manifest

```tsv
case_id	repo	pr	base_sha	workflow_path	sha256
RW-0001	Ermal-Mamaj/Mobileria-Mamaj	12	8105fc047cad4e4112812452051d2e975d3d7dd1	.github/workflows/deploy.yml	186a93ff687134df0ab9524a555049440e6ebfc4f1d1a5e1bb2354dbf59b8973
RW-0002	dougis-org/session-combat	633	bc1abad4af168dec3d7d287300a2bd0cae94a5ae	.github/workflows/deploy.yml	5421a50073f079499ac337f314f6b9637199c08b9b6a915f57771fd2157740a7
RW-0003	carstenartur/Taxonomy	924	703daa1636eda61c8e723e1c4d746b3917d90146	.github/workflows/cleanup-workflow-runs.yml	660e5562f02b2e629a3e87600851c319b9c8c0e5055dcca565d168699e2dd6b4
RW-0004	jamesthemullet/roastdinnersaroundtheworld	173	6991d5c2899336bca3dbc89db77f33c7cdd9e035	.github/workflows/pull_request_audit.yml	fa72b223ac188336253f9f89b6d6f7066a71c894586a61d9b8b4480ebf8833ae
RW-0005	mrploch/ploch-data	125	d6724a3710a3ab0f3db80cf9a0fa0b85ac9ab3f8	.github/workflows/build-dotnet.yml	bf6b0b13b97e9c602bb94cd2765bf7610f7059394a0eb06d173ef49eedbb6d74
RW-0005	mrploch/ploch-data	125	d6724a3710a3ab0f3db80cf9a0fa0b85ac9ab3f8	.github/workflows/deploy-nuget-org.yml	ada79abf6b451c7ad502669fd80c21fd0389598230126db7754c588bdb6c79d2
RW-0006	memogrg/Compound-Ascend	679	c81e12120fd2fd544d627f2475fefb8c2c42160d	.github/workflows/ci.yml	9e210a67957e95d1f101573aff6d356739ea0dd39dfec0bb59b969666e401b99
RW-0007	hdot123-org/infra-core	40	b7ea3716e7a480749118ebf861ef04caa7964e79	.github/workflows/ci.yml	ef6313a48d5607e4dffde753556ffee5bad3f26ba03afc999c01a6b8e5ea4cd7
RW-0008	Avarok-Cybersecurity/atlas-recipes	34	95e6922d0ef95957eb8d22c2d8ecd2a18d04185d	.github/workflows/release.yml	34c5b79925cb9dcb3a3c71050d3a4d07f88d5e8c49a8dd8234227ac4809f6ab9
RW-0009	dis-bzh/OpenAether-infra	147	731fbcd28faf6eae9d83f0dfed44baf5988ffcfc	.github/workflows/ci.yml	b6c7aae9d9514a24aefb73214514f482612cadbd10919eb9785d7aaf0516a077
RW-0010	iwacollection/CICD	27	92130cf69d35d122440ad31c3d8c3c689ab98e8a	.github/workflows/ci.yml	41f6263dec61dcaf3c9e30695abcb41a0d7347f40b658d39ab47978e7b6a8d3f
RW-0011	ClearMeasureLabs/bootcamp-palermo-workorders	9003	2b66f8204a165f2300afda0672cd5d000b8dff7c	.github/workflows/deploy.yml	8df9a1f9a2379175b139a571ed160c368407fa09137f7402fce05a647ac11842
RW-0012	Azure/osdu-spi	144	9a2a202b3c40cc00ba7a3077560972b8181625a1	.github/template-workflows/codeql.yml	435f1ad4266c2d72f114e47425f88e1bf562f50dc73c7e51076dc0771aeda779
RW-0013	Daatan/daatan	1599	1cc7e465ae5a1f47b0a8b96ab913b6601f033bf6	.github/workflows/deploy.yml	b12f36a5eb607472cf16b2b7ff88f68ef0d0cc1bbdfa1c2d5509952a54e61953
RW-0014	geoff-coppertop/nixos-config	147	e631ac2d11066812770a2dd0f1aa7376680535fd	.github/workflows/ci.yml	ef62f9a362e5cc699c287504e14202a9ddc8bead2e2985ae6605ffc3c5cba854
RW-0015	meshtastic/firmware	11549	74119c088b6ca1e7c8febfec843363c949cf8f01	.github/workflows/main_matrix.yml	6c91d3d38d84c791dd15e22b663f58e4daae8c39f2cd8551bbb4acdc600e1fcb
RW-0016	DartHealth/ex_audit	1	18a1424ca9b154a8a3773072c63ba60fc3ea2543	.github/workflows/elixir.yml	09d092453645f32500f22ea05d21f65d47ec56a9b1481f4f558f8fd845ea8947
RW-0017	0x524a/onvif-go	70	7a4a1b6e280d1348c153157f1c346d325f6d78a7	.github/workflows/release.yml	86dd6ae39f85b1b0bd9b729dc31a02c1763ffac6cca7eb58134dbf85a1589266
RW-0019	dipakkrishnan/lore-mcp	162	6ec24c39ab4ecfa24dc052880520baea45eb93f3	.github/workflows/deploy-qa.yml	17f8bb16a824e5da7c07bb2ab170c86d2c79f6fb78e014e5a8c0ff350f0dd1fb
RW-0020	Paca-AI/paca	413	c639e7493b9e2f18a6f7cb854a5067e95d18d774	.github/workflows/cd.yml	ec3dc59018e6bd9e41d1af4997dbc488099bfadd2e97ea35f973701a22247b8b
```

## Run metadata

```text
run_id=34177365064
run_attempt=1
harness_commit=ac521ba912b738fe763154995dc31658fccc3b76
actionlint=1.7.12 shellcheck_integration=disabled
zizmor=1.28.0
poutine=1.1.4
```

## Rule for future manuscript/release work
Do not silently replace the historically recorded 557 with 529, and do not claim 557 was freshly reproduced. If the historical 557 number is included, label it as a result preserved by the consolidated study record and disclose the loss of the original per-finding artifact. Prefer emphasizing the raw-warning/repair-specific-detection contrast rather than relying on 557 as a headline reproducibility statistic.
