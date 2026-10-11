Grade: silver

**Abstract.** Claim: at 10⁹ bodies on the 8 GB M1, memory capacity binds (tube store and a per-body event queue each 3.2× over the 5 GB usable) while compute and bandwidth clear by 3–5 orders once the measured levers (kick-setup 12.5×, tide averaging 114×) compose; the board's "about 190 cores" re-derives as 175 and dissolves to 0.12. Reproduced bit-for-bit: steady hits 414/1738/40 (0.0207/0.0579/0.0020 per body per orbit), `budget.py` output byte-identical; every cited constant traced to H0210, golds 20261006-0737 and components-98bc, H0190, law.md. My blind extensions held: ρ=1e-2 → 0.2229 (ρ^1.01 predicts 0.211), n=10⁴ → 0.1962 (linear predicts 0.207), truth check 0 missed / 0 false. Cost to adopt: none in code — refocus scale work onto memory.

## Reproduction (clean tree, no patch — work/patch.diff is empty)

- `steady 1000 0.001 20`, `steady 3000 0.001 10`, `steady 1000 0.0001 20`: every counter identical to `steady.jsonl` (hits 414/1738/40, cone_pairs, checks, evals; only wall times differ, shared host). Bit-for-bit.
- `python3 budget.py` → byte-identical to `budget-out.txt` (diff exit 0). I re-derived every row by hand: 175 = 10⁹×32.5/5400×29 µs; 0.122 averaged+fixed; 764 ev/s; 1.07 s full pass; 1 B/body/frame; 16 GB vs 5 GB = 3.2×; 0.0158 GB programs; 33 MB queue at 0.1-orbit lookahead; 2.65 bits/body/orbit; 15.1-orbit fill; 1.51-orbit cadence; 828 B/s. All correct.
- Constants traced: 29 µs = H0210 Limitations ("kicks cost 29 µs"); 92 % setup = gold 20261006-0737 (board taste log); 32.5/orbit and 114× = H0190 (board "Known"); 0.126 bits = gold components-98bc; 16-byte tube = law.md; M1 60 GB/s and 10¹⁰ ops/s = board figures, disclosed as such.
- Belt-0 identity: r8 v2's rung defines the N=10³ scaling belt as σ_e=10⁻², ρ=10⁻³, a∈[1,1.5], 20 periods — exactly the steady config. 427/1000/20 = 0.0214 vs this run's 0.0207: 3 % seed noise. "Reproduced independently" is fair.
- Numbers that differ from the dossier: none in reproduction. Two nits below (year constant, scar factor).

## Predictions

