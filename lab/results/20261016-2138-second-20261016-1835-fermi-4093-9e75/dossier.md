# Dossier — 20261016-2138-second-20261016-1835-fermi-4093-9e75 (second author on 20261016-1835-fermi-4093)

**Claim.** The checker's named experiment is done and the freeze law now stands on direct
measurement: the crest's **spell** (the longest run of frames whose presented time the 12-ms
budget did not deliver) lasts **7.0–7.1 s at 10⁵ and 21.9–22.1 s at 3×10⁵** at the game's
real 60-fps pacing, matching **E_spell·Ĉ/0.72 with same-run constants at ratio 1.01–1.04**
across four arms (Ĉ 50.5–52.7 µs/event, delivered 13.6–14.1k ev/s ≈ the 0.72/Ĉ ceiling); the
**deficit integral** (Σ(target−presented)·TICK_SECONDS = 23.1k / 42.3k / 79.6k game-s) replaces the
saturated lag — at rtf 3600 the lag prints exactly its 60.000 ceiling while the spell and
E_spell are unchanged (E ratio 1.02) and the deficit doubles (1.88×); the crest's events are
**linear in N** (E ratio 3.08–3.09 for 3× belt bodies ⇒ one crest event per body), so the 10⁶
crest is **72–73 s** and the 10⁹ crest **20.1–20.3 h** of frozen presented time (52,049–52,549 s
CPU, or 185–187 cores sustained at rtf 100) — measured-derived, no longer resting on the lag; and the **burn
arm inverts the dossier's risk**: on the burn the freeze is absent (spell 0.7 s, deficit 1,610
game-s) because the crest **breaks the budget instead** — 167–178 frames over 12 ms, worst
**2.5–2.6 s carrying ~50k events at the usual ~50 µs each**, the run truncated at 55 s and
memory at 5.9 GB: one started item resolved a whole wave through the per-item stop's
first-item escape (universe.rs:1007–1010; the shipped comment's documented worst overrun is
1.4 ms — measured 2,515–2,585).

**Bottleneck.** Board item 1 (bodies: 10⁶→10⁹) and item 3 (the kick), continuing 4093. Gain:
the crest arithmetic at 10⁶/10⁹ is measured (integer spell frames, event counts, same-run Ĉ)
rather than derived from a metric that saturates; deletes the last soft spot in 4093's silver
and adds a new measured fact — the budget's *binding*, not just its rate, is what the burn
removes. Deletes nothing shipped; corrects a9d7's record sentence (below).

**Evidence** (shipped `nladder` on merged main, coast/burn, 40-s flights, budget 12 ms, rtf
1800/3600; patch = the Linux `footprint()` fallback + an additive `freeze:` print, no law
touched; full log `flights.log`, ledger `ledger.txt`, machine state `state.txt`; box: 8 vCPU,
load 0.3, shared x86):

| arm | ran | spell @ | spell frames | spell wall | E_spell | presented inside | Ĉ µs/ev | E·Ĉ/0.72 | ratio | deficit game-s | lag prints |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F1 10⁵ coast rtf 1800 | 2,400 | 499 | 423 | 7.0 s | 96,981 | 1,461 game-s | 51.2 | 6.9 s | **1.02** | 23,064 | 29.14 (°30) |
| F2 3×10⁵ coast rtf 1800 | 2,400 | 504 | 1,317 | 21.9 s | 298,562 | 1,623 game-s | 52.3 | 21.7 s | **1.01** | 42,317 | 29.80 (°30) |
| F4 3×10⁵ coast rtf 3600 | 1,800 | 278 | 1,312 | 21.9 s | 304,508 | 1,841 game-s | 51.1 | 21.6 s | **1.01** | 79,626 | **60.000** |
| F3 3×10⁵ **burn** rtf 1800 | 1,460✝ | 109 | 39 | 0.7 s | 2,033 | 195 game-s | — | — | — | 1,610 | 29.27 (°30) |

1. **The freeze measured.** Every coast spell closes inside its flight (F2's ends at frame
   1,821 of 2,400) — the crest fully drains. Inside F2's spell the presented time advances
   1,623 game-s against 39,510 wanted: **96% frozen**. The spell is 87% of all deficit frames
   (1,517); the rest is the post-crest tail. The law's residual is ≤ 2% at three arms and
   both N — the crest's event count at the budget's per-event cost IS the freeze. Flown
   twice (first flight, then regen from a clean tree): spell 424→423 (F1), 1,327→1,317 (F2),
   E 299,138→298,562, burn max 2,585→2,515 ms — the timing-defined quantities (spell
   membership) move ≤ 1%, the law ratios do not move; the table shows the regen's flights
   (the committed `flights.log`).
2. **The lag metric retired.** F4 = F2's scene at rtf 3600: lag prints its ceiling 60.000
   while spell wall (21.9 vs 21.9 s) and E (ratio 1.02) are rtf-independent and the deficit
   scales with want (1.88 ≈ 2 = rtf ratio). The deficit integral is the metric that survives.
3. **N-scaling and the 10⁶/10⁹ arithmetic.** E_spell(3×10⁵)/E_spell(10⁵) = 3.08 against 3.00
   belt bodies — the crest is one first kick per body. 10⁶ **cannot fly here** (build alone
   2,340 B/B = 2.34 GB > the 2-GB process cap), so it is priced from the measured linearity:
   E ≈ 995k, spell **72 s** per 28,141.5-game-s interval. 10⁹: E ≈ 9.95e8, CPU 52,049 s per
   crest = **20.1 h** frozen presented time, or 1.8 cores sustained at rtf 1 (18 at rtf 10,
   **185 at rtf 100**) — 4093's ≥ 19.3 h and 120–190 cores stand, now measured-derived.
