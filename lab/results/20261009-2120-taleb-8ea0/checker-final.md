Working...
**Grade: silver** — `check.md` written to the run folder (abstract 120 words; nothing else in `lab/results/20261009-2120-taleb-8ea0/` touched; my cells and JSONL live in `/tmp`).

**Reproduced, bit-for-bit:** both key-cell digests (`8ab0b55c40140b35`, `03e62d9683a30e1c`) plus the control a third time (`41343a14…`), seed 2 differs, timings within shared-machine noise; all dossier tables match `ladder.jsonl`; predictions pre-registered (mtime order verified), 4/6 held, misses honestly reported.

**Adversarial findings beyond the dossier (5 new cells):**
- rtf 10⁵: the bench **aborts** at ~2.6×10⁵ game-s (`no view: the player is lost`, no report, wall-dependent abort tick). The dossier's excuse for skipping this rung — "could not fit in the minute" — is wrong; it fails in 4.3 s. rtf 3×10⁴ aborts at ~4.3×10⁵ game-s: the harness ceiling is ≈3×10⁵ game-s, exactly where the ladder stopped.
- The omitted paced 55 s run works fine (55.1 s, digest identical to the unpaced cell) — the author's own driver timeout killed it, undisclosed.
- Cliff brackets tighter: dead by 8 250 game-s at rtf 150, and on seed 2.
- Memory slope reproduces cross-seed (29.4 MB at seed 2) and tracks game time, not events — a one-run mechanism clue the author skipped.

**Why not gold:** solid negative result (no growing liability to 3.5 days) that closes a HANDOFF risk line, but moves no board bottleneck, deletes nothing, and its actionable output (bench script fix + graceful dead-player abort) is proposed, not built. Plus three record dings (paced-run omission, wrong skip reason, 16-vs-18 run count). One experiment to gold: keep the scripted player alive and reporting at any depth, then re-run the ladder — that unblinds every living-player horizon probe.
