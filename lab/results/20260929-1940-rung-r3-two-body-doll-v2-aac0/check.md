# Check — rung r3 v2 (two bodies as one doll), run 20260929-1940-aac0

## Abstract

The run is **incomplete and voidable**: no `metrics.json`, `dossier.md` or picture exists (`author-final.md` still "Working...", an `assists.py` re-run was still burning CPU at check time), and the handoff leg **crashed in the author's own log** (55 reference crossings, 0 doll crossings, polyfit on an empty vector), so no `handoff_energy_growth_exponent` exists from anyone; I report `null` → verdict VOID on incompleteness. Binaries reproduce exactly, but `r3lib.schw_cycle` dropped the `cos χ` in `dφ/dχ = √(p/(p−6−2e·cosχ))` (the frozen Rust has it): with the one-term fix, verified against an independent Binet-ODE to 1e-13, eob-doll gets period 1.0 (645 judged), ν-effect 1.0 (800 judged), reading-B precession 40/40 (author: 0/40) — yet precession still cannot be judged: the true doll-vs-oracle gap `(8.5+2.25e²)/p ≥ 0.81%` exceeds the half-tolerance for all p ≤ 1000, so `min_judged_seeds = 0` and the rung's `judged` criterion is unmeetable — the author's rung-design finding, confirmed with clean numbers. The stored assists json (0.047 pass) predates the current code; my spot-check of 4 seeds against a converged reference gives 0.25–0.66% (passing), so `assist ≥ 0.99` is not established in either direction. eob-doll fails `judged` and `prec` on reproduced numbers alone, regardless of the handoff/assist voids.

## The state of the run

- No `metrics.json`, `dossier.md`, `picture.*` or `handoff_data.json`; `run.log` empty; `author-final.md` = "Working...". The author's outer session sat in `lab/run.sh wait` on a re-run of `assists.py` (27+ CPU-min, ~seed 40/64) that never finished inside this check's window.
- `handoff.log` (20:40:57), the author's own run: `reference crossings: 55` (warning: fewer than 100), `doll crossings: 0`, then `TypeError: expected non-empty vector for x` in `np.polyfit`. The shot IC (`x0=0.994, ẏ0=4.0846`, a 2:1-resonance grazer with a≈0.63 AU, r_apo≈0.993 AU) crosses the SOI about every 2.2 yr, not twice per year; the patched doll then loses the resonance after the first handoff and records zero crossings. Predicted fallback ("co-orbital chain, report honestly") never ran. I could not rebuild a 100-crossing case inside the check window and refuse to fabricate the number.

## Reproduction (every number)

- `assists.json` (64 flybys, 20:13): pass fraction **0.0469**, median err 2.9%, max 13.0% at b = 45 R⊕, |Δv| 6.4–7.6 AU/yr. **Stale**: the file predates the current `assists.py` (20:19) — see Assists below.
- `validate.py` **crashes** (`float()` of a length-1 array under this numpy) — the author's anchors were not re-runnable as shipped.
- Oracle: `eih_EJ`'s closed form equals the Rust literal-ratio form to 4e-15 over 2000 random seeds (and cures the Rust's e→0 division by zero, which I hit). `damour_derelle` matches the Rust line-for-line. Cross-checked against the repo's `eih_ode` (exact 1PN EIH dynamics, ported): the DD period agrees to 8e-5 at p=1000, but the DD advance `6π/J²` differs from the exact-1PN advance by −5.2e-3 at p=1000 — an O(1/p) framing offset the *repo itself* carries (`eih_weak_series` returns `6π/p` as the advance). Not the author's fault; the rung freezes `damour_deruelle`, so I judged against it as frozen. It inflates the doll-vs-oracle gap by (4+2e²−νe²)/p.

## The port bug (decisive)

`r3lib.py:59`: `K = np.sqrt(pt/(pt - 6.0 - 2.0*et))` — constant. The frozen Rust (`gr_oracle_extended.rs:143`): `dphi = (p/(p - 6.0 - 2.0*e*chi.cos())).sqrt()`. The author kept `e`, dropped `e·cos χ`. Consequences against my Binet-ODE ground truth: at (p,e) = (100,0.3) Δφ +3.2e-3 and T +4.2e-3; (100,0.6) Δφ +6.4e-3, T +1.0e-2; (20,0.6) Δφ +4.4e-2, T +7.1e-2 (relative). The periastron advance carries a p-independent `≈ e/3` relative error — the author's own npz shows it (`EPS_PREC = 0.0118` at p=932, e=0.0066, where the true gap is 0.0081). It contaminated the eob/test precession pass fractions (0/40 under reading B), the period at e²/p level, and both truncation-estimate readings (EPS_*), since the estimates were built from the same buggy doll. With the `e·cos χ` fix alone: reading-B precession **40/40 pass** (author: 0/40), period 1.0 over 645 judged seeds, ν-effect 1.0 over 800 — the doll design itself behaves.

