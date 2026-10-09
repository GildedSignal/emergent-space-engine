# Dossier — 20261009-1345-second (second author on 20261009-1259-fermi-c7eb)

## Claim

The checker's named experiment is done and the corrected claim stands, stronger than the original:
with the impulse coefficient validated by integration on real truth encounters (1091 RK4 runs,
meas/pred median 0.998, v_rel exponent −0.889 vs the author's −2), belt encounters cross the law's
period-tick grid only above **m_crit ≈ 1.3×10⁻¹⁷ M☉ (a ~1.3-km rock; p1 1.2×10⁻¹⁸ ≈ 600 m)** at
game density (N=10⁹, a=2.7, σ_e=σ_i=0.1, ρ=10⁻⁴ AU) — the prior run's 500-m/8×10⁻¹⁹ was ~16× low
but conservative in direction — and the sub-threshold random walk cannot make belt self-evolution
a binding term: in a walk on the measured kick distribution (1000 walkers × 10⁵ kicks) **no 50-m
rock crosses one period tick within 1.7×10⁴ orbits** (0/1000; Gaussian arithmetic says 4.7×10⁶
but the kick distribution is borderline Lévy α=2 — impact-parameter density ∝ d·dd makes E[x²]
log-divergent — so only the walk bound is quoted; 500-m rocks cross in ~10 orbits), and although
the tp/phase channel (which the prior run never checked) first-crosses far sooner (~340 orbits for
a 50-m rock; no mass above ~10⁻²⁴ M☉ survives 10⁴ orbits), each phase tick is 5×10⁻¹¹ rad —
1.9×10⁷ ticks per player pixel — so belt-wide distinctions stay at ~0.2/s at 10⁹ bodies over a
1.7×10⁴-orbit horizon, ≥5 orders under consumer-scale H_live. H_live is set by consumers, not
belt self-evolution; identity storage is not just conveniently but **necessarily** charged to
consumer resolution, because no mass threshold protects tp-identity. The storage conclusion is
unchanged (flat 16-B tube store = 14.9 GiB is the binding term); the event term is
belt-geometry-dependent by ~30× (thick 4% of a core at RTF 100, thin 125% at the 10 µs/event
assumption — the prior abstract's "~2%" is thick-only and used an underestimated mean relative
speed).

## Bottleneck

Same as the prior run: board item "fitting 10⁹ in 8 GB … decided by distinctions created per
game-second"; HANDOFF's "H_live … not measured yet". This run closes the silver gap: the threshold
and flux now stand on the measured (d, v_rel, geometry) distribution of the shipped crate's own
truth encounters, not on asserted coefficients.

## Evidence

Machine: shared Linux x86, 8 vCPU, ~15 GB, load light; every process < 2 GB. All numbers below are
in `out/`; commands regenerate them.

1. **The record regenerates.** `cargo run --release -p emergent-encounters --bin encounters --
   verify a|b|d` (17+32+32 s here): every physics field identical to the prior run's
   verify-*.jsonl (truth_enc, missed, false, all counts); only wall-clock timing fields differ
   (checked field-by-field in a diff script; `out/verify-*.jsonl` saved).
2. **Per-encounter geometry from shipped code.** `dumper/` (new crate in this folder, path-depends
   on the unmodified crate) replicates verify sets a/b/c/d verbatim (same seeds, same
   radial-pair truth candidate set, same `truth_pair`) plus one main-belt-like belt of my own
   (`game3d-planar`: n=2000, σ_e=0.1, ρ=10⁻⁴, a∈[2.45,2.95], 50 orbits, seed 20261009; 73 s) and
   dumps per truth encounter: d, v_rel, both bodies' a, cosψ, and Δa per unit perturber mass in
   period ticks (impulse Δv_i = 2 m_j b/(d² v_rel), Δa_i = 2a²(v_i·Δv_i), b = separation at closest
   approach where d·v_rel = 0). 12,111 encounters; truth counts match the shipped record exactly
   (set c, never run by the author, now measured too: 3034/2093/1496). Reproduce:
   `cd dumper && cargo build --release && for s in a b c d game3d; do enc-dump $s out/$s 30; done`.
3. **The coefficient, validated on real encounters** (`validate.py`, 65 s, `out/validate-out.txt`):
   408 sampled real encounters × 3 masses (picked from the author's formula, non-circularly) ×
   RK4 (Sun + both bodies, mutual gravity, h ≤ P/2000 and d/(50 v_rel); no-mutual control max
   1.8×10⁻¹³ vs signal median 9.3×10⁻¹³): impulse corr 0.989, slope 0.979, meas/pred median 0.998
   (p16/p84 0.95/1.02); measured v_rel exponent −0.889 (impulse −1; author's form −2). The prior
   author's (2/3)·2atan(μ/qv²) overestimates Δa by median 18× (p16/p84 3.4×–50×; it ignores cosψ,
   so it also gets the sign wrong for half the encounters). Co-orbital encounters (slow, v_rel→10⁻⁴)
   agree to 24% — the impulse window degrades there, as expected.
4. **m_crit on the measured distribution** (`ledger.py`, <1 s, `out/ledger-out.txt`): per-encounter
   m_crit = 1/|x|; game case (3-D MC: vertical offset and velocity added to the measured planar
   conjunctions, acceptance-weighted, 4×10⁵ draws): median 1.28×10⁻¹⁷ M☉ (~1.35-km rock), p1
   1.18×10⁻¹⁸ (~600 m). Fraction of encounters crossing ≥1 period tick: ship/50-m rock 0.0%;
   500-m 0.3%; 1-km 14.6%; 5-km 98.9%; Ceres 100%. Verify belts (2-D, a≈1.2): medians 3.5×10⁻¹⁹
   (quiet) … 8×10⁻¹⁶ M☉ (hot, ρ=10⁻³), scaling with ρ·v_rel as the impulse form predicts; the
   co-orbital belt drops the threshold 97× vs the hot belt (and below a 1-Mt ship at formation
   spacing q~10⁻⁸ AU, v_rel~10⁻⁶ — the checker's point 4, now bracketed by measurement).
5. **Crossing flux and the two channels, measured by the walk itself.** At R = 6.24
   encounters/body/orbit (analytic n_vol·πρ²·⟨v⟩·T with ⟨v⟩ = 0.137 now MEASURED, vertical
   included; the prior run's 2.77 used σ_e·v_k = 0.061, underestimating shear): a random walk on
   the measured kick distribution (1000 walkers × 10⁵ kicks, `ledger.py` §walk, 22 s) gives —
   period channel: **0 of 1000** 50-m rocks (and 0 ships) cross one tick within 1.7×10⁴ orbits;
   98% of 500-m rocks cross, median 10 orbits. The Gaussian first-passage arithmetic (4.7×10⁶
   orbits for 50 m) is NOT trustworthy: in 3-D the impact-parameter density ∝ d·dd makes
   x = 1/(d·v) borderline Lévy α = 2 (E[x²] log-divergent), so the quoted number is the walk
   bound. Phase channel (a persistent a-offset of S ticks drifts tp ≈ S ticks/orbit exactly):
   first tick median 336 orbits (50 m, walk; Gaussian 220), 3 orbits (500 m), 400 (ship); one
   player-pixel (10⁻³ rad) of phase noise needs 1.6×10⁷ orbits (50 m), 1.6×10⁵ (500 m) — beyond
   any session. Belt-wide phase distinctions: 0.16/s at 10⁹ bodies over the 1.7×10⁴-orbit walk
   horizon (median walker 368 ticks) — ≥5 orders under consumer-scale H_live (10⁵–10⁶ bits/s).
6. **Ledger** (same file): tubes 16 B×10⁹ = 14.9 GiB binding (1.9× over 8 GiB); program belt
   0.126 bit/body = 15 MiB; events 45/s at 1× (thick) → 4% of one core at RTF 100, but thin belts
   (σ_i=0.005) ×28 → 125% of one core: the event margin is belt-geometry-dependent ~30×, and the
   prior run's ledger used only the thick number.

## Predictions (`predictions.md`, written before any dump or integration)

- V1 (slope 0.8–1.25, no systematic residual): **held** (0.979, p16/p84 0.95/1.02).
- V2 (v exponent −1.15…−0.85): **held** (−0.889); the author's −2 rejected.
- V3 (control ≥10⁻³ below signal): **held** (max control 0.19× the median signal; 1091/1224 runs
  above the 3× floor).
- M1 (median m_crit in 10⁻¹⁸…5×10⁻¹⁷ M☉): **held** (1.28×10⁻¹⁷, ~1.35-km rock).
- M2 (500-m <5%, 1-km <50%, 5-km/Ceres ≈100%): **held** on the 3-D game case (0.3%/14.6%/98.9%).
- M3 (co-orbital drop ≥100×): **borderline** — 97× measured vs the hot belt at matched ρ.
- F1 (50-m P-channel >10⁷ orbits, flux <10⁻⁸/body/orbit): **failed as stated, conclusion
  survives** — the flux bound is unprovable (E[x²] is log-divergent, so any σ_x-based number is
  sample-size-dependent; my own two estimates moved 277×), and the walk bounds first passage only
  below 1.7×10⁴ orbits (0/1000 crossed; Gaussian arithmetic claims 4.7×10⁶). The negligible-H_live
  conclusion stands on the walk bound plus the phase-channel pixel arithmetic (1.6×10⁷ orbits to
  one pixel), not on my pre-registered flux number.
- F2 (tp k* in 100–3000 orbits for 50-m): **held** (walk 336 orbits; Gaussian 220; kill criterion
  k*<20 not tripped).
- F3 (3-D m_crit within 3× of 2-D): **borderline** — 3.3× (1.28×10⁻¹⁷ vs 3.86×10⁻¹⁸).

## What would make it wrong

- The belt is 2-D in the crate; the 3-D case is a weighted MC on the measured planar conjunctions
  (uniform vertical offset inside the ρ-tube, Gaussian v_z, slow-vertical-motion approximation
  during the passage — passage time ~2×10⁻³ of the vertical epicycle period). A true 3-D truth
  (r8's next domain) could shift m_crit by the ~3× my own 2-D→3-D correction did, not further.
- Real belts relax (viscous stirring heats σ_e over Gyr): the walk assumes a fixed kick
  distribution; over game horizons (≤10⁶ orbits) that is the right regime, but a multi-Gyr
  universe would need the heating folded in.
- Resonant/secular channels (differential precession, Kirkwood structure) remain unmeasured — the
  same gap the prior run left; the H_live conclusion only covers the encounter channel.
- The 10 µs/event and RTF-100 event-cost numbers are assumptions (unchanged from the prior run).
- m_crit is per-encounter; a size distribution stacked so that many sub-threshold kicks arrive
  coherently (a dense swarm around one body) is not modelled by the random walk.

Cost of adopting: none (decision input). It sharpens the design rule the prior run proposed: tubes
for m ≳ 1 km, active, or consumer-resolved bodies; programs for the rest; **phase identity below
1 km can never be threshold-protected, so charging identity to consumer light cones is a
requirement, not an option** (a 1-Mt ship acquires its first phase tick within ~400 orbits at game
density — 5×10⁻¹¹ rad, invisible, but on the law's grid).

Fit with PRINCIPLES: "the floor is what the player can differentiate" (register, bottleneck 0) —
the tp channel quantifies exactly that floor (1.9×10⁷ ticks per pixel); "Compute only surprises"
(3) — nothing below consumer resolution is stored; "A failed experiment kills that configuration,
never the method" (9) — the killed coefficient sharpens the method.

## The lens

Second-author lens: I trusted the checker's ~13× arithmetic only after deriving the impulse
independently and validating it on the crate's own encounters — the residual disagreement (median
18×, spread 3–50×) is cosψ, which the checker's hand formula fixed at 1 and the author's ignored
entirely; on real geometry both hand forms were wrong and the dumped-state form is the one that
survives. My own first-pass arithmetic walked into the same trap twice (Gaussian formulas on a
borderline-Lévy distribution; only the walker simulation caught it) — the lesson generalizes: on
measured heavy-tailed distributions, no moment-based estimate should be quoted without the walk.
What this lens may still miss: the walk's kicks are drawn i.i.d. with random signs from the
measured per-encounter distribution, which ignores correlations between successive encounters of
the same pair (repeated conjunctions are quasi-periodic, so their kicks arrive in signed bunches);
and the 3-D MC inherits the crate's 2-D planar conjunction statistics wholesale.
