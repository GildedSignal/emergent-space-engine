Working...
**Grade: gold** — `check2.md` written, author's page corrected in place.

**Verification performed (blind, ~15 min):**

- **Reproduction:** `regen.sh` exits 0; all 30+ dossier numbers match exactly (letter ratios 0.6248…0.9971, escape ×3.042/1.610/1.219/1.036, radial ΔL +3.14%, flush ×3.95/×3.98). `patch.diff` empty as claimed.
- **Provenance:** the sentence is verbatim in all four places (`representation.md` §2, `law.md:42`, `plane.md:21`, `thrust.rs`'s comment); the shipped `burn` line-by-line does a local exact boost, never work; no rung (15 files) mentions thrust. Predictions (02:24) precede the decisive run (02:59).
- **My attacks, all outside the author's grid:** letter ratio 0.189/0.092/0.030 at r=4/3.5/3.2 M; **sign flips** (−0.17 ΔE on an E=1 infall event at 6 M, −0.33 ΔL on an eccentric radial burn); 0.059 flat at γ 2.3, 0.0019 at γ 7 — the player's own flight regime; replica exact ≤3e-15 everywhere; shipped `cosh_sinh` truncation is 0.0 at the engine's per-flush η≤2⁻⁶ (exactness holds in the operating domain).
- **One dossier error found and confirmed:** the "FW/compass coincide to ~1e-5" line is an artifact — the q=2⁻⁸ lump sits 1.79e-4 from its own continuous limit and coincidentally 4.1e-7 from the compass law; true gap 1.79e-4 ≈ 14% of ΔE. It strengthens the under-determination claim; the page already carried this correction, now numerically verified by me.

**Page corrections (in place):** fixed the wrong "0.19–0.24 at r=3.5–4M" range (true: 0.09–0.12 at 3.5 M) in both occurrences, fixed "deepens outward"→toward the hole, added my blind-verification bracket to Refuted, deduped Runs 48→18 (inherited duplicates). Page: 186 lines, current best 6 — within budgets.

Gold because: reproduced, the load-bearing predictions held (misses disclosed, one corrected by the author's own control and confirmed analytically by me), a premise of the law is shown wrong on two stacked channels with sign errors, and adoption is four sentence edits + one comment with zero engine change.
