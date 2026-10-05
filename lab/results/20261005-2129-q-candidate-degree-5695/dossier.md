# Dossier — q-candidate-degree (run 20261005-2129)

## Claim

A two-tier certificate — the Binet-cone test lifted to envelopes of (U,V,W) points, plus an analytic
integer "arming" test per candidate pair (linear windows + exact first-hit, no state evaluations) —
finds **every** encounter from N = 10³ to 10⁶ with **zero misses** (against the rigorous truth and
against the crate's full-candidate machinery), keeps armed pairs at **4–5× the real encounters** in
every scenario, makes a kick cost O(log N) envelope work plus the armed set, and **measures the
board's gold criterion into two halves**: at a fixed belt distribution, candidate work per body
stays **proportional to the real encounter rate** (≈200 arm tests and ≈5 armed pairs per
encounter, constant over three decades of densification), while the strict C·log N form is
**unreachable for exact discovery** — under dilution (ρ∝1/N, encounters per body flat) the arming
touch per body grows ∝ N (26 → 19,603 tests per fire from 10³ to 10⁶), because the firing set is
pseudo-random among crossing pairs.

## Bottleneck

Board's top scaling risk: "candidate pairs per body grow with N at a fixed distribution (O(N²)
pairs); candidate work must track real encounters". This run shows the *touch* per crossing pair is
irreducible for exactness (one O(1) integer test per pair per horizon — an information-theoretic
floor, not an algorithmic one), and that this floor is **harmless at fixed distribution** (constant
tests per encounter) and **fatal only under dilution**. The measured remaining cost is elsewhere:
**the tangency ("Wide") sections' numeric windows**, 0.67–0.7% of sections but 91% of all state
evaluations at 10⁶ (30.8M of 33.9M evals): armed-but-not-firing tangency pairs pay ~1,200 evals each
once per horizon. Expected gain from the next run: ≥ 10× on total encounter cost by replacing the
numeric window with a tangency-native certificate; the tier structure itself (this run) buys the
zero-miss skeleton, the O(log N) kick path, and the correct invariant to optimize.

## Evidence

All commands run in `lab/results/20261005-2129-q-candidate-degree-5695/enc` (a copy of
`crates/encounters` plus `src/tier.rs`; `cargo build --release`; binary at
`/home/glmlab/lab-target-0/release/encounters`). JSON lines saved: `scale-decisive.jsonl`,
`tree.jsonl`, `kick.jsonl`, `verify-heldout.jsonl`. Timings are Linux/x86 single-thread — orders of
magnitude only.

- `encounters tier-verify` (6 s): N=600 belt, 100-orbit horizon, vs the crate's rigorous
  conservative-advancement truth: **79/79 events, misses 0, extra 0**; armed 349 of 14,921
  candidate tests.
- `encounters tier-scale fixed` (35 s): ρ=1e-4 fixed, N = 10³→10⁶ (the belt densifies). Misses 0 at
  every N. Fires per body per horizon: 0.16 → 2.3 → 20.5 → 208 (×10 per decade, as density).
  **Arm tests per fire: 285 → 193 → 220 → 223 — constant.** Armed/fires: 5.5 → 4.2 → 4.7 → 4.8 —
  constant. Total tiered work per fire ~constant (1.3–1.9 ms; the printed `*_us_per_fire` fields
  are per-body-µs over all-sample fires — multiply by the sample count), base ~1.6–2.3 ms/fire:
  **work per body is proportional to the real encounter rate** for both, with the tier 1.3× ahead
  and the armed set (not the candidate set) defining the exact work.
- `encounters tier-scale dilute` (35 s): ρ = 1e-4·10⁴/N (r8's convention; encounters per body flat
  ~2.3/horizon). Candidates per body 48 → 450 → 4,462 → 46,067 (∝N, set by the eccentricity spread,
  not ρ). **Arm tests per fire: 26.5 → 193 → 2,238 → 19,603 (∝N): the strict C·log N gold fails,
  and must fail** — see "What would make it wrong". Misses 0 at every N. Arm cost 1.4–1.9 µs/test
  (`armbench`: arm_sections 0.93 µs, first_hit ≈ 0.5 µs, u64 Euclid recursion).
- `encounters tier-heldout` (15 s): fleet crossing a belt (200 e≈0.3 bodies through a cold belt),
  narrow belt (a∈[1,1.05]), 3× densified belt: **misses 0, extra 0 in all three**; armed/fires
  3.95–4.79; armtests/fire 151–219.