## The rung-design finding, confirmed clean

With the corrected quadrature the faithful truncation estimate (reading A: exact-vs-oracle at ν=0) is `(8.5+2.25e²)/p`, min **0.81%** > the 0.5% half-tolerance for **every** seed in [20,1000] (the sampler's p_max = 993): `precession` judges 0 seeds even for a correct doll, so `min_judged_seeds = 0` and `judged ≥ 64` fails for all three configurations. The author's headline number ("min gap 0.76%", 7.6/p) was bug-contaminated, but the conclusion stands: a 1% precession tolerance at p ≤ 1000 sits below the oracle's own truncation plus framing; v2's exclusion rule starves the metric it was meant to clean. This is a property of the frozen rung, not of the doll.

## Assists

Author prediction 0.9–1.0 pass; the stored json says **0.0469** — but that json is **stale**: it predates the 20:19 rewrite of `assists.py`, and its stored |Δv_ref| (6.58–7.43 AU/yr on my spot-check seeds) disagrees with my converged reference (two RK4 resolutions agreeing to ~2e-10; |Δv_ref| = 8.95–9.12 AU/yr) by ~20%. Running the **current** doll against my reference on seeds 0, 10, 32, 50 (b = 2.6, 31, 12, 43 R⊕) gives errors **0.25%–0.66% — all within the 1% bar** the stored json fails (it claims 1.8–9.6% there). So the stored pass fraction likely misrepresents the current code; the author's own re-run (never finished in-window) was presumably regenerating it. Two caveats found: seed 1 shows a churn pathology (my doll trace records **454,568 SOI legs** on one flyby — the exit bisection re-enters immediately), and the stored json lacks the predicted `turn` angles entirely. Full-set verification (64 × ~1 min of converged integration) exceeded the check window; `metrics-check.json` therefore carries the only full-set number in existence (0.0469, provenance-stale) — the rung's `assist ≥ 0.99` outcome is **not established** in either direction.

## Spec deviations and smaller notes
- `test-mass` orbits the **total** mass M=1 with ν=0 invariants; the rung says "a fixed M = m₁". Outcome-neutral (it fails ν 0.0; with the corrected quadrature it also fails period, 0.9008, matching the rung's intent better than the author's 1.0).
- `events_per_orbit = 0` (analytic binary doll, no kicks): defensible reading; the handoff case's 2 crossings/star-planet-year also passes ≤ 512 under any reading.
- Each stage restarts `Random(20261002)` fresh rather than continuing one stream; reproducible, disclosed.
- `predictions.md` (20:12:45) predates all decisive outputs ✓ held-out honored. Scored above: binaries period/ν held, reading-B precession held for a *correct* implementation (the bug betrayed the author's own prediction), handoff prediction failed outright; the assists prediction (0.9–1.0) fails against the stored json but my spot-check suggests the *current* code may meet it — unresolvable in-window.
- Adversarial checks I ran: e→0 and e=0.6, p=20 and p=1000, ν=0.25 (Binet-ODE vs both quadratures); exact-1PN ODE vs DD at six (p,e,ν) corners; closed-form identity over 2000 seeds.

## What the author missed

The `cos χ` in the one formula they ported by hand; that their truncation estimates were self-referential (built from the same buggy doll they were excusing); that the handoff case needed a fallback path they had predicted but never built; and that `assists.json` was left on disk from a superseded version of `assists.py` with no provenance marker, so the run's only full-64 assist number describes code that no longer exists. Also: no guard against SOI-boundary churn in the patched doll (454,568 legs on one flyby).

## Metrics provenance (metrics-check.json)

Binaries: my corrected-quadrature recomputation on the author's exact 1024-seed set, faithful reading A (test-mass period 0.9008 differs from the author's 1.0 — same criterion outcome, fail, for the negative). `assist_pass_fraction`: the only full-64 number in existence (author's stored json, provenance-stale; my 4-seed spot-check against a converged reference contradicts it in the doll's favour). `handoff_energy_growth_exponent`: `null` — nothing exists to reproduce; with a null the rung verdict is VOID (incomplete), the truthful state of this run: eob-doll already fails `judged` and `prec` on reproduced numbers alone.
