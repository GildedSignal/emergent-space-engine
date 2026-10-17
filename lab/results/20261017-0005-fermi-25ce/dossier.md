# Dossier — 20261017-0005-fermi-25ce (Fermi lens)

## Claim

**The 10⁹ schedule ("who is due") costs no per-body bytes — but only because it chooses
the store class: a per-body record store (the 21–40-bit phase-locked class) laid out
(doll, step, hash-phase-class)-major IS its own calendar, stable between kicks (a body's
next due = last + interval re-enters the same class), with the stagger quantized onto the
class grid; every other form busts or dies — explicit entries 7.1–9.1 GB, a due-ring index
5.6 GB on top of the program store (Shannon floor of the ordering alone: log₂(N!) = 3.6 GB),
and per-frame rescans 0.13–23 s against a 16.7-ms frame — so the bijective 0.126–2.4-bit
program class, which cannot be enumerated by due at any of those prices, is excluded by the
calendar, not by its own bytes.** The class dial saturates at K ≈ frames-per-interval
(~1.4×10⁵–4.4×10⁵ classes; ≤ 0.5–1.8 MB of cursors, ×100 fan-out ≤ 3% of 6 GB); beyond it
nothing improves (measured: K=10F ≡ K=100F), and at 10⁹-scale loads the Poisson
concentration is max/μ ≈ 1.05 (measured law confirmed at μ=7.4: 2.84×, exactly
1+√(2lnF/μ)). The board's "the queue" first-break candidate is dead: the queue was never
the wall — the store class was.

## Bottleneck

