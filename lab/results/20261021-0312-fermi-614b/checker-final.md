Working...
Check complete. `check.md` written; the author's wiki page corrected in place; the shared tree left clean (patch reverted); nothing else in the run folder touched.

**Grade: silver.**

**What I did:**
- **Reproduced** every dossier number from `work/patch.diff` in my own build and 7 arms (all ≤ 60 s, < 1.5 GB each): the 32.0 B × bodies chain (320,896 → 19,200,896 B), crossing-frame times, recs rungs (464 B), capture rungs, capture.max, fallback counts, rates — all match, plus `predictions.md` verifiably predates every decisive JSON.
- **Attacked**: seed 3 (law exact), N = 6×10⁵ — 2× the author's range (19,200,896 = 32.0 × 600,028 exact, capture still belt-flat at 134), and m400+belt (629/906/11,029 vs author's 628/890/11,046).
- **Found three constant-level errors**, all decidable from the run's own data: the belt chain is `pos.push([0.0;2])` (16-B entries doubling; realloc ladder 160,448 = 16 × 10,028; my backtraces resolve to universe.rs:896) — **not** `info.push`/"BodyInfo = 32 B"; capture tuples are 224 B (57,344 = 224×256), not 448; the both-in crossing is ~960 B/body ≈ 24 s of bus at 10⁹ (author's 16.5 s counts one doubling). The full-scan gate attribution is also wrong on the heaviest arm (radial fallback carries ~98% there). None overturn the laws or the wall; all corrected in the page.
- **Novelty confirmed**: the live page's od 7 was "name the burn chains' site" — named here; and 8994's 3.67/7.34 MB chains are exactly 224 × 16,384/32,768, confirming the fleet-scaling resolution.

**Not gold** because the held-out predictions did not hold (site, capture.max band, exponent — honestly reported) and the letter's mechanism constants are wrong; **the gold experiment**: one members ~10⁴ arm to recover the 8–16k-entry chains by measurement and re-issue with the corrected constants.
