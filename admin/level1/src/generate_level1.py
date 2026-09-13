#!/usr/bin/env python3
"""
Generator script for Level 1: Network Scope & Perimeter Reconnaissance
Case File: EVIDENCE 05 - THE ATTENTION ECONOMY / THE MONEY TRAIL
Threat Actor: $CYBERLEEK (August 2026 GTA VI Leak Monetization Trail)
Dual-emits network_scope.txt to admin/level1/uploads/ and user/level1/files/.
"""

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ADMIN_LEVEL1_DIR = SCRIPT_DIR.parent
ADMIN_UPLOADS_DIR = ADMIN_LEVEL1_DIR / "uploads"
ROUND5_DIR = ADMIN_LEVEL1_DIR.parent.parent
USER_FILES_DIR = ROUND5_DIR / "user" / "level1" / "files"

TARGET_HOST = "target.cyberleek.lan"
FALLBACK_HOST = "127.0.0.1"
SERVICE_PORT = 9042

NETWORK_SCOPE_CONTENT = f"""====================================================================
CYBERLEEK INCIDENT RESPONSE // PERIMETER RECONNAISSANCE SCOPE
CASE FILE: EVIDENCE 05 - THE ATTENTION ECONOMY / THE MONEY TRAIL
TARGET IDENTIFIER: $CYBERLEEK Auxiliary Transaction Gateway
====================================================================

OPERATIONAL BRIEFING:
Forensic analysis of the August 2026 GTA VI leak monetization campaign
has isolated dedicated transaction settlement infrastructure operated
by threat actor $CYBERLEEK. While public web services have been purged,
an auxiliary transaction gateway remains operational on a high-order port.

INVESTIGATION OBJECTIVES:
1. Conduct full-spectrum TCP reconnaissance scanning against the target.
2. Locate and verify the active auxiliary gateway listening on port {SERVICE_PORT}.
3. Connect and interrogate the diagnostic service banner to extract the
   initial reconnaissance telemetry signature.

TARGET SPECIFICATION:
- Network Identifier : {TARGET_HOST}
- Local/Loopback IP  : {FALLBACK_HOST}
- Port Scope         : Non-standard TCP service ports (1024 - 65535)
- Active Service     : Auxiliary Transaction Gateway ({SERVICE_PORT}/TCP)

RECOMMENDED RECONNAISSANCE METHODOLOGY:
- Full port discovery:
    nmap -sS -p- --min-rate 1000 -T4 {FALLBACK_HOST}
- Service banner inspection:
    nmap -sV -sC -p {SERVICE_PORT} {FALLBACK_HOST}

FLAG RECOVERY NOTE:
The Level 1 diagnostic signature is transmitted directly inside the
gateway's initial ASCII connection banner upon TCP socket handshake.

STATUS: TARGET PERIMETER ACTIVE
====================================================================
"""


def generate_challenge():
    """Generates Level 1 network scope files into admin and user directories."""
    print("[*] Generating Level 1: Network Scope Artifacts...")
    ADMIN_UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    USER_FILES_DIR.mkdir(parents=True, exist_ok=True)

    admin_file = ADMIN_UPLOADS_DIR / "network_scope.txt"
    user_file = USER_FILES_DIR / "network_scope.txt"

    admin_file.write_text(NETWORK_SCOPE_CONTENT, encoding="utf-8")
    user_file.write_text(NETWORK_SCOPE_CONTENT, encoding="utf-8")

    print(f"    [+] Emitted: {admin_file.relative_to(ROUND5_DIR)}")
    print(f"    [+] Emitted: {user_file.relative_to(ROUND5_DIR)}")


if __name__ == "__main__":
    generate_challenge()
