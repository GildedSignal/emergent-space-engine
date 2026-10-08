Grade: gold

**Abstract.** Claim: with the angular in-band window (|Δλ| ≤ 2.5·2·e_hi + drift, range search over sorted longitudes), the unified certificate is exact on clustered phases. Every recorded line reproduced bit-for-bit in a clean tree (F1 109× evals cut, CONVOY 0 of 10,987 missed where the rank form silently missed 76%, TROJANC 7.5×, convoy honestly 2.7×, kick ratios ≈ 1 with other_added = 0). My six adversarial scenes — a convoy straddling the λ = 0/TAU wrap, e down to 1e-6 (e_hi ≪ ρ/r), a clustered swarm whose drift clamps past 64 renewals, and e = 0.5/0.55 swarms — all 0 missed. Candidates per real encounter ≈ 4.1 on the convoy: work tracks real encounters in the concentrated regime. Cost: swap the rank materialization for per-band λ range search; tier-exit-on-envelope after kicks.

## Reproduction (clean tree, `work/patch.diff` empty, crate unmodified)

- Built `exp` against the main-tree `crates/encounters` (`git status` clean). Ran every command in the dossier: F1, CONVOY, TROJANC, F2, F2 with `BANDS=1`, X, B, `W_SAFETY=0.2/0.5` on CONVOY and F1, KICKBELT, KICKCONVOY, `KICK_POLICY=exit`. All counters (pairs, evals, checks, hits, sections, missed, false, matched, kick ratios) match `scenes.jsonl` and `boundary.jsonl` exactly; only ms differ (shared machine). Each command ≤ 41 s, well under memory budget.
- Cost numbers re-derived: F1 109.3×, CONVOY 2.69×, TROJANC 7.51×, F2-maximal 41.7×, X 2.11×, B 1.00×. The four inherited cone rows match the original run's record, as claimed.
- Self-destruction reproduces: `globalrank` on B gives half-window 4.654 ≥ π → all 499,500 in-band pairs, 0 missed; the banded form stays at cone cost (808,884 vs 813,788).
- Boundary is real: W_SAFETY 0.2 → missed 1/10,987 (CONVOY), 9/275 (F1); 0.5 → 0; 1.0 → 0 everywhere.

## Predictions

Filed before the record and consistent with file times (code 13:06:39 → predictions 13:07:03 → scenes 13:07:50 → boundary 13:08:29 — exactly one clean pass of ~41 s + ~40 s, matching my own run times). Smoke runs (F1, both kick scenes) disclosed with their numbers marked. P1 held (44,977 pairs, just inside 30–45k), P2 held, P3 held (F2-maximal 372k vs predicted ~450k evals), P5 held exactly (other_added = 0, convoy 0 touches). P4 held in direction only (misses 1 and 9 at ×0.2, not hundreds) — honestly reported as an overshoot. No undisclosed scene resizing this time; the hygiene flaw of the original run is fixed.

## Attack (my six cases, all in the claimed regime)

1. **WRAP** (CONVOY's a/e, λ-cluster straddling 0/TAU): 7,893 encounters, 0 missed. The hand-rolled circular wrap branch of the range search is correct — no scene in the record ever crossed the wrap.
2. **ULTRACOLD** (σ_e = 1e-5, e_hi = 4.5e-5 < ρ/r = 1e-4): 3,879 encounters, 0 missed. This probes the window constant's coverage of the ρ/r term in the meeting bound |Δλ_mean| ≤ 2(e_i+e_j) + ρ/r: the constant 2.5·2·e_hi has no absolute ρ/r term, so its coverage relies on e_hi ≳ ρ/r.
3. **ULTRACOLD2/3** (σ_e = 2e-6 and 1e-6, renewals clamped at 64, half-window down to 1.5e-4): 0 missed both. The ρ/r exposure does not bite even three decades below it: encounters are conjunction-centred, so |Δλ_mean| at the encounter stays ≈ |Δeoc| ≈ 2(e_i+e_j).
4. **DRIFTWIDE** (clustered λ, a-spread 1e-2 → renewal need ≫ 64, 15 bands): 774 encounters, 0 missed; the tier still cuts evals 1.25×. The clamp-then-swell path is sound.
5. **HOT/HOT2** (e = 0.5/0.55 swarms, half-window 2.83/3.08, just under π): 0 missed, band ≈ cone cost — exactly the "win dies, exactness survives" the dossier disclosed, now measured at twice X's eccentricity.

## Novelty and goal fit

Not in HISTORY.md or the docs: taleb-09b5 established the phase tier with a rank certificate; the original run unified tiers but its rank-from-mean-spacing scale was killed by the convoy (silver, 76% silent miss); this run lands the angular replacement the first checker prescribed, verifies it is exact on the killer case and on a clustered Trojan cloud, keeps or improves every cost number, and adds the tier-exit kick rule. It corrects the silver's record: those numbers stand, its in-band scale does not. Board fit: the top scaling risk (candidate work must track real encounters). The unstated headline is better than the stated one — candidates per real encounter ≈ 4.1 on the convoy and 3.9 on F1 (the rank-4 order taleb-09b5 found), so total work scales with real encounters, not with N² of the candidate set. PRINCIPLES 19 ("a fix signals the wrong representation"): the rank count was the wrong representation of the window and the angular window is the geometry's own statement; PRINCIPLES 32 (the same range search serves uniform and clustered phases); PRINCIPLES 33 (the convoy pays its own true density).

## Reasons for gold, and residuals

Every number regenerates bit-for-bit; the pre-filed predictions held (P4 in direction, disclosed); my six adversarial cases, aimed where the lens was thinnest (wrap, cold, clamp, hot), all pass at 0 missed; the experiment the first checker named as "the one to gold" is run completely and holds; adoption is one step (swap the in-band materialization, add tier-exit-on-envelope). Residuals, all disclosed by the author and none blocking: the r8 v4 `isolated` gate fails its literal reading (44/45 removal-touches per 100 belt kicks, added = 0) — the deferral-to-expiry policy that would restore the letter is named but unmeasured as a running system; the kick measurement is certificate bookkeeping, not dynamics under mid-run element changes with truth re-integration (the author's own named next rung); the convoy's honest 2.7× is not 60×, and the phase tier is not yet proven the formation's sole answer at 10⁶ scale.

## What the author missed

- No wraparound test: every cluster sat away from λ = 0/TAU, and the wrap branch is hand-rolled — the single most likely place for a silent bug. It is correct (WRAP above).
- The ρ/r term: the derivation "|Δλ| ≤ 2(e_i+e_j) at a meeting" omits that the closest approach can sit ρ/r away from conjunction, and the constant's coverage of it is e-relative, never stated. It survives empirically down to e ~ 1e-6 (conjunction-centred encounters), but the margin argument now on record is incomplete, not just conservative.
- The renewal clamp (> 64) is never exercised by the record's clustered scenes; the DRIFTWIDE case shows it is sound and still profitable.
- The scaling claim is understated: "evals cut" frames the convoy as a modest 2.7×, but candidates per real encounter ≈ 4 is the number the board's top risk asks for, and it is never computed.
- The removal-touches fix (defer drops to natural expiry) is one flag away from measurable; leaving it as policy keeps the `isolated` gate red on paper.
