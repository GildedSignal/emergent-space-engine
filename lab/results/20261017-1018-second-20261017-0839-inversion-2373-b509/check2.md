Grade: silver

The calendar (shipped `tier::arm_pair`) is measured, sound and sweep-deleting: 1.01–1.16 µs/pair
vs the exact check's 57.7/414.7 µs (57×/411×), 0 dropped/added vs `group_events` on keys, train,
clustered, bimodal, high-e and H=500-orbit fleets (three seeds + my 424242); negative controls
drop 45–6,492. The sweep basis of silver 2373 was understated 128–143×. But the claim's central
derived number fails recomputation: compose.py's `** 0.5` F* interpolation assumes a term ∝ F²
while the run's own three decades measure ∝ F^1.03–1.07 — honest keys F* ≈ 4,100 (L=100) /
1,050 (L=25), not 6,463/3,232; train F* < 1 (stronger than the claimed 89). The dossier's
2.4×10⁸-core standing-contact figure is a ~4,500× slip (true: 5.4×10⁴; conclusion survives).
Clustered formations — taleb-09b5's battle-group — were unmeasured: my probe shows the birth
pass pays a complete-graph window there, F* ≈ 200 (L=100), barely above the sweep's ~124; the
65× lift is uniform-phase only. Page corrected in place. Cost to adopt: wiring (standing-contact
state, due-queue), no new physics.

## Reasons

**Reproduction (clean tree, my own runs).**
- `bash regen.sh` was run by the runner (exit 0, full log in `regen.log`): every number in
  `work/composed.txt` matches the author's dossier basis. My own rerun: `fleetk` count-identical
  (32 lines, only µs/ns timing fields differ at noise level); `fleetcal 20261017` rows through
  the first train arm are count-identical (pairs 666,260/24,976/2,660,189/312,839,484/267,330/
  36,192,643; armed 1,156/54/4,775/9,541-sampled/4,708/9,409,913; reach to 4 decimals). The
  instrument is print-only, shipped pieces only (`arm_pair`, `pair_events`, `group_events`,
  `Neighbours` — all verified present on main, `tier.rs:538`, `dioph.rs:9`).
- Held-out seed 777 reproduces every page citation: train fire_per_kick 1,862.45, keys 17.52,
  ddue_med 0.0000, γ = 1.92, truth 0/0 on both populations, negctl drops 1,264/6,293/45.

**Predictions.** `predictions.md` mtime precedes the decisive outputs by ~27 min (fit on pilot
seed 7 only, `work/pilot-seed7.jsonl`). 14/16 bands hit; P7 miss disclosed and the composition
switched to the measured value; P10's band actually hit (0.72 ∈ [0.6,1.3]×iv0) but the author
killed the recurrence model anyway per pre-registered K4 — conservative, honest. No kill
criterion fired except K4's declared fallback.

**Attack (my five, seed 424242, all outside the author's tested set; probe preserved at
`/tmp/checker2-adv.rs`).**
1. H = 500 orbits (5× the author's horizon): 65,002 events, 0/0.
2. Bimodal two-key fleet (untested population shape): 13,319 events, 0/0.
3. Clustered σ_l=0.02 + σ_e=0.05, H=200: 77,602 events, 0/0 — but window = 1,999,000 = the
   complete graph at F=2,000.
4. Refusal boundary da=1.2/1.4e-4 at interval horizon: reach 2.70/3.13 < π, not refused, armed
   10.3/11.0 M — the H* law behaves; no anomaly.
5. eps=1e-2 kick (10× the author's ladder max): 82.7 firings/kick, ddue_med ≈ 4.07 intervals —
   slack-deferred re-arm dies at burn-scale kicks; re-arm cost flat (1.15 ms/kick).

**Novelty.** The wiki page held 2373's proposal unmeasured and the sweep basis uncorrected;
189e's belt-scale calendar kill is a different domain and a different (CF-rank) calendar. The
129–143× horizon correction rewrites 2373's own composition; the firing-flow and kick-created-
firings terms are new. Not a repetition.

**Findings that cost the grade.**
1. **F* interpolation error (in the claim sentence).** `compose.py:72` uses
   `fstar = f * (BUDGET/cores)**0.5`, valid only for a term ∝ F². The measured keys term runs
   0.95 → 10.08 → 118.08 cores per decade (∝ F^1.03–1.07, near-linear, because pairs ∝ F² is
   divided by F fleets). Honest: F* ≈ 4,100 (L=100) and ≈ 1,050 (L=25), not 6,463/3,232 — the
   "65× up" is ~40× (sweep's own linear refit: F* ≈ 124). The train F* ≈ 89 understates the
   floor in the other direction: the train term is also ∝ F, so no da=1e-4 train size fits at
   φ=1 (F* < 1). The verdict row (F=10³ FITS, 10⁴ OVER) is measurement, unaffected.
2. **Arithmetic slip.** Dossier: "armed×31.6 ms per interval (2.4×10⁸ cores at F=10⁴)". The
   measured numbers compose to 4,775 × 31.7 ms × 10⁵ fleets / 281.4 s = 5.4×10⁴ cores. The
   qualitative conclusion (standing contacts must be stored state; 5.4×10⁴ is 13,000× over
   budget) stands.
3. **Clustered-formation domain gap.** fleetcal has no clust arm. For σ_l ≲ reach the birth
   arm pass pays a near-complete-graph window (my A3/A5), so the calendar's keys F* collapses
   to ≈ 200 (L=100; ≈ 50 at L=25) — no meaningful lift over the sweep for exactly the
   formation shape (taleb-09b5) that motivates the fleet row. The dossier scopes to "keys
   fleets" honestly, but the page's "up to ~6×10³ ships" generalized across the gap.

**Goal fit.** Board item 2 (encounter work at 10⁹). Deletes the window sweep as the fleet
representation and closes the missing ledger row with a certificate term and a population
term. PRINCIPLES #19: "a fix signals the wrong representation… the right representation always
just feels right" — the calendar is the boat for uniform fleets; and #3 "compute only
surprises" — the firing flow it leaves standing is the surprise rate, correctly not hidden.

## The one experiment to gold

Refit the composition on the measured exponent (F* linear in the measured term, both keys and
train) and add a `clust` arm to `fleetcal` (clustered keys birth pass at F=10³–10⁴, σ_l
0.01–0.05) so the page's corrected numbers — F* ≈ 4.1k/1.05k uniform, ≈ 200 clustered, train
F* < 1 — are regenerated by the shipped instrument instead of by this checker's probe. Every
constant for it is already measured.

## What the author missed

- The sqrt-vs-linear scaling of their own composed term (three measured decades were in hand).
- The clustered-formation cost: they cite taleb-09b5 on the page and still left the battle-group
  shape unpriced — the one population where the calendar fails to lift the ceiling.
- The 2.4×10⁸ slip would have been caught by recomposing their own JSONL once.
- Minor: page said "~9.4 M again at interval 10 — steady"; the JSONL says 6.80 M (0.72×) —
  corrected in place. My A4 shows slack dies entirely at eps=1e-2 (ddue ≈ 4 intervals), which
  the dossier's "kick rates are policy" caveat covers but never bounded.
