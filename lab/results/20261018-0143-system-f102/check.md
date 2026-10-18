# Check — 20261018-0143-system-f102

Grade: gold

**Abstract.** Claim: the scan memo's reuse walk is its soundness proof — no change-signal coarser than the candidate set certifies a duplicate — so scan-queue direction (d) ("memo the candidate list") is unsound or empty, and the lever is the re-timed pending kick upstream. Reproduced: burn N=10³ duplicates 217/453 (47.9%), both_hit=0, cheap_only_soundness=0, coast inert; digests bit-identical across probe modes and load levels at 10³. Adversarial: held-out seeds 7/23 → 48.3%/47.6%; N=0 (bare 28-body world) → 0/213 certified, so belt ships are not the mechanism; N=10⁵ → 47.3%; test suite 77/0. Adoption cost zero: strike the direction, redirect upstream. One prediction half-failed (price at 10⁴), disclosed and diagnosed; the 0.24%-of-wall cell corrected to ~0.5%.

## Reasons

**Reproduction.** `regen.sh` exit 0 (runner, loadavg 5.10) and my own runs on the hand-applied patch (loadavg 4.7–11.1). Every load-bearing cell regenerates: burn 10³ verify `captures=453 both_hit=0 cheap_only_soundness=0 rebuild_only_lost=217 fresh=236`; coast all-fresh (18–19); 10⁴ held-out holds the fraction (217/453) and the per-dup price falls 2.56× (74.6→29.1 µs; author's 44.1→17.5, 2.52×). The 10³ digests are bit-identical to the author's across loads (`a961253c…`, `2389ab28…`); the 10⁴ whole-flight digest is load-dependent exactly as disclosed (my off/on at load ~7–11: `81e5739a…`, the author's value; the runner's regen at load 5.1: `86690d0c…`, the author's rerun value), and mode equality — the probe-innocence claim — held at both 10³ and 10⁴ (off=on=verify). Suite on the patched tree: 77 passed, 0 failed (the dossier's "40" undercounts; 0 failed is the claim that matters).

**Adversarial cases (mine).**
1. *Held-out seeds* 7 and 23 at 10³ burn (a seed-parameterized copy of the probe): duplicates 222/460 (48.3%) and 219/460 (47.6%), both_hit=0, soundness=0 — the class fraction is seed-stable.
2. *N=0* (bare 28-body world, no belt ships): 213/445 (47.9%) duplicates, per-doll versions still certify 0. This kills the dossier's stated mechanism ("belt ships in the root doll"): the core world's own binding changes suffice. The claim is stronger than stated — page corrected in place.
3. *N=10⁵* (one decade past the author's range): 112/237 (47.3%) duplicates, both_hit=0, soundness=0, 18.2 µs/dup — in this plane scene the apsidal filter holds at 10⁵, so the walk is cheap; the 30–34 ms belt-band number is a different scene (player inside the belt band) and the page keeps them distinct. The class and the kill both persist a decade out.
4. Probe innocence at the heldout N: 10⁴ off=on digests equal.

**Instrument.** `sloppy` is the planted-fault test path (default false): the shipped comparison is the full candidate-list equality, so `rebuild_hit` is a genuine reuse proof and the classification is against the real memo verdict. The cheap key is a plain conjunction; `binding_at`/`candidates` take `&self`, so a capture cannot bump the versions it later reads — the 0s are facts, not artifacts. Caveat recorded below: `both_hit` never fired in any arm, mine included; no positive control exists in any flown scene.

**Predictions.** `predictions.md` predates the final runs (file times: predictions 10 min before close, regen.sh and wiki 9 min, dossier last). Predictions 1–3 held exactly (burn class ~48%, coast inert, digest identity). Prediction 4 half-failed — the per-dup price at 10⁴ fell 2.5× instead of growing 8–12× — and the author reported the miss and diagnosed it with cdf0's own threshold finding (fallback at 10³, apsidal filter at 10⁴), which my 10⁵ arm corroborates. Disclosed failure with a correct diagnosis; the claim does not rest on the missed half.

**Novelty.** Direction (d) was proposed by 7343 and stands in the page's Open directions; cdf0 and 1250 priced the walk; no prior run measured whether a cheap validator for the memo exists. This run refutes it at every natural grain. The duplicate-class census (47.8% of burn captures are the 5 October re-timing class) is new, and the upstream-lever citation checks out (nladder: "its owner is the player's own kick re-timing"). HISTORY holds no earlier kill of this direction.

**Why gold.** It shows a premise is wrong (a proposed outcome-free cheap fix does not exist at any natural grain: global and guard-only arms certify subsets of the measured per-doll arm, which certifies 0 of 217–220 while staying sound everywhere), it is adoptable within one step at zero cost (strike (d), spend upstream), and the record regenerates. The coarse-grain closure is argued, not exhausted — but where the walk is expensive (fallback regime) any sound certificate must span the whole doll, which is the measured doll grain, and where the filter holds the walk is already 17–29 µs with nothing left worth saving. Same shape as gold components-4643: a wrong turn killed, nothing to build.

**Goal fit.** Via negativa and §19: "a fix signals the wrong representation … the right representation always just feels right" — two pages repairing one walk was the signal, and the error is relocated upstream (the re-timed pending kick re-scanning a tick), not patched in the memo. §3's "compute only surprises" is honored with the caveat the author states: the surprise here is manufactured.

**Page corrections made in place** (`wiki/scan-queue.md`): 0.24%-of-wall → ~0.5% (the author's own 9.71 ms / 2 s = 0.49%; loaded regen 0.8%; no wall reading yields 0.24); the belt-ships parenthetical scoped as one instance, not the mechanism (N=0 evidence); "the two pages' repairs are one walk" scoped — the memory page's byte fence bounds bytes at capture and is untouched by this run (the unification is of the code under study, not of the repairs); open-direction (d) marked killed with a pointer to Refuted; checker evidence added (fixed-cost half of the per-dup price, 10⁵ arm, seeds).

## What the author missed

- The mechanism is not belt ships: the minimal 28-body world misses 0/213 — the kill holds in every scene, not just belt-loaded ones. Stronger than claimed.
- ~Half the per-duplicate price is fixed cost (21.5 µs/dup at 28 bodies), so "~43 ns/body" misprices the scaling; the µs-at-N cell is the measured one.
- The 0.24%-of-wall arithmetic does not close under any wall reading (~0.5–0.8% is right; the non-bottleneck conclusion is unchanged).
- The memory-h-live framing ("repaired twice") overstates: the byte fence neither assumes nor needs the memo; this run neither measures nor refutes it.
- `both_hit` has no firing control in any arm (mine included). The counter is a plain conjunction and its co-counters fire, so I accept the reading, but a synthetic zero-mutation recapture would close the instrument.
- The intermediate arms (global-only, guard-only) are not regenerable from the final patch; both are implied by the measured finest arm (coarser keys move at least as often), so no record hole remains in the load-bearing cell — but the dossier's "all from regen.sh" leans on that implication silently.
