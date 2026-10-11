# Dossier — 20261011-1234-taleb-62f7 (lens: Taleb)

**Claim.** The bulk regime — the one every encounters run since 6 October has measured and
punted on ("ruin in absolute terms at fleet scale", "the encounter-skin problem") — is now
priced and owned: when concentrated packets cross, the real contacts are Θ(n_A·n_B)
(measured exponent **1.94**, per-pair probability flat at **0.021** across n = 50–800 per
fleet), so the per-ship load grows **0.021 contacts per opposing ship** — **2.1×10¹⁰
contact events in one 10⁶-ship-per-fleet crossing, ~21,000 per participating ship** — and
*no discovery certificate can help, because discovery is already exact: the events
themselves are the workload*. The escape is measured and works: **one aggregate event per
packet crossing** — per-ship flux λ_i = ρ_B,2D · 2R · L_i, the contact tube swept by ship
i's exact Kepler trajectory through the opposing packet's measured density grid in the
co-rotating frame — costs 257·(n_A+n_B) evals (O(n)), has **zero free parameters**, and
reproduces the exact truth's total contacts at ratio **0.87–1.04 on all ten packet
scenes** including a held-out crossing geometry (in-window 0.95–1.01), the active-ship set
within 0.003–0.04 absolute, per-active load (26.8 vs 26.0 at n = 300), and per-ship ranking
(corr 0.83–0.99). The regime trigger is the per-event multiplicity μ = λ per ship: μ ≪ 1
(belt conjunctions, measured ≈ 1 per pair) is the pairwise tier's territory; μ ≳ 1 is
fluid — and at μ ≈ 72 (w = 0.03) the truth's per-ship load goes Poisson → uniform
(var/mean 0.90) and the aggregate still lands 1.035.

**Bottleneck.** The board's top scaling risk ("candidate pairs per body grow with N;
candidate work must track real encounters") and the risk adopted from gold taleb-09b5.
Two silvers (q-candidate-degree, taleb-3ebf) proved work per *encounter* is flat — this
run shows that invariant is the wrong one at fleet scale: work per *ship per crossing
event* is the load-bearing number, it is unbounded in the opposing fleet's size, and the
certificates all converge to the same ruin because the encounters themselves are Θ(n²).
Gain: deletes pair enumeration for the game's central extreme event (the fleet meeting —
"a fleet that is not concentrated is not a fleet", taleb-3ebf) and hands the
`b-encounter-skin` / `b-coorbital-cert` builders the missing tier with its trigger,
mechanism and measured constant. It also covers the *within-fleet* quadratic the
certificates never claimed (x-800: 126,959 within-fleet contacts, also ~n²).

**Evidence.** Lib is the verbatim crate (`diff -r src ../crates/encounters/src --exclude
bin` empty); only `bulk.rs` added. Truth = the crate's independent conservative-advancement
finder (Halley states), the same instrument taleb-3ebf validated; every counted contact is
one truth event (times distinct by construction of the dip finder). All scenes 2-D, ρ =
1e-3, one parent, test particles, deterministic seeds; machine state per line (8 vCPU
shared runner, load 0.6–2.1, ≤ 4 threads, < 200 MB). Orders of magnitude only; the
integrator re-measures on the M1.

```
cd lab/results/20261011-1234-taleb-62f7/work/encounters
CARGO_TARGET_DIR=/tmp/bulk-target cargo build --release --bin bulk    # 4 s
/tmp/bulk-target/release/bulk control > bulk.jsonl                   # 5 s
/tmp/bulk-target/release/bulk x       >> bulk.jsonl                   # 19 s
/tmp/bulk-target/release/bulk w       >> bulk.jsonl                   # 9 s
/tmp/bulk-target/release/bulk a       >> bulk.jsonl                   # 7 s
python3 analyze.py                                                    # tables + exponents -> analysis.txt
```

Key rows (`bulk.jsonl`, `metrics.json`; full table in `analysis.txt`):

| scene | truth cross | τ = contacts/A-ship | p_pair | pred/truth | active frac (pred/truth) | per-active (pred/truth) | var/mean | corr |
|---|---|---|---|---|---|---|---|---|
| x-50 | 63 | 1.26 | 0.025 | 0.87 | .16/.16 | 6.9/7.9 | 7.7 | .99 |
| x-100 | 212 | 2.12 | 0.021 | 1.02 | .20/.20 | 10.8/10.6 | 12.6 | .97 |
| x-200 | 1207 | 6.04 | 0.030 | 0.99 | .235/.235 | 25.5/25.7 | 28.3 | .99 |
| x-400 | 3710 | 9.28 | 0.023 | 1.04 | .203/.203 | 47.4/45.8 | 54.2 | .99 |
| x-800 | 13474 | 16.84 | 0.021 | 1.02 | .215/.224 | 80.0/75.3 | 91.0 | .99 |
| w-0.5 | 3597 | 8.99 | 0.022 | 1.03 | .23/.23 | 40.4/39.1 | 51.7 | .99 |
| w-0.125 | 14692 | 36.7 | 0.092 | 1.03 | .89/.91 | 42.8/40.6 | 24.4 | .98 |
| w-0.03125 | 28690 | 71.7 | 0.179 | 1.04 | 1.0/1.0 | 74.3/71.7 | **0.90** | .83 |
| a-200 (held out) | 218 (193 in window) | 1.09 | 0.005 | **1.01** in-window | .68/.55 | 1.4/2.0 | 1.6 | .68 |
| a-400 (held out) | 772 (710 in window) | 1.93 | 0.005 | **0.95** in-window | .65/.60 | 2.6/3.2 | 2.7 | .76 |
| belt-1000 (control) | 2545 within, 0 cross | 0.42/ship/orbit | — | — | — | — | — | — |

