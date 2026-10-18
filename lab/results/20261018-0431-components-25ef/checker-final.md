Working...
Check complete. **Grade: lead** — `check.md` written, the author's wiki page corrected in place, tree restored.

**The finding:** every number in the dossier reproduces bit-for-bit, but the run's arm is dead code. The two-word write in `step.rs` differences against `prev.kick.word?` — an `Option` chain that needs a previous `Some` to produce a `Some`, while both seed sites (`Kick::NONE`, `kick_clock`) write `None`. No first word can ever exist. Proven three ways:

1. **Instrument**: `A_WORD=2` on the gates' own scene → "word armed on 0 of 162 binding reads; any armed binding in history scan: false".
2. **Behaviour**: my adversarial probes (steps 2⁷→2³ kicks/period — a decade below the author's 2⁶ domain floor — and deep passes at 1.0–1.5 Hill radii) print digit-identical figures arm ON vs OFF on every ship; the shipped ratios hold (worst 1.90× at 2³, bar 3×), but they were never the arm's.
3. **Code**: the fired-kick closure is the only `Some`-writer in the patch; the induction is airtight.

So the headline — "the two-word passes every frozen readout gate at 1.11×, the per-read field evaluation is deletable" — measured only the shipped path; the ON=OFF identity the author read as "both quadratures sit under the boundary's own error" was structural, not physical. The predictions (genuinely pre-run, 04:40 < 04:48) held vacuously. The design remains plausible and is one seed line from testable — that experiment, plus a word-coverage census as the missing control, is named in check.md for the next run.
