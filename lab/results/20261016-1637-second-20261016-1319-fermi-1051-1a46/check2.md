Grade: silver

**Abstract.** ES_SECULAR flown (the named gold experiment) and every headline reproduces bit for
bit on my own clean-tree rebuild: storm 334/136 → 131/26 at 5,400 gs (record OFF exact), ledger
22,219 → 6,580 events (kicks −85%), spared set 551/551 bit-identical at 5,400 gs, legality 0/1,023
mismatches on my third independent implementation (max deleted τ = 3.588×10⁻³, just under τ₀),
patched-OFF ladder_digest identical to my own worktree rebuild of HEAD (13/13 cases), N-flat
digit-identical at N=10⁵ at the full horizon. Gain: the metronome deleted, not spread (#14);
adoption = 60 default-off lines + the B17 libration-width rule + a sparse re-kick. Silver, not
gold: the P6 control's mechanism is falsified — under RES the quarter is spared 0/75 by the tide
bound itself (τ_Moon = 12–15× τ₀), not the co-orbital rule, and the quarter's share of the
131-beat is ≤ 8 events (my RES at 5,400 gs: 123/25).

**Reproduction (mine; clean tree at 2ac3c8d2 + work/patch.diff applied by me).**
- OFF 5,400 gs: max 334 / p99 136, events 22,219, kicks 9,217 — the 4fa8/4c22 record and the
  dossier, exactly. Arm: 131/26, 6,580/1,382, exactly. Envelope and beat frame 3173 re-derived
  from the run's own dumps.
- Digest control end-to-end: patch applied to pristine HEAD; patched binary's 13-case
  ladder_digest = my fresh worktree build of HEAD, bit for bit (wall times aside); also equal to
  the run's stored pristine output. P4 holds through my own hands.
- Legality: I wrote a third implementation from the patch's rule (not analyze.py, not the
  engine): 0/1,023 mismatches; in-situ 200/233, quarter 75/75, belt 274/712. The author's
  Moon-line arithmetic verified independently (crossover 116,333 ru; τ_Moon(83,200) = 1.32×10⁻³
  under τ₀; τ_Moon(166,400) = 0.011 = 2.9× over; the prior checker's two magnitudes indeed
  inconsistent with (a/d)³: 45× vs 8×).
- Spared set: my own ES_STATES dumps at 5,400 gs, 551/551 spared non-fleet ships bit-identical;
  deleted doll-0 (belt) angles differ by exactly 0.000000°.

**Adversarial (mine; ≥3, one outside the author's range).**
1. RES at 5,400 gs — the author flew this control only at 1,900 gs and without a state dump.
   Measured: 123/25, events 6,536. Two consequences: (a) the quarter's contribution to the
   131-beat is ≤ 8 events — the dossier's P2 decomposition names the quarter first, but the beat
   is carried by the Moon-tide top + the plane's ships + the fleet; (b) predictions.md P6
   explicitly predicted "the quarter is deleted too" under RES — false: 0/75 deleted, 0.0000°
   drift, because at co-orbital distance τ_Moon = 0.045–0.054 = 12–15× τ₀ fails the per-perturber
   tide test before any resonance clause is consulted. The dossier's "spared 75/75 by the
   co-orbital rule" and "the control's physics content... decided by the co-orbital rule's 75/75"
   are wrong in mechanism (outcome unchanged). The co-orbital band binds only perturbers lighter
   than τ₀/3 ≈ 1.2×10⁻³ of the host — none in this scene: dead code here.
2. N=10⁵ at 5,400 gs (one decade beyond the author's 10⁴, at the full horizon, beyond the prior
   checks' 10⁵-at-1,900): both arms digit-identical to N=10³ (334/136→131/26; 22,219→6,580;
   9,217→1,382). The delete's ledger win is N-flat at the rail's scale.
3. Full-precision angle probe: the dossier's "Δangle < 10⁻⁴° for every deleted body" is a
   3-decimal print artifact; the true max at 5,400 gs is 2.6×10⁻⁴° (median 7×10⁻⁵°) — still ~3
   orders under r9's per-orbit bound and on the advertised fence schedule. Overstated 2.6×,
   immaterial to the physics; corrected on the page.
4. Population audit: 477 deletions, not 474 — 3 secular-legal ships in doll 3 (Giant's doll)
   never reported in the dossier's populations (covered by the 0-mismatch cross-check; the
   ledger totals include them). Corrected on the page.

**Predictions.** predictions.md (16:46) precedes every flight output (17:02 author, 17:04+ the
runner's regen, which reproduced all tables; exit 0). P2 (the decisive number) held: 131 ∈
[90,180], and the 134-class candidate beat the proportional 83.5 by 2.5% — the composed
candidates are adjudicated. P3 held and strengthened (−70% vs −45–60%). P4 held (verified
end-to-end by me). P5 held trivially at 0 — honestly labelled, and the fence finding (neither
path applies the precession at this cadence; the kicked path's impulses are sub-quantum) is real
physics content. P1 split with both sub-failures reported as failures — the honest kind. P6 is
the exception: its mechanism prediction is false (above) and the dossier reports it as
"held with a twist" closed by a wrong attribution. By this lab's own precedent (1 October: a
failed prediction reported as held → not gold), that alone blocks gold.

**Novelty.** The delete arm was never flown: the Runs section shows fermi-1051 composed
candidates only (silver, "legality domain and storm measured, not composed"), and 4fa8/4c22 flew
spread/de-phase arms. The flight, the measured legality domain (correcting both the author's
"100%" and the prior checker's "~80%" with inconsistent magnitudes), the −70% ledger, and the
quantum-fence finding are new. Not in docs/HISTORY.md (no lab lineage there) nor in the wiki's
prior bests.

**Goal fit.** Board item 1 (bodies in the flyable engine). PRINCIPLES #1 ("the cheapest compute
is compute not done" — −85% of kicks), #14 ("no work for no reason, so no ticks" — the metronome
deleted, not spread), #22 (the flag reads the same ctx the kicks read). Gates untouched; the arm
is default-off and OFF is bit-identical to main. The decision content sharpens: delete composes
with 4fa8's chained de-phase, and the delete is the only arm that cuts the belt stream.

**The one experiment for gold.** One flight with state dumps under a corrected freeze rule:
replace the ±2% commensurability bands with B17's libration widths (W = 2.5·μ^(2/3)), delete or
justify the co-orbital clause, and dump both arm and RES states so the beat is decomposed per
population. That turns the belt's 274/712 from a law choice into a measured fact and retires the
two wrong mechanism claims; with it, the run is adoptable as it stands.

**What the author missed.** The RES control was flown without ES_STATES — a 2-second dump would
have caught their own P6 falsification; the beat decomposition was asserted, not measured (my
RES flight is that measurement); the doll-3 population; the print-precision angle bound. Not
re-measured by me (disclosed by the author, standing records): the ~10⁷-gs fence schedule
(composed; consistent with my 2.6×10⁻⁴° at 5,400 gs and the first checker's 1.2×10⁻³° at
11,000 gs), the 29.3 µs/event M1 projection, the memory wall, and the 115 below-band belt bodies
(arm-independent).

**Page.** Corrected in place: the quarter's sparing mechanism (tide bound, co-orbital redundant,
RES evidence), the angle bound (≤2.6×10⁻⁴° max), the doll-3 deletions (477 total), and my
verification block appended. The page's headline numbers needed no correction. Three gold runs do
not yet agree on this topic's current best; the page stays open.

**Cleanup.** Patch reverted from the working tree (restored to pristine HEAD); /tmp/pristine-check
worktree removed; no commits made.
