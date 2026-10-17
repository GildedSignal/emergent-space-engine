Grade: gold

**Abstract.** The certificate's angle bars, frozen from the shipped consumers (map pixel, contact scale, aggregate dipole), delete the re-kick from the flight law: 0 firings at every flyable N (T* = 3.37×10⁷ vs the 8×10⁶-gs horizon at 10⁶; my re-derivation puts the fence's N-threshold at ≈4.3×10⁸, ~260× beyond the memory wall), 0.28% of the deleted stream at 10⁹ (k* = 213). The mass bar never binds (dipole noise 2.5×10⁻⁸ of the host field even fully coherent). Contacts are forced below the law's acting angle grid (49 m is the shipped belt-body radius, scenario.rs:344; break-even at 547 m). Reproduced exactly; all constants verified in-tree; all five pre-registered predictions held. Closes f5bd's open requirement; corrects 10c4's q_mass. Adoption: the compose rung drops the re-kick arm and gains derived q_view(N).

## Reproduction

- `regen.sh` exit 0 (runner); my independent rerun: `bars.py` byte-identical, `verify_quotes.py` 5/5, exit 0.
- Every shipped constant verified in-tree: `AU_LS=499.004784` (page.html:58); belt a-band [2,3) AU (scenario.rs:333); kind===4 → `fillRect(x-1,y-1,2,2)`, names kind≤2 (page.html:142), `fitLog` kind≤3 (page.html:154); periapsis angle 32 bits (docs/law.md); 49 m = `Scalar::raw(34,-10)` = 49.06 m (scenario.rs:344); 313 = nladder's doll-born locals (nladder.md:21). f5bd's flown constants all on library-directions (belt max 2.2×10⁻³° at 7.41×10⁶ gs, cadence 3.55×10⁻⁵/B/gs, re-kick 0.51–0.6×, 8×10⁶-gs horizon, T* = 2.6×10⁴ gs at 10⁻²°).
- All arithmetic re-derived independently and exact: q_view 0.1436°/0.04542°/1.436×10⁻³°, T* 5.99×10⁷/3.37×10⁷/5.99×10⁶ gs, k* 2126/1196/213, q_contact 7.507×10⁻⁹°, grid break-even 547 m.

## Predictions

`predictions.md` (21:50:32.212) precedes `bars.out` (21:50:34). All five held numerically. Caveat: P2's premise sentence mis-attributes the 49 m ("encounters-page miss quantum, ev = −45"); it is the shipped belt-body radius, and the coarse-end distance quantum is D* = 1.6 km (cf2a) — the value was right, the provenance wrong.

## Adversarial cases (three of my own, two outside the author's tested range)

1. **Contact radius across the whole belt** (author tested r_mid only): at the inner edge p = a(1−e) ≥ 1.2 AU, q(49 m) = 1.56×10⁻⁸°, still 5.4× below q_grid. The forcing survives the belt's full radial range; physical touch scale (98 m) is 5.6× under break-even.
2. **The coarse dial turned against the claim**: at D* = 1.6 km (ev = −45's own quantum), q = 2.45×10⁻⁷° sits 2.9× ABOVE q_grid — but that dial cannot resolve 98-m contacts at all (cf2a: same-size pairs never charge). So the forcing holds exactly for dials that see contacts (b* ≤ 547 m); the page (checker 1's correction) states this domain correctly.
3. **The fence's N-threshold** (outside the author's N grid): the fence starts firing inside the horizon only at N ≳ 4.3×10⁸ (where q_view < 2.2×10⁻³°). "Zero firings at every flyable N" holds with ~260× margin in N beyond the 1.65×10⁶ wall, and ≥4.2× in time at 10⁶ (drift would need to run ~18× faster than f5bd's measured law). The t² inversion is conservative (late laws bend slower).
4. **Coherent drift on the mass bar**: the random-walk formula is the optimistic case; fully coherent secular drift gives (M_belt/M_host)·θ = 2.5×10⁻⁸ — 7.6 orders under 1, not "≥10 orders". The q_mass deletion survives regardless.
5. **Positional vs semi-major annulus**: bodies occupy r ∈ [1.2, 4.2] AU (Rayleigh-e ≤ 0.4), wider than the a-band [2,3): true neighbour spacing is O(1) larger, q_view coarser, the fence later — the safe direction for the deletion (the author conceded O(1); the 10⁹ constants k*/0.28% shift by ~1.4×, inside P4's band).

## Novelty

f5bd (this morning) left exactly this open: "the horizon derived from the certificate's angle bar stated in degrees — a number no page has frozen yet." 10c4 guessed "two bars q_live/q_mass from the view's belt-band resolution" with no numbers. This run freezes the bar (client paint code as the instrument spec, N^−1/2 from the annulus geometry), deletes q_mass, forces contacts to margins, and closes the fence question at flyable N. Nothing equivalent on view.md (its "map half-pixel free-run horizon" is the observer's row cadence — a different consumer), belt.md, kick-cadence.md, nladder.md or HISTORY. A refinement of 10c4, not a repetition: it kills half of 10c4's L4.

## Goal fit

Board #1 (bodies: 10⁶ flyable vs 10⁹): the freeze removes the compose rung's last free constant and deletes the re-kick arm from the flight law; the belt row's remaining bind is named (the resonance exclusion — corrected below), not the fence. PRINCIPLES: "the floor is what the player can differentiate" (register); §3 "Compute only surprises" (a sub-neighbour drift is not one); §28 "The view is an instrument"; §19 contacts below the acting grid signal the wrong representation.

## Page corrections (made in place)

- "the exclusion width (38.5% kept)" flipped: kick-cadence.md:251 — the belt's own measured **delete** is 274/712 = 38.5%, survival 61.5%. Corrected in wiki/library-directions.md.
- Checker 1's 49-m provenance correction verified (scenario.rs:344) and left in place.

## What the author missed

- The 49 m is the shipped belt-body radius, not a "delivered miss quantum"; the forcing's honest domain is "any dial that resolves contacts" (b* ≤ 547 m) — the coarse dial's own D* = 1.6 km sits above the grid.
- The coherent-drift worst case for the mass bar (7.6 orders, not ≥10).
- The fence's N-threshold ≈ 4.3×10⁸ — a stronger, unclaimed margin for the headline deletion.
- Two cosmetic slips: "38.5% kept" (flipped; corrected) and the dossier footnote "every 43 min at rtf 100" (2.6×10⁴ gs / rtf 100 = 4.3 min — 10× off; noise in the ledger either way, not carried into the page).
- The burn's interaction with the drift constants and the locals' pixel bar remain unmeasured — both author-flagged; neither touches the flyable-N deletion, which carries ≥4.2× time margin against any constant drift acceleration.
