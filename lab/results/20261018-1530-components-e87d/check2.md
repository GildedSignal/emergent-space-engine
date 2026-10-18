Grade: gold

**Abstract.** Claim: the beat-resident pair record (od 1) and the leak-gated skip (od 2) are
dead at the design reach — one belt-quantum kick fully decorrelates the section rotation's due
(flips = armed·(1−armed)·0.88–0.97, dv-independent over 64×, every horizon KH ∈ 10³–10⁶) — and
the float section (72% of the 1,394 ns eval) is kick-stable and cacheable: 416 ns/pair/kick,
3.4× (355 → ~105 cores in 1a29's units). I reproduced every physics mode bit-identically
(timing 1,365–1,372 ns, clock noise). My adversarials extend the kill outside the author's
domain: Full formations (pre-kick due "never", post-kick 45% armed at KH=10⁶) and the thinnest
reachable windows (a=1, σ_e 0.3: law ratio 0.99–1.03, drift/slack 1.17). Adoption: the kill is
free (deletes two design lines); the cache is ~1 day of wiring, exactness-preserving.

**Reasons.**

1. **Reproduction.** Applied `work/patch.diff` to a clean tree, rebuilt, reran every regen
   mode: anchors, control, sweep, slack, stale, anchors-heldout, control-heldout all
   **bit-identical** to the stored outputs. `timing` differs only in clock noise (arm_pair
   1,372 vs 1,365 stored vs 1,394 quoted; cut 3.4–3.5×) — disclosed as orders-of-magnitude on
   a shared Linux box. The instrument is a faithful integer replica of the shipped
   `arm_pair` setup (`rots()` reproduces tier.rs:552–565 at t0=0 exactly).

2. **Predictions.** `predictions.md` (15:41) predates the decisive outputs (15:56). P1
   (dv=0 → 0 flips, bit-identical) held — the negative control is real. P2 held in mechanism
   and the author reported the literal miss honestly; the kh=10³ arm reproduces 1a29's
   5–7×10⁻⁶ regime as the same law at their armed fraction (flips ≈ armed at armed 1.4×10⁻³).
   P3–P5 failed *in the kill direction* and fired the frozen kill criterion — for a
   falsification run that is the result, and it is reported as such.

3. **Adversarials (mine, all outside the author's tested populations).**
   - **Full formations** (identical a, e, ϖ; uniform λ — the author's named unmeasured corner,
     keys fleets): 240,000/240,000 Full sections; pre-kick d = 0 exactly, so the due is
     "never" for every pair (armed 0) — there is no record to store; one quantum kick flips
     4.47×10⁻¹ of pairs on at KH = 10⁶; δw p50 0.39·w per kick, so the cache lever does not
     extend. Kill extends, stronger.
   - **Thinnest reachable windows** (a = 1, σ_e 0.3, 10⁻³ cell, fresh seed 424242): w p50
     3.8×10⁴ ticks — 1a29's "w ≈ 23" is a different unit; in-crate, c₀ ≤ v bounds
     w ≥ ρ/v ≈ 2–4×10⁴ ticks at the design reach, so no δd/w ≈ 10³ class exists. Measured
     there: re-roll ratio 0.99–1.03 (tighter than the author's 0.88–0.97), δd/w ≈ 0.19,
     drift/slack 1.17, leak 0.18 at L = 10⁵. The kill holds by measurement.
   - **Wide attempt** (a = 2, σ_e 0.3): 0 Wide sections in 480,000 — P6's "if ≥ 10% Wide"
     branch never fires at the design reach; still unmeasured but apparently unreachable
     except via near-identical (V,W), which lands in Full instead.

4. **Novelty.** 1a29 (the page's prior best) killed the due-band rule and left od 1 ("a
   representation that stores the beat") and od 2 ("leak-gated slack") as the row's remaining
   certificate hopes. This run kills both (the slack does not exist: 2.7 window widths at
   L = 10⁵ against 2.0 widths of drift per kick; the leak of a certified-safe pair ≈ 2×10⁻³
   per kick-set, flat in 1/8/64 kicks, i.e. the leak *is* the re-roll rate), and adds the
   replacement lever: cache the kick-stable float section, maintain the integers exactly,
   decide with `first_hit` — 3.4× measured. Not previously in the wiki, HISTORY or docs.

5. **Goal fit.** Board live question 2 (encounter work at 10⁹). It shows a premise wrong
   (the row's last two certificate designs), deletes two design lines at zero cost, and
   prices the adoptable constant (3.4× now; the u64 `first_hit` port next; below ~100
   ns/pair/kick the row is candidate density, not certificates). PRINCIPLES #3: the re-roll
   is now *measured* as the surprise rate — the per-kick integer decision is the floor and
   the float rebuild was compute-not-needed. #19: the beat store was the bandaid; the stable
   object is the section integers.

6. **Page.** The proposed page folds the result in faithfully (od 1/od 2 struck through with
   the measured numbers; 1a29's text preserved). I appended one correction note in place:
   the "~10³·w thin class" line is 1a29-unit arithmetic, not an in-crate class (in-crate
   δd/w ≈ 0.2–0.5 at the floor w ≈ 2–4×10⁴ ticks), and the Full-corner flip constant is
   formation-dependent (0.227 on checker 1's formation, 0.447 on mine — same verdict).

**What the author missed.**
- The thin-class claim ("δd/w ≈ 10³") is unit-conditional and unverifiable in the crate; the
  honest statement is that the reachable window floor makes δd/w ≈ 0.2–0.5 everywhere, and
  the kill there rests on drift/slack ≈ 1 and the leak, which I had to measure for them.
- The cache lever's *tail*: p50 δw < 1 tick, but `IDENTITY max δd/w = 1.4×10⁶` in their own
  anchors shows a tail where one kick moves the rotation by a full modulus (period re-quant);
  the 3.4× pricing is a p50 statement and the cache's invalidation rule (element-class
  change) must catch that tail or soundness is p50-only. Unpriced.
- The stale-record probe stops at 64 kicks and L = 10³; the leak's flatness is asserted on
  three points. Minor.
- Wide sections remain wholly unmeasured (0 in every population tried, including mine at
  σ_e 0.3) — a named open corner, not a hole in this kill.
