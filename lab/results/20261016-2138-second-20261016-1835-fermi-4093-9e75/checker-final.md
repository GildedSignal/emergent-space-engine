Working...
Check complete. **Grade: gold** — `check.md` written, the author's page corrected in place, tree left clean (patch reverted; nothing committed or pushed).

**What I did:**

1. **Reproduced** — re-applied the instrumentation-only patch to a clean tree, confirmed regen's four arms concordant with the dossier (integer E_spell repeats almost exactly: 298,115/298,465/298,514/298,562 across four flights; law ratio 1.01–1.02; F4's lag prints exactly its 60.000 = rtf/60 ceiling). Verified both mechanism claims in code: `target = now + want` per frame (universe.rs:1077) and the per-item stop with `done == 0 → margin 0` plus `resolve_wave` (universe.rs:1007–1026, shipped comment prices 1.4 ms; the burn measures 2.5 s).

2. **Attacked with five arms of my own** — two outside the author's grid:
   - Held-out N = 2×10⁵: E_spell 197,543 = **0.988 events/body** (ratio 2.04 to 10⁵) — linearity and one-event-per-body confirmed at an untested point.
   - 10⁵ at rtf 3600: spell 7.7 s — rtf-independent.
   - 60 s / 70 s flights: one contiguous spell, E stable; clamp deepens 14.8→22.4 deficit game-s/frame at presented ≈ 42k.
   - 160 s at rtf 450 (stream fits the budget: p50 2.0 ms): law ratio 1.01, and lag_frames 2,081 ≈ 1.9× one spell with a second deep clamp beginning at presented ≈ 42.2k = exactly 1.5 intervals — **crest recurrence supported in two independent arms**, which every author arm (all ≤ 1.02 delivered intervals) had left unobserved; a full second spell is still unprinted, noted on the page.

3. **Corrected the page** where the author's two-flight ranges overstated precision: spell 21.9–22.1 → 20.9–23.5 s, cores 185–187 → 176–187, 19.2–20.3 h, 10⁶ 69–73 s, plus the recurrence status and the stream-fits bound (below rtf ≈ 650 the crest is the only freeze — covering the player's rtf 100).

**Why gold:** the run executes exactly the experiment the first checker named as the gate (direct spell/deficit measurement with same-run constants, the burn arm, the a9d7 confrontation — its quote verified verbatim at memory-h-live L314), everything reproduces, my adversarial extension confirms rather than breaks it, the prediction accounting is honest (P5's miss mined as the headline finding, nothing relabeled), and the burn arm shows a premise wrong — the risk inverts: no freeze, 2.5-second frames instead, a failure mode no presented-time metric can see. Adoption cost: zero engine code.
