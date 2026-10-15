Grade: lead

**Abstract.** Reproduced bit-exact (`python3 falsifier.py` rerun: every A/B/C number
identical, 1.7 s; adversarials hold — second GR energies E = 0.97/0.99 keep the log
form and the (δL/d)² error law, one decade deeper d, e → 0.999995 confirms the belt
e* boundary, non-crossing 0.9× boundary kick errs 9.9%). But the kill is not new:
`docs/law.md` retired this exact update on 12 October (six golds; "a kick recompiles
its cycle exactly"), and kick-jet's wiki already holds the same constant (9a04:
(15/8)(δE/(1−E))²), the plunge-fabricated-as-bound type error (4978) and the
root-distance certificate (ee08 = the run's proposed fix), measured on the shipped
integer law. New only: the Newtonian e* table, log-fit constants, ring budget.
Adoption residue: sync representation.md §3 to law.md.

## Reasons

1. **Reproduction: exact.** Clean rerun matches the stored `falsifier_out.json` on
   every field (float-identity compare; only `wall_s` excluded). `work/patch.diff` is
   empty and `git status` shows nothing outside the run folder. All headline numbers
   (16.3% at e = 0.99/1e−3; e* = 0.9616/0.6483/0.999995; 7.1/139 turns; T = 192.7 +
   21.8·ln(1/d); 4.9% at d = 1e−3; MA T = 365 vs plunge) regenerate. The math is
   sound: I verified the closed forms (x = 2√(1+e)δv/(1−e) at periapsis, |E| = (1−e)/2;
   the separatrix conditions (1−2u)² = E²(1−3u) and L² = 1/(u−3u²); the Binet
   first-integral and cubic) independently.

2. **Predictions: honest.** mtime order is predictions.md (20:46) → falsifier.py
   (20:52) → output (20:54). Two misses disclosed (H1's "1% to x ≤ 0.3"; H5's 1e−6 vs
   2.3e−6). The GR exponent was genuinely held out; the log reading is correct (local
   exponents 0.065 → 0.060 decreasing; a power law would hold them constant).

3. **My adversarial cases (one class outside the author's range):**
   - Second GR energies (author fixed E = 0.95): E = 0.97 → T ≈ 457 + 14.4·ln(1/d),
     E = 0.99 → T ≈ 2294 + 12.0·ln(1/d); MA error at d = 1e−3, δL/L = 1e−3 falls to
     1.9e−2 / 3.5e−3. The (δL/d)² scaling holds; the prefactor is b/2T and collapses
     as E → 1. The family itself exists only for E ≥ √(8/9) ≈ 0.9428 — E = 0.95 sits
     0.8% above the family's birth, so the 4.9% headline is the worst point of a
     narrow band (not stated in the dossier).
   - Non-crossing boundary kick (0.9× the gap at d = 1e−3): exact bound T = 394.9, MA
     355.9 → 9.9% error. The near-boundary band is bad on both sides; crossing adds
     the type error. Extends, does not refute.
   - Deeper Newtonian tail (author swept e ≤ 0.999): belt quantum at e = 0.999995 →
     ε₁ = 0.87% (the e* boundary confirmed numerically); encounter kicks at e =
     0.9999/0.99999 kill at 6.6e3/2.0e6. The (15/8)x² law tracks to 1–2%.
   - Site control: apoapsis kicks (x = 2δv/√(1+e)) err 3.8e−6 at e = 0.99 vs 16.3% at
     periapsis — 10⁴–10⁶× safer. Confirms the "worst site" framing; the e* table is a
     *periapsis* boundary, which the dossier implies but never numbers.

4. **Novelty — the decisive point.** The premise was already killed, by stronger
   instruments, and already deleted from the live law:
   - `docs/law.md` (Events → Perturbed motion): "**The jet is retired (12 October):**
     updating a compiled cycle from stored derivatives by a multiply-add carries a
     one-signed phase error that fails both frozen budgets on every orbit within its
     margin… (lab golds 20261006-1249-redteam-4978, …-0ccd-b33f, …-4808-d617…).
     **A kick recompiles its cycle exactly, as the plane does.**" Commit 49d59704,
     12 October — three days before this run. The adopted fix (always-recompile) is
     stricter than the trigger this run prices.
   - `lab/wiki/kick-jet.md` — 70 runs, titled "updating a compiled cycle from stored
     derivatives (law.md line 36)", i.e. exactly this run's premise — already holds:
     df81 (gold) "multiply-add error C·drift² unbounded… re-anchor rule proposed";
     4978 (gold) "jet invalid near the Schwarzschild separatrix… **plunge fabricated
     as bound**"; 9a04 (gold) "E-axis failure **(15/8)**(δE/(1−E))²… tri-predicate
     complete, freeze-ready"; 6164/ee08 (gold) "the multiply-add is false outside a
     corner… the T-channel **(15/8)** dominates; one **both-ends root-distance
     certificate**" — the same constant, the same class-change error, and the same
     fix shape as this run's |δL|/|L−L_sep| trigger.
   - The attacked sentence survives only in `docs/representation.md` §3 — a DRAFT
     ("supersedes nothing until the falsifiers in §7 have run and Julien says yes"),
     untouched since 6 October. The dossier's framing ("deletes a wrong law before it
     is frozen into r2's successors"; "no such trigger exists… its absence is what
     freezes") is true of the draft's text but false of the repo: the live law
     carries both the kill and the fix. "Rung: none" is technically true and
     rhetorically misleading — three golds and a law retirement guard it; only the
     frozen-rung family does not. Per the lab's rule ("a repetition is not gold,
     however well done… cite the run or H entry"), this is a lead.

5. **Dossier defects (small, named):**
   - "φ cycle to 1.2e−5" is not regenerable: stored and rerun both give 7.3e−5 (6×
     worse than written).
   - "half of r1's own sampler" for e ≥ 0.6483: the sampler spans e ≤ 0.9, so that is
     the top ~28% of a uniform draw. "Half" overstates. (Corrected in the page.)
   - "unbinds after 18 kicks": 17 kicks complete; the 18th would unbind.
   - "the belt's own churn record, 27–55% at eps 0.03–0.10": not findable in
     lab/wiki/belt.md or any wiki page I searched.

6. **Page:** corrected in place — the Current-best paragraph and the Refuted bullet
   now cite kick-jet's golds and law.md's retirement; "half of r1's sampler" fixed;
   the Runs entry records the grade context. Physics claims left standing: they
   reproduce and generalize.

7. **Process finding for the integrator:** two red-teams in one day (fe85, then this)
   missed kick-jet's page on the same premise — the wiki's discovery path failed, not
   just one author. A cross-reference from binet-cells' open directions to kick-jet
   (or an index alias "cycle update → kick-jet") would have prevented both.

## What the author missed

- `docs/law.md`'s retirement paragraph — the single most load-bearing text on this
  premise — and kick-jet's page. The wiki rule ("every author reads the page of its
  topic") points here: the topic page is titled with this run's premise and cites
  law.md line 36. Filing under binet-cells also hides the result from the topic's
  history.
- The separatrix family exists only for E ≥ √(8/9) ≈ 0.9428, and the error prefactor
  b/2T collapses as E → 1 (3.5e−3 at E = 0.99, same d and δL): the 4.9% headline is
  the worst point of a narrow family. A one-line domain statement would have made the
  GR arm honest about its range.
- The belt-quantum safety row conflates kick size with site: at apoapsis even
  encounter-scale kicks are safe at any e; the trigger should carry the site factor
  (√(1+e)/(1−e) vs 1/√(1+e)), not only x.
- The adoptable residue is not an experiment but a doc patch: amend
  representation.md §3's stale sentence to law.md's rule. The run's numbers (e* table,
  ring budget) are the right annotation for that patch, and the proposed r2
  near-separatrix arm remains reasonable as a guard for the law's integer grid —
  where, as the author's own lens notes, the shipped plane already recompiles per
  kick.
