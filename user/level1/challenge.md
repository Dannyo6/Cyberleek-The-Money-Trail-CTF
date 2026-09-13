# Challenge 5.1: Perimeter Reconnaissance
**Case File: EVIDENCE 05 - THE ATTENTION ECONOMY / THE MONEY TRAIL**

> "Every transaction leaves a trace."

---

## Mission Briefing

In August 2026, threat actor `$CYBERLEEK` shook the digital ecosystem by leaking unreleased development builds and assets of Grand Theft Auto VI. Intelligence indicates that the leak was not merely for notoriety—it was the core driver of an elaborate attention-monetization network. Behind decentralized mixers and proxy relays, the syndicate operates an auxiliary transaction gateway responsible for managing private escrow distributions and bounty payouts.

Your forensic task force has isolated an IP subnet tied to the syndicate's infrastructure. Most standard web frontends have been taken dark or point to honeypots, but intelligence reports that an auxiliary gateway daemon remains listening on an unassigned high-order TCP port.

Find the auxiliary gateway, probe the port, and extract the service diagnostic signature.

---

## Operational Objectives

1. Review the scope parameters in `files/network_scope.txt`.
2. Perform a full TCP port reconnaissance scan against the target host.
3. Identify the active auxiliary transaction gateway port.
4. Establish a connection to retrieve the diagnostic connection banner.
5. Submit the recovered diagnostic signature token to the central CTF platform.

---

## Target Information

- **Host**: `target.cyberleek.lan` / `127.0.0.1`
- **Scope**: High-order TCP ports (1024–65535)
- **Reference Document**: `files/network_scope.txt`

---

## Tiered Investigation Hints

<details>
<summary>Hint 1: Port Scanning Scope</summary>
Standard default port scans (e.g. <code>nmap &lt;target&gt;</code>) only probe the top 1,000 common ports. High-order auxiliary services will be missed unless you instruct your scanner to inspect the full port spectrum (1–65535).
</details>

<details>
<summary>Hint 2: Banner Grabbing</summary>
Once an open port is identified, simple TCP inspection utilities like <code>nc -nv &lt;ip&gt; &lt;port&gt;</code> or <code>nmap -sV -sC -p &lt;port&gt; &lt;ip&gt;</code> will capture the service banner returned upon connection.
</details>
