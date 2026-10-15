Working...
Check complete. **Grade: silver** — written to `lab/results/20261015-1615-scout-ee30/check.md`, with the author's `wiki/view.md` corrected in place.

**What held (reproduced bit-identically in a clean tree):**
- All nine arms match exactly: steady flux 3.35×10⁻³/s at 10⁵ (3.37 held-out seed), 0 fitted-zoom events over 5×10⁶ s, burn 507 events/worst frame 6, zoom worst frames 2,722/5,539, solver residual 4.4×10⁻¹⁶. `work/patch.diff` empty.
- Fidelity verified against sources: `view.rs:58` + `page.html drawMap` (retarded offset, root frame, ship-centred box) and `scenario.rs:333-344` (belt birth law) — the replica is faithful in form.
- My three adversarial cases all confirm: **zoom at 10⁶** (next decade) worst frame 27,321 — exactly linear, drain mandatory; **full observer year** (author's window covered only 16% of the orbit) flux 3.08×10⁻⁸/body/s — inside the claimed band; **all-e=0.4 tail** 2.85×10⁻⁸, fitted zoom disjoint, solver exact at the extreme.
- Novelty holds: the view page named this exact gap ("the missing engine half… the p99 owner"); no prior run priced row-set membership.

**Why silver, not gold:**
1. One composition line is contradicted by the run's own table: at 10⁹ the burn is **not** "worst frame ~600 (2 ms) — under budget" — linear scaling (the author's own rule, confirmed by my 10⁶ run) gives ~6×10⁴ entries ≈ 0.21 s; the burn needs the drain too, so "the one drain-required moment is the zoom" is wrong at that scale.
2. The "79–86×W, permanent" margin is horizon-limited: 68–71×W over a full year, 31×W at the e-tail (disjointness itself survives).
3. It's a pricing on a float replica with borrowed constants (2df1, cf45 — not in this checkout, disclosed); the certificate form is proposed, not wired.

**The one experiment to gold:** wire the envelope + per-row boundary root + drain into the shipped `view.rs` gather and measure on the ladder at 10⁵–10⁶, digest unchanged.
