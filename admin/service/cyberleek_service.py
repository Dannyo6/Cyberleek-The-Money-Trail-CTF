#!/usr/bin/env python3
"""
CYBERLEEK Hardened Auxiliary Transaction Gateway Daemon
Evidence 05: The Attention Economy / The Money Trail
Domain: Network Reconnaissance, TCP Socket Interaction, WAF-filtered SQL Injection (Levels 1-4)
Threat Actor: $CYBERLEEK (August 2026 GTA VI Leak Monetization Trail)

Hardening Features:
- Multi-threaded TCP daemon on port 9042 using socketserver.ThreadingMixIn + TCPServer
- Rate Limiting: Max 10 requests per minute per IP to block dumb fuzzers
- Handshake Guard: Requires 'INIT_TRANSACTION_SESSION' before interactive prompt is unlocked
- WAF Filter on Auth Input: Rejects raw ASCII spaces and naive injections; enforces comment-based spaces (/**/)
- Structured Schema Protection: 4-column UNION projection required to exfiltrate cyberleek_escrow_ledger
"""

import os
import re
import sqlite3
import socketserver
import sys
import threading
import time
from collections import defaultdict
from pathlib import Path

BIND_HOST = os.environ.get("BIND_HOST", "0.0.0.0")
BIND_PORT = int(os.environ.get("BIND_PORT", "9042"))

FLAG_L1 = "CYBERLEEK{p0rt_9042_tr4ns4ct10n_g4t3}"
FLAG_L2 = "CYBERLEEK{0p3r4t0r_t3l3m3try_0v3rr1d3}"
FLAG_L3 = "CYBERLEEK{g4t3k33p3r_byp455_4cqu1r3d}"
FLAG_L4 = "CYBERLEEK{M0n3y_5@Qz}"

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "cyberleek_ledger.db"

# Rate Limiter State: IP -> list of request timestamps
RATE_LIMIT_PER_MIN = int(os.environ.get("RATE_LIMIT_PER_MIN", "10"))
RATE_LIMIT_WINDOW = 60.0
RATE_LIMIT_TRACKER = defaultdict(list)
RATE_LIMIT_LOCK = threading.Lock()

ASCII_BANNER = rf"""
======================================================================
  ____ _  _ ___  ____ ____ _    ____ ____ _  _ 
  |    \  / |__] |___ |--< |    |___ |___ |_/  
  |___  \/  |__] |___ |  \ |___ |___ |___ | \_ 
                                                
  $CYBERLEEK // AUXILIARY TRANSACTION GATEWAY (HARDENED)
  "Every transaction leaves a trace."
  "This is where attention becomes currency."
  AUGUST 2026 // ESCROW MONETIZATION NETWORK
======================================================================
[+] SERVICE STATUS: ONLINE
[+] GATEWAY PORT: 9042/TCP
[+] DIAGNOSTIC SIGNATURE: {FLAG_L1}
======================================================================
[!] HANDSHAKE GUARD ACTIVE: Transaction bus locked in pre-session state.
    Transmit initiation packet 'INIT_TRANSACTION_SESSION' to proceed.
======================================================================
"""


def check_rate_limit(client_ip: str) -> bool:
    """Enforces per-IP request frequency threshold (default 10 req/min)."""
    if os.environ.get("RATE_LIMIT_DISABLED") == "1":
        return True
    now = time.time()
    with RATE_LIMIT_LOCK:
        timestamps = RATE_LIMIT_TRACKER[client_ip]
        # Prune timestamps outside window
        RATE_LIMIT_TRACKER[client_ip] = [t for t in timestamps if now - t < RATE_LIMIT_WINDOW]
        if len(RATE_LIMIT_TRACKER[client_ip]) >= RATE_LIMIT_PER_MIN:
            return False
        RATE_LIMIT_TRACKER[client_ip].append(now)
        return True


