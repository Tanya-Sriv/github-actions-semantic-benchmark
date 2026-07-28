# Rule Definitions

## AF001 — Artifact Consumer Without Guaranteed Producer

Reported when a download step has an explicit artifact name and either:

1. no upload step in the workflow has the same explicit name; or
2. matching producers exist in dependency ancestors, but all carry additional
   conditions that make production non-guaranteed for an unconditional consumer.

## AF002 — Artifact Consumer Without Declared Producer Dependency

Reported when a matching artifact producer exists, but none of its jobs appears
in the consumer job's transitive `needs` ancestry.

AF002 is evaluated before conditional-producer reasoning to prevent duplicate
AF001+AF002 findings for the same missing-dependency defect.
