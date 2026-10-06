Working...
Check complete. `check.md` written; tree restored to clean (only untracked `lab/results/`).

**Grade: silver.**

What I did:
- **Reproduced** from scratch: applied `work/patch.diff`, built, ran the bench 3× — digests (`989892a4…` replay, `8283cbe3…` plane) bit-identical to the author's runs *and* to the unpatched control; `cycle_memo` 11 hits/56 shapes exact; leavers 364.8–365.5 µs; passage compile 73–74% of kick-path time, 368 µs/call on a quiet box.
- **Prediction precedence held**: `predictions.md` at 03:55:17, decisive patched runs ~04:00 (baseline 03:53 is quoted inside it as input).
- **Three adversarial cases**: unseen seeds 2 and 7 (law-identity held — digests match patched vs unpatched; the 9× leaver bill is seed-1-specific, 2.6–3.3× elsewhere, but the passage compile still dominates per call at 528 µs vs 17 µs); memo growth (unbounded, 111 shapes on seed 7 — author flagged it).
- **Code-level correction**: the 4-SOI tail is read by `Passage::state()` and `at_radius` too, not only `next_exit`/release — the lazy-tail lever survives (pure function of key + outer radius) but needs more lazy-init points than the dossier claims.
- **Novelty**: the memo-negative re-treads committed ground (`crates/universe/tests/memo.rs` pins exact-memo miss on distinct kicks at <5%; `records.rs` already wires `ShapeMemo`); the new measured content is the leaver cost split and its attribution to one `Passage::compile`.
- Two headline numbers flagged as artifacts: 538 µs/call is the loaded run's average (quiet ≈ 367, which sits exactly on the leaver median), and 16.4% mixes replay/real/non-kick rebinds (distinct-kick rate is 0%).

One experiment from gold: implement the lazy tail, re-run, show digest equality plus the measured ~5–7× leaver cut.
