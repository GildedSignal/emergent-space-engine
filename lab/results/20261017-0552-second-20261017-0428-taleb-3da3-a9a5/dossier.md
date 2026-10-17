# Dossier — 20261017-0552-second-20261017-0428-taleb-3da3-a9a5 (second author)

## Claim

**The checker's named experiment is flown, and it splits the silver's claim in two: the
over-merging tax does not exist — in the most benign archipelago geometry the arms tie
within 5% with digests bit-identical (shipped 6/6, cap16 6/6, cap64 5/6 clean; one cap64
draw panics even there), because the wave's Fermi-pumped vmax, not its latch margin,
carries the forecast to the quiet sea — but "bounding the latch buys nothing at any size
tried" is refuted at its own named edge (28,160 bodies, paired, back-to-back: cap64
finishes 143.8 s with the checker's bit-identical digest while shipped DNFs at 400 s),
and the probe's decisive find is third: the rollback path has a shipped-only,
draw-flippy published-finality breach (`alloc.rs:1510`, "rollback … would revise its
published tick", no env vars, plain battery at stagger ≥ ~3·10⁴, shipped's latch at E=2⁶⁴
trying to absorb the storm) that the cap does not cause and does not fix — so ES_CAP
stays killed as an adoption (its one win is a 10 c/s grind vs a DNF; everywhere else it
ties, panics with shipped, or hangs at one core), the kill's "not a reachable ruin"
sentence loses its knobless half, and the page's next experiment is the breach, not the
latch.**

## Bottleneck

The prior silver's named gold experiment (check.md): "a controlled archipelago (quiet sea +
one cannon, or the 28,160 early wave) run paired under measured load … If the wide latch
does not tax quiet regions (caps win or tie nowhere), the kill generalizes → gold. If it
does, the cap's verdict flips." This run is that experiment, both branches, plus the
shipped crash basin the probe uncovered. Board: allocator; wiki page `allocator-ratchet`,
open directions 1, 3 and 6, and the "Shipped's own ruin tail" contradiction (now a named,
reproducible panic).

## Evidence

Instrument: the prior runs' `tax` verbatim (their `work/patch.diff`) plus two scene knobs in
`tax.rs` only — `TAX_CANNONS=K` (first K cells fire; default all) and
`TAX_ARCHI="M:pitch_q:x0_q"` (a quiet sea of M one-world cells, `pitch_q·q` apart, starting
`x0_q·q`; nothing physically crosses to it). Allocator surgery byte-identical to the prior
runs' (ES_CAP arm only; default-off = shipped verbatim). Scene: 128 cannon cells (stagger
30; alone it latches E=128–512 with 7–14 rollbacks and ends one region) + sea at pitch
784·q = 200,704 (quiet-quiet edge gap ≈ 200k: bridged by a latched quiet forecast
v = 2(2E+E−1) ≥ 736 within the ≤ 272-chronon plan lookahead; not bridged at E ≤ 64),
coupled at x0 = 40.0M / decoupled at 102.4M. Horizon 6,000 (2×3,000) at M=1,280; 3,000
(2×1,500) at M=64. Loads 0.5–2.2 logged per run (`work/battery.log`); every number below
regenerates via `regen.sh` (≤ 15 min; the DNF timeouts are the spend, and regen's shorter
DNF timeouts reproduce the class).

**A — decoupled sea, 64 cells (the most benign geometry): all arms tie where they finish,
digests bit-identical, and even here the basin reaches a capped draw.** Battery window,
six runs (3 arms × 2 draws), load ~2/8 cores: walls 2.16–2.26 s, regions end 1 every run,
rollbacks 8–14, digests `9567902a…/4aa5ba0b…` in all six. Fresh draws after the battery
(4 per arm): shipped 4/4 and cap16 4/4 clean (6/6 with the battery), **cap64 3/4 — one
1510 panic in the same scene that tied** (5/6 clean overall). Wasted-ops stays
draw-scattered within arms (shipped 347k/921k) — the checker's fragility verdict,
confirmed on the new geometry. The sea is swallowed under every arm (regions=1 already at
tick 1,500, even at cap16): the pumped cannon vmax gives the wave's own region a forecast
reach that bridges any x0 at these horizons, so the wide latch is not what couples the
sea. **There is no over-merge for a cap to refuse: caps win and tie nowhere here — and
the most benign geometry is already a crash basin for the 64-cap.**

