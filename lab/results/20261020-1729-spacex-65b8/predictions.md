# Predictions — 20261020-1729-spacex-65b8 (written before the decisive runs)

The mint-knots page carries a 100x conflict between two published headline numbers for
"the traversed fraction" of a minted knot table: 624a (rtf 100, fleet) says cycles walk a
median 14% of panels; 1991 (rtf 1, m400) says cycles walk 0.04-0.23% of the arc. My
instrument measures BOTH quantities (panel landings split quad/probe, and the psi spread
of post-mint quadrature) in one binary, one run, plus each row's cadence
(next-kick interval / period, closed from the bench loop).

- **P1 (the floor):** on 624a's arm (m400, rtf 100, seed 1, 30 s) my `panels_frac`
  (quad+probe panels / knots, closest to their landing count) reproduces their cycles
  median 10-25%, but `quad_frac` (panels where the node() arithmetic actually ran) is
  dominated by the 1/n table-size floor (one bracket panel per read, median table small)
  and `walk_frac` (psi spread / span, 1991's quantity) is <= 2%. The 14% is mostly the
  floor plus bisection probe scatter, not arc walking.
- **P2 (both numbers, same run):** on the default arm (seed 1, 10 s) I reproduce BOTH
  published numbers simultaneously: panels_frac ~15-25% (624a's "20%") AND walk_frac
  ~0.1-0.5% (1991's "0.23%"). If instead walk_frac ~ panels_frac, the conflict is real
  dynamics and the adjudication flips to 1991 being wrong.
- **P3 (rtf is not a cadence dial):** mint counts scale ~100x from rtf 1 to rtf 100 on
  the same m400 scene, but the interval/period distribution and the per-mint medians
  (walk, quad) are unchanged (within 2x). If per-mint coverage changes ~100x with rtf,
  then rtf IS a cadence dial and the conflict is a confound, not an instrument
  difference.
- **P4 (the cadence law / belt fork):** across cadence bins, walk_median rises with
  interval/period; the bench contains no closed row at interval >= period (level 0 /
  the belt cadence), because the nested split rebinds members 8-64x per period. The
  measured walk(cadence) form answers the page's belt fork by extrapolation: at one
  kick per period a read-per-frame body walks ~its whole table, so a lazy compile is
  belt-neutral exactly there; below that, waste tracks (1 - interval share).
- **P5 (never-read):** mints with zero post-mint quadrature (`never_quad`) are 50-90%
  on the m400 arms; `never_any` (no panel traffic at all, probes included) is lower by
  the probe scatter. ptr_reuse = 0 (kick keys never recur, so no address reuse).

Kill criterion for my own claim: if `walk_frac` on 624a's arm is ~14% (i.e. the
published number was a true walk), my P1 is wrong, the two runs measured the same
thing, and the conflict is in the dynamics (rtf/cadence) — the page then keeps 624a's
pricing and 1991's kill argument must be re-examined.
