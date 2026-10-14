Grade: gold

**Abstract.** The a669 "one dial" is refuted on shipped code, and the mint it targeted is
counted. Independently reproduced from a clean tree: default-neutrality is bit-identical
(wave raw-equal; crossing/frame5 wall-times only; patched-default jacobi byte-equal),
34,606 compiles for 34,537 kicks — 1.00 compiles/kick, zero exact-key reuses — the full
dial table, 1,342 refusals at (12,12), Jacobi 30–500×/900–1600× at (20,36)/(16,32).
New arms outside the author's domain: the mint holds at 1.00 at N=10³–10⁴, under L8 burn,
and on seed 2; seed 2 leaks −14% encounters at map-alive dials; the corrected frontier is
(12,16), reuse 0.682 → 3.1×, and its readout panics like every material-reuse grain.
Run ~22–100 is unbought at every grain; the surviving lever is a key that does not walk.
Cost to adopt: the wiring merges default-neutral; the result redirects the kick bottleneck.

**Reasons.**

1. **Reproduction (clean tree, patch applied by me).** Every number in the dossier's
   evidence regenerates: pristine vs patched-default digests identical on the ladder wave
   (raw), crossing and `frame_digest 5` (wall-time brackets only), and `jacobi 6 100 6`
   byte-identical; the shipped stream is exactly `digest d2632de9…, kicks 34537,
   encounters 934, compiles 34606, reused 0`; every dial cell matches — (48,16) reuse
   0.000/1.04, (24,16) 0.136 (kicks 33323, the page's typo note confirmed), (12,12) 0.747
   with refused 1342, (12,24) 0.249 with encounters 928 and refused 0, (12,32) 0.009,
   (16,32) 0.010 with 934; Jacobi arms 16,32 → 4.6e-3 worst (~900–1600×), 20,36 →
   8.0e-5…9.7e-4 (30–500×), 12,24 panics `Space(Range)`. The runner's `regen.sh` log
   matches the dossier line for line.
2. **Predictions.** `predictions.md` (21:46) predates the author's dial runs (21:50+,
   `work/dial_33_20.txt`, `work/jacobi_12_12.txt` survive with earlier mtimes) and the
   dossier (22:02). P1 held (neutrality). P2/P4 failed — as pre-registered expectations of
   the refuted premise — and are reported as failed with the mechanism named; that is the
   experiment working, not a record defect (H0183). P3 held at (12,24) on seed 1 and
   failed at coarse grains, reported.
3. **Adversarial arms (mine, beyond the author's and the first checker's).**
   - *Burn L8* (author flew coast only): mint 1.00 (37,426/37,338); (12,20) map-alive,
     reuse 0.397, encounters −0.05%; (12,12) reuse 0.691 with −2.7% encounters and 422
     refusals — the frontier and its failure reproduce under thrust.
   - *Seed 2*: (12,20) reuse 0.446 but encounters 2406→2052 (**−14.7%**), (12,24) −13.9% —
     the "encounters within ~1%" leak is a seed-1 property; on other seeds the map-alive
     dial moves decisions materially. Strengthens the refutation.
   - *N=10³/10⁴*: mint 1.00; (12,24)/(12,20) reuse 0.264/0.456 and 0.207, map alive.
   - *Shape-degate probe*: **(12,16) is map-alive** (encounters 928, kicks −0.03%, 9
     refusals) at reuse 0.682 — a 3.1× cut, the best measured, correcting the page's
     1.75×; its Jacobi readout panics, as (12,20)'s and (12,24)'s do. (2,16) wrecks the
     scene (kicks −34%, encounters 250, boundaries −38%) with reuse 0.009; (4,16)
     degrades it (encounters 454). The (4,16) jacobi arm does not finish in 120 s
     (baseline 4 s).
   - The operative sentence — no measured dial has material reuse and a working oracle —
     survives the corrected frontier: every grain with reuse ≥ 0.25 either kills the map,
     refuses ~4% of fits, or panics the deep-field readout; the running grains ((16,32),
     (20,36), (24,24) at 1.5e-4…5.7e-6) sit at reuse ≤ 0.04.
4. **Novelty.** Not in docs/HISTORY.md. The nladder page holds a669 as silver and
   "one build from gold" — this run is that build, and it kills the premise: the
   per-population coarser key with flip-gated rebind cannot buy the ~10²× compile cut.
   law.md's standing "Not adopted: a quantized (E, L) memo … a random walk" is now
   *measured* on shipped code in the one form the record left open (the flip gate plus
   the residual carry). The counted mint (1.00 compiles/kick, robust across N, seed,
   thrust) is the new fact the real lever builds on.
5. **Goal fit.** The board's kick bottleneck (75–160 µs vs ~50 ns). PRINCIPLES #9: "A
   failed experiment kills that configuration, never the method" — the configuration
   (coarser key quantum) is dead, the method (delete the compile stream) survives as "a
   key that does not walk" (integer phasor on the binding). #13: the coarser key's walk
   compounds — the Jacobi instrument measured it. #34: the oracles rejected the coarser
   representation as guards should. Gold route: "shows that a premise is wrong", with
   the record regenerating end-to-end and the wiring default-neutral and mergeable.

**Corrections folded into the page** (by me, in place): (a) the best map-alive cut is
3.1× at (12,16), not 1.75× — "encounters 0 at scale ≤ 16" and "the map survives from
scale 20 up" are both wrong as rules (map death is grain-idiosyncratic: (12,16) alive,
(33,20)/(24,16)/(12,12) dead, (2,16)/(4,16) degraded); (b) "~2⁻¹³ relative per rebind,
~600× the replica" is a tail statement, not a median — the coarse arms fit it, the fine
arms sit on ~2⁻²²·⁵ (the replica's own p50: run 1.33 at quantum 2⁻²³, not the 1.001 a
2⁻¹³ constant predicts), and the de-gated (2,16) reuses 0.009 in a wrecked scene. What
stands, and what the refutation rests on: at every map-alive grain the run is ≥10×
shorter than the replica's q/p50 arithmetic ((12,16): predicted ~158, measured 3.1), the
maximum reuse measured anywhere is 0.747 (run 4, map dead), and the map-alive maximum
0.682 panics the readout.

**What the author missed.**
- The grain map was sampled too coarsely in the scale word (24 → 20 → 16 by 4): (12,16)
  is map-alive at 0.682 — the frontier was 2.3× understated, and "scale ≤ 16 dead" was a
  sampling artifact, not a threshold. Nothing below reuse 0.75 was coming anyway, but the
  record should not state a threshold it did not resolve.
- The mechanism was inferred from run lengths only; a direct Δ-key-per-rebind instrument
  (log quantized-word jumps at events) would have separated the shape word's walk from
  the scale word's and the tail from the median — the "~600×" sentence overstates the
  typical rebind (my mixture read: median ≈ the replica's own p50; the tail ≳2⁻¹¹ in
  ~15% of rebinds is what caps coarse grains).
- One seed only, and the seed changes the story's second decimal: on seed 2 the
  map-alive dials move encounters −14%, so the dial is not merely useless, it is
  law-visible — worth one line in any adoption argument.
- The author's own (33,20) probe (encounters 0) sat unreported in `work/` while the page
  said "the map survives from scale 20 up".
