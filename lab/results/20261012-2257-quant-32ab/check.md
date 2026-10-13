Grade: silver

**Abstract.** The sweep's L8+ stutter is the burn-input replan waterfall (up to 1,036 player items in the frame the burn lands) priced by the O(all-bodies) player scan — not the fixed tier; `wt/frame`'s lazy re-keying cannot fix it. Reproduced on shipped code (7117f6a8): burst counts bit-identical (166/579/1,036 at L10/12/15, frame 60), paced overflows 22/36/41/55, L15 burst frame 368 ms, m400 2,475 ms, P1 remainder ≤2.4% on burn flights. Adversarial: members 200 and 60 s generalize; the pure resolve is population-flat (~143 µs at 400 members), so the growth is the scan. Silver: P2's threshold failed (60 vs 41, not ≥10×) yet is reported held; "87–91%" and "rtf-independent" overstate the author's own logs. Adopt the redirect; page corrected.

## Reproduction (clean tree, `git apply` of the examples)

- `frame_split paced 100 20 48`: overflows 1/1/1/1/1 at L-1…L6 then 22/36/41/55 at L8/10/12/15 (author 22/34/41/55; runner 22/34/40/54). Stutter reproduced.
- `frame_split demand 100 20 48`: it3_fr_max = 1/3/11/42/166/579/1036 at L-1/4/6/8/10/12/15 — **bit-identical to the author** across four independent runs (author, runner regen, mine ×2). Burst trace identical: all bursts at frame 60 (wall 1.00 s), decay over 2–4 frames. L15 worst frame 376.8 ms (author 375.2, runner 376.9). Player share of flight CPU 0.79/0.82/0.85/0.91 at L8–L15 — the author's own CSV says the same: **the dossier's "87–91%" is contradicted by the author's own log; the true range is 79–91%** (rising with level).
- P1 (the falsifier): Σcpu − Σcost_ns remainder = +2.4% (L6) … −0.4% (L15) on burn flights; +7.4% on the 252 ms coast flight (≈15.6 µs/frame — exactly the known 15 µs fixed tier). P1 holds where it matters; the fixed-tier premise for the stutter is dead by ≈4 orders of magnitude (≤19 µs vs a 368–2,475 ms frame).
- m400: L15 worst frame 2,475 ms at it3_max = 1,036, per-item 2,384 µs (author 2,228–2,946 across levels; dossier "1.8–2.45 ms" understates the top).
- Micro-probe regenerated conceptually; see defects below on its numbers.

## Held-out predictions

- P1 held, P3 held (L8 p99: 3.10 ms at r25 → 13.6 at r100 → 48.6 at r400 ≈ ∝ rtf; no flat 12 ms floor).
- **P2 did not hold as written and is reported as held.** `ev_fr_p99` at L15 = 60 against a coast baseline of 41 (1.5×, not ≥10×), and it is not monotone past L8 (113 → 66 → 62 → 60). The dossier's "Held: … P2 (event density grows with level)" re-reads the prediction's threshold down to its weakest form after the run — the same defect class that cost r3 v3 its gold.
- P4/P5/P6 failed and are reported as failed, informatively. Good.
- `predictions.md` (23:01) predates every decisive artifact (23:02–23:12). ✓

## Adversarial cases (mine, outside the author's range)

