# check2.md (independent checker, blind to check.md)

**Abstract.** The doll's spin χ is compiled in the crate's representation (`crates/space/src/kerr.rs`: Darwin ψ, root-factored cubic, GL quadrature, all `Scalar`), wired through the adapter; frozen gate B19 passes all six criteria on `--law space` and G1–G6, B16 keep bit-identical lines. Reproduced bit for bit from `work/patch.diff`: advance worst 2.0e-13, fates 1680/1680, dragging 379/379, Penrose 85/85, χ=0 digest `59d54de0f9ead66f` on three sides, 0.26 s; module tests 10/10; `gen_tables.py` regenerates `golden.json`; four negative controls fail; the 7 xtask failures pre-exist on pristine main. My attacks — photon boundaries at six (χ, sense) points vs hand-derived b_c, E=1 retrograde L_mb, whirls at χ=0.9999/e=0.9/1.001×separatrix — agree to ≥10 digits outside the gate's domain. The −8πχ(M/p)^{3/2} coefficient is settled and confirmed. Cost: one file plus an adapter method.

## Reproduction (clean tree, patch applied by me)

- `behave --law space --gates G1,G2,G3,G4,G5,G6,B16,B19`: every number, count and digest identical to `gates-after.txt`; only wall-clock fields differ (B19 0.26 s vs 0.27 s). B19 PASS, all six criteria; G1–G6, B16 unchanged.
- `cargo test --release -p emergent-space --test kerr`: 10/10. Whole crate suite green (61 tests, all binaries).
- `gen_tables.py` (rerun redirected to /tmp): regenerates `golden.json` identically; BPT values match textbook (χ=0.998 ISCO 1.23697M/8.99437M, horizon 1.06321M).
- Controls: `--law echo` PASS B19; `planted-proonly`, `planted-penrose`, `planted-rcapture` all FAIL B19.
- `cargo test -p xtask`: 198 pass, 7 fail — the same 7 (echo events, handoff, plane) fail on pristine main (stash + rerun), so the patch breaks nothing.

## Held-out predictions

`predictions.md` (18:30:01) precedes the decisive B19 run (18:30:36, machine_state agrees). P1 held with margin (predicted ≤1e-5, measured 2.0e-13; 256/256 every cell). P2's first run failed all retrograde fates (864/1680) — the adapter's pre-existing `scalar()` refused negative L and b; the fix (`signed_scalar`, sign plumbing only) touches the judge boundary, not the law or the gate, and is disclosed with both runs kept (`b19-after.txt` → `b19-after2.txt`). P3–P6 held; P7 cost over-predicted (0.26 s vs <10 s). This is the honest-disclosure case, not post-hoc tuning: the frozen seeds were never seen before the predictions.

## Attacks (mine, independent methods)

1. **Photon capture boundary.** Hand-derived double-root conditions (k=2/u³, m=3/u² ⇒ 3u−1 = ±2a·u^{3/2}, b_c = a ± u^{−3/2}, bisected in mpmath) agree with the author's closed forms to 30 digits; the module's `photon_fate` flips Captured/Scattered within ±1e-11 of b_c for all six (χ ∈ {0.5, 0.9, 0.998}) × senses.
2. **E=1 retrograde boundary.** My analytic L_mb = a − (1+√(1+a))² (double root, disc ≈ −6e-39): fate flips within 1e-9 of it. At the exact knife edge the module reads the double root as a turning point (Scattered) — convention-dependent, and the frozen dense seeds keep margins (1536/1536 exact vs the oracle).
3. **Whirls outside the gate domain** (χ=0.998 and 0.9999, e=0.9, p = 1.001× separatrix, advance up to 104 rad/cycle): module matches my own 40-digit ψ-quadrature (own root-finding via polyroots) to ≥10 significant digits — the trapezoid converges far beyond where the gate looks.

## Novelty

H0214 froze B19 (5 October) with the named gap "no Kerr compiler yet". The prior silver `20261006-0030-q-kerr-compile-0528` built the float reference and left the odd-in-χ coefficient open ("the checker should fix it analytically"); this run is the integer-law implementation, the gate pass, and the coefficient. **Bonus verified independently**: from Kerr epicyclic frequencies, Δφ = 2π(1/κ−1), κ² = 1−6u+8χu^{3/2}−3χ²u², the odd part is −8πχ(M/p)^{3/2} (twice the −4π node rate; the prior run's −12π guess is refuted); the scan −8.18π → −8.05π over p = 400→1600 converges as required.

## Goal fit

First item of the board's focus ("rotating holes" — Julien: "especially rotating black holes"). Deletes the second-law alternative structurally: χ = 0 routes to the Schwarzschild core bit for bit (digest identity on all three sides, reproduced), and bound/plunge/capture/light are one cubic's root structure — "no central control and no categories", "floats never decide them" (the law runs on `Scalar`; floats appear only at the judge boundary).

## What the author missed

- **Extremal limit**: `isco(a=1, prograde)` returns 6.0 (true extremal ISCO is 1M; the triple root at the bracket endpoint is sign-blind, so the bisection slides to `hi`). Unreachable through the judge (the adapter rejects χ ∉ [0,1)) and correct for all a < 1, but it is a latent crate edge worth one guard.
- `cycle` at the CYCLE_MAX cap returns its last value without an error flag; nothing in the gate's domain binds (2.0e-13 worst), but a whirl beyond it would silently degrade.
- Non-equatorial orbits (Carter's Q), the band/crossing table and B9 cost structure for Kerr, and M1 timings remain open — all disclosed by the author.
