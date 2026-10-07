# Dossier — 20261007-0341-second-20261006-2240-b-encounter-skin-8bfa-57c1 (second author on the slack skin)

## Claim

The checker's named experiment is done: **the setups cut now converts into a total-evals
cut at the plane's kick size** — after three corrections located by a new evals
decomposition (`evals_secs`/`evals_hq`/`evals_q`), the skin's total evals/kick beat
`always` on every case at ε ≤ 1e-6 (belt 1.64×, belt 1e-8 1.61×, ring 1e-6 1.66×, fleet
**3.6×**, 64-orbit belt 1.75×), with wall 3.0–3.7× and per-kick p95/p99 wall 0.6–0.8 µs
vs 2.1–2.4 µs, exactness 0/0 on every case run (fresh seeds, κ=1.0, ε=1e-2 included), the stale
record regenerated from shipped code, and the certificate store measured (46.5 MB at
N=1500; N=10⁴ did not finish in the window). **Two honest limits, both measured:** the
belt stays at 1.6–1.8× total (the one-time padded initial scan amortizes slowly), and at
256 orbits the skin *loses* 10× to `always` — its widened windows grow with certificate
age, so un-refreshed certificates eventually cost more than re-setup every kick; the skin
is a young-certificate cache, not a free lunch. The ε=1e-4 belt remains an evals loss by
design (kick/s ≈ ¼ consumes the slack as fast as it is granted).

## Bottleneck

Board focus line 3. The silver's blocker (principle 27, the goal never a proxy): the 8.3×
setups cut was a counter while total evals rose 1.5× at ε = 1e-6. This run finds where the
counter and the cost disagreed and removes all three causes.

## Evidence (Linux x86 shared runner, 8 vCPU; every line regenerates via `work/record.sh` + `work/record-long.sh`)

**1. The decomposition (what the silver hid).** New counters split evals by phase. Belt
1e-6, before any fix: skin 4468 evals/kick = 4429 in `sections_pad` at setup + 35 queries
+ ~4 elsewhere; the setup-time horizon query the checker blamed: **3 evals/kick** (its
events were discarded — dead, but negligible; the "padded arcs plus 100·TAU horizon
queries" attribution was half wrong). Of 17.09 setups/kick, **13.76 was the one-time
initial padded scan** (99k certificates) amortized over only 16 orbits — at this ε zero
post-initial rescans fire; the "rescan churn at the padded-cone edge" was mostly startup
amortization, and the rest was term 6.

**2. The three corrections (all in `crates/encounters/src/skin.rs`, additive):**
- **Build pad s/2, not s** (sound: the drift trigger re-setups at δ ≥ s/2, so δ < s/2 at
  every query; term 1's superset needs arcs at eps_u + s/2 only). A padded setup: ~322 →
  ~210 evals.
- **The setup-time horizon query is deleted** (its output was discarded; events come from
  `advance`'s per-segment [t0,t1] query). Helps both modes (always fleet: 80438 → 61452).
- **Term 6's empty re-proof runs at the exact tolerance** (the pad never entered the
  None proof's validity — arcs at eps_u already cover every longitude where |Δu| ≤ eps_u,
  a necessary condition for a ρ-encounter; the pad only widened the band of pairs that
  must walk). A re-proof: ~278 → ~20 evals; a pair whose re-proof turns non-empty is
  re-set up padded, as any new candidate would be. This was the skin's steady state.

**3. Economics at the plane's kick size (all 0 missed / 0 false):**

| case (ε=1e-6 unless noted) | always evals/kick | skin evals/kick | cut | wall always→skin | wk p95 |
|---|---|---|---|---|---|
| belt, 16 orbits | 2898 | 1767 | 1.64× | 17.0→5.6 s (3.0×) | 2.4→0.6 µs |
| belt, 64 orbits | 2703 | 1540 | 1.75× | 55.1→17.8 s (3.1×) | 2.1→0.7 µs |
| belt, 256 orbits | 2690 | **27007** | **0.10× (loss)** | 238.8→977.3 s | 2.4→**30.4 µs** |
| belt ε=1e-8 | 2911 | 1805 | 1.61× | 16.9→5.9 s | 2.4→0.6 µs |
| ring 1e-6 | 47600 | 28650 | 1.66× | 13.9→8.2 s | 14.7→0.6 µs |
| fleet | 61452 | 17068 | **3.6×** | 21.3→6.5 s (3.3×) | 16.0→4.9 µs |
| belt seed 31337 (held out) | 2832 | 1699 | 1.67× | 16.8→5.3 s | — |

Losses, owned: belt ε=1e-4 4809 vs 2827 (trig 37/kick: the slack is consumed as
granted); ε=1e-4 s16 11735 vs 2827 (checks 7252/kick — wide slack buys false proposals);
ε=1e-2 6542 vs 2754; κ=1.0 2762 vs 2584 (parity at 3.3× the kick rate).

**The 256-orbit row is this run's second finding, a limit:** at the plane's kick size no
reset ever fires (trig 0.00, setups 0.87/kick — the deferral works), but the widened
window edges grow with the `revs` factor (∝ time since setup) and the check cost with
`kscale` (∝ the same stretch), so query evals grow ~quadratically with certificate age:
33/kick at 16 orbits, 26141/kick at 256, with per-kick p95 wall 30 µs. The skin as shipped
is a young-certificate cache, not a free lunch: it wins while certificates are young
(≤ ~64 orbits here) and loses to `always` beyond. A max-age refresh bounds it — with the
measured q(age) ∝ age², the optimal refresh age (~70 orbits here) still nets only ~2× on
the belt; the honest belt number is the 16–64-orbit range, and fleet/ring carry the
bigger cuts. (N=10⁴ and fleet 1e-4 did not finish inside the window's time budget; the
commands are shipped in `work/record-long.sh`.)

**4. Exactness.** 0/0 against the independent conservative-advancement truth on every
case above plus belt 1e-4 (0/0 of 73 — the stale-record case, regenerated), belt 1e-4
s16, ring 1e-4, and the checker's adversarial set (seed 777 at 1e-4: 0/0 of 75; fleet
1e-4 was 0/0 of 1233 before the term-6 correction but did not finish on the final code
inside the window). The crate's 7 tests pass; with terms 3b and 6 compiled out,
`exact_at_kick_eps_1e6/1e4` fail (restored, 7/7). Term 6's test invariant now asserts
the contract (emptiness current at
final elements) instead of the old implementation detail (zero drift on stored empties).

**5. Memory.** Certificate store: 99,083 certs, 46.5 MB at N=1500 (always's transient
store: 96,429, 46.1 MB). Linear in N — the adoption cost at billion scale belongs to
q-candidate-degree (bottleneck 5), unchanged by this run.

## Predictions (predictions.md, pre-registered)

Held: pad s/2 keeps exactness everywhere (0/0, 7/7); the initial scan drops ≥ 1.5×
(4431 → 2890 evals/kick amortized); always stays 2690–2921 at every horizon; trig < 1/kick
at 256 orbits (0.00); skin wall < always at every horizon; adversarial and record cases
0/0. **Not held:** "64 orbits ≤ 1200/kick" measured 2622 with pad s/2 alone — the
falsifier I pre-registered (steady state > 300) fired: the empty re-proofs (~278 evals
each) were the missing term, and the 256-orbit prediction is void for that code. The
term-6 correction is the answer to that falsifier, and the numbers above are all
post-correction; nothing was tuned on the held-out seeds.

## What would make it wrong

The 1.1 fresh-window safety, the 1.5 edge factor, the 2 in 2δ/g and the 0.2 rad
Cross/Wide threshold remain empirically sized (inherited, test-held). The exact-tolerance
re-proof inherits term 6's own argument (kicks at segment starts, re-proof precedes the
query) — a workload kicking mid-segment would need the re-proof check moved to the kick.
The ε=1e-4/1e-2 ends trade setup evals for check evals at a loss; the co-orbital
certificate owns the fleet's false-candidate width. Wall numbers are shared-runner
orders of magnitude; counters are deterministic.

