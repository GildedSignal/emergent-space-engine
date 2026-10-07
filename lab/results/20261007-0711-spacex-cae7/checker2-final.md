Working...
Check complete. `lab/results/20261007-0711-spacex-cae7/check2.md` written; tree restored to clean at 70f27a9.

**Grade: gold.**

**What I verified:**
- **Reproduction, bit-exact.** Applied `work/patch.diff` to a clean tree, ran all three dossier commands: all three stored JSONs reproduce **byte-identical** (modulo `machine`/`wall_seconds`). Plane 4,665 B/body with slices frozen at 3,027 and bytes flat from ~2×10⁵ s (steady-state claim holds); formation 1,245 / belt 1,277 B per Ship; `catalogue_live = 2,076`; exactly 1.000 segments/body.
- **Mechanisms confirmed in source**, not just output: `Catalogue::insert` reuses only freed ids — no dedup ever; `bytes_of` = 448 rec + plan + knots×88 + history×192 (matches the 47/35/15/3 split); `prune` = `2·d/c + 2²⁶` ticks with `h.len() > 1` — the mandatory segment is the rule, not the rate.
- **Adversarial:** seed 2 → 1,272 B/body; belts of 200/2,000/6,000 flat (~1.26–1.48 KB, tracking per-body events 126 vs 114); `catalogue_live == n_bodies` at every scale — the 1.28 TB / 160×-over extrapolation is supported.
- **Predictions** (07:17:36) precede all result JSONs (07:21–07:25); behavioural predictions held, width guesses failed lean-ward and are reported honestly.
- **Novelty:** HANDOFF line 69 — H_live "not measured yet". First measurement.

**Dings recorded for the integrator:** the "7 passed / 3 failed" test claim regenerates only in debug (release gives 55/0 — mode unstated); the patch silently deletes the `--level` CLI flag; the probe's 50 s cap doesn't cover the final settle (belt 6,000 took ~220 s here); `bytes_of` omits the 224 B Entry slot (understates, direction favors the claim). None touches the headline: two premise-kills with numbers — a billion individual records exceed 8 GB even at law-native widths (14–18 GB), and trajectory sharing is designed, not built.
