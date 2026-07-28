# Artifact-Flow Analysis v0.2

Two changes were made after Holdout 1 and no others:

1. A matching producer earlier in the same job is accepted through sequential step order. A same-job producer at or after the consumer remains AF002.
2. An exactly equivalent normalized producer and consumer condition is treated as correlated, preventing AF001 when both endpoints execute on the same path.

The original 28-case corpus and consumed Holdout 1 are regression sets. Holdout 2 was created and evaluated only after the v0.2 analyzer hash was frozen.
