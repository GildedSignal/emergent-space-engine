Grade: silver

**Abstract.** The run prices fe85's open direction 2 (the per-band u_k refit) on the frozen
r1 sampler: the one-law form (each visited band's constant = geometric mean of the
u-extremes the orbit attains there; exactly the frozen centre for crossed bands) lifts
precession to 256/256 at every m ∈ {8,16,32} (frozen: 250/256 at m=8, 255/256 at m=16) at
−25% median advance error (1.45e-4 vs 1.83e-4), at the measured price of a canon change
(256/256 turning-band constants move; the contained-only form never fires on this draw).
Every number reproduces exactly (11 s, clean tree). Checker held-out: a fresh 1024-seed
draw replicates the win (m=16 GEO 1024/1024 on both channels; m=8 prec 0.999 vs frozen
0.955, period 0.976 — m=8 stays unlicensed); the near-circular limit holds (e=1e-4: GEO
worst 1.7e-8 vs frozen 3.0e-2; 96/96 vs 61/96 prec). Adoption: canon reset plus an r1
re-freeze naming the band-constant rule; the integer form is unpriced.

## Reasons

1. **Reproduction: exact.** `regen.sh` in a clean temp tree, 11 s: every sampler, circle,
   strong-field, ISCO, capture and repeat number matches `run_console.txt` and
   `report.json` line for line. `work/patch.diff` is empty (script-only run, no tree
   edits). The oracle ports are faithful in form to the shipped
   `xtask/src/gr_oracle.rs` / `gr_oracle_extended.rs` (same formulas, same K−π/2 series,
   same Darwin-quadrature refinement), and the frozen arm reproduces fe85's published
   m=16 median (1.83e-4) with the published pass pattern (255/256 at m=16, failures
   concentrating at m=8) — the instrument is calibrated on the record.
2. **Held-out predictions.** `predictions.md` (mtime 29 min before dossier/script) is
   genuine pre-registration: seven predictions, a kill bar, and one honestly-flagged
   uncertain call (P7). P3 and P6 held exactly, including the uncertain branch (m=8
   period stays below 0.99). P1 partially (draw detail, disclosed). P2, P4, P5 and the
   kill bar are **undecided by the author's own instrument** — disclosed in the dossier,
   the wiki page and the claim itself. That honesty is correct, but it means the
   mechanism's decisive channel (the deterministic near-circular family, fe85's measured
   weak flank) was never measured by the author.
3. **Attacks (this check, on the author's unmodified module).**
   - *Fresh draw, N=1024, different RNG seed (outside the tested range):* m=16 GEO
     1024/1024 on precession **and** period (frozen 1018/1024 both), median 1.49e-4 vs
     1.96e-4 (−24%). m=8: GEO prec 1023/1024 vs frozen 978/1024 (=0.955, below the frozen
     0.99 bar), but GEO period 999/1024 = 0.976 < 0.99 — m=8 stays unlicensed, exactly as
     the dossier says. Crossings identical across arms (16/32 median); prograde holds
     (min advance ≈ 1.9e-2 > 0 in every arm); one seed throws in all arms equally
     (instrument).
   - *Near-circular family (m=16, e ∈ {1e-4, 1e-3, 1e-2, 3e-2}, 24 p per e) — the
     refit's target family, the author's broken channel:* GEO worst advance error 1.66e-8
     at e=1e-4 vs frozen 3.0e-2 (six orders; the e→0 limit of P2 holds without needing
     the broken e=0 row); 1.4e-4 at e=1e-3; 2.0e-3 at e=1e-2. Family pass: GEO 96/96
     prec, 96/96 period vs frozen 61/96, 75/96; CONT 90/96, 93/96. **New caveat the
     author missed:** at e≈0.03 (radial excursion ≈ band width, straddling) GEO is
     mildly *worse* than frozen (worst 3.1e-3 vs 2.2e-3) — the win is not uniform in e,
     though both sit far inside the 1% bar.
   - *Moderate strong-field rows outside the author's NaN set* (u_apo < 1/6 so the
     hyperbolic path never engages: (9.5,0.5), (12,0.7), (30,0.9), (8,0.15), (50,0.85)):
     all arms 1.6e-3…2.3e-4 advance, 3.7e-5…6.6e-4 period — no GEO regression beyond
     noise; the strong-field hole is confined to r_peri < 6 rows.
   - *Fixed-point audit (352 seeds):* converges in 3–5 rounds, zero 12-round-cap hits,
     re-walk with converged constants bit-stable. The "self-consistent fixed point"
     claim holds empirically; the author asserted but never measured it.
   - *m=64 (next doubling):* GEO 9.9e-6 vs frozen 1.1e-5 median, crossings 137 < 512 —
     pattern continues; the relative gain shrinks per doubling (28%→24%→13%→11%),
     consistent with a first-order-cancelling representative-point correction.
