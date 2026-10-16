# Dossier — 20261016-0213-fermi-1a1c (Fermi lens): the 10⁹ budget of the flyable plane, assembled

**Claim.** On merged main, the plane's ladder to 10⁹ has its first engine-side breaker at ≈ 8×10⁴
bodies — the belt's unstaggered first-kick wave, whose TRUE peak frame (487 events, 22.95 ms
budget-free at 10⁵ on this box; 14.3 ms at the M1's 29.3 µs/event) already violates F1's 12-ms
letter at 10⁵: the record's "the wave holds at 3×10⁵" (after2) was the 12-ms budget cap hiding
the peak, not the wave fitting; the budget absorbs the excess into window slack (lag 0) only until
the throughput break at ≈ 1.0×10⁶, where memory (1.6×10⁶ at the 4 GiB gate; 1.3×10⁶ at the
post-first-kick 4.75 kB/body) takes over — and at 10⁹ every compute term fits ONLY as
(ES_STAGGER ∧ kick-at-the-0.11 µs-key-arm) together (each alone leaves 45–11,900× over), while
the terms no kick lever touches are memory at the driven-belt floor (15.8 GB = 2.6× the machine,
the known 4-field wall), the player's first scan (113 B/body × 10⁹ = 113 GB pinned) and the
page's view gather (8×10⁵×) — so the next rung's lever order is wave cadence, standing store,
never the frame.

**Bottleneck.** The board's top item (bodies: 10⁶ flown against 10⁹). The lens's question — bytes
per body, events per body per game-second, ns per event, which term breaks first and by how many
OoM — had per-term answers scattered across pages and the integrator's ladder.txt, but no single
unit-checked budget on merged main, and one wrong shared reading (the wave "holding" at 3×10⁵,
an instrument artifact). Gain: the lever order for the next rungs, and one artifact killed.

**Evidence** (Linux 8 vCPU i7-4790, load 0.01–0.55, 13 GB free; state in raw/state_*.txt;
orders of magnitude — the M1 constants are quoted from artifacts/runs/nladder/ladder.txt after2):

- `nladder 100000 coast 160 100 100000` (budget-free, the decisive arm; raw/wave_n100000.txt):
  frames after 1 s: 9,540 (15,900 game-s, through the wave at 13,051–14,542); engine p50 0.007 ms,
  p99 15.9, max **22.95 ms with 487 events** (worst-5 all inside the wave window, 21.8–23.0 ms /
  439–487 events ⇒ **47–51 µs/event** this box); events/frame p99 324; over: 0 (budget-free),
  lag 0.000; kicks 125,077 (7.86×10⁻⁵/b/game-s incl. the wave), boundaries 25,086 (N-independent:
  the locals), held scans 0; peak footprint 475 MB at end = **4,750 B/body after the first kick**
  (2,349 at build).
