# Dossier — 20261018-1126-library-686f (library lens)

**Claim.** Composed from the levers measured since ladder.txt froze the breaks (14 Oct), the
10⁷ rung of the N ladder is decided by arithmetic before it flies: the frame terms stay fixed
(exponent 0.00 since 0f112b89) and the rung's walls reorder to **the birth protocol first
(25.5 GB, 295 s shipped — unrunnable), the belt's first wave second (28–56× the frame budget;
it passes only with the full RES delete, 0.2–0.3×), and nothing else at 10⁷** — while at 10⁹
the same pair fails the wave 18–31× in one doll and leaves the steady spared stream at
0.61–1.02 s/s against the 0.72 single-thread budget, so the 10⁹ row's levers are the doll
partition/stagger and threads, not any per-kick term. Five verbatim library lessons hold the
five decisions (birth dose, subtraction over the metronome, survival sizing at the wave,
wiring-in-the-plane, directness for the rung's four unmeasured terms).

**Bottleneck.** The board's #1 (bodies in the flyable engine: the furthest gap). The lab-run
letter asked "which term breaks first as the plane grows (per-frame walks, rekey, the queue,
memory per live body)"; every term has since been measured on its own page, and no run had
recomposed the rung order with the levers landed. Expected gain: the 10⁷ rung becomes a
protocol+wiring decision (lazy birth + compact row + RES arm) with margins known in advance,
deleting the "which wall first" search; the 10⁹ CPU question moves off the belt row entirely
(0.6–1.0 s/s spared stream) to the partition/thread decision.

**Evidence** (composition on page-cited constants; every number regenerates, ~30 s:

    cd lab/results/20261018-1126-library-686f && ./regen.sh        # fetches Readwise fresh, runs both scripts

`compose_rung.py` on constants cited to ladder.txt (shipped artifact), nladder.md,
kick-cadence.md (3570), promotion.md (cbc5/8792/c4d3), memory plateau (b30b via 6793),
HANDOFF's scoreboard bits, e29c's frozen T* bars; calibration anchor the flown 5×10⁵ wave
point (composed 15.0 s vs flown "~15 s", exact). Table (wave = first-kick work over the
1,483-gs arrival window as a multiple of the window's 10.7-s engine budget):

    arm                    N    birth GB  build s  wave×bud   live GB  steady s/s   +re-kick
    shipped                1e6      2.55       30    2.8-4.7     5.06  0.108-0.181    <1e-4
    shipped                1e7     25.50      295   28.1-47.2   50.60  1.080-1.814    <1e-4
    lazy birth only        1e7      0.16        0   32.3-55.8   50.60  1.080-1.814    <1e-4
    lazy + ES_SECULAR      1e7      0.16        0   19.8-34.3   31.13  0.664-1.116    <1e-4
    lazy + RES             1e7      0.16        0    0.2-0.3     0.29  0.006-0.010    <1e-4
    lazy + RES             1e9     15.75        0   18.1-31.4   28.43  0.607-1.019   <1e-4

- Shipped steady rows already assume the boundary skip (16ec/49e9, digest-neutral) lands;
  without it, double them. Lazy "birth GB" uses the solo worst 126 bits (the wired row's own
  bytes are one of the rung's four measurements). Live GB = spared bodies at the 5,060-B
  plateau if nothing demotes; the dwell dial only shrinks it.
- The add-back never binds: one sparse re-kick per body per T* ≥ 3.37×10⁷ gs (e29c's frozen
  bars, conservative arm held constant in N) is < 10⁻⁴ s/s at every N and literally zero
  inside any flyable horizon — Musk's 10% add-back budget is idle by ≥ 3 orders (dc8f's
  prediction 1, re-derived on the honest rate; the naive 0.28%-of-stream reading would say
  0.33 s/s at 10⁹ and is wrong by 4 orders — it treats a horizon-crossing count as a rate).

**The five lessons** (all 7 quote fragments byte-identical against a fresh 4,590-highlight
export, `quote_check.py`):
1. **Ferriss, The 4-Hour Body — the MED.** "The minimum effective dose (MED) is defined
   simply: the smallest dose that will produce a desired outcome." / "Anything beyond the
   MED is wasteful. … Boiled is boiled." Mechanism: the birth's outcome is a step function
   (bit-for-bit is bit-for-bit). Change: the rung's birth path is the lazy birth (compact row
   + first plan against the sources' tick-0 snapshot; ladder.txt: "bit for bit;
   ladder_digest's 13 cases are the check") — live-at-birth (25.5 GB, 295 s) and
   promote-at-first-item (the wave's compile bill: 4.2–8.6× the window budget on compiles
   alone) are doses beyond the outcome. Test: the 13 ladder_digest cases on a lazy-birth patch.
2. **Taleb, Incerto — subtraction.** "Knowledge is subtractive, not additive—what we
   subtract (reduction by what does not work, what not to do), not what we add (what to do)."
   Mechanism: break 1's open law change reads as cadence tuning (pick a better Δs) but the
   measured lever is subtraction: delete the tide-legal belt's kick stream (RES, 708/712,
   checker-verified bit-identical tail) and the secular generator answers. Change: the arm
   choice for the rung is ES_SECULAR_RES inside the composed law (f134/7fcf), not any Δs
   change. Test: one wave flight (the belt_first protocol) with the composed+RES arm at 10⁶.
3. **Card, Ender's Game — survival first.** "Humanity does not ask us to be happy. It merely
   asks us to be brilliant on its behalf. Survival first, then happiness as we can manage
   it." Mechanism: ruin asymmetry — the wave is the one batch that kills the machine (28–56×
   budget unpruned; 31 GB resident at ES_SECULAR), while the quiet stream is 100× under.
   Change: the compact-row wiring's two dials (the delete's legality coverage at birth, the
   dwell ceiling) freeze against the WAVE arithmetic, never the mean stream; at 10⁹ the wave
   (18–31×) is the named survival case for the doll partition/stagger decision. Test: the
   10⁷ wave flight with resident-memory tracking (16ec's pinned-cut harness).
4. **Isaacson, Elon Musk — designers feel the pain.** "Separating the design of a product
   from its engineering was a recipe for dysfunction. Designers had to feel the immediate
   pain if something they devised was hard to engineer." Mechanism: the compact store's solo
   numbers (21–126 bits) never met the engine's frame; the pains live only in the wiring —
   the wave's promotion bill (4.45–9.2 µs each) and the legality flag that must fire from
   the compact row BEFORE any kick (if it is post-kick, the wave is the ruin again).
   Change: the 10⁷ rung flies b29a's smallest honest wiring (the belt's event on the compact
   row and back) inside the plane, not the store's bench. Test: the rung itself.
