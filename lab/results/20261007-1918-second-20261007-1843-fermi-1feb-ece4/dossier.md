# Dossier — 20261007-1918-second-20261007-1843-fermi-1feb-ece4 (second author on the Fermi run)

## Claim

The checker's named experiment is done and the silver's claim **holds, measured**: at 10⁹ the slice-free belt rate (0.0153 events/body/game-s, this box) times the **measured** scar cost of the plane's own kicks on the shipped Shelf (39–56 bits/kick, exact readback) puts H_live reabsorption at **75–107 MB/game-s** — inside the silver's assumed 37–292 MB bracket, low half — and the affordable hot fraction at rtf 1 (designed 3 µs kick) at **13 %** (silver said 5–10 %; the slice-free fix raises it). One premise-level finding: **the shipped belt column space cannot hold the plane's real orbits** — `Key::darwin`'s domain (p ≤ 8192 M, L ≤ 4096) excludes **100 %** of 682 captured kick ends (plane orbits at p ~ 10⁸ M, planets at 0.4–5 AU in star-GM/c² units) — so B18b's belt at game scale needs another column basis; the tube's own (p Q16, k Q48, ω, t_p) basis, used here, works. And the saturated belt (every body kicked once) holds **~70 bits/body ≈ 2.2× the whole 32-bit state budget**, so reabsorption must refit the program, not merely delete scars.

## Bottleneck

Board "fitting 10⁹ in 8 GB" and "distinctions per game-second (H_live)": the two binding numbers of the silver (reabsorption rate, affordable hot fraction) move from assumption to measurement, at zero adoption cost; the domain kill says B18b's belt, as shipped in `pop`, is measured in a part of the orbit space the game never visits.

## Evidence

Shared Linux x86 runner, 8 vCPU, load/meminfo in each JSON. Driver crate in `work/scarkick/` (path-deps on the shipped crates; no crate edits — `git status` clean except `lab/results/`).

```
cd lab/results/20261007-1918-second-20261007-1843-fermi-1feb-ece4/work/scarkick
CARGO_TARGET_DIR=./target cargo build --release --bins            # ~40 s
./target/release/capture 1 10 48 kicks-seed1.json                 # 0.3 s
./target/release/capture 1 25 400 kicks-seed1-m400.json           # 2.5 s
./target/release/capture 7 25 48 kicks-seed7-s25.json             # 0.5 s
# pool with the python one-liner in the run log -> kicks-pooled.json (11,076 kicks)
B=./target/release/shelfrun
$B kicks-pooled.json 1048576 40 0.0001 plane 5EED 0 19661918714588 > shelf-2e20-doll0.json      # 1 s
$B kicks-pooled.json 1048576 40 0.0001 plane 5EED 2 13846749307529 > shelf-2e20-doll2.json
$B kicks-pooled.json 1048576 40 0.0001 synthetic 5EED 0 > shelf-2e20-synth.json
$B kicks-pooled.json 1048576 120 0.001  plane 5EED 0 19661918714588 > shelf-2e20-doll0-r1e-3.json
$B kicks-pooled.json 1048576 60  0.01  plane 5EED 0 19661918714588 > shelf-2e20-doll0-r1e-2.json
$B kicks-pooled.json 8388608 40 0.0001 plane 5EED 0 19661918714588 > shelf-2e23-doll0.json
/home/glmlab/lab-target-1/release/xtask universe --bench --rtf 100 --seconds 15 --members 0 --seed 1
python3 ../budget2.py
```