- `encounters tier-kick 10000; … 100000` (24 s): player burn at eps ∈ {1e-7, 1e-5, 1e-3}, 30 kicks.
  Base re-setup: 8.0 ms → 81.9 ms per kick (∝N, taleb's O(N) re-setup reproduced). Tiered: envelope
  path refresh **9.7 → 13.0 recomputes (O(log N))**, slack (first-hit time beyond horizon) skips
  98% of pairs, exact re-runs only on the armed set (~190 pairs at 10⁵): 1.3× faster at tidal eps
  (the armed Wide pairs dominate), **5.6–5.9× at a real burn** (1.4 ms vs 8.1 ms; 13.4 vs 79 ms).
  The slack rule at factor 1.5 is **not sound**: 0.4–0.5% of skipped pairs changed their hit set at
  eps ≥ 1e-5 (validated exactly) — a sound version needs a drift bound, not a factor.
- `encounters tier-tree` (7 s): the envelope cone between groups **degenerates to the U-sweep in
  belts** — node tests per body 2.9 → 26.9 → 267.4 (∝N), prune fraction 2–3%; the fleet prunes no
  better (its orbits genuinely cross the belt: spacelike everywhere). The tree's value is the kick
  path and holding envelopes, not belt discovery.

## Predictions

`predictions.md` was written before the 10⁵/10⁶ scaling, kick and tree runs. Held: misses 0
everywhere (1); candidate degree ∝N in both series (2); fires flat under dilution, ∝N at fixed ρ
(3); armed/fires ∈ [3,6] at every scale (4); the dilute/fixed asymmetry, including arm tests per
fire ∝N under dilution and constant at fixed ρ (5); kick path O(log N) (7, partial). Failed: the
slack rule with zero violations (7: 0.4–0.5% violations at eps ≥ 1e-5 — reported as unsound); the
tree predictions (8: node tests per body grow ∝N, not log N, and the fleet prunes ~3%, not >80%) —
both failures are informative and now part of the claim.

## What would make it wrong

- The arming windows are analytic supersets validated by zero-miss diffs against the base machinery
  and the truth (10⁶-scale, two ρ conventions, three held-outs). A single missed event would break
  the claim; the fast linear window on tangency arcs (guard: decisively narrower than the cap) is
  the least-rigorous piece — one adversarial high-e case away from being unsound, and the fleet
  held-out is the case that would show it.
- The C·log N impossibility argument: firing within the horizon depends on the pair's phase offset
  c = (t_i − t_j) mod T through an integer rotation; as the partner's phase varies, c sweeps [0, T)
  uniformly, so the firing set is a pseudo-random subset of the candidates (measure ≈ 2wL/T). No
  sound group certificate can separate it without reading each pair's phases — the same structure
  that makes the *armed* set 4–5× fires but the *touched* set equal to the candidates. This is an
  argument plus a measurement, not a proof; a representation that makes the firing set locally
  structured (e.g. resonance-keyed belts, `keys > 1` in the belt generator, where rotations are
  exactly periodic) would break it — untested here.
- Cost of adoption: `tier.rs` (~510 lines) on a copy of the crate; the sweep gains a per-horizon
  arming pass (1.5 µs/test, engineering headroom to ~0.5 µs), a u64 Diophantine path, and the tree
  for kicks. The slack rule must not ship as-is (violations); a kick must either re-arm all
  candidates of the kicked body (still ~10× cheaper than base re-setup per test) or carry a sound
  drift certificate.

## Fit with PRINCIPLES

- "candidate work must track real encounters within the horizon… plus a small constant per body"
  (board): at fixed distribution the touch *is* a constant per encounter (≈200 tests); under
  dilution no exact method can do better — the target itself splits in two, and the fixed-
  distribution clause is the physical one (a real belt has fixed body size).
- "You cannot average a population" (Julien): every body stays exact and individual; the hierarchy
  only skips work that provably cannot fire, and every reported event comes from the crate's exact
  per-pair check.
- "Compute only surprises" / "we only care about changes": the arming pass runs once per horizon,
  not per orbit; kicks walk one tree path.
- "A failed experiment kills that configuration, never the method": the envelope cone as a belt
  discovery mechanism is killed (it degenerates to the sweep); it survives as the kick structure.

## The lens

This lens (candidate pairs must track encounters, not N) pushed toward group certificates; the run
shows that in a phase-mixed belt the *geometry* tiers (envelopes, cones) buy nothing for discovery —
the win lives in the *time* tier (integer arming) and in what the measurement exposed: the tangency
windows, not the candidate count, now hold >90% of the cost. What the lens may have missed: the
3D/inclination structure (the crate is 2D; the cone test changes with nodes), resonance-keyed
populations where rotations are exactly periodic (the impossibility argument may not hold), and the
compiler angle — the armed set (4–5× fires) is small enough to *store* per body, which turns the
encounter schedule into data the allocator can lay out in causal order rather than a scan.
