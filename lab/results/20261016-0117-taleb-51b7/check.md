Grade: gold

**Abstract.** The ladder's named next rung — the flight into the belt — is flown on merged main, bits held (pristine `ladder_digest` digests equal). Reproduced (regen exit 0): the quiet belt and the first-kick wave mint zero scans at 10³–10⁵; a burn mints one scan per player binding change — 1.11/11.33 MB at 10⁴/10⁵ (111–113 B/body) — backlog +1/frame, fenced at 1.92 GB (148 scans); `SCAN_BACKLOG`'s count cap pins 2048×113 B×N and never engages first. My adversarial flights extend the law: 112 B/body at 3×10⁴, 115 at 2×10⁵ (fenced at 62); a 35,000-game-s quiet flight mints exactly one scan (cf45's interval, not 59,400). Gain: the encounters tier's 10⁶× target anchored on main at four N. Adoption: reading-only; the cure stays the candidate-set certificate.

## Reproduction

Applied `work/patch.diff` myself (the runner had restored the tree after regen). `regen.sh` exit 0; every headline number regenerates:

- Quiet belt 10³/10⁴/10⁵: held 0, enc 0, p50 0.030–0.032 ms, RSS 15/36/252 MB — table row exact.
- Wave arms: held 0 both; 10⁴ max 43.5 ms (over 1) at **the same frame 8,509 with the same 35 events** as the author's disclosed 45-ms frame; 10⁵ max 11.95, RSS 322 MB.
- beltburn 10⁴: 732 MB / held 633 / p50 2.21 — inside the author's 730–732/632–634/2.0–2.2. beltburn 10⁵: fenced, 1915 MB, held 148, digest `c85be13a…` identical to the author's ×2; held tail `60:1, 90:31, …, 180:121` = +1/frame.
- Marginals recompute: (732−27)/633 = 1.11 MB (111 B/body); (1915−237)/148 = 11.33 MB (113 B/body).
- Budget-free 10⁴ ×2: p50 39.2/38.8, digests identical (`73972744…` ×2). Pristine digests `4b822570…`/`6895ce06…`/`df0e87cd…` equal, 4 schedules agree — the scenario edit leaves the shipped plane bit-for-bit, so this is shipped-code measurement.
- Load-noise deltas (fenced-arm p50 29→33.5 ms, 10³ held 103→83) are exactly the wall-coupling the run itself documents; the load-independent content (B/body, mint source, fence counts) is stable.

Code checks: `SCAN_BACKLOG = 2048` (universe.rs:79) whose own comment says "about 10 KB each" — the dossier's sizing story is the source's; `Scan.candidates: Vec<(usize, Binding, Scalar)>` (encounter.rs:75) = "every candidate's binding"; `same_inputs` (encounter.rs:80) is the reuse rule; `answer_front` logs what scans found (universe.rs:1198–1209), so `enc` is the player-scan log, not a universe-wide count.

## Predictions

`predictions.md` predates the decisive arms (mtime order consistent; the author's raws were overwritten by regen, weakening the file-time check, but the tuned-on declaration matches the smoke arms and the misses are reported as misses). Held: (1) fence ✓ (148 vs ~170 predicted, p50 over budget ✓); (2) quiet 10⁵ zero ✓ exactly; (3) wave 10⁴ held 0 ✓, memory 65 ✓, the 45-ms frame disclosed unattributed and reproduces at the same frame; (4) wave 10⁵ held 0 ✓, memory 322 vs 520–540 — meter difference disclosed; (5) digest identity failed under budget, reported as failed, root-caused (input tick) and turned into a process rule — better than the prediction; (6) cap arithmetic ✓.

## Adversarial cases (mine; one beyond the author's range)

1. **N = 3×10⁴ (mid-decade, never flown):** held 419, RSS 74→1486 MB → **112.1 B/body/scan**; the per-body law holds between decades.
2. **N = 2×10⁵ (the next decade):** fenced at 62 scans, 471→1904 MB → **115.5 B/body/scan**, capture ~317 ns/body, cap 33× from engaging. The law and the never-engages bracket hold through the decade the author never reached. (10⁶ is not runnable on this box: build alone ≈ 2.4 GB > the 2 GB fence — the claim's domain is honestly 10³–2×10⁵.)
3. **Quiet belt flown to 35,000 game-s** (author's ceiling was 14,534): **held_max = 1** — the first player item fires and mints exactly one scan, answered in idle time; enc still 0. Confirms the cadence mechanism and pins the interval at ≤ 3.5×10⁴ game-s, matching cf45's measured 2.814×10⁴ and **excluding the dossier's ~59,400 arithmetic** (page corrected).
4. **Digest discipline, from regen + the author's own raws:** the binary form "wall-coupled whenever any frame bites" is wrong in both directions — the 10⁴ wave arm is bitten (43.5 ms) yet identical across 3 processes, while the no-input 10⁵ wave arm shows a third digest (`2aadee42…`) at max 11.95 (no bite), and regen's beltburn 10⁴ is a fourth distinct digest. The coupling runs through input ticks and the final horizon; the practical rule (trust budget-free and far-from-budget arms only) stands. Page corrected.

## Novelty

The seam was known: 625b (in-band burn = 11.2 GB ruin), c481 (29.4 MB/mint pins-inclusive, drain frozen, ruin band [1.7,3.0] AU), d7bc (count cap does not bound memory; byte-cap fence; hidden answer bill), cf45 (doll interval), 6138/4487 (wave ruin basin, freeze deletion, digest instability named) — the dossier cites all of them. What is new and durable: (a) the **named next rung** (`ladder.txt:71`) flown on merged main with a bits-held certificate — the ladder's own protocol, the board's #1 lane ("which term breaks first… measured on shipped code"); (b) the **separation**: quiet coast and the wave mint zero on merged main (625b's era had a 2-s coast monster; now p50 0.03 ms), so the ruin is the player's binding changes alone — a premise correction, folded into Refuted; (c) the clean **marginal law 111–115 B/body** at four N (two mine), reconciling c481's 29.4 MB as pins-shared; (d) the **never-engages arithmetic** anchored in code and data; (e) the playability reading (enc = 0 at belt radii, semantics verified in `answer_front`) feeding "navigation and knowledge must be perfect" (OC#16); (f) the digest-discipline mechanism (4487 named the instability; the input-tick mechanism and the rule are new, and my correction sharpens it). Not a repetition: nothing on the page or in HISTORY had the belt flight, the separation, or the per-body marginal.

## Page

Faithful, resolves the standing conflict additively, and I corrected three overstatements in place: the doll interval (2.8×10⁴ measured, 59,400 excluded), "exactly one scan per frame" (one per binding change; 0.6–1.5/frame at 10⁴–3×10⁴), and "(or no input) bit-identical" (no-input arms near the budget still move). Three gold runs do not yet agree on this topic's best; the page stays open.

## Goal fit

Board #1 (28 → 10⁹ bodies): names the term that first breaks the 12-ms frame budget on merged main (the player's scan: standing p50 29–34 ms at 10⁵, +11.3 MB/frame) and hands the encounters tier (`crates/encounters`, built, unwired) its 10⁶× target at four N. PRINCIPLES: #3 "Compute only surprises" — the scan recomputes a 10⁵-body neighbourhood per player kick though only the player changed; #13 "Errors never compound" — memory compounds monotonically to swap death; #5 "his direct influence is bounded" — the separation result demonstrates the player is the only mint source. Adoption cost is zero (a reading plus d7bc's existing fence); the cure direction is the page's standing Open 2.

## What the author missed

- The mint rate is not exactly +1/frame (0.6–1.5 at 10⁴–3×10⁴; the +1.0 holds at 10⁵ where over-budget frames slow game time) — mechanism unaffected, phrasing corrected.
- enc = 0 has two stacked causes: cadence (items fire per doll interval) **and** density — budget-free arms answer every scan and still log nothing at 10³–10⁴ belt densities. "Cadence-gated" is half the story; the window finds nothing to log even when served.
- The digest binary phrasing (corrected above); the author's own two-value reading of the 10⁵ wave arm was the hint.
- The player is born mid-belt; no handoff arm was flown (disclosed). The mint mechanism (binding-change re-capture) is birth-agnostic, but a handoff could carry state that shifts the cadence numbers — the natural follow-up flight.
- The 10⁵ answer cost stays extrapolated (disclosed); measuring it needs a budget-free 10⁵ burn, which the fence makes ~40 s — cheap, and worth one line in the tier's design.
