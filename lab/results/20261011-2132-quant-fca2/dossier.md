# Dossier: the plane's frame capacity — the readout breaks first, at ≈10³ members

## Claim

The shipped plane's 60 Hz frame breaks on the members axis at **M\* ≈ 7×10²–10³ fleet members**
(frame p99 crosses 16.7 ms between M=500 and M=2000), and the breaker is the **unbudgeted readout**
(gather 55–63% of every bad frame), not the budgeted engine; the engine's own failure mode is the
designed graceful dip, holding zero hitches to rtf 10⁴ — but its contact-epoch batch is one
unbounded synchronous claim (49.5 ms at M=8000), violating plane.md foundation 7 as shipped.

## Bottleneck

Board #4 (smoothness and the allocator) and the scale risk ("work must track real encounters"):
the allocator's builders need to know which stage's tail actually breaks the frame and at what
capacity. Measured answer: the frame is a readout with a physics rider (engine 4–24% of the frame;
gather+json+wire 76–96%). The readout costs ~10 µs per handed-out body per frame and sweeps every
body every frame with no culling, so the frame's cost tracks the body count, not what the player
can distinguish. This sets the ceiling for battles in the first-flight scope three orders of
magnitude below any scale goal, and it names the lever for the readout lens (b-readout-cost) and
the belt build (B18b): cull and cheapen the per-body readout, and slice the contact batch.

## Evidence

All runs: `xtask universe --bench`, Linux/x86 cloud runner (8 vCPU, shared; orders of magnitude
only — the M1 re-measures), release build, 1 thread, seed 1, machine state (uptime/load) recorded
inside each JSON (`uptime_before/after`); peak RSS from `/usr/bin/time -v` in the `.time` files.
Reproduce with `bash reproduce.sh` (uses this run's patch: `--members` clamp lifted to 4×10⁶ and a
`--csv` per-frame dump added to the bench; the patch is saved by run.sh).

**A. Members sweep** (rtf 100, unpaced, 10 s = 600 frames; `data/A-m*.json|csv`):

| M | bodies at end | frame p50/p99/p99.9 ms | hitches >16.7 | engine max | view max | peak RSS |
|---|---|---|---|---|---|---|
| 48 | 71 | 1.04 / 2.87 / 6.02 | 0 | 5.2 | 1.3 | 12 MB |
| 500 | 488 | 6.63 / 11.7 / 12.3 | 0 | 11.2 | 5.3 | 45 MB |
| 2000 | 1940 | 28.7 / 41.8 / 43.7 | 560 | 18.3 | 31.2 | 332 MB |
| 8000 | 6048 | 68.0 / 92.3 / 157.8 | 589 | 49.5 | 120.5 | 2138 MB |

- p99 crosses 16.7 ms at M\* ≈ 750 (interpolation). The worst frames are view-dominated (frame
  594 at M=8000: 172 ms = view 119 + json 19 + wire 4 + engine 30). Stage shares at M=2000–8000:
  view 59–63%, json 17–24%, wire 4–5%, engine 8–20%.
- **Why gather breaks:** members do not stay cheap extrapolated emitters. The battle disperses and
  members are handed out into the doll as bodies (M=500: 488 bodies at end, 96% handed out), and
  every doll body is read through a Newton light-cone crossing every frame: view p50 19.6 ms /
  1940 bodies ≈ **10 µs per body per frame**, json+wire ≈ 1.9 µs per seen emitter.
- **The leak (time axis):** frame CPU median grows monotonically with game time — M=2000:
  18.5 → 20.5 → 32.9 → 32.6 ms over the run's quarters; M=8000: 40.5 → 60.4 → 73.3 → 84.9. The
  battle's aftermath converts cheap members into expensive bodies at a roughly constant rate: a
  leak, not a burst (per-frame CSVs `data/A-m2000.csv`, `data/A-m8000.csv`).
- **Memory:** peak RSS grows superlinearly in handed-out bodies (168 MB at 852; 324 MB at ~2.2k;
  2138 MB at 6k): ~170–355 KB per member at peak against `bytes_per_body` 8.3 KB — the store is
  not the cost; the peak is aftermath-side (catalogue plus retained light-cone histories;
  mechanism unattributed — [INFERENCE]). At this rate a 10⁶-member battle needs hundreds of GB.

