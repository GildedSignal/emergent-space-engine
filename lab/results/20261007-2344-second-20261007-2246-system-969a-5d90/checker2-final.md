Working...
Check complete. `check2.md` written to the run folder; nothing else there changed (my only touch inside it was an mtime-only `touch` to force a rebuild from delivered source; all builds and probes ran in `/tmp` and the external target dir).

## Verdict: silver (physics gold-quality; record defect caps it)

**Reproduced bit-identically** (rebuilt from delivered source, only wall-times differ):
- steady full ladder incl. r8 v4 case-b gates: key ratio **1.400** / cone 1.296 (≤ 2.0) at 10⁵ orbits, checks/hit **1.1027** (≤ 1.5), truth 922, 0 missed / 0 false; key-only breadth = 0 tier-2 events at every horizon
- dense/spread/formation 0/0; highe400 tiers bit-identical (inherited 36/268 miss); extremee400 key **206/289** missed vs cone 0/0

**My four adversarial probes:**
1. Independent Python port of `key_window_pairs` (incl. `Body::new` period quantization) matches the binary exactly on all 5 scenes; binary itself confirms a negative `u_hi` (−45.98) — inversion real
2. Boundary sharpened: exact condition is g² < qp(1+g+g²) on the gq lattice, and the **ρ term pulls it to e = 0.968525** at ρ=5e-4 — the exclusion band starts slightly *earlier* than the claimed 0.9692; mechanism claim survives with corrected constants
3. The proposed one-line fix, run in a /tmp copy: extremee400 → **0 missed, key ≡ cone bit-identical** — exactly as claimed
4. The dossier's own first reproduce command (`check_port.py`) **crashes** against the delivered code — `keydump` emits no per-body rows, and nothing limits to 50 bodies; that quoted number regenerates from nothing delivered

Predictions were pre-registered (timestamps verified: 00:02:34 before both logs). Novelty holds — this executed the parent checker's named gold experiment and corrected its 0.9995 boundary. Silver not gold per the lab's own 5-October standard (results the shipped code cannot regenerate) plus failed prediction 7; the gold path is one command: emit the port cross-check from the delivered tree.
