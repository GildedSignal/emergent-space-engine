# Dossier — run 20261012-0311-scout-6759 (lens: scout)

**Claim (one sentence).** A real kicked belt generates ~10² bits of per-body
distinguishing information in its first orbit (67 bits/body at 1 km / 2⁻²⁴-angle
quanta, then ≈ +1 bit/orbit, diffusive log-law), which is already ~2× the entire
4 GiB/10⁹ live budget, and neither a Chebyshev tensor deformation (0.4%
absorbed) nor Fourier harmonics ≤5 (10% absorbed) absorbs it — so at 10⁹ bodies
the population-program store survives only if high-harmonic action-angle
programs absorb the kick field (open, next rung) or reabsorption runs about
every orbit.

**Bottleneck.** Board item "fitting 10⁹ in 8 GB … decided by distinctions
created per game-second" and HANDOFF risk "H_live … not measured yet". Expected
gain: the number that sizes `crates/shipmem`'s reabsorption cadence and the
scar-word widths; it deletes the guesswork in B18-family gating (10⁰–10¹: it
changes a design constant by a factor ~2–30, not an algorithm by 10×).

## Evidence (commands, each ≤ 60 s, all from this folder)

```
python3 h_live2.py ctl control    # 18.9 s: ZERO distinctions, all epochs  (P1 pass)
python3 h_live2.py cold cold      # 25.1 s
python3 h_live2.py res resonant   # 24.1 s
python3 h_live3.py                # Fourier-basis repair (timed out at 2880 cols)
python3 h_live4.py                # cheap Fourier variant, harmonics<=5, 1 orbit
```
Model: plane-native kick semantics — exact analytic two-body program, kick =
perturber impulse per P/32 interval (H0190 cadence), 6-pt Gauss–Legendre along
the program arc (Encke's trick: only the deviation is computed). Planar belt,
16 384 bodies, Jupiter (m/M = 9.54e-4, a = 5.2 AU, e = 0.048) as the only
kicker. Deltas quantized on belt-scale quanta (a: 1 km, e: 10⁻⁷, angles:
2π/2²⁴); every count below is an integer count. Machine: Linux x86, 8 vCPU,
numpy 1.26.4, processes ≪ 2 GB.

Measured (medians over 256 epochs; JSONs in this folder):

| Quantity | Cold belt | 3:1 resonant | Control |
|---|---|---|---|
| Raw per-kick delta entropy | 51.4 bit | 51.2 bit | 0 |
| After deg-3 tensor fit (256 cols) | 51.3 bit (absorbed 0.4%) | same | 0 |
| Shuffle control absorbed | −0.2% (estimator valid) | — | — |
| Scar stock after orbit 1 / 8 | 66.6 / 77.3 bit/body | 66.0 / 76.9 | 0 |
| Fourier harmonics ≤5 (816 cols) | 10.1% absorbed; stock 52.2 bit | — | — |

Budget: 4 GiB / 10⁹ = **34.4 bits/body total** (approved plan budgets,
HANDOFF). Scar word cost at the law's own grid style is 1.9× over after one
orbit, 2.3× after eight, growth +3.6, +1.9, +1.5, +1.2, +1.0, +0.8, +0.7
bit/orbit — a decelerating (diffusive, ≈ ½log₂k per element) law, mean flow
≈ 1.1×10⁻⁸ bits/body/game-s (P(2.7 AU) = 1.4×10⁸ s).

## Predictions vs outcomes (predictions.md written before each decisive run)

- P1 instrument control (perturber off ⇒ exactly 0): **held** (bit-exact zero).
- P2 shuffle control (absorbed ~0 on permuted data): **held** (−0.2%).
- P3 (≥90% absorbed by smooth function of a, off resonance): **falsified** —
  absorbed 0.4%. Diagnosis (H0183): the kick field is a function of the full
  initial state, dominated by the body's instantaneous phase, not by a; the
  a-basis was the wrong instrument.
- P3b (deg-3 tensor over (a,e,ω,M) absorbs ≥90%): **falsified** — absorbed
  0.37% (256 columns; shuffle floor −0.2%).
- P4 (resonant ≥5× the cold residual): **not observed at 8 orbits** — both
  belts sit at the saturated ceiling; resonant Lyapunov times (10²–10³ orbits;
  Murray & Holman 1997, outer belt ~10³–10⁴ yr) lie far beyond the window.
- P5 (cold breach beyond 10⁵ orbits): **falsified in the interesting
  direction** — breach is immediate (orbit 1) at these quanta; P5b's per-element
  scar word bound (≤24 bit) held (~17–19 bit/element).

## What would make it wrong

- Wrong basis, not wrong physics: if the per-kick delta field is Fourier-smooth
  in the angles (tidal multipoles at harmonic ≲ a/a_J scales), a Fourier×Chebyshev
  program absorbs it and the per-body floor collapses; `h_live4.py` (harmonics
  ≤5, 1 orbit, 816 columns) measured the first rung of that ladder: 10.1%
  absorbed per-kick (shuffle floor −0.6%), stock 52.2 vs 55.0 bit — real but
  far from collapse; harmonics ~11+ remain open. Even then the *stock* must be
  re-fit each program generation — the harmonic content of the deformation
  grows with kick count (phase mixing), which is a reabsorption cost, not zero.
- Quanta: scar bits scale as log₂(kick effect/quantum). Coarser scar quanta cut
  the stock but change the law's grid — the quantized-cell memo already showed
  that changes orbits (5 Oct artifact), so this valve is closed by evidence.
- Session scale: at rtf 100 a one-hour session advances the belt 2.6×10⁻³
  orbits, so a *fresh* belt never breaches during one session at low rtf; the
  budget question bites for long-lived universes, high rtf, and 10⁹-body
  populations that must stay resident — exactly the goal's regime.

## Cost of adopting, and fit with PRINCIPLES

Adoption is informational: `b-h-live` (queued) should measure conditional
(smooth-residual) entropy, never the marginal entropy of deltas — the marginal
is saturated at ~4·log₂N by phase spread and says nothing (measured above).
Reabsorption cadence for shipmem at 10⁹: stock ≤ 34.4 bits ⇒ recompile roughly
every orbit at these quanta (or coarsen scars per-population, accepting a law
change per the memo-artifact evidence). PRINCIPLES: P3/P6 ("compute only
surprises", "store the generator") — the surprise here is per-body, not
shared, at polynomial program order; P24 (the memory floor is information) —
this is that floor measured; P33 (aggregates at scale) — the aggregate fails
to absorb the phase structure, which is the open question; P13 — scars stay
exact integers throughout.

## The lens (what scout may have missed)

Planar model, one perturber, 8 orbits, one seed per belt; inclinations and
self-gravity absent; the "program" was modeled as a fixed-basis least-squares
deformation over initial elements, not a re-derived bijective generator
(components-98bc) — a smarter generator could beat my basis. Prior-art scan ran
thin (two web searches verified: Murray & Holman 1997 Lyapunov times; LSM
write-amplification bounds UNVERIFIED). Encke's method (1852) is the closest
skin-in-the-game ancestor of the program+kick split and is verified by use.

## Prior art, ranked by fit (mechanism → our mapping)

1. **Encke's method** (1852, asteroid ephemerides; compute-starved astronomy):
   integrate only the deviation from a conic program. Already the plane's shape;
   this run measured the *memory* consequence Encke never faced.
2. **Video P-frames with motion compensation** (H.26x; FFV1 lossless): shared
   motion field + per-block residual = Δ-program + scars; the shared/residual
   split is exactly what I measured (and found degenerate at polynomial order).
   Lossy by default — inadmissible (P13), lossless mode exists.
3. **LSM-tree compaction** (RocksDB tiered/leveled; write-amplification theory
   UNVERIFIED at source): scars = memtable deltas, programs = SSTs, reabsorption
   = compaction; predicts a write-amplification floor for re-pay.
4. **Secular / resonant normal-form theory** (Murray & Holman 1997, verified):
   the true absorbable structure lives in action-angle harmonics; our own r4 v3
   kill of nf1/nf2 already showed resonant normal forms mis-pump e — consistent
   with the absorption failing near structure.
5. **Procedural generation + edit overlays** (No Man's Sky; UNVERIFIED detail):
   seeds + sparse diffs at 10¹⁹ scale — existence proof, no cadence theory.
6. **Elias–Fano / Roaring** — already law.md's scar index; orthogonal.
7. **Hashlife memoization** — board candidate; the memo-artifact (5 Oct) showed
   quantized-cell memoization changes orbits, so adoption is law-level.

**Grade suggested:** silver — real, reproduced controls on both sides
(zero-control and shuffle), one held-out prediction held (P1/P2), two
pre-registered predictions honestly falsified with diagnosis; the gold-moving
experiment (Fourier/action-angle absorption of the kick field) is named and
cheap, and the queued `b-h-live` build must incorporate the marginal-entropy
trap regardless.
