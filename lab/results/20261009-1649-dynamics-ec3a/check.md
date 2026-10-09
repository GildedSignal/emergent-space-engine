Grade: silver

# Check — run 20261009-1649-dynamics-ec3a (independent GLM checker)

**Abstract.** Claim: in a stable belt under the design's own split (exact Kepler drift + tide/J2 kicks), the per-body element-quantum re-key rate is BROAD (p99/mean ≈ 3.3, max/mean ≈ 5.7, hot-10×-median fraction 0), a p99-uniform cadence wastes ~70%, and the exploitable structure is predictability (librators) not concentration. Reproduced bit-for-bit (my C0: identical crossing arrays, S 3.299, f/l/w 0.083/0.562/0.328; 199 s). Adversaries: seed 21 (S 2.99, same classes), dsamp 0.1 (scale ×1.74, shape unchanged). Gain: first measured shape for q-cadence and H_live; no 10× delivered yet. Adopt cost ~zero (a policy input, no code). Two headline corrections below (J2 freeze overstated; cut sensitivity understated).

## Reproduction

- Clean tree (`work/patch.diff` empty; scripts live in the run folder). `python3 belt_surprise.py --out runs/C0_main --tmax 2400 --nbody 1024 --dtper 32 --dsamp 0.05 --qa 3e-3 --qe 1e-2` → **cross_a and cross_e arrays bit-identical** to the author's npz; every summary number identical (live 0.974, mean 0.907, med 0.713, p99 2.993, S 3.299, waste 0.697, burst 1.359). Wall 199 s vs author 330 s (load only).
- All 8 stored JSONs match the dossier table digit-for-digit.
- C1 (m'=0): with `mp=0 and J2=0` the kick branch never runs (`belt_surprise.py` step loop), so exact drift conserves a,e to machine precision and zero crossings is structural — stored JSON confirms 0 at every mult. Negative control valid by construction and by run.

## Held-out predictions

Timing verified: `predictions.md` 17:09:59; script final 17:08:30; decisive outputs 17:14+ (mtimes). Calibration (T=300 main config) disclosed.

- HELD: P1, P3 (H1 mean ×1.73, in [1.5,2.6]), P6, P7 (S 3.3 ∈ [3,10]; walkers 0.33 ∈ [0.25,0.75]).
- FAILED, cause verified by me: P2/P4 — Holman–Wiegert S-type edges are a_c ≈ 0.375 (e'=0.15) and ≈ 0.28 (e'=0.3), so both stress belts sat genuinely past the edge (97%/94% ejected is the physics, not the instrument). The pre-registered "else VOID" for C2 does not fire as blindness: the instrument saw the ejections and the edge; the control was simply mistuned. The "no concentration" conclusion therefore stands only for stable belts — exactly how the claim is scoped.
- PARTIAL: P5, honestly reported (1/quantum scaling with amplitudes ≫ quanta is real signal, not the leak floor; frac_zero freeze-out appears only under J2).

## Adversarial cases (mine)

1. **Seed 21** (not the author's 7/8): S 2.99, waste 0.67, f/l/w 0.09/0.56/0.33, hot10x = 0. Shape robust on a third seed.
2. **Instrument attack, dsamp 0.1** (perturbs the time-domain double average): absolute rate ×1.74 (1.58 vs 0.91) — matches the author's disclosed ×1.7 systematic — but S 3.22, waste 0.69, classes 0.05/0.60/0.32, burst 1.34. The load-bearing shape survives a scale-shifting instrument change.
3. **Freeze-out audit of H3 (J2)**: the "frozen 81%" is the a-key only. 100% of those bodies still re-key (median 0.177/orbit, e-key driven; 94% of them above 0.1/orbit) and they carry **53% of H3's total crossings**. J2 collapses the a-layer (median a-rate 0), not the belt's re-key work.
4. **Classification-cut sensitivity** (C0 npz): the walker/librarian **work** split (not just body fractions) moves from 0.15 to 0.61 across reasonable cuts (net-drift fraction 0.1–0.5, frozen ≤1–4 quanta); at the author's cut, librarians carry 0.62 of work, walkers 0.35. The dossier's "~10 pp" understates this. Librarians and walkers have nearly the same mean rate (0.97 vs 0.96): the classes differ in drift structure, not hotness — which actually sharpens "no hot minority".

## Novelty

docs/HISTORY.md and the board have no prior measurement of belt re-key/surprise rates; HANDOFF lists H_live as "not measured yet". Adjacent but distinct: q-secular-v2 (6 Oct) killed zero-kick secular phasors at belt scale — consistent, and a caveat the dossier misses (a scheduler built on secular predictions inherits secular e-amplitude errors ~15% at belt scale; the named gold experiment must judge behaviour, not just cost).

## Goal fit

Feeds q-cadence ("cadence is the lever") and H_live (the 10⁹-in-8 GB risk). PRINCIPLES: "No work for no reason, so no ticks"; "Compute only surprises" — the 70%-waste number is that principle quantized. Scope honestly planar-restricted, single secondary, T≈1700 orbits (walker fraction a lower bound).

## Why silver, not gold

Reproduced and robust, but it measures a shape; it neither delivers a 10× nor deletes a component. "No hot minority" was an open question, not an adopted premise, so killing it is not a premise reversal. Two headline corrections must fold into any adoption: (a) J2 freezes the a-key layer, not re-keys; (b) the predictable/surprise work split is cut-sensitive (0.15–0.61), so the policy must state its cut.

**The one experiment for gold** (the author names it, I agree): a predictability-tiered cadence policy — event keys for librators, surprise-following for walkers, a stated classification cut — judged by the plane's cost judge at equal behaviour against a uniform-p99 tick, on the plane (not the float instrument), plus the corrected just-inside-the-edge control (belt straddling a_c at its actual e').

## What the author missed

- The J2 headline ("freezes 81% outright") contradicts their own H3 key-rate median 0.21; the belt keeps re-keying through the e-key.
- The stated ~10 pp cut sensitivity is understated for work share (±25 pp).
- Librators and walkers have equal mean rates — the "walkers are the surprises" framing hides that surprise-ness is drift structure, not rate; a hot-minority allocator heuristic would find nothing to grab even if it wanted to.
- V0 (dt halved) also changed the survivor population (live 0.97 → 0.84), so its ×1.7 scale shift is part sampling systematic, part population — does not affect the shape claims.
- traces.png includes the pre-settle zero rows, so all traces share a cosmetic init jump (~|k_a| ≈ 970 quanta) before the drift story shows.

Checker's runs: /tmp/check-ec3a (C0 reproduction, A1_seed21, A3_dsamp10), ~200–260 s each, single core, < 300 MB.
