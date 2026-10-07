# Dossier — 20261007-0621-autoresearch-f521

## Claim

Caching the non-kicked body's arc states out of the window-advancement march (they do not
depend on the phase offset s) plus dropping the scan's unused relative-acceleration terms cuts
the encounters engine's setup cost 1.43x and a kick's re-certification 1.66–1.77x with
bit-identical certificates and zero missed encounters on every verify set.

## Bottleneck

Board focus "finding encounters without work per orbit or per element change": the gold
components-4643 finding says 92% of per-kick evals are window setup, so setup ns per candidate
pair (ns per event) is the steady-state price of every kick. Instrumentation (this run):
87% of setup evals sit in `d_of_s`'s fixed 33-sample arc scan, called from the conservative
s-advancement in `numeric_window` (66 716 calls for 1 547 Wide sections at n = 10 000).

## Evidence

All commands from the repo root, `cargo build --release -p emergent-encounters` first
(binary at `$CARGO_TARGET_DIR/release/encounters`); the machine was shared (load 7.6),
so A/B binaries were alternated under the same load and the min of 3 taken.

- Baseline vs candidate (this run's patch), `encounters scale n 10000`:
  setup 9 452 -> 6 636 ns/pair (1.43x); run(1000 orbits) 10 041 -> 7 392 ns/pair (1.36x);
  Kepler solves per pair 40.5 -> ~21; hits_per_pair_orbit and checks_per_hit unchanged
  (4.546e-5, 1.105). Raw JSON: `baseline-scale-n.jsonl` (unloaded baseline: 8 348 ns/pair).
- Held-out correctness, candidate binary, `encounters verify a|b|c|d|long` (10 belts,
  including narrow-adversarial, coorbital, equal-period-keys, hot e = 0.1, mixed a 0.5–3,
  1000-orbit long): **missed 0, false 0, method events == truth events exactly** in all ten.
- `encounters kick` (n = 10 000, horizon 1000 orbits): us_per_kick 13 770 -> 8 294 at
  eps = 1e-5 (1.66x), 14 699 -> 8 303 at 1e-3 (1.77x), unchanged at 1e-9;
  slack_skippable_fraction identical to baseline at every eps (0.9458 / 0.5746 / 0.0295 / 0.0025)
  — the slack-skin lever is untouched. Raw: `kick-base.jsonl`, `kick-cand.jsonl`.
- Reproduce the A/B: build baseline with `git show HEAD:crates/encounters/src/pairs.rs` over
  the working file, save the binary, restore the patch, rebuild, alternate `scale n 10000`.

Each command above ran in well under 60 s except `verify long` (46 s) and `scale n` (15–37 s).

## Predictions

`predictions.md` was written before the held-out run. Held: solves/pair <= 27 (got ~21),
missed = 0 everywhere, false = 0, slack_skippable unchanged, verify identical events.
Missed: setup_ns_per_pair <= 5 500 (got 6 636, 1.43x not 1.5x) — the closed-form section
work (travel/passage_tick/cross_window, 45% of setup at n = 10k) dilutes the window gain;
my point prediction treated setup as all-window.

## What would make it wrong

The caching is sound only because f(tau) evaluates j at `mj + n_j*tau` with no s term; any
future change that shifts j's arc with s breaks it (verify would show misses). The rel_rv cut
assumes the scan never reads the acceleration; refine still computes it (Newton on d(rv)/dt).
If a checker finds missed != 0 on any set, the patch is wrong, not the method.

## Cost of adoption, fit with PRINCIPLES

One function signature change (`d_of_s` takes the precomputed grid), one helper (`rel_rv`),
~20 lines in `crates/encounters/src/pairs.rs`; no representation change, no new state.
PRINCIPLES #1 "The cheapest compute is compute not done. Delete before optimizing" and #17
"the best part is no part": both changes are pure deletions of recomputed work; behaviours
(verify sets, certificates, slack budgets) are bit-identical. #11: measured before claiming,
A/B under equal load after the machine was found contaminated.

## Grade suggested: silver

Real, reproduced, adopted-ready, but 1.4x, not the 10x a gold needs. It is one named
experiment away from a bigger cut: the d-histogram (54% of advancement calls below 16 rho)
says the geometric tail of conservative advancement is the next lever — either the local
Lipschitz constant (i's speed over the anomaly range it actually traverses) or a per-pair
second-order window model for tangential pairs, as `cross_window` already does for
transversal ones.

## The lens (what it may have made me miss)

A local search on hot loops finds local optima. The structural change that would beat this
best configuration: store the arc grid (or the whole certificate) per pair so a kick re-pays
no setup at all — the slack skin the board already holds as the 12.6x lever; and the
closed-form 45% (true_to_mean/atan2 per section) yields to a trig-free Binet-domain
formulation. Both are outside this lens's one-metric loop.
