# Dossier — 20261007-0842-fermi-fc22 (Fermi lens): the 10⁹ budget and H_live

## Claim

H_live is bounded in steady play — not by clever reabsorption but by physics: every dynamics-side distinction source at 10⁹ bodies produces ≤ 1 MB per 300-hour game — and the term that actually breaks 10⁹-in-8 GB is the **store's uniform tube precision** (16 GB raw, 2.35 TB as measured today, before any dynamics), so the memory work is tiered materialization, not scar management.

## Bottleneck

Board item "fitting 10⁹ in 8 GB", decided by distinctions per game-second; handoff "Risks to attack first": "not measured yet". Expected gain: kills the scar-ledger design track (nothing to build), redirects memory work to quantum tiers (shipmem's shelf), and gives encounters a steady-state churn number at 10⁹.

## Evidence

Machine state: GitHub Actions runner, 8 vCPU, load 0.22/0.48/0.90, 13 GB available, Linux x86 (orders of magnitude only). All commands < 60 s.

Measured anchors:
- `cargo run --release -p emergent-universe --example plane -- 100` → **2349 B/body today** (N = 28, overhead-dominated; the tube word itself is 16 B). Budget at 10⁹: 8 B = 64 bits/body all-in.
- `python3 lab/results/20261007-0842-fermi-fc22/ledger.py` → `ledger-out.json` (0.5 s). Belt model: 3D Chandrasekhar flux, kick δv = 2Gm/(b·v_rel), first passage = max(single-kick rate at b* = 2Gm/(v_rel·q), diffusivity D/q² with ln Λ ≈ 22). Two in-script Monte Carlos validate the machinery: the kick tail is x⁻² to 3 decimals at three thresholds, and the first-passage rate D/q² to 1%.

The ledger at 10⁹ bodies (belt 2–3.3 AU, σ_e = 0.02, q = 10⁻⁶·v_kep ≈ 1.9 cm/s, 300-h game):

| source | rate | ledger per game |
|---|---|---|
| belt–belt gravity (m = 10¹⁵ kg each) | 2.7×10⁻¹² /body/s | 18 KB |
| same, 30× tighter belt (rung-calibration gap) | 8.1×10⁻¹¹ /body/s | 546 KB |
| physical collisions (M_belt = 10²¹ kg) | 0.31 events, all bodies | 16 bits |
| 10⁶-ship formation, sub-km flybys | 1.4×10³ events | 9 KB |
| near-cone fine quantum (10⁶ bodies, q = 10⁻⁹ v_kep) | 2.7×10⁻⁹ /body/s | 0.02 MB |
| player inputs (~10 bits/s) | — | ~4 MB |

Every dynamics term is ≥ 3 orders under the 8 GB budget. The player, not N, sets the ledger (principle 5 in action).

Budget terms at 10⁹, ranked by how far they break:
- **births: 16 MB** (0.126 bits/body, gold `components-98bc`) — 3 orders under. Never binds.
- **store: 2.35 TB measured today / 16 GB at the raw 16-B tube** — 294× / 2× over, **at birth, before any dynamics**. Breaks first.
- **throughput: 1.7×10⁴ kicks/s worst case** (all 10⁹ at 0.39 AU, 2⁷ kicks/orbit; 10³/s for a 2.5 AU belt; 39/s and 2.4/s with the known 0.3/orbit averaging) — ≤ 1.7% of a second at 1 µs/kick. Not breaking.
- **bandwidth:** view gather ≈ 100 MB/s at 60 Hz (estimate) against ~60 GB/s. Not breaking.

Two design numbers that fall out:
1. **The belt-mass ledger constraint:** the 30-bits/body ledger budget (10⁻⁸ crossings/body/s) is crossed at per-body mass 6×10¹⁶ kg (≈ 18-km rock) at N = 10⁹ in this geometry — i.e. total belt mass ≈ 6×10²⁵ kg (10 Earth masses; and the threshold relaxes as √N at fixed volume). Any belt the plane would actually ship (≤ 10²³ kg) sits 3–4 orders under budget. There is no mass regime between "negligible ledger" and "these are planets, they get dolls".
2. **Far-belt certificate churn at 10⁹: ≈ 2.7 element-word writes and recertifications per game-second** at the far quantum — the O(N²) candidate fear has a ~3/s steady-state exit rate, so 99.999% of far bodies' certificates never need re-touch in a play session. At the rung's ρ = 10⁻⁴·a a single flyby of a 10¹⁵-kg rock changes δv by 9.5×10⁻⁶ m/s — two orders below even the far quantum; only the accumulated drift crosses, at the D/q² rate above.

## Predictions

`predictions.md` held 7 predictions. **P1 and P2 failed as numbers, in the same direction, and the failure is the run's most instructive result:** I had predicted the quantum-crossing rate ≤ 10⁻³⁰/body/s and "no sub-stellar mass reaches budget"; the script gives 2.7×10⁻¹² and a 6×10¹⁶ kg threshold — my mental G·(10¹⁵ kg) was off by 10⁹. The Fermi *conclusions* survived with 2–4 orders of margin, but the estimates themselves were worthless until computed: exactly why the lens says estimate *then verify*, never estimate alone. P3 came in 3× under its range (0.31 vs 1–100 collisions/game; conclusion unchanged, stronger). P4 (1.4×10³ events, in range), P5 (1.7×10⁴ ≤ 3×10⁴), P6 (model 32× under the rung's measured rate — within the predicted 2 orders; covered by the tight-belt sensitivity row) and P7 (tiered store 4.0 GB at tube floor ≤ 6 GB) held.

## What would make it wrong

- A belt shipped with ≳ 10²⁵ kg in one volume at fine quantum (crosses the ledger budget; must live coarse — self-consistent, since a coarse quantum pushes the threshold as q²).
- Gameplay distinction sources I cannot see from physics: wrecks, salvage, faction marks (AI is off the plan) could write bits per body per event at player intensity — bounded by the same 4 MB/game class as player inputs unless the design writes per-body history deliberately.
- My rates are belt-geometry-dependent (the 32× gap to the rung's belts); the ln Λ floor and sheet saturation are Fermi-grade, not fitted. All conclusions carry ≥ 2 orders of margin against these.
- The 2349 B/body is at N = 28 (fixed overhead included); the marginal live-body cost is lower. The tiered-store arithmetic uses the tube floor for the near system.

## Cost of adopting

Nothing to build (a kill, not a feature): drop any design work on per-body scar logs (the current-state word IS the collapsed ledger — "the right representation always just feels right"); put the memory work into quantum-tiered materialization (shipmem shelf) with the belt-mass constraint as a gate; treat far-belt certificates as write-rarely (≈ 3/s at 10⁹).

## Fit with PRINCIPLES

- "The cheapest compute is compute not done. Delete before optimizing" — the ledger design track deletes itself.
- "Compute only surprises… redshift and co are not derived but emergent" — sub-quantum influences accumulate in deterministic drift and are never stored; only quantum crossings write.
- "The memory floor is information-theoretic" — the floor here is births (16 MB) + player inputs (~4 MB/game); everything above it is cache, free to tier by distance.
- "A fix signals the wrong representation" — a growing scar structure would be the fix; the collapsed word is the right representation.

## The lens

The Fermi lens sees mass, distance and rates; it does not see *designed* information (what a game designer makes ships remember). It also nearly validated its own headline with wrong constants — the estimates moved by 14–18 orders under the script, so any Fermi number in this dossier that the script did not print should be read as a structure, not a value.
