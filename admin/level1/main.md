# Level 1: Perimeter Reconnaissance — Administrator Solution & Exploitation Walkthrough
**Case File: EVIDENCE 05 - THE ATTENTION ECONOMY / THE MONEY TRAIL**
**Threat Actor: $CYBERLEEK**

---

## 1. Challenge Specification
* **Domain**: Network Reconnaissance & Port Scanning
* **Difficulty**: Easy
* **Estimated Solve Time**: 5–8 minutes
* **Target Endpoint**: `target.cyberleek.lan:9042` / `127.0.0.1:9042`
* **Target Flag**: `CYBERLEEK{p0rt_9042_tr4ns4ct10n_g4t3}`
* **Reference Document**: `uploads/network_scope.txt`

---

## 2. Vulnerability & Design Analysis
The threat actor `$CYBERLEEK` operates an auxiliary transaction gateway daemon on an unassigned high-order TCP port (`9042`). Standard top-1000 Nmap scans will fail to detect this port. Participants must conduct a full-range port scan (`-p-` or `-p 1024-65535`) or banner interrogation.

Upon socket connection, the daemon immediately transmits an ASCII banner displaying service identification, taglines, diagnostic telemetry containing the Level 1 flag, and announces the active Handshake Guard:
```
======================================================================
  $CYBERLEEK // AUXILIARY TRANSACTION GATEWAY (HARDENED)
  "Every transaction leaves a trace."
  "This is where attention becomes currency."
  AUGUST 2026 // ESCROW MONETIZATION NETWORK
======================================================================
[+] SERVICE STATUS: ONLINE
[+] GATEWAY PORT: 9042/TCP
[+] DIAGNOSTIC SIGNATURE: CYBERLEEK{p0rt_9042_tr4ns4ct10n_g4t3}
======================================================================
[!] HANDSHAKE GUARD ACTIVE: Transaction bus locked in pre-session state.
    Transmit initiation packet 'INIT_TRANSACTION_SESSION' to proceed.
======================================================================
```

---

## 3. Step-by-Step Exploitation Walkthrough

### Step 1: Full-Spectrum Port Scan
Execute an aggressive SYN port scan across all ports:
```bash
nmap -sS -p- --min-rate 1000 -T4 127.0.0.1
```
Result indicates port `9042/tcp` is open.

### Step 2: Service Interrogation & Banner Grab
Interrogate the discovered service:
```bash
nmap -sV -sC -p 9042 127.0.0.1
```
Alternatively, connect directly with Netcat:
```bash
nc -nv 127.0.0.1 9042
```

### Step 3: Flag Recovery
Parse the banner output for the flag token:
`CYBERLEEK{p0rt_9042_tr4ns4ct10n_g4t3}`.

---

## 4. Standalone Automated Verification Script

Save as `verify_level1.py` and run against the target:

```python
#!/usr/bin/env python3
import socket

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 9042
EXPECTED_FLAG = "CYBERLEEK{p0rt_9042_tr4ns4ct10n_g4t3}"

def verify():
    print(f"[*] Probing {TARGET_HOST}:{TARGET_PORT} for Level 1 diagnostic banner...")
    with socket.create_connection((TARGET_HOST, TARGET_PORT), timeout=5.0) as s:
        banner = s.recv(4096).decode("utf-8", errors="replace")
        assert "$CYBERLEEK" in banner, "Banner must contain $CYBERLEEK identification."
        assert EXPECTED_FLAG in banner, f"Banner missing flag: {EXPECTED_FLAG}"
        print(f"[+] SUCCESS: Extracted Level 1 Flag: {EXPECTED_FLAG}")

if __name__ == "__main__":
    verify()
```
