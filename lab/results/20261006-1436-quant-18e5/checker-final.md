Working...
Check complete. `lab/results/20261006-1436-quant-18e5/check.md` written: **Grade: silver**. Tree restored (patch reversed, nothing tracked modified, no commits).

**What I did (30 min):**
- Applied `work/patch.diff` to a clean tree, rebuilt, reran the dossier's commands: e (worst 37.5 ms / engine max 31.2 ms, digest `bc132cb0…` bit-identical to the author's at the same cut_tick), e2b (51 vs 50 hitches), sizes audit (exact, Seen 152 B), unpaced g (0.698 vs 0.689 ms). Verified the mechanism in shipped code: wall-clock budget checked between items at universe.rs:808, `--threads 1` default, so the 31.2 ms engine frame does imply one ~26 ms item.
- Adversarial: seed 2 (no giant item — magnitude is seed-1-specific, mechanism holds), 5 s run (tail appears early, engine max 45.6 ms), rtf 1e4 overload (no exploding frame, smooth rtf dip), paced/unpaced pair on the quiet box.
- Novelty: view dominance and 33–51 ms hitches already known (H0210 "view gather is 83% of a light frame"; H0213 tail regression assigned to Sonnet); new is the item-granularity attribution, the 1:1 budget-dial→hitch conversion, and the 428-body live cap.

**Why silver, not gold:** core measurements reproduce (digest-level), but central predictions P1/P4 broke (honestly reported), the 2.7–5× paced factor is a window-contention artifact (1.06× on a quiet box — their unpaced number matches mine across boxes, their paced doesn't), the machine-state probe returns "unavailable" on Linux so no load/thermal record exists, and the gain is a redirection of allocator work plus one instrumentation line — not a 10× move, deletion, or premise kill. Gold experiment: max-per-kind in `Stats`, ≥5 seeds, name the 25–30 ms item.
