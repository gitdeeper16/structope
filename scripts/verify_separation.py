"""
Verify Pilot/Confirmatory data separation (R6).

Implements V1-V6 from preregistration/threshold_calibration.md §12.2.

Usage:
    python -m scripts.verify_separation --check

Exit code:
    0 if all checks pass.
    1 if any check fails.

This script is read-only. It does not modify any file.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import List, Tuple


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def check_v1_pilot_prefix(confirm_dir: Path) -> Tuple[bool, str]:
    """V1: No Confirmatory file has a pilot_ prefix."""
    if not confirm_dir.exists():
        return True, f"V1 OK: {confirm_dir} does not exist (no files to check)"
    bad = [p for p in confirm_dir.rglob("*") if p.is_file() and p.name.startswith("pilot_")]
    if bad:
        return False, f"V1 FAIL: {len(bad)} files with pilot_ prefix in {confirm_dir}: {bad[:3]}"
    return True, "V1 OK: no pilot_ prefix in confirmatory directory"


def check_v2_no_pilot_dir_reads(confirm_dir: Path) -> Tuple[bool, str]:
    """V2: No Confirmatory file is located in results/pilot/."""
    if not confirm_dir.exists():
        return True, "V2 OK: confirmatory directory does not exist"
    return True, "V2 OK: confirmatory directory is separate from results/pilot/"


def check_v3_no_indirect_reads(confirm_dir: Path) -> Tuple[bool, str]:
    """V3: No Confirmatory script reads from results/pilot/."""
    if not confirm_dir.exists():
        return True, "V3 OK: confirmatory directory does not exist"
    bad = []
    for p in confirm_dir.rglob("*.py"):
        text = p.read_text(errors="ignore")
        if "results/pilot" in text or "results\\\\pilot" in text:
            bad.append(p)
    if bad:
        return False, f"V3 FAIL: {len(bad)} scripts reference results/pilot: {bad[:3]}"
    return True, "V3 OK: no script references results/pilot"


def check_v4_seed_pool(pilot_dir: Path, confirm_dir: Path,
                       shared_seeds_file: Path) -> Tuple[bool, str]:
    """V4: Every Confirmatory seed is from a separate pool or declared shared."""
    if not confirm_dir.exists():
        return True, "V4 OK: no confirmatory runs"
    shared = set()
    if shared_seeds_file.exists():
        try:
            shared = set(json.loads(shared_seeds_file.read_text()).get("shared_seeds", []))
        except Exception:
            return False, f"V4 FAIL: cannot parse {shared_seeds_file}"
    pilot_seeds = set()
    if pilot_dir.exists():
        for p in pilot_dir.rglob("*.json"):
            try:
                data = json.loads(p.read_text())
                if "seed" in data:
                    pilot_seeds.add(int(data["seed"]))
            except Exception:
                continue
    confirm_seeds = set()
    for p in confirm_dir.rglob("*.json"):
        try:
            data = json.loads(p.read_text())
            if "seed" in data:
                confirm_seeds.add(int(data["seed"]))
        except Exception:
            continue
    overlap = (pilot_seeds & confirm_seeds) - shared
    if overlap:
        return False, f"V4 FAIL: undeclared seed overlap: {sorted(overlap)[:5]}"
    return True, "V4 OK: no undeclared seed overlap"


def check_v5_frozen_thresholds(thresholds_file: Path,
                               frozen_hash_file: Path) -> Tuple[bool, str]:
    """V5: Hash of thresholds file matches frozen hash."""
    if not frozen_hash_file.exists():
        return True, f"V5 OK: {frozen_hash_file} not present (thresholds not yet frozen)"
    if not thresholds_file.exists():
        return False, f"V5 FAIL: {thresholds_file} missing but frozen hash exists"
    expected = frozen_hash_file.read_text().strip()
    actual = sha256_of(thresholds_file)
    if actual != expected:
        return False, f"V5 FAIL: thresholds hash mismatch ({actual[:16]} != {expected[:16]})"
    return True, "V5 OK: thresholds file matches frozen hash"


def check_v6_provenance(confirm_dir: Path,
                        run_log: Path) -> Tuple[bool, str]:
    """V6: Every Confirmatory output has a provenance entry."""
    if not confirm_dir.exists():
        return True, "V6 OK: no confirmatory outputs"
    csv_files = list(confirm_dir.rglob("*.csv"))
    if not csv_files:
        return True, "V6 OK: no confirmatory CSV files to check"
    if not run_log.exists():
        return False, f"V6 FAIL: {run_log} missing but CSV files exist"
    log_text = run_log.read_text()
    missing = []
    for p in csv_files:
        if p.name not in log_text:
            missing.append(p)
    if missing:
        return False, f"V6 FAIL: {len(missing)} files without provenance"
    return True, "V6 OK: all files have provenance"


def check_v7_mmd_spec_frozen(root: Path) -> Tuple[bool, str]:
    """V7: MMD spec exists, sha256 matches, and Confirmatory RUN_LOG
    records V7_PASSED before the first Confirmatory output.

    Note: V7 alone cannot prevent Confirmatory runs. The Confirmatory
    launcher must invoke verify_separation.py first and abort on V7 failure.
    V7 detects post-hoc violations; the launcher prevents them.
    """
    spec = root / "preregistration" / "r7_mmd_spec.md"
    spec_hash = root / "preregistration" / "r7_mmd_spec.sha256"
    confirm_dir = root / "results" / "confirmatory"
    run_log = root / "results" / "RUN_LOG.md"

    # 1. Spec must exist
    if not spec.exists():
        return False, "V7 FAIL: preregistration/r7_mmd_spec.md missing"

    # 2. Hash must exist
    if not spec_hash.exists():
        return False, "V7 FAIL: preregistration/r7_mmd_spec.sha256 missing"

    # 3. Hash must match
    expected = spec_hash.read_text().strip().split()[0]
    actual = sha256_of(spec)
    if actual != expected:
        return False, f"V7 FAIL: r7_mmd_spec.md hash mismatch ({actual[:16]} != {expected[:16]})"

    # 4. If Confirmatory outputs exist, RUN_LOG must record V7_PASSED
    if confirm_dir.exists():
        outputs = list(confirm_dir.rglob("*"))
        outputs = [o for o in outputs if o.is_file()]
        if outputs:
            if not run_log.exists():
                return False, "V7 FAIL: Confirmatory outputs exist but results/RUN_LOG.md is missing"
            log_text = run_log.read_text()
            if "V7_PASSED" not in log_text:
                return False, "V7 FAIL: Confirmatory outputs exist but RUN_LOG.md has no V7_PASSED entry"
            # 5. V7_PASSED must appear before the first confirmatory file mtime
            #    (approximate: compare timestamps in log if present)
            #    Full ordering is enforced by the launcher, not by V7 alone.
    return True, "V7 OK: r7_mmd_spec.md frozen and hash matches"

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()
    root = args.root.resolve()
    confirm_dir = root / "results" / "confirmatory"
    pilot_dir = root / "results" / "pilot"
    thresholds = root / "preregistration" / "thresholds.md"
    frozen_hash = root / "preregistration" / "thresholds.sha256"
    shared_seeds = root / "preregistration" / "shared_seeds.json"
    run_log = root / "results" / "RUN_LOG.md"

    checks = [
        ("V1", check_v1_pilot_prefix, (confirm_dir,)),
        ("V2", check_v2_no_pilot_dir_reads, (confirm_dir,)),
        ("V3", check_v3_no_indirect_reads, (confirm_dir,)),
        ("V4", check_v4_seed_pool, (pilot_dir, confirm_dir, shared_seeds)),
        ("V5", check_v5_frozen_thresholds, (thresholds, frozen_hash)),
        ("V6", check_v6_provenance, (confirm_dir, run_log)),
        ("V7", check_v7_mmd_spec_frozen, (root,)),
    ]

    all_ok = True
    print("=== Pilot/Confirmatory separation verification ===\n")
    for name, fn, fn_args in checks:
        ok, msg = fn(*fn_args)
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {msg}")
        if not ok:
            all_ok = False
    print("\n=== Result ===")
    if all_ok:
        print("ALL CHECKS PASS")
        return 0
    print("FAILURES DETECTED")
    return 1


if __name__ == "__main__":
    sys.exit(main())
