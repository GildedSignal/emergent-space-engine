Grade: gold

**Abstract.** The design's kink law — "in a field, E and L change by the work done" (four copies: representation.md L50, law.md:42, plane.md:21, thrust.rs L7's comment) — is dead as written; the shipped `burn` is exact and implements something else; no rung has ever judged thrust. Every number regenerates in 0.7 s: the letter under-reads ΔE/ΔL at 0.43–0.97 over r = 6–10⁴ M and over-calls the escape burn 3.04× at 6 M. Blind attacks only deepen it: sign flips on infall/eccentric events, 0.059 flat at γ 2.3, 0.09 at 3.5 M. Gain: a wrong law sentence deleted before builders implement it, replaced by ΔE = √f·Δγ (one multiply-add). Cost: four sentence edits plus one comment; no engine change.

## Reasons

**Reproduction.** `regen.sh` exits 0 and every dossier number matches exactly: the 12 letter ratios (0.6248/0.5228 flat; 0.5101/0.4269 at 6 M … 0.9971/0.9511 at 10⁴ M), escape over-calls ×3.042/1.610/1.219/1.036, radial ΔL +3.14 % of L₀, held-heading E 0.94570 vs 0.94138, flush deferral −0.184 % → −0.047 % (×3.95) and −0.0016 % → −0.0004 % (×3.98). `work/patch.diff` is empty — no tree edits, as claimed.

**Provenance verified in the shipped tree.** The sentence is verbatim in all four places. `thrust.rs::burn` (read line-by-line) converts to the static orthonormal frame (v̂_r = v_r/f, v̂_t = v_t/√f), composes the exact boost `u2 = u·cosh η + (n + u(u·n)/(γ+1))·sinh η`, converts back — it never computes work. The float replica matches this algebra term-for-term; I re-derived the |along|² = 1 + (u·n)² identity by hand (felt-α clause holds). None of the 15 rung files contains thrust/burn/rapidity.

**Predictions.** `predictions.md` (02:24) precedes the final script (02:43) and results (02:59). P3 held decisively (0.0–1.3e-13 vs <1e-12). P2 held at 6 M (0.427 vs 0.4–0.6); its escape sub-claim failed in direction, was disclosed, and the correction is right — I verified analytically that E = √f·γ = 1 ⇒ w_esc = √(2M/r) local and η_esc(6 M) = 0.1092, matching the code. P1 failed toward a *stronger* kill (SR channel). P4 held (refinement 3.95×, first order, reported as marginal honestly).

**My attacks (all outside the author's grid, all confirmatory).**
1. Deeper radii: letter ratio 0.189 at 4 M, 0.092 at 3.5 M, 0.030 at 3.2 M (photon sphere at 3 M); shipped replica ≤ 1.1e-15 everywhere.
2. Non-circular starts: on an E = 1 radial-infall event at 6 M the letter flips ΔE's **sign** (−0.17); an eccentric-event radial burn reads ΔL at **−0.33**; 45° attitude 0.52. The kill is not just magnitude.
3. High-γ flat: 0.059 at γ 2.3, 0.0019 at γ 7 — the player's own regime (the record's flight is at 0.89c; a held burn reaches γ 1,761). Retrograde is exactly symmetric (0.4269 = prograde).
4. The shipped `cosh_sinh` is a 6th-order truncation the float replica cannot see: its error is 0.0 at the engine's per-flush η ≤ 2⁻⁶, 3.7e-10 at η = 0.25, and breaks (7e-2) only at single-shot η = 4, which the flush-quantum policy forbids. "The code is exact" holds in its operating domain; I scoped this on the page.
5. FW vs compass: the dossier's "coincide to ~1e-5" is an artifact — the q = 2⁻⁸ lump sits 1.79e-4 from its own continuous FW limit and happens to land 4.1e-7 from the compass law; the true continuous gap is 1.79e-4 ≈ 14 % of ΔE. This *strengthens* the under-determination claim (the two clause-1-consistent readings differ), and the page already carries the correction, which I verified numerically. This is the dossier's one wrong sentence.

**Novelty.** The live `representation-premises` page had zero thrust coverage; HISTORY's thrust entries (H3074 "thrust as rapidity kinks", H3186 held-burn clock cap, H3200) are feature and validation work — none judges the sentence against a GR oracle. Novel.

**Goal fit.** Gold path "shows that a premise is wrong": a load-bearing sentence of the law section, repeated in four places, measured dead on two stacked channels, with the exact replacement being *simpler* — ΔE = √f·Δγ is principle 3's own additive form ("Every quantity is kept in the form in which its change is an addition"), and principle 30 makes navigation the thing that "needs to be perfect". Adoptable in one step: four sentence edits and one doc comment; the engine changes nothing.

**Page corrections made (checker2, in place).** Fixed the wrong "0.19–0.24 at r=3.5–4M" range (true: 0.19–0.24 at 4 M, 0.09–0.12 at 3.5 M) in both places; fixed "deepens outward" → toward the hole; added the blind-verification bracket (sign flips, high-γ, cosh_sinh scoping) to the Refuted entry; deduplicated the Runs section 48 → 18 lines (duplicates inherited from the live page; one line per run restored). Page now 186 lines, current best 6 lines — within budgets.

## What the author missed

- The FW/compass "~1e-5 coincidence" compared an unconverged q = 2⁻⁸ lump against the *other* law's continuous limit; the two continuous readings differ by 1.8e-4 (≈14 % of ΔE). Secondary, and it strengthens the claim, but it is an error in the dossier.
- The shipped integer `cosh_sinh` truncation was invisible to the float replica; harmless in the engine's operating domain, but "the code is exact" needed that scope.
- The flush-cadence model approximates the engine's `thrust_step` floor (author: local circular speed √(M/(r−2M)); engine: max(|v|, 1/r) coordinate) — immaterial to the first-order-in-q conclusion, but it is a model, not the shipped step.
- Sign errors (infall, eccentric radial) are the cleanest player-visible refutation and went unmeasured; measured now on the page.
