# Dossier — 20261016-1459-spacex-7fd2 (SpaceX lens)

**Claim.** The kick's recompile is information-forced at its own resolution: one kick
moves the compiled key's own integer inputs by ~2⁻²⁶ relative (median; 15–23 low bits of
the shape mantissa's 48-bit field, up to 31), so **no bit-identical reuse exists at any
granularity between the law's refused 12+12-bit memo (~96–100% reuse, re-rounds the
orbit) and the exact key (0% reuse) — the same-bin rate decays with no plateau
(≈1.0 @ ≤16 bits, 0.93–0.98 @ 20, 0.49–0.84 @ 24, 0.06–0.26 @ 28, ≤0.02 @ 32) — which
closes the memo/cache family for the kick and moves the lever to cheaper exact
arithmetic, not reuse**; and the leaver kick's 5× cost is its knots (37–195 vs 6), not
key displacement (leavers move their key *less* than made bodies).

**Bottleneck.** The board's `kick: 75-160 µs against a ~50 ns floor` (~10³·³); the
record's repeated dead ends on kick reuse (exact memo 0% at 0/203,017 and 0/3,225;
quantized memo refused as re-rounding). This run removes the whole reuse family in one
measurement instead of one candidate at a time, and names where the remaining 10³
actually lives for the expensive half of the population (shape size, not novelty).

**Evidence** (all from `xtask universe --kick-bench`, shipped resolver, patch
print-only and digest-neutral — replay_digest and digest-at-cut bit-identical to the
pristine build at seed 3: `0e52330e…`, `972cde44…`; refused 0 everywhere; medians
reproduce the record: made 35.2 µs, leavers 152–177 µs):

- Author arm seed 3; held-out seeds 7 and 11 (not tuned on). Kick µs medians:
  made 35.1–35.3 µs (365 samples/arm), leavers 152–177 µs (666–1,132 samples/arm).
- Consecutive kicks of one body (986–1,496 pairs/arm, exact integer arithmetic):
  **zero** exact repeats of p or k in any pair, any seed (control: matches the bench's
  `exact_hit_rate` 0.0 and `exact_shapes == cycle_rebinds`).
- Displacement per kick: p moves median 2⁻²⁵·⁵…2⁻²⁷·⁶ relative (p10 2⁻²⁸·⁵…2⁻³²·⁰);
  the shape mantissa k moves median 2⁻²⁵·⁹…2⁻³²·⁵, with **15–23 low bits (median) of its
  48-bit field changing per kick, max 30–31** — every kick injects ~2⁴·⁶⁺ bits of fresh
  information into the exact inputs the compile consumes.
- Reuse curve (both p and k in the same g-bit bin): made 1.000/1.000/0.988–0.997/
  0.927–0.950/0.49–0.55/0.06–0.08/≤0.006 at g = 8/12/16/20/24/28/32; leavers slightly
  higher (0.80–0.84 @ 24). Control at g = 12: curve 0.998–1.0 vs the bench's measured
  global `quantized_hit_rate` 0.955–0.969 (bin sharing across bodies, consistent).
- Knots per compile: made bodies 6 (median = max); leavers 37–195. Leavers' keys move
  *less* (p: 2⁻²⁶·⁴…2⁻²⁷·⁶ vs made 2⁻²⁵·⁵…2⁻²⁶·⁶) while their kicks cost ~5×.
- Code structure (read, not measured): the production path
  `Rebinding::from_state → fit_key → Orbit::compile` (crates/space/src/binding.rs:419,
  orbit.rs:551) keys its expensive layer (OrbitShape: knots, crossings, clock factors)
  on exact Scalar mantissas — p's significand and the Q48 k; compactness collapses only
  below q = 2⁻¹⁸ (WEAK_EXPONENT). There is no integer seam (like darwin16's root triple
  in lib.rs, the galaxy debug view) at which the shape layer repeats sub-exactly.

**Commands** (each ≤ 60 s after a one-off ~50 s build; full regen ≤ 5 min):
```
cargo build --release -p xtask
ES_KICK_DUMP=kicks-s3.json cargo run --release -p xtask -- universe --kick-bench --seed 3 --rtf 100 --seconds 30
# seeds 7 and 11 likewise; then:
python3 lab/results/20261016-1459-spacex-7fd2/analyze.py kicks-s3.json kicks-s7.json kicks-s11.json
```
`regen.sh` reproduces every number (patch, build, three arms, pristine control, analysis).

**Predictions.** `predictions.md`: the original memo design died by code reading before
any measurement (pivot recorded); re-registered A–E for the census all held, including
held-out seeds 7/11; the one tail claim (displacement ≤ 2²⁰) fails at the max (31 bits).

**What would make it wrong.** The reuse curve is measured on one scene family (the
plane's own: 365 made bodies + fleet hand-outs) at rtf 100 for 30 s; a scene with
kicks that move keys by *whole* quanta at coarser granularity (deliberate burns at
high γ, resonance pumps) could shift the curve's middle (g = 20–28) — but not its
ends: 0% at exact is structural (fit_key derives the key from the exact integer state),
and the decay-with-no-plateau shape follows from the displacement being one smooth
random variable. The knots-not-displacement attribution for leavers is by population
median comparison, not a per-kick regression; a per-kick join (µs vs knots) would
tighten it.

**Cost of adopting / fit with PRINCIPLES.** Nothing to adopt (a deletion of a research
direction, priced); zero code change shipped — the patch is print-only in the bench
harness, digest-neutral by measurement. Principle 3 ("compute only surprises"): the
census shows the kick's recompute *is* the surprise — ~2¹⁵⁻²³ fresh bits per kick —
so the compiler's cost is honest work at this representation, and the remaining 10³
to the floor must come from representation (fewer/narrower knots, per-regime shapes —
leavers' 37–195 knots are the visible fat), not from caches. Principle 9: this kills
the memo configuration, not the method.

**The lens (SpaceX) and what it may have missed.** The lens pushed
delete-before-measure; the honest outcome is that the cheapest falsifying test here
*killed the lens's own first instinct* (the reuse cache). What it may have missed: a
warm-start arithmetic lever (recompute the same exact outputs faster from the previous
key — bracket-doubling on moved bits) is *not* closed by this census; it is reuse of
work, not of results, and stays legal because outputs stay bit-identical. The census's
15–23 moved bits price its ceiling: root-finding over a moved window costs ~2·log₂(2³¹)
≈ 62 f-evals — no better than today's two full bisections; but the *knots* could be
warm-integrated (each panel's endpoints move by ~2⁻²⁶) only if panel sums were
somehow incremental, which exactness forbids. The real survivor of this run is the
knots column: 6 knots for made bodies against 37–195 for leavers is a 6–32× spread in
arithmetic per kick that no prior attribution (bind 41–65%, search 45%) separated by
shape size.
