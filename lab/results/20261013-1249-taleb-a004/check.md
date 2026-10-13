Grade: gold

**Abstract.** The shipped interactive loop logs key changes at the frame's presented tick, so load and frame rate rewrite canonical history — and this run measures the break as *compounding*, not a bounded offset: 0.31→2.3→18 AU player separation per 3× flight time (×7.5–7.8, no saturation), contacts 6 vs 54 at 756M ticks on identical inputs. The a342 fix (`sched` timeline + `input_frame`, 0.25 s wall quantum) ported to the current tree closes it: one digest across 30/60/144 Hz, load, rtf 100/1, 48/400 members. I reproduced all 20 arms bit-identically on a clean tree, suite 69/0/2, and could not break the fix in five adversarial families (seeds 7/42, fix at 756M, rtf 10/30, threads 8, boundary presses). Cost to adopt: the 36-line patch + regression test; price 0.05–0.15 s input lag, declared straddle ambiguity.

**Reasons.**

1. **Reproduction.** Applied `work/patch.diff` myself to a clean tree; `regen.sh` exit 0; all 20 arms bit-identical to the stored matrix modulo `wall_ms`; `summary.txt` identical; 6/6 predictions HELD; `decision_tick` 2/2. Full suite `cargo test --release -p emergent-universe`: **69 passed, 0 failed, 2 ignored** (clock, motion flights) — the dossier's first regression paragraph is correct; the second ("58/58, run once") is a stale duplicate paragraph contradicting the first (hygiene flaw, not a substance flaw). `xtask` builds (regen builds it).

2. **Predictions.** `predictions.md` predates every work artifact (file times; content concedes "I have not run it yet" on the current tree), names its own kill criteria, and all six held. The pre-registered superlinearity criterion (>3 per 3×) is honestly stronger than the result needed.

3. **Adversarial cases (five families, three outside the author's domain).**
   - *Seeds 7 and 42* (author used only 11): raw 4 arms → 4 distinct digests each; fix 4 arms → exactly 1 digest each. The mechanism (starved arm logs the first press ~19–21.6 game-s earlier) reproduces at seed 7 (10,151,250 vs 6,291,479).
   - *The fix at the ladder's top* (author ran fix only at 84M): fix rich-vs-starved at 252M and 756M → one digest each (`5edbd226…`, `d4f008e7…`), identical ticks — the fix closes the compounding channel where the raw hole is worst.
   - *rtf 10 and 30* (author: 100 and 1): load pair one digest each.
   - *Threads 8* (never varied in this run; the doc comment claims thread-independence): fix rich and starved at thr8 = thr1 (`711b3acf…`).
   - *Boundary geometry*: press 0.49 and 0.50 → 30/144 Hz agree; 0.51 and 0.76 (10 ms past a quantum boundary) → straddle by exactly one quantum (10,151,272 vs 15,226,908; 15,226,908 vs 20,302,544). Deterministic, exactly as the declared model. The fix's equality held everywhere I attacked it.

4. **Novelty** (against `lab/wiki/frame-cost.md`, HISTORY, and the run records in git). The hole and the fix are prior art: 40c0 (silver) found the four-digest split; a342 (ungraded, never merged) built the identical fix — same `sched`, same 0.25 s quantum, same wiring, even the same logged ticks — and already measured the 0.26 s straddle and the ~5% ambiguity estimate. What is new here: (a) the **compounding ladder** — no prior run measured whether the divergence is bounded; ×7.5–7.8 per 3× time to 18 AU with contacts 6 vs 54 refutes "bounded offset" and makes the in-flight recorder's `--replay-all` flag a coin flip on machine load (a gate-validity premise overturned); (b) the **port to the post-clock-merge tree**, wired, suite-green, one-step adoptable — a342's evidence was on a tree five days stale. The dossier and page credit a342 throughout; P1/P3/P5 are honestly labelled "ported"/"reproduced".

5. **The page.** Faithful to the evidence (every number checks against `work/matrix.txt`; 21.6 game-s = 10,151,250−5,767,303 ticks; ticks are quantum multiples). Two overstatements corrected in place: the "quantizing the presented tick" refutation belongs to 20261012-2257-scout-64e4, not 40c0; and "the straddle limit made deterministic" → reproduced (a342 had measured it, same ticks). Topic stays open: one gold here, one silver (40c0), one ungraded (a342) — not three agreeing golds.

6. **Goal fit.** AGENTS.md Truth: "Canonical outcomes are exact and independent of cache, partition, observation, schedule and hardware" — the hole is a live violation of exactly this in the shipped loop, and the fix restores it at one integer add per frame. PRINCIPLES #13: "divergence is not a joke and it compounds" — here measured doing precisely that, then deleted. #5: the log returns to being the player's intent. Taleb's ruin-before-optimization: the one reachable ruin state closed before the recorder freezes it into a merge gate. Not a speed lever and does not need to be.

**What the author missed.**
- The fix was never run at the long cuts where the raw hole is worst (84M only); I ran 252M/756M — it holds, and that fact belongs in the page's domain line.
- The compounding ladder is one seed/scene/script; the mechanism generalizes (seed 7's decision shift, above) but the exponent itself was not re-measured on a second seed.
- Threads were claimed (doc comment, a342) but never varied in this run; I verified thr8.
- The snap-past-cut residue is more than a footnote for the recorder: a flight's last quantum of decisions can be silently dropped at the cut (here the 4th press at 84M) — the recorder must place its cut a quantum past the last logged press.
- Dossier hygiene: the duplicated contradictory "No regression" paragraph (69/2-ignored vs 58/58); "encounters ±33%" blends a −33% and a −39% pair.
- The follow-up the run itself names (snap the quantum to the input event's own wall timestamp) deletes the straddle class entirely and is the right recorder-grade resolution; the ambiguity-rate figures (~13% at 30 Hz) remain analytic, not swept.
