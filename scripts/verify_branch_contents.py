from pathlib import Path
import hashlib
import sys

root = Path.cwd()
workflows = sorted((root / ".github" / "workflows").glob("*.yml"))

if not workflows:
    raise SystemExit("No active workflow files found.")

print("Active workflows:")
for path in workflows:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    print(f"- {path}: {digest}")

fixture = root / "fixture"
print(f"Fixture present: {fixture.exists()}")
