Working...
Check complete. `check.md` written to the run folder — nothing else touched, no commits.

**Grade: silver**

**What held under reproduction and attack:**
- `python3 probe.py` in a clean tree: **bit-identical** to the stored `probe-out.json` (12.5 s, ~30 MB). All dossier numbers exact (+69% fast e₀=0.05, −33% slow e₀=0.2; labels matched 8/8).
- Predictions genuinely pre-registered (06:23 vs output 06:29); held-out e₀=0.05 prediction held, two others failed and were honestly reported.
- My adversarial round **strengthened** the core claim: errors persist at half step (+64%/−33%); from a 4W start (the author's 2W start makes any gate ≥±2W degenerate — it never switches) **no fixed width in {1,2,3}W passes the author's own 25% bar** (worst −48/−27/−42%); a clean 3:2 run gives −52%/−90%. Half-step and threshold sweeps both done.
- Novelty verified: no chirp or gate-crossing test exists anywhere in docs/, lab/rungs/ or HISTORY; r4 v3 and B17 sit at fixed detunings. The doc-staleness attack checks out line-for-line (representation.md still teaches the killed Minsky map; r5/r6 promised, never frozen).

**Why not gold:**
- The outside branch is a linear-fit frozen-e **stand-in**, not the design's orbit-averaged kick layer — the same reason the 29 Sep premise red-team capped at silver ("claims must be measured on the design's cheap path").
- The dossier's stated **mechanism is a threshold artifact**: the "reach" numbers (1.9W at e₀=0.005) move to 1.07W when the response threshold rises 8×, and are polluted by osculating-a swings of ±W inside the pumped zone. The conclusion survives on outcome evidence, for a different reason: missed pumping plus a handoff-phase channel (error non-monotone in gate width) the author didn't isolate.

**Gold-making experiment:** r4 v4 on the real cheap path, chirping 2:1 and 3:2 as proposed, plus an error-vs-gate-width curve at fixed 4W start to separate the two failure channels.
