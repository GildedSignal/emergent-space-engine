# Predictions (written before the decisive runs)

Mandate: the checker of 20261014-2248-inversion-4af4 named the gold experiment — "fly N=10⁶
through ≥2-3 waves with the absolute-tick cut" — and a cheap in-box complement: "20+ waves at
2×10⁵ to turn the dissolution extrapolation into a measurement". It also named the record
defects: `analyze.py` crashes as shipped (TypeError masked by `|| true`), a MiB/10⁶ slip in the
post-wave B/body, and an overstated wiki clause ("h2 = 0 at every census").

**The 10⁶ flight cannot run on this box**: the build alone is ~2.6 KB/body ≈ 2.6 GB > the
2 GB/process rule (steady ~5.1 GB). The cheapest decisive in-box parts, run here:

- **Arm D (the complement):** N=2×10⁵, canonical absolute-tick cut, cut 700,000 game-s
  (2.8× arm C's horizon, ~117 min of play at rtf 100) — past the dossier's extrapolated
  dissolution (~wave 20, ~550 k game-s), so the extrapolation becomes a measurement and the
  staircase question is tested at ~25 waves.
- **Arm E (N at the box ceiling):** N=4.2×10⁵, cut 60,000 (two waves) — the largest N whose
  steady rss (~4,743 B/body → ~1.9 GB) fits under the 2 GB rule; the closest in-box approach to
  10⁶. If it is OOM-killed that is itself the measurement (kill-N on this box) and I fall back
  to 3.8×10⁵.
- **Record fix:** `analyze.py` repaired (the `%`-format TypeError: a list, not a tuple) and the
  census parser taught `hist_sample=a/b`, so the dossier's wave tables and census numbers
  regenerate from the run's own script on the shipped logs; `regen.sh` no longer masks errors.

Code reading that motivates each prediction (unchanged from 4af4: `prune` keeps one retired
binding per body, keep-window ≈ 2.8 k game-s ≪ wave spacing ≈ 27.5 k game-s; the catalogue's
free list returns every rebound slot; `enc_log` capped at 4,096):

1. **Memory stays a step through ~25 waves.** rss at 2×10⁵ ends within +1.5% of the post-wave-1
   value (arm C: +0.9% over 10 waves; steady-state slope ≤ 10 B/body/wave). *Falsified* if
   cumulative growth > +5% by wave 10, or any wave beyond 3 adds ≥ +3 MB that persists to the
   next census, or the process is killed for memory.
2. **The train dissolves roughly where extrapolated.** With windows = samples above 10× the
   median sample's kicks, the last detectable window falls in waves 12-22 (the dossier said
   "after ~20 waves / ~550 k game-s"); after it, the belt is a steady stream (no sample above
   10× median for the rest of the flight). *Falsified* if sharp windows (peak ≥ 10× median)
   persist past 620 k game-s, or if the stream's median rate itself grows with play.
3. **Peak decay is monotone past wave 2** and the last detectable window's peak is < 5× the
   median. Width grows ~monotonically (~875 game-s/wave at 2-5) but stays < half the spacing
   until dissolution.
4. **Census:** from just after wave 1 to the end, hist_sample = 4,106/4,106 with h2 = 0 at
   every census outside waves (transient h2 ≤ 4, hmax ≤ 2 inside); refusals 0; dead ≈ 30
   constant from ~15 k game-s. *Falsified* if h2 > 0 stands between waves at any point past
   wave 2, or hmax ≥ 3 persists past a wave + 3 k game-s.
5. **Cadence holds to the end:** lag 0.000 at every sample; settle drains 0 events at the cut;
   ≤ 5 frames over 12 ms in the whole flight (~420,000 frames); worst frame < 13 ms.
6. **Encounters stay linear in play time** (~12,170 per 250 k game-s → ~34,000 ± 10% at 700 k)
   and the store stays bounded.
7. **Determinism at the new horizon:** D's canonical digest is bit-identical across independent
   runs (mine, regen's, the checker's); E's likewise. *Falsified* if any counter differs on a
   rerun of the same command.
8. **Held-out (E, not tuned):** post-wave-1 rss/body at 4.2×10⁵ = 4,743 ± 150 B (the 3×10⁵
   value); catalogue = N + 76 ± 5 at every sample; the wave-1 step is ~2.3-2.5 KB/body; lag
   0.000 and 0 backlog through both waves. *Falsified* if B/body at 4.2×10⁵ deviates > 5% from
   the 3×10⁵ value (that would be a new N-scaling of the per-body state on the plane).

Meaning: (1, 4, 7, 8 confirmed) the 4af4 claim holds on a regenerating record, its horizon
extended past the extrapolated dissolution and its N-axis pushed to this box's ceiling — the
in-box parts of the named gold experiment, with the 10⁶ flight left as one command on a 6+ GB
box (exact command recorded in the dossier). (1 or 4 falsified) memory grows with play at the
plane's scale, on main, measured — the project's named failure mode. (7 falsified) the
canonical-cut protocol itself breaks at the new horizon.
