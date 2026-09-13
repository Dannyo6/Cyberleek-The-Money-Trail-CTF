# Round 05: Participant Environment & Tooling Prerequisites
**Case File: EVIDENCE 05 - THE ATTENTION ECONOMY / THE MONEY TRAIL**

> [!NOTE]
> **Participant Guidance Document:** This guide outlines the operational environment and required security utilities for investigating threat actor `$CYBERLEEK`'s transaction tracking and unreleased escrow infrastructure. Do not attempt disruptive attacks (DDoS or host exploitation); all objectives are achieved through reconnaissance, protocol interaction, and database query analysis.

---

## 1. Operational Context & Architecture

Round 05 (**THE ATTENTION ECONOMY / THE MONEY TRAIL**) tracks the financial and operational monetization trail of the August 2026 GTA VI leak:

- **Target Service:** Hardened auxiliary transaction gateway listening on TCP port `9042`.
- **Target Addressing:** `target.cyberleek.lan:9042` or `127.0.0.1:9042`.
- **Communication Protocol:** Raw bidirectional line-buffered TCP text streaming.
- **Backend Storage:** Local SQLite transaction and escrow ledger (`cyberleek_ledger.db`).
- **Security Defenses:**
  - Connection Rate Limiting: Max 10 requests per minute per IP to block dumb fuzzers.
  - Handshake Guard: Requires an exact session initiation handshake (`INIT_TRANSACTION_SESSION`) before unlocking the command console.
  - Gateway Input WAF: Filters raw whitespace characters (` `) on sensitive authentication inputs.
  - Buffer Limits: Strict 2048-byte line threshold.

---

## 2. Recommended Operating Environment

- **Operating System:** Kali Linux, Parrot Security OS, Ubuntu 22.04/24.04 LTS, Debian, macOS, or Windows 10/11 running WSL2.
- **Terminal Shell:** Bash, Zsh, or PowerShell.
- **Network Interface:** Local loopback interface (`127.0.0.1`) or direct lab VPN/subnet bridge.

---

## 3. Recommended Participant Tooling Checklist

| Tool | Category / Purpose | Verification Command / Syntax Example |
| :--- | :--- | :--- |
| **Nmap** | Full-spectrum port scanning, high-port identification, service banner interrogation | `nmap -sS -p- --min-rate 1000 -T4 <TARGET_IP>`<br>`nmap -sV -sC -p 9042 <TARGET_IP>` |
| **RustScan** *(Optional)* | High-speed multi-threaded port scanner across all 65,535 ports | `rustscan -a <TARGET_IP> --range 1-65535` |
| **Netcat (`nc` / `ncat`)** | Interactive raw bidirectional TCP socket streaming | `nc -nv 127.0.0.1 9042`<br>`ncat 127.0.0.1 9042` |
| **Telnet** *(Alternative)* | Text-based TCP terminal connection fallback | `telnet 127.0.0.1 9042` |
| **Python 3** | Scripting, custom socket automation, structured response parsing | `python3 -c "import socket; print('Socket OK')"` |
| **SQLMap** *(Optional)* | Automated SQL injection testing and schema enumeration | `sqlmap --version` |

---

## 4. Required Conceptual & Technical Competencies

1. **Full TCP Port Scanning (`-p-`):**
   Standard top-1000 port scans will miss auxiliary services hosted above port 1024. Participants must inspect the full 1–65535 TCP port range.

2. **TCP Session Handshakes & Interactive Streaming:**
   The auxiliary transaction gateway enforces a pre-session handshake state. Understanding newline conventions (`\n`) and stateful socket interaction is required.

3. **WAF Whitespace Evasion Techniques:**
   When input filters block raw ASCII spaces (` `), standard injection payloads will be rejected. Understanding SQL comment substitution (e.g. `/**/`) or inline parenthesis grouping allows query execution across restrictive filters.

4. **Structured Multi-Column UNION Injection:**
   - UNION compatibility requires matching column counts and aligned data types.
   - Determining column counts via `ORDER BY <N> --` or trial NULL projections.
   - Extracting records from sequestered backend tables.

---

## 5. Security & Fair Play Rules

- Do not perform brute-force attacks or denial-of-service against the network daemon port.
- Respect rate limiting constraints (10 req/min).
- The service enforces deterministic query processing. Arbitrary OS command execution is not supported or required.