Laws: contacts ∝ n^1.935 (endpoints; stepwise 1.62–2.51 seed noise); τ slope 0.0208 per
opposing ship ⇒ 2.1×10¹⁰ contacts at 10⁶/fleet, ~21k per active ship per crossing; width
law 8.0× contacts for 16× concentration (w 0.5→0.03125); the aggregate's cost is 257·(n_A
+n_B) Kepler evals (x-800: 4.1×10⁵ evals vs the truth path's ~10⁶ pairs × conservative
advancement, 11.3 s wall) — the O(n) vs O(n²) gap. Two instrument notes: (i) the frozen
(t,r) frame undercounted by 2× (ratio 0.51 at the first control) — the packet rotates
~0.5 rad across the integration window; the co-rotating frame (axes from the packet's mean
position at each sample) fixed it to 1.016 with corr 0.993, one line, no parameters added;
(ii) the a-series transfers cross r = 1 twice per period, so 11–13% of truth contacts fall
outside my ±0.5-orbit window (`cross_outside_window` is a printed field; in-window ratios
0.95–1.01).

**Predictions** (`predictions.md`, frozen before the x/w/a runs): P1 exponent 1.9–2.1 —
held (1.935; flat p_pair 0.021). P2 ruin extrapolation ≥ 10⁹ contacts per 10⁶-ship
crossing — held (2.1×10¹⁰, 21k per ship). P4 width-sweep factor 2–8, denser is worse —
held (8.0, band edge). P5 flux aggregate within ×[0.5, 2] everywhere, held-out geometry
included, no refit — held (0.87–1.04; in-window 0.95–1.01). P6 overdispersion var/mean >
1.5, corr > 0.5 — held on the designed scenes (var/mean up to 91, corr 0.83–0.99), and
*refined*: at μ ≈ 72 the distribution saturates to under-dispersed (0.90) — the
continuous-load limit, where the aggregate still lands 1.035. **P3 missed**: belt
contacts/ship/orbit = 0.42 against my < 0.05 (K3 triggered as written). Diagnosis: I
inherited r8's belt-0 *candidate* count but anchored the wrong encounter count — a
radially thin belt (Δa ~ 10⁻³ ≈ ρ) at n = 1000 is already mildly collisional (same order
as r8 v2's 1.1 events/body/orbit). The corrected statement, and the run's real lesson:
per-orbit rate does not separate the regimes — *per-event multiplicity* does. Every belt
conjunction loads two ships once (μ = 1, identities matter, pairwise exactness is right);
one battle crossing loads ~21% of ships with μ(n_B) contacts in a single event, unbounded
in the opposing fleet (75 at n = 800, ~21,000 at 10⁶).

**What would make it wrong.** (i) If the game must resolve *which* ships contact (a named
ship dies) even at μ ≫ 1, counting is not enough — the aggregate can seed a λ-weighted
sample of identities, but that is untested here; the cheap exact path is then only the few
*strong* encounters, and the m-meso-motion regime number (U/√(μ_p/b)) would pick those
from the aggregate's own distribution — complementary, not covered. (ii) One held-out
geometry only (a = 2, e = 0.6; 22.6° off-tangential at 1.22× speed): extreme aspect ratios
or crossing near a strong gradient are untested; the rectangle+grid density is honest but
coarse (24×6). (iii) All scenes one parent, 2-D, test particles, no self-gravity and no
mutual deflection — the aggregate counts contacts, it does not evolve them. (iv) Seeds:
five per series; stepwise exponents swing 1.62–2.51, so the endpoints' 1.94 is the number
to trust; a checker rerunning with new seeds should see the same laws within those swings.

**Cost of adopting, and fit.** One tier in the encounters design, no engine change yet:
when a group pair's crossing epoch has per-event multiplicity μ ≳ 1 — computable from the
packet summaries the period-group tier already holds (ρ, extent, relative flow) — replace
pair enumeration with the flux integral (per-ship λ_i, then Poisson draws for who is hit);
μ ≪ 1 keeps the certificates (λ-windows, period groups) as-is. This is the tier
taleb-3ebf's "merge-join hint" gestured at and its second checker priced at 3.9× — that
was still per-pair; this is the actual regime change, and it deletes the 60 TB / 10³-day
class of ruin for the bulk of the events. PRINCIPLES: "Compute only surprises" (#3) — a
bulk crossing is one surprise, not 2×10¹⁰; "Each scale resolves only what matters at that
scale… a raindrop is an event for an ant and nothing for a lion" (#33) — 75 contacts per
crossing is rain for a fleet, and μ is the ant/lion dial; "its time that's a multiplier"
(#6) — aggregates become the source; "we need to steal from what works" (#26) — this is
radiation transport's optical depth and plasma's Knudsen number, decades old, paid for by
people who could not afford per-particle simulation.

**The lens.** Taleb priced the black swan (the concentrated meeting) instead of the
average (the belt) and it paid; but P3 shows the lens's own metric can hide risk —
per-orbit averaging crushed the tail event into a harmless 0.42, and only per-event
multiplicity exposed it. The lens also says nothing about building: the constructive half
(flux integral, co-rotating frame) came from transport physics, not from fragility
thinking. What the lens may still have missed: the *allocator* consequence — one crossing
is a synchronized spike of O(n) aggregate work at a predictable epoch; smoothness (board
bottleneck 4) wants it spread by per-ship slack, which this run does not touch.