`predictions.md` mtime 19:22:32 precedes `budget-out.txt` 19:24:56 and `steady.jsonl` 19:25:50; `budget.py` 19:24:54 → output 2 s later. Log order consistent. P2 held (2.80× vs 3, inside ±30 %); P3 held (α = 1.015 vs [0.7, 1.3]); P4–P6 arithmetic verified. P1 missed 15× low ([0.3, 5] vs 0.0207), reported as a failure with the P7 protocol followed (the failing term named: the conjunction pre-factor, anchored on element-sort's 1.1 *events* per body per orbit — a work metric — rather than the encounter rate). The exponents, the falsifiable part, held; the verdicts use the measured rate, never P1's value. Honest, but a held-out prediction failed by 15×, and the gold bar says the held-out predictions held.

## Adversarial cases (mine, blind to the author's tuning)

1. **ρ = 1e-2** (10× up, exponent from the other side): 0.2229 hits/body/orbit vs ρ^1.01's prediction 0.211 (8 % off). ρ² would give 2.07 — decisively rejected. The one-pinned-dimension claim holds from both sides.
2. **n = 10⁴, ρ = 1e-3, 5 orbits** (10× density): 0.1962 vs the linear prediction 0.207 (5 %). n-linearity holds across a decade, not just 3×. (54 s method time on the loaded host; my probe, not the dossier's command.)
3. **Truth check at the steady config** (`verify b`, `r8like-s1e-2-r1e-3`, other seed, 50 orbits): truth 921, method 921, matched 921, missed 0, false 0. The steady hits are the true encounter rate, not just the method's. Rate 0.0184 — third seed, Poisson-consistent with 0.0207 and 0.0214.
4. **Combined extrapolation** (`verify d`, `dense-n3000-s1e-2-r3e-4`): 0.0174 measured vs 0.0183 predicted from 0.0207×3×(0.3)^1.01 — 5 %.
5. **σ_e sensitivity** (`verify d`, `hot-s0.1-r1e-3`, σ_e 10×): 0.0698 at n=500 ≈ 7× at density-corrected n — sublinear in σ_e; and the dilute mixed belt (a∈[0.5,3], σ_e=0.2) gives 0.023. The rate stays within one order across wild geometries, which strengthens the Fermi verdict; the cadence number inherits belt-0's config as the author disclosed.
6. **Sensitivity of the verdict to the memory figure**: at the approved plan's 4 GiB the overs are 4×; at 20 GiB tubes (16 GB) fit but tubes+queue (32 GB) do not. Capacity binds in every case, as the dossier claims.

## Novelty

docs/HISTORY.md and the board record the levers separately (H0190, gold 20261006-0737, components-98bc) and name H_live as the open decider, but no entry decomposes the 10⁹ budget, measures the encounter-creation rate, or derives the scar-fill timescale. This run's new numbers: 0.0207 hits/body/orbit with its n·ρ scaling law, the 2.65 bits/body/orbit creation rate, the 15-orbit fill / 1.5-orbit recompile cadence, and "no ticks" quantified as 1 B/body/frame. Not previously tried; no H entry to cite.

## Goal fit

Moves board item 3: its premise ("We need 10–100× less" event compute at 10⁹) is shown wrong at belt scale by composition of measured levers on independent axes (kicks/orbit × cost/kick — not H0089's overlapping factors), 175 cores → 0.12 (LEO, conditional on averaging, disclosed) and 2×10⁻⁴ (belt). PRINCIPLES #24 "The memory floor is information-theoretic" becomes numbers (40 bits/body; 2.65 created per orbit); #1 "The cheapest compute is compute not done" — the event-speed hunt at belt scale is deletable; #10 measure before claiming — the rate is measured and truth-validated, not just estimated. Fit is good; the lens's limits (pre-factors, config inheritance) are stated by the author and confirmed by my probes.

## Why silver, not gold

One named experiment away, and the dossier names it itself: the reabsorption side is unmeasured. The cadence number rests on an assumed 128-bit scar and an assumed 1:1 encounter→scar mapping (see below), and whether a recompiled program holds near 0.126 bits/body as scatter accumulates (B18b's open question) decides whether the 40-bit steady state is reachable. Plus P1, a held-out prediction, failed by 15× — honestly reported and non-load-bearing, but the gold bar says the held-out predictions held.

**The experiment that would make it gold:** measure reabsorption in `crates/shipmem`'s real representation — scar size in bytes, scars created per encounter, and the recompile cost per body as scars accumulate (does the program family hold near 0.126 bits/body, or grow toward the mixed-belt entropy). That turns the 15-orbit fill and 1.5-orbit cadence from an estimate on assumed constants into a measured design constraint, and the capacity verdict into a design.

## What the author missed

- **A factor of 2 in the scar accounting.** `hits_per_body_orbit` counts pair-encounters per body per orbit; each encounter involves two bodies, and shipmem's scars are per-ship. If both participants scar, creation is ~0.041/body/orbit, the budget fills in ~7.5 orbits, and the cadence is ~0.75 orbits (~1 game-year) — unless the design attributes one shared scar per pair, which is nowhere stated. Not verdict-changing; the headline cadence is optimistic by ~2×.
- **The 1.26 yr/orbit constant at a = 1.2 is 4 % low** (1.2^1.5 = 1.31 yr): 19 vs 20 years. Immaterial.
- **"Truth-checked hits" overstates the command.** `steady` never runs the truth; exactness at this config is r8 v3's result, which I re-ran (`verify b`: 0 missed, 0 false, same config other seed). The number is right, but the evidence for it is borrowed, not in the run.
- **"Work tracks real encounters" is only half-visible in the cited data.** `steady_work_per_encounter` (1.3–2.0) counts checks only; the dominant setup cost per encounter grows superlinearly at fixed volume (109 → 239 → 473 for n = 10³ → 3×10³ → 10⁴). The certificate's promise holds for steady maintenance work and at fixed density (q-candidate-degree's silver), not as stated on this data.
- The σ_e dependence was measurable with the same binary (`verify d`) and was left to the checker; it bounds the cadence's config sensitivity at about one order, which the dossier argues but does not show.
