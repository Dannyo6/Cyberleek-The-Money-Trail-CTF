# Challenge 5.4: Escrow Vault Exfiltration
**Case File: EVIDENCE 05 - THE ATTENTION ECONOMY / THE MONEY TRAIL**

> "This is where attention becomes currency."

---

## Mission Briefing

With operator clearance established, you now have access to the **Escrow Transaction Query Console** (`QUERY`). Standard lookups against known Transaction IDs (`TX-1001`, etc.) return only public routing memos and dummy transfers.

However, forensic intelligence detailed in `files/escrow_investigation.txt` confirms that the threat actor's primary monetization reserve and the master clearance token for the August 2026 GTA VI leak are sequestered in an isolated database table: `cyberleek_escrow_ledger`.

The query interface does not provide a direct lookup parameter for the escrow vault. You must analyze the projected query columns and construct a structured multi-column `UNION SELECT` injection to bridge the public search and exfiltrate the sequestered vault records.

---

## Operational Objectives

1. Review the intelligence briefing in `files/escrow_investigation.txt`.
2. Access the Escrow Transaction Query Console (`QUERY`).
3. Determine the column count and schema projection of the active query.
4. Construct a matching multi-column `UNION SELECT` payload targeting `cyberleek_escrow_ledger`.
5. Exfiltrate the case authoritative flag and conclude the money trail investigation.

---

## Target Information

- **Host**: `target.cyberleek.lan:9042`
- **Interface**: `CYBERLEEK-GW> QUERY` / Transaction Query prompt
- **Reference Document**: `files/escrow_investigation.txt`

---

## Tiered Investigation Hints

<details>
<summary>Hint 1: Column Count Discovery</summary>
Before a <code>UNION SELECT</code> can succeed, the injected query must project the exact same number of columns as the original query. Use <code>ORDER BY &lt;N&gt; --</code> to determine the exact number of columns returned.
</details>

<details>
<summary>Hint 2: Sequestered Table & Projection</summary>
Check <code>files/escrow_investigation.txt</code> for the sequestered table name and column list. Ensure your UNION projection matches the 4-column structure (<code>tx_id, sender, recipient, secret_clearance</code>).
</details>
