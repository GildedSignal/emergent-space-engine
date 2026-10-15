Grade: gold

**Abstract.** The shipped contact law drops the impulse of every detected pair whose closest approach falls inside its detection chronon. Reproduced byte-identically from `work/patch.diff` + `regen.sh` (294/294 boundary arms, 0 misses; positive control an exact velocity swap; missile-at-0.9c ghosts). The premise sentence in `docs/representation.md` §2 is killed in a closed-form domain: v\* = reach × 2.03×10⁵ m/s, so ship-scale pairs above ~10⁻²–10⁻¹ c closing pass through — collision play at high c, the game's stated content, is absent. Checker extensions all hold: oblique b ≠ 0 (453/453, effective-reach form), mass 1:65535, reach 1000× beyond the author's range, and a reflecting-box 0.9c pair that never exchanges in 334 re-encounters. Adoption is one rule (resolve at τ\*), canon reset, r5 re-freeze criterion written. Completes f50d's named open decomposition.

**Reasons.**

1. **Reproduction.** `git apply work/patch.diff` then `regen.sh`: exit 0, twice, output byte-identical to `out/passthrough.txt` (diff empty), 0 warnings. Every headline number (294 arms/0 misses, 7/7→0/7 ladder rows, all six game cases, both controls, the threshold table) regenerated. Mechanism verified in code independently of the author: `relativity.rs:236` and `law.rs:598` (identical gate, both laws), `chronon.rs:71` (detection admits full crossings), `chronon.rs:118-121` (every detected pair logged Contact + consumed regardless of exchange).

2. **Predictions.** `predictions.md` predates the probe (file times 16m vs 12m; log order consistent; the disclosed velocity-sign fix happened before any number was read). All six held, including the pre-registered exact boundary and the rung audit.

3. **Adversarial cases (three outside the author's domain, all pass):**
   - *Oblique b ≠ 0* (author's grid is b = 0 only; probe `crates/lattice/examples/checker2_probe.rs`): 453 arms on exact Pythagorean triples — the general form (skip ⟺ τ\* ≤ 1, effective reach √(reach²−b²)) has **0 misses**; the dossier's headline phrasing "i.e. d0 ≤ |w|" fails 47/453 (it is the longitudinal projection that must be ≤ |w|, not |d|). The author's own predictions.md carries the correct general form; the claim survives, the equivalence phrasing is head-on-only.
   - *Mass asymmetry* (author always ran 1000/1000, even the "missile" case; the lattice bounds mass to [1, 2¹⁶]): boundary mass-independent at 1:1000 and 1:65535 both orientations; missile case at m=1 vs 65535 still ghosts at 0.9c and exchanges at 0.0034c.
   - *Scale* (author's max reach 709 q): reach 70,993 q (100 m) and 709,936 q (1 km, |w| = 1.35×10⁶ — beyond even the dossier's claimed |w| max), boundary holds, skip counts match (1−ρ)·7.
   - *Reflecting-box eternity*: 0.9c pair in a box, 3000 chronons: 334 contacts, 666 wall bounces, **0 exchanges** — cross-checked exactly by revision accounting (rev0+rev1 = 666 = walls). The ghost is permanent through re-encounters; severity stronger than the author's free-space 300-chronon watch.

4. **Novelty.** The only prior art is chaos-shadowing f50d (20261015-0250, same base commit): pass-through rates measured blind (87.5% gas, 55–62% pump) with "the geometric decomposition (which closing speeds cross) is open". This run is that decomposition, in closed form, plus the premise kill, the game thresholds, the Newtonian-gate generalization, the where-it-bites map (fleet lattice yes, universe sparse order no, tubes no — all code-verified) and a freeze-ready rung criterion. A completion of a named open direction, not a repetition.

5. **Rung audit verified, and stronger than claimed:** the "independent integer reference" `xtask/src/gas.rs:152` carries the identical `dot >= 0` skip gate, so even the Chronon↔gas cross-check cited in chronon.rs's header cannot see the convention. Nothing in the engine observes it.

6. **Goal fit.** Error of type, not size (principle 2); the regime the goal names — "it lets the player feel what living at high c would feel like", "navigation, knowledge and dynamics those need to be perfect" (principle 30) — is exactly the regime where the law resolves nothing. Lens-0 (the representation) on the board. The fix adds no state and no per-contact cost.

7. **Errors found (dossier prose only; no measured number affected; the wiki page carried one of them, now corrected in place):**
   - ×10³ unit slips: "1 unit = 1.409 m" (it is 1.409 mm: M = 1.477 km, Q = 2²⁰); "reach {7,71,709} quanta (10 m–1 km)" (actually 1 cm–1 m); predictions.md's "50.5 m ≈ 36 quanta" (the probe itself used the correct unit and got 35,851 q). The load-bearing constant c·chronon = 1.477 km and the threshold table are correct.
   - "|w| from 2 to 1.9×10⁶ (β_cl to 1.8)": no measured arm exceeds 9.4×10⁵ (β_cl 0.9). My arms extend to 1.35×10⁶ and the boundary holds, so the overstatement is harmless in direction. Corrected on the page.
   - "measured 7/7…0/7 down the ρ ladder at each reach" is an idealization: no single column reads exactly that (integer phase truncation at wa = 10 shifts one row, 3/7 at ρ = 0.7); the exact instrument is the 0/294 boundary check, which is what carries.
   - Negative control's ρ is 8.5×10⁻⁵, not "≈ 4×10⁻⁴". Immaterial (both ≪ 1).

**What the author missed.**
- The `gas.rs` reference shares the gate — the engine's own independence claim is void for this convention; the audit under-claimed.
- The oblique domain (their predictions stated it, their probe never measured it; the dossier's equivalence phrasing is wrong there).
- The box/eternity case: wall-bounce revisions invalidate `consumed`, so the pair is re-tested and re-skipped on every re-approach — the hole is not a one-shot.
- The mass bound [1, 2¹⁶] constrains the fix's design space (an arbitrarily light missile cannot exist on this lattice).
- The ×10³ prose unit slips (a reader scaling thresholds by "1.409 m per unit" would misplace every threshold by three orders of magnitude — worth fixing before adoption).

Gold, not silver: reproduced exactly, predictions pre-registered and held, a documented premise is wrong with the exact domain stated, and adoption is one step (one rule, canon reset, r5 re-freeze with the written criterion). The prose slips are corrected here and on the page; none touches a measured number or the claim.