Board focus item 1 ("which term breaks first as the plane grows — per-frame walks, rekey,
**the queue**, memory per live body") and item 5's memory row. The memory ledger closed on
program classes as if interchangeable ("every measured program class fits", e7ef); no page
prices the schedule structure that must fire 4.4×10³–3.55×10⁴ events/game-s at 10⁹ (frame-cost
priced the live queue's CPU; scan-queue is the player's scan). Gain: deletes a whole
per-body structure before it is built (the wheel/heap the shipped live plane implies), and
fixes one law choice (quantize the adopted f82a stagger) at wiring time instead of after a
10⁹-scale surprise.

## Evidence

All from `fermi_calendar.py` (numpy replica on cited constants; ≤ 2 s; this shared x86
box, 8 vCPU — orders of magnitude only):

| Form | At 10⁹ | Verdict |
|---|---|---|
| (a) explicit per-body entries (id 30b + due 16–24b + link 3–27b) | 7.1–9.1 GB | **busts 6–8 GB alone** |
| (b) due-ordered ring: index on top of program store | 5.62 GB + store | busts (8–11 GB) |
| (b') ring with program inlined, 36–55 b/body | 4.5–6.9 GB | busts or destroys birth classes; Shannon floor of the ordering alone **3.6 GB** (log₂ N!) |
| (c) per-frame rescan of the store | measured 21.9–23.2 ns/body (10⁶–10⁷, flat); 10⁹ pass 22 s; **bandwidth floor 0.13 s = 8 frames** | dead by 8–1,300× |
| (d) class-major per-body store + cursors | 2.6–5.0 GB (the measured 21–40-bit class, e7ef) + 0.5–1.8 MB cursors | **the only form that fits** |

Class dial (sim, N=10⁶, one composed interval of 135,079 frames, μ=7.4 ev/frame):
comb K=1 → 10⁶ in one frame (control FAILS as it must; the measured comb/crest, 4c22/9e75);
K=512 → class concentration max/mean **1.06×** (pre-registered ≤1.25 held) but 512 classes
on 135k frames → carrying frames see 280× μ (FAILS — the count must reach ~frames);
K=F/10 → 13.0× μ; K=10F → **2.84× μ = 1+√(2·lnF/μ) exactly**; K=100F identical
(**saturation**); at μ=7,403 (10⁹ composed) the same law gives **1.05×**. Cursors:
4 B × K; K spans F=1.35×10⁵ to N/bar=4.4×10⁵ → 0.5–1.8 MB (0.01–0.03% of 6 GB; ×100
doll/step/cell fan-out ≤ 3%).

Ledger cross-check (P4, independent): shipped 3.55×10⁻⁵ ev/B/gs × 10⁹ × rtf 100 ×
29.3 µs = **104.0 M1 cores** (e7ef: 104–178); composed 4.44×10⁻⁶ → **13.0** (98cb: 13.2;
ratio 0.985); rate×interval = 0.999–1.000 ev/B/interval ✓. The cadence term — not the
calendar — is the 3.25×-over-bar residual (7,403 vs 2,275 ev/frame), i.e. the standing
5.1/4-core overage, unchanged by this run.

Stability (the layout's reason): hash-class(id) is id-derived and fixed; `aligned`'s
interval law re-anchors to the absolute grid, so next = last + interval re-enters the same
class — the bulk never re-keys; only kicked bodies move (they are live at the kick site;
the measured rekey tax 43–60 ns/body, 115e, applies to the hot set 1.3–2.7×10⁴, ba64/cbc5,
~1 ms/interval — noise). [The `aligned`-vs-`chain` reading is from the wiki's measured
record (4c22/4fa8), not re-read in code; chain from previous event is grid+phase for a
never-kicked body, so the claim holds under both interval laws.]

Reproduce: `cd lab/results/20261017-0005-fermi-25ce && python3 fermi_calendar.py` (2 s;
`regen.sh` runs the same).

## Predictions

`predictions.md`, written before the run. What held: P2's comb control fails, class
concentration ≤1.25× at class size ~2,000 (1.06×), cursor memory ≤0.03–3% (P3), P4's
re-derivation within 1.15× (0.985). What missed, reported as missed: **P1's ns/body band
(1–5) — measured 21.9–23.2** on the numpy path (temporaries; a tuned SIMD pass is the
band's referent) — the kill it fed is strengthened, not weakened (dead by ≥8 frames at the
bandwidth floor even granting the band); **P2's "≤1.25× at the working point" — measured
2.84× at the sim's μ=7.4**, because the pre-registered figure was calibrated for 10⁹-scale
μ; the underlying law (max/μ = 1+√(2lnF/μ)) is confirmed exactly and gives 1.05× at scale.
The pre-registered 512-class arm also exposed a framing error in my own prediction: the
dial is set by frames-per-interval, not by N/budget alone.

## What would make it wrong

- The bulk's next-due is NOT derivable from (id, cell constants, grid) — e.g. if the
  interval law needs carried per-body state after all (CHAINED offsets that don't
  re-anchor). Then form (d) dies with the rest and the calendar is a real 10⁹ wall; the
  falsifier is one read of the shipped interval law against a kicked-then-demoted body.
- Quantized classes change fire times by up to interval/K ≈ 0.1 game-s ≪ the 1.67-gs
  frame: sub-frame, same legality class as f82a's stagger (itself an unflown-through-B-gates
  law change, 98cb) — but that is an argument, not a flight; B13/B14-class gates unflown.
- The 21–40-bit class's 2.6–5.0 GB at 10⁹ leaves 1–3.4 GB for everything else (view, hot
  set, cursors, OS): if the wiring's measured per-body price is above ~40 bits, the
  class-major store busts with it — this run prices the schedule's share (0.5–1.8 MB), not
  the store's.

## Cost of adopting, and fit with PRINCIPLES

Cost: one law line (quantize the stagger: `hash(id) >> shift` for the class, the residual
bits for within-class order), the compact store wired class-major instead of birth-major
(a layout choice at wiring, before anything is built), and the bijective-program belt class
demoted to archival/replay duty. PRINCIPLES #6 "Store the generator, not the generated"
survives with a boundary: the generator is the *birth* program; the *standing* store at 10⁹
must be per-body (the 21–40-bit class) or it cannot be scheduled. #17 "the best part is no
part": the calendar is the deleted part — the store's own order is the schedule. #26: the
layout-as-calendar is Crash-Bandicoot causal-order layout (bottleneck 0's own lead).

## The lens

Fermi's blind spots here: the estimate loves clean forms (a/b/c/d) and nearly missed that
form (d)'s cursors answer WHEN, not WHO — membership is the real price, and it is what
forces the store-class choice (found while writing the dossier, not while estimating).
The 8-vCPU shared box's ns/body is an upper bound; the M1 re-measures. No flight: the
plane does not link on Linux unpatched (`proc_pid_rusage`), and this question's numbers are
bytes and counts, which the replica carries exactly.
