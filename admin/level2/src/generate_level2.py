#!/usr/bin/env python3
"""
Generator script for Level 2: Gateway Terminal Interaction & Operational Telemetry
Case File: EVIDENCE 05 - THE ATTENTION ECONOMY / THE MONEY TRAIL
Threat Actor: $CYBERLEEK (August 2026 GTA VI Leak Monetization Trail)
Dual-emits terminal_protocol.txt & session_telemetry.log to admin/level2/uploads/ and user/level2/files/.
"""

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ADMIN_LEVEL2_DIR = SCRIPT_DIR.parent
ADMIN_UPLOADS_DIR = ADMIN_LEVEL2_DIR / "uploads"
ROUND5_DIR = ADMIN_LEVEL2_DIR.parent.parent
USER_FILES_DIR = ROUND5_DIR / "user" / "level2" / "files"

SERVICE_PORT = 9042

TERMINAL_PROTOCOL = f"""====================================================================
CYBERLEEK TERMINAL PROTOCOL // INTERACTION SPECIFICATIONS
CASE FILE: EVIDENCE 05 - THE ATTENTION ECONOMY / THE MONEY TRAIL
TARGET PORT: {SERVICE_PORT}/TCP
====================================================================

PROTOCOL SUMMARY:
The $CYBERLEEK Auxiliary Transaction Gateway is a raw TCP streaming
daemon. Unlike HTTP/REST services, it accepts line-buffered ASCII text
directives terminated with standard newlines (\\n).

SECURITY HANDSHAKE REQUIREMENT:
The daemon operates with an active Handshake Guard. Raw connection drops
into pre-session state ('[PRE-SESSION]> '). To establish interactive
operator command mode, participants must transmit the session initiation
packet:
    INIT_TRANSACTION_SESSION

CONNECTION TOOLS:
1. Netcat (Direct interactive streaming):
   nc -nv 127.0.0.1 {SERVICE_PORT}
   
2. Ncat / Telnet (Line-buffered terminal alternatives):
   ncat 127.0.0.1 {SERVICE_PORT}
   telnet 127.0.0.1 {SERVICE_PORT}

3. Python Socket Automation:
   import socket
   s = socket.create_connection(('127.0.0.1', {SERVICE_PORT}))
   # Step 1: Complete Handshake
   s.sendall(b'INIT_TRANSACTION_SESSION\\n')
   # Step 2: Issue Directives
   s.sendall(b'HELP\\n')
   print(s.recv(4096).decode('utf-8'))

CORE RULES & BUFFER CONSTRAINTS:
- Directives must be non-empty and UTF-8 encoded.
- Maximum input threshold: 2048 bytes per line. Overrunning this limit
  triggers immediate defense termination.
- Discover available commands using the built-in 'HELP' directive.
- Unreleased maintenance/diagnostic routines can override default locks.

STATUS: OPERATIONAL PROTOCOL ACTIVE
====================================================================
"""

SESSION_TELEMETRY = """====================================================================
LEAKED DAEMON OPERATIONAL LOG DUMP // $CYBERLEEK NODE TELEMETRY
SOURCE: Intercepted Relay Node Cache (August 2026)
LOG CHANNEL: escrow-relay-node-09.internal.net
====================================================================

[2026-08-16 02:41:10.104] [INFO] [HANDSHAKE] Inbound TCP connection accepted from relay 10.14.88.2:51240
[2026-08-16 02:41:10.882] [INFO] [HANDSHAKE] Initiation packet received: 'INIT_TRANSACTION_SESSION'
[2026-08-16 02:41:10.890] [AUTH] Session bus granted. Active mode: OPERATOR_CONSOLE
[2026-08-16 02:41:22.019] [WARN] [SECURITY] Public HTTP frontends disconnected due to law enforcement attention on GTA VI drops.
[2026-08-16 02:41:35.441] [DEBUG] [TELEMETRY] Operator executed diagnostic maintenance directive: 'STATUS'
[2026-08-16 02:41:35.450] [INFO] [STATUS] Diagnostic routine executed. Primary escrow reserve online.
[2026-08-16 02:41:35.452] [INFO] [STATUS] Telemetry override token generated and passed to operator.
[2026-08-16 02:41:40.118] [AUTH] Redirected session to Operator Gatekeeper Authentication Portal ('AUTH').
[2026-08-16 02:41:50.002] [NOTICE] Inbound transactions routed to sequestered escrow ledger.
[2026-08-16 02:42:01.309] [SESSION] Connection terminated cleanly.
====================================================================
"""


def generate_challenge():
    """Generates Level 2 protocol instructions and leaked session telemetry log."""
    print("[*] Generating Level 2: Terminal Protocol Artifacts...")
    ADMIN_UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    USER_FILES_DIR.mkdir(parents=True, exist_ok=True)

    # 1. terminal_protocol.txt
    (ADMIN_UPLOADS_DIR / "terminal_protocol.txt").write_text(TERMINAL_PROTOCOL, encoding="utf-8")
    (USER_FILES_DIR / "terminal_protocol.txt").write_text(TERMINAL_PROTOCOL, encoding="utf-8")

    # 2. session_telemetry.log
    (ADMIN_UPLOADS_DIR / "session_telemetry.log").write_text(SESSION_TELEMETRY, encoding="utf-8")
    (USER_FILES_DIR / "session_telemetry.log").write_text(SESSION_TELEMETRY, encoding="utf-8")

    print(f"    [+] Emitted: terminal_protocol.txt -> uploads/ & files/")
    print(f"    [+] Emitted: session_telemetry.log -> uploads/ & files/")


if __name__ == "__main__":
    generate_challenge()
