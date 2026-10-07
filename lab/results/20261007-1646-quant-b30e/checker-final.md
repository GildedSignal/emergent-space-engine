Working...
Check complete. Verdict: **gold**, with two corrections the integrator must read.

**Reproduction** — clean tree, empty patch (no engine edits); every saved CSV regenerates bit-for-bit. The two 0-byte CSVs (`belt15-n32-8`, `belt15-n64-64`) were runs that died at launch, but their quoted numbers regenerate exactly (128.5 / med 41 / p99 57 at n=32; 134.0 at n=64×64 orbits) — a storage slip, not fabrication.

**Predictions** — written 16:58:19, before every decisive CSV (17:07–17:11). Held: no reabsorption to 512 orbits, μ-linearity (−7…−9 vs −8±1), N-independence (+5%), 466.7 kicks/ship/orbit at every N. Failed honestly: #5 (hill). Miscounted: #2 — the med growth letter didn't happen (42→42, a plateau its own prediction called "against my expectation"); disclosed but tallied "CONFIRMED". Truly 5 clean, 1 range-only, 1 failed.

**My three adversarials:**
1. Quiet belt at 2.5·sep — still ~130 bits/member within half an orbit, Form P dead: the width is regime-independent (strengthens the claim).
2. n=4 family — Form P dies at majority loss, not "the moment any member is kicked" (alive at orbit 0 with 1/4 deviating); overstatement, mechanism otherwise faithful to `infer`'s strict Boyer–Moore majority.
3. belt21 at 64 orbits — growth reverses (139.5 → 135.4 ≈ belt15's 134.0): the "+0.3 bits/member/orbit" resonant growth is a 32-orbit transient. Adopt the bounded floor, not the growth rate.

**Why gold despite that:** the load-bearing result is untouched — first measurement of the HANDOFF-named risk "H_live: not measured yet", on the real engine, with controls on both sides, showing the premise "population programs keep kicked belts cheap" is wrong (every member scarred within half an orbit, never reabsorbed, 16 GB > 8 GB at 10⁹, 11× under the 176 B binding). Timely: `shipmem` is a measured deletion candidate today, and this run supplies that decision's numbers. Adoptable in one step, no engine change.

Verdict written to `lab/results/20261007-1646-quant-b30e/check.md`; nothing else in the run folder touched.
