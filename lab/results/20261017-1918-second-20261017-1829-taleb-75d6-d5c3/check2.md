Grade: gold

**Abstract.** The commissioned experiment is done and reproduced: at one common absolute
tick per seed, against the finest ladder, the symmetric clock start pays the identical per-body term
as ed3a's stagger (ρ(on−off, sym−off) = 0.90; medians 2.09/2.08×10⁻⁷) — direction-1's
successor is refuted, and 75d6's seed-2 "resonance drowning" is proven to be that run's horizon bug
(arms read one belt orbit from their reference; verified in 75d6's frozen CSVs). Checker2
extensions: held-out seed 3 fires 2.9–4.3× with ρ = 0.97; three orbits confirm the bill is one-time
(the differential decays); ref10 drops the seed-1 ω firing under the 3× bar (2.59×), so
the freezable statement is the ref-free 3.0–3.4× band, not a 3× bar. Adopt: close direction 1, price
the bar at the gates.

## Reasons

**Reproduction.** The runner's `regen.sh` exited 0 and regenerated `analysis.json`; every dossier
number I cross-checked matches it. I re-applied `work/patch.diff` to a clean tree, rebuilt, and
recomputed the headline numbers from the raw CSVs with my own code (not `analyze.py`): K2 ratios
(on 2.82/2.54/3.00, sym 2.48/2.43/3.05 at s1h1 vs ref9 on ln a/e/ω), same-tick differentials
(2.07/2.07×10⁻⁷), K5 ρ (0.904/0.898/0.902 at h1; 0.798/0.798/0.743 at h2), seed-2 ratios (ln a
3.10/2.92, e 4.03/3.78, ω 3.80/3.91), C1/C2, P5 (alive 128/128, refusals 0, every arm), P8, wave
widths — all match within median convention. The common-tick readout is real: the `tick` column is
byte-identical across arms in every CSV. `analyze.py` is clean — all 128 bodies, no selection, and
in K5 the reference cancels exactly (d = on − off).

**Predictions.** `predictions.md` (mtime 49 min before the dossier, 16 min before `analyze.py`)
predates the decisive artifacts. The pre-registered criteria all resolved: K1 passes (max |z| 0.99 /
2.59), K2 fires for both arms on ω at the registered point (ref9, s1h1), K3 passes (deltas +0.15 /
+0.27), K4 passes, K5 ρ = 0.90 ≥ 0.7 — "the two arms pay the same per-body term". The Fermi
expectations are honestly accounted: P1 and P7 wrong, and their failure is the run's discovery (the
4.8× was still tick-inflated; the drowning was v1's horizon bug). One gloss: P2's registered
quantity (K2_sym(ln a) ≥ 3) did **not** fire on any seed (2.46/2.48 s1; 2.80/2.92 s2; 2.85/2.92 s3)
— "P2's core (sym pays like on)" is the mechanism reading and is true, but the registered number
belongs under "wrong" too.

**Adversarial cases (mine; three, each outside the author's tested range).**
1. **Seed 3** (75d6's checker's held-out seed, on which v1's instrument fired 86–200×): at the
   common tick vs ref9, both shapes fire ≥ 3× on e (4.31/4.34) and ω (3.24/3.33), ln a 3.36/2.85;
   ρ(on−off, sym−off) = 0.97. The kill direction and the shared-term mechanism hold on a third seed;
   v1's 86–200× is confirmed instrument-bound, now 2.9–4.3×.
2. **Three orbits past the wave** (author measured 1–2): class ratios 1.7–3.1× (no growth past the
   bar), same-tick differential decays monotonically (on 2.09→1.53→1.31, sym 2.08→1.82→1.50 ×10⁻⁷;
   h2/h1 0.73/0.87, h3/h2 0.85/0.83). The one-time, non-compounding typing holds on a longer arc.
3. **ref10** (the author's own named missing rung; settle 157 s, exactly 2× ref9's kicks): at s1h1
   nothing fires ≥ 3× (on 2.53–2.59, sym 2.50–2.91 across the three elements), and ref9−ref10 ≈
   ½ ref8−ref9 (the ladder converges). The ω@h1 firing is ladder-marginal exactly as the dossier's
   "what would make it wrong" cautioned.

**Novelty.** The symmetric arm (`ES_STAGGER_SYM`), the K5 decomposition, and the v1 seed-2
horizon-bug diagnosis are all new; the wiki page's direction 1 explicitly named this experiment, and
docs/HISTORY.md holds no stagger entry. The horizon-bug claim is verified against 75d6's frozen
branch: `off_s2` at mult=2 (tick 30,946,906,758,455), `ref_s2` at mult=1 (tick 15,473,453,379,227) —
one belt orbit apart, exactly as the dossier states.

**The page.** Faithful in substance; corrected in place where it misled: the blanket "2.5–3.0×"
band is seed-1's (across seeds vs ref9 it runs 2.4–4.3×); the "e 2.4–2.5×" clause hid that seed-2's
e fires 3.7–3.9× for both arms — a number in the run's own `analysis.json` that the dossier also
omits; direction 1's ref10 request is answered (do not freeze a 3× gate on ω@h1). Not a closure:
75d6 stands silver, so fewer than three gold runs agree on this topic.

**Goal fit.** Two premise kills, both measured: the adoptable-successor premise (direction 1) and
the resonance-drowning scope carve-out. PRINCIPLES #9 — "A failed experiment kills that
configuration, never the method": what dies is the symmetric-shape hypothesis, and the measurement
hands the decision to the gates; #13 — "types of errors and not just errors": the term is typed
(one-time, unbiased, non-compounding, shared), which is what makes it priceable. The birth-wave
cure's compute claim (ed3a's 17×) is untouched and the wave spread is shown to survive in the
symmetric arm, so the 10⁹-bodies thread keeps its cure with the legality question converted from
"which shape" to "which bar".

**Why gold and not silver.** Gold rests on the premise kill and the instrument corrections, not on
the asked-for "illegal at the registered 3× bar" phrasing: that firing survives at ref9 on every
seed (ω everywhere, e on seeds 2–3) but not at ref10 on seed 1, so no 3× bar may be frozen on it —
a sharpening the dossier itself pre-registered as its own fragility, not a hole in the work. Nothing
named remains that would change the conclusion: I ran the three obvious next experiments and all
landed inside the run's stated envelope. The work is adoptable within one step (close direction 1,
price the bar), which is the gold rule.

## What the author missed

- P2's registered quantity (K2_sym(ln a) ≥ 3) failed on every seed; the dossier counts P2 as right
  via its "core" and should have carried the number under "wrong".
- The K2 seed-2 line omits that e fires ≥ 3× for both arms there (3.9×/3.7× in `analysis.json`) —
  it strengthens the kill and was left on the table.
- No ref10 arm (disclosed): my run shows the 3× firing at the registered point is not ladder-robust,
  so the "grade asked" justification is fragile even though the honest headline already covers it.
- Seed 2's quietness is measured at one orbit past the wave only (disclosed); slower resonance
  growth over many orbits remains unmeasured, as does any third stagger shape (disclosed).