- `nladder 10000 coast 160 100 100000` (raw/wave_n10000.txt): max 15.57 ms is frame 61 (the
  fleet's exodus, 71 events — present at every N); the WAVE's own frames never reach the worst-5
  (locals' 257–334-event storms dominate), i.e. the 10⁴ wave peak ≲ 49 events (clump 4.35 × mean
  11.2) as predicted; kicks 35,077 of which the belt's ≈ 10⁴.
- `belt_first 100000 / 10000` (raw/belt_first_1e{4,5}.txt): first-kick window 13,051–14,542 and
  13,051–14,535 game-s — **width 1,491 game-s, N-independent** (the wave is one shared anchor,
  cf45/ed3a's mechanism, confirmed on main).
- Short arms `nladder {1000,10000,100000} coast 20` (raw/short_n*.txt): B/body 2,465 → 2,348
  (M1 anchor 2,443); build 42 µs/body flat (M1 28.7); engine p50 0.034–0.039 ms **flat in N**
  (the frame-walk fix holds on Linux); ev/b/game-s falls as 1/N (total ≈ 5.85 events/game-s — the
  locals and player only); warm view 19.7 → 2,118 ms = 21.2 µs/body, exponent 1.03.
- The budget itself: `python3 budget.py` → budget_table.txt + budget.json (all constants, laws,
  break-Ns, gaps at 10⁹). Ranked by break-N (M1-projected):
  view gather 1.2×10³ (page-side) → **wave F1-letter 8.4×10⁴** → wave throughput 1.0×10⁶ →
  memory 1.6×10⁶ (post-kick 1.3×10⁶) → build 2.1×10⁶ (8.0 core-h at 10⁹) → steady stream
  1.6–8.1×10⁷ (49–243 cores at 10⁹, rtf 100) → player scan 5.3×10⁷ (one held scan pins 113 GB at
  10⁹; an answer costs 1,700 s). Gaps at 10⁹: wave letter 1.19×10⁴ (÷16.7 stagger, ÷266 key-arm
  ⇒ 2.7× the letter; ed3a's own staggered-birth composition puts it at ~0.5× — both compositions
  agree the two levers are jointly REQUIRED); steady stream 49–243 cores ⇒ 0.19–0.91 cores at the
  key arm; memory 407× standing ⇒ 15.8 GB at the 126-bit driven floor (2.6×) / 5.0 GB phase-locked.
- Claim-check (lens item 3): cf45's composed "steady stream 148× the frame budget at 10⁹"
  re-derives as 49–243 cores (68–338× the 0.72-core budget) from three independent rate anchors
  (the doll law 128 kicks/Cinder-period = 1.68×10⁻⁵/b/game-s; this run's post-wave residue
  ≈ 4.5×10⁻⁵; ed3a's plateau 8.3×10⁻⁵) — bracketed, no 10× disagreement anywhere.

**Predictions** (predictions.md, written before the flights): P1 held exactly (B/body, build µs,
flat p50). P2 half-held: the window (13.0–14.6k, width ~1.5k) and the 47–51 µs/event held; the
break-N did NOT — the true peak is over the 12-ms letter AT 10⁵ (I predicted the crossing at
2–5×10⁵, trusting after2's capped peaks; measuring budget-free moved it down ~3×). P3 held (the
10⁴ wave stays under the locals' own storms). P4 held (the three rate anchors bracket cf45's
148×). P5 did not fire (µs/event ≈ 49 > 10; the ranking stands with the M1 constant).

**What would make it wrong.** The F1-letter break-N scales the 10⁵ true peak by 1/N (peak
sublinear in N would LOWER it — an upper bound; the 10⁴ arm cannot resolve the wave under the
locals' storms). The wave-peak composition at 10⁹ keeps a clump after staggering (ed3a's measured
staggered plateau says the remainder is ~0.5×, not 2.7× — the truth is between; either way both
levers are required). All Linux rates are one shared box at low load; the M1 constants are quoted,
not re-measured (the integrator re-measures). The steady-stream rates are cold-belt (quiet coast,
player at Home): a driven or burning belt raises the event rate (taleb-51b7: one scan per player
binding change) and the scan term early.

**Cost of adopting / fit.** Nothing to merge: this is a budget and one instrument lesson. The
adoption it argues: (1) ES_STAGGER is load-bearing for any flight that reaches 13–14.5k game-s
(the integrator's call — it is built, default-off); (2) the wave arms of any future ladder rung
must fly BUDGET-FREE for the peak (a 12-ms arm reports the cap, ~410 events on the M1, as its
max — after2's 390/409 "max events" are cap readings); (3) the next rung's order: wave cadence
(stagger default), then the standing store (compact, phase-locked), never the frame walk.
PRINCIPLES: "Measure before claiming, and never strawman" (the 3×10⁵ reading was an instrument
artifact, now named); "the cheapest compute is compute not done" (the budget shows which term to
delete first); "controls on both sides" (the budget-free arm is the positive control the capped
arm lacked).

**The lens.** Fermi estimation composes constants but cannot create them: every rate here is
someone's measurement, and my only new ones (µs/event, true peak, post-kick B/body, N-independent
window) come from two flights on one quiet box. What the lens may have missed: the locals' event
storms (N-independent, 10–15 ms frames at EVERY N) sit under every wave number — the F1 letter's
real first binder in a 20-s flight is the exodus/storm baseline, not N; and I did not fly a burn
arm (the scan term is quoted from taleb-51b7, not re-measured).

## Commands (each ≤ 60 s except the two wave arms)

```
cargo build --release --example nladder --example belt_first -p emergent-universe   # ~30 s warm
for N in 1000 10000 100000; do ./nladder.bin $N coast 20 | tee raw/short_n$N.txt; done
./nladder.bin 100000 coast 160 100 100000 > raw/wave_n100000.txt   # ~19 s wall
./nladder.bin 10000  coast 160 100 100000 > raw/wave_n10000.txt    # ~5 s wall
./belt_first.bin 100000 | tee raw/belt_first_1e5.txt; ./belt_first.bin 10000 | tee raw/belt_first_1e4.txt
python3 budget.py > budget_table.txt
```
