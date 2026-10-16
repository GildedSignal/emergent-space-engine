# Check of 20261016-1637-dynamics-87fd (dynamics lens)

Grade: silver

**Abstract.** Claim: the comb cure (ES_CHAIN+ES_LOCAL_STAGGER), first adjudicated on the 313 doll-born locals no frozen gate can see, is innocent at every gate-level quantity (ensembles ≤3×10⁻⁵, tails flat) but triples the median per-body drift (|ΔE/E₀| 2.0→7.4×10⁻⁶ per 4,500 game-s; kill criterion fired). Reproduced **bit-identically** — but only after I deduplicated `work/patch.diff` (shipped as the same 522-line diff appended twice, so the runner's `regen.sh` exits 1 from any clean tree; the fix round's "verified from the restored tree" is false). My held-out cases: seed 3 replicates (OFF 2.06, cure 9.2×10⁻⁶); N=10⁴ identical; **2× horizon flips the channel** — arms cross by 6,700 game-s and OFF ends worse (19.8 vs 19.4×10⁻⁶ med, 1.28 vs 0.87×10⁻³ max), so the "priced channel" is a closing transient, not a stable bill. Gain: the legality debt is measured and the doll-born gate is freezeable. Gold needs the self-regenerating record plus the horizon series.

## Reproduction

- `regen.sh` as shipped **cannot run from a clean tree**: `work/patch.diff` is byte-identical to itself twice (`diff` of halves: IDENTICAL; `git apply` is atomic → always fails, matching the runner's exit 1 and regen.log). The fix round touched only untracked `regen.sh`, so its tree-save re-appended the author's identical diff; `fix-final.md`'s "full end-to-end run from the restored tree" evidently ran with the author's edits still applied (regen.sh's `grep ES_CHAIN` guard then skips the apply). Per the lab's own precedent (5 October: "results that the shipped code could not regenerate" barred gold), this caps the grade.
- After deduplication (`sed -n '1,522p'`), the patch applies cleanly at HEAD 2ac3c8d, and **all five flights are byte-identical to the committed ones**. Every table number verified: off s1 251/136 ev/fr, enc 183, kicks 7,736, med/p99/max |ΔE/E₀| 2.0e−6/3.2e−4/6.3e−4; cs s1 52/25, 184, 7,937, 7.4e−6; ph s1 53/25, 183, 7,928, 7.9e−6; off s2 274/140, 208, 7,939, 1.9e−6; cs s2 66/26, 210, 8,143, 7.1e−6; E₁/r₁ medians to the digit; census {2:310, 3:3}, dead 0, refusals 0 in all arms.
- The engine diff is env-gated and default-off (flags checked before the original `aligned` path; OFF ≡ shipped law). The probe is print-only, index-matched drifts through the shipped `Binding::readout`, doll filter `b.doll != 0`, budget-free coast as claimed. Sound instrument.
- Ensemble claims recomputed from the outputs: cure-vs-OFF E₁/L₁/r₁ deviations ≤3×10⁻⁶; seed band 3.46×10⁻²; P2's band test fails on the medians (27–32× outside) and holds on p99/max/counts; kicks +2.6%. All as the dossier states.

## Predictions

`predictions.md` is concrete, arms and quantities match the flights, and the pre-registered kill (P4) fired **against the author's own cure** and was reported as fired — strong honesty signal. The original flight mtimes were overwritten by the fix round's rerun, so file-time order can no longer be audited; I accept the pre-registration on internal evidence (a post-hoc author rarely registers a kill that fires on themselves).

## Attack (my cases)

1. **Third seed (the dossier's own named kill):** OFF's band stays tight (s1 2.01, s2 1.92, **s3 2.06×10⁻⁶**) and the channel replicates (**cs s3 9.2×10⁻⁶**, 4.5×). The tight-band premise survives; the channel is real at the flown horizon.
2. **Double horizon (9,000 game-s — outside the flown range):** the channel **closes and reverses**. |ΔE/E₀| med: off 2.0→19.8, cs 7.4→19.4 (×10 vs ×2.6 growth); at 6,700 game-s they have already crossed (off 16.2 vs cs 14.3×10⁻⁶); OFF's max is worse (1.28×10⁻³ vs 8.7×10⁻⁴). Ensembles stay innocent at 9,000 s (≤3×10⁻⁶). So the shared tick **delays** the drift's onset without bounding it — the "midpoint-class sampler" mechanism cannot be the whole story, and the headline constant (×3–4) is horizon-local. The dossier itself flagged this as its wrong-maker; it fired, in the cure's favour.
3. **N=10⁴ (next decade):** identical to the digit on every doll statistic (same 313 doll bodies; frame collapse 251→50). The channel is N-flat. Supports.
4. The 9,000 s arm also confirms the arming control one horizon out: OFF returns to the record's 334-class, the cure holds 52.

## Novelty

4fa8 measured the collapse and its cost; 21a7 proved the frozen gates structurally blind; **no prior run adjudicated the cure on the doll-born population** — no HISTORY.md entry and no wiki page holds the per-body drift measurement. Genuine increment, not a repetition.

## Page

Faithful, and I corrected three overstatements in place: the channel is now marked horizon-local with the crossing numbers (Current best), the growth-law "open question" is marked answered (direction 1, freeze the gate at the worst horizon), and direction 4's channel is marked a closing transient. Also noted the doubled patch on the page.

## Goal fit

Moves the board's furthest bottleneck (bodies in the flyable engine) by replacing an unmeasured legality debt with a measured band, exactly the "rough first, refine when a certificate could break" (21) shape; behaviours over many bodies and seeds, never trajectory identity (20); the fired kill is reported as a priced bill, not a dead method (9, H0183).

## The one experiment for gold

Dedupe `work/patch.diff` (one line) so `regen.sh` exits 0 from a restored tree, and fly the horizon series (4,500/6,700/9,000+ game-s, both arms, seeds 1–3) into the record, restating the channel as a measured transient — then freeze the doll-born gate at the worst horizon. That makes the record self-regenerating and the claim horizon-qualified; both are within one short run.

## What the author missed

- The shipped record does not regenerate (doubled patch), and the fix round's verification claim is false as delivered — the exact failure mode that has barred gold before in this lab.
- The channel's horizon dependence: one more decade of the swept number (time) was the natural next arm and it flips the sign of the headline; the "midpoint-class sampler" inference is marked [INFERENCE] but the data that would have qualified it was one flight away.
- The ensemble at the doll's centre uses doll-units M=c=1 — fine for band comparison, but |E₀| near zero (p01 drift 10⁻¹⁴) means some bodies normalize on the 10⁻¹² floor; harmless for medians, worth knowing for tails.
- Burn and long-lived-battle arms remain unflown (flagged honestly by the author).
