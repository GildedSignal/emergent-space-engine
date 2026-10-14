# Dossier — 20261014-0000-fermi-3071

## Claim

The nladder conflict is resolved by decomposition: ea91's heavy-tailed surprise census
(Gini 0.72–0.74) and 7497's flat per-orbit bulk are the same stream, and the tail is
**manufactured** — the native half is the compiled period ladder (a 1,600:1 rate spread,
identical counts for same-rate bodies, identical across seeds 3/7/11, exactly 2× with a
doubled window), the member half is birth-burst-then-death, and the head is the driver —
so **rule 2 dies as a ladder rule** (the promotion certificate is arithmetic on stored
birth constants), while every one of ea91's measurements stands as a correct description.

## Bottleneck

Board focus 1 (28 bodies against 10⁹): the flagged nladder conflict decided what the
compact→live promotion certificate must read — a *measured* rank over a live census
(ea91's reading, which at 10⁹ means per-body census instrumentation on every body) or a
*constant* (7497's reading). Gain: the census instrumentation is deleted from the ladder
design before it is built; the live fraction is set at generation (on the plane, 12 of 28
natives sit above 3×10⁻³ items/s by construction); the promotion question stays where
frame-cost put it (`resolve_handout` cost and stickiness). This is a decision unlocked,
not a speedup — no 10× compute claim.

## Evidence

All numbers from `bash lab/results/20261014-0000-fermi-3071/regen.sh` (~2 min warm).
The instrument is ea91's published probe applied verbatim (`work/patch.diff`,
digest-neutral per that run); no new probe code.

**Reproduction first:** rerunning ea91's ho1 scene gives digest `aca905ad7792…`,
bit-identical to their stored census on this box (Linux/x86).

**1. The native "distribution" is a compiled step function.** The plane's 28 GR bodies
carry compiled rates 0.0484 (player) down to 3×10⁻⁵/s (haulers) — 1,613:1 by
construction (7497's roster constants). Measured over any window: same-rate bodies have
*identical* counts (Orbiters 1–2: 133,133; Orbiters 3–5: 67,67,67; Skimmers 2–3:
17,17 — at T=5,500 game-s), counts are *identical across seeds 3, 7, 11 and members
48, 120, 400* (native items equal to the item), and *exactly double* with a doubled
window (T=11,000: 266,266 / 133,133,133 / 33,33 = 2× −1). Gini of the roster-predicted
counts {r_i·T}: **0.759**, against ea91's measured native Gini **0.718–0.745**
(ρ = 0.94–0.96). Gini of {r_i·T} is T-invariant — and so is the measured one.

**2. The whole census is reproduced by the model "natives = birth constants × T,
members = measured".** Model G_all = 0.727–0.748 vs measured 0.715–0.737 (within
±0.013, zero free parameters: the items/kicks scalar 2.04–2.07 is reported, and Gini is
scale-invariant to it). Even ea91's Zipf slope is manufactured (model −1.58…−2.18 vs
measured −1.58…−1.99). Counter choice is immaterial: G_all(kicks) = 0.736–0.771
≈ G_all(items).

**3. Held-out scorecard** (`predictions.md`, written before the runs):
- **A (seed 11, m120, 55 s — used by neither author): 5/5 held.** G_all 0.721,
  G(nat) 0.736, ρ 0.958, dead fraction 0.47, alive h2 median 2 — and the native counts
  are *identical* to seed-3/seed-7 runs.
- **B (seed 3, m400, window 2× via rtf 200; disclosed schedule change): the
  discriminator held exactly where it cuts.** Ladder bodies 2× to the item
  (533 = 2·267−1); zipf −1.59. Two misses, both outside the ladder: the player's items
  are schedule-bound (350 ≠ 2×417 → G(nat) 0.713 vs band [0.716, 0.756], miss 0.003),
  and G_all *rose* (0.753 vs predicted <0.737) while the per-second rate amortized as
  predicted (3.7 → 2.4 items/s): dead members' one-time bursts freeze while ladder
  bodies grow ∝T, concentrating the cross-section. Both misses live in the driver/member
  channels both prior runs already exclude from any rank — neither revives rule 2.

**Verdict on the conflict:** ea91 measured truly (Gini 0.72–0.74 is real) but read a
compiled ladder plus a transient as a surprise distribution; 7497's verdict (rule 2
dead, certificate = birth constant) is correct, and ea91's unique findings — the death
exit channel (47–64 % of promotions), the steady-stream avalanches (Fano 8–28), the
regime-frozen ranks (now *explained*: the regime is the compiled period) — survive
untouched. The belt remains the one honest revival path (conjunction clustering), as
both runs already flagged.

## Predictions

[predictions.md](predictions.md): A held 5/5; B held the structural discriminator
(ladder T-invariance, exact 2×) and zipf, missed the two member/player-side point
predictions (G(nat) 0.713 vs ≥0.716; G_all rose) — reported above with mechanisms.

## What would make it wrong

The adjudication stands on the plane's 28 natives, whose rates the law fixes at compile
time by design (`step_for` = period/2⁷) — a shipped scene where per-body surprise is
*intrinsic* (a dense belt where conjunctions cluster on bodies, no driver) would
revive a measured tail; neither run nor this one touched belt scenes. The player is
schedule-bound (B), so any promotion rule aimed at the player must read the decision
channel, not the census. Linux/x86 shared runner; digests deterministic, timings not
claimed. Adoption cost: negative — it deletes the ladder's census rungs before they are
built. Fit with PRINCIPLES: "The cheapest compute is compute not done" (a rank nobody
needs to measure); "we just need to have the right representation so that math is
trivial" (counts are rate × time, and the rate is already stored — the law schedules
by it); "one law at every scale" (#19: the cadence law is the promotion law; rule 2
would have been a second convention beside it).

## The lens

A Fermi lens estimated first and almost did not run: the decomposition was visible on
paper (three decades of period ÷ flat per-orbit ⇒ Gini ≈ 0.7 for any mixed window), and
the runs' own data confirmed it before the engine ran. What the lens may have missed:
nothing about the belt (unmeasured, the honest revival path); the member-side burst
distribution was taken as measured rather than modelled, which is why prediction B's
G_all sign was wrong — the member half of the manufacture is not yet a formula.

## Files

`analyze.py` (all tables), `census-hoA.json` / `census-ho1rep.json` / `census-hoB.json`
(raw, deterministic), `predictions.md`, `ea91/` and `p7497/` (the two prior runs' saved
data, refreshed from their branches), `regen.sh`, `wiki/nladder.md` (the conflict
resolved).
