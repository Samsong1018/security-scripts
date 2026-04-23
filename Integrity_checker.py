import hashlib
import json
import sys
from pathlib import Path

FOLDER = Path('./example_files')
BASELINE_FILE = Path('./baseline.json')


def hash_file(file_path: Path) -> str:
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()


def hash_folder(folder: Path) -> dict[str, str]:
    hashes = {}
    for file_path in sorted(folder.rglob('*')):
        if file_path.is_file():
            rel = str(file_path.relative_to(folder))
            hashes[rel] = hash_file(file_path)
    return hashes


def save_baseline(hashes: dict[str, str]) -> None:
    BASELINE_FILE.write_text(json.dumps(hashes, indent=2))
    print(f"Baseline saved → {BASELINE_FILE}  ({len(hashes)} files)")
    for path in sorted(hashes):
        print(f"  {hashes[path][:16]}…  {path}")


def check_integrity(folder: Path) -> None:
    baseline: dict[str, str] = json.loads(BASELINE_FILE.read_text())
    current = hash_folder(folder)

    modified = [f for f in current if f in baseline and current[f] != baseline[f]]
    added    = [f for f in current if f not in baseline]
    removed  = [f for f in baseline if f not in current]

    if not any([modified, added, removed]):
        print("[OK] No changes detected — folder integrity verified.")
        return

    print("[ALERT] Changes detected!\n")
    if modified:
        print(f"  MODIFIED ({len(modified)}):")
        for f in modified:
            print(f"    {f}")
    if added:
        print(f"  ADDED ({len(added)}):")
        for f in added:
            print(f"    {f}")
    if removed:
        print(f"  REMOVED ({len(removed)}):")
        for f in removed:
            print(f"    {f}")


# --save-baseline flag forces a fresh baseline even if one exists
force_baseline = '--save-baseline' in sys.argv

if force_baseline or not BASELINE_FILE.exists():
    reason = "re-saving baseline" if force_baseline else "no baseline found — saving now"
    print(f"[{reason.upper()}]")
    save_baseline(hash_folder(FOLDER))
else:
    print(f"Checking '{FOLDER}' against baseline…\n")
    check_integrity(FOLDER)
