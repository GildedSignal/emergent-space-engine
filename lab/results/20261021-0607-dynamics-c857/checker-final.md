Grade: gold**Grade: gold** — `check.md` written, page corrected, tree reverted.

**Reproduction.** Runner's `regen.sh` (exit 0) matches every headline number digit-for-digit: pooled excess +20.6/+19.1 → +0.90/+0.84 → +0.38/+0.25 → +0.25/+0.28; β = 2.018/2.020; drift 6.5–7.0×10⁻⁵ flat; floors 1.335–1.371; locked pairs 6,654/6,568 with control 0; flights deterministic across processes (delta identical in all four runs). Recorded diffs, all seed-2, all < 1%, none load-bearing: 6,547→6,568 pairs, 267,917→269,348 distinct steps, 357,195→359,212 intervals; the claim's `r = 0.974` is not derivable from any artifact (measured: 0.998/0.997).

**Predictions.** Pre-registered (mtime order verified) with a two-branch kill criterion; the kill branch fired exactly — P1/P5 fail at both seeds (that failure *is* the finding), P3/P4/P6 hold, P2 holds in direction.

**Adversarial cases (all in the dossier's favour):**
1. **Same-geometry MT control** — `analyze.py` floors at min(w,512) while tiling ~1,400–1,700 windows: true late excesses +0.21/+0.24 (quoted ≤ 0.05 high), engine still outside the control's p90 in every band, both seeds.
2. **Depth 2× (g → 278**, the author's named blind spot): excess flat at +0.3 through g = 200+, no decay resumes past a97f's endpoint.
3. **N decade ×4.33 (n = 11,700**, outside the tested range): excess *grows* (+0.29–0.41) as the floor drops to 1.16–1.22 — the frozen-profile prediction; locked pairs sub-linear (×1.65 at ×4.3 N), killing the N-growing-pairs alternative at the next decade.

**Page.** Within budgets (110 lines; current best 5); corrected in place: r = 0.998, 6,568, checker note on the floor-cap bias. No closure — no gold runs yet on calendar. Gold stands on: reproduced, pre-registered falsification executed, premise (Poisson windows outside the epoch in the 10⁹ ledger) shown wrong, adoptable in one step (ledger correction; stagger-from-birth vs carry ~1.5× contrast). Checker evidence in `work/chk/` (scripts + flight logs; dumps deleted, regenerable).
