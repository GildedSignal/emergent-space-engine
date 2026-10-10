# Dossier — 20261010-1947-second-20261010-1920-spacex-cb3f-f79a (second author on 20261010-1920-spacex-cb3f)

**Claim.** The named next probe is done and it is a **kill**: a provably-safe same-doll rejection
pre-filter at the scan seam exists and is bit-identical everywhere tested (9/9 seeds × placements,
plus full 3×10¹⁰ runs), but the only airtight bound rejects 0.07 % of ship-scale pairs — no
deletion; every tightening that would reject measurably misses encounters (three independent
digest breaks recorded), because the player's scan interval (2⁴⁰ doll-time, its ~22 s step)
multiplies any velocity-bound looseness across every ship-scale gap, and the cheap bound (the
binding's own velocity word) sits 8–16× above the true speed once kicks begin. The dense
same-doll cohort the original never grew is now measured: the exact tier is **4.1 µs per pair,
linear in population** (3.02 M pair checks at cohort 200; 794–860 µs per player item vs 57–64 µs
in the star-doll belt; ~4 s per player item at 10⁶ same-doll bodies) — the deletion belongs to the
encounters seam (phase certificates), not a per-pair filter.

**Bottleneck.** The checker's one-experiment-to-gold: the safe ≥10× on the scan intercept, or a
kill. Board line 1 and the top scaling risk. Delivered: the kill, with the frontier measured on
both sides of safety.

**Evidence** (Linux x86 shared runner, orders of magnitude; `work/patch.diff` on top of the
original run's patch; build `CARGO_TARGET_DIR=/home/glmlab/lab-target-3 cargo build --release -p
emergent-universe --example spacex_probe`):

    T=/home/glmlab/lab-target-3/release/examples/spacex_probe
    ESPACEX_NOCACHE=1 $T 200 7 30000000000 1 0        # baseline: digest d4413b80… = the original dossier's, the record regenerates
    ESPACEX_NOCACHE=1 $T 200 7 30000000000 1 1        # dense home-doll cohort, filter off (66 s; also place 2: 105 s)
    ESPACEX_NOCACHE=1 ESPACEX_PREFILTER=1 $T 200 7 30000000000 1 1   # filter on: same digest, 0.07–9 % rejected
    # zero-miss matrix (this exact loop, seeds 7/42/2026 × places 1/2/3, 5e8 ticks): 9/9 IDENTICAL (work/final-matrix.txt)

1. **The record regenerates.** Rebuilt from the patch on the same base commit (a838a28): baseline
   digest `d4413b80…` bit-identical to the original dossier; scan 31 %, 64 µs/item (shared-box
   noise on the original's 57 µs).
2. **The missing experiment: the exact tier grown.** Cohort 200 in the player's own doll
   (placement 1: annulus at 1.5–1.7 Home radii; 2: co-radial at 1.08–1.12; 3: wide, e ≤ 0.3):
   3 019 749 same-doll pair checks at **4.07–4.44 µs/pair**; player scan 794–860 µs/item (10–19 %
   of settles of 66–111 s). Co-radial (place 2): **611 777 real contacts** — the tier is not
   hypothetical. The original's "~4 µs/pair" intercept and the checker's "10⁶ same-doll ⇒ ~4
   s/item" wall are both confirmed by direct growth.
3. **The airtight pre-filter is safe and useless.** Envelope: orbit turning points from the
   tube's own key (apoapsis = periapsis/k, Q48), position margin = 2 word quanta + the exact
   residual integers; velocity bound structural: i64 word ≤ 2⁶⁴·2^vexp × exact shear growth
   (turn coefficients a, b over 2⁶⁴) + exact residual integers. Digests identical on 9/9
   matrix cells and all 3×10¹⁰ runs. Rejections: **36/50 722 (0.07 %)** at 5e8; 0 at 3×10¹⁰
   seed 7. It rejects only moon-scale gaps (6×10¹⁰ doll units), never ship-scale (≤10⁹).
4. **The frontier, measured on the unsafe side.** Tightening vmax to the word *convention*
   (2⁶¹·2^vexp, "60-bit words" per `choose_units`/`word_for`): rejects 92 % on the separated
   annulus but **misses encounters** — seed 7 place 1: digest `8c84c079…` ≠ `bf4dea59…`,
   encounters 40→23. Re-adding the exact turn/residual corrections (2⁶¹ again): safe on seed 7
   short runs, **still misses** at seeds 42 and 2026 place 1 (`cad102e0…`, `a27c2800…` ≠ off) —
   the word convention does not survive kicks. Measured looseness: belt bindings carry
   vexp −74/−75 ⇒ vmax 1.2×10⁻⁴–6.1×10⁻⁵ against true β ≈ 2.8×10⁻⁵, and h ≈ 2⁴⁰ doll-time, so
   slack ≈ (1.5×10⁻⁴)·2⁴⁰ ≈ 1.7×10⁸ erases every ship-scale gap (belt gaps 0.7–1×10⁹ survive
   only the 8.7 % widest). The safe/tight boundary sits exactly where the decode's information
   (velocity at t) begins.
5. **Co-radial overhead.** Where it cannot reject (place 2), the filter *costs* 8 % of the scan
   (859 vs 794 µs/item) — a per-pair filter that does not delete must not ship.

**Predictions** ([predictions.md](predictions.md)): Q1 safety held for the final bound but I
predicted it for the word-convention bound too, which then broke twice — reported as the frontier,
not as success. Q2 failed (0.07 % not ≥99 %, no 10×). Q3 held (0.07 % < 10 %, +8 % < 1.2×). Q4
failed (0.07 % not 10–60 %). Q5 (clone-free doll test, `doll_at`) — built, never A/B-timed: a
lead, not a result. Q6 held and is now measured, not argued.

**What would make it wrong.** A per-pair bound I did not think of that is both airtight and
~2× the true velocity (e.g. a binding-carried exact vmax written at bind time — that is a law
change, not a scan change); or the M1's timing shifting the 4 µs/pair by 2× (shape unchanged).
The kill is about the scan seam's representation, not about radial envelopes in general: a
*windowed* certificate paid once per binding (cached decode + acceleration ball) was not tried
and remains open, but it is the encounters seam's design, not this one.

**Cost of adopting.** Zero: nothing ships. The ledger gains the measured wall (4.1 µs ×
same-doll population per player item, ~4 s/item at 10⁶) and the negative result: do not spend a
rung on per-pair scan pre-filters; the phase-neighbour certificate (6 Oct gold) is the only
deletion path for the dense tier.

**Fit with PRINCIPLES.** "A failed experiment kills that configuration, never the method" (P9) —
the killed configuration is the per-pair pre-filter at the scan, with the numbers that kill it.
"Rough first, refine when a certificate could break" (P21) — the rough tier was built, and the
measurement shows where its certificate breaks (velocity looseness × the 22 s interval).
"Measure before claiming" (P10) — three of my own predictions failed and are reported as failed.

**The lens.** The second-author brief (make the record regenerate; run the named experiment)
pushed me to deliver the kill's evidence, and the two digest breaks were found only because the
brief demanded held-out seeds; my first two "safe" bounds were not. What I may have missed: the
untested `doll_at` (the foreign-doll slope, 33 ns/body — the original's other term) is one
timing run away from a real, safe deletion, and I ran out of window before measuring it.
