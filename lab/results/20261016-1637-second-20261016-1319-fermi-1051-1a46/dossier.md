# Dossier — 20261016-1637-second-20261016-1319-fermi-1051-1a46 (second author on fermi-1051)

**Claim.** The checker's named gold experiment is flown — step 5's delete arm (ES_SECULAR: a ship
secular-legal against **every** perturber of its doll, r9's τ_p = 3·(m_p/m_host)·(a/a_p)³ < τ₀ for
the parent and every secondary, plus a resonance exclusion, default off) behind a per-body flag —
and the flight **adjudicates the composed candidates and corrects both the author and the
checker**: the locals' storm falls 334 → **131 max / 26 p99** events per frame over 5,400 game-s
(envelope 212·240·207·251·229·195·334 → 46·37·21·48·26·9·131; the residual 131-beat at frame
3173, the same frame as OFF's 334), 2.5% from the checker's "≈134 Moon-corrected" candidate and
57% from the script's proportional 83.5 (refuted), with the event ledger **−70%** (22,219 →
6,580; kicks −85%) — and the legality domain measured from the runtime flag (cross-checked by an
independent recomputation, 0 mismatches over 1,023 ships): **in-situ 85.8% legal** (the Moon's
line at a = 116,333 ru, inside the top octave — the author's "100%" and the checker's "~80%" both
wrong; the checker's magnitudes are mutually inconsistent with (a/d)³), the L4/L5 quarter spared
75/75, the belt only 38% deleted because the frozen resonance rule (every q/r ≤ 8 within 2%) is
wider than any tide fact; and the freeze's own B14-class debt is behind the law's quantum fence
(Δangle < 10⁻⁴° vs the kicked path: the shipped metronome's tide impulses are sub-quantum and
carried, so it never applies the precession either at this cadence).

**Bottleneck.** Board item 1 (bodies in the flyable engine). fermi-1051's silver said "legality
domain and storm measured, not composed → gold"; both are now measured, on shipped code (patched
OFF bit-identical to pristine main on the full 13-case `ladder_digest` pass), and the decision
content sharpens: the delete and the chained de-phase (4fa8) compose — delete the legal set,
chain the spared — and the delete is the only arm that also cuts the belt stream (the 10⁹ rail).

**Evidence** (this Linux box, budget-free coast, rtf 100, seed 1, threads 1, `nladder` ported to
Linux by this run's patch; every command in regen.sh, ≤ 15 min total):

*The arm* (`crates/universe/src/step.rs`, `plan_interval_inner`: legal ships' plans cleared —
the `has_forces == false` pure-tube state; never the player or a fleet member; legality from the
ctx's own units: mass ratios via `Ctx::tide` and `info[j].gm`, distance ratios from the keys).

| Flight (max/p99 ev per frame) | OFF | ES_SECULAR |
|---|---|---|
| N=1000, 1,900 gs | 240 / 146 (4fa8's record ✓) | **46 / 33** (below the N=0 floor 51) |
| N=1000, 5,400 gs | **334 / 136** (the record ✓) | **131 / 26** |
| N=0, 1,900 gs | 51 / 36 (the floor ✓) | 46 / 33 |
| N=10⁴, 1,900 gs | 240 / 146 (N-flat ✓) | 46 / 33 (N-flat ✓) |
| events 5,400 gs | 22,219 (kicks 9,217 — the record ✓) | **6,580** (kicks 1,382) |

- OFF reproduces 4fa8/4c22's record **exactly** at both horizons (334/136/22,219/9,217 and
  240/146/11,111/3,624): the instrument is the record's, not a new one.
- The residual 131-event beat sits at **frame 3173, the same frame as OFF's 334** (4c22's
  biggest beat): the spared standing set's comb (the quarter 75 + the Moon-tide top 33 + the
  plane's ships + the fleet), exactly the class the resonance exclusion protects.
- **Patched OFF = pristine main**: full `ladder_digest` pass (13 cases × 4 schedules) identical
  to the pristine binary's, hashes and counts bit for bit (flights/digest_off_{patched,pristine}.txt;
  the two files differ only in wall-time annotations).

