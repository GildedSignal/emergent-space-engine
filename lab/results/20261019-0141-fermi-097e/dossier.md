# Dossier — 20261019-0141-fermi-097e (Fermi lens)

**Claim.** On the week's measured laws the board's interlocking 10⁹ ledger composes to **10.8–16.6 CPU cores (2.7–4.2× the M1's "few cores", every remaining lever named and ≤ 2.1×)** and memory **294× over on the shipped build but 0.2–2.0× over on the wired compact store** — so the top row's remaining 10³ is the store's wiring plus the live-residency dial (τ ≤ 43.6 game-s at today's 5.1 KB live cost if every fired kick promotes; τ ≤ 0.12 orbit even for SOI promoters alone: orbit-scale residency stands 66.8 GB), not CPU and not physics.

**Bottleneck.** The board's #1 row (bodies: 28→10⁹) and the interlocking formula (13 Oct): CPU = N·rate·cost + encounters; memory = N·bits + N_live·bytes. The assembled answer: which term breaks first at 10⁹ and by how many orders — the question no single topic page holds, because its pieces live on six pages. Expected gain: re-ranks the board (the CPU 10³s are composed away; the memory 10³ is ~978× of pure wiring debt) and prices the one dial (promotion residency) that gates every plan to 10⁹.

**Evidence.** Two shipped `nladder` flights (this box, coast seed 1, rtf 100, 10 s wall, < 250 MB) + `python3 ledger.py` (~0.1 s, every constant page-cited, full JSON `ledger-out.json`):

- **P1 held:** `b_per_body` = 2,464 (N=10⁴) / 2,348 (N=10⁵) — the page's 2,340–2,459 law (dcf1/99da).
- **P2 held to 3 digits:** per-body kick rate 2.134×10⁻⁴ → 2.139×10⁻⁵ as N grew ×10 ⇒ total kicks identical (ratio 1.002); events/frame distribution identical at both rungs (p50 2, p99 154, max 212). The ladder belt is **inert**; the engine's frame stream is player-only and N-flat — this is the load-bearing assumption behind every "smooth at 10⁶" claim, now printed as a census.
- **P3 held:** engine p50 0.076/0.078 ms, p99 8.9/8.8 ms, held_max 1 at both rungs.
- **Ledger (P4 held, P5 did not fire):** CPU = stream 5.3–8.4 (cd3b) + churn 2.8–5.5 (08d0 epoch rule; 9fd1 awaiting grade) + mint ≤ 1.9 (cd3b) + view serve ≤ ~0.1 (e3a4 due-event form) + frame ≤ 0.72 (the 12-ms budget itself) = **10.8–16.6 cores**. Conditional, honest: **if the epoch rule falls, churn = 355 wholesale (1a29) and the total is 363 cores = 91×** — the row's whole residual risk is one ungraded run.
- **Memory (P6 held):** shipped build 2,348 GB = 294×; wired store 1.7–2.4 GB (self-stirred, 07b4) / 15.8 GB (driven worst, 2.0×, fc48/0820) / 2.6–5.0 GB (phase-locked); **build/floor = 978×** — wiring (shipmem measured but not in the plane; 5465/efd4 proved 58–99.6% of the build regenerable or duplicated), not information.
- **P7 half-held, half-failed (reported as failed):** every-kick residency τ ≤ 43.6 game-s (predicted 20–80 ✓); but SOI-promoters-only at orbit-scale residency stands 66.8 GB (τ ≤ 4.2×10⁷ game-s = 0.12 orbit) against my predicted "fits ≤ 3 GB" — the miss: I forgot the standing live stock is rate × τ × bytes, and Γ_SOI×N per orbit is 1.31×10⁷ bodies.

**Predictions.** `predictions.md`: P1–P4, P6 held; P5 did not fire; P7 half-held, half-failed as above.

**What would make it wrong.** (a) 9fd1's pooled curve failing grading → the churn conditional (363 cores) is the row, not 10.8–16.6. (b) The composed stream constants (cd3b) ride the shipped belt geometry: a deliberately 10–100× denser belt rescales the flow linearly (cd3b's own caveat). (c) Gravity at c, rotating holes and dispersed-fleet certificates are **not composed** (designed/compiled, unwired — named in the ledger's `not_composed`): adding them can only raise the total. (d) All CPU anchors except the probes are x86→M1 page-cited conversions (orders of magnitude only, per the lab README; the integrator re-measures on the M1).

**Cost of adopting:** none — arithmetic + two shipped flights + one print-only patch (the macOS `footprint` call → `/proc`, dcf1's swap; no engine change, `regen.sh` applies `work/patch.diff` first). **Fit with PRINCIPLES:** "the cheapest compute is compute not done" (#1: the 978× is compute-and-store not done — regenerate, don't hold); "the memory floor is information" (#24: the wired floor is 0.2–2× of budget, so the goal is reachable); "Measure before claiming" (#10: the census before the extrapolation).

**The lens.** Fermi deletes: this deletes the board's three ~10³ CPU gaps as *current* numbers (they were 13-Oct states of four different pages) and concentrates the top row on one wiring item and one dial. What the lens may have missed: the composed total's error bars are the cited runs' domains, not mine — I re-measured only the anchors P1–P3; and the ledger's cleanliness depends on the ladder's inert belt, so a stirred 10⁹ belt (a9d7's rate is plane-measured, not ladder-measured) is the one scene where the census should be re-flown before the number is trusted.

## Machine state
Linux 6.8.0-111 x86, 8 vCPU, 15 GB (load ~1–2 during probes), shared runner; orders of magnitude only. M1 anchors page-cited, not re-measured.
