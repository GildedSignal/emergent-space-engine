Grade: gold

**Abstract.** The 4-field sorted floor of a stirred belt at the tube's own quanta is 125.5/126.1 bits/body = 15.7/15.8 GB at 10⁹ — ≈2× over the 8 GB budget — because every exact non-replay encoding carries the phase (t_p, 64 bits per radial cycle, uniform by construction; law.md: "position and velocity are derived when asked"). The "under budget, ≤3% margin" restatement covered 3 of 4 fields. I reproduced everything byte-identically (hlive.json, final_state.npz, floor9.json; floor.py 75.5/76.1); all six pre-registered predictions held; the −log₂N slope (−0.996) holds on my own fresh seeds (H₁ 90.01–90.05); the strict 16-byte reading gives 90.4 bits = 11.3 GB, still over; shipmem's Elias–Fano port sits +1.06 bits/key above the multiset bound. Adoption: B18's stirred-clause floor is the 4-field one; the requantization law stands with a real margin.

## Reproduction (clean dir, shipped scripts, no patch to apply)

- `python3 hlive.py` (77 s, seed 20261010): `hlive.json` and `final_state.npz` **byte-identical** to the shipped copies (`cmp` both).
- `python3 floor.py`: 75.5 / 76.1 bits/body; its GB line (9.44/9.51) is the −log₂N artifact the dossier flags honestly.
- `python3 floor9.py` on the shipped state: regenerates `floor9.json` **identically** (dict equality). Every dossier number checks: slope −0.996/−0.996; H₁ 90.034±0.02 / 90.593±0.03 (analytic 90.087); floor₃(10⁹) 61.58/62.14; H_phase 63.96; floor₄ 125.54/126.09 = 15.69/15.76 GB; strict reading 90.36 = 11.30 GB; EF gap +1.06 at k=2¹⁶ and 2²⁰; full-tube EF 127.2/132.6.
- Scar row: hlive.json orbit-1 fields 126.43, orbit-1024 fields 149.3, slope 2.949, 874 kicks/body, σ_e 2.87×, H_tp_mod saturating 63.9 — all as quoted (P6, record-hygiene items).
- Patched quick path (T_ORBITS=2): 0.38 s, full-run JSON unchanged (I regenerated it byte-identically with the patched script, which is the property that matters).

## Predictions

`predictions.md` predates the decisive script (folder mtimes: predictions 15:53 < floor9.py 15:58; consistent ordering). P1–P6 all held within their bands; the kill criterion (floor₄ < 64) did not trigger — and cannot, which is the point.

## Attack (my own cases)

1. **Fresh seeds, unseen N** (999 at 2¹⁶/2¹⁹, 31337 at 2¹⁸): H₁ = 90.01–90.05, floor₃(10⁹) = 61.55–61.60 — the one-H₁ extrapolation is not a shipped-seed artifact. (My first attempt used a fixed too-fine grain and collapsed the plug-in estimator; the adaptive occupancy rule is what makes it valid.)
2. **Phase independence in the heated state**: conditional H(Φ|a-bin) at the 64-bit quantum measures ≈61.7–63 bits vs marginal 63.92 — shear correlates phase with a. So floor₄_final is overstated by ~1–2 bits (≈124, 15.5 GB). P3's "±1" is marginal on the final state, but the verdict is insensitive: 1.94× over budget instead of 1.97×.
3. **Phase-budget sensitivity**: at 10⁹ the 3-field class leaves only 1.86–2.42 bits/body of phase headroom — the "under budget" reading survives only by carrying effectively no phase; under the strict reading a 32-bit phase would fit (58.4 bits, 7.29 GB), so the 64-bit phase is the decider in both readings. This strengthens, not weakens, the claim.
4. **Spec grounding**: law.md line 12 confirmed — the tube's 16 bytes are (E,L) 32 bits, ϖ 32 bits, t_p 64 bits, and "position and velocity are derived when asked". The (E,L)-share-32-bits reading is the spec's own; section D covers it (90.4 bits, over). Both readings over budget.
5. **EF port faithfulness**: Rust `Ef::new` uses l = 63 − clz(u/k) (the port's `bit_length()−1`), nhigh = (u>>l)+k+1, one u32 sample per 64 zeros — the port matches, sans padding, as disclosed.

## Novelty

docs/HISTORY.md, law.md, plane.md and HANDOFF contain no prior −log₂N sorted-floor correction and no prior statement that the phase dof decides the belt floor. HANDOFF line 70 lists H_live as "not measured yet"; the parent (git `2c9d36b`, graded silver) is the first measurement, and this run is the named experiment that silver asked for, done.

## Goal fit

Board bottleneck "fitting 10⁹ in 8 GB"; B18's "measured information floor" now has a defensible definition (4-field, phase included, exact non-replay class). Principle 24 ("the memory floor is information") is now a measured number: 15.7–15.8 GB-worth per 10⁹ at the tube's quanta. The decision the checker flagged as "unexamined" (which fields an exact encoding must carry) is examined, with both spec readings and an operational-encoder bound. Premise shown wrong: "an exact encoding at the tube's own quanta fits 8 GB at 10⁹" is dead, and so is the "no action needed" reading of the 3% margin; the requantization/replay adoption stands with a real margin. Adoptable in one step (B18 stirred-clause floor := 4-field).

## What the author missed

- The heated state's phase is not conditionally uniform given (a, e_vec): floor₄_final ≈ 124, not 126.1 (my attack 2). Never measured; only the marginal was. Immaterial to the verdict, but P3's band is really ±2 on the final state.
- `work/patch.diff` is empty (0 B) while hlive.py is patched — the edit capture failed. I could verify the patch is behavior-neutral only because the patched script regenerates the shipped artifacts byte-identically; `run.log` is 0 B too.
- The "~43 doublings" margin-persistence remark uses the birth margin (2.42 bits at 0.056/doubling); from the heated state it is ~33 doublings, and the slope is assumed constant. Side remark; the 4-field class never fits either way.
- One belt, one perturber, one kick law; the 10⁹ point is extrapolated (justified: the −log₂N term is exact, the slope verified, fresh seeds stable — but a resonantly heated belt would only raise H₁ and tighten the verdict).
- 8 GB is read as 64 bits/body (decimal); with 8 GiB (68.7 bits) both verdicts stand unchanged (4-field 1.83× over, 3-field under).

The binding number for the *proposed* requantized law (3-field floor + anchor state per body) remains unmeasured — the author says so themselves; that is the next run, not a defect of this one.
