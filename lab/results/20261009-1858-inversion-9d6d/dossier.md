# Dossier — 20261009-1858-inversion-9d6d (inversion lens)

## Claim

The gold's phase-neighbour certificate (20261006-0346-taleb-09b5: "every real encounter lies within
partner rank 4 along the orbit", O(n·k)) has a k that is not a constant of the geometry: the rank an
encounter's partner occupies at window start is set by synodic drift across the window over local
phase spacing — **k must scale as κ = m·E|Δn|·H/TAU** (fleet size × drift × window, divided by phase
spread) — and a fixed k = 4, measured on a 300-ship fleet, misses ~50% of encounters at 1,200 ships
and ~80% for a bunched 600-ship fleet on the same orbit.

## Bottleneck

The board's top scaling risk ("candidate work at scale; work must track real encounters") and the
seam between representations. The gold replaced the quadratic tier with the phase certificate
"triggered by a dimensionless number"; that trigger decides *when* to switch, but nothing in the
adopted record sizes the certificate itself. If the integrator adopts rank-4 (or any constant k),
the certificate silently drops encounters — a wrong-type error (a miss), the exact failure class the
gold was built to remove — precisely at fleet sizes the board targets (10⁶). Expected gain: none in
compute; it prevents adopting a miss-generating certificate, and it supplies the missing half of the
design: the same dimensionless number that triggers the certificate must also set its width, with
cost m·k ≈ O(encounters), which stays encounter-linear.

## Evidence

Exact truth per pair (the crate's rigorous conservative-advancement truth, independent solver path),
fleet on one orbit (a uniform in [1, 1+band], Rayleigh e σ_e = 3e-4, uniform phase, ρ = 1e-3 unless
stated), window H = 50 orbits, rank = circular |order| distance in the mean-longitude sort at t = 0
(what a rank-k certificate can see). Raw: `evidence.jsonl`.

| scene | κ_pred | p50 | p99 | miss(k=4) | tier pairs/enc |
|---|---|---|---|---|---|
| anchor: the gold's own `coorbital` spec (m=300, band 1e-4, seed 20261010) | 0.75 | 1 | 3 | 0.05% | 21.4 |
| m=300, band 4e-4 | 3 | 2 | 9 | 13.3% | 21.1 |
| m=600, band 4e-4 | 6 | 3 | 15 | 30.6% | 23.0 |
| m=1200, band 4e-4 | 12 | 5 | 28 | 50.8% | 23.8 |
| collapse: m=300, band 1.6e-3 (same m·band as above) | 12 | 4 | 25 | 48.0% | 28.3 |
| m=600, band 4e-4, H=25 (half window) | 3 | 2 | 9 | 12.7% | 46.2 |
| m=600, band 4e-4, seed 999 | 6 | 3 | 16 | 35.0% | 23.3 |
| m=600, band 4e-4, ρ=3e-4 | 6 | 3 | 16 | 28.8% | 87.3 |
| **bunched fleet**, m=600, band 4e-4, phase window TAU/8 | 48 | 15 | 98 | 80.4% | 3.1 |

1. **The gold reproduces in its own domain:** its exact scene gives p99 = 3, miss(4) ≈ 0. Rank 4 was
   safe there by a factor ~5 because κ = 0.75 — an accident of m = 300, band 1e-4, H = 50.
2. **k scales as the law says:** at fixed band, p99 goes 9 → 15 → 28 for m 300 → 600 → 1200 and
   miss(4) 13% → 31% → 51%; encounters grow ∝ m² (2,130 → 7,808 → 30,168, ×14.2 over ×4 m), so a
   κ-scaled certificate still costs O(encounters).
3. **Dimensionless collapse:** at fixed κ the rank distribution is the same scene regardless of how
   κ is composed — (m=300, band 4e-4, H=50) vs (m=600, band 4e-4, H=25) are identical (p50 2/2,
   p90 5/5, p99 9/9); (m=300, band 1.6e-3) matches (m=1200, band 4e-4) (p50 4 vs 5, p99 25 vs 28).
4. **ρ does not enter the law** (only counts): ρ = 3e-4 gives the same stats with 3.8× fewer
   encounters. Seeds agree (35.0% vs 30.6% miss at m=600).
5. **A bunched fleet is the killer** (fleets fly bunched, not uniformly spread): local phase spacing
   8× tighter ⇒ κ 48 ⇒ p99 = 98, miss(4) = 80%, and even k = 64 misses 6.4%. Same law, one more
   factor: κ = m·E|Δn|·H/W with W the fleet's phase spread.
6. **The tier is not cost-quadratic at these bands** (pairs/encounter ≈ 21–28 flat in m): the gold's
   135× was the near-identical-orbit window-setup degeneracy it already killed; the certificate's
   residual failure mode at scale is misses at fixed k, not its cost.

**Reproduce** (each ≤ 30 s, 6 threads, < 100 MB; Linux x86, load 1.3–2.2 of 8 recorded, orders of
magnitude only): build `cargo build --release -p emergent-encounters --bin rank` (source:
`crates/encounters/src/bin/rank.rs`, added by this run), then e.g.
`CARGO_TARGET_DIR=<target> <target>/release/rank 1200 4e-4 3e-4 1e-3 50 777 6`
and `.../rank 600 4e-4 3e-4 1e-3 50 777 6 0.7853981633974483` (bunched). One JSON line per scene;
anchor uses seed 20261010, band 1e-4.

## Predictions

`predictions.md` was written before the grid; P1–P8 held (P7 within its stated band, P8 exact); P9
held on p99 (98, predicted 90–130) and missed narrowly on the two sub-numbers I under-predicted
(p50 measured 15 vs predicted 20–30; miss(4) 80.4% vs predicted > 85%). The kill criterion did not
trigger (anchor p99 = 3 ≤ 4; m1200/m300 p99 ratio 3.1 > 2).

## What would make it wrong

- If the certificate is re-applied with a horizon much shorter than one orbit, κ shrinks ∝ H — but
  the law carries H: at per-kick cadence (H ≈ 1 orbit) a 10⁶-ship fleet on the gold's own band
  (1e-4) still has κ ≈ 50, and a bunched one far more; fixed k = 4 misses most encounters. Only
  H ≲ 4/κ restores rank-4, i.e. re-derivation every 4/κ-th of a window.
- If "partner rank 4" was always meant as "rank κ, tuned per fleet", this run supplies the tuning
  law and the miss curve, and the design note shrinks to one sentence.
- The rank measured is at window start in a mean-longitude sort; a certificate sorting by true
  longitude or re-sorting mid-window shifts constants, not the κ scaling (collapse across (m, H, W)
  pins the mechanism).

Cost of adoption: one dimensionless number (κ, from m, band, window, phase spread — all already in
the certificate's trigger) setting k and the re-derivation cadence; no new state, no per-orbit work.
Fit with PRINCIPLES: "Certificates need independent, adversarial checks" and "types of errors and
not just errors" — a fixed k turns a zero-miss certificate into a silent dropper, the wrong error
type; and "the simulation decides, not us" — k must come from the fleet's own drift number, not
from a constant measured once at m = 300.

## The lens

Inversion attacked the most recent gold's silent assumption (that its measured rank is a
scale-free property) rather than the tier's window math (already red-teamed by the gold and
components-4643). May have missed: 2D swarms (e- or ϖ-spread wide enough that "rank along the
orbit" is the wrong sort entirely — encounters there may need a second certificate, not a wider k);
inclined/3D fleets; κ at the trigger seam (a fleet at the concentration threshold, half in, half
out); and the checker should try e-spread ≫ band, where the radial gate closes and the encounter
set thins differently than any scene here.
