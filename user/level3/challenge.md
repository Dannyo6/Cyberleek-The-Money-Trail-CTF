# Challenge 5.3: Operator Gatekeeper (WAF Evasion)
**Case File: EVIDENCE 05 - THE ATTENTION ECONOMY / THE MONEY TRAIL**

> "Every transaction leaves a trace."

---

## Mission Briefing

Dispatching the maintenance diagnostic routine exposed the internal gateway's primary security checkpoint: the **Operator Gatekeeper Authentication Portal** (`AUTH`).

The gatekeeper demands a valid syndicate Operator Key ID before permitting access to the internal transaction ledger. While source fragments in `files/sanitizer_rules.txt` reveal that the backend relies on dynamic SQL queries, the system has been hardened with an active Web Application Firewall (WAF) rule specifically configured to block raw ASCII whitespace (` `) and intercept naive injection strings.

Analyze the sanitizer rules, discover alternative SQL token separators, and craft an evasion payload that forces the operator verification check to evaluate to TRUE.

---

## Operational Objectives

1. Review `files/auth_audit.txt` and `files/sanitizer_rules.txt`.
2. Access the `AUTH` portal through the gateway terminal.
3. Test the input field to observe WAF filter reactions against whitespace characters.
4. Construct an SQL injection payload utilizing comment-based token separation (`/**/`) or parenthesis grouping to bypass the WAF.
5. Recover the Level 3 gatekeeper bypass token and gain operator clearance.

---

## Target Information

- **Host**: `target.cyberleek.lan:9042`
- **Interface**: `CYBERLEEK-GW> AUTH` / Operator Key ID prompt
- **Reference Files**:
  - `files/auth_audit.txt`
  - `files/sanitizer_rules.txt`

---

## Tiered Investigation Hints

<details>
<summary>Hint 1: WAF Whitespace Filtering</summary>
The gateway WAF rejects raw space characters (ASCII 0x20). Try submitting <code>' OR 1=1 --</code> and observe the specific violation warning. How does SQL handle whitespace inside queries?
</details>

<details>
<summary>Hint 2: SQL Comment Token Separators</summary>
In SQL standards (including SQLite), block comments (<code>/**/</code>) act as valid token delimiters. Can you replace every space in your boolean tautology with a comment block?
</details>
