Working...
Check complete. `check2.md` written; tree restored (patch reversed, probe deleted; only untracked `lab/results/` remains, untouched except `check2.md`).

**Verdict: gold.**

What I did and found:

1. **Reproduced everything** from a clean tree + `work/patch.diff`: `belts`, `fleet`, `adj`, `ranks` all regenerate `evidence.log` bit for bit — adj's `d_min` identical to 15 digits (4 missed of 233 true encounters, 193 extra all true, 0 false). The log's odd interleaving resolved cleanly: `rank_probe` prints its adjudicate before its summary, and `method_too=false` probes report "missed" against an empty method set.
2. **Predictions** were written 17+ minutes before any evidence; three of six failed, each disclosed — the failed "zero misses holds" *is* the headline.
3. **Attacks confirmed and strengthened the claim**: a sound true-longitude brute (fixing the equation-of-center blind axis the author disclosed) on fresh seeds 31–33 gives method misses 3/232, 5/238, 2/234 with zero false positives; the rank guard held on ~1,100 further encounters including my e-spread 1000×ρ case (r_max ≤ 4, mostly 1).
4. **One correction**: the miss mechanism is misattributed. My probe shows the missed pairs are standing proximities (synodic drift ≈ 0.4ρ/orbit) — sections *are* built with wide windows, `run_section` still returns zero hits. The second tier's event model (windowed conjunctions) has no event for pairs that never conjunct; the fix is a persistent-proximity certificate, not a wider window.
5. **Novelty**: `q-candidate-degree` (`eaac72b`, adopted silver) answered fixed density only; nothing in HISTORY/docs touches concentration, co-orbital regimes, or train certificates. This run corrects a premise of already-adopted work — the gold criterion.
