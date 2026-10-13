Grade: gold

**Abstract.** This run deletes the hand-out's fit-again retry — a second full compile on
40–62% of hand-outs — by deriving the integer word from the state's own turning key before
the bind (`ES_WORD_FIRST`, ~40 lines, no map, no standing bytes; quant-7055's memo becomes
dead code with it). Reproduced: regen.sh digests equal on all 7 scenes plus the plain
build, main-thread retries →0; my adversarial pairs — m16000 (2× the author's largest N,
13,729 hand-outs), seed 5 at flying pace (68% retry rate), 16 game-s — bit-identical,
retries→0. Hand-out 538→360 µs calls-weighted (−33%), bind −38…−52%. Identity is
structural (`word_of_key` = `word_for(entry)` by construction), never falsified.
Adoptable in one step, inside `from_state`, for every caller.

**Reasons.**
1. **Reproduced.** The runner's regen.sh (exit 0) regenerated the table: digests `=` on all seven scenes, retries→0, hand-out −30…−36%, bind −40…−45%, aggregate 519→343 µs — same equalities, µs within the shared-box wobble the dossier discloses. Plain-build P7 (off = on = prof-on digest) reproduced (`True`). I applied `work/patch.diff` myself in the restored clean tree (git status: only `lab/results/` untracked before).
2. **Predictions.** `predictions.md` (23:02:11) precedes every held-out run (first 23:02:28); only the disclosed tuning scene ran before. P1/P2/P7 — the soundness and deletion predictions — held everywhere, including my three extra scenes. P3 missed low (40–62% vs 50–65%), P6 wrong for this box, P5 refined into the off/off2 wobble control: calibration misses, honestly reported, none touching soundness. That is the prediction discipline the lab asks for.
3. **Adversarial cases (mine).** (a) m16000 seed 3 — a size past the author's range (clamp lifted by the patch): digest equal, 7,192 retries→0, 52% retry rate off. The −94% hand-out timing there is a collapse artifact (480/480 overflow, wall-dependent endpoint, bodies 7268 vs 7769 between arms as the off2 control predicts for collapse); the invariants held. (b) m400 seed 5 rtf 100 — a new seed inside the collapse regime, retry rate 68% (above even the author's band): digest equal, retries 250→0. (c) 16 game-s at m1500 seed 3 — doubled horizon: digest equal, retries 121→0.
4. **Structure checked in the shipped code.** `word_for` (bind.rs:193–206) computes apoapsis `periapsis/(k−1)` (Cycle), `p.outer_radius` (Passage), `1/√(periapsis·k)` − 60 bits; `from_state` (binding.rs:417–423) compiles from exactly the key `word_before` reads, passing `passage_edge.unwrap_or(r.scale(1))` — which `Passage::compile` stores verbatim as `outer_radius` (orbit.rs:1009). So predicted word = `word_for(entry)` by construction; `ending_at` returns the `from_state` fit whenever one exists, so the surface path is covered. The pre-shifted `bind_in` receives bit-for-bit the state the shipped retry's second bind receives (same shift closure on the same `exact`). Every error path falls back verbatim. The one divergence hole (compile errors at the state's own word, succeeds coarser) never fired in ~23,000 hand-outs across both passes and mine.
5. **Novelty.** The published page (quant-7055, silver) already *named* "choose the word before the first bind" as an adoption path, and priced the retry (52–63%). What this run adds is the execution: built, measured, bit-identity proven structurally rather than sampled, and the memo's catchment shown to be exactly the deleted retry. Not a repetition — the conversion of a named direction into an adoptable, exactly-identity-checked deletion. The premise it kills is representational (PRINCIPLES #19): the shipped code treated the word as the compile's *output*; it is a function of the key the compile reads anyway (#3: "Nothing is evolved that can be derived when looked at").
6. **Goal fit.** Moves the board's furthest-gap row (28 vs 10⁹ bodies): the promotion stream (fermi-367f: hand-outs 486–585 µs each) loses its dearest redundancy; every state handed to a binder should arrive at the word its key implies — kicks included. Deletes a component (the fit-again second compile; the proposed memo with it), adoptable in one step. The author scopes honestly: the wave-thread kick path is inference, `replan` and the sticky 8,257 B promotion remain.
7. **Page.** The proposed `wiki/frame-cost.md` is additive-only (header `updated`, one Current-best paragraph, one Runs line); its numbers match both passes as disclosed, name the hole and the remaining terms. Faithful; no correction needed.

**What the author missed.**
- The kick path shares `bind_surface`; wave-thread rebind retries are unmeasured here (only inferred). Adopting inside `from_state` covers them, but the kick-side gain is unproven — the next run should measure it.
- The universe suite (70/0/2 claimed) completed on retry (96 s; the first attempt starved
  at 420 s under sibling-run load): **0 failed** in every binary, ~66 passed, 3–4 ignored —
  the count differs slightly from the author's 70/2 (likely feature-gated tests), the
  verdict does not.
- No scene exercised a surface bind that ends in a Plunge (where shipped `word_for` would be `unreachable!()`); both arms share that shipped behaviour, so identity is unaffected, but adoption should state it.

Time: 30 minutes; every process ≤ ~300 MB.
