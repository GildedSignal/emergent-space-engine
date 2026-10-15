Working...
Check complete — `check.md` written, the author's wiki page corrected in place, nothing outside the run folder touched.

**Grade: silver.**

**What I did:**
- **Reproduced**: ran `regen.sh` myself — 158 s, `CERTIFICATE: PASS`, every counter and digest identical to the dossier (demotions 93,200/91,212/273,200/89,843; promotions 1.66 M/2.11 M/2.38 M/1.56 M; rss 545→377 MB; `b_per_body` 1,603→1,002). Binary sha256 matches the disclosure; its lazy-off arms reproduce the scout's three digests bit for bit.
- **Verified the certificate's mechanism**: the shipped digest (`universe.rs:1266`) hashes key/tube/residual/carry/plan state, never `Arc` addresses, so control-vs-lazy equality is a state certificate; and the wall delta closes on the bill (10⁵: Δ10.6 s ≈ 2.38 M promotions × 4.6 µs) — the promotions are real flight-path work.
- **Attacked beyond the author's domain** (N ≤ 10⁵, ≤ 48 k game-s, seeds 1/7): **N=2×10⁵** (digest `933403d7…` identical, rss −31% again, 6.7 prom/dem), **seed 13** (`48abb970…` identical), **96 k game-s** (`e75c90f2…` identical, rss flat through ~3.5 waves). All hold.
- **Predictions**: 1/2/3/5 held (5 beat); 4 split exactly as disclosed; `predictions.md` (04:10) predates the dossier (04:33).
- **Page**: corrected one overstatement — "2.4–15.1 cores" quotes one run's printout; the instrument's own number spans 2.3–20.3 with the run's p50 compile (worst arm the 10⁴ burn), and the dossier's "× 6.5 µs" multiplier matches no printout. Folded my note + adversarial arms in.

**Why not gold**: `work/patch.diff` and `work/fix.diff` are both 0 bytes (verified) — the seam and instrument source exist nowhere (not in the tree, not on the scout's branch, not recoverable from the cargo target). `regen.sh` works only from a prebuilt off-repo binary and FATALs on any fresh clone; adoption requires re-deriving 10 files from prose. That is the lab's named silver pattern — short on the record, not the physics. **The one build to gold**: re-derive the seam, commit the diff, re-fly from source.