- **Regenerability.** My capture replays the `--kick-bench` loop verbatim (same script, same dedup, same pure resolver): seed 1, rtf 100, 10 s → **663 distinct kicks = the shipped bench's 663 rebinds**; refused 0. Digests in each summary JSON.
- **Domain kill.** Converting both kick ends into the shipped belt columns (`Key::darwin` on both OrbitKeys) excluded **682/682** kicks: periapses 3–5×10⁸ root units vs darwin's 8192 M cap (scenario: Home at 99.3e6, Giant at 5e8 = 0.39–5.2 AU). The tube-native basis (p Q16, k Q48, ω u32, t_p ticks) loses only 19/682 (passage ends): that basis carries the belt.
- **Scar bits per kick** (shipped Shelf, `update`+`compact`, readback `bad=0`; belt = the ladder's perfect convoy program rebuilt at plane scale in this folder, 1.91 bits/body at birth, `inferred_ok=true`): sparse rate 1e-4 — **39.1 bits** (doll 0, 2²⁰), **41.2** (2²³: scale-free), **56.1** (doll 2, the fleet/encounter regime), synthetic-ladder control **62.2** (the plane's real kicks are *cheaper* than the ladder's uniform ones: median |Δp|, |Δk| ≈ 2^14 quanta, 62 % of doll-0 kicks move t_p not at all, |Δω| ~ 2 turns). Dense: 1e-3 → 43.5 bits/kick; 1e-2 (~47 % of members scarred) → 55.1 bits/kick and **32.92 bits/body held**, i.e. ~70 bits/body saturated.
- **Slice-free rate.** `--members 0` seed 1: 49.0 events/wall-s ÷ rtf 100 ÷ 32 bodies = **0.0153/body/game-s**; rtf held (median ≈100, 0 overflow frames — the silver's 21 overflows were box load, as the checker suspected). `bytes_per_body` here 2451 (silver quoted 5067 on a 76-body scene: it is a scene-dependent field, confirmed).
- **Budget** (`budget2.py`, every quoted number): compute 45.9 core-s/game-s belt-only designed (rtf_max ≈ 0.13), hot fraction ≤ 13 % at rtf 1; H_live creation 0.60–0.86 bits/body/game-s → the 32-bit budget fills in 37–53 game-s, reabsorption **75–107 MB/game-s**; bandwidth 3.9 GB/s per rtf. Ranking unchanged: compute first, H_live second, bandwidth third.

## Predictions

`predictions.md` written before every run. Held: capture count 663 (650–670), slice-free rate 0.0153 (0.012–0.030), dense-regime bits/kick 55 ∈ [40,150]. Missed, all informative: (a) the darwin bridge hit my own kill criterion **harder than predicted** — 100 % excluded, not 10–40 % (the belt program's domain is 10⁴–10⁵× below the game's orbits, a fact, not noise); (b) delta magnitudes ~2^14 quanta, far below my 2^20–2^38 (one kick's rebind barely moves the orbit: that is why the exact memo never hits and yet scars stay cheap); (c) so plane kicks cost **less** than synthetic ones (39–56 vs 62, I predicted more), and reabsorption lands at 75–107 MB/game-s, below my 250–800. Direction errors reported, not absorbed.

## What would make it wrong

- The belt generator is mine (this folder), not the shipped `pop::ladder` — unavoidable, since the shipped one cannot express plane-scale orbits (that is the finding); its structure (all-shared columns, t_p affine 2^12) is the ladder's own, and the Shelf/compact/scar path is 100 % shipped.
- Kick deltas are doll-local; I replay each doll's kicks on a belt at that doll's own captured scale. Only 48 of 11,076 pooled kicks are doll 0 (the star's doll — the billion-body belt's home); the 39.1 bits/kick rests on those 48 distinct deltas, cycled. More seeds would firm the tail.
- ~70 bits/body saturated extrapolates from 47 % scarred at one delta scale; fatter deltas (deep encounters) would raise it.
- Shared-box timings; orders only; the integrator re-measures on the M1.

## Cost of adopting, and fit

Zero code adoptions; three input lines change: reabsorption 75–107 MB/game-s (measured), hot fraction ≈ 13 % at rtf 1 (slice-free), and **B18b's belt needs a game-scale column basis** (tube (p, k) basis measured; darwin/Key basis killed for belts at 1 AU) before its ladder numbers can speak for the game's belt. PRINCIPLES: "The memory floor is information" (24) — the floor is now measured, not assumed, and the saturated belt is 2.2× the budget the goal allows, which forces refit-not-delete on the allocator; "a failed expectation is not a failed method" (H0183/9) — the darwin miss killed the bridge, and the measurement went through the tube's own basis instead.

## The lens

A second author inherits the first run's framing: I nearly measured "bits per kick" in a column space (E/L via darwin) the game cannot use, and only the 100 % exclusion forced the representation change — the same trap the first run's lens section named for the allocator. The saturated-belt number is the one this lens could have missed: per-kick creation fits the old bracket, but the *stock* held once every body is kicked (70 bits/body) is what actually breaks the 8 GB promise, and no per-kick rate shows it.
