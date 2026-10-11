Working...
Check complete. `check.md` written to the run folder; nothing else there touched (reproduction ran on a copy in `/tmp/check-b12`; the stored `falsifier-out.json` verified untouched by diff).

**Grade: silver.**

Verdict basis:

- **Reproduced bit-identically** (18 s, <100 MB, deterministic). The synthetic port is faithful where it claims to be: exponent gate matches `fit.rs` line for line; FLOOR/ERR_MAX/GROWTH_MAX, 16 ships, 200 P at P/8, BOUNDED=1e-7, compound steps, KICK=1e-3 all match `handoff.rs`/`laws.rs`; the cited real-scene 0.49 exists as the ignored probe test at `handoff.rs:348`.
- **Negative half is robust**: exp/Allan/rank all false-flag the bounded control at the gate's horizon — structural (bounded-in-state is a walk in observation space), and it survives my attacks and seed sweep (12/12). This kills the statistic-hunting branch of the three in-flight B12 rebuilds.
- **Positive half is real but unproven**: my adversarial cases found (a) the at-floor leak `leak[1e-9]` fails only 10/12 master seeds — "ten of ten contracts" is seed-fragile at the margin; (b) the shipped 10× run was an independent redraw, not the extension it names (prefix ratio for bounded is 1.48, not 1.1); (c) at 5× slower a-diffusion the ratio clause **false-fails the bounded control** (2.30 > 2) — an unstated saturation assumption in exactly the dimension the author admits is unfaithful; (d) sub-floor leaks are invisible exactly as the dossier's floor claims.
- **Prediction ledger selectively reported**: three partial misses unacknowledged (echo Allan −1/2 vs −0.0; rank still failing bounded at 10× contra prediction 5; prediction 7 contradicted by the induction argument). The author's own flags (post-hoc composite, unverified cap derivation and drift shape) were already honest.
- **Novelty held** against H0215 and redteam-b12-stat (which killed only the exponent and a recurrence ratio); this run answers the queued `q-b12-design` question clause for clause.

Gold experiment (stated in check.md): the composite in `xtask`'s harness on the real frozen ships — cap from each ship's real C_J zero-velocity curve, real planted laws plus a floor leak, measured a-diffusion saturation, two machines, seed sensitivity reported.