**B. Time-factor sweep** (M=48, unpaced, 5 s; `data/B-r*.json`): rtf 10³: p50/p99 1.86/7.51 ms,
0 hitches, lowest-1% rtf 70/1000. rtf 10⁴: p50/p99 6.30/7.05 ms, 0 hitches, engine p50 4.92 ms
(saturated at its 5 ms budget), lowest-1% rtf 620/10⁴. The dip stays a ~6–7% tail at both factors:
**no hitch to rtf 10⁴; the graceful dip is the only failure mode on this axis.**

**C. The player's burst** (paced, rtf 100, 20 s, level 15 = 11,561 g; `data/C-l15.*`): burn frames
median 1.70 ms vs coast 1.60 ms (+6%); worst frame 8.67 ms; 0 hitches; player alive. The market
order is priced like a coast frame: the player's wake is its own body's rebinds, as designed.

**D. Controls.**
- *Invariance (the allocator's foundation):* identical digest `09e40859…` at the same cut for
  paced vs unpaced and engine budget 5 vs 0.5 ms (`data/D-paced.json`, `data/D-eng05.json`,
  `data/A-m48.json`). The budget moves work, never outcomes — verified, not just claimed.
- *Positive:* M ≥ 2000 breaks massively (above) — the instrument can fail.
- *Paced vs hot loop:* the as-flown (paced) frame at M=48 rtf 100 costs p99 10.2 ms against 2.9
  unpaced — **3.5× at p99** (cache cooling between frames). Unpaced lab numbers understate the
  player's frame; the dashboard's paced mode is the honest one.

## Predictions (predictions.md, written before these runs)

- P1 half-right, mechanism wrong in an instructive way: crossing measured at ≈750, not 8×10³
  (4–10× optimistic), and I picked json+wire as the breaker; gather is (59–63% share) because I
  underweighted the handout: members become Newton-crossed bodies. json is the second breaker.
- P2 (handout leak) **held**: monotone growth, bodies 28→6048.
- P3 (rtf axis) held on "no hitch to 10⁴, graceful dip only", but the dip does not deepen with rtf
  in this range (stays ~6–7% at the 1st percentile): predicted a fall below 0.9× by 10⁴; measured
  0.93× at 10³ and 0.94× at 10⁴ — held only marginally, reported as such.
- P4 (burst is free) **held** (+6% on burn frames, no hitch at 11,561 g).
- P5 (positive control) **held**.

## What would make it wrong

The frame measured here includes the debug view (gather+json+wire); plane.md says the visual layer
comes later. If the shipped view is replaced by a culled, LOD'd readout whose cost tracks what the
player can distinguish, M\* moves up by the culling factor and the engine (budgeted, dipping
gracefully) becomes the binding stage — the contact batch and the aftermath memory would then be
the next breakers, both measured here. On the M1 the constants change (unified memory, different
cache geometry); the M\* is an x86 number, the stage shares and mechanisms are the transfer.

## Cost of adopting, and fit with PRINCIPLES

Nothing to adopt in main: this is a measurement (the patch adds a `--csv` dump and lifts the
`--members` clamp for the lab only). The findings route work: (1) the readout must cull — its cost
must track distinctions, not bodies ("Compute only surprises"; board #3: "never computing what
nobody can observe"); (2) the contact-epoch batch must be sliced into budgeted pieces (foundation
7: "nothing takes an unbounded synchronous claim on the frame"); (3) unpaced bench numbers must
not be quoted as the player's frame. All three are one step from their owners (b-readout-cost,
the fleet/lattice owner, and the lab's reporting rule).

## The lens

The Quant lens prices tails and capacity, and it got what it prices: a crossing, a leak, an
unbounded claim, and an invariance check. What it may have missed: nothing here says the readout
is *wrong* — the view is doing exact light-cone crossings per body, which is the game's point; the
HFT instinct to shave it must not spend the exactness (the lens's own blind spot). The memory
mechanism (histories vs catalogue vs settle temporaries) is unattributed; a memory-lens run should
nail it before anyone optimises it.
