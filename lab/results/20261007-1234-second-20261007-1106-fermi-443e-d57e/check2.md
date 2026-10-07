# Check 2 — 20261007-1234-second-20261007-1106-fermi-443e-d57e

Grade: silver

Abstract: Claim: H_live stays non-binding at 10⁹ on a concentrated belt with handoffs; the sharper target is per-binding history retention. Reproduced in a clean tree from `work/patch.diff`: the plane stream is bit-identical to the silver author's `hlive_deltas_s3600_seed1.bin`; belt N=10³ (309,980 bindings, 7.55×10⁻⁷/body/game-s, 27.1 bits/event, ratio 1.05), held-out seed and N=10⁴ `.bin`s bit-identical; both fermi tables regenerate (belt 2.6 KB/s, all-inner 79 MB/s vs 60 GB/s). Predictions were pre-registered (12:48:00, after only the 12:47 smoke); the 7/1/1 tally is as disclosed. Four attacks of mine held: seed 7 (+1.2%), 2 orbits (ratio 1.05), 8× denser sampling (+6% rate), 4× crossers (29.5 bits/event). Gain: the risk is re-ranked on the checker-named scene class; adoption cost none. Silver because the genuinely falsifying scenes — a massive belt whose encounters re-bind bodies, and real capture — remain unmeasured (the second is not constructible under law v2).

## Reproduction

Clean tree, `git apply work/patch.diff`, `cargo build --release -p emergent-universe --example hlive_belt --example hlive -j 6` (7 s warm).

- `hlive 3600 1 400`: every printed number matches the dossier (28 bodies, 9,846 B/body, 1,582 kicks, 615 bindings, 323/292, medians 21/20, ratio 1.09, 13.00 B/event); the delta stream is bit-identical both to this run's `plane_regen.bin` and to the original silver author's `hlive_deltas_s3600_seed1.bin` fetched from `origin/claude/lab-20261007-1106-fermi-443e` (`cmp`, twice).
- `hlive_belt 1000 1 1 2048 96`: matches the author's log line for line (350,288 kicks, 96 handoffs, 309,980 bindings, 282.8/body, 7.551e-7, 27.1 bits, 3.39 B/event, doll-change 28 events median 50 p99 56, ratio 1.05, 1,682 B/body); `.bin` bit-identical.
- Held-out seed 2: matches (7.575e-7, +0.3%; 27.2 bits; ratio 1.04). N=10⁴: matches (7.367e-7, 25.6 bits, ratio 1.08, 1,291 B/body); `.bin` bit-identical.
- zlib on the three `.bin`s: 9.0 / 9.0 / 12.5% saved — exactly the disclosed split (the N=10⁴ compressibility half is the one miss).
- `python3 fermi_belt.py` / `fermi.py`: every headline regenerates (belt 2,562 B/s; inner 7.93e7 B/s; 23.4×10⁶× and 756× under 60 GB/s; 73 core·s at inner binding cadence).

## Predictions

Timestamps: `smoke.bin` 12:47:09 → `predictions.md` 12:48:00 → `plane_regen.bin` 12:49:06 → decisive belt artifacts 12:51–12:54 → dossier 12:56. Pre-registration is genuine; only the N=12 smoke preceded it. The tally (7 held, 1 split, 1 missed) checks out against my reruns; the missed half is in the safe direction (steady cache smaller than predicted) and the 1-orbit-for-5 deviation is disclosed and is itself a measurement.

## Attacks (four, all held)

1. **Seed 7, a true third realization** (see findings: seed 3 ≡ seed 2): rate 7.642e-7 (+1.2% vs seed 1), 27.2 bits/event, ratio 1.04.
2. **Two orbits (24 game-years, double the author's horizon):** rate 7.647e-7, 27.1 bits, ratio 1.05, peak RSS 0.19 GB — the same as 1 orbit; the bounded-residual claim extends without memory cost at this scale.
3. **8× denser sampling (spo 16384):** bindings 328,796 (+6%), rate 8.009e-7, 27.7 bits/event — the rate anchor is not an undersampling artifact.
4. **4× crossers (M=384, deeper close approaches):** rate 7.641e-7, 29.5 bits/event (+9%), handoff re-reference still median 50 bits, ratio 1.01, 0.68 GB peak.

Code facts verified in the shipped tree: `maybe_capture` returns false for every doll-0 ship (step.rs:397–400, comment matches the dossier's law-v2 quote), and `prune`'s floor is `min(now − 2·light_distance − 2²⁶, oldest − 2²⁶)` (universe.rs:970–971), so at belt kick spacing (~2.4×10⁸ ticks) the `oldest` term retains everything — the "shipped-code fact, not an information fact" claim is accurate.

## Novelty and fit

No HISTORY entry measures H_live on a belt; the parent silver (plane-only, branch `claude/lab-20261007-1106-fermi-443e`) named exactly this experiment in "what would make it wrong", and the 0.126 bit/body program floor it cites is prior gold (components-98bc). This run is that named experiment, done. Board fit: the "fitting 10⁹ in 8 GB … decided by distinctions created per game-second" item; PRINCIPLES: "The memory floor is information-theoretic"; "Measure before claiming" — bits are exact integer counts, and the record regenerates bit for bit.

## Why silver, not gold

Reproduced and pre-registered, but it is a measurement that confirms the parent's premise-kill on a restricted scene class: massless test bodies, one planet, circular ring (e=0), a 12-game-year horizon, and handoffs present only by construction (birth-crossers — law v2 cannot yet produce the real-capture scene that would re-rate the handoff path, and the author says so). No bottleneck moves 10× and nothing is deleted; the risk re-ranking was the parent's contribution, now made robust. The doll-change population is also thin at the reported sampling (28 events; my M=384 run's 112 agree, but the author never stressed it).

**The one experiment:** rerun `hlive_belt` unchanged on a massive co-orbital formation where mutual encounters re-bind bodies (the 20261006-0346 gold's scene), or on any real-capture scene once a changeover exists. If the per-body binding rate stays N-linear and residuals stay bounded there, the premise-kill covers the worst known concentration and the measurement is complete.

## What the author missed

- **`seed | 1` collapses even seeds onto the next odd one** (hlive_belt.rs): the held-out "seed 2" is byte-for-byte the same scene as seed 3 (identical kick and binding counts). The instrument's seed space is odd-only; future runs should pass odd seeds, and this run effectively rests on two realizations (1, 3) — my seed 7 supplies the third.
- The 2-orbit rerun peaks at the same 0.19 GB as 1 orbit, so the 1.5 GB five-orbit kill is superlinear in horizon, not in N — a cheap 3-orbit point would have located the knee of the retention growth the dossier names as the sharper target.
- The eccentric regime (B9's e up to 0.9) is untested; kicks per orbit grow near periapsis, and the ring is circular by construction.
