Grade: gold

**Abstract.** Claim: 3eb3's "kick machinery, 5.3–9.9 KB/kick" wall at the 10⁵ rung is the
interstellar held-scan channel; with e181's TTL fence the rung flies 3.3× further at 2.5× less
memory, and no per-kick memory law exists. Reproduced in a clean tree to the digit (guard
f≈22101, gs 36,834–835, rss 1,619 MB, held 171, scan_cand 9,846,528; fence arm 72,000 frames,
end 635 MB, no guard; 3eb3's subtraction reproduces at 7.2 KB/kick). My distinct-`Arc` census
closes the ledger directly: 84 distinct scans pin 1,058 MB = **82% of the wall**, + hist 218 +
store 19 = 101% of Δrss. A coast arm at 10⁵ (701k kicks, shipped loop, rss 484 MB, held 0)
kills the per-kick reading without the fence. K-linear to 3×10⁵ (cand_max 299,715 = K−313).
Adoption: print-only census free; the fence is a law change owing the digest re-freeze.

## Reasons

**1. Reproduction (clean tree, `git apply work/patch.diff`, my own four flights + regen
commands).** Every deterministic digit identical to the dossier and the runner's regen: arm A
guard f=22101–22102, gs 36,834–36,835 (frame diff is when rss crosses 1.6 GB intra-flight),
rss 1,619 MB, kicks 157,705, hist_total 106,309, held 171, scan_cand 9,846,528, scan_mb 2,206,
cand_max 99,716; arm B completes all 72,000 frames (120,000 game-s), end rss 635 MB, peak
(VmHWM) = 635 = end rss — the probe-cadence worry the author pre-named is covered; arms C/D
match (209/558 MB). Schedule-elastic digits vary as the dossier discloses: mints/expired
2910/499 (mine), 2913/459 (runner), 2910/400 (author); encounters 3,955 (B) vs 3,986 (A at its
guard). 3eb3's subtraction reproduces: (1,619−262−218)/157,705 = **7.2 KB/kick**, inside their
5.3–9.9 band.

**2. Predictions.** Written 19:14, before the flights (logs first existed 19:17; the author's
logs were later overwritten by regens, but two independent regens reproduce the deterministic
digits bit-for-bit, so the comparison stands). **P1 held** (≥60%: my direct count gives 82%,
see §3). **P2 held** (7.2 ∈ [3,12]). **P3 half-held**, disclosed exactly as measured: identity
holds at every probe, rss < 850 (635), but the letter's slope fails on the history wave steps
(my arm B: quiescent 26k–92k slope 0.067 MB/1k gs; steps +85 MB at gs ~100k). **P4 held in
substance only**: the registered residual(t) = rss − base − Δstore − scan_mb never subtracted
hist, so its letter (<0.3 KB/kick vs measured 0.35) was mis-registered from the start —
disclosed. The named falsifier ("staircases ≥ +1 MB/1k gs with scans expired and store flat")
does fire in its strict letter during wave steps (my arm B gs 98k→100k: +54 MB/2k gs, scan 0,
store +7) — but the same windows show hist +30k bindings: the stairs are the history channel,
not kick machinery. The substance (no retained per-kick machinery) survives every attribution:
honest bound 0.09–0.25 KB/kick over 576k kicks, ≥20× under the killed band.

**3. Attack (three adversarial arms of my own; one outside both the author's and the first
checker's grids).**
- **X3 — the instrument (distinct-`Arc` census, my patch, print-only).** At gs 36,028: 166
  deque entries hold **84 distinct scans** (entries/distinct = 1.98 — b911's ×1.99–2.00 law,
  now measured at 10⁵), pinning 4,724,734 distinct candidates × 224 B = **1,058 MB**, with hist
  218 MB and store Δ19 MB: the three channels sum to 1,295 MB against Δrss 1,289 MB (**101%
  closure**). The census's summed-candidates figure (2,206 MB) is exactly the disclosed
  over-count (×2 reuse), and the scan channel is **82% of the wall by direct allocation
  counting**, not subtraction. The author's "82–100%" is honest and now measured.
- **X2 — the scene edge (10⁵, coast, shipped loop, 60 s cap).** 80,404 frames, 132,110 game-s,
  **701,422 kicks**, rss 484 MB, held 0 at every late probe, all 12,973 mints answered. The
  same binary and K, 4.5× arm A's kicks, no wall: a 5.3–9.9 KB/kick law would have pinned
  3.7–6.9 GB. The wall needs the interstellar departure (the player leaves the SOI at frame
  948), exactly the mechanism claimed; the claim's domain is scene-stated and this control
  passes on the right side.
- **X1 — outside both grids (3×10⁵, shipped).** Guard at gs 18,655, rss 1,639 MB; scan_cand_max
  **299,715 = K+28−313 exactly** (the K-linear law: 29,715 / 99,716 / 199,715 / 299,715 at
  3×10⁴/10⁵/2×10⁵/3×10⁵); first-wave frames now cost 2,188 ms max (2×10⁵: 1.2–1.3 s) — the
  next wall at that rung is compute, confirming the first checker's observation one rung up.

**4. Novelty.** The fence (e181), the byte-cap-not-count-cap fix (b77d-1fcf, 527a) and the
per-scan pinning at 10⁵ (527a: 7.36 MB/scan; e181: 12.7 MB/scan) are all prior art and all
cited by the author. The novel core is the refutation of the standing wiki reading — 3eb3's
"the wall is kick machinery, the 10⁵–10⁹ premise is inverted", which the live `lab/wiki/nladder.md`
still carries — via the channel decomposition, the collinearity mechanism (kicks and held scans
turn on in the same first-wave window), the no-per-kick-law bound, and the fence flying the
10⁵ rung 120k game-s (2.9× past e181's 41.9k fence arm). No prior run did this decomposition;
527a measured the channel before 3eb3's subtraction reading existed. Not a repetition.

**5. The page.** `wiki/nladder.md` folds the result in faithfully, with the first checker's
corrections inline (the 2.1 KB×hist double-count vs `bytes_of`, per-binding 1.3–1.9 KB on this
tree — my own wave-step measurement gives 1.67 KB/binding, so ≲0.15 KB/kick stands; the
schedule-elastic identity split; P3/P4 letter failures disclosed). It flags rather than hides
the one real tension: 3eb3's split bought 2.30× wall-life at 10⁵, which the scan-channel
reading cannot explain directly — the page names the missing measurement. No overstatement
found; no in-place correction needed. Not a closing run (one gold on the topic so far among
these; the page's older blocks disagree by construction until the next run re-reads the 2.30×).

**6. Goal fit.** Board bottleneck #1 (bodies in the flyable engine; "which term breaks first
as the plane grows... measured on shipped code at 10³–10⁶"): the run answers it for 10⁵ — the
term that breaks is the held-scan channel, with a measured fix, and the "premise inverted"
consequence that would have re-priced the whole 10⁵–10⁹ column is dead. PRINCIPLES: "Compute
only surprises... nothing is evolved that can be derived when looked at" — a scan whose player
has left the system at ~c holding 100k candidates is work for no reason; the fence deletes a
channel that grows without bound rather than numerically bounding it ("errors never compound"
in the structural sense of 4447).

## The one experiment that would make it more

Fly the split arm (88e9's `BELT_SPLIT`) at 10⁵ under this census: if the scan channel is
untouched there (as at 3×10⁴), 3eb3's 2.30× wall-life must ride binding churn into the reuse
rate — the missing link between the two same-day readings; if the scan channel shrinks, the
collinearity story gains a second mechanism. Already named on the page as the next step.

## What the author missed

- The distinct-scan count was one `Arc::as_ptr` away from turning their 82–100% subtraction
  bound into a direct measurement (done here: 82%, 101% ledger closure, ×1.98 reuse law).
- The coast control: one cheap flight that kills the per-kick reading with the fence entirely
  out of the picture (done here).
- The P4 residual's registration flaw (hist never subtracted) is disclosed but was knowable
  before the flight from the formula alone.
- The fence's front-only expiry assumes mint ticks are non-decreasing in deque order — true on
  this engine (verified in code: `now` is monotone, `capture` runs at frame ticks), but one
  sentence in the dossier would have closed it.
