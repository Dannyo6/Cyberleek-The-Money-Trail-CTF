#!/usr/bin/env python3
"""
Generator script for Level 3: Operator Gatekeeper Authentication Bypass & WAF Evasion
Case File: EVIDENCE 05 - THE ATTENTION ECONOMY / THE MONEY TRAIL
Threat Actor: $CYBERLEEK (August 2026 GTA VI Leak Monetization Trail)
Dual-emits auth_audit.txt & sanitizer_rules.txt to admin/level3/uploads/ and user/level3/files/.
"""

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ADMIN_LEVEL3_DIR = SCRIPT_DIR.parent
ADMIN_UPLOADS_DIR = ADMIN_LEVEL3_DIR / "uploads"
ROUND5_DIR = ADMIN_LEVEL3_DIR.parent.parent
USER_FILES_DIR = ROUND5_DIR / "user" / "level3" / "files"

AUTH_AUDIT = """====================================================================
CYBERLEEK SECURITY AUDIT // OPERATOR AUTHENTICATION DIAGNOSTICS
CASE FILE: EVIDENCE 05 - THE ATTENTION ECONOMY / THE MONEY TRAIL
TARGET SUBSYSTEM: Operator Gatekeeper Portal ('AUTH')
====================================================================

SYSTEM ARCHITECTURE:
To query the internal $CYBERLEEK transaction ledger, participants must
clear the Operator Gatekeeper Authentication Portal ('AUTH').

Standard operator access requires a registered Operator Key ID (e.g.,
'OP-0992'). In the absence of valid syndicate credentials, participants
must analyze the query verification mechanism and active WAF rules.

VULNERABILITY CHARACTERISTICS:
- Backend Database: SQLite (`cyberleek_ledger.db`).
- Query Formulation: Dynamic SQL string concatenation without input
  parameterization.
- Error Behavior: Verbose SQLite database OperationalErrors are returned
  over the socket connection, providing immediate syntax feedback.

OBJECTIVE:
Formulate an authentication bypass payload that evades the input WAF
filter and manipulates the SQL Boolean evaluation logic, unlocking
administrative operator clearance without a known key.
====================================================================
"""

SANITIZER_RULES = """-- ====================================================================
-- $CYBERLEEK APPLICATION GATEWAY // INPUT SANITIZER SPECIFICATION
-- RECOVERED FROM DEPLOYMENT REPOSITORY
-- ====================================================================

-- 1. Active Web Application Firewall (WAF) Rule:
-- Prohibited Characters:
--   - ASCII 0x20 (Raw Space ' ')
--   - ASCII 0x09 (Horizontal Tab)
-- Naive payloads like "' OR 1=1 --" are automatically intercepted.
--
-- Security Note:
-- "Developers must use parameter binding. If concatenating strings,
-- ensure that whitespace substitution via SQL block comments (/**/)
-- does not allow logic manipulation."

-- 2. Relevant Schema Fragments:
CREATE TABLE node_operators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operator_id TEXT UNIQUE,
    handle TEXT,
    clearance_level INTEGER,
    role TEXT,
    signature_hash TEXT
);

CREATE TABLE public_ledger (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tx_id TEXT UNIQUE,
    sender TEXT,
    recipient TEXT,
    amount TEXT,
    memo TEXT
);

-- [!] NOTICE: Primary escrow reserves and high-value transaction drops
-- are sequestered in dedicated internal tables.
-- ====================================================================
"""


def generate_challenge():
    """Generates Level 3 audit notes and sanitizer rules snippet."""
    print("[*] Generating Level 3: Operator Authentication Bypass Artifacts...")
    ADMIN_UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    USER_FILES_DIR.mkdir(parents=True, exist_ok=True)

    # 1. auth_audit.txt
    (ADMIN_UPLOADS_DIR / "auth_audit.txt").write_text(AUTH_AUDIT, encoding="utf-8")
    (USER_FILES_DIR / "auth_audit.txt").write_text(AUTH_AUDIT, encoding="utf-8")

    # 2. sanitizer_rules.txt
    (ADMIN_UPLOADS_DIR / "sanitizer_rules.txt").write_text(SANITIZER_RULES, encoding="utf-8")
    (USER_FILES_DIR / "sanitizer_rules.txt").write_text(SANITIZER_RULES, encoding="utf-8")

    print(f"    [+] Emitted: auth_audit.txt -> uploads/ & files/")
    print(f"    [+] Emitted: sanitizer_rules.txt -> uploads/ & files/")


if __name__ == "__main__":
    generate_challenge()
