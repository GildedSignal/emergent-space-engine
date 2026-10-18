Grade: gold

**Abstract.** Second-author closure of 16ec's burn question, reproduced. The shipped harness's burn divergence was its own logged decision tick: `digest()` hashes `self.inputs` (universe.rs:1352); `input(p.u.now)` logs the load-presented tick. With the decision pinned via `schedule` at 365,400,000, burn ctl = ctl-rerun = fast = fast-rerun = `1198b23ec9b91432` (100% belt skip, 338 passages) across a 49% schedule spread; the never-flown `slow_cycle` refusal branch is flight-proven (5,126 refusals, 1,753 deaths, digest identical); the decomposition regenerates (clock_share 0.166–0.187). My four adversarial cases all held — a 59-decision stream, seed 2, all-refuse straddle, and N=10⁵ (ctl = fast, 100% skip), one decade past the author's domain. Gain: belt clock path 10–20× (≈0.15 → ≈0.007 cores at 10⁹); adoption is 16ec's flag plus print-only census. Gold.

## Reproduction

- `regen.sh` exit 0 (runner) and re-verified from its log and the `a_*`/`r_*` files: every deterministic number in the dossier matches — pinned `1198b23e…` ×4 (19,761 total / 19,423 fast / 338 passage), straddle `0c3b1c7d…` (12,549 fast / 5,126 slow_cycle / 1,753 deaths, both arms), coast control `a725217f…` = 16ec's known answer, probe byte-identical to 16ec's (1,204 bindings, worst excursion +0.000e0), decomp clock_share 0.1657–0.1874 over 20 flights.
- **No physics delta vs 16ec:** I applied `base-16ec.diff` and `patch.diff` to identical pristine copies; the resulting `step.rs` files are byte-identical. The delta is exactly the claimed harness additions (`ES_INJECT_TICK` scheduled pin, `ES_LEAVE_LOG2`, the decomp line, Linux footprint).
- **Mechanism verified in shipped code, not just observed:** `digest()` hashes `self.inputs` (universe.rs:1352–1355); `schedule` logs the decision at exactly its canonical tick via `pending`/`take_due` (1100–1131); the shipped harness's `input(p.u.now)` logs the presented tick. Two burn runs with different presented ticks cannot share a digest — by construction.

## Predictions

`predictions.md` (30 m) precedes the `a_*` flights (27–28 m). H2–H6 held as written. H1 was honestly split: the author window observed only the agreement half and reported it as such; the regen windows completed the divergence half. Kill criteria were pre-registered and inherited from 16ec.

## Attack (four adversarial cases, one beyond the author's range)

| case | digest ctl | digest fast | result |
|---|---|---|---|
| 59-decision stream (`schedule` every 1800 game-s, the author's named "real player session" gap) | `bded8cda3fb3d550` | `bded8cda3fb3d550` | identical; 100% skip, 338 passages, 0 refusals |
| N = 10⁵ pinned burn, full cut (next decade; author flew 10⁴) | `4ec3a8a91ca8d0f8` | `4ec3a8a91ca8d0f8` | identical; 199,423/199,423 belt skips (100%), 338 passages, ~199 ns vs ~4,152 ns/event |
| seed 2 pinned burn | `60aedfad64f94648` | `60aedfad64f94648` | identical; 19,424 fast, 338 passages |
| all-refuse straddle (leave_log2 = 27: 99.95% refusal, 9,707 deaths) | `ad5ee4ba3e3a63a1` | `ad5ee4ba3e3a63a1` | identical; 9,713 slow_cycle, deaths equal |

My first stream pair "diverged" — my own instrument bug, and a live re-demonstration of the mechanism: I flew the ctl at 30 s wall vs the fast at 60 s, so the two arms scheduled (and logged) different decision *sets* (29 vs 32 taken), and the digests differed by construction. A stream harness must pin the decision set, not just each tick. Reflown with matched walls: identical. Lesson for any future hand-flown-session harness; the author's one-decision arm is immune by construction.

## Novelty

The lab wiki's current best (pre-run) names this exact step as next: "a pinned-input harness first, then the bisect if a real difference survives." No real difference survived, so the bisect is moot. The pinned arm, the both-sides mechanism measurement, the flight-proven refusal branch, and the regenerable decomposition are all new; nothing in docs/HISTORY.md anticipates them. This run also completes 16ec's two-checker requirement (first checker gold; this second-author run reproduces and extends).

## The page

`wiki/kick-cadence.md` delta checked line by line against the evidence: header, the rewritten burn paragraph, one appended Runs line; all numbers match (71% = 12,549/17,675; 100.0% = 19,423/19,423; WH ≥ 4.3× = 1/0.1874 − 1). Faithful; no correction needed. One provenance nuance, not an overstatement: the "unequal ticks → unequal digests" citation (shipB 342,397,356 → `c3038c23…`) is from the fix-window regen whose `r_*` files the runner's rerun overwrote (this window's shipA/shipB both hit 343,400,821 → equal digests). The unequal half remains demonstrated by the current files themselves (a_shipA 247,463,935 → `37efae11…` vs r_shipA 343,400,821 → `08b6399c…`) and by 16ec's record; the dossier discloses the overwrite.

## Goal fit

Lifts the last adoption blocker on the belt boundary fast path — the board's belt stream, boundary half: "encounter work … what never needs a pair test at all" and the kick-cadence ledger (0.15 → 0.007 cores at 10⁹). PRINCIPLES: "Compute only surprises … Nothing is evolved that can be derived when looked at (clocks, redshift, views)" (3); "the cheapest compute is compute not done" (1); and the instrument lesson is Julien's "real vs displayed is not the same thing" (28) — the presented tick is display, the logged tick is law. Adoption is one step: flag-gated branch, print-only census, zero physics delta vs 16ec.

## What the author missed

1. The stream case was named but not flown — I flew it; it holds, with the set-pinning subtlety above.
2. N = 10⁵ was one decade beyond the record; now flown, holds at 100% skip.
3. The straddle arm flies a modified `leave_log2`, not the shipped scene (disclosed); the shipped scene's own refusal rate is whatever the belt's real apoapsis slack gives — 0 in these flights — so the branch's shipped trigger remains rare by construction.
4. The WH-split boundary path (~82% of boundary mass at 10⁴; 31% at 10⁵ in my flights — its share *falls* with N, worth one census) remains unprobed on its own path; named by the author, still open, and now the page's live question.