5. **Young, Ultralearning — directness.** "Directness is the practice of learning by
   directly doing the thing you want to learn." / "Passive learning creates knowledge.
   Active practice creates skill." Mechanism: this composition is passive knowledge — it
   fixes order and margins; only the flight fixes four numbers. Change: the rung's
   measurement list is exactly those four: (a) the legality-at-birth firing on the compact
   row, (b) the wave's max arrivals per frame (the batch peak, realization-dependent),
   (c) the wired row's real bytes vs the solo 21–126, (d) dwell under the wave (the cliff's
   burst structure, never flown with the wave). Nothing else needs the flight.

**Predictions.** `predictions.md`, all six held: P1 three walls at once (25.5 GB / 295 s /
1.08–1.81 s/s); P2 lazy-only stays a ruin (compile share alone 4.2–8.6×; total 32–56×); P3
every term ≥ 3× margin (0.2–0.3×, 0.29 GB, 0.006–0.010 s/s, 0.16 GB); P4 ES_SECULAR-only
fails the wave 19.8–34.3× with the steady stream borderline (0.66–1.12); P5 at 10⁹ the wave
fails 18–31× and the steady spared stream is NOT cleared on one thread (0.61–1.02 of 0.72);
P6 quotes 7/7 byte-identical and the 10⁶ sanity row reproduces the flown record (N1 = 10⁶
passed on the 20-s rung — 2.55 GB, 30 s, 0.11–0.18 s/s — with the wave lags-but-frames-hold
verdict, matching the flown 5×10⁵ point and ladder.txt's "10⁶: twice that").

**What would make it wrong.** Any row contradicting a flown number by > 2× (none does: the
anchor is exact). The named assumptions, each a rung measurement: (i) the delete's legality
is birth-derivable from the compact row (the tide bound needs the body's elements and the
sources' snapshot — true in principle, unflown on the row); (ii) the wave's arrival window
stays ~1,483 gs at 10⁷ (the spread is light-distance set; its per-frame PEAK is
realization-dependent — measurement (b)); (iii) 10⁷ stays one doll (the root) — the 10⁹ row
is per-doll and the multi-doll wave spread is the 10⁹ rung's own term; (iv) the solo 126-bit
worst stands in for the wired row until measured. **Cost of adopting:** none beyond the two
adoptions already digest-verified (the composed law f134/7fcf; the skip 16ec/49e9) plus the
lazy-birth patch and the compact-row wiring — every one of them already on a page as the
next step; the composition only fixes their ORDER and their margins. **Fit with PRINCIPLES:**
"Less is more. The cheapest compute is compute not done" (the RES stream is exactly compute
not done); "No work for no reason, so no ticks … you don't advance a ship tick by tick" (the
deleted 99.4% is the ticks not advanced); "Iteration speed. … Run the simplest falsifying
test first" (the rung's list shrinks to four numbers); the player remains the only wildcard
(nothing here touches observables).

**The lens.** A composition run never touches shipped code: its numbers are the pages'
numbers, so it inherits any page's error (the memo artifact's lesson: agreement is not
independence — my table agrees with ladder.txt because it is built from it; the only
independent check inside it is the anchor, exact, and the 10⁶ sanity row). The library lens
buys decisions, not measurements: if the integrator wants the four numbers, they cost one
flight, and this run's honest limit is that it cannot price the wiring's own overhead. The
60-s rung limit and the 1-thread budget were requirements I did not question (threads buy
4×, the wave is 18–56× — they change nothing here, but they will at 10⁹'s steady row).
