# Predictions (written before the decisive flights)

Question: the 10⁹ steady-state bill of the plane's belt, composed from measured
constants. Anchors flown on shipped code (`crates/universe/examples/nladder.rs`,
no patch): two cuts a rung — shallow (pre-settle, ≤ ~20k game-s) and deep
(past the first settle at ~26k game-s, ≥ ~40k game-s) — differenced for the
depth rate. Rungs 10⁴ and 10⁵ coast, seed 1.

Constants used in the composition (each cited in the dossier): first settle
~26k game-s ≈ one belt period (20261015-1926-taleb-d6ba); doll interval
2.814e4 game-s ⇒ cadence law 1/2.814e4 = 3.55e-5 kicks/body/game-s
(20261014-1719-fermi-cf45); cycle promotion p50 3.7 µs, passage 316 µs
(d6ba); reads-per-demotion without retention ~12.7 (f55d); kick cost 43–53 µs
(c01c via kick-cadence page), scoreboard 75–160 µs; record stack bpb_engine
980–1,317 B/body at depth (d6ba); arcs at depth 8.6 B/body with the seam
(d6ba); burn knee = demotions, ~1.4 TB at 10⁹ (20261015-1615-quant-0619);
"~0.15 cores re-mint at 10⁹" (20261015-1450-second-…-0757).

- **P1 (the cadence law holds at depth, on shipped code).** The differenced
  depth kick rate (deep minus shallow) lands within ×2 of 3.55e-5 per body per
  game-second, and is N-flat (10⁴ vs 10⁵ within ×2). If it lands > 3× above,
  cf45's interval law is wrong at depth or the wave train adds kicks; if > 3×
  below, the doll's clock is not running at the shipped step and the depth bill
  collapses.
- **P2 (the shallow cut understates the steady state).** The shallow-cut rate
  (≤ 20k game-s) is at least 3× below the depth rate: births are quiet, the
  doll's clock reaches the belt only at the settle. If shallow ≈ deep (within
  ×1.5), every 20k-cut re-mint projection already measured the steady state and
  the "0.15 cores" sentence stands as steady-state.
- **P3 (shipped memory at depth).** b_per_body at ≥ 40k game-s grows ≥ 1.5×
  over the 20 s baseline (2,378–2,632 B/body in artifacts/runs/nladder/ladder.txt)
  — the first settle pins every body's compiled arc — but stays ≤ 5 kB/body
  (no unbounded growth inside two doll periods).
- **P4 (the composed 10⁹ bill).** With P1's rate: kicks at today's cost ≤ ~4
  cores; re-mints with a sufficient cap 0.1–0.3 cores (bracketing 0757's 0.15),
  without a cap (12.7 reads/dem) 1.5–3 cores; the record stack ≥ 100 GB ⇒
  memory binds ≥ 25× harder than every CPU term combined. If the composed CPU
  exceeds ~10 cores or memory lands under ~30 GB, the "record stack binds"
  claim is wrong as composed.
