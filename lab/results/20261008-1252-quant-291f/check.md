Grade: silver

**Abstract.** Claim: one held L15 player order wakes a bounded transient — ~2,000 extra events, 94–116 budget-saturating frames, RTF floor 0.23×, worst frame ≤ 3.1× coast p99.9, digests bit-identical at a fixed canonical cut. Reproduced from a clean tree: seed-2 wake 1,929 events, 95 overflow frames, owners kick +561 / bound +515 / slice +3,046; digests 47dd9c71… / 6ed7b26b… identical ×3 — and, beyond the dossier, identical at 1 ms and 10 ms budgets and at rtf 200. My probes sharpen the claim: the stable core is the player's own ~700-event wake plus a 69–116-frame dip the fleet does not own (fleet-stripped: 69 frames, worst frames pure c_player); the ~2,000 headline and the ≤ 3.1× ratio are seed- and baseline-relative. Three of six held-out predictions failed (author-reported). Adoption cost zero: two constraints for b-root-keys and b-encounter-skin.

## Reproduction (clean tree, `git apply work/patch.diff`, release build, pinned core, loadavg ≈ 1)

- Fresh panel seed 2 matches the stored CSVs within ±1 %: wake 1,929 extra events (author 1,921), 95 frames over the 5 ms budget (author 95), owners kick +561 / bound +515 / slice +3,046 / enc +46 (author +561/+515/+3,037/+46). `analyze.py` on the stored CSVs regenerates every table number: 2,112/1,921/2,016/1,938 events, ratios 2.71/3.01/2.71/2.58×, overflows 101/95/116/93, noop 0–1 events. Per-frame re-analysis confirms min rate 768 ticks/frame (0.227×), 94–116 frames below ⅓ rate (coast 0), decay-window 3.6–3.8 events/frame ≈ coast, and slice-dominant worst frames in the shipped plane.
- Determinism reproduced exactly: burn15 ×3 → `47dd9c71…`, coast ×2 → `6ed7b26b…` (the dossier's prefixes), refused = 0 everywhere, burn ≠ coast at both cut styles (positive control holds).
- Adversarial extension: the fixed-cut digest is **identical at budget 1 ms and 10 ms, and at rtf 200** (decisions stamped at canonical ticks). Exactness is budget- and schedule-independent, not merely repeat-stable.

## Predictions

Frozen at 12:55:49; first run 13:02:21; panel 13:03:43+ (mtime order; seed-1 shakeout disclosed). Held: P1, P2, P6 (on the panel seeds). Failed and honestly reported: P3 (owners), P4 (60 → ≤ 120 frames), P5 (overflow frames exist: "100× with no hitch" does not survive a held burn). Three of six held-out predictions failed, so the lab's own gold bar ("the held-out predictions held") is not met; the author's frozen band rule (HOLD needs ≤ 3×) is also marginally breached at seed 2 (3.01×).

## Adversarial cases (mine)

1. **Fleet-stripped plane** (members 48 → 4; the dossier's own falsifiable next probe, run causally): net wake 720 events — inside the predicted "player's own 500–1,100" band, so the *count* prediction holds. But the service-level dip does **not** shrink: 69 frames > 5 ms (vs 95), min rate 1,024 ticks/frame (0.3 %), and the worst frames are pure player items (c_player 5.6–6.6 ms, c_fleet = 0 ns, kick+bound only). A held-burn player item is a ~1.4–6 ms atomic (the tube recompile). The encounter skin will cut the event count, not the dip.
2. **Held-out seed 4** (never run by the author): net wake 704 events with dslice = **−1,681** — the slice term is fleet-phase noise around the burn window, not an addition; noop wakes 5 events (P6's "exactly 1" is not seed-stable); 91 frames > 5 ms; min rate 768 (0.2 %); worst 6.04 ms = 4.34× the (quiet) coast p99.9. The invariant across seeds 1–4 and both fleet sizes is the player's own ~500–1,100 kick+bound wake, the 69–116 overflow frames, the 768–1,024 ticks/frame floor, and exactness — not the 2,000-event headline or the ratio.
3. **Budget/schedule sweeps** (above): digest identity at 1/5/10 ms and rtf 100/200.

## Novelty

No prior measurement of a decision's wake: H0210/H0211's "p99 2.45–2.72 ms, no hitch" benches coast (no held burn in the loop); components-4643 priced per-kick evals. But instrument lesson 1 (canonical-tick input stamps) is already adopted ground — H0213: "Decisions are taken at logged canonical ticks (one digest over five schedules and budgets)"; law.md Ties; taleb-c271 — and the dossier cites none of it. The author adds only the API angle (`Universe::input` accepts a schedule-derived stamp); the gold-request lever over that lesson is thin.

## Goal fit

Board #4 (smoothness/allocator), priced for the first time under the wildcard. PRINCIPLES #5: "the player is the only wildcard… priority is slack, not proximity" — the measured dip is exactly the deadline-0 starvation that principle predicts, and P5's failure is a real premise correction (the hitch exists under a held burn, in the real-time factor). #12: judged by p95/p99 and overflow frames, not means. No 10× move, nothing deleted; adoption cost zero.

## The one experiment that would make it gold

Precompute the wake in idle time — the dossier's own slack-native fix — on the shipped plane: the burn program is queued at decision time (`schedule` before the loop), so spend idle frames on it and show the held L15 burn runs at ~100× with **0 overflow frames** while the fixed-cut digest stays `47dd9c71…`. My fleet-4 probe shows the precomputation must cover the player's own kick/bound items (c_player ≈ 366 ms per window; the dip survives with c_fleet = 0), so the skin alone cannot be this experiment.

## What the author missed

- **The dip's owner.** The CSV carried the per-frame cost split (cost_ns, incl. c_player/c_fleet) and the dossier never used it; read directly, it inverts "the slice term owns the worst overshoot frames": true only for the shipped plane's counts — the player's own items alone reproduce the dip.
- The headline number is not stable: 1,921–2,112 is the player's ~700-event wake plus a fleet-phase term that is +715…+3,046 on seeds 1–3 and −1,681 on seed 4. Say "~700 player-owned, ± fleet phase".
- The ≤ 3.1× service claim is baseline-relative (fleet-4: 6.8×; seed 4: 4.34×). The absolute invariant is budget + one item — 6.9 ms here, 10.92 ms at L12, 65 % of the 16.67 ms deadline; the M1 re-measure must check the deadline, not the ratio.
- P6's "exactly 1 event" is not seed-stable (seed 4: 5).
- The canonical-stamp lesson overlaps H0213 / law.md Ties, uncited.
- (Author-disclosed: 3 seeds, one geometry family; no bytes-per-body measurement.)
