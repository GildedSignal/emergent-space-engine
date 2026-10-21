Grade: silver

**Abstract.** Claim: the child-doll family certificate kills the tube-family inside planets' dolls. Reproduced byte-identical (`regen.sh`, 113 s, deterministic f64). Real and independently confirmed: the r²·H death law (checker at the untested r = 15,000: Xi 2.16e-4 vs 2.08e-4 predicted; first fork 69 kicks), the tube-family dead above ~1.5e4 root radius (3–5 kicks at GEO scale), no family/lattice crossover at any child-doll dx, belt sharing 554–13,512 kicks (35–845 orbits) at dx 1e4–1e5. Corrected on the page: the quoted belt range (2.5e3–1.3e4) is the best arm alone; "residue 20–30× below at every arm" is false (exceeded at star-doll dx ≥ 5e5); at the fleet lattice radius the 682–716 fork is a phase-lottery and the steady rate (0.16% disagreement) beats the 1 AU control (4.5%) — the LEO kill is unproven. Measurement only; no adoption cost.

## Reproduction

- `regen.sh` re-run in a clean shell: `census.csv` **byte-identical**, 112.9 s wall (claimed 112 s), single-threaded f64, no engine build; `work/patch.diff` is empty (standalone instrument — "no engine change" is true).
- File times: `predictions.md` 16:01 → `family_hill.rs` 16:04 → `dossier.md` 16:09. Predictions were written first.
- Arithmetic anchors re-derived: Moon tide GM_M/d_M³ = 3.39e-24 vs measured 4.39e-24 (tensor factor 1.29, as stated); Home 2e6-root pass 4.77e-25 ≈ claimed 4.8e-25; Giant at 1 AU 1.27e-26 ≈ claimed 1.3e-26; `dbg.rs` direct pull difference 1.16e-23 vs 1.65e-23 arithmetic (order-anchor; note `dbg.rs`'s own `diff=` line prints a position difference, not a pull difference — a wart, not load-bearing). The 110×/decade is 110.9× at dx 1e3 (census).
- Constants match `scenario.rs` as claimed (Home 2⁻¹⁸ a=1.0133e8 e 1/50; Giant 2⁻¹⁰; Moon 2⁻²⁴ periapsis 260,000; AU 1.013e8); word scheme matches `step.rs::quantize`'s sigma-delta at 2⁻¹⁶·q with q = 2⁻¹¹·v.

## Adversarial cases (mine)

1. **r = 15,000 — outside the author's radius set.** Xi(dx1e3) = 2.162e-4 vs 2.08e-4 predicted by the r² law (within 4%): the law is real at an untested radius. First fork 69 (dx 1e4), 504 (dx 1e3): the family is already dead at 1.5e4 root — this *sharpens* the kill boundary but falsifies the page's "≤5 kicks above ~10⁴" (69 at 1.5e4). Page corrected to ~1.5×10⁴.
2. **r = 250,000 — inside the Moon's shell.** Fork at kick 1, disagreement 61–98%, H_eff ~1e-22 (Moon-crossing conjunctions): everything word-based dies there. Confirms the dossier's P4 remark that nothing wins near the Moon.
3. **Moon-phase sweep at the headline arm** (4740, dx 1e4): first fork 682 (m0 0.7) → 1,477 (m0 2.9) → 3,367 (m0 4.7); th0 2.0 → 682. The 682–716 is phase-sensitive by ~5×.
4. **Mechanism probe** at the same arm: at the fork (k=716) the reference's accumulated input is S_r = 2.0000334 quanta and the member's S_m = 1.9995645 (gap −4.7e-4). The fork is the **common-mode wrap straddle** — the pair's shared accumulated kick crossing a quantum boundary — not the differential's magnitude. dx below the author's ladder confirms it: dx 100/316 → first fork 21,484 (not ~700); dx 3162 → 716. The first-fork integer is a lottery over the wrap schedule, exactly as the dossier's own caveat ("order markers") implies — but the claim sentence and the page led with "forks within ~700 kicks" as the kill.
5. **Steady-state inversion, from the author's own census.** disagree_frac at 4740/dx1e4 = 0.16% (99.84% shared; ~625 kicks between re-syncs) vs star1AU/dx1e4 = 4.5% (~22 kicks). By steady rate the fleet-lattice family is ~28× *steadier* than the 1 AU control — consistent with Xi (1.7e-4 vs 5.5e-3, 32× cheaper) and with the author's own pre-registered kill criterion ("if P3's Xi at dx 1e4 measures < 1e-3, child-doll families are as cheap as star-doll ones"), which **fired** (1.7e-4) and is nowhere addressed in the dossier. The corrected-P3 conclusion "child-doll certificates ~10–100× shorter than star-doll at equal dx" holds only for first-fork integers; the run's own rates say the opposite at 4,740.

## Overstatements found and corrected in the page

- **"the lattice's linear-tide residue runs 20–30× below the family differential at every arm, radius and dx"** — false. Census range is 1.4×–3,000×; the residue *exceeds* the differential at star1AU dx 5e5 (2.90e-1 vs 1.90e-1) and 1e6 (6.14e-1 vs 2.58e-1), and at home150000 dx 5e5 (14.2 vs 8.1). It is below at every *child-doll* dx (1.4–210×), so the no-crossover conclusion inside the dolls stands — on the corrected domain only.
- **Belt horizon "2.5e3–1.3e4 kicks / 160–850 orbits at dx 1e4–1e5"** — that is the 4:1 arm alone. Cross-arm: 554 (3:1, dx1e5) and 1,040 (plain, dx1e5) to 13,512; i.e. **35–845 belt orbits**. Also the dossier's "2,569–3,699 (dx 1e5)" mislabels 3,699 (it is the dx 5e4 row).
- **P2 as pre-registered failed**: "belt families share to dx ~5e4–1e5 for a 2^17-kick horizon" — every belt arm forks at 477–3,699 ≪ 131,072. The dossier's "half-held" silently redefines the horizon from 2¹⁷ to 2.6e3.
- **P3 as written missed by three decades** (0.1–0.3 predicted vs 1.7e-4 measured); the post-hoc arithmetic fix (2.1e-4 vs measured 1.7e-4) is correct arithmetic but is a disclosed miss, not a held prediction.

## What stands (and is worth the integrator)

- The Xi = h·H·dx/q law and its r²·H radius scaling, confirmed at an untested radius; three independent anchors check out.
- The tube-family is dead as a child-doll representation above ~1.5e4 root radius (69–1 kicks, steady disagreement 1–98%); a configuration deletion per PRINCIPLES 9 ("A failed experiment kills that configuration, never the method") on the board's "families and formations" row.
- No family/lattice crossover at any child-doll dx where the family word still holds.
- The belt sharing horizon, corrected: 554–13,512 kicks (35–845 orbits) at dx 1e4–1e5, h = P/16 — feeds the row's memory arithmetic directly.
- Novelty: `lab/wiki/formation-family.md`'s od 4 ("the crossover is unmeasured") is this run's question; a877 measured the root-doll word only, b560 the key half. No HISTORY entry measures child-doll certificates. Not a repetition.

## Goal fit

Board row "Macro, families and formations: how long a member's certificate lasts against its separation, in the plane's own fleets and belts" — the row's exact question, measured. PRINCIPLES 33 ("each scale resolves only what matters at that scale") is the right frame: the cadence law h/q ∝ r² is what kills the shared word at GEO radii.

## Why silver, not gold

Reproduced and real, but the held-out predictions did not cleanly hold (P1 miss at dx 1e6, disclosed; P2's horizon silently redefined; P3 off by 10³ with a post-hoc fix), two universal quantifiers in the claim are falsified by the run's own census, and the headline kill at the plane's own fleet lattice radius rests on a phase-lottery integer while the run's own steady-state rate and its own pre-registered kill criterion point the other way there. Page corrected in place; the corrected result is adoptable as measurement.

**The one experiment that would make it gold:** re-quote the certificates as steady re-sync rates (the instrument already records disagree_frac) over a phase ensemble (≥8 Moon/th0 phases) at 4,740 and the belt arms, family vs lattice. Either the rate at 4,740 beats the control (current numbers say yes: 0.16% vs 4.5%) and the claim becomes the sharper "the tube-family is a LEO/belt object, dead above ~1.5e4 radius" — or the child-doll kill is complete. One instrument run, no engine change.

## What the author missed

- disagree_frac was in the census all along and contradicts the LEO-kill reading of the first-fork integers.
- The pre-registered kill criterion fired and is unaddressed.
- Belt ranges quoted from the best arm; "at every arm" never checked against the census's own star-doll rows.
- One debug print (accumulated sums at the fork) would have exposed the wrap-straddle mechanism and reframed the 682–716.
- e ≠ 0 family orbits (belt e ~ 0.07) untested — H varies along the orbit; flagged by the author but not bounded.