4. **The burn arm (the dossier's untested risk, answered and inverted).** Held scans do not
   lengthen the freeze — on the burn the crest's ~300k events resolve inside over-budget
   frames instead: 167–178 frames over 12 ms, p99 465–491 ms, worst 2,515 ms with 49,894 events
   (the worst frames carry 30–52k events at ~50 µs: the frame's whole wall is event work at
   the usual cost), zero deficit on those frames, run truncated at 1,460/2,400 frames,
   memory 705→5,953 MB (19.8 kB/B), held_max 1,701. The budget's stop is per item with `done == 0 → margin 0`
   (the first item of a frame always runs) and margin = recent item cost — tuned for a 1.4-ms
   worst item; on the burn one started item resolves a whole crest wave. The player feels
   2.6-s frames instead of a 22-s slowdown: a different and arguably worse failure, and one
   no presented-time metric can see.
5. **a9d7 confronted** (the checker's missed item): its gold record sentence "the rate is
   trivially affordable" (memory-h-live L314, 3.55×10⁻⁵/B/game-s) is true of the average and
   false of what the player feels at 10⁹ rtf 100 — the crest needs ~185 cores sustained or the
   ~20-h freeze, per interval. The rate sentence needs the crest qualifier.

**Predictions** (`predictions.md`, written before the flights): P2 (the law, ratio ≤ 1.25)
**hit — 1.01–1.02 at all three coast arms**; P4 (metric replaces lag) **hit** (60.000
ceiling, E ratio 1.02, deficit ratio 1.88); P3 ratio **hit** (3.08 ∈ 2.8–3.6) but the 10⁶
absolute missed high (72 s vs 90–110); P1 **half** — the spell closes and is contiguous,
window kicks 343k in range, but E_spell ≈ 299k below my 340–420k (I took the checker's 382k
*total* events as the spell; the spell is the ~299k core, 87% of deficit frames); F2's spell
(1,317–1,327 frames) also fell just under my 1,400–2,000 range. **P5 missed, and the miss is
the finding**: the burn's spell is 0.6–0.7 s against a predicted ≤ 26.5 s — the crest bypasses the
clamp entirely (arm 4). P6 stands with corrected arithmetic (185–187 cores at rtf 100; my ledger
draft first divided by the wrong interval and I fixed it against the definition
cores = CPU·rtf/interval).

**What would make it wrong.** The spell→wall conversion (frames/60) assumes the game's real
pacing changes nothing per frame — per-frame work is budget-capped either way, and the tight
loop's spell frames each ran ~11.9 ms < 16.7 ms, but a paced run would have to confirm it.
The 10⁶/10⁹ numbers extrapolate crest linearity past 3×10⁵ (measured 3.08–3.09 at 3×; the locals'
share shrinks with N, so linearity is conservative). Ĉ is this box's (12db's kick-bench
34.8 µs, the M1 record 43–52.8). The burn mechanism is measured as arithmetic (one frame =
one wave at the usual per-event cost) plus the code's documented escape; *which* item kind
resolves the wave is not profiled (a `--features prof` rerun peaks at 5.9 GB, over the
process cap — not repeated). One seed, one scene (`plane_extra`), shared x86: orders of
magnitude.

**Cost of adoption.** Zero engine code (the patch instruments the example only). Page
corrections: the freeze is now directly measured (the checker bracket resolves), the burn
row is new, a9d7's sentence gets the crest qualifier. The N1 gate window finding of 4093 is
unchanged (20 s at rtf 100 is still 6.6–7.4× pre-crest; ≥ 15k game-s ⇔ ≥ 125 s at rtf 100).
PRINCIPLES: #10 "Measure before claiming" — the freeze was asserted through a saturated
metric, now measured; #12 the smoothness budget is the allocator — and the burn shows its
*binding* is load-bearing; #22 "the simulation decides" — the burn, not the schedule, picks
the failure mode; #2 "Exact means deterministic and reproducible" — spell frames, E and
deficit counts are integers; only Ĉ and the ratios are floats.

**Commands** (≤ 60 s each; regen.sh does all of it in ~4 min warm):

```
cargo build --release -p emergent-universe --example nladder   # patch applied first
B=$CARGO_TARGET_DIR/release/examples/nladder
$B 100000 coast 40 1800   # F1   (F2: 300000 coast 40 1800; F4: 300000 coast 30 3600)
$B 300000 burn 40 1800    # F3 — peaks ~5.9 GB; may be killed under a 2-GB per-process cap
python3 ledger.py flights.log   # the table above, the law ratios, the 10^6/10^9 arithmetic
```

**The lens.** A second author inherits the first checker's numbers as anchors: I predicted
the spell from its 382k total events and landed 27% high — the spell is the crest's core,
not the whole window. And the process cap cut both ways: 10⁶ cannot fly at all (its build
exceeds the cap), while the burn arm *breached* it at 5.9 GB — reported, not repeated — so
the burn's stage attribution stays one `--features prof` run short of named.

✝ truncated by the example's own 55-s guard.
