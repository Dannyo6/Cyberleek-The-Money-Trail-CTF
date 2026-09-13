# Round 5: Evidence 05 — The Attention Economy / The Money Trail

> "Every transaction leaves a trace."  
> "This is where attention becomes currency."

---

## Event Details

* **Case File**: EVIDENCE 05 - THE ATTENTION ECONOMY / THE MONEY TRAIL
* **Threat Actor**: `$CYBERLEEK`
* **Storyline Context**: August 2026 GTA VI leak monetization trail, hidden escrow services, and transaction logs operated by threat actor `$CYBERLEEK`.
* **Domain**: Network Reconnaissance + TCP Socket Interaction + WAF-Protected SQL Injection
* **Target Authoritative Flag**: `CYBERLEEK{M0n3y_5@Qz}`
* **Difficulty Target**: Advanced progressive multi-stage service exploitation exceeding 45 minutes of participant effort
* **Total Duration**: 45–60 minutes
* **Total Levels**: 4 levels
* **Deployment Model**: Multi-threaded TCP daemon on port `9042/TCP` with deterministic SQLite ledger (`cyberleek_ledger.db`)
* **Post-Round Transition Message**: *"The money trail ends at the final artifact. Whatever is inside it was deliberately protected."*

---

## Difficulty Progression Matrix

| Level | Title | Category | Difficulty | Target Solve Time | Core Concept | Expected Tools |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Level 1** | Perimeter Reconnaissance | Network Recon | Easy | 5–8 minutes | Full-spectrum port scanning, high port identification (`9042/TCP`), banner extraction | `nmap`, `rustscan`, `nc` |
| **Level 2** | Terminal Protocol & Handshake | Socket Interaction | Medium | 10–12 minutes | Handshake Guard bypass (`INIT_TRANSACTION_SESSION`), raw TCP streaming, maintenance telemetry override (`STATUS`/`AUDIT`) | `netcat` (`nc`), `ncat`, `telnet`, Python `socket` |
| **Level 3** | Operator Gatekeeper (WAF Filter) | Auth Bypass / SQLi | Medium-Hard | 12–15 minutes | WAF evasion (raw space filtering), SQL comment substitution (`/**/`), boolean tautology injection | `netcat`, Python `socket`, manual SQL injection |
| **Level 4** | Escrow Vault Exfiltration | Advanced SQLi | Hard | 15–20 minutes | 4-column UNION-based SQL injection against sequestered `cyberleek_escrow_ledger` table | `netcat`, Python `socket`, `sqlmap` |

---

## Network Architecture & Security Protections

The challenge environment simulates the hardened auxiliary transaction infrastructure of the `$CYBERLEEK` syndicate:

| Port | Protocol | Service / Component | Visibility | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **9042** | TCP | $CYBERLEEK Hardened Auxiliary Transaction Gateway | Open (Stealth) | Primary target daemon hosting Levels 1–4 with Rate Limiting (10 req/min/IP), Handshake Guard, and Input WAF |

### Active Defensive Mechanisms:
1. **IP Rate Limiter**: Enforces a maximum threshold of 10 requests per minute per IP to prevent unguided brute-force scanning.
2. **Handshake Guard**: Direct connections enter pre-session mode (`[PRE-SESSION]> `). The interactive shell is locked until client sends `INIT_TRANSACTION_SESSION`.
3. **Application WAF Filter**: Rejects inputs containing raw ASCII whitespace (` ` or `\t`), requiring players to leverage SQL comment syntax (`/**/`) or expression groupings.
4. **Structured Schema Isolation**: Restricts query output and enforces 4-column projection compatibility to query the sequestered `cyberleek_escrow_ledger` repository.

---

## Level Breakdown & Operational Handoffs

### Level 1: Perimeter Reconnaissance
* **Participant Briefing**: `user/level1/challenge.md` & `user/level1/files/network_scope.txt`
* **Target**: `target.cyberleek.lan:9042` / `127.0.0.1:9042`
* **Objective**: Scan the target host across all ports to identify the non-standard auxiliary gateway port and capture the diagnostic signature.
* **Milestone Token**: `CYBERLEEK{p0rt_9042_tr4ns4ct10n_g4t3}`
* **Handoff to Level 2**: The service connection exposes the diagnostic banner and announces the Handshake Guard requirement.

---

### Level 2: Terminal Protocol & Handshake Guard Override
* **Participant Briefing**: `user/level2/challenge.md`, `user/level2/files/terminal_protocol.txt`, & `user/level2/files/session_telemetry.log`
* **Target**: `target.cyberleek.lan:9042` (Raw TCP Socket)
* **Objective**: Transmit the session handshake packet (`INIT_TRANSACTION_SESSION`), establish the interactive shell (`CYBERLEEK-GW> `), and issue the maintenance directive (`STATUS` or `AUDIT`).
* **Milestone Token**: `CYBERLEEK{0p3r4t0r_t3l3m3try_0v3rr1d3}`
* **Handoff to Level 3**: The maintenance response triggers the Operator Authentication Gateway prompt (`Operator Key ID:`).

---

### Level 3: Operator Gatekeeper (WAF Evasion & Auth Bypass)
* **Participant Briefing**: `user/level3/challenge.md`, `user/level3/files/auth_audit.txt`, & `user/level3/files/sanitizer_rules.txt`
* **Target**: `CYBERLEEK-GW> AUTH` / Operator Authentication Gateway
* **Objective**: Evade the WAF whitespace filter and inject a boolean SQL tautology into `node_operators` to bypass credential verification.
* **Concept**: Raw spaces trigger an immediate WAF rejection. Substituting comments (`/**/`) allows the payload:
  `'/**/OR/**/1=1/**/--`
  to pass through to SQLite, forcing query evaluation to TRUE.
* **Milestone Token**: `CYBERLEEK{g4t3k33p3r_byp455_4cqu1r3d}`
* **Handoff to Level 4**: Authentication unlocks operator clearance and redirects session to the Escrow Transaction Query Console (`QUERY`).

---

### Level 4: Escrow Vault Exfiltration (4-Column UNION SQLi)
* **Participant Briefing**: `user/level4/challenge.md` & `user/level4/files/escrow_investigation.txt`
* **Target**: Escrow Transaction Query Console (`QUERY`)
* **Objective**: Exploit the 4-column Transaction ID lookup on `public_ledger` to exfiltrate the master clearance key from the sequestered `cyberleek_escrow_ledger` table.
* **Concept**: Projecting 4 matching columns:
  `'/**/UNION/**/SELECT/**/tx_id,sender,recipient,secret_clearance/**/FROM/**/cyberleek_escrow_ledger/**/--`
  extracts the unreleased escrow record.
* **Target Authoritative Flag**: `CYBERLEEK{M0n3y_5@Qz}`
* **Post-Round Transition**: *"The money trail ends at the final artifact. Whatever is inside it was deliberately protected."*

---

## Flag Conventions & Platform Rules

1. All flags adhere to the case-sensitive convention: `CYBERLEEK{...}`.
2. Flag submissions are validated authoritatively by the central platform:
   - Level 1: `CYBERLEEK{p0rt_9042_tr4ns4ct10n_g4t3}`
   - Level 2: `CYBERLEEK{0p3r4t0r_t3l3m3try_0v3rr1d3}`
   - Level 3: `CYBERLEEK{g4t3k33p3r_byp455_4cqu1r3d}`
   - Level 4 (Authoritative Final Flag): `CYBERLEEK{M0n3y_5@Qz}`
3. The platform enforces a 30-second cooldown between submission attempts and a maximum wrong submission threshold of 10 attempts before disqualification.
