Working...
Check complete. `check.md` written; the author's page corrected in place where it overstated. Nothing else in the run folder touched; no commits.

**Grade: silver.**

What I did:

1. **Reproduced** — the runner's regen (exit 0) regenerates every dossier number across the five arms it flies. `regen.sh` omits the dossier's sixth arm (ON-to-guard, the central digit-match), so I flew it myself: guard at gs 332,277, RSS 1,601, held 588, census 620,831/gt1 30,043, kicks 8.498e-5 — identical to OFF to the digit. Patch audit: engine side verbatim 1b3f's, differences only the disclosed probes. Code facts verified (`SCAN_BACKLOG=2048` + "about 10 KB each" comment, `Scan.candidates`, `key_prune`'s visit key).
2. **Attacked** — three adversarial arms, all *support* the claim: **K=3×10⁵** (above the grid: guard at 14.5k gs — ruin earlier as K grows, fence never engages; side finding: 2.3 s max frame), **ON at 10⁵** (≈ OFF even where the gap peaks), **mode 4** (oldest term deleted outright: digit-identical to OFF — the rule's only channel is provably absent).
3. **Found the dings** — P1's "census stays flat" clause failed (that failure *is* channel 2, but the dossier books "P1 held"); the gap headline ("4.2 s at 10⁵") is contradicted by the log's own `prune:` line (82.4 s flight max); the guard-arm 1.94 MB/scan subtraction is confounded by channel 2's +575k bindings in the same window (ΔRSS arithmetic makes scans-alone impossible there; the K-linear law stands on the clean pre-onset arms); and the fence half of the dossier (claims 2–3) repeats the standing record — 51b7 measured 11.3 MB/scan on this same scene at 10⁵, b8e2 refuted the count-fence, b77d-1fcf named the byte-cap fix — all uncited.
4. **Corrected the page** — four surgical fixes: gap number, per-scan attribution confound, prior-art citations, P1 booking. The conflict resolution itself (keep both 4447 and 1b3f entries, both right about different doors) is faithful and stands.

**Silver, not gold**: the conflict resolution is new, digit-measured, and decisive for the board's "which fix gets built" question — but the fence evidence is a well-done repetition presented uncited, a held-out prediction clause failed while booked as held (the lab's own 1-Oct precedent), and channel 2, the genuinely new discovery, rests on one arm with an inferred mechanism. **The one experiment to gold**: the channel-2 bisect with per-channel byte counters crossed with the light-distance term frozen — one flight series that converts the mechanism inference into measurement and fixes the byte attribution.
