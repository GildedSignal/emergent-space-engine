# Dossier — 20261015-1615-spacex-1343 (spacex lens)

## Claim

The passage/plunge tail (this page's open direction 4) is measured and half-closed: a compiled
`Passage` stands at `knots(compactness) + 96 B × panels`, panels growing **10.74 per octave** of
window exponent `w = log2(outer/periapsis)` beyond the join at 2^10 — 18.8 kB per comet at the
plane's own maximum window (w=14, measured in flight) against a belt body's 670 B — and the
never-demote rule is **unnecessary for passages**: `Passage::compile(key, outer_radius)` is pure
in its two arguments, so re-mint is bit-identical (0/64 differing readouts at every w from 9 to
61), and demotion extends to passages with a ~120 B record (key + edge + sense/unit). Plunges
keep the rule: they have no key.

## Bottleneck

Bodies in the flyable engine (the board's first live question): memory per live body. The seam's
standing store was priced at 962 B/body on the belt; a far-falling population pays 20× that per
body, forever, for arcs that are provably regenerable — pure P6 waste ("store the generator,
not the generated"). This also corrects the shipped accounting: `body.rs:193` hardcodes
`Passage(_) => 4096` — 2.3× over the player's actual mint (1.8 kB at w=2) and 4.6× under the
comet worst case (18.8 kB at w=14).

## Evidence

All from `regen.sh` (build + `passage_tail` bench + 5 flights; `bench.txt`, `flights.txt`;
Linux x86 cloud box, 8 vCPU shared — orders of magnitude only, per the lab rules).

**The bench (the law's own bind path, `Rebinding::from_state`, one probe state, e≈1.5,
peri ≈ 9.97e5):**

| w | panels | knots | standing B | compile µs | re-mint diffs |
|---|---|---|---|---|---|
| 0 | refused `Topology` (negative control) | | | | |
| 9 | 0 | 145 | 13,904 | 327 | 0/64 |
| 10 | 0 | 161 | 15,440 | 354 | 0/64 |
| 11 | 12 | 161 | 16,592 | 378 | 0/64 |
| 16 | 66 | 161 | 21,776 | 505 | 0/64 |
| 26 | 173 | 161 | 32,048 | 767 | 0/64 |
| 41 | 334 | 161 | 47,504 | 1,183 | 0/64 |
| 61 | 549 | 161 | 68,144 | 1,633 | 0/64 |

- Slope: (68,144−16,592)/(549−12) = **96.0 B/panel**; 537 panels / 50 octaves = **10.74/octave**
  (P1 held, with the join's exact behaviour: knots carry the window to 2^10, panels beyond).
- Re-mint: keys equal and all 64 `at_radius` readouts (time + full `OrbitState`) bit-identical
  between the two compiles at **every** w. Cycle control: `Orbit::compile(key)` re-mint 0/16
  everywhere (reproduces 760f's flight-level result at the bench).
- Cycle knots vs apoapsis span: 6 / 10 / 19 / 37 / 58 knots at spans 2^1–2^4 (536→5,552 B) —
  the belt's 43 knots sits on this curve; **cycles grow with span too**, ~13 knots/octave here.
- Compile cost grows with the window: ~+26 µs/octave — a passage promotion is 70–350× a cycle's
  4.6 µs (760f), the one real cost of demoting passages.

**The flights (shipped plane, patched accounting only):**

- 10³ and 10⁴ coast: **0 passages**; standing cycles 632/668 B/body (cross-checks 760f's census).
- 10⁴ burn: **exactly 1 passage** (the player's escape from Home), w=2, 0 panels, 1,808 B —
  e0f9's "1 passage here" reproduced with its window and price.
- **comet12** (2,000 comets unbound about the star, born at r0=1.04e12 < 2^40 root units,
  peri≈1.2 AU): all 2,000 alive as passages at **w=14, 35 panels, 18,800 B each** (census
  37.6 MB standing arcs); rss 60→383 MB over 20 s. The churn beyond the arcs (kicks
  3.06e-3/body/game-s = 16× the belt's coast rate; p50 frame 11.3 ms) is the known seam plus
  one structural fact: unbounded bodies are *always* scan candidates (`radial.rs:16`).
- **comet13** (r0=2.08e12 > 2^40): **990/2,000 LOST at the loss radius** — the root doll's
  2^40 cap (binding.rs:400) measured in flight — survivors hold w=15, 46-panel, 19,856 B
  passages. **The plane's passage windows are structurally capped at w≈15** (root loss radius;
  planet dolls at 2×SOI give w ≲ 9–10 with surface-bounded periapses).
- The minted window exceeded the requested one (12→14, 13→15): the birth bind's unit/edge
  rounding widens it — windows are engine-chosen, which is why the placeholder constant cannot
  be right by construction.

## Predictions

`predictions.md` was written before any run. P1 held (10.74/octave, join at 2^10); P3 held
(0 diffs everywhere — the certificate); P4 held (0/1 passages, windows ≤ 2² — the cap is even
tighter than predicted); P6 held (code: `Trajectory::key()` is `None` for Plunge only).
**P2 failed as written** ("the 4096 constant over-prices ~6×"): it *under*-prices 4.6× at the
plane's real maximum — I had not derived the join saturation (161 knots ≈ 15.4 kB) from the
code before predicting. **P5 failed as written** (2^16 window, 3–7 kB): the root loss radius
2^40 caps windows at ~2^15 and the knots term dominates — the honest worst case is 18.8 kB at
w=14 (the bench extends to 68 kB at w=61, outside any doll's reach today).

## What would make it wrong

The identity certificate is sampled, not exhaustive: one compactness class in the bench, the
comets' in flight, 64/16 readouts each. Purity is code-visible (`compile` reads only `key` and
`outer_radius`, orbit.rs:1020–1078, no global state), but a demote-passages build on the seam
must re-prove digest identity across scenes (not done here). The promotion cost of a demoted
passage (0.3–1.6 ms at high w) could bite a kick-heavy unbound population: retention's working
set gains a third regime (planet-cap w≲10, root-cap w≤15, and the dearer re-mints). Linux
timing: orders of magnitude only.

## Cost of adopting

Two lines of decision for the seam's owner: add `Passage` to the demote set with the record
carrying `outer_radius` (~16 B) beside the key, and replace `body.rs:193`'s 4096 with the
measured formula (knots + crossings + 96·panels — the accessor ships in this patch). No law
arithmetic changes; the patch here is accounting, scenario plumbing (comets born before
`start()`, `plane_comets`), and a Linux footprint shim in the example.

## Fit with PRINCIPLES

- P6 "Store the generator, not the generated": the compiled arc is exactly regenerable from
  120 B — standing tails are the anti-pattern named.
- P1/17 "the best part is no part": 18.8 kB/body deleted by a proven re-mint, no new mechanism.
- P10 "map how things break, think in extremes": the comet stream is the falsifying edge; the
  loss radius is where the plane itself says the representation ends.

## The lens

SpaceX's delete-first framed this as "price the part, prove it deletable" — and it skipped a
build: the demote-passages variant of the seam was not flown (60-minute window; the seam is a
one-way door worth its own run). The idiot-index reading (18.8 kB standing / 120 B record =
157× waste) is the adopting argument; the blind spot is that deletion here moves cost into
re-mints whose tail (1.6 ms at w=61) only matters outside today's dolls.
