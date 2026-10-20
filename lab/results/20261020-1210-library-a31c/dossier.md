# dossier.md

**Claim.** The nladder's two named exits are decided by five library lessons, and the
composition they carry is new: after the boundary comb is deleted, the 10⁹ era wall
is one term (the kick item's µs — 658× over the play budget, fitting at 0.72× on
the ~50 ns floor), so the deletion and the interleave are complementary (different
terms), and the deletion's honest gate is behaviour on the moved-anchor arm, never
digest identity.

**Bottleneck.** Board #1: bodies in the flyable engine (10⁶ now, 10⁹ goal), on the
nladder page's own open targets (payload interleave adoption; boundary-comb
deletion, "the cheapest next target"). Expected gain: the deletion removes ~50% of
the belt's stream events (49.7% burn / 50.7% coast, page regen) and halves the era
alternation; it deletes a component (the boundary certificate) rather than tuning
it. The interleave (28k, checker2-flown: walls 1.06×) is the wall-equalizer the
deletion cannot replace.

**Evidence** (commands run from `lab/results/20261020-1210-library-a31c/`; all ≤ 60 s):
- `./regen.sh` — full regen: fresh Readwise fetch (token) or the cached 9 pages
  (fetched 2026-10-20, 770 books / 4,590 highlights), then:
- `python3 verify_quotes.py` — 5/5 PASS byte-identical (L1 Ries; L2 Hoffmann;
  L3 Kahneman; L4 Farnam Street Power Laws; L5 Darwin via Farnam Street).
- `python3 compose.py` — era budget 69.75 s (27.9k gs ÷ rtf 400); kick comb
  1e9 × 45.9 µs = 12.75 h (658× over); boundary comb 1e9 × 8.6 µs = 2.39 h (123×
  over); at the 50 ns item floor the kick comb is 50 s = 0.72× budget; the deletion
  buys 1.2× on the era wall (12.75+2.39 → 12.75 h) while removing ~50% of events;
  era-2/4 walls at 1e5 lose ≈ 105k × 8.6 µs = 0.90 s of items (P4: the alternation
  halves, it does not equalize — the interleave stays necessary).
- Code anchors (grep-verified, `regen.sh` step 4): `step.rs:717-718` inserts the
  Boundary item at `t + full/2` and the next kick at `t + full`; `kick_clock`
  (`step.rs:663-676`) already runs the star/planet/doll crash checks at every kick
  and does NOT check the leave edge; `boundary_clock` (`step.rs:725-739`) is
  surface + leave + anchor stamp; `universe.rs:1327` hashes `rec.anchor` into the
  frame digest.

**Predictions** (`predictions.md`, written before `verify_quotes.py`/`compose.py`
ran): P1 held 5/5; P2 held (12.75/2.39 h vs the page's 12.8/2.4 h, within
rounding); P3 held all four; P5 held (770/4,590); P4 is unflown by design — it is
the flying run's falsifier (walls halve, not flatten), stated as a prediction.

**What would make it wrong.** The 45.9/8.6 µs constants are 8365's sequential
carrier on this box (draw-band ±22% per 476d) — the composition's ratios, not its
absolute hours, are the claim; a kick-item lever below 45.9 µs without a law change
would collapse L4's "918× is representation". The deletion's behavioural safety
(leaves detected within one full step; no crash seen later than a full step) is
asserted from the code paths, not yet flown — the rung must fly it. The boundary
may also carry consumers I did not audit beyond the anchor and the leave (the plan
insert at `step.rs:580,588` for non-clock bodies is untouched by this proposal).

**Cost of adoption.** Two small arms on shipped code: (a) env-gated removal of the
`step.rs:717` insert for clock-stepped bodies + leave-compare folded into
`kick_clock` + anchor stamped at kick; (b) the 28k interleave as birth default.
Both re-freeze on the M1 (per the taste log's rule for schedule-visible changes);
neither is a law change if the canonical cuts hold across schedules.

**Fit with PRINCIPLES.** "The cheapest compute is compute not done. Delete before
optimizing" (#1); "No work for no reason, so no ticks … we only care about changes"
(#14 — the boundary comb is a metronome certificate); "Compute only surprises" (#3);
"minimize spike compute and average compute usage" (#12 — the interleave); "a test
that cannot fail is a control" (criteria passable in principle, L5).

**The lens.** A library run composes, it does not fly: every number here is
page-cited constants or grep-verified code, none re-measured — a flyer (inversion
or second-author lens) must fly the deletion arm before any of L2/L3's changes are
adopted. The lens may also have missed boundary consumers outside
`crates/universe` (the client's map readout reads anchors; the exact consumer set
of `BodyRec::anchor` beyond the digest hash and `Kick.lead` is un-audited). And
quotes are Julien's reading, not the engine's: L1–L5 change decisions only through
the mechanics named above, not by authority.