*Legality, measured from the flight and cross-checked* (work/analyze.py on work/states_*.csv; the
engine's own per-body decisions dumped at the flight's end, recomputed independently in python
from the dump's dolls/sources/keys — 0 mismatches over 1,023 non-fleet ships):

- The Moon, not the star, draws the in-situ line: τ_Moon = 3·2⁻⁶·(a/273,684)³ crosses τ₀ at
  **a = 116,333 ru** (the star's line: 168,243 ru); top deleted in-situ a = 108,966 < 116,333 ✓.
  Octave 4 (top): 12/42 deleted; octave 3: 38/41 (3 resonance stragglers); octaves 0–2: all.
  **In-situ 200/233 = 85.8%** — the author's 100% wrong, the checker's "~80%" closer in fraction
  but wrong in mechanism: τ_Moon(83,200) = 1.32×10⁻³ is 2.7× UNDER τ₀ (their "1.1× over"), and
  their two magnitudes (3.9×10⁻³ at 83,200, 0.175 at 166,400) differ by 45× where (a/d)³ gives
  8× — their Attack-1 arithmetic is internally inconsistent even where its verdict survives.
- The quarter: spared 75/75 by the co-orbital rule (|a/a_Moon − 1| < 5%).
- The belt: 274/712 deleted — the frozen resonance exclusion (every q/r ≤ 8 within 2% for each
  of Home, Cinder, Giant) spares >half the belt (Home's 7/3, 5/2, 8/3, 3/1 chain is dense in
  [1.8, 3) AU). A law choice, not a tide fact: my own P1 belt prediction (85–98% legal) failed
  on exactly this.

*The freeze's own legality (the B14-class probe, measured)*: |angle(arm) − angle(OFF)| at the
final tick, every deleted local: **0.000°** (below 10⁻⁴°). The continuum secular precession
(~(1/4)·2π·τ per orbit) is not applied by EITHER path at this cadence — the kicked path's tide
impulses are sub-quantum (`quantize` carries them; a kick that fires nothing changes no state),
so the delete's debt is behind the same quantum fence, going live only near ~2¹⁶ carried kicks
(~10⁷ game-s at the locals' cadence). On game horizons the delete is behaviour-identical to the
path it replaces; the spared set is bit-identical by construction (an event's ctx is read-only in
others — verified: every spared body's end state matches OFF at the dump's full printed
precision).

**Predictions** (predictions.md, written before the decisive flight): P2 **held** (max 131 ∈
[90, 180]; the 134-class candidate won — and my sub-call "p99 ∈ [35, 75]" beaten: 26). P3
**held and strengthened** (−70% vs predicted −45–60%). P4 **held** (OFF = pristine, 13 cases).
P1 **split**: the in-situ fraction measured 85.8% — my own sub-prediction (94–97%) failed by
under-counting the Moon's reach (I misplaced the crossover, 152k vs the true 116k), and my belt
sub-prediction (85–98% legal) failed on the resonance rule's width; both failures are reported
as the measured corrections above. P5 **held with a twist** (every per-orbit residual under the
τ₀ bound — trivially, at 0: the fence finding). P6 (RES control): with the resonance exclusion
off, the storm does not drop below the arm's (46 = 46 at 1,900 gs) — the quarter's own comb is
below the plane's floor at that horizon; the control's physics content (the quarter's protection)
is already decided by the co-orbital rule's 75/75.

**What would make it wrong.** The resonance exclusion's domain is not measured against B17's
libration widths — as frozen it spares over half the belt, so the belt's delete share is a law
choice, not a fact. The 115 belt bodies whose current key a sits below the 2-AU birth band
(identically in both arms, radii consistent with the low-a keys) are unexplained within this
run's budget — arm-independent, so unbiased for every A/B number here, but the belt readout
needs its own run. The freeze's far-horizon debt (~10⁷ game-s) is composed, not flown; the
29.3 µs/event M1 projection and the memory wall are standing records, not re-measured here.

**Cost of adopting.** The flag is 60 lines in `step.rs` + the Linux port of `nladder`'s
footprint (work/patch.diff, default off, OFF bit-identical). A shipping version needs the
libration-width resonance rule (B17's W = 2.5·μ^(2/3)) in place of the ±2% bands, and the sparse
secular re-kick for horizons past the quantum fence. Fit with PRINCIPLES: #14 "no work for no
reason, so no ticks" (the metronome deleted, not spread); #1 the cheapest compute is compute not
done (−85% of the kicks); #22 "the simulation decides" (the flag reads the same ctx the kicks
read — no external table).

**The lens.** The second author's lens is the checker's named experiment; what it may have
missed: no second seed, no burn arm, and the RES control ran at 1,900 gs only (the quarter's comb
may show at longer horizons — the 5,400-gs arm beat of 131 already contains the spared set's
contribution, so the control's content is mostly decided).

## Commands (regenerate everything: `bash lab/results/20261016-1637-second-20261016-1319-fermi-1051-1a46/regen.sh`, ~13 min)

- Flights: `nladder <N> coast <s> 100 1000000` with `ES_SECULAR=1` / off; `ES_STATES`/`ES_DUMP`
  for the dumps (regen.sh rebuilds every table above).
- Analysis: `python3 work/analyze.py` (legality cross-check + probe), `python3 work/legality2.py`
  (the corrected domain and the wall ladder with the measured storm constant).
- Digest control: patched-OFF vs `bin/ladder_digest_pristine`, 13 cases × 4 schedules.
