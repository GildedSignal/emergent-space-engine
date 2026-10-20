Grade: silver

**Abstract.** The rung r13-sky-shift is frozen (sha256 verified) and executed — PASS, reproduced
exactly by me (regen 44 s, byte-identical metrics both seeds, verdict PASS). The struct read is
verbatim-true on 959a's branch: `e.lum += row.luminosity` with `row.luminosity = lum·shift⁴`,
served as `luminosity: lum` — the shipped record already stores the exact per-member seen-flux
sum, so 9c08's brightness kill (18–141%) hits a readout the record never serves, and 9c08's cure
was already shipped (cost 0). The letter L59 one-sample rule is now rung-dead (one-shift fails
0.77 bright / 0.96 oct colour; controls read 2.5·10⁻⁵; candidate exact-sum 0.0 / ≤ 0.036 oct).
Gain: deletes the "add Σ(lum·k⁴)" adoption step and kills any future sum-collapse "optimization"
at a gate. Cost to adopt: one rung file into `lab/rungs/`; the record needs nothing. Not gold:
one evidence headline is contradicted by the run's own log (below), and prediction P7 was
misreported as held.

**Reasons.**

1. **Reproduction: exact.** `bash regen.sh` (44 s, ~275 MB): metrics.json identical to the
   author's, verdict.txt identical, rung sha256 `ed91f4c0…` verifies, both struct-read greps
   guard against the 959a branch patch. `verdict.py` semantics checked by hand: candidate passes
   all four criteria, negative fails bright+colour, positive passes → PASS is correct.

2. **Struct read: verified verbatim.** I read the 959a patch myself: row maker
   `luminosity: lum * shift.powi(4)`, `blackbody(temp * shift)`; `sums_add`/`sums_sub` mirror;
   serve `luminosity: lum`, `color: lc/lum`, `shift: cs.sh/lum`; `members.len() == 1` singleton
   branch; fallback walk computes the same sums. The hinge resolves as claimed: the record is
   exempt from 9c08's brightness kill, and nothing downstream rebuilds brightness from
   `Seen.shift` (checked in this tree).

3. **Predictions: existed pre-run (mtime order; frozen sha quoted inside), but 6/8 held, not
   7/8.** P5's miss is honestly disclosed. **P7 is misreported:** the dossier says "the γθ_f
   collapse holds in 2D at the p99 readout: every fine-floor case equals its stock twin to 4
   digits (0.628794 both floors at γθ_f=4 2D)" — but the run's own evidence table reads
   **0.708354 (fine) vs 0.628794 (stock)** at γθ_f=4, and 0.268844 vs 0.278442 at γθ_f=1. I
   re-ran three fresh seeds: ratio 1.127 ± 0.001 at γθ_f=4 — systematic, ~40× seed noise. The
   author read the forward-cell column (which does collapse: 0.6288 both floors) as the p99.
   What actually collapses: the continuum forward error (quadrature identical to 6 digits), the
   3D p99 (0.630141/0.630142), and 2D p99 at saturation only. Mechanism: at fine floors the 2D
   flux-weighted p99 tail picks just-off-axis cells whose relative k-span depends on γ and θ_f
   separately. **The verdict and all gated criteria are unaffected** (both floors fail the
   negative by ≥ 14×); the E(γθ_f) law itself stands for the flux-dominant error.

4. **Adversarial (three of mine, one beyond the swept range):**
   - **γθ_f to 10⁶** (author's max 8000; γ to 1.25·10⁸, seed 777): one-shift still fails
     (p99 0.772 2D / 0.687 3D); exact-sum colour at frozen B=128 ≤ 0.060 oct — the claimed
     B=128 domain (γθ_f ≤ 2.6·10⁴) is ~40× conservative. The candidate is stronger than
     stated, not weaker.
   - **Heavy-tailed rest luminosity** (σ_ln 3, ~×20 spread; the rung froze equal-lum): literal
     L59 k̄ = Σlum·k/Σlum still fails p99 0.785; exact-sum stays exact. The equal-lum freeze
     did not prop up the negative.
   - **The `lc/lum` "linear-mix identity": false as stated.** The shipped `blackbody()`
     (crates/universe/src/view.rs L41-46) max-normalizes per member and gamma-encodes
     (pow 1/2.2) *before* the flux-weighted mix; mixing a 3000 K with a 10000 K member errs
     up to 0.47 oct (0.55 for a 4-temperature mix) against the encoded linear blend. It is
     γ-independent (exists identically at γ = 1, vanishes as T·k saturates) and shared with the
     per-body render path — so the substantive guard ("no k needed; no γ-aggregate error")
     survives, but the word "identity" is wrong and I corrected it on the page.

5. **Novelty: real.** `lab/rungs/` has no r13; the wiki held only 9c08's freeze-ready note.
   The struct read is new and resolves a documented ambiguity — 959a's own wiki entry says
   "Σlum" without saying seen-vs-rest, which is exactly what misled 9c08 (its checker named
   this fork as the gold condition). The 2D p99 numbers are new. Not a repetition: it
   reverses 9c08's applicability claim for the shipped record.

6. **Goal fit.** Premise layer under the adopted view record, pre-high-c: guards the channel
   at a gate (letter L59 one-sample rule dead as a rule) and shows a run's premise about the
   shipped record was wrong. PRINCIPLES 34: "the oracles are guards, not shepherds" — r13
   guards the readout channel, does not size it. PRINCIPLES 3: each member's k⁴ folded at the
   event the record already pays for. Not itself a 10× board-bottleneck move; its value is the
   guard plus the licence correction.

**Page corrections made in place** (wiki/representation-premises.md): the "per-case collapse
across floors case-identical" line now states the true domain (continuum + 3D p99 + 2D
saturation; 2D fine-floor p99 1.13× at γθ_f=4, systematic); the "linear-mix identity" now reads
"no k needed, not an exact identity for the shipped palette, ≤ ~0.5 oct, γ-independent, shared
with the per-body path"; the predictions line now says 6/8 with P7 misreported.

**The one experiment to gold.** Re-fly and state the floor law honestly as its own result —
freeze the 2D p99-vs-floor split as a criterion or addendum (one-shift at fine floor ≠ stock,
1.13× at γθ_f=4, systematic over seeds; the worst flux-visible one-shift error at fine floors
is off-axis, not a function of γθ_f alone — this *strengthens* the negative) — with the
dossier's P7 outcome and the "4 digits" bullet corrected in the record, and the palette
"identity" reworded. No new mechanism is needed; every number regenerates from the shipped
script today.

**What the author missed.** (1) Their own evidence table contradicts the 2D p99 collapse bullet
— the forward-cell column was read as the p99; P7's failure went unreported. (2) The palette
mix is not an identity for the shipped `blackbody()` (per-member normalization + gamma before
weighting; ≤ ~0.5 oct, γ-independent). (3) B=128's stated domain is ~40× conservative — worth
stating, it strengthens the candidate. (4) The record's own documented corner (959a's wiki:
the Σlum drift bound does not cover a hot, magnitudes-brighter body churning a cell's sums)
is the real gap between r13's algebraic 0.0 and a Rust re-fly — worth naming in "Unflown"
beside the serve-path re-fly, since float sub/add cancellation on churn is exactly where the
shipped sums could stop being exact.
