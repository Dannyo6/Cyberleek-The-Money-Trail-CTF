# Production Flag Submission & Central CTF Platform Security Rules
**Round 5: Evidence 05 — The Attention Economy / The Money Trail**

> [!IMPORTANT]
> **Central CTF Platform Enforcement Only:** The flag validation, rate limiting (30-second cooldown), wrong-attempt tracking (10 attempts max), scoring, authentication, and team disqualification rules documented below are enforced **authoritatively by the CENTRAL CTF PLATFORM backend**, NOT by the local challenge containers.
>
> Round 05 features a hardened auxiliary network daemon running on port `9042/TCP` (simulating threat actor `$CYBERLEEK`'s transaction tracking and escrow systems for the August 2026 GTA VI leak monetization). Participants progress through sequential operational milestones (Levels 5.1–5.4) and submit each recovered milestone token (`CYBERLEEK{...}`) to the central CTF platform.

---

## 1. Backend Authoritative State Requirements

The central platform database maintains authenticated per-team state with the following fields:

- `team_id` (UUID / string): Authenticated team identity derived from session token or API key.
- `score` (integer): Cumulative points earned by the team across the round.
- `solved_challenges` (array of strings): Challenge IDs correctly completed by the team (`5.1`, `5.2`, `5.3`, `5.4`).
- `wrong_flag_count` (integer): Cumulative count of incorrect flag submissions across Round 5 (0–10).
- `next_submit_at` (timestamp / epoch ms): Server timestamp indicating when the team may next submit a flag (enforces the mandatory 30-second cooldown).
- `is_disqualified` (boolean): Flag indicating if the team has exceeded the maximum permitted incorrect submissions (10 attempts).
- `disqualified_at` (timestamp, nullable): Server timestamp recorded upon team disqualification.

---

## 2. Server-Side Submission Handling Workflow

Upon receiving a flag submission request (`POST /api/v1/submit-flag` with JSON payload `{ challenge_id, flag }`):

1. **Authentication & Team Identity Verification:**
   - Verify JWT or session cookie to identify the requesting team. Reject unauthenticated requests with `401 Unauthorized`.

2. **Disqualification Check:**
   - If `team.is_disqualified == true` or `team.wrong_flag_count >= 10`:
     - Reject request immediately with status `403 Forbidden` (`TEAM DISQUALIFIED — Maximum incorrect flag submissions reached.`).

3. **Sequential Challenge Milestone Unlock Rules:**
   - Verify that the requested `challenge_id` is unlocked for this team:
     - `5.1` is unlocked by default upon round activation.
     - `5.2` requires `5.1` in `team.solved_challenges`.
     - `5.3` requires `5.2` in `team.solved_challenges`.
     - `5.4` requires `5.3` in `team.solved_challenges`.
   - If attempting to submit to a locked milestone, reject with `400 Bad Request` (`CHALLENGE LOCKED — Preceding milestone not yet cleared.`).

4. **Rate Limit / 30-Second Cooldown Enforcement:**
   - If `server_time < team.next_submit_at`:
     - Calculate remaining seconds: `Math.ceil((team.next_submit_at - server_time) / 1000)`.
     - Reject immediately with status `429 Too Many Requests` (`SUBMISSION BLOCKED — Submission cooldown active. Wait X seconds.`).
     - **Do NOT increment `wrong_flag_count`**, do NOT modify score, and do NOT extend the cooldown timer.

5. **Set Immediate Submission Cooldown:**
   - Set `team.next_submit_at = server_time + 30 seconds` immediately for the team (regardless of whether the submitted token is valid or invalid).

6. **Flag Processing & Canonical Comparison:**
   - Trim leading and trailing whitespace from the submitted string.
   - Perform strict, case-sensitive comparison against the canonical flag string.
   - Do NOT lowercase or modify the character casing of the submitted flag.

7. **Duplicate Submission Protection & Scoring:**
   - If the submitted flag matches:
     - Do **NOT** increment `wrong_flag_count`.
     - If `challenge_id` is already in `team.solved_challenges`:
       - Return `200 OK` with status `DUPLICATE_SUBMISSION` (Score remains unchanged).
     - Otherwise:
       - Append `challenge_id` to `team.solved_challenges`.
       - Add challenge point value to `team.score`.
       - Return `200 OK` with status `FLAG_ACCEPTED`.

8. **Incorrect Flag Handling & Disqualification Trigger:**
   - If the submitted flag does NOT match the canonical flag:
     - Increment `team.wrong_flag_count` by 1.
     - If `team.wrong_flag_count >= 10`:
       - Set `team.is_disqualified = true`.
       - Set `team.disqualified_at = server_time`.
       - Return `403 Forbidden` (`TEAM DISQUALIFIED — Threshold of 10 failed attempts exceeded.`).
     - Otherwise:
       - Return `200 OK` with status `INCORRECT_FLAG` and remaining attempts count (`10 - team.wrong_flag_count`).

---

## 3. Authoritative Flag Registry (Round 5)

| Challenge ID | Level Name | Canonical Flag | Points |
| :--- | :--- | :--- | :--- |
| `5.1` | Perimeter Reconnaissance | `CYBERLEEK{p0rt_9042_tr4ns4ct10n_g4t3}` | 100 |
| `5.2` | Terminal Protocol & Handshake | `CYBERLEEK{0p3r4t0r_t3l3m3try_0v3rr1d3}` | 200 |
| `5.3` | Operator Gatekeeper (WAF Evasion) | `CYBERLEEK{g4t3k33p3r_byp455_4cqu1r3d}` | 300 |
| `5.4` | Escrow Vault Exfiltration | `CYBERLEEK{M0n3y_5@Qz}` | 400 |

---

## 4. Operational Transition

Upon successful completion of Level 5.4, the platform broadcasts the transition prompt:
> *"The money trail ends at the final artifact. Whatever is inside it was deliberately protected."*
