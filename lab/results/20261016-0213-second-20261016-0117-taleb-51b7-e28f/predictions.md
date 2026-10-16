# Predictions (written before the decisive arms)

Tuned on: the 10³ smoke only (`beltburn 4` budget-on; `beltburn 3 100 10000` A/B — digest
`5a2dd13c` ×4, mints 1 vs 212). The arms below were not run when this was written.

The cure: `Scan.candidates` behind an `Arc`, shared with the last scan when every entry is the
same (`same()` per entry — the same invariant the shipped reuse rule trusts); `SCAN_SHARE=0`
restores the shipped mint inside the same binary. The answer's inputs are `t`, `me`, `interval`,
`candidates`; a shared snapshot passes `same()` entry-wise, so answers are bit-identical.

1. **Identity (budget-free arms, the trusted digest class):** SHARE=0 and SHARE=1 give the same
   digest at 10³ (3 s), 10⁴ (8 s) and 10⁵ (2 s, unfenced under SHARE=0: ~60 burn frames ×
   11.3 MB + 252 MB build < 1.9 GB). The 10⁴ arm also equals the record's budget-free digest
   `73972744…` (same arm, same box). If it does not, the wall coupling (not the cure) is the
   suspect: SHARE=0 run twice must then decide.
2. **The mint:** on every burn arm with the cure, `mints = 1` and `shares ≈ burn frames`
   (the belt's own re-key window is at 13–14.5k game-s; the arms end ≤ 2.5k game-s; the
   player's burn wave is below one quantum for belt bodies). If bodies near the player re-key,
   mints > 1 and the drop shrinks accordingly — reported as measured.
3. **The drop:** on the 10⁴ budget-free 20-s arm (1200 frames, 1140 burn frames), the mint
   drops by the count ratio 1140× ≥ 10³×, and by bytes ~1.27 GB shipped vs ~1.1 MB cured.
   On the 10⁵ 12-s arm the shipped run fenced at 148 scans (the record); the cured run
   completes all ~660 burn frames, RSS end ≈ build + one snapshot (260–290 MB), held ≈ +1/frame,
   no fence.
4. **The answer bill, measured:** on the 10⁵ cured arm the end-of-run flush answers ~660
   distinct scans; ans/scan lands at the extrapolated 150–190 ms (encounters.md's 1.5–1.9 µs/body
   × 100k). All answers empty (enc = 0 at belt radii) — the bill is paid and buys nothing.
5. **The shipped plane untouched:** quiet 10⁴ digest = the record's `612c1388…`; `ladder_digest`
   pristine values equal (`4b822570…`, `6895ce06…`, `df0e87cd…`); crate tests pass.
6. **Standing costs unchanged:** p50 at 10⁵ burn stays 28–34 ms (the capture walk is still
   paid; the per-frame entry comparison adds ≤ 0.5 ms at 10⁵); frame over-count and lag stay
   the shipped arm's class; the count cap (2048) still never engages inside 12 s.

Kill criterion for the cure: any budget-free A/B digest mismatch that persists when SHARE=0
is run twice (then the cure changes the answers, and the run reports that honestly).
