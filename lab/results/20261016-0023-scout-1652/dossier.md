# Dossier — 20261016-0023-scout-1652 (scout)

## Claim

The history stack's `len() > 1` floor pins one retired segment per kicked body forever, and
**98.3–98.4% of that standing stack is past the engine's own certified forget-window at steady
cuts** — but the deletion is **not free**: the page's view gather serves retired eras up to
**27,645 s old (≈ 0.98 of the belt's 28,141.5 s kick interval)**, far past every keep window, so
**retention's honest horizon today is the view's reconstruction walk, not the light cone**; the
lever (~10× standing cut on the record stack, the memory wall 398f measured at 1.0–1.3 TB for
10⁹) exists only behind the view's documented outcome-free fallback.

## Bottleneck

`memory at 10⁹` (board focus 4; the scoreboard's 10^2.6–2.9 gap): the causal history stack is
the newest exposed wall (20261015-2041-inversion-398f: 1.04 segments/body standing, 336 B a
`Segment` under ctl each pinning its compiled arc, 1.0–1.3 TB at 10⁹). This run prices the
floor itself against the engine's own forget-rule and finds where the rule stops being the
binding constraint.

## Evidence (all from `regen.sh`, one build + one 14 s flight)

Scene: the ladder belt (`scenario::plane_extra`, seed 1, 48 fleet, N = 10⁴ → 10,028 bodies),
coast at rtf 1500, past the first kick wave (13,051–14,534 game-s; interval 28,141.5 s), census
at four cuts (`census_n10k.log`; the instrument is the run's patch: `Universe::history_window`,
the retired-serve counters in `PlainBodies::binding_at`, and one cold view gather a cut):

| cut game-s | with_hist | in window | pinned past | age p50 | keep min/p50/max |
|---|---|---|---|---|---|
| 15,050 (just past the wave) | 1.003/body | **91.2%** | 8.8% | 1,727 s | 331 / 2,763 / 6,642 s |
| 20,050 | 1.003/body | 1.7% | **98.3%** | 6,721 s | 331 / 2,764 / 6,641 s |
| 32,050 | 1.004/body | 1.6% | **98.4%** | 18,721 s | 331 / 2,764 / 6,638 s |
| 48,050 | 1.004/body | 1.6% | **98.4%** | 6,564 s | 331 / 2,765 / 6,636 s |

Standing store 1,404–1,438 B/body whole (`bytes_of`; the 1.05 segments/body reproduces 398f's
census class for class). The view's cold gather at each cut: **retired serves 21,558 / 21,558 /
714 / 21,561**, deepest read into a served era 2,844.5 → **6,268.6 s**, and the **oldest segment
ever served grows monotonically 10,511 → 17,182 → 27,645 s** — past every keep window (max
6,642 s), to ≈ the full kick interval. Refusals: none surfaced (the fallback path exists in
`observe.rs`: "history pruned … the tube alone is read").

Mechanism, read off the shipped code: `Universe::prune` forgets at `keep = 2·light_distance +
2²⁶` ticks and certifies "changes no outcome" — but `PlainBodies::prune` holds
`while h.len() > 1`, keeping one segment forever. The belt's light window (keep p50 2,764 s) is
**9.8%** of the kick interval, so in steady state only ~10% of bodies (≈ 100% transiently for
one window after each unstaggered wave, then ~0% between waves — the cuts sampled the ~0% phase)
have a segment any light-cone-bounded reader can reach. The measured deep serves come from the
view's own path (`observe::partial`'s walk "back through the bindings until the whole step's
level (0) is met"): it reconstructs retarded reads from the last boundary and reads eras as old
as the interval regardless of the light distance (the served ticks are 24+ ks behind the body's
own d/c ≤ 3.3 ks). So the floor is **view-load-bearing, outcome-free**.

Composition to 10⁹ (published constants, not re-flown): 1.05 segs/body × 336 B = **353 GB
inline standing** (398f's 1.0–1.3 TB with the arcs pinned under ctl). Light-cone-windowed
retention: duty cycle keep/interval = **9.8% → ~35 GB** inline (~11 GB at the seam's 113-B
record), plus the unstaggered wave's one-window transient at 100% (f82a's genesis stagger
removes even that pulse). ~10× standing on the wall, behind one named view change.

## Predictions

`predictions.md` was written before the decisive run. **P1 held** (32k/48k in-window 1.6% ≪
15%; 20k 1.7% ≪ 3%; 15k 91.2% > 50%). **P2 held** (98.4% pinned ≥ 95%). **P3 FAILED as
registered** ("max depth below median keep"): the view served eras to 27,645 s ≫ keep p50
2,764 s and ≫ keep max 6,642 s — this failure is the run's finding, not an instrument error (the
serve counter survived three build iterations; the numbers are stable across repeated gathers at
a fixed cut: 15k repeats gave identical 2,844.5 / 10,511.3). **P4 held** (dead bodies hold
segments: 18–20 of 10,063; 336 B × 1.05 × 10⁹ = 353 GB ≈ 398f's inline share). **P5 partly
held** (the existing prune shortens the frequently-kicked locals: 105–133 bodies hold > 1
segment at every cut; the per-class split was not printed). Per the pre-registered kill
criterion, the deletion is reported as conditional (a lead-priced lever with a named blocker),
not as adoptable as-is.

## What would make it wrong

- The deep serves could be an artifact of the cold-cache gather (each cut gathers cold; a warm
  page may never walk that deep). Falsifier: instrument a warm gather loop; if max age-at-serve
  stays ≤ keep, the floor is dead weight and the ~10× cut is free.
- The `bytes_of` 1,404–1,438 B/body is the store's own accounting (inline history + record +
  plan + shape share), not the pinned-arc cost; the 10⁹ composition leans on 398f's measured
  standing widths for the arcs. Falsifier: re-fly with the seam patch and the census aboard.
- A burn flight (held scans clone bindings) may read deeper or wider than the coast gather
  measured here; the census is coast-only.
- The keep-window duty-cycle composition assumes the belt's interval stays the doll grid at
  10⁹ and the wave stays unstaggered; f82a's stagger changes the 100%-transient phase, not the
  ~9.8% steady duty cycle.

## Cost of adopting

Small: drop the `h.len() > 1` floor (one predicate) **plus** accept `observe::partial`'s
documented fallback ("the tube alone is read") for reads whose boundary chain is pruned — a
view-only fidelity change (the O(Δ²) partial correction), zero outcome change by the engine's
own digest invariant — or cap the walk at `keep`. The view change is the integrator's call; the
census instrument (`history_window`, the serve counters) is 60 lines on shipped code and should
survive as the adoption gate's meter.

## Fit with PRINCIPLES

- #23 "Nothing past c … it allows to cheaply partition compute, even gravity is light speed":
  the light cone already partitions retention in the law; this run measures that the *view's*
  walk, not the cone, is what the shipped floor serves.
- #3 "Compute only surprises … Nothing is evolved that can be derived when looked at": a
  retired segment 98.4% past every certified window is stored surprise nobody certified.
- #28 "The view is an instrument … real vs displayed is not the same thing": the one reader
  that needs the past is the instrument, and it has a documented degraded mode.

## The lens

The scout lens searched for the representation (retention as a light-cone window) and measured
it on shipped code; what it may have missed is the view's internals (`observe::partial`'s walk
was read, not instrumented per-call-site — the deep serves are attributed by elimination and
doc-reading, not by a backtrace) and the burn/held-scan reader. A falsifier on the warm-gather
path is the one experiment that separates "the floor is view-load-bearing" from "the floor is
dead weight".
