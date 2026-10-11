Grade: silver

**Abstract.** Claim: at 10⁹ bodies the walls rank kick-path per-event cost (18–69 µs measured, ~0.2 µs at a memo hit), then the view at 10⁹-in-view (25–37 ms/frame), then memory as un-reabsorbed scars (~1 per body per session); the board's "190 cores" is one scene (re-derived 178), and belt compute is 0.026 cores. Everything reproduces: plane benches bit-identical (digest, event counts; ship 59–71 µs, fleet 18–25 µs), galaxy scene deterministic (13,963 compiles, hit 0.987, 0.43 s build; view medians within 5%), budget.py output identical. Gain: a measured re-ranking of board #3 plus a scar ceiling for b-h-live. Cost to adopt: none (queue re-ordering). Not gold: two held-out predictions failed, and the 150–350× memo lever rests on an unmeasured 0.2 µs.

**Reasons.**

*Reproduction (clean tree, HEAD a838a284, empty patch.diff, binary at `$CARGO_TARGET_DIR/release/xtask`).*
- `universe --bench --rtf 100 --seconds 15 --unpaced`: digest `01c9be77…` identical, stats identical (kicks 941, slices 3734), events/s 367.5, bytes/body 5,044, ship 71.0 µs, fleet 18.1 µs, player 361 µs, engine 21.9%/gather 65.8%. Dossier: 69/17.8/352 µs, 22%/66%.
- `--members 4096`: digest `29662bc6…` identical; ship 59.4 µs, fleet 25.0 µs, 417 bodies, 1,745 events/s (dossier 60/25, 417, 1,745).
- `galaxy --bench --ships 1e9 --tubes 1e6`: scene line byte-identical (13,963 cycles, hit 0.98717, compile 0.42 s); far/mid/deep medians 31.8/35.4/25.9 ms (stored 32.3/37.2/25.8), ns/ship 0.032/0.053/0.152 (stored 0.032/0.055/0.151); peak RSS 256.7 MB (stored 247.0; shared machine). My wall_s 18.7 s vs stored 5.7 s is contention only; medians unaffected.
- `budget.py` output identical to `budget-out.txt`. Arithmetic re-derived independently: 178 cores (190-scene), 5.1×10⁶/7.7×10⁸ hot bodies, 34.4 b/ship state budget, 1.05 scars/body, 444 wall-hours/orbit, 423 wall-hours session — all check.

*Predictions.* `predictions.md` (06:19:42) precedes all three outputs (06:20:12, 06:20:45, 06:21:17); `run.log` is empty, so pre-tuning runs cannot be excluded, only the stored timeline verified. Held: galaxy < 60 s/< 1 GB/≥ 10⁷ ships/s/compiles < 10⁵; the 190-cores re-derivation (178 vs 190, 7%); per-event 1–100 µs for ship/fleet. Failed, both honestly reported: bytes/body 40–600 B predicted vs 5,044–6,227 measured; events/s ≥ 5×10² predicted vs 368 measured. Under this lab's own precedent (1 October red-team: one failed prediction → silver), gold is excluded.

*Adversarial cases run.*
1. Seeds 7 and 42 (held out): ship 66.5–77.2 µs, fleet 18.6–20.7 µs, events/s 362–421, bytes/body 4,439–4,838 — the per-item bands and the 30 µs anchor hold across seeds (seed 7's 77 µs slightly exceeds the quoted 69, same order).
2. `universe --kick-bench --rtf 100 --seconds 15` (the dossier never runs it): distinct-kick median 37.2 µs, all-kick median 84.1 µs, leavers 96.5 µs — the 30 µs anchor is optimistic by 1.2–3×, and its `memo` block shows exact_hit_rate 0.0 on distinct kicks (the 5 October correction). The "~0.2 µs at a memo hit" is a target for a mechanism not yet wired; the 150–350× lever is a projection, not a measurement.
3. `galaxy --ships 4e9 --tubes 4e6 --png`: 153 MiB peak RSS (0.33 b/ship, sub-linear — cycles and track knots amortize); "billions" holds and the memory claim is conservative.
4. `galaxy --bench --frames 1` gives 246 MB (render buffers), while `galaxy --ships 1e9 --tubes 1e6 --png` gives 104.2 MiB ≈ the dossier's 106 MB. The 106 MB is real but regenerable only by a command the dossier never lists; its listed command yields 247 MB.

*Novelty.* H0210 already recorded "kicks cost 29 µs" and the gather share; the board's #3 already said "10–100× less". New here: the one-law budget with measured per-kind anchors, the 10⁹ galaxy scene measured end to end, the 190-cores premise correction (scene-conditioned: 0.026 cores at belt scale against 778 at hour-orbits/rtf 100), the view wall priced at 2× over 60 Hz, and the scar-session ceiling handed to b-h-live. docs/fermi.md is Julien's original estimate, not a competing run. No prior entry prices this.

*Goal fit.* Board #3 and the H_live line, directly. PRINCIPLES #3: "Compute only surprises" — the law makes cost the event rate, not the body count. #27: "the goal, never a proxy" — rtf and P are the player's scene choices, t_event is ours. Lens limits are honestly stated (concentrations and the GPU ceiling untouched).

**The one experiment that would make it gold.** Measure the memo-hit kick on the plane's own path (wire the cycle-keyed memo behind `--kick-bench` and report the hit-cost median alongside the 37 µs miss cost). That turns the first wall's 150–350× from projection into measurement and fixes the ranking's only unmeasured term; with it, and the two failed predictions' numbers restated correctly, this is a gold re-ranking.

**What the author missed.**
- The kick bench exists in the same binary and answers the dossier's central quantity directly (37–96 µs, memo hit rate 0.0 exact); the 30 µs anchor and the 0.2 µs target were never cross-checked against it.
- Two claim-line numbers are wrong against their own evidence: the bandwidth crossover is 6.4 ns at the script's 96 B/60 GB/s (4 cores), not "~64 ns"; and the plane is ~1,200–1,500× above the 34 b/ship envelope (5,044–6,227 B = 40,352–49,816 b), not "~150–400×" (that ratio matches the 16 B tube target). Both slips leave the conclusions standing but understate the memory miss by ~4–10×.
- The player's per-item cost is 1,658 µs in the m4096 scene (stored JSON, reproduced at 1,656 µs) — 4.7× the quoted 352 µs; "per-item cost stable" is quoted only for ship/fleet.
- The belt row's P = 5.2 yr is an assumption (a ~3 AU belt about the sun-radius star), not a repo number; it is undocumented, though the row's verdict holds for any year-scale period.
- "0.03–0.06 ns per ship in view" omits the deep view's 0.151; and 25.8–37.2 ms spans three views of which only "far" has 10⁹ in view (32.3 ms).
- "1.2% of one M1 under averaging plus a memo hit" is 0.28% of the M1 at e = 0.3 (kicks only) and 1.3% at e = 1.4; the event mix behind the quoted figure is unstated.
