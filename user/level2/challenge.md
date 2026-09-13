# Challenge 5.2: Terminal Protocol & Handshake Guard
**Case File: EVIDENCE 05 - THE ATTENTION ECONOMY / THE MONEY TRAIL**

> "This is where attention becomes currency."

---

## Mission Briefing

Connecting to the auxiliary transaction gateway on port `9042/TCP` presents a locked pre-session prompt (`[PRE-SESSION]> `). Any commands issued in this state are dropped by the active Handshake Guard.

Forensic logs recovered from an intercepted syndicate cache (`files/session_telemetry.log`) reveal that legitimate relays transmit a specific session initiation handshake before establishing command mode. Furthermore, internal developer notes indicate an undocumented maintenance diagnostic directive exists to inspect node operational telemetry.

Review the protocol specification, complete the handshake, analyze the session telemetry logs, and trigger the maintenance override.

---

## Operational Objectives

1. Review the connection guidelines in `files/terminal_protocol.txt`.
2. Inspect the recovered relay logs in `files/session_telemetry.log`.
3. Connect over raw TCP to `target.cyberleek.lan:9042` and complete the handshake.
4. Unlock the interactive command prompt (`CYBERLEEK-GW> `).
5. Dispatch the maintenance diagnostic directive to retrieve the Level 2 override token.

---

## Target Information

- **Host**: `target.cyberleek.lan` / `127.0.0.1`
- **Port**: `9042/TCP`
- **Reference Files**:
  - `files/terminal_protocol.txt`
  - `files/session_telemetry.log`

---

## Tiered Investigation Hints

<details>
<summary>Hint 1: Pre-Session Handshake</summary>
Check <code>terminal_protocol.txt</code> and <code>session_telemetry.log</code>. What exact packet string does the gateway daemon expect before unlocking the interactive console?
</details>

<details>
<summary>Hint 2: Telemetry Directive</summary>
Review the log entries in <code>session_telemetry.log</code> timestamped around the maintenance event. What command did the operator run to inspect node telemetry?
</details>
