#!/usr/bin/env python3
"""
Evidence Bundle Packaging & Distribution Utility for Round 5
Case File: EVIDENCE 05 - THE ATTENTION ECONOMY / THE MONEY TRAIL
Threat Actor: $CYBERLEEK
Bundles all participant materials in user/ into admin/evidence_bundle.zip
while strictly verifying zero leakage of admin files, solutions, code, or databases.
"""

import hashlib
import os
import sys
import zipfile
from pathlib import Path

ADMIN_DIR = Path(__file__).resolve().parent
ROUND5_DIR = ADMIN_DIR.parent
USER_DIR = ROUND5_DIR / "user"
BUNDLE_OUTPUT = ADMIN_DIR / "evidence_bundle.zip"

EXCLUDED_EXTENSIONS = [".py", ".pyc", ".db", ".sqlite", ".sqlite3"]
EXCLUDED_KEYWORDS = ["admin", "solution", "__pycache__", "target_config"]


def should_exclude(rel_path: str) -> bool:
    """Checks if a relative path violates participant bundle isolation rules."""
    lower_path = rel_path.lower().replace("\\", "/")
    for ext in EXCLUDED_EXTENSIONS:
        if lower_path.endswith(ext):
            return True
    for kw in EXCLUDED_KEYWORDS:
        if kw in lower_path:
            return True
    return False


def run_generators():
    """Invokes each level's generator script to refresh artifacts."""
    print("[*] Running generator suite for Levels 1–4...")
    generators = [
        ADMIN_DIR / "level1" / "src" / "generate_level1.py",
        ADMIN_DIR / "level2" / "src" / "generate_level2.py",
        ADMIN_DIR / "level3" / "src" / "generate_level3.py",
        ADMIN_DIR / "level4" / "src" / "generate_level4.py",
    ]

    for gen in generators:
        if not gen.exists():
            raise FileNotFoundError(f"Missing generator script: {gen}")
        sys.path.insert(0, str(gen.parent))
        module_name = gen.stem
        if module_name in sys.modules:
            del sys.modules[module_name]
        module = __import__(module_name)
        module.generate_challenge()


def verify_required_artifacts():
    """Verifies that all required participant artifacts are present."""
    required = [
        USER_DIR / "ROUND5_PARTICIPANT_PREREQUISITES.md",
        USER_DIR / "level1" / "challenge.md",
        USER_DIR / "level1" / "files" / "network_scope.txt",
        USER_DIR / "level2" / "challenge.md",
        USER_DIR / "level2" / "files" / "terminal_protocol.txt",
        USER_DIR / "level2" / "files" / "session_telemetry.log",
        USER_DIR / "level3" / "challenge.md",
        USER_DIR / "level3" / "files" / "auth_audit.txt",
        USER_DIR / "level3" / "files" / "sanitizer_rules.txt",
        USER_DIR / "level4" / "challenge.md",
        USER_DIR / "level4" / "files" / "escrow_investigation.txt",
    ]
    missing = [str(p.relative_to(ROUND5_DIR)) for p in required if not p.exists()]
    if missing:
        raise RuntimeError(f"Missing required participant artifacts: {missing}")


def build_evidence_bundle():
    """Archives user/ into evidence_bundle.zip with strict zero-leak audit."""
    print("\n" + "=" * 75)
    print("ROUND 5: EVIDENCE 05 // PACKAGING PARTICIPANT EVIDENCE BUNDLE")
    print("=" * 75)

    # 1. Run generators and ensure user/ is populated
    run_generators()
    verify_required_artifacts()

    # 2. Package zip file
    bundled_files = []
    with zipfile.ZipFile(BUNDLE_OUTPUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(USER_DIR):
            for f in sorted(files):
                full_path = Path(root) / f
                rel_to_round5 = full_path.relative_to(ROUND5_DIR).as_posix()

                if should_exclude(rel_to_round5):
                    print(f"    [!] EXCLUDED VIOLATION: {rel_to_round5}")
                    continue

                zf.write(full_path, arcname=rel_to_round5)
                bundled_files.append((full_path, rel_to_round5))

    # 3. Print Manifest
    print(f"\n[+] Successfully generated evidence bundle: {BUNDLE_OUTPUT.name}")
    print("-" * 75)
    print(f"{'ARCHIVED RELATIVE PATH':<45} | {'SIZE':<8} | {'SHA256 (PREFIX)'}")
    print("-" * 75)
    for full_path, arcname in bundled_files:
        data = full_path.read_bytes()
        sha = hashlib.sha256(data).hexdigest()
        print(f"{arcname:<45} | {len(data):<8} | {sha[:16]}...")

    bundle_data = BUNDLE_OUTPUT.read_bytes()
    bundle_sha = hashlib.sha256(bundle_data).hexdigest()
    print("-" * 75)
    print(f"[+] Output Archive : {BUNDLE_OUTPUT.relative_to(ROUND5_DIR)}")
    print(f"[+] Archive Size   : {len(bundle_data)} bytes")
    print(f"[+] Archive SHA256 : {bundle_sha}")
    print("=" * 75 + "\n")
    return bundle_sha


if __name__ == "__main__":
    build_evidence_bundle()
