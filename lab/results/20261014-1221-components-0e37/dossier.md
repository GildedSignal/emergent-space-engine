# Dossier — 20261014-1221-components-0e37

## Claim

On the shipped wave scene the compiled orbit a kick stores is **write-only memory for the
engine** (read only in the burst at its own next kick; the retired generation is read **0**
times in flight), it is **exactly its `OrbitKey`** (1,001/1,001 sampled tables regenerate
bit-identically from `Orbit::compile(key)`), so the law-mandated standing floor is **673 B/body
against 1,806 B standing** — and the one real reader of the past is the **view's ramp
completion** (309,227 retired-binding reads in two gathers, ≥1/row post-wave), which the two-word
completion (a-word's open direction 1) replaces: deleting the retired generation moves the
ladder's break #2 (4 GiB at 10⁶) out to ~2×10⁶ bodies at zero CPU cost, and with the closed-form
kernel the current generation deletes too (~750 B/body standing).

## Bottleneck

The scoreboard's memory row (live bodies in the flyable engine: 2.46 KB at birth, 5.1 KB after
the first kick, 10^2.6–2.9 over the ≤ 6 B/body goal) and nladder's measured next-break #2: "the
compiled shape is a cache of the key … the representation's lever, not a prune rule" — named,
unmeasured. This run measures that lever: the read census, the floor, the idiot index, and the
design within 10×. Gain: −37% standing bytes / −~800 B/body of footprint for free (retired
generation), −~60% standing with the kernel priced in; deletes the first memory wall the N
ladder meets.

## Evidence

All numbers from `regen.sh` on this tree (Linux shared cloud, orders only; the counter patch is
in `work/patch.diff`, digest-neutral: `frame_digest` identical pristine vs patched, every flight,
4 schedules agree).

Scene: `plane_extra` belt, N=100,028 bodies, 80 wall s at rtf 200 → 15,997 game s, past the
first-kick wave (13,051–14,534). Build 4.3 s, 226 MiB; flight max frame 11.97 ms, 0 over 12 ms,
153,993 events.

**Sizes (shipped structs):** BodyRec 464, Binding 192, Segment 208, Tube 16, Knot 88, OrbitKey
56, Item 16 B.

**The census** (`census_1e5_v3.txt`):

- Held at end: **200,567 tables** (100,076 current + 100,491 retired) — 2.0 tables/body after
  the wave; history grew by exactly the belt (+100k at the wave, 638–785 before it).
- Accounted split B/body: rec+plan 464 (2.0 plan items), current shape 672, retired shape 670 —
  **74.3% of standing is derived knots**; floor (rec + plan + 1 Segment) **673**; standing
  **1,806**; idiot index **2.68×** accounted, **~4.6×** on footprint (459 MiB / 100k = 4.59
  KB/body vs ~1 KB/body floor-with-mallocs; footprint rose 226→459 MiB = +2.33 KB/body across
  the wave — ladder's 2.6→5.1 KB reproduced).
- **Flight reads are O(1) in N:** steady 107–191 decodes/frame at N=10⁵ — the same 191/frame the
  N=2,000 smoke read (50× the bodies, flat). The belt's tables are read only at their own kicks:
  2,199,316 flight reads ≈ the wave's kicks × ~10–15 (fit readout + τ reads), ≈ 6.9×10⁻⁴
  reads/held-table/game-s overall.
- **Retired reads in flight (sampled before any gather): 0.** Every retired-table read in the
  process comes from the view's gather.
- **The gather is the only mass reader:** cold gather 4,238.7 ms, 1,071,968 decodes, 100,048
  seen = **10.71 decodes/row**; 309,227 rows completed through a *retired* binding across two
  gathers — post-wave nearly every row is mid-kick-window and the ramp (`observe::partial`)
  decodes the previous tube 2–3× per row.
- **Regen:** 1,001/1,001 sampled current Cycle tables reproduce exactly from
  `Orbit::compile(key)` — knot count, crossing count, `advance`/`period`/`proper_period`. The
  cache holds no information beyond the key (plus `clockwise`/`unit`, already in `Entry`).

## Predictions

`predictions.md` was written before the decisive run. P1 (flight reads O(1) in N, ≤ ~600/frame at
50× bodies) **held** (107–191). P2 (wave adds ≈ +N retired segments, retired shape ≈ current
within 2×) **held exactly** (670 vs 672 B). P4 (100% regen) **held** (1,001/1,001). P3 held its
first half (retired tables ≈ 0 reads in flight) and **failed its second half as written**: I
predicted the gather would read retired tables at ≪1/row; post-wave it is ≥1/row (309k/2
gathers) — the ramp completion is a real, mass reader of the past at today's Θ(N) view. That
failure is the useful half: it names the deletion's missing piece (the completion word, below).

## What would make it wrong

- A between-kicks consumer my headless flight does not exercise: the encounters tier, once wired
  (H0216), reads candidate states at conjunction ticks — each miss then costs one 30 µs rebuild
  (or the tier's key-space arithmetic, b29a). The census bounds every such reader: reads/frame
  are countable, and today's flight has none beyond the fixed cast.
- The 309k retired-read share is a post-wave snapshot (everyone freshly kicked). At steady state
  the mid-window fraction is a birth constant (window/interval, `step_log2`-set), still O(1) per
  gathered row; agather at longer flight could read it lower, never to zero — the word, not the
  count, is what the design changes.
- Linux footprint (VmRSS+swap) vs the M1's phys footprint: orders only; the accounted-byte split
  is allocator-independent.
- The regen sample is current *Cycle* bindings on the belt band (e ~0). Passages (`edge` in the
  catalogue key) and Plunges (no key) are out of the sample; the plane's members are the
  high-e tail where shape bytes are 5–20× larger — the same lever, thinner tables (5a3b).

## Cost of adopting, and fit with PRINCIPLES

Adoption is one build on the storage seam (`Segment` drops `entry`, gains the key and the
completion word; `observe::partial`'s `base.cartesian(mid)`/`(t)` read the word; `binding_at`
recompiles on the rare non-window read): canon-neutral for the law (the word completes to the
same integers a-word measured digest-identical), the view unchanged, prune unchanged. It deletes
the retired generation's knots everywhere (~520 B/body accounted, ~800 B/body footprint), needs
the **two-word** (a, ȧ) completion — the one-word form is gate-refuted (a-word, f2b7), the
two-word is "the only stored form second order at the handover by construction" — and then the
current generation can follow the same route once the kernel lands (de99: all-three channels
2.9 µs), taking standing to ~750 B/body ≈ 1.1× the floor.

- PRINCIPLES #6, verbatim the requirement this component serves: "Store the generator, not the
  generated." The knots are the generated; the key is the generator; the census shows they are
  stored and (for compute) never looked at.
- #3: "Nothing is evolved that can be derived when looked at (clocks, redshift, views)."
- #1 (delete before optimizing) and #24 (the memory floor is information): the deletable share
  is 74.3% of standing, and deleting it costs 0 CPU in flight.

## The lens

The components lens prices one component against its floor; a local optimum can move cost to
another component. Measured neighbours: the reader side (the view's Θ(N) gather at 10.71
decodes/row is what makes the tables *look* live — with the far-row fix (view.md) the working
set collapses to visible rows and the word serves those); the kick side (one extra compile per
kick only if the current generation is dropped; Carlson prices it at 2.9 µs, de99); the widths
(BodyRec 464 B + Segment 208 B is now the floor's own fat — the quanta question, memory-h-live's
territory, not this run's). What the lens may have missed: I did not measure the gather's
retired-read share at steady state (post-wave only), and the regen check samples Cycle keys
only.
