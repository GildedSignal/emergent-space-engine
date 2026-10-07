# Dossier — 20261007-1234-second-20261007-1106-fermi-443e-d57e (second author)

## Claim

The checker's named experiment is done and the original claim holds, now on both scene classes: **H_live is not the binding term at 10⁹** — on a concentrated belt with handoffs present (1,096 and 10,096 ships, the restricted class), each doll binding event injects only ~26–27 bits (3.2–3.4 B varint) on the kick path, the handoff path costs ~50 bits per re-reference at a rate of zero for doll-0 passages (law v2: a passage is resolved by the time transformation, so only bodies born in a child doll hand off), residuals reabsorb (late/early 1.04–1.08 over a 3.74×10⁸ game-s horizon ≈ 12 game-years, 1.39M bindings), so at 10⁹ bodies the belt creates **2.6 KB/s** (2.3×10⁷ under the M1's 60 GB/s) and the all-inner anchor, correctly per binding event, is **79 MB/s** (756× under, replacing the original's mixed 182 MB/s); the walls stay **today's stored representation** (1.68 TB at 10⁹ even at the belt's steady 1,682 B/body; the binding history held today is ~0.25–2.5 KB per binding and effectively never pruned at belt cadence) and **inner-cadence event compute** (73 core·s per game-s at 12 µs per binding event).

## Bottleneck

The same board item ("fitting 10⁹ in 8 GB … decided by distinctions created per game-second"), closed on the scene class the silver run had not measured. No 10× engine gain claimed; the risk stays re-ranked to non-binding, and the measurement now names the sharper cache target: per-binding history retention (`prune`'s `oldest − 2²⁶` floor keeps everything at belt cadence — a shipped-code fact, not an information fact).

## Evidence

All from this folder; every number below is printed by these commands (Linux x86, orders of magnitude only; the integrator re-measures on the M1). Instrument: `crates/universe/examples/hlive_belt.rs` (new, in `work/patch.diff` together with the original `hlive.rs`), the original instrument extended to the belt: chunked settle with `prune()` per chunk (the frame path's own rule), sampling each chunk before its history is forgotten, and the two event populations kept apart (same-doll deltas vs doll-change re-references).

```
cargo build --release -p emergent-universe --example hlive_belt --example hlive -j 6   # ~10 s warm
cd lab/results/20261007-1234-second-20261007-1106-fermi-443e-d57e
HLIVE_BELT_OUT=belt_deltas_n1000_s1.bin  <bin>/hlive_belt 1000 1   1 2048 96   # 18 s, decisive
HLIVE_BELT_OUT=belt_deltas_n1000_s2.bin  <bin>/hlive_belt 1000 1   2 2048 96   # 20 s, held-out seed
HLIVE_BELT_OUT=belt_deltas_n10000_s1.bin <bin>/hlive_belt 10000 0.5 1 2048 96  # 71 s, scale row
HLIVE_OUT=plane_regen.bin <bin>/hlive 3600 1 400                                       # 0.3 s, regeneration
python3 fermi_belt.py                                                                  # the 10⁹ table
python3 fermi.py                                                                       # the original table
```

- **Plane regeneration (the record):** every printed number matches the silver dossier (28 bodies, 9,846 B/body, 1,582 kicks, 615 bindings, 323/292, medians 21/20 bits, ratio 1.09, 13.00 B/event) and the delta stream is **bit-identical** to the author's `hlive_deltas_s3600_seed1.bin` (`cmp`).
- **Belt (N=1000+96 crossers, 1 planet orbit at 5.2 AU):** 309,980 distinct bindings (282.8/body; kicks/binding 1.1), 96/96 crossers handed off; rate **7.55×10⁻⁷ bindings/body/game-s**; same-doll delta **27.1 bits/event** (zlib saves 9.0%); handoff re-reference **median 50 bits** (p99 56) per doll-change; reabsorption **1.05** (seed 2: 1.04, 27.2 bits/event, rate within 0.4%). N=10⁴ (0.5 orbit): rate 7.37×10⁻⁷ (**2.5% from N=10³** — per-body, no concentration blowup), 25.6 bits/event, ratio 1.08, 46 µs/engine event. Belt rerun: bit-identical `.bin`, log identical modulo wall lines.
- **The handoff rate fact:** under law v2 `maybe_capture` returns false for every doll-0 ship (step.rs: "every ship of the root doll stays in it; a passage needs no handoff"), so a belt's handoff H_live is zero unless bodies are born in child dolls — measured 96 handoffs, all from birth-crossers.
- **Memory, honestly:** the pre-registered 5-orbit decisive run was killed at ~1.5 GB / ~600k bindings (unpruned history ~0.5–2.5 KB/binding; the 1-orbit run peaks at 0.19 GB, N=10⁴ at 0.34 GB). `bytes_per_body` after the run is 1,682 (N=10³) / 1,291 (N=10⁴) — the 1-orbit cache point, run-length dependent exactly as the checker showed for the plane.

## Predictions

`predictions.md` was written before the decisive runs (only an N=12 smoke test had run). Tally, clean: **7 held, 1 split, 1 missed.**

- Held: handoffs 96/96 (predicted 90–96); same-doll bits/event 25.6–27.2 (25–40); handoff re-reference 50 (40–70); reabsorption < 1.3 (1.04–1.08); rate 5×10⁻⁷–1.2×10⁻⁶ with N=10⁴ within 2.5% (≤×1.5); kicks/binding 1.1 (1.0–2.0); 10⁹-belt creation 2.6 KB/s (≤5 KB/s); held-out seed within 0.4% (≤±30%).
- Split: zlib saving predicted <10%, measured 9.0/9.0/**12.5%** — the bits/event half held, the compressibility half missed at N=10⁴ (still near-incompressible).
- **Missed:** bytes/body after prune predicted 2–6 KB, measured 1.3–1.7 KB — the steady cache is smaller than predicted (safe direction; my range came from the smoke's 3,119).
- Deviation disclosed: the decisive run is 1 orbit, not the pre-registered 5 (the memory ceiling above); the kill is itself a measurement.

## What would make it wrong

The belt is still test-body physics: massless ships, no mutual encounters (the `encounters` crate's tier is not exercised), one planet, 10⁴ bodies measured (10⁵–10⁶ extrapolated from the per-body rate that held constant from 10³ to 10⁴), and the reabsorption horizon is 12 game-years, not 10³. A massive belt whose encounters re-bind bodies (the co-orbital gold's formation) is the next scene class; the instrument carries there unchanged. Cloud timings are Linux/x86. Adoption cost: none (measurement plus two example binaries); `fermi_belt.py` supersedes `fermi.py`'s mixed 182 MB/s line with the separated anchors. Fit: "The memory floor is information-theoretic"; "Measure before claiming" — bits are exact integer counts.

## The lens

The second-author lens made me verify before extending: the plane record regenerates bit-identically, so all effort went to the named experiment. What it may have missed: the belt's zero-handoff law-v2 fact makes the "handoffs present" ask partly a construction (birth-crossers) — a belt with real capture (a redesigned changeover, JANUS) could re-rate the handoff path; and I accepted 10⁴ as the top measured scale rather than fight the 2 GB ceiling for 10⁵.
