Grade: silver

**Abstract.** Composed from page-cited constants (no flight, `compose_family.py`, 0.1 s), the formation family's store is the fleet/driven population, never the phase-locked belt: family bytes floor at w = 8–32 B (misses the ≤6 B scoreboard row at every F; loses the belt to the compact store 1.6×), beat the compact store's driven worst 1.44× (10.93 vs 15.75 B) and cut the fleet population 113–245× off the 5,060 B plateau; 1–10% fleet share swings the 10⁹ kick row 0.69×→6.87× budget; the fork bill ≤0.23% of the stream saving closes od 3 at the belt. Reproduced byte-identically; every constant traced to its source; P1–P5 pre-registered. Silver because P4's baseline ("longest flown horizon" 1.2e5 game-s) is misidentified — e29c flew a fence to 8×10⁶ game-s, making the fleet certificate 0.03× that horizon — and T4's absolute multipliers ride the floor-belt cadence, unreconciled with the same ledger's λ = 4×10⁻⁵. Adoption is a scoping decision (gate flights at belt+fleet only; calendar-item change first): zero code, one step.

## Reproduction

- `python3 compose_family.py` re-run in the clean tree (base 802861cd = HEAD; `work/patch.diff` empty, correctly declared): exit 0, **byte-identical** to `compose_out.txt` and to the runner's `regen.log` (which re-fetched Readwise live: 4,590 highlights, identical output — the quotes are genuinely from the library).
- Code literals verified in-tree: `4_740 * Q` (scenario.rs:266), `Scalar::raw(260_000, 18)` (:192), "two thirds of the Moon's distance" (:325), `unwrap_or(48)` (tail.rs:15), `pub const Q: i64 = 1 << 20` (fleet.rs:42).
- Page-cited constants traced: compact 21–40/126 bits and ~6 GB goal (HANDOFF scoreboard, lines 62–63); cache 1,171 (HANDOFF:24, 3bb7e9d9); 58 µs rebind (board, 20 Oct); fit_key 4.4 µs (kick-jet); 35.1–35.4 µs made kicks (6faa, via library-directions:122); 21.9 ev/orbit floor + 16/orbit conjunction floor (kick-cadence:93, cbe6:20); 2,432–2,452 B standing + the 1,200-s arm (a990, live-residency:10–14); 5,060 plateau (b30b/6793); T* = 3.37e7 gs (e29c, library-directions:61); 4e6 events/wall-s (3aec via budget-1e9:11). 033c's anchors (69@15,000; 1–20@150,000; 1@250,000; 682–3,367 sweep; 0.16%/4.5%; 554–13,512 kicks = 35–845 orbits; 110.9×/decade) all confirmed by 033c's own silver check.
- Independent recomputation (my own script, different structure): T_LEO = 5,828.5 s, T_BELT = 1.248e8 s (the author's Kepler is right; my first draft was not), 8.12/10.93 B, 1.44×, 44.6×, 32.1/9.3/7.2%, 0.69/3.44/6.87, 1.56e4×, 2.07–10.2×, 0.216–0.230%, 130× — all match. One trivial nit: the plateau ratio is 113.3–245.0×, not "113–244×".
- Prediction ordering: predictions.md 17:05 → compose_family.py/compose_out.txt 17:07 → dossier 17:08. Held before the decisive run.

## Adversarial cases (mine)

1. **The λ-convention attack (T4).** The script's belt rate (21.9/1.25e8 = 1.76e-7 ev/B/gs) is the *floor* cadence; the budget-1e9 page's own ledger basis is λ = 4×10⁻⁵/B/gs (population average; belt-pure 7.2×10⁻⁵ both combs, d709) — 228× higher. Under λ the quoted absolutes become 1.68×/4.38×/7.76× (0% share = exactly 1.0×), and "belt-only 0.0044×" does not exist. **The load-bearing claim survives under both conventions** (fleet term = 6.9× the belt term at 10% share; "closes at any share with F = 10⁴" holds under both; I verified), but the dossier never names the convention it uses — for a run whose product feeds that same 10⁹ ledger, that is a real precision fault, the exact page-inheritance risk the lens itself names.
2. **The e29c horizon attack (T5, outside the author's tested baseline).** "The longest flown horizon (1.2e5 game-s)" is false: e29c's fence flew "at every flyable N to 8×10⁶ game-s" (library-directions:467). The fleet certificate (2.48e5–1.23e6 gs) is **0.03×** that horizon; the fleet fork recurs ~30–130× per T* in a persistent store. "Never a session event" stands (2.07–10.2× a 1.2e5-gs session); "store-lifetime" is belt-only. P4's "≥2×" held against a misidentified control.
3. **Boundary-combs-free attack (T3).** The saving prices both combs at the kick's 35.1 µs; if boundary combs were free the bill is 0.46% — past the pre-registered 0.3% bound, though the decision (immaterial) does not flip. The P3 bound is convention-fragile.
4. **The fleet's own fork bill (unpriced by the author).** Fork every 43–210 LEO orbits at 58 µs against a saving of 16×35.1 µs/orbit: 0.05–0.25% — od 3 closes for the fleet too; the conclusion extends beyond the author's belt scope.
5. **The 0.16% disagree transfer.** Measured at dx 1e4; the plane's 48-member ring spacing is ~620 root (16× tighter, Xi ∝ dx), so 0.16% is an upper bound — the 44.6× collapse is conservative. Holds.

## Novelty and the page

Not on the page before (the published Current best holds a877/b560/033c; no bytes comparison, no population split, no 10⁹ fleet-share row) and not in docs/HISTORY.md (the H family entries are the old engine's 2026-09-12 phase families). Method precedent exists (cf2a, 6faa — library compositions on published constants, both quoted in library-directions); the question is new. Gold-run closure does not apply (topic stays open, correctly).

The proposed page was **over budget** (Current best 29 non-blank lines vs 15) and carried the overstatements above. Corrected in place: trimmed to 8 lines, the λ dual reading added, the horizon claim fixed ("never a session event", not "store-lifetime"; 0.03× the e29c fence), 244→245×, the fleet fork bill and the 0.46% boundary-free case folded into od 3, the run line graded. Total 102 lines, 4 run lines, append-only.

## Goal fit

Board focus area 3 (families/formations) and the scoreboard's memory row. It deletes one whole adoption route (the family as the 10⁹ phase-locked belt store) and any gate flight at dead radii, and corrects the 10⁹ ledger's premise (its kick row is population-split). PRINCIPLES 33, quoted by the author, is exactly right: "An ant cares about a raindrop but the lion does not" — the belt-averaged row hides the fleet's 1.56e4× per-body rate. Composition-not-flight is honestly declared everywhere, including the falsifiers.

## Why silver, not gold

Real, reproduced, and premise-correcting, but two of the five quoted headline number-sets stand on baselines the author did not check: T4's absolutes are floor-convention numbers fed to a λ-convention ledger, and T5/P4's "longest flown horizon" is contradicted by a flown fence in the lab's own record. The decisions survive (I verified under both conventions, and priced the missing fleet bill), but a gold composition must reconcile its own ledger's conventions before the integrator reads its multipliers.

## The one experiment for gold

Re-compose T4/T5 dual-convention — belt-pure λ_k+λ_b (d709) beside the floor rate, the corrected horizon set (session 1.2e5 vs e29c's 8×10⁶), the fleet fork bill included — with the λ-convention multipliers pre-registered. One script edit, no flight; alternatively folded into the od-1 gate flight design it scopes.

## What the author missed

- The 10⁹ ledger's own λ = 4×10⁻⁵ basis (budget-1e9:11,14) — the convention clash above.
- e29c's 8×10⁶-gs flown fence as the true longest horizon.
- The fleet's own fork bill (0.05–0.25%, immaterial — the omission weakens the page's own adoption story).
- The boundary-comb cost assumption inside "stream saving" (P3's bound flips at 0.46% under the free-boundary adversarial case).
- The page budget (29 > 15 lines) — trimmed; and a dead `rate_at` lambda plus an unused `MINT_B` constant in the script (cosmetic).
