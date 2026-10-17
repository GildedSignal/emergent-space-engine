Working...
Check complete. `lab/results/20261017-0005-fermi-25ce/check.md` written: **Grade: gold**.

**Reproduction** — `python3 fermi_calendar.py`: P3/P4/P2 identical digit-for-digit vs `regen.out`; P1 timings 23.0–24.6 ns/body on this loaded box (author 23.1–23.3) — same verdicts. `patch.diff` empty; `predictions.md` (00:13) precedes the script and its run (00:16) — pre-registration genuine. `proc_pid_rusage` confirmed unconditional in `crates/universe/examples/nladder.rs:17`, so the no-flight claim is real.

**Adversarial (4 cases, 3 outside the author's range)** — all confirm:
1. The 10⁹-scale concentration the author only extrapolated: measured 1.050–1.055 over 5 seeds vs claimed 1.05 (law 1.056).
2. The author's own model one decade up (N=10⁸, μ=740): 1.186 vs law 1.179 at K=10F; K=F 1.213 — saturation at K≈F holds.
3. P1's declared-but-never-run held-out arm 3×10⁷: 25.7 ns/body (10⁸: 21.9) — flat, within the 2× bar, still dead by ~1,300 frames.
4. Mixed dyadic steps (the shipped reality per `step.rs`, vs the author's single-interval model): concentration 1.17×, cursors 56.6 MB — inside the ×100 budget.

**The named falsifier, read** — the shipped interval law is `aligned` (`crates/universe/src/step.rs:107`, block steps: one stub after handoff/decision, then back on the absolute grid); no carried chain state ships (ES_CHAIN was a lab arm). Form (d)'s stability premise holds against shipped code — recorded in the page's open direction.

**Novelty** — clean: no page prices the schedule's bytes; `frame-cost`'s queue runs price live-queue CPU at 10⁶; `scan-queue` is the player's scan; the encounters "conjunction calendar" is who-meets-whom. The exclusion of 98cb's bijective class on the *enumeration* axis is new.

**Page corrections** (in place) — "the adopted hash stagger (f82a)" softened (its gates are open per kick-cadence od8); the 1.05 figure marked checker-measured.

**Recorded weaknesses** — a ×10⁹ unit slip in the script's "frames of budget" display (never quoted in the dossier), the silently-swapped 3×10⁷ arm, and two disclosed prediction misses (P1's band, P2's working-point figure) that don't touch the claim. Nothing committed or pushed.