1. **rtf 1** (a decade below the swept 25–400): the waterfall spreads — it3_max = 53 at L15, worst frame 8.9 ms, under the 12 ms budget. The stutter binds at and above the sweep's flying pace. This **contradicts the dossier's "the burst item counts are rtf-independent"**: per-frame concentration scales with rtf (L12: 166 at r25 → 579 at r100 → 864 at r400 — visible in the author's own regen traces), and even totals grow (L15: 1,505 → 2,118 → 2,400 items) because a faster pace covers more flight per wall second. The page never carried this claim; the dossier must not be read as saying it.
2. **members 200** (between the author's 48 and 400): it3_max = 1,036 (same waterfall), worst frame 1,430 ms, per-item 1,365 µs — monotone in population, exactly between 433 and 2,384 µs. The scaling generalizes.
3. **60 s flights** (beyond 10–20 s): L15 survives (vmax 0.91c), the only burst remains the input frame and its decay — no second waterfall at later boundaries. Coast: p99 1.24 ms, worst 13.4 ms. The "worst frame = input frame" claim extends.
4. **Pure resolve at 400 members**: `step::process` on the player record costs ~143 µs/item — the same as at 48 members — while the universe-side item costs 2.4 ms there. The population growth is entirely the O(all-bodies) scan plus the fleet catch-up dragged inside each player item (`resolve_body`, `universe.rs:566–589`). This decomposition, which the author inferred, is now measured.

## Novelty

No prior run measured the flight regime (the wiki page's domain note said so before this run's edit; docs/HISTORY.md has no flight-sweep attribution — its "stutter" entries are the old engine's lattice/SAP work). What was known: the fixed tier is ~15 µs/frame at plane scale (762d-119f, gold) and the player scan is the p99 lever (open #7). What is new: the burn-input waterfall (one word minting 42→1,036 due items in one frame, deterministic), the refutation that lazy re-keying addresses the sweep's stutter, per-item cost flat in γ, the m400 multiplication (waterfall × scan = 2.4 s), and the F1 boundary note. HANDOFF items 2 and 5 verified verbatim: the integrator's named fix for this stutter is indeed "lazy re-keying and the incremental deadline first". This run kills that premise with measurements — the "shows that a premise is wrong" gold criterion.

## Page

Faithful fold-in structurally (new current-best block, two refuted lines, open #1 note, new open #2, #7 extended, run appended). I corrected in place: "87–91%" → 79–91%; the micro-probe numbers (coast ~29 µs; burn ~140–150 µs steady, ~390 µs in the first post-burn seconds — the dossier's "75–80 µs" is L8's overall median of a bimodal mix, not a per-snapshot median); per-item totals 430–500 µs (48) / 1.7–2.9 ms (400) with the resolve split stated; the "within 3%" claim qualified to L10+; the rtf-scaling of burst concentration added; F1's exclusion softened (only frame 60 sits at the boundary — the 50–60 ms decay tail is after second 1 — but F1's zero-lag clause catches the stutter regardless).

## Goal fit

Moves `frame-cost` by killing the assumed lever for the sweep's stutter and redirecting it to two already-open directions (#2 spread the waterfall — digest-safe by the 2517 schedule-independence gold; #7 replace the scan). PRINCIPLES #19: "a fix signals the wrong representation… if you find yourself fixing things that's oftentimes a signal that it is the wrong representation" — fixing the L8+ stutter with re-keying would be the bandaid. And #3, "Compute only surprises": the burn input is the only surprise in these flights. Adoption is a decision, not a build.

## Why silver, and the one step to gold

The physics and the redirect are gold-grade and fully reproduced. The record is not: one prediction outcome is misreported (P2 held → actually failed at its threshold), and three secondary numbers are contradicted by the author's own logs ("87–91%", "within 3% at every level ≥ 6", "burst item counts are rtf-independent", plus the "75–80 µs" resolve). Under this lab's precedent (r3 v3: solid physics, undisclosed metric redefinition → silver; "a headline the log contradicts… the run loses its grade"), that is silver. **The one step to gold:** re-fly the strict thresholds with corrected, pre-registered wording (P2's density on a second seed; the share range; the rtf-scaling of burst counts) — a 30-minute rerun of the same harness; no new physics is needed, and this check plus the corrected page already carry the honest numbers.

## What the author missed

- Why one thrust word mints ~1,000 due items (the replan semantics inside `input()` — the author names this as "one question deeper" and leaves it; it decides *how* to spread the waterfall).
- Other input patterns (reverse, turns, key mashing — all in the shipped sweep's flight list) and a second seed; the rtf dependence of the burst concentration.
- The r400 flights die early (frames 61–69, alive=false) — unmentioned in the dossier.
- The paced `player_items` probe flights lag (12 ms budget inside the probe), so their speed trajectory differs from the demand flights the CSVs are compared against.
