# Dossier — gravity at c kept by a cursor: exact, ~1 test/kick, and the ghost cost stated per scale

Run 20261005-1540-q-gravity-cursor-05b0. Probe: `cursor.rs` (self-contained,
`rustc -O cursor.rs -o cursor`, no deps); all outputs in `out-all.txt`, numbers in
`results.json`. Cloud Linux/x86: orders of magnitude only. Predictions in
`predictions.md` (written before every decisive run).

## Claim

The cursor of memo R5 — one integer index per (body, source) pair, advanced by
squared-form tests `t ≥ t_k and (t−t_k)² ≥ |x−x_k|²` — selects **exactly** the
brute-force retarded prefix on 7,203,000 kicks over random integer worldlines
(β_consumer and β_source to 0.9, head-on closing, photon consumers moving at c,
dense news, exact lightlike ties): **0 mismatches, 0 times ahead of the cone**;
it costs **1 + arrivals-since-last-kick** integer tests per kick, independent of
history length K (brute force pays K), with the exact identity
`total tests ≤ total kicks + total events` holding in every configuration; the
Laplace control holds through it (naive retardation spirals the binary out, news
stays bound, cursor and brute-force selection give **bit-identical trajectories**);
and one premise of the memo is falsified in a useful way: **a frozen single-version
ghost is structurally unstable** (mutual L3: explodes within 3–7 orbits at any
cadence), so the news chain must include the source's per-rebinding versions —
ghost depth = cadence × light-orbits (≈1 version in a star system at real c;
~10–15 in lowered-c β = 0.9 scenes; galaxy ghosts must ride generators).

## Bottleneck