4. **Novelty.** fe85's wiki page open direction 2 names the per-orbit u_k refit and says
   "needs one measured row to price"; this run is that row, plus the one-law form
   (frozen-equal on crossed bands, no regime branch) and the canon-change price. No
   HISTORY.md entry covers it. Not a repetition: it changes the page's current best
   (deletes the "m=32 minimum" premise through the precession channel, m=16 becomes
   margin-free on both channels on both draws).
5. **The page.** The proposed `wiki/binet-cells.md` is faithful to the evidence: numbers
   match, limits are named as instrument-broken, the kill bar is reported undecided, m=8
   is not claimed licensed. I added the checker's held-out rows (fresh draw, near-circular
   limit, the e≈0.03 reversal) in place.
6. **Goal fit.** Bottleneck 0 (the representation): it fixes the representative point of
   the primary in-cell law, one m-doubling of headroom (half the crossings at equal
   behaviour). PRINCIPLES 19: "a fix signals the wrong representation" — the band-centre
   point was the wrong representative point, and the refit derives it from the orbit's
   own attained range instead of adding a regime branch (principle 4). Honest pricing of
   what it costs (canon reset, principle 13's spirit).

**Why not gold.** The author's own decisive channel never ran: the kill bar is undecided,
not passed, and four of seven instrument channels (circles, hyperbolic strong field,
capture, ISCO) are broken in the run's own walker — the lab's rule from the premise
red-team applies: claims must be measured on the design's cheap path, and the graded path
is the r1 rung, which has still never been graded (open direction 1). Adoption is more
than one step: canon change + a re-freeze that must name the band-constant rule + an
unpriced integer form of the fixed point. My check closes part of the gap (the
near-circular limit and draw-independence), which is what makes the core claim stand.

## The one experiment to gold

Re-freeze r1 (m ∈ {16, 32}) with the band-constant rule **named in the freeze** (frozen
centre vs one-law refit), the deterministic worst-offset e=0 circle rows and the
hyperbolic strong-field rows measured on a working walker (fe85's branch code or the
shipped harness — both exist), and run it for grade at the full frozen case set. Expected
from this check's limit row: the refit arm passes the circle family; the frozen arm fails
it (3.0e-2 first order). One rung execution decides gold or kill.

## What the author missed

- The near-circular family was measurable with their own instrument one loop away
  (small nonzero e); treating the broken e=0 row as closing the family left the
  mechanism's best evidence on the table.
- The e≈0.03 straddle reversal (GEO mildly worse than frozen): small, inside bars, but
  the one place the one-law form overcorrects — relevant when the freeze is written.
- "CONT never fired" is a property of their draw: on my 1024-seed draw it fires 17–35
  times and lifts m=8 precession (+23 seeds), still below the bar. The conclusion
  (contained-only carries no win) stands, the absolute ("never") does not.
- The m=8 period failures are asserted as "the second-order tail" but never localized
  (which seeds, which band); the fresh draw says the same 2.4% fails under GEO.
- The sampler-draw question (their dead first line consumes one RNG draw; m=16 median
  matches fe85 exactly while m=8 pass counts differ by 2–7 seeds) is unresolved; the
  comparative claim is insensitive (same instrument, both arms), but a rung freeze must
  pin the draw order first.
