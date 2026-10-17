Working...
Check complete. **Grade: gold** — `check.md` written, the author's wiki page corrected in place.

**What I did:**

1. **Found the regen illusion.** `regen.sh` passes `flights.sh "$BIN" 1000 1600 …`, but `flights.sh` consumes `$2` as `OUT` — so the runner's regen re-flew 8 arms into a stray `./1000/` dir (since cleaned) and `analyze.py` re-analyzed the author's *committed* logs; the K1000 arms never re-fly. "regen: exit 0" is deterministic re-analysis, not reproduction. Undisclosed in the dossier.

2. **Re-flew everything fresh myself** (patch applied to clean tree, full 10-arm grid + unpaced arms + an adversarial K=20,000). The flat law replicates: pooled **221 B × C (r² 0.940)** vs the author's 226 B (r² 0.974), per-arm 224–287 B/entry across C=1,028→8,296, quiet≈loaded; the K10⁴ view wall (66–74 ms gather p50) and K1000 drain bimodality replicate bit-for-class. My K=20,000 arm (C→18.5k, outside the domain) shows no superlinear blow-up (~400 B/entry, n=2) — 40× below the old extrapolation.

3. **Verified the mechanism independently:** `SCAN_BACKLOG=2048` and the per-scan `candidates Vec` confirmed in engine source; births pin ~25 kB each (n=591 frames) and held+1 frames have median catalogue growth 0 — transitions are birth-clean, and births alone account for the 26.8 MB/scan window slope that carried the superlinear reading.

4. **Predictions:** the author's own P2/P3 died exactly per their pre-stated kill criteria — the strongest pre-registration signal available. P1 held, P4 split honestly.

5. **Page corrections (5):** "decade of scenes" → one scene family/seed; unverifiable "froze at 405" → 290 committed (359–405 across reruns); Entry-pinning marked inferred; two dangling fragments from the direction-2/3 rewrites removed; the 0739-vs-crowd drain-class lead restored as still open.

The result is the integrator-named gold experiment, executed and replicated: the pin is the candidates `Vec` (224 B × C), the superlinear premise is dead, and the byte fence is adoptable in one counter — with the regen arg fix and a `candidates.len()` (not `catalogue_live`) counter required at adoption.
