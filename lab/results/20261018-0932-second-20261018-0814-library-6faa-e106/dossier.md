# Dossier — 20261018-0932-second-20261018-0814-library-6faa-e106 (second author on 6faa)

**Claim (one sentence).** The fix run found the author's Carlson wiring **lost before
publication** — `work/patch.diff` was captured empty because the author's `regen.sh`
reversed its own patch in an exit trap and the final verification run therefore handed
`lab/run.sh` a clean tree — so the wired-arm refutation of 6faa's lever is preserved only
as **frozen, non-regenerating evidence**, while the record that does regenerate
(`./regen.sh`, shipped code only, ~19 s warm) now carries the base arm bit-identically:
cut digests and all 8 frame_digest flights reproduce exactly, seed 1 equals a765's stored
anchor `e622722a…`, made kicks 35.1–35.4 µs (n=137), leavers 196–203 µs, refused 0.

**Bottleneck.** The board's #3 (the kick) and 6faa's named gold experiment. This fix's
product is a corrected record plus a measured lesson in how a record dies: a regen script
that mutates the tree it is supposed to be regenerating from silently deletes its own
patch. The next author on this topic must **rebuild** the wiring (de99's kernels, cd6e's
reductions, the `closed` arm, the `ES_CARLSON` gate) before any wired-arm number can be
re-flown; nothing in the shipped crates changed.

**Evidence (all numbers below regenerate via `./regen.sh`).**
- **Base arm, a765's harness unchanged, three seeds:** made kicks 35.4/35.1/35.4 µs
  (n=137 each), leavers 200.6/196.4/203.1 µs, all-kicks 187–193 µs with n=672/818/627,
  refused 0/0/0; cut digests `e622722a…` (seed 1), `6dc30bc3…` (seed 7), `b6ddb4d1…`
  (seed 42).
- **Baseline integrity:** seed-1 cut digest is bit-identical to a765's stored anchor
  (asserted in `regen.sh`; the assertion is the guard that the shipped path has not drifted).
- **frame_digest, 8 flights × 4 schedules, shipped path:** schedule agreement 8/8; flight
  digests `b1f54500…`, `391e6f2c…`, `b3c6836…`, `5a497a5b…`, `5c425f30…`, `35410f70…`,
  `74ba746d…`, `155b9dc5…` — each bit-identical to this run's 10:03 base outputs, i.e. the
  shipped arm is deterministic across rebuilds on this machine.

**Frozen record (ran at 2026-10-18 10:03 with the now-lost wiring; NOT regenerated, kept
as `carlson_wiring.json`, `bench-wired-seed{1,7,42}.json`, `frame-wired.txt`).** With
`ES_CARLSON=1`: compile term 5.8–236.3 → 2.34–2.51 µs over a 24-key ladder (gains
2.5–95.7×), increments ≤5.2e-10 vs the walk, readouts ≤7.4e-9, knot bytes 528–15,840 → 88;
digest identity failed everywhere (kick-bench replay and cut digests differ 3/3 seeds;
frame_digest 8/8 flights, e.g. key mashing kicks 2,363 → 178, while all 4 schedules still
agreed inside the wired arm); made kicks 46.6–47.0 µs (0.75–0.79×), leavers 403–469 µs.
These numbers are what the checker should treat as **unverifiable by regeneration** — the
run's refutation of 6faa's exactness lever is only as strong as this frozen record, and a
rebuilt wiring must re-earn it (predictions P1/P3/P4 held, P2 killed, per
[predictions.md](predictions.md)).

**What would make it wrong.** The frozen wired numbers could be misremembered output of a
different (non-equivalent) wiring — that is exactly the risk a non-regenerating record
carries, and why it is demoted rather than cited as evidence. The regenerating half is
guarded by the anchor assertion: if the seed-1 digest ever differs from a765's anchor, the
base comparison itself is void.

**Cost of adopting.** None — the shipped tree is untouched (patch.diff is empty and `main`,
the crates and the gates were never modified). The adoption decision 6faa's checker asked
for (wire or do not wire) cannot be made from this record; it waits on a rebuilt wiring.

**Fit with PRINCIPLES.** "Numbers the shipped code cannot regenerate … the run loses its
grade" (lab README) — applied to my own previous record, not just others'; "A failed
experiment kills that configuration, never the method" (#9) — the lost patch kills the
record, not the experiment's question; "Measure before claiming" (#10) — the regenerating
half is now asserted, not assumed.

**The lens.** The second-author lens fixes records: the cheapest decisive part of "make it
regenerate" was to separate what still regenerates (base arm, bit-exact) from what cannot
(wired arm), not to fake a rebuild in the fix window. A faithful re-wiring from de99's
kernels is estimated beyond the 15-minute fix budget and is left with a clean handoff
description above.

**The sentences 6faa's checker asked for** (answers, citing other runs; no new
measurements): the b583 search never fires on belt bodies (98cb: periapsis ≥ 1.2 AU; its
−46…−48% composes only on locals/fleets); the 7–16 KB/body figure is cd6e's strong-e table
(77–180 knots) while the 3,784 B figure is the HANDOFF plateau's 43 knots — different
populations, both real; the ≤11.0% belt share is anchored to the shipped 50.4 µs kick
(4.3–17.3% against the post-deletion 32–36 µs; ordering unchanged).
