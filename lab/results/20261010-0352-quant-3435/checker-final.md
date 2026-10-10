Working...
Check complete. `check.md` written to the run folder; nothing else touched, no commits.

**Grade: silver.**

What I did and found:

**Reproduced bit-for-bit** (clean tree, empty patch.diff): all seven digests (`c1c28574`, `c4307bb5` ×3 incl. unpaced, `f546d996`, `cbac1322`, plus f1/e1 against the author's own files), event counts (encounters 2→442, boundaries 0→263), ev/s, bpb growth, stage shares (readout 80–95 % of frame CPU everywhere), the members clamp (`--describe`: 4800→400, `mod.rs:32`), and the code structure: `view.rs:300` loops `0..n_bodies()` + fleets with `ViewCache` seeding only Newton's guess, and `session.rs:83` budgets only `frame_to` — gather/JSON genuinely unbudgeted. Predictions pre-registration confirmed by mtimes (03:56:58 < first run 03:58:27).

**The break did not reproduce.** My b1 reruns on seeds 1 and 7 both give p99 11.4 ms, 0 hitches (author: 16.9 ms, 3,240/h); my e1 flipped the other way (540/h vs 0). The crossing lives inside the box contention the author disclosed — so the proposed falsifier already passes on unfixed code and can't discriminate a fix.

**Adversarial addition:** b1 at `--engine-ms 15` gives the *identical digest* at a worse tail (p99 18.2, engine p99 riding the new clamp) — outcomes are budget-invariant while engine spend is elastic; the gather is the only non-tradable floor. Stronger than anything in the dossier, and it still supports the ranking.

Gold needs one experiment: a box-robust tail metric (CPU-hitch counts, multi-seed, load-controlled) plus one gather-bounded b1 variant — proving the 10× lever instead of inferring it from shares.
