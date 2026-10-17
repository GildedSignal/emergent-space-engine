Working...
`Grade: gold` — written to `check2.md`, page corrected in place, tree restored to pristine.

**What the check established:**

- **Reproduction clean.** Patch applied to a verified-clean tree, rebuilt, re-run: all four digests bit-identical patched vs pristine; every census count matches the author's stored evidence within 0.15% (the law is deterministic; the ≤0.15% drift is scheduling-dependent extra reads).
- **The structural kill is real code, not instrument.** `bind.rs:276–287` — `bind_in` decodes the fresh trajectory at the binding event to build the `turn` and `residual`. The mint is necessarily the first reader, so "compile at first read" defers nothing; never-read=0 is structural, not statistical.
- **Held outside the author's domain.** seed 7 × 400 members (65.6 reads/rebind-gen, birth-read first 10,573/10,573), seed 3 at rtf 300 = 3× flight (51.9, 1,908/1,908), kick-bench seed 7 (32.0). Also found `--members` is clamped to 400 in the CLI — the author's held-out arm already covers the bench's entire member axis; no larger-N bench exists to run.
- **Novel.** Direction 2 stood open on b9ae's "read ~once per binding" and 0e37's reader guess; both premises are now measured dead, with b8fc's cell-level census kept distinct.
- **One correction folded into the page:** "view 1%" counts view.rs's direct decodes only — the view's per-frame gather routes through `observe::root_state` (view.rs:282) and shares the observe bucket with the engine's per-event apply reads (universe.rs:673), so "the reader is the engine" holds as immediate-caller attribution only. The kill itself is attribution-independent, so the grade stands.
- Minor integrity nits logged (three stale last-digit numbers in the dossier vs its own stored files, the 0.1–0.2 µs/read amortization actually measures 0.21–0.49 µs, ×98 is the no-cache upper bound) — none decision-relevant.

`check.md` was never opened; the first checker's `/tmp` scratch files were left untouched; no git commits or pushes.
