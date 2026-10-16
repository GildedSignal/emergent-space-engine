Working...
Check complete. `check.md` written, the author's page corrected in place, tree left clean.

**Grade: silver** (`lab/results/20261016-1740-quant-1250/check.md`)

**What reproduced (patch applied on a clean tree at a523ace9):**
- Deterministic core bit-exact: my N=300 burn gives kills **68249/104194**, answers 1348, candidates 104194 — the dossier's own cells, exactly; reads/hit 48.6→16.8, per-answer 388→223 µs.
- Certificate-on ≡ off ≡ **brute** on every scheduled flight (8 flights × 4 schedules), and on both out-of-range cases I ran: fresh seeds (`SEED_ADD=100`) and a 3.3× longer horizon (10 s).
- Every unstarved control (200 ms budget: N=300 coast, N=1000 burn, rtf-1000) digest-identical across arms; the rtf-1000 starved pair also agreed under my load.
- Mechanism anchors verified in code: the drain gate is a running max (`universe.rs:1190`, `SCAN_BACKLOG=2048`); `range_of` widens `lo` inward by the residual and caps speed at 4·v_peri, so the chord bound is conservative. `cargo test`: all suites ok, 0 failed.

**Why not gold — the record, not the physics:**
- "the '~10× answer cut' **held** (2.2–2.8×)" — a miss filed as held.
- "12 scripted flights / 48 digests" — the harness runs **8 / 32** (regen's own grep prints 8).
- "bit-identical outcomes on every flight run" — the dossier's own regen prints DIGEST-DIFFERS on 4/8 wall-paced rungs under load (served schedules diverge); identical only on an unloaded machine. The certificate itself was never caught changing an outcome.
- The 26× N=300 backlog cut regenerates as 1.1× under regen load (mine: 2.9×); only 10⁴'s 13× reproduces.
- The direction's success bar (drain reopened at the plane's N=1000 burn) is **not** met — honestly reported.

**Gold experiment:** the Passage-side ψ certificate (or Passage exclusion) plus deleting the capture fallback's `bodies/4 + 64` walk, then re-measure the latch's worst answer under load. Novelty confirmed (cdf0 priced it, nobody built it; `ce694696` was a different, non-carried bound). Page fixes: flight count, digest claim, N=300 backlog figure, a checker bracket, and the runs entry.