def init_ledger_database():
    """Initializes SQLite database with node_operators, public_ledger, and cyberleek_escrow_ledger."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Node Operators Table (Level 3 Gatekeeper Target)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS node_operators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operator_id TEXT UNIQUE,
            handle TEXT,
            clearance_level INTEGER,
            role TEXT,
            signature_hash TEXT
        );
    """)

    # 2. Public Ledger Table (Level 4 Standard Lookup Target - 4 Columns)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS public_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tx_id TEXT UNIQUE,
            sender TEXT,
            recipient TEXT,
            amount TEXT,
            memo TEXT
        );
    """)

    # 3. Sequestered Hidden Escrow Ledger (Level 4 UNION Target - Holds Flag)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyberleek_escrow_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tx_id TEXT UNIQUE,
            sender TEXT,
            recipient TEXT,
            amount TEXT,
            secret_clearance TEXT
        );
    """)

    # Seed node operators
    cursor.execute("SELECT COUNT(*) FROM node_operators;")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO node_operators (operator_id, handle, clearance_level, role, signature_hash) VALUES (?, ?, ?, ?, ?);",
            [
                ("OP-0992", "cyb3r_v4ult_m4st3r", 4, "Lead Escrow Broker", "sha256:7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069"),
                ("OP-1402", "attention_broker_x", 3, "Traffic Monetization Specialist", "sha256:9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"),
                ("OP-8821", "leek_syndicate_lead", 5, "Syndicate Operations Lead", "sha256:60303ae22b998861bce3b28f33eec1be758a213c86c93c0764b9691811097851"),
                ("OP-3310", "escrow_settlement_bot", 2, "Automated Settlement Engine", "sha256:4a44dc15364204a80fe80e9039455cc1608281820fe2b24f1e5233ade6af1dd5")
            ]
        )

    # Seed public ledger
    cursor.execute("SELECT COUNT(*) FROM public_ledger;")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO public_ledger (tx_id, sender, recipient, amount, memo) VALUES (?, ?, ?, ?, ?);",
            [
                ("TX-1001", "cold_wallet_alpha", "crypto_mixer_relay_01", "250.00 BTC", "GTA-VI-LEAK-SRC-BOUNTY-01"),
                ("TX-1002", "syndicate_treasury", "darknet_escrow_alpha", "410.50 BTC", "EXPLOIT-PAYLOAD-BROKERAGE"),
                ("TX-1003", "offshore_holdings", "anon_wallet_7721", "120.00 BTC", "ATTENTION_ECONOMY_MONETIZE_P1"),
                ("TX-1004", "escrow_pool_main", "operator_payout_pool", "85.25 BTC", "RESERVE_PAYROLL_AUG_2026")
            ]
        )

    # Seed sequestered escrow ledger with authoritative flag
    cursor.execute("SELECT COUNT(*) FROM cyberleek_escrow_ledger;")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO cyberleek_escrow_ledger (tx_id, sender, recipient, amount, secret_clearance) VALUES (?, ?, ?, ?, ?);",
            [
                ("ESCROW-TX-9901", "GTA_VI_UNRELEASED_DROP_RESERVE", "PRIMARY_LEEK_TREASURY", "5000.00 BTC", FLAG_L4),
                ("ESCROW-TX-9902", "COLD_STORAGE_DEPOSIT", "ESCROW_VAULT_RESERVE", "12500.00 BTC", "RESTRICTED_ESCROW_SEAL_LOCKED"),
                ("ESCROW-TX-9903", "KEYHOLDER_STAKING_POOL", "CONSENSUS_MULTI_SIG", "3200.00 BTC", "PENDING_KEYHOLDER_CONSENSUS")
            ]
        )

    conn.commit()
    conn.close()


