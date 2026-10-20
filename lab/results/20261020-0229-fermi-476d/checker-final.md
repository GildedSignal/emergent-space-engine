Working...
Check complete. **`Grade: silver`** written to `lab/results/20261020-0229-fermi-476d/check.md`, page corrected in place, tree restored (patch reverted; only `lab/results/` untracked, as found).

**What I did:**
- **Reproduced** every dossier number from the author's own CSVs (`git apply` on clean 5908f98, rebuild, `wave_analysis.py`/`compose.py`): crest 4,633/9,814/15,231/15,578, tails 2,019/7,639, full windows 6,651/22,866/15,578, and the 1e9 arithmetic. Patch verified print-only. Timeline verified: `predictions.md` (02:39:50) precedes all decisive flights (02:40:14+).
- **Four fresh flights** (all ≤1.5 GB): three reproduction arms plus 5e4, outside the author's grid — all under load average 24 vs the author's 0.25, a dimension the author never varied.

**Findings that decided the grade:**
1. The kill of ×2.37 is **confirmed and stronger than claimed**: at load 24 the same 2e5/3e5 arms read **74/78 ms** full-window (wave beyond 600 frames, end lag 16–31 s) vs 9,814/15,686; 1e5 s17 reads **16,441 ms** with the burst at frames 965–997 — same arrival object (1.034 events/body) at 152.9 µs/event (3.2× light-load). 5e4 under load: no burst at all, amortized. Same arm now spans 6,619→16,441 ms.
2. But the run's **substituted constants are artifacts**: from the author's own CSVs, crest-window arrivals/body is **flat at 0.979/0.997/1.000** (the "falling 1.26→1.02" mixed windows: first_over 65 vs 468), and per-event cost rises **~5%/doubling** (46.7→51.9 µs), not +18%. Tail α 1.92 is a two-point estimate leaning on the 2.7 GB-pressure flight.
3. **Unreported third 1e5 flight** in the run's own folder (regen's k100000_s17: 9,011 ms) — the "1e5 agrees to 0.5%" was a two-draw coincidence.
4. P2 failed on its letter (1.596 ∉ (1.42,1.58)); P3 mis-scored ("≤0.18 held (1.02–1.26)" is false as written — only the worst-frame gulp ratio ~0.17–0.18 holds).

**Gold experiment (named in check.md):** crest anchored on game-time (gs), per-frame event counts, ≥3 flights per rung at two load regimes, one TTL-fence arm to pin the tail channel by deletion.
