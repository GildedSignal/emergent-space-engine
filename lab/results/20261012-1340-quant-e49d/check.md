Grade: silver

Abstract: Claim: one kick's wake in the Binet-cone tier is O(N) single-thread (6.6–6.9 ms at N=10⁴, slope 1.04; full 16.7 ms frame at N≈2.4×10⁴), the queued slack skin cannot absorb player burns (skippable 0.95→0.0025 from δa/a 1e-9→1e-3, with exactness violations), and ~98% of the wake is deferrable by deadline. Reproduced bit-for-bit on every deterministic field (both experiments, shared-runner timing noise only); skin boundary re-confirmed on a fresh seed (violations 6 at 1e-3, 3 at 1e-2). Adversarial: the deadline 1/|Δn| is the synodic *period*, not the first conjunction — 11.3% of pairs (not ~0%) first conjunct within 10 orbits and 0.8% encounter *before* their assigned deadline. Phase-aware fix is one line; the stream conclusion survives. Cost to adopt: two scheduling rules for `b-encounter-skin`; nothing built.

## Reproduction

Clean tree, `work/patch.diff` empty (edits live in `work/encounters`; diff vs `crates/encounters` is packaging plus exactly one added experiment `burn()` and one match arm — no hidden edits). Built and ran both commands in a /tmp copy:

- `kick`: pairs_per_kick 812.8/812.9/812.8, changed/flipped/skippable fractions and all 5 slack_skip_violations at eps=1e-3 **identical to every digit**; only us_per_kick differs (7.2–7.7 ms, load).
- `burn`: all 16 lines identical on pairs/scanned/fractions; us_p50 within ±5%.
- Slopes recomputed from the author's own JSON: µs p50 (eps 1e-3) log-log slope 1.04; pairs slope 0.98; capacity interpolations N≈5×10³ (3.3 ms) and N≈2.4×10⁴ (16.7 ms) check out; scan_frac 1.3–2.1% ✓; crate `kick` mean (7,470 µs, 813 pairs) ✓; the 0.35 g Fermi (δa/a≈2×10⁻³) ✓.

## Held-out predictions

`predictions.md` carries numeric ranges and a pre-declared kill criterion, which fired (0.0025 < 0.2 at eps ≥ 1e-3). 4/5 held; the miss (skippable 0.575 vs ≥0.8 at 1e-7) is reported and diagnosed (budget p10 4.7e-8 vs 1.5·rel_dt). Caveat: file mtime is 13:56, after both runs (13:54:37/43) — outcomes were appended to the same file, so pre-registration is not provable from the container alone. The honest miss and the specific ranges argue genuine, but the taste log's standard (r3 v3) counts unverifiable pre-registration against gold.

## Adversarial cases (mine)

1. **The deadline rule is unsound as measured.** `1/|Δn|` (units check out: it is the synodic period in orbits at fixed a=1 clock) is *not* the first post-kick conjunction time, which is phase-dependent and ~U(0, T_syn). I re-ran the burn geometry computing the true first conjunction from mean longitudes (n=1e3/1e4/3e4, eps=1e-3, same seed/kicks): **tc ≤ 10 orbits for 11.28–11.31% of candidate pairs** (dossier: "no candidate pair's first post-kick conjunction inside 10 orbits … ~0%"), ≤ 1 orbit for 1.1%, ≤ 100 orbits for 73% (dossier's 48% is the period, not the deadline). Decisively: **0.79–0.87% of all candidate pairs have an exact `pair_events` hit strictly before their `1/|Δn|` deadline** — i.e. the proposed rule ("deadline-sorted setups keyed by first synodic conjunction (a float bound, one divide per pair)") misses real encounters for ~19% of encounter-bearing pairs, against this tier's own zero-miss certificate (q-candidate-degree). The author's own data already showed it: hit_le1 > 0 while syn_le1 = 0. The conclusion *survives* the fix (phase-aware deadline = one subtraction + rem_euclid + divide): 89% of setups still defer past 10 orbits, ~30 setups/orbit at N=3e4 ≈ 0.25 ms/orbit — a stream, not a burst.
2. **Skin violations are not seed luck.** Fresh seed 777001: skippable 0.9459 @ 1e-9 → 0.028 @ 1e-5 → 0.0023 @ 1e-3 and 1e-2; violations 6 @ 1e-3, 3 @ 1e-2. The unsoundness-at-burn-magnitude claim is robust and slightly understated.
3. **Tail summary overstated.** From the author's own JSON: p99/p50 = 3.10 (n=1e3, eps=1e-3) vs claimed ≤ 2.9; max/p50 = 2.51 (n=3e3, eps=1e-5) vs claimed ≤ 1.9 at N≥3e3. The "no unlucky-body spike" claim only holds at N ≥ 1e4 (ratios ≤ 1.9 there). Summary slip, right direction.

## Novelty

- **Skin-for-thermal-not-burns, with violations: new.** Gold components-4643 left "the slack skin (12.6×) stays the lever"; this run bounds its domain (thermal eps only) and shows the coded 1.5×rel_dt rule is *unsound* at burn eps. That corrects a gold's takeaway and directly constrains the queued `b-encounter-skin`.
- Wake O(degree)/O(N) at fixed belt geometry and per-pair µs: new concrete numbers (frame capacity ≈ 2.4×10⁴ single-thread); the linear scaling itself was implicit in q-candidate-degree/taleb-09b5 and docs/law.md's open setup cost.
- Deadline-ordered allocation is **already adopted design** (docs/plane.md foundation 7: "spends it in causal-deadline order"; docs/representation.md §3: the slack queue ordered by deadline). The run sizes it for the encounter tier rather than introducing it; the genuinely new scheduling fact is the urgency split (cone re-scan 1.3–2.1% eager). No H entry covers the burn/skin boundary or the wake sizing.

## Goal fit

On the board's top scaling risk (candidate work vs real encounters) and bottleneck 4 (smoothness/allocator). Respects principle 5 ("The player is the only wildcard") by measuring the wildcard's own magnitude, and 12 ("the algorithm that allocates the work … it's the most important one"). The violations finding is an exactness result first and a cost result second — the right order for this project.

## Why silver, not gold

Reproduced exactly, honest miss, real premise correction (skin ≠ lever for burns) — but the headline's new quantity ("first post-kick conjunction … ~0% inside 10 orbits") is wrong by two orders of magnitude (11.3%), and the proposed adoption rule misses ~0.8% of pairs' encounters as written. It is one named experiment from soundness, and that experiment is cheap.

**The experiment that would make it gold:** re-run the urgency split with the phase-aware first-conjunction deadline (λ-crossing, one divide) and show (a) zero exact hits before deadline, (b) the stream rate (~30 setups/orbit at 3e4) — then the two scheduling rules are adoptable as-is for `b-encounter-skin`.

## What the author missed

- Period-vs-first-conjunction conflation (above) — including that their own hit_le1>0/syn_le1=0 cells already contradicted the rule's soundness.
- The tail line (≤2.9/≤1.9) does not match their own JSON at n≤3e3.
- Deadline scheduling as adopted design (plane.md foundation 7) is cited nowhere; the run reads as more novel than it is on that half.
- One belt, one ρ, uniform a: the flagged co-orbital clump (Δn→0, T_syn→∞) not only stretches deadlines, it breaks the one-conjunction-per-T_syn sparsity the stream rate relies on; untested.
- `changed_frac`'s 1e-3 raw-time tolerance ≈ 1.6×10⁻⁴ orbits over a 1000-orbit horizon — their tolerance-dominated caveat is correct and honest.
