# Dossier — H_live measured on the plane's dashboard (run 20261009-1210-fermi-e7a9, Fermi lens, directed brief b-h-live)

**Claim.** H_live — live distinguishing bits per game-second — is now defined from the engine's
state and measured on the plane's dashboard: a body carrying a remainder carries a stable ~70–90
bits, reabsorption returns 86–97% of creation past the battle transient, and the net stock sits at
72.7 bits per live body after 15 h in a scene where *every* body is individually managed — so the
8 GB / 10⁹ line is drawn by representation width (~600× the information), not by H_live's growth.

## Bottleneck

Board risk "distinctions per game-second (H_live): not measured yet"; the item that decides
whether 10⁹ fit in 8 GB. Expected gain: not a speedup — a deletion of an unknown (the memory
question now has a measured numerator), which redirects scale work from body count to
representation width.

## What was built (work/patch.diff, applies to main)

- `Universe::live_bits() -> LiveBits`: significant bits of every live body's binding remainder
  (four integers, magnitude + sign; zero is free), bodies carrying one, and the player's decision
  words (8 bits each). Read-only.
- `Dash` samples it after each frame; `Summary::h_live` reports created (sum of rises),
  reabsorbed (sum of falls) and net, per game-second of simulated time.
- `xtask universe --bench` prints the block (`h_live` in the report); the page's `/frame` serves
  it in `dash` and the stats panel shows an H_LIVE line. No gate, threshold or digest path
  touched.

## Evidence (commands, each ≤ 60 s except where marked; Linux x86, orders only)

```
cargo build --release -p xtask
cargo test --release -p emergent-universe            # 52 passed, incl. the plane's digest tests (~4.3 min)
cargo run --release -q -p xtask -- universe --bench --rtf 1    --seconds 55 --unpaced   # 55 game-s
cargo run --release -q -p xtask -- universe --bench --rtf 100  --seconds 55 --unpaced   # 5.5e3 game-s
cargo run --release -q -p xtask -- universe --bench --rtf 1000 --seconds 55 --unpaced   # 5.5e4 game-s
cargo run --release -q -p xtask -- universe --bench --members 5000 --rtf 100 --seconds 20 --unpaced  # ~2 min
curl -s -X POST localhost:8799/frame -H 'Content-Type: application/json' -d '{"keys":0}'  # dash.h_live served
```

| run | game-s | live | carried | bits/body | created /game-s | reabsorbed /game-s | net /game-s | kicks | bits/kick |
|---|---|---|---|---|---|---|---|---|---|
| rtf 1 | 55 | 39 | 17 | 44.9 | 32.7 | 0.95 | +31.7 | 16 | 98* |
| rtf 100 | 5,500 | 49 | 34 | 66.2 | 1.61 | 1.02 | +0.59 | 1,937 | 4.4 |
| rtf 1000 | 55,000 | 45 | 43 | 72.7 | 0.375 | 0.321 | +0.054 | 9,287 | 2.2 |
| members 5000 | 2,000 | 221 | 201 | 85.4 | 23.4 | 12.7 | +10.7 | 7,399 | 6.1 |

\* the rtf-1 figure is the opening transient (the fleet battle: leavers 11, encounters 10) over
16 kicks, not a steady per-kick width. Full tables: `work/estimate.md`; raw reports in `work/`.

- **Digest unchanged:** seed 1, rtf 100, 6 s, unpaced → `a7d089f9…1ca8df7` before and after the
  patch; `crates/universe/tests/h_live.rs` (`sampling_moves_no_digest`,
  `a_kicked_scene_stays_under_the_billion_body_line`) passes, and the crate's whole suite is green.
- **Gate, both ways:** `behave --law plane` fails identically on clean `main` and with the patch
  (G1/G2/G6/B7 "0/256, worst inf, unanswered"; B13 same numbers both ways) — the gate's oracle
  does not answer on this Linux host; pre-existing, not touched (handoff trap: check the oracle's
  domain before blaming the law). B14 times out at 60.0/60.1 s both ways.
- **Fermi extrapolation (work/estimate.md):** program ~0.126 bits/body ≈ 16 MB at 10⁹; exception
  stock ≈ 80 bits × kicked-fraction × 10⁹ (10 GB at fraction 1 — the all-exceptions worst case —
  far under with any generator coverage); flow ≈ 1 MB/s created, 0.15 MB/s net at the 15 h
  per-body rate — trivial against 60 GB/s. `bytes_per_body` on the same dashboard: 5,143–6,089 B
  against 73–85 bits live: **~600×**. The memory bill is the representation, not the information.

## Predictions (predictions.md, written before the decisive runs)

- P4 (digest unchanged): **held**.
- P1 (per-game-second rates rtf-invariant within 2×): **failed** — 32.7 → 0.375 bits/game-s.
  Three measured causes, none of them wall-scheduling: the opening battle transient; the canonical
  script's decision density falling as 1/rtf (28 words at every rtf); the scene quieting
  (encounters 354 → 84 over 10× game time). The rates are functions of game time, which is the
  invariance that matters.
- P2 (per-body < 64 everywhere; net ≤ 10% of gross after the first orbit): **failed on the
  letter** (72.7 bits/body at 15 h; net 14% of gross), **held in spirit** (stock bounded, net
  slope decaying ~10× per 10× game time).
- P3 (20–200 bits/kick): **failed low** — steady marginal width is 2–6 bits/kick; the fit
  discards far less than estimated. The estimate's error direction is the good one for memory.
- Neither kill criterion triggered.

## What would make it wrong

The accounting counts *significant* bits of stored remainders, which upper-bounds true entropy
(coroled bits in an i128 are not independent); if residuals were compressed by their actual
distribution the per-body width would fall further, strengthening the claim. The scene is a war
where every body is an exception and it quiets as ships leave or die: a belt with population
programs and sustained encounters could hold creation flat — that would raise the flow, not the
per-body stock. The "bounded" claim is measured to 15 h of game time, one seed, one scene.

## Cost of adopting, fit with PRINCIPLES

~150 lines, read-only, two fast tests; nothing else moves (digest proven identical). It is the
instrument for "the memory floor is information-theoretic" (PRINCIPLES #24: "this is nowhere near
the floor on the size and information theory says so") and for "compute only surprises" (#3): the
dashboard now prices surprises in bits. Next rung it enables: H_live on the wired belt (b-belt-wire),
where the kicked fraction — this run's missing denominator — becomes measurable.

## The lens

Fermi first: the estimate said 40–160 bits per kicked body and a bounded stock — the stock held
(70–90), the per-kick flow did not (2–6). What the lens may have missed: I estimated the wrong
denominator for the 10⁹ question (per-live-body in an all-exceptions scene) before the runs
corrected me to the kicked fraction; and the page's DOM render is verified at the endpoint level
only (no browser on the lab host).
