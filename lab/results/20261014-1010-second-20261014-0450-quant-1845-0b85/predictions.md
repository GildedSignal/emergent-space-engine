# Predictions (written before the decisive arms; the build is still warming)

The experiment: the warm-start gallop (`ES_IMP_WARM`, this run's patch) against the shipped cold
bisection, one binary, A/B by env. The prior run (quant-1845, silver) priced the deletion by
arithmetic; the checker's named experiment to gold is to build it, count the fallbacks, and prove
digest identity on the battle arms, flying pace and 16,000 members.

Numbers I have not tuned on (my only smoke arm is m400/s3/rtf1, identity-class):

- **P1 (identity).** Digest(warm-on) == Digest(warm-off), bit-identical, at every arm: m4000/s3,
  m1500/s3, m4000/s7 (rtf 1, 8 s), m400/s3 rtf 100 (flying), m16000/s3 (rtf 1); and the patched
  plain build (prof off, warm on) == the pristine HEAD build at m400/s3, m1500/s3, m16000/s3.
  This is the load-bearing prediction: the gallop is bracket-independent on a monotone predicate,
  so any digest difference kills the construction, not the tuning.
- **P2 (search cost).** Readouts per search (K_PING/K_IMP) falls from the cold ~25–27 to **≤ 8**
  at the battle arms.
- **P3 (fallbacks).** K_FB/K_WARM **< 25%** at m4000/s3 and m1500/s3. The named risk: near-apoapsis
  kicks on shallow-dipping tubes move the crash tick far; if that dominates, the fallback rate is
  high and the win dies. **Kill criterion: > 50% fallbacks, or a kick saving < 20%, kills the lever.**
- **P4 (kick).** The fired kick at m4000/s3 falls from the prior run's 254 µs to **130–180 µs**
  (point guess ~150): the bisection's 45% share mostly goes, the bind (46%) stays.
- **P5 (share).** K_IMP falls to **≤ 20%** of the fired kick at the battle arms.
- **P6 (hand-outs).** Hand-out µs (H_BIND, H_REPLAN) **unchanged within ±10%** at every arm: a
  leaver has no retired tube, so the hand-out's first search stays cold (the honest half of the
  prior run's price).
- **P7 (flying pace).** At m400/s3/rtf 100 the fired kick falls **≥ 40%** (the bisection was 57%
  of a 192 µs kick there, and K_IMP/kicks was 1.01: every kick, no other callers).
- **P8 (16,000 members).** The overflow regime (no fired kicks) leaves the hand-out as the only
  searcher; its µs unchanged, digest identical, K_WARM ≈ small (only kick/boundary rebinds carry
  a warm tick).

## Addendum (written before the clean-base arms, after the HEAD arms)

The HEAD arms overturned the premise: at HEAD the fired kick is 13–19 µs and rebinds twice
(K_REST = 2 of 1032 kicks at m4000/s3) — the crash-tick search now lives only in the hand-out's
replan (K_IMP = 1032 of 2041 hand-outs, ~118 µs each, inside H_REPLAN). The warm start never
fired (K_WARM = 0 everywhere): its only source is a rebind's retired memo. New predictions for
the decisive clean-base arms (8498d1c8 + this patch, rebuilt cold after the warm-cache
staleness bug — the first "base build" silently linked HEAD objects):

- **P9 (the base regenerates the prior run).** m4000/s3 at the clean base: fired kick
  230–280 µs, K_IMP ≈ 2 × kicks (2064ish), rebinds ≈ kicks, digest `2e97e580…` (their stored
  JSON's). If the clean base instead gives the HEAD picture (13 µs kicks, digest `31a75a15…`),
  the prior run's own record does not regenerate at its own base and the silver's reproduction
  claim is broken — either way the wiki page must be rewritten.
- **P10 (the warm start works where the premise lives).** At the clean base with ES_IMP_WARM:
  digest(warm-on) == digest(warm-off) == the base's own; K_WARM ≈ K_IMP − hand-out searches;
  fallbacks < 25%; the fired kick falls to 130–180 µs (the checker's ~140 target); readouts per
  search (K_PING/K_IMP) ≤ 8 warm.
- **P11 (attribution).** The term's death is in 8498d1c8..HEAD; prime suspect the far-flyby
  merge 9143329b (the key's k carries its own exponent → the leaver tube's word → the kick's
  quantize threshold → dv sub-quantum → carried, no rebind, no search). A clean build at
  9143329b shows cheap kicks if that is the commit; if kicks are still dear there, it is the
  ladder stack (0f112b89's frame change), to be named by one more build.

What would make me wrong: a digest that moves (the monotone assumption or the gallop is wrong),
a fallback rate above the kill line (the boundary really does jump brackets under kick-sized dv),
or the kick µs not moving (the search was not the wall after all on this tree, which has moved
since f687ec25 — the N ladder merge changed the frame).

## Addendum 2 (before the fixed arms: my patch's own bug, caught by the clamp-only control)

The "term died at HEAD" story above was MY artifact: a kick-tail repair dropped kick's
`self.rebind(next, t, d)?;`, so my patch's kicks never rebinded (hence 13 µs kicks, K_REST = 2,
and digests 31a75a15/08c33f95 that belong to no tree). The clamp-only control at base 8498d1c8
gives 2e97e580/7b33d0b8 — the prior run's digests; its patch reproduces its record exactly
(kick 241.7 µs, K_IMP 2064, rebinds 1034). Predictions for the FIXED patch's arms:

- **P12 (HEAD has the term).** m4000/s3 at HEAD, warm off: fired kick 230–280 µs, K_IMP ≈ 2 ×
  kicks, digest 2e97e580… (the base's — the ladder merge was digest-preserving). If the digest
  differs, the trees diverge canonically at this scene and I report which.
- **P13 (the warm start, for real).** Warm on: digest bit-identical to warm off; K_WARM ≈
  kicks (every fired kick's rebind carries a retired memo — only when the retired tube had found
  one; the first search of a fresh orbit stays cold); fallbacks < 25%; kick ≤ 180 µs; readouts
  per warm search ≤ 8 (K_PING falls ~2×); hand-out replan µs unchanged (no warm source).