class HardenedTerminalHandler(socketserver.StreamRequestHandler):
    """Interactive socket session handler with Rate Limiting, Handshake Guard, and WAF Filter."""

    def safe_send(self, text):
        try:
            if isinstance(text, str):
                self.wfile.write(text.encode("utf-8"))
            else:
                self.wfile.write(text)
            self.wfile.flush()
        except Exception:
            pass

    def read_client_line(self, allow_empty=False):
        try:
            chunk = self.rfile.readline(2050)
            if not chunk:
                return None, False

            if len(chunk) > 2048:
                err = (
                    "\n[-] SECURITY COUNTERMEASURE: Buffer threshold exceeded (>2048 bytes).\n"
                    "[-] Payload rejected. Session terminated by CYBERLEEK Defense Bus.\n"
                )
                self.safe_send(err)
                return None, False

            try:
                decoded = chunk.decode("utf-8")
            except UnicodeDecodeError:
                err = (
                    "\n[-] PROTOCOL FAULT: Malformed non-UTF-8 character stream detected.\n"
                    "[-] Terminal session terminated by CYBERLEEK Dispatch Subsystem.\n"
                )
                self.safe_send(err)
                return None, False

            val = decoded.strip()
            if not val and not allow_empty:
                err = (
                    "\n[-] DIRECTIVE REJECTED: Null or whitespace-only directive submitted.\n"
                    "[-] CYBERLEEK security policy requires valid directive. Session terminated.\n"
                )
                self.safe_send(err)
                return None, False

            return val, True

        except (ConnectionResetError, BrokenPipeError, TimeoutError):
            return None, False
        except Exception as e:
            self.safe_send(f"\n[-] I/O FAULT: {e}\n")
            return None, False

    def handle(self):
        client_ip = self.client_address[0]

        # 1. Enforce IP Rate Limiting
        if not check_rate_limit(client_ip):
            self.safe_send("\n[-] RATE LIMIT EXCEEDED: Maximum 10 requests per minute per IP. Session terminated.\n")
            return

        # 2. Emit Banner & Handshake Notice
        self.safe_send(ASCII_BANNER)

        # 3. Handshake Guard Loop
        handshake_verified = False
        while not handshake_verified:
            self.safe_send("\n[PRE-SESSION]> ")
            packet, ok = self.read_client_line(allow_empty=False)
            if not ok:
                return

            if packet.upper() in ("INIT_TRANSACTION_SESSION", "INIT"):
                handshake_verified = True
                self.safe_send("\n[+] HANDSHAKE ACCEPTED: Interactive transaction gateway console unlocked.\n")
                break
            elif packet.upper() in ("EXIT", "QUIT"):
                self.safe_send("[+] Session aborted.\n")
                return
            else:
                self.safe_send(
                    f"\n[-] HANDSHAKE FAILED: Directive '{packet}' rejected.\n"
                    "[-] Gateway bus requires 'INIT_TRANSACTION_SESSION' to establish session.\n"
                )

        # 4. Interactive Command Loop
        while True:
            try:
                self.safe_send("\nCYBERLEEK-GW> ")
                cmd, ok = self.read_client_line(allow_empty=False)
                if not ok:
                    break

                upper_cmd = cmd.upper()

                if upper_cmd == "HELP":
                    help_msg = (
                        "\n--- $CYBERLEEK AUXILIARY TRANSACTION GATEWAY COMMANDS ---\n"
                        "  PING     : Test auxiliary network latency\n"
                        "  SYSTEM   : Display node telemetry and threat actor status\n"
                        "  STATUS   : Diagnostic telemetry & maintenance check\n"
                        "  AUDIT    : Syndicate transaction audit inspection\n"
                        "  AUTH     : Operator Gatekeeper Authentication Portal\n"
                        "  QUERY    : Public ledger transaction query console\n"
                        "  CLEAR    : Clear terminal screen buffer\n"
                        "  EXIT     : Terminate active gateway session\n"
                    )
                    self.safe_send(help_msg)

                elif upper_cmd == "PING":
                    self.safe_send("\n[+] PONG - Gateway node response latency: 0.14ms [STABLE]\n")

                elif upper_cmd == "SYSTEM":
                    telemetry = (
                        "\n[+] NODE TELEMETRY // $CYBERLEEK NETWORK:\n"
                        "    Node Identifier : CYBERLEEK-AUX-RELAY-09\n"
                        "    Campaign Context: August 2026 GTA VI Leak Monetization\n"
                        "    Subsystem       : Escrow Settlement & Transaction Tracking\n"
                        "    Protection Mode : WAF_WHITESPACE_FILTER_ENABLED\n"
                    )
                    self.safe_send(telemetry)

                elif upper_cmd == "CLEAR":
                    self.safe_send("\033[2J\033[H")

                elif upper_cmd in ("STATUS", "AUDIT"):
                    # Level 2 Flag & automatic bridge to Authentication Gateway
                    status_report = f"""
======================================================================
[+] EXECUTING OPERATIONAL DIAGNOSTIC TELEMETRY...
[+] NODE: GTA-VI-ESCROW-MONETIZATION-RELAY-09
[+] STATUS: OPERATIONAL // ATTENTION ECONOMY ESCROW ACTIVE
[+] THREAT ACTOR: $CYBERLEEK
[+] LEVEL 2 OVERRIDE FLAG: {FLAG_L2}
[+] NOTICE: Operator Authentication Gateway active on transaction bus.
======================================================================
"""
                    self.safe_send(status_report)
                    self.run_auth_gateway()

                elif upper_cmd in ("AUTH", "LOGIN", "GATEWAY"):
                    self.run_auth_gateway()

                elif upper_cmd in ("QUERY", "LEDGER", "TRANSACTIONS", "ESCROW"):
                    self.run_ledger_query()

                elif upper_cmd in ("EXIT", "QUIT"):
                    self.safe_send("\n[+] Closing gateway session. All traces logged.\n")
                    break

                else:
                    err = f"\n[-] Unknown directive: '{cmd}'. Enter 'HELP' for available command set.\n"
                    self.safe_send(err)

            except (ConnectionResetError, BrokenPipeError):
                break
            except Exception as e:
                self.safe_send(f"\n[-] Terminal Error: {e}\n")
                break

    def run_auth_gateway(self):
        """Level 3: SQLite Operator Authentication Gateway with WAF filter blocking raw spaces."""
        prompt_header = (
            "\n" + ("=" * 70) + "\n"
            + "CYBERLEEK OPERATOR GATEKEEPER // CREDENTIAL VERIFICATION (WAF PROTECTED)\n"
            + ("=" * 70) + "\n"
            + "Syndicate operator authorization key required.\n"
            + "[!] WAF POLICY: Raw ASCII whitespace (' ') is filtered.\n"
            + "(Type 'BACK' to return to gateway console)\n\n"
            + "Operator Key ID: "
        )
        self.safe_send(prompt_header)

        user_input, ok = self.read_client_line(allow_empty=False)
        if not ok:
            return

        if user_input.upper() == "BACK":
            self.safe_send("[-] Aborting operator authentication sequence.\n")
            return

        # WAF FILTER: Block raw ASCII whitespace and naive injection
        if " " in user_input or "\t" in user_input or "\r" in user_input:
            waf_err = (
                "\n[-] WAF VIOLATION DETECTED: Raw whitespace token rejected by syndicate input filter.\n"
                "[-] Directive dropped by security gatekeeper.\n"
            )
            self.safe_send(waf_err)
            return

        # VULNERABLE SQL QUERY (Vulnerable to comment-based spacing: /**/)
        conn = None
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            vulnerable_query = (
                "SELECT id, operator_id, handle, clearance_level, role FROM node_operators WHERE operator_id = '"
                + user_input
                + "';"
            )
            cursor.execute(vulnerable_query)
            operator_record = cursor.fetchone()

            if operator_record:
                op_id, handle, clearance, role = (
                    operator_record[1],
                    operator_record[2],
                    operator_record[3],
                    operator_record[4],
                )
                success_msg = f"""
======================================================================
[+] OPERATOR KEY VERIFIED: {handle} ({op_id})
[+] CLEARANCE LEVEL: {clearance} | ROLE: {role}
[+] GATEKEEPER AUTHENTICATION BYPASS CONFIRMED!
[+] LEVEL 3 FLAG: {FLAG_L3}
======================================================================
[+] Redirecting to Escrow Ledger Query Interface...
"""
                self.safe_send(success_msg)
                self.run_ledger_query()
            else:
                self.safe_send("\n[-] ACCESS DENIED: Operator ID not registered in escrow cluster.\n")

        except sqlite3.OperationalError as db_err:
            err_msg = f"\n[!] DATABASE ERROR: {db_err}\n[!] Query executed: {vulnerable_query}\n"
            self.safe_send(err_msg)
        except Exception as e:
            self.safe_send(f"\n[!] DATABASE FAULT: {e}\n")
        finally:
            if conn:
                try:
                    conn.close()
                except Exception:
                    pass

    def run_ledger_query(self):
        """Level 4: Transaction Record Query with 4-column UNION injection."""
        header = (
            "\n" + ("=" * 70) + "\n"
            + "CYBERLEEK ESCROW LEDGER // TRANSACTION QUERY CONSOLE\n"
            + ("=" * 70) + "\n"
            + "Public transaction tracking: TX-1001, TX-1002, TX-1003, TX-1004\n"
            + "Query schema projects: tx_id, sender, recipient, memo\n"
            + "Enter Transaction ID or type 'EXIT' to return to gateway console.\n"
        )
        self.safe_send(header)

        while True:
            self.safe_send("\nTransaction Query: ")
            query_input, ok = self.read_client_line(allow_empty=False)
            if not ok:
                break

            if query_input.upper() in ("EXIT", "QUIT", "BACK"):
                self.safe_send("[+] Returning to gateway terminal console.\n")
                break

            # VULNERABLE 4-COLUMN SQL LOOKUP QUERY (Target for UNION into cyberleek_escrow_ledger)
            conn = None
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                vulnerable_lookup = (
                    "SELECT tx_id, sender, recipient, memo FROM public_ledger WHERE tx_id = '"
                    + query_input
                    + "';"
                )
                cursor.execute(vulnerable_lookup)
                rows = cursor.fetchall()
                if rows:
                    out = "\n--- TRANSACTION RECORD SEARCH RESULTS ---\n"
                    for r in rows:
                        out += f"[+] TX ID     : {r[0]}\n    SENDER    : {r[1]}\n    RECIPIENT : {r[2]}\n"
                        if len(r) > 3 and r[3]:
                            out += f"    MEMO/DATA : {r[3]}\n"
                    out += "-----------------------------------------\n"
                    self.safe_send(out)
                else:
                    self.safe_send("\n[-] No ledger records matching specified Transaction ID.\n")

            except sqlite3.OperationalError as db_err:
                err_msg = f"\n[!] DATABASE ERROR: {db_err}\n[!] Query executed: {vulnerable_lookup}\n"
                self.safe_send(err_msg)
            except Exception as e:
                self.safe_send(f"\n[!] DATABASE FAULT: {e}\n")
            finally:
                if conn:
                    try:
                        conn.close()
                    except Exception:
                        pass


class ThreadedCyberleekServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True


def run_service(host=BIND_HOST, port=BIND_PORT):
    init_ledger_database()
    server = ThreadedCyberleekServer((host, port), HardenedTerminalHandler)
    print(f"[*] CYBERLEEK Hardened Auxiliary Gateway listening on {host}:{port} (TCP)...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down gateway daemon...")
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else BIND_HOST
    port = int(sys.argv[2]) if len(sys.argv) > 2 else BIND_PORT
    run_service(host, port)
