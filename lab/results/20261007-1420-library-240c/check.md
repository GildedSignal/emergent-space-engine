Grade: silver

**Abstract.** Claim: B12's verdict must judge the worst seed's error *type* via the Allan-deviation slope, not the median seed's growth exponent. Reproduced bit-identically: at N=2048 one threshold (0.10) classifies 96/96 planted seeds; on my fresh seeds too (0/96 miscalls, gap −0.065…+0.225). Fleet-16 measured: the median-exponent rule certifies a fleet whose 16th ship leaks; the worst-seed Allan slope (0.496) flags it. The plain variogram is correctly killed (bounded-white 0.847, 16/16 false). Gain: unblocks q-b12-design (first in queue). Cost: one slope fit per seed plus scene requirements — my attack shows zero false leaks at any N, but 2–3/16 per-seed misses below N=256, and bounded oscillations slower than ~3 periods per scene false-leak 16/16.

## Reasons

1. **Reproduction: bit-identical.** `python3 probe_b12_stat.py | diff - probe-out.txt` → empty. Every dossier number matches the stored output: Allan medians (bounded-white −0.067, bounded-chaotic −0.523, leak-rw 0.431, leak-slow 0.401, drift 1.000), bounded max −0.066 vs leak min 0.193, fleet-16 (median expo 0.000 passes; worst-seed vario 0.967 / allan 0.496, seed 15), exponent scatter 0.146–0.759. Patch is empty — probe-only run, nothing outside the folder, as the rules require.
2. **Predictions.** `predictions.md` (mtime 14:27:54) precedes the run (probe 14:30:18, out 14:30:20). P2 held (median passes a leaking fleet, tail catches it), P5 held (sub-floor leak reads bounded, correctly), P1 *failed* for the variogram and the author reports that failure as the finding — the τ-averaging inside Allan is load-bearing; P4's variogram negative control fails by 1/16 (dossier pivots to Allan, whose controls pass). P3 failed: the logistic synthetic does not reproduce the plane's known inversion (0/256), so the Allan slope is validated on planted cases only — the author says so in the dossier. Honest scorekeeping throughout.
3. **Adversarials (mine, fresh seeds 10000+/20000+/…, threshold 0.10).**
   - *Fresh seeds:* 0/96 miscalls; gap −0.065…+0.225. The threshold is not overfit to the 96 planted seeds.
   - *Short series* (B12's real regime — law.md: "≥ 20 crossings per ship"; the probe only tests N=2048). With the leak's end magnitude fixed at 10× the floor (the author's clean regime) and N varied: **0 false leaks at every N ∈ {20,…,2048}**; per-seed misses 3/16 (N=20), 2/16 (N=40–128), 0/16 (N≥256). Degrades gracefully, but the dossier's "N is larger in the gate's favour" is asserted, not measured, and is wrong at today's scene spec.
   - *Slow bounded oscillation* (the author's stated risk, unmeasured by them): a bounded sine with ≤2 periods per scene reads slope ≈ +0.73 → **16/16 false leaks**; 4 periods/scene is safe (max −0.042). The scene must guarantee the horizon spans several bounded periods.
   - *Marginal leaks:* the dead band is amplitude-ratio-dependent — leak end-magnitude ≈1–2× the floor reads bounded (step 1e-8 on a 1e-6 floor: 16/16 bounded); consistent with the author's "minimum detectable leak ≈ floor" but the dossier presents 0.10 as if ratio-free.
   - *AR(1) ρ≥0.99* (stationary, long-correlated): reads as leak (11–16/16). On-horizon indistinguishable from a walk; defensible for a gate, but it means the statistic classifies correlation structure, not compounding per se — must be stated when freezing bands.
4. **Novelty.** No Allan/variogram mention anywhere in docs/HISTORY.md or docs/*. The prior attempt on this bottleneck (redteam-b12-stat, 6 October, silver) was a recurrence ratio that failed to separate slow leaks from bounded error; this is the live replacement candidate. That the exponent is broken is known (H0215, board 6 Oct, HANDOFF line 22) — this run's new content is the replacement statistic with pre-registered controls, the worst-seed verdict, and the minimum-detectable-leak disclosure.
5. **Goal fit.** First entry of lab/queue.txt (`q-b12-design`); HANDOFF line 71 names exactly this inability. PRINCIPLES: "Errors never compound… types of errors and not just errors" (13, OC#42) — the Allan band is an error *type*; "a test that cannot fail is a control" — P4's two-sided planted controls embody it. The five lessons are applied, not decorative (lesson 3's unfalsifiability point matches the recorded echo failure).

## Why silver, not gold

The statistic is validated where the probe lives (N=2048, planted shapes) and unvalidated where the gate lives: the author's own P3 admits no real plane series was tested, and my short-N run shows per-seed misses below N=256 plus a hard false-leak when bounded structure spans fewer than ~3 periods per scene. Adoption is therefore not "one slope fit in the B12 adapter" (dossier's cost): B12 v2 must freeze N, the horizon-to-period ratio, and the threshold *together*. That is precisely the q-b12-design step — real, one named experiment away.

## The one experiment that would make it gold

Freeze the triple (N, threshold, min-detectable-leak) and run the classification matrix at the gate's real conditions: the plane's actual Jacobi population (chaotic ships — the case P3's synthetic missed) at the chosen N, planted controls on both sides, plus the slow-oscillation and AR(1) cases above. If a frozen configuration separates real and planted series with 0 false leaks and 0 misses on the worst seed, it is gold and drops into B12 v2.

## What the author missed

- Series length was never varied; the gate's spec is ≥20 crossings and the clean-separation claim only holds at N≥256 (misses 2–3/16 below).
- The dead band is a function of leak/floor ratio, not a fixed slope interval; the transition zone (leak ≈1–2× floor at horizon) should be in the stated minimum-detectable-leak.
- The bounded-period requirement (horizon ≥ ~4 periods of any bounded structure) is a scene requirement the gate must freeze; ≤2 periods false-leaks 16/16 — the author named the risk but did not measure it.
- Minor: the "within 0.08" N=4096 stability claim is exactly 0.079 — accurate, but at the edge of its own rounding.
