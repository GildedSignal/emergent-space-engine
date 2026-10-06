Grade: silver

# Check — 20261006-0737-scout-b73e (checker: independent GLM, 30 min)
 
**Abstract.** The claim reproduces. Clean tree + `work/patch.diff`, `cargo build --release -p xtask --offline`, the dossier's five commands: fixed 5 ms → 0 hitches but RTF lo1 0.000 (58 overflows); fixed 13 ms → lo1 3.53 but 37 hitches; AIMD and work-ahead dominated, same order as reported. Every discipline, seed and budget gives one digest bit-identically (87f51de403a46799 at seed 1; 0c9bbe61… at seed 7; c0e6a443… at members 200; b411cce8… at rtf 1) — schedule-independence holds under policy churn and 10-way load. My held-out runs (seed 7, members 200, patched rtf 1) and an interior sweep (7/9/11 ms: 0 hitches at 7 with lo1 0.023; 5 hitches at 9 with lo1 2.9) confirm the knee is structural, not endpoint noise. No 10×: it kills four session-layer disciplines and fixes the target. Adopt the knee and the digest control; none of the policies. (~115 words)

## Reasons

1. **Reproduction.** Built from the patch in the restored tree; all five core commands re-run serially (seed 1, members 400, rtf 4). Digest `87f51de403a46799` identical across fixed 5/13, aimd, ahead, both — matches the dossier's `87f51de403a4…`. Overflows reproduce (58 vs author 55–56 at fixed 5; 25 vs 18–27 at fixed 13; 73 vs 72–77 for both). Hitch *patterns* reproduce (fixed 5: 0; fixed 13: 37 counts here vs 19–25 author; box load 2.5–6.6 from the window's other runs — orders of magnitude agree, per the lab's cloud-timing rule).
2. **Unit defect (found).** The evidence tables' "hitch>16.7/h" column holds raw `hitch_counts` (frames), not per-hour rates: `Dash` divides counts by wall-seconds/3600, so 19–25 counts in a 30 s run is ~2,300–3,000/h, ×120 off. The comparisons are unaffected; the dossier's "19–25 hitches/h" mislabels its own JSON.
3. **Predictions.** `predictions.md` (07:46) precedes `evidence.md` (07:59); the tuned-on case is disclosed as pre-measured. P1/P2 failures are reported honestly, and the digest control (the prediction that mattered) held. The held-out rows (seed 7, members 200) were never run by the author (disclosed); I ran them: seed 7 clean serial gives fixed 5 → 0 hitches, lo1 0.011; fixed 13 → 17 counts, lo1 4.000; members 200 gives fixed 5 → lo1 0.0 vs fixed 13 → lo1 3.89. Direction identical to seed 1 — sign robustness holds.
4. **Attacks.**
   - *Knee interior* (the claim's biggest hole: "no constant meets both halves" was measured only at 5 and 13): caps 7/9/11 give 0/5/11 hitches with lo1 0.023/2.95/3.82. The knee is real and tight; no interior cap meets both halves. This strengthens the claim beyond what the author measured.
   - *Load*: 10 benches concurrently — digests bit-identical to serial runs; frame-time metrics inflate (as expected), digest control is load-proof.
   - *The unbinding check*: the author ran it pre-patch with the stock binary (disclosed), so prediction 6 was untested. Patched rtf-1 members-48 runs: fixed/aimd/ahead all p99 ≤ 4.3 ms, 0 hitches, one digest — prediction 6 holds.
   - *Ahead's RTF metric*: the dashboard records `f.ticks` from inside `frame_to`, before the v2 clamp rewinds `u.now`, so ahead's reported RTF is the frontier's rate, not the presented clock's (median 4.28 vs 4.00 at rtf 4; 1.29 vs 1.00 at rtf 1 — in both my runs and the author's tables, unexplained). The kill still stands: a frame recording ≈0 ticks has frontier ≈ previous presented tick, so presentation gained ≈0 too — lo1 0.000 does imply presented dips. The code reading also confirms v2 is a faithful audio split, not a strawman: the clamp touches only `u.now`; `advance` works off the event queue, so resolved lead persists as real inventory.
5. **Novelty.** No plane-era prior measures the budget knee or transplants session-level disciplines (H0210–H0214). But the dossier cites no in-repo prior: H0164–H0168's allocator era already listed "least-slack, SITA lanes, AIMD windows" as scheduler lessons (pre-pivot, different engine — the transplant's failure is a new measurement, the idea was not new), and H0213's tail regression (hitches 33–51 ms) is the live motivation, unmentioned. The digest control extends plane.md foundation 7 / H0210's "one digest across budgets and threads" to per-frame budget churn and lead-clamping.
6. **Goal fit.** Board §4 (smoothness and the allocator), principle 12. Honest negative result: "A failed experiment kills that configuration, never the method" (9). Not gold: no bottleneck moves 10×, nothing is deleted from `main` (the policies were never in it), and the structural mechanism — bursts are resolution cascades longer than any rebuildable lead — is *inferred* from lo1/overflow patterns, never measured directly (no burst-length distribution anywhere in the artifacts).

## The one experiment that would make it gold

Measure the cascade itself, on the plane's own bursts: log each resolution cascade's length in game time (events from first surprise to quiescence) and compare it to the lead rebuildable from idle frames (spare budget × idle frames ÷ rtf). If cascades exceed the rebuildable lead by the tens of frames the dossier asserts, the session-layer kill becomes a measured law with a number, and the engine-side target (peek/cheapen the cascade) gets its required gain — adoptable in one step by the motion-law work. Building the one-frame lookahead probe is the stronger version.

## What the author missed

- The knee's interior (asserted "no constant meets both halves" from two endpoints; 7/9/11 ms close it).
- The hitch units in both tables are frames, not per-hour (×120).
- The ahead RTF median inflation is a dashboard artifact (pre-clamp frontier ticks), present in the author's own tables and unexplained.
- Batch-1 (v1) numbers cannot be regenerated from the shipped patch (v2 only) — the lab's own 5 October lesson about regenerable records.
- No in-repo prior citations (H0164–H0168, H0213).
- The rtf-1 unbinding check ran the stock binary, so prediction 6 shipped untested (I tested it; it holds).
