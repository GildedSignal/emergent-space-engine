Working...
Second blind check complete.

**Grade: silver** — written to `lab/results/20261017-0005-fermi-25ce/check2.md`; the author's page corrected in place where it overstates (`wiki/calendar.md`, marked `[Checker2]`).

**Reproduced:** `fermi_calendar.py` reruns in 2 s — P3/P4/P2 digit-identical to `regen.out`; P1 26.5/26.9 ns/body here (author 21.7/22.4; shared box, same verdicts — the kill rests on the 0.13 s = 8-frames bandwidth floor, which is hardware arithmetic). Pre-registration genuine (`predictions.md` 00:13 < script 00:16); `patch.diff` empty, consistent with a constants-cited replica; `proc_pid_rusage` confirmed unconditional so the no-flight claim is real. I read the interval law myself: `aligned` (`crates/universe/src/step.rs:100–118`) is grid-anchored block stepping — the class-constancy premise holds; all cited constants verified against the wiki pages.

**Adversarial findings (3 outside the author's range):**
1. **10⁹ concentration measured** (author tested 10⁶ only): streamed all 10⁹ ids, 3 seeds — max/μ = 1.081–1.086, p99/μ = 1.055, law 1.0565. The excess is the K mod F class-per-frame imbalance (verified analytically: 1.0306 × 1.0541 = 1.0863); at the dial's low end K=N/bar it reaches ≈1.29×, so the 1.05× needs K a multiple of F.
2. **A fifth form breaks the headline binary:** the run's own quantization insight (phase implicit in class-major layout) applied to its form (b) gives a class-major id-only index — 30–32 b ids + bijective store = 3.77–4.30 GB — which fits the 6 GB budget, enumerates sequentially (fetches ≈ 0.7 ms/frame, noise beside 29.3 µs/event) and pays the same maintenance as form (d). "Every other form busts or dies" / "the only form that fits" / "the bijective class is excluded" are overstated; the store-class decision is a two-way trade. The central kill (queue dead, ≥3.6 GB permutation floor for any who-enumeration, rescan dead) survives.
3. **Novelty holds:** wiki/HISTORY "calendar" hits are the conjunction calendar and the live plane's wheel/deadline CPU prices at 10⁶; nothing prices the compact schedule's bytes at 10⁹.

Minor author errors noted: 4.44×10⁻⁶ is split-only (the 61% delete applies on top — 13.2→5.1 cores), the "3.25× i.e. 5.1/4" conflation, and a ×10⁹ display bug in P1's frames-of-budget line. The one experiment to gold: price/fly the id-index arm — it is the wiring decision itself.
