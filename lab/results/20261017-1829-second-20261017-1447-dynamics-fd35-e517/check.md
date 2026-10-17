Grade: gold

Abstract: Second author closed fd35's named experiment: the finality assert's firing is state-decided at certify time. Reproduced from the raw logs: 9/18 sweep fires, each preceded by PRE D = 16 = fin_hi − s0 (9/9) and armed A > 0 from publish 8–12 (leads 51–452 publishes); all 2,286 non-fatal clashes at m = 0; the sibling-closure field out= empty on all 2,295 RB events; regen 4/7 fires with identical invariants. Checker's own arms added 5 fires across two untested drivers/regimes (batch 4/9; vmax-8 late reclash, viol 48) — D = violation exact on every one, out= shut on 2,632 further RB events. Deletes the fix's window Monte Carlo: its gate is now a per-draw state read. Adoption is print-only, no engine line touched.

## Reasons

**Reproduction.** regen.sh exit 0 (runner); my independent re-analysis of `work/sweep` with `analyze2.py` regenerates every dossier number: 9/18 fires (s11/13/15/16 2-of-2, s14 1-of-2), P2 0 fails with measured leads 51–452 publishes (dossier 51–449), P3 9/9 with 18 fatal D = 16 lines (2 per fatal clash list), P4 `out=` 0/2,295 with mo = 0, P5 950 PRE at D = 0, D < 0 never, m ≠ 0 only on the 9 fires, P6 all 9 survivors armed (139–376 armed publishes). The raw fire log shows the exact sequence: `PRE ... D=Some((16, ...))` → `FIRE id s0 fin_hi` (the assert's own inputs) → `RB ... m=16 out=[]` → the unmodified assert panics ("rollback of region 308 from 32 would revise its published tick 48"). Print-only confirmed by patch reading: added lines are eprintln plus read-only scans (haz counter, PRE danger scan, RB out=/mo, hazard()); asserts and control flow untouched — only wall-clock timing shifts, which the dossier discloses as the race.

**Predictions.** predictions.md (18:33:44) precedes the sweep outputs (18:33:47–18:35:36, serial ~6 s/draw); one disclosed pilot (s11). All of P1–P6 held on the sweep draws, verified from the raw logs rather than the analyzer's weaker P2 check (I recomputed the armed lead per fire myself).

**Adversarial cases (mine; scratch logs removed, commands below).**
1. *Batch driver* (`finpol selfchurn batch 120 1800 128 600 2 s`, s ∈ {11,12,13,14,15,16,17,21,23}) — a driver this run never touched: 4 fires (s11/13/15/16), every one viol = 16 = fatal D, armed from publish ~20 with ~240-publish leads, `out=` shut, all non-fatal m = 0.
2. *vmax 8 frames* (next decade of the spread axis; s ∈ {11,15,16,21}): one fire at s0 = 1376 — the late-reclash class, outside the author's range — viol = 48 (three windows), PRE D = 48 = viol exact, armed lead > 314 publishes, `out=` shut.
3. *crossing family* (s 11,13,15,21,23): 0 fires; realized clashes all D = 0, m = 0, `out=` shut; armed survivors (115–311 armed publishes).
4. *window 32* (FINPOL_WINDOW=32, firing seeds ×3 tries): 0/9 fires (01e7's margin lead confirmed) but 114–116 PRE `D = 32` lines per draw without any fire; window 8 clean.
5. *Controls*: min_region 32 — rb = 0, never armed, no fire; seeds 21/23 outside 11–19 survive with the equality law intact.
Total: 5 further fires, all D = viol exact; ~2,632 further RB events, `out=` never opened (pooled with the author's and the runner's: > 8,000 RB events, zero opens).

**What the adversarial cases broke — two descriptive clauses, not the claim.** "Violations are always exactly one window" is a window-16/vmax-2 family descriptor (my vmax-8 fire: viol = 48), and "D > 0-without-fire never" is false at window 32 (armed D = 32 lines are common with zero fires — consistent with the run's own "armed ≠ incidence", but the equality-law row stated it without that bound). Both corrected in place on the page. The load-bearing directions — fire ⇒ fatal D = violation; realized non-fatal clash ⇒ m = 0; rollback's affected never leaves PRE's descendants closure — held on every draw of every family, driver, window and seed I ran.

**fd35's regen bugs genuinely fixed.** h_nosab SUM shows sab=None, rgn0=1, rb=0 with the armed episode regenerating (14–15 armed publishes to A = 128 in the window run, 13 in the runner's regen — schedule-moved); the churn arms rerun under the e517 patch keep the equality law (never armed, all m = 0, `out=` shut; rollback counts move with the wall clock exactly as the page says).

**Novelty.** docs/HISTORY.md holds no state-decision claim for this assert; the topic page (fd35's entry) names exactly this work as the open item — "one firing reproduction on the integrator's selfchurn harness to time the armed lead" and the PRE closure "asserted, not shown". e517 is the first to close both; fd35 itself had 0 fires, so this is not a repetition. The page stays open: this is the first gold on this specific current-best sentence (e704's gold is a different result).

**Goal fit.** Deletes a component: the window Monte Carlo that validating the engine-side fix would otherwise require (≥ 3 seeds × ≥ 2 replicates × 6 s per config, per config axis) is replaced by a per-draw state read ("armed ≤ 0 ∧ D ≤ 0 ∧ out = ∅"). PRINCIPLES 13: "basically we don't want errors that can compound" — the certificate reads the assert's exact inputs before it fires, so the abort becomes a guarded boundary. PRINCIPLES 34: "the oracles are guards, not shepherds" — D judges the boundary, it does not move it. The cost note is decision-relevant for direction 1: armed covers 85–99% of publishes on every draw (survivors included), so a hold-while-armed rule alone starves publication — the fix must pair with the disarm channel.

## What the author missed

- The sweep is one family, one driver, one window; the batch arms and one vmax-8 draw (each seconds cheap, already built into regen.sh's finpol) would have widened the domain — the checker had to run them, and they strengthen rather than weaken the claim.
- Two family descriptors were written as laws ("always exactly one window", "D > 0-without-fire never"); corrected on the page with the counter-evidence attached.
- Minor number slips, none load-bearing: armed share "89–99%" (measured 85–99% over all draws, 95–99% on survivors); the regen quote "`out=` 0/906" vs the runner's 0/852 and "1,123 further clashes" vs 1,101 — raced counts the dossier itself flags as schedule-moved, invariants identical.
- The 2-armed-truths-per-fatal-list structure is counted but not explained; the geometry derivation (why `alone_at` and `certify` pin the same contact tick) remains the missing soundness argument the fix should be written against — correctly named as open, and the right next run.

## Reproduce my checks

    B=$CARGO_TARGET_DIR/release/examples   # built by regen.sh from work/patch.diff
    $B/finpol selfchurn batch 120 1800 128 600 2 11   # fires; grep -E '^PRE|^FIRE|^RB' stderr
    $B/finpol selfchurn frames 120 6 128 600 8 15     # late-reclash fire, viol 48
    FINPOL_WINDOW=32 $B/finpol selfchurn frames 120 6 128 600 2 11   # armed D=32, no fire
    $B/finpol crossing frames 120 6 128 600 2 11      # survivor, invariants hold
