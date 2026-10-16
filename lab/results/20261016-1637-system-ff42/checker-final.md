Working...
Check complete. Verdict: **silver** — `lab/results/20261016-1637-system-ff42/check.md` written, tree restored to the runner's clean state.

**What I did**

- **Reproduced** from `regen.sh` in a clean tree: 36/36 bit-identical answers, mean 55.5→27.9 µs, 2.0× — every deterministic number matches; wall means wobble with box load as expected.
- **89 adversarial cases of my own** in regimes the author never tested (`after≠0` mid-fall/next-cycle/outbound/already-inside; e 0.1–0.97 — their grid is all e≈0.9; grazing; μ=3/2 non-unity dolls, which their own predictions promised): **zero tick mismatches**, guess fires ~43–48% of answered cases at every e and in non-unity dolls. Exactness is structural: single downward crossing in the bracket, exact integer readout.
- **Closed the adoption gate the author left unflown**: `frame_digest 3 burn` patched vs pristine — digests `6a0c3cf7…`, `2373bdb3…` bit-identical, 2 flights × 4 schedules.
- **Found the run's real defect**: the bench's verified-counter mirrors the guess around raw `tube.periapsis_time` instead of `next_periapsis(b, after)` — off by whole periods for cycles. The printed "5/36 (13.9%) verified" and the dossier's "~40% fallback" are artifacts from opposite sides; corrected replication + the author's own timing agree the truth is **~half fire, ~half fall back**. Their fallback-mechanism story (residual offset past the ±1 window) survives.
- **Novelty**: the stateless analytic guess in `next_impact` is new (the warm-start/AB-IQI line is stateful/policy), but the page's standing composed best already cuts search readouts −78–83% digest-proven on the plane — this patch alone (2.0× synthetic, fallback adds a wasted inverse) doesn't beat it; its value is composition and the structural finding.
- **Corrected the wiki page** where it overstated (fallback rate, the counter artifact, the now-flown digest, 55.9→55.5 µs).

**Why not gold**: no 10× on a bottleneck, no deleted component, predictions 2–3 missed, and the miscalibrated instrument. **The gold experiment** (named, one step): the ±k window sized by closed-form fall speed + unrounded periapsis epoch, correctly re-instrumented, measured on the plane's flights alone and composed — if fallback →~0, the crash search retires behind its inverse and the policy layer becomes insurance: a deleted component with flight-level identity.
