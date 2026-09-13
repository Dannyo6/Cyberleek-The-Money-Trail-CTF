#!/usr/bin/env python3
"""
Generator script for Level 4: Escrow Ledger Exfiltration & Multi-Column UNION Injection
Case File: EVIDENCE 05 - THE ATTENTION ECONOMY / THE MONEY TRAIL
Threat Actor: $CYBERLEEK (August 2026 GTA VI Leak Monetization Trail)
Dual-emits escrow_investigation.txt to admin/level4/uploads/ and user/level4/files/.
"""

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ADMIN_LEVEL4_DIR = SCRIPT_DIR.parent
ADMIN_UPLOADS_DIR = ADMIN_LEVEL4_DIR / "uploads"
ROUND5_DIR = ADMIN_LEVEL4_DIR.parent.parent
USER_FILES_DIR = ROUND5_DIR / "user" / "level4" / "files"

ESCROW_INVESTIGATION = """====================================================================
CYBERLEEK FORENSIC INTELLIGENCE // ESCROW EXFILTRATION DIRECTIVE
CASE FILE: EVIDENCE 05 - THE ATTENTION ECONOMY / THE MONEY TRAIL
TARGET SUBSYSTEM: Escrow Ledger Query Console & Sequestered Vault
====================================================================

INTELLIGENCE ASSESSMENT:
Authenticated operator sessions gain access to the Escrow Transaction
Query Console ('QUERY'). Standard lookups against `public_ledger` by
Transaction ID (`tx_id`) project 4 data columns:
  Column 1: tx_id (TEXT)
  Column 2: sender (TEXT)
  Column 3: recipient (TEXT)
  Column 4: memo (TEXT)

SEQUESTERED REPOSITORY SPECIFICATION:
Staging configuration traces identify the primary escrow distribution
table storing the monetization reserves and master transaction key:
  Table Name: cyberleek_escrow_ledger
  Columns   : id, tx_id, sender, recipient, amount, secret_clearance

The authoritative case flag is stored within the `secret_clearance`
column of the primary GTA VI monetization drop transaction.

EXPLOITATION STRATEGY:
1. Column Count & Projection Discovery:
   Probe the active query using `ORDER BY <N> --` or trial null projections
   to confirm the query requires exactly 4 columns.
2. Multi-Column UNION Formulation:
   Construct a SQL `UNION SELECT` query matching the 4-column projection,
   pulling `tx_id`, `sender`, `recipient`, and `secret_clearance` from
   the hidden `cyberleek_escrow_ledger` table.
3. Payload Construction:
   Escape the string delimiter and terminate trailing syntax with `--`.

FLAG IDENTIFICATION:
The exfiltrated token strictly follows the authoritative format:
CYBERLEEK{...}

POST-ROUND TRANSITION:
"The money trail ends at the final artifact. Whatever is inside it was deliberately protected."
====================================================================
"""


def generate_challenge():
    """Generates Level 4 escrow investigation briefing artifact."""
    print("[*] Generating Level 4: Escrow Investigation Artifacts...")
    ADMIN_UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    USER_FILES_DIR.mkdir(parents=True, exist_ok=True)

    # escrow_investigation.txt
    (ADMIN_UPLOADS_DIR / "escrow_investigation.txt").write_text(ESCROW_INVESTIGATION, encoding="utf-8")
    (USER_FILES_DIR / "escrow_investigation.txt").write_text(ESCROW_INVESTIGATION, encoding="utf-8")

    print(f"    [+] Emitted: escrow_investigation.txt -> uploads/ & files/")


if __name__ == "__main__":
    generate_challenge()
