# Dossier — 20261013-0459-library-36bf (lens: Julien's library)

**Claim.** The library's practitioners name the same fix the high-gamma-clock page is circling —
the wall is no longer the clock but the record and the instruments — and the cheapest of their
lessons is executed here: one `end` word tells the three silent deaths apart (crash, planet,
leave) with bit-identical canonical outcomes.

**Bottleneck.** `high-gamma-clock` (top of the board). The page's own residue after the
exact-in-E merge: open directions 1, 2 and 4 are HUD/word/fit questions, not clock questions.
Expected gain: no orders of magnitude — this deletes the defect that "the record cannot tell
[the three ends] apart", which is the prerequisite for the playability HUD (open dir 1) and the
fault-tag proposal (open dir 4). Cost: 22 lines of patch.

**Evidence** (commands run from the repo root, base 86a4c7d6; Linux x86 CI, 8 vCPU, load 2.5;
all flights ≤ 2 s wall):

- The five lessons, each with a verbatim highlight from Julien's Readwise (4,580 highlights
  fetched and cached), each mapped to an open direction and a cheapest test: `lessons.md`.
- The probe (lesson 2, executed): `work/patch.diff` adds `BodyRec::end` (+ `End { Crash, Planet,
  Leave }`), set at the seven `Resolved::Lost` sites in `step.rs`, nowhere else; not a digest
  input. Reproduce:
  - crash: `end=Some(Crash) fault=None event_time=118,489,088` (0.1 s)
  - leave, tight cage (`leave_log2` 40→30): level 8 leaves at 12,438,249,776 ticks; level 15 at
    1,562,576,868; control, same log in the default cage at 2×10⁹: `alive=true end=None`.
  - digest identity (two builds): `git stash push -- crates/universe/src && cargo run -q -p
    emergent-universe --release --example lab_digest && git stash pop` → unpatched digests
    `ca9ecffac3139391783c6fd1089d3873` (crash) and `acdeac981fcb3971cf02865de056cc0a`
    (leave-tight15), bit-identical to the patched runs; event times identical too.
- The shipped suite on the patched tree: `cargo test -p emergent-universe --release` —
  59 tests, 0 failed (2 ignored, pre-existing), 342 s.
- `Planet` is wired (kick-time planet-surface site) but not demonstrated in flight — scripting a
  blind planet hit was not attempted beyond the control flight, which stayed alive.

**Predictions** (`predictions.md`, written before the probe): 1 held (crash, event time inside
the predicted 5×10⁷–2×10⁸ window); 2 failed at the stated horizon — a level-8 climb is alive at
2×10⁹ — and held after a disclosed horizon/level extension (the leave is real, cage-relative,
and slower than predicted; even level 15 leaves at 1.56×10⁹, outside the predicted <10⁹); 3 held
(bit-identical digests, two builds); 4 held (planet wired, not shown).

**What would make it wrong.** A death path that bypasses the seven sites (e.g. an end applied by
the universe rather than `step.rs`), or `end` leaking into any persisted/hashed state — the
two-build digest control covers the hashing half for these flights, not every flight. The
lessons are analogies except lesson 2; 1, 3, 4, 5 each name their cheapest test and none has run
beyond lesson 2.

**Cost of adoption.** The 22-line patch, one accessor read in the HUD/session error path
(`xtask/src/universe/session.rs` already prints `r.fault`; `r.end` slots beside it), and the
checker's re-run. Nothing else moves: no law, no gate, no crate boundary.

**Fit with PRINCIPLES.** "The player is the only wildcard" (§5) — the record is what lets the
player's instruments speak; "A game is an illusion spectacle, the oracles are guards, not
shepherds" (§34) — the word guards the record, it does not steer the law; "the cheapest compute
is compute not done" (§1) — one word set at a site that already ran.

**The lens.** A library lens finds lessons that flatter the plan; I kept only ones that name a
decision, and executed the cheapest to keep the run honest — but the quote-mining could still
have missed practitioners outside Julien's Readwise (no Kelly Johnson, no Ignition!, no Forth:
those books have no highlights). The four unexecuted tests are exactly where this run is one
experiment away from more.

**Grading note for the checker.** `regen.sh` re-fetches Readwise (token required, else reuses the
cache), verifies every quote verbatim, applies the patch, runs the probe, and re-runs the
unpatched digest control via `git stash`.
