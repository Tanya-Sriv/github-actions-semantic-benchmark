#!/usr/bin/env python3
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parent
EXCLUDE={"FREEZE_SHA256.txt"}
rows=[]
for p in sorted(ROOT.rglob("*")):
    if not p.is_file() or p.name in EXCLUDE or any(part in {"raw_requests","raw_responses","outputs","logs"} for part in p.parts):continue
    rows.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT)}")
(ROOT/"FREEZE_SHA256.txt").write_text("\n".join(rows)+"\n")
print(f"Wrote {len(rows)} hashes")
