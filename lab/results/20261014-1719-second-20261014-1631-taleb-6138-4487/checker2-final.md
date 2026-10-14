Working...
Check complete. **Grade: gold** — written to `check2.md`, with one bracketed confirmation block added to the run's `wiki/nladder.md`.

**What I did (blind to `check.md` and `check_raw/`):**
- Applied `work/patch.diff` myself to a clean tree at `9fcae60f`, built independently, then restored the tree (0 dirty files at exit).
- **Reproduced every certificate:** `frame_digest` 8 flights × 4 schedules byte-identical across pristine / fixed / forced (identical digest-list md5 in all three builds); 2×10⁵ belt at 21,000 game-s `ae06c773…` with 233,600/473,200/7,356 identical pristine-vs-fixed; N=2,000 and coast identical; the 16,000 mid-drain divergence and main's wall-digest instability both corroborated.
- **Four adversarial arms of my own**, one outside the author's digest domain: **3×10⁵ under the deterministic budget** — pristine freezes at 2,615 ms with 52,846 events in one frame, my fixed build holds 12.0 ms / evmax 218, digest `d4f4441e…` identical to the digit (217× deletion, box-native); **seed 7** — identical digest at 21,000 (`3c31c508…`), with the events counter 6,116 apart at equal digest/kicks/encounters (the counter is pace-dependent, the digest is the certificate); **`NLADDER_HOLD=1`** — canonical state matches default-hold and pristine, so the key-ordered drain is slice-invariant; **code-level** — the Waiting branch's `map_or_else(Vec::new, …)` is literally the shipped `find` (encounter.rs:159), no dropped-`find` hole.
- Predictions pre-registered before all flights; every kill criterion held; novelty confirmed against HISTORY and the topic page (6138 named the fix; this run implements and certifies it).

**Noted for the integrator:** the 3×10⁵ wall worst-frame is load-conditional (123.8 quiet / 535.5 loaded on 0-event frames — already corrected on the page); the deterministic-budget arm is the stable form of that claim, and the M1 re-measure remains the integrator's.
