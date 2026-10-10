# Check 2 — 20261010-1407-inversion-5c2a (independent, blind to check.md)

Grade: gold

**Abstract.** Claim: the adopted phase-neighbour certificate (gold `20261006-0346-taleb-09b5`) is not zero-miss at O(n·k) for concentrated fleets in general. Reproduced bit-for-bit (ctrl: 2093 encounters, 44,850 pairs, 15,948,922 steps — exactly the crate's frozen `verify.jsonl`): two warm crossing fleets give 43.7% cross-fleet contacts, per-group ceiling 56.3%, and 99% coverage needs 519 certs/encounter against the quadratic tier's 37; retrograde gives 96.4% cross-sense, ceiling 3.6%. Rank stability is the ratio 4e/spacing: my warm single fleet (σ_e = 0.04) covers 22% at W = 1; break-even near σ_e = 0.012; a cold dense n = 1500 fleet still covers 99.5% — the valid domain, positively confirmed. Retro's mirrored truth verified analytically and by brute-force scans. Adopt now, before the queued build: scope the certificate per co-orbital group, gate the trigger on e-spread vs k×spacing, and add two-fleet, warm and retro tests to `b-coorbital-cert.md`.

## Reproduction

Clean tree, `git apply work/patch.diff`, built and reran all three scenes:

- ctrl: enc 2093, pairs 44850, steps 15,948,922 — identical to the author's artifact and to `artifacts/evidence/opus-encounters-20260930/verify.jsonl` (`truth_enc: 2093`, `truth_steps: 15948922`). Body and encounter lines byte-identical to the author's `ctrl.jsonl` (only `wall_s` differs).
- fleet2: enc 4623, pairs 171049; retro: enc 71923, pairs 169431 — byte-identical body/encounter lines to the author's stored outputs.
- `analyze.py` reproduces every table number: fleet2 cross 43.7%, per-group ceiling 56.28% (saturates at the intra fraction), merged 15.64% @W=1 (26 certs/enc), 99.00% @W=0.05 (519.1 certs/enc); retro 96.4% cross, ceiling 3.60%, merged 1.28% @W=1 (1.7), 7.51% @W=0.05 (33.4); quadratic tier 37.0 and 2.4 pairs/enc; 15.5× = retro/fleet2 count. VOID conditions clear (ctrl rank@event 100%, dup 0 everywhere; max 99 events/pair over 50 orbits).

The author's `sample` matches `belt::make_belt`'s RNG draw order exactly (a, u→Rayleigh-e, pom, lam), so CTRL is a genuine re-instantiation of the crate's coorbital belt, not a look-alike.

## Instrument (independent check of the one non-crate path)

RETRO uses a mirrored copy of `truth_pair`. I ported `Body::state` from `kepler.rs` to Python independently and checked:

- 40 random reported retro events: analytic mirrored distance at the reported t is < ρ and equals the reported d to 1e-9.
- Brute-force fine-grid scans (dt = 1e-4, control at 2.5e-5) of d(t) over all 50 orbits on the busiest intra-A, intra-B and cross-sense pairs: the scan finds exactly the reported minima — no false positives, no misses. The conservative-advancement bounds depend only on rmin and reflection-invariant dot products, so the march is rigorous for counter-orbiting pairs.

## Predictions

`predictions.md` predates the outputs (folder mtimes: predictions 20 m, jsonl 16 m) and the fixed kill criterion (≤200 certs/enc → <99% coverage) is in it. Held: ctrl band (1500–3000; exactly 2093), 100% rank@event; fleet2 count band; merged W=1 ≤10% (15.6%, direction held); 99%-needs-W≤0.05; kill verdict; retro predictions (ceiling, ≤5% merged @W=1 → 1.28%). One miss, disclosed as a miss: predicted ≥95% cross-fleet, measured 43.7% — the intra e-crossing layer outnumbered the author's drift estimate. That is a pre-registration failure handled per the house rule (a failed expectation diagnosed, not hidden), and it produced finding 2.

## Adversarial cases (mine)

1. **warm1** — one fleet, n = 600, σ_e = 0.04, no grouping confound: 22.1% at W = 1, 99.6% only at W = 0.05 (407 certs/enc). Layer 2 stands alone; the quadratic tier is 30.5 pairs/enc with zero misses.
2. **cool1** — σ_e = 0.012 (oscillation ≈ 4.6 spacings): 42.3% at W = 1. The mechanism is the dimensionless ratio, as claimed.
3. **big1** — cold denser fleet, n = 1500, σ_e = 3e-4 (0.29 spacings): 99.51% at W = 1, 6.1 certs/enc. Control on the other side: the certificate's cold-formation domain genuinely works; this is a scoping kill, not a hit piece.
4. **fleet2b** — different seed: cross 44.3%, ceiling 55.7%, 99.1% at 525 certs/enc. Seed-stable.
5. Maintenance model: an incrementally-maintained order (swaps, not window rebuilds) gives rank@event coverage at ~2k certs per swap; warm fleets swap ~7.6 times per body per orbit → ~4×10² certs/enc — same cost class as the windowed 519. The kill is robust to how re-ranking is implemented.

## Novelty

No HISTORY entry or doc attacks the certificate's domain; the gold is 6 October (board only), the build `b-coorbital-cert` is still queued on both lanes (HANDOFF "In flight"), so no prior test covers multi-population, warm or retrograde concentration. The inversion lands before the component is built.

## Goal fit

HANDOFF's first risk ("candidate work at scale: co-orbital concentration (fleets)"). It shows a premise of an adoption is wrong — a gold criterion — and the fix is adoptable within one step (a spec edit, negative cost). PRINCIPLES: "a failed expectation is not automatically a failed method" (H0183) — the dossier kills the configuration "phase rank replaces the pairwise tier under concentration", keeps phase rank for cold single populations, and my big1 control confirms that residue.

## Caveats (why not a clean sweep)

- The headline "fails its own contract on the scene it was adopted for" slightly overreaches: the gold's adopted scene is one cold formation, where the certificate works (ctrl: 100% at 2.9 certs/enc, reproduced). What is killed is the board's adoption gloss — "replaces the quadratic tier… for concentrated workloads" — for warm, multi-population and retrograde concentration. The dossier's own fit section states this correctly.
- The spec says "beside the existing tiers", so cross-group zero-miss was never the certificate's alone to carry; the kill there is economic (battles restore the 10¹²-pair window tier the gold condemned), which the dossier argues but does not and cannot measure at 10⁶.
- The 10⁶ rank-break at the gold's σ_e (e must be < ~spacing = 6.3e-6) is arithmetic plus the mechanism measured at n = 600; a direct probe needs n > 2×10⁴ and was not run.
- "Any period-concentration trigger that fires there fires per fleet" assumes a dimensionless trigger; a width threshold tuned to exactly the gold's 1e-4 would not fire on 2e-4-wide fleets — narrowing the fleets preserves the finding.

## What the author missed

- 3D mutual inclination (self-disclosed): crossing planes should behave like the crossing e-ellipses, likely worse; the crate is planar.
- Single seed per scene (self-disclosed); I varied seeds — stable.
- The incremental-maintenance reading of "windows" (checked here; conclusion unchanged).
- The exact wording gap between the board's "replaces the quadratic tier" and the spec's "beside the existing tiers" — the dossier flags it only in "what would make it wrong"; the economic dilemma is the load-bearing argument and holds either way.