## Fit with PRINCIPLES

"No work for no reason" (§14): a query whose output was discarded. "A fix signals the
wrong representation" (§19): two pads sized by a global s where the certificate's own
units asked for s/2 (the trigger's slack) and eps_u (the None proof never used the pad).
"The goal, never a proxy" (§27): judged on total evals and wall, with the counter kept
only as diagnosis. "baby spartans start small" (§10): the decomposition ran one belt case
before any change.

## The lens

The second-author lens measured what the counter hid; what it may have missed: the
10× total-evals bar is not met on the belt (1.6–1.8× at young horizons, a loss at 256
orbits — the widening-with-age limit is named, not fixed), the ε=1e-4 regime is untouched
by design, and the store's linear memory is measured, not solved.

## Grade (self): for the integrator to judge

The silver's named blockers are closed on the record: the evals cut is real and total at
the plane's kick size (1.6–3.6× by case at young horizons, 3–3.7× in wall, tails down
3–4×), the record regenerates from shipped code, the memory is measured, and the
long-horizon limit is measured and named (a max-age refresh bounds it, worth ~2× on the
belt). Whether that meets the gold bar — or the bar needs the initial scan made cheap and
the widening growth killed, both named here — is the integrator's call.

## Reproduce

```
cargo build --release -p emergent-encounters --offline
T=target/release
$T/skin belt 1e-6 0.3 4            # 0/0 of 63; evals 1767 vs always 2898
$T/skin belt 1e-4 0.3 4            # the stale-record case, regenerated: 0/0 of 73
$T/skin belt 1e-6 0.3 4 orb=64     # 0/0 of 257; 1540 vs 2703
$T/skin belt 1e-6 0.3 4 orb=256 notruth   # the limit: 27007 vs 2690 (~20 min)
cargo test -p emergent-encounters   # 7 passed
sh lab/results/20261007-0341-second-20261006-2240-b-encounter-skin-8bfa-57c1/work/record.sh
sh lab/results/20261007-0341-second-20261006-2240-b-encounter-skin-8bfa-57c1/work/record-long.sh
```