**B — coupled sea (40M): a draw-flippy crash basin for every arm.** 64-cell sea, 2 draws
per arm plus the calibration pilot: shipped = 1 panic / 1 finish, the finisher saturating
the latch at **E=2⁶⁴ = 18446744073709551616** (64 rollbacks; digest `a7080be9…/e61f13e0…`);
cap16 = 1 panic / 2 sixty-second hangs at ~1 core; cap64 = 2 panics / 1 finish (84
rollbacks, wasted 4.6M, same digest). The swallow breeds a rollback storm (64–84 rollbacks
vs the wave's own 7–14) and the storm breaks the invariant or the schedule, whichever the
draw picks. Where arms finish, digests agree across arms.

**C — the full-size probe (1,280-cell sea, 11,648 bodies): nobody finishes.** Coupled:
shipped panics in 13 s (region 1698 restored from tick 128 against published 144); cap16
and cap64 grind to DNF at 300 s, ~1 core, stage 1 never completing — even a 600-chronon
horizon DNFs at 200 s under cap16 (≤ 3 c/s: the many-region regime's own cost, not the
rollback path). Decoupled: shipped 2/2 draws panic within seconds; the caps grind the same
(cap16 DNF at a clean 420 s; cap64's decoupled run was killed at ~7 min in a script
cleanup — regen reproduces the class). At this size the quiet sea is not a tax anyone
pays: shipped's failure mode is the instant certificate break, the caps' is a sub-3-c/s
grind. Neither is adoptable; neither fixes the other.

**D — the breach is shipped's own, knobless, and the latch is implicated.** Plain battery,
128 cells, horizon 3,000, no scene knobs: stagger 300 and 1,000 clean (0 rollbacks, E=1);
3,000 → 16 rollbacks, E=65,536, finishes; 10,000 → 18 rollbacks, E=262,144, finishes;
30,000 → draw-flippy across four draws in two windows (finishes: 2.97 s with 11 rollbacks,
E=2,048, one region, digest `2210113c…/fdbb5ae5…`, and 38.6 s-class with 27 rollbacks,
E=1.3×10⁸; panics twice on `alloc.rs:1510`); 99,999 → panic both times tried, no result.
At the same stagger-30,000 edge, **cap64 finishes both draws** (38.6 s, 25 rollbacks, E=64,
238 regions end, merges/splits 613/649, the *same* digest `2210113c…`) — 13× shipped's
clean-draw wall, but no panic. So the breach needs the unbounded latch's growth (the cap
suppresses it here), is draw-flippy at the edge, and costs 13× to suppress: the cap is a
mask, not a fix.

**E — the checker's 28,160-body draw, paired and settled.** Same window, back-to-back:
**cap64 finishes 143.8 s** (8 rollbacks, E=64, 6,877 regions end — the row stays
fine-grained, 10 c/s, digest `ae37a51c…/4c0f7996…` — **bit-identical to the checker's
57.2 s draw**); **shipped DNFs at 400 s** (0 panics; the prior box finished it in 149 s,
so it is borderline, not wedged; region trajectory unrecorded — a DNF prints no stage
row). The confound is resolved: not load. In the quiet-heavy early-wave regime the bound
buys a finish against a DNF — the one cap win on record — and it is a 10 c/s grind vs a
≥ 2.8× slower collapse, the same many-region regime that DNFs outright at the
archipelago's full size.

## Predictions

`predictions.md`, frozen before D1/D2/D3/D4. **PD2 half-failed, honestly:** all arms
finished decoupled-64 with identical digests (held), but the caps' sea did NOT stay
fine-grained — the pumped-vmax channel swallows it under every arm (my pitch arithmetic
priced the latch's margin channel and missed the wave's own velocity channel; the
calibration pilot caught it, the file records the miss). **PD1 half-held:** the caps break
in the coupled sea as predicted, but shipped breaks with them (1/2 panic at 64 cells, 2/2
at 1,280 — I predicted shipped finishes). **PD3 failed into its pre-registered
alternative:** cap64 survives the stagger-30,000 edge where shipped panics — so the basin
needs the wide latch, exactly the alternative the file named. **PD4 held:** cap64 finished
< 120 s? No — 143.8 s on this slower box (the checker's 57.2 s stands for the fast box),
shipped DNF ≥ 250 s (400 s), and the finisher's digest matches the checker's bit for bit.

## What would make it wrong

- The panic's draw-flip makes single-draw claims unsafe; every deciding row above has ≥ 2
  draws, a paired same-window control, or a knobless reproduction (D4's pairing is
  back-to-back; D3's edge is 4 draws across two windows plus the 5-point sweep). A quieter
  machine could turn the caps' hangs into finishes — restoring ties, not wins, everywhere
  except D4/E, where the separation is the row's granularity itself (6,877 regions vs the
  swallow), not scheduling.
- The mechanism chain (pumped vmax → swallow → rollback storm → invariant breach) is read
  off trajectories and counters, not instrumented inside the allocator: which restore
  crosses which published tick, and why finality let it publish, is unopened
  (direction-3 work). If the breach turns out not to need latch growth, the D3 arm-check
  (cap64 clean at the edge, twice, same digest) still bounds it to the storm's depth, not
  the cap.
- Batch only; the player-visible surface of the panic (crash vs hitch) is unmeasured. Sea
  scenes ≤ 11,648 bodies; the sweep and D4 at 1,408/28,160 bodies.

## Cost of adopting, and fit with PRINCIPLES

Adopting: nothing — ES_CAP stays dead (its one win, E, is a 10 c/s grind against a DNF;
everywhere else it ties, crashes with shipped, or hangs). The adoptable output is the bug
report: `alloc.rs:1510` is reachable from quiet-heavy scenes on shipped `main` with no env
vars, a certificate break ("nothing published can be touched") that neither the ratchet's
permanence nor its bound prevents. Via negativa (PRINCIPLES #1): the run deletes the
over-merge tax from the page and demotes the latch question behind the breach.
#25 (don't multiply by zero): a draw-flippy panic in the allocator is the ruin class this
page exists to price, and it is now the cheapest one to reproduce (stagger 30000, 40 s).

## The lens

The second author's job was the named experiment; Taleb's question — where is the ruin —
got an answer nobody priced: not in the latch's level (capped or not) but in the storm the
swallow breeds, and shipped's own permanence feeds it (E=2⁶⁴) as often as it absorbs it.
The 28k "cap win" is real but it is survival into the slow regime, not upside — capping
the downside here still caps the upside, and neither survives the archipelago. What this
lens may have missed: I did not instrument the panic inside the allocator, did not run
frames, and priced the geometry with one channel (margin) where two exist (pumped vmax).