Board item 0 / law.md "Gravity travels at c" (Julien, 5 October: "gravity must
travel at c we can't get lazy here"). The a237 run (`claude/lab-20261005-1404-q-
gravity-at-c-a237`, silver) measured the news *physics*; this run measures its
*mechanism*: the per-pair cursor that makes gravity-at-c cost about one
comparison per source per kick instead of a retarded search per kick. Gain: the
causal contract of law.md becomes adoptable at ~0 cost above the force itself —
it deletes the search, not a component. With R4 it is what makes the event trace
wide (light-cone independence).

## Evidence (each command ≤ 60 s)

**E1 exactness — `./cursor exact` (8 s).** 7 random-worldline configurations
(300 pairs × 3000 kicks each) + a photon consumer (exactly lightlike integer
steps — the view/gather path) + a head-on 0.9c pair + 1999 exact lightlike ties:
**0 mismatches vs brute force, 0 cursor-ahead**. Ties: `(t−t_k)² = |x−x_k|²`
counts as arrived (`≥`), one quantum farther does not — the boundary is exact
because both sides are integers. Precondition measured as held: consumer steps
obey `Δx² ≤ Δt²` in integers, so k\* never moves backward (cone inclusion).

**E2 cost — `./cursor cost` (15 s).** K-sweep at matched rates: tests/kick
1.964 → 1.991 → 1.997 as K grows 600 → 60,000 (**flat while K ×100**; brute
pays 600 → 60,000). News-rate sweep at fixed kick cadence: tests/kick = 1 +
adv/kick to within 0.03–0.4 at every rate (0.099→1.099 … 99.37→100.37): the
cursor's cost is the *arrival rate*, nothing else. Even at news 100× denser
than kicks (K = 400,000) it is 100 tests vs 400,000 — 4000× under brute.
Identity `tests ≤ kicks + events` holds everywhere (each test is one advance or
one kick's single failing test — the information-theoretic floor: every news
event is delivered exactly once per consumer).

**E2b burst — `./cursor burst` (instant).** A 1000-event thrust phase: one kick
pays 1000 tests (max), the mean over the run is 20.3, identity holds
(1034 ≤ 51 + 1000). A burst is paid once, not rescanned — the allocator can
spread it on slack, and law.md's tie rule ("a key held is one decision") already
collapses held thrust into one news event.

**E3 Laplace control — `./cursor laplace` (4 s).** Equal-mass binary, versions
recorded at consistent (x, v) boundaries every step, c lowered so v_orb/c = β
(β is per-body; relative v/c = 2β), 400 steps/orbit, 60 orbits:

| law | β=0.1 | β=0.3 | β=0.9 |
|---|---|---|---|
| inst | dE 2.4e-13 | dE 2.4e-13 | dE 2.4e-13 |
| naive retarded | a ×12.4, dE 0.93, not yet unbound at 60 | **unbound 0.3 orbit**, e→1.2 | **unbound 0.2 orbit**, e→41 |
| news via cursor | bound, dE 3.1e-3, a +0.31% | bound, dE 8.1e-3, a +0.82% | bound, dE 1.7e-2, a +1.7% |
| news, frozen 1 version | **unbound 5.1 orbits, dE 310** | same | same |

- Cursor-driven and brute-force-selection news runs: **0/1200 selection
  mismatches at every β, final states bit-identical** — the cursor is an index,
  not a law change.
- Version lag: 13.0 / 37.0 / 89.4 versions vs theory 2β/dt = 12.7 / 38.2 / 114.6
  (β=0.9 runs low: orbital curvature shortens the effective light path).
- **The falsified premise:** "between news events, the field is the source's
  present free-fall path" is right, but that path must be re-anchored at every
  rebinding. A single frozen version makes each body move in the other's
  *external* frozen field — mutual L3 saddle — and explodes from machine-noise
  seeds: unbound at 3.2 / 5.1 / 6.1 / 7.2 orbits for 100 / 400 / 1600 / 6400
  steps per orbit (onset only log-delayed by refinement: structural, not
  truncation). Same class as a237's checker attack on strongly-perturbed tubes.

**E4 ghosts — `./cursor ghost` (instant).** Retention (influence radius / c):
Earth doll 5 s, Jupiter doll 175 s, Sun doll 6.9 h, an individual star 3.3 yr,
galaxy cells 3,260–26,080 yr. Per source: 24 B × depth of (t, x, y) cone-test
entries + one shared 16 B tube + 4 B per (body, source) cursor. **Depth =
ceil(cadence × light-time-in-orbits)** (E3's lag ÷ versions-per-orbit): at real
c in a star system the ring is 1–2 versions deep (6.9 h vs months between
rebinds) → ~40 B/source; in lowered-c β = 0.9 gameplay scenes ~10–15 versions
(~400 B); at galaxy scale alive ghosts per cell ≈ news rate × retention =
(1/5·10⁸ yr) × (3·10³…2.6·10⁴ yr) ≈ 10⁻⁵…10⁻⁴ — sparse. **What the galaxy case
requires:** the ghost must be a *generator* — the cell's orbital program in the
smooth galactic field, advanced by addition, zero kicks; a stepped ghost would
buy a second body per news event for 10⁴–10⁵ years. Ghost fields enter as
aggregate multipole differences (old program − new program), shrinking to zero
as consumers' cones pass; ghost-of-ghost branches are second order in the news
size and pruned at retention.

## Predictions (`predictions.md`)

Written before all four decisive runs. **Held:** P1 fully (0/7.2M mismatches,
ties exact); P2 fully (cost = 1 + arrivals, flat in K, p99 ≤ 3 at λ ≤ 1, burst =
burst-size-once, identity exact); P3's structure (ret spirals out — unbound
0.3/0.2 orbits at β = 0.3/0.9 ≤ predicted 8; news bound at every β; cursor ≡
brute bit-identically; inst at floor); P4's lag law (13.0 vs 12.7, 37.0 vs 38.2).
**Missed, disclosed:** P3's numbers at the margins — ret at β = 0.1 not unbound
within 60 orbits (a ×12.4, self-quenching as ωa/c shrinks — later than a237's
12.1, whose β is relative-v-based and whose force convention differs); news
|dE| < 5e-3 held only at β = 0.1 (8.1e-3 and 1.7e-2 at 0.3/0.9, 60 orbits);
|Δa|/a < 1% missed at β = 0.9 (1.7%). **Falsified:** P4's "a pure binary
generates 0 news, one version suffices" — the ns0 run (E3): one frozen version
is L3-unstable; per-rebinding versions are load-bearing. That is the held-out
process doing its job.

## What would make it wrong

- Exactness relies on the precondition that consumer steps are causal *in
  integers* (Δx² ≤ Δt²). A representation that lets a body's stored step violate
  that (a Galilean handoff, an unguarded quantization) breaks cone inclusion and
  the cursor can legitimately disagree with brute force. The law's "nothing past
  c" already forbids it; E1 enforces it by construction.
- The one-test-per-kick figure is for sparse news (the engine's regime: free
  fall generates no news, a237's 1e-7 flyby twins). Dense-news consumers pay the
  arrival rate (E2's 100/kick row) — bounded by the identity, never by K.
- E3 is a float behaviour probe of the selection mechanism on the plane's
  representation (velocity-Verlet, every-step versions), not the integer law;
  the integer selection itself is E1. a237's open e-ladder (0.6→0.9) bounds the
  *news physics*, not the cursor, and stays open.
- Cost to adopt: 4 B per (body, source) pair of doll-local cursors + the version
  ring (depth above); both fit the plane's doll layout; no existing gate
  touches it. The cursor compares i128 products of i64 coordinates (exact,
  no roots), i.e. integer tests of the law's own kind.

## PRINCIPLES fit

- #23 "Nothing past c… it allows to cheaply partition compute": the cursor is
  that partition as data — one monotone index per pair, no scan.
- #3 "Compute only surprises": total work over a run = kicks + news events
  exactly; nothing is paid for the silence between them.
- #13 "Errors never compound": the selection is exact in integers, so no float
  retarded-solve drift can accumulate in *who* is felt (E1); the physics that
  remains is the news law's own, measured by a237.
- #6 "Store the generator, not the generated": the ghost is the source's tube
  (a generator); the falsified variant (freezing it forever) is exactly what
  breaks — generators must be re-anchored where the dynamics actually bind.

## The lens (what it may have made me miss)

The causality/cost lens made me measure selection and memory, not *observational*
consistency: the same cursor governs what the player sees (photons were tested
only as consumers of gravity, not as light gathered by the view). Untested: the
cursor inside a SyMBA changeover (sub-step kicks reading each other's versions
mid-hierarchy); cursors at a handoff (the index is doll-local — a re-anchored
body needs its pair cursors rebuilt, which costs O(pairs), not O(1)); and the
galaxy-scale ghost claim is analytic, not simulated — no generator-ghost run
exists yet. The ns0 instability also suggests checking the plane's *own* memo
idea (a memo hit = a version reuse): reuse across a light lag may hit the same
L3 mechanism.

## Reproduce

```
cd lab/results/20261005-1540-q-gravity-cursor-05b0 && rustc -O cursor.rs -o cursor
./cursor exact    # 7,203,000 kicks, 0 mismatches          (~8 s)
./cursor cost     # flat in K, = 1 + arrivals               (~15 s)
./cursor burst    # 1000-event burst paid once              (<1 s)
./cursor laplace  # ret spirals, news holds, bit-identical   (~4 s)
./cursor ghost    # retention and depth per scale           (<1 s)
```
