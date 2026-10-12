Working...
Check complete. `check.md` written to the run folder; nothing else in `lab/results/20261012-1438-…/` was touched (all reproduction and probes ran in a `/tmp` scratch copy, since removed).

**Grade: silver.**

**What held (reproduced bit-for-bit, all four dossier commands, 236 s total):**
- Record regeneration exact (npz `array_equal`, summary differs only in tag/wall_s); decisive T=3·10⁴ run deterministic — fresh `counts` and ladder identical.
- Ladder 33→8→4→1 chaotic; departed class 75 (1.83%, empty 24–35 gap, 10.6× D<1 enrichment); retained cross-val 8087/8243 (98%), 91% exact, ρ=0.82; gross:net 203:1; forced 0.76 bits/body; every item-7 record correction verified.
- `shelf.rs:8-10,819-821` confirms the cited engine semantics (events→hot tier, compact seals exact deltas, reabsorption at base).

**My five adversarial findings:**
1. **A=0 control: the departed class vanishes** (0 bodies ≥30 bits) — it is drive-created, so the "birth-quantum separatrix ambiguity" mechanism sentence is incomplete and the 1.8% has an unmeasured drive dependence.
2. Seed 777 replicates the split (departed 1.66%, forced 0.69 bits/body, 224:1).
3. 8× finer scar scan moves traffic only 1.05× — the 203:1 is not a cadence artifact.
4. **Persistence baseline**: `floor(b_half/b*)` alone scores 87% exact, ρ=0.70 — the cross-validation is persistence-dominated; the log-fit adds ~4 pts. "Memory predicted" is weaker than the headline reads.
5. All 75 departures complete by t≈2117 (median 66 periods): the "feeding per decade" worry is gate relabeling — forced memory does *not* accumulate, a stronger claim the author left unclaimed.

**Why not gold:** the pre-registered S4 failed by its own kill criterion and the passing variant is post-hoc and persistence-dominated; the departed fraction is measured at one drive. **The one experiment:** a pre-registered drive ladder (A ∈ {0, 0.01, 0.05, 0.15}, two seeds) with the persistence baseline beside every cross-validation number. Plus two record slips to fix ("98.0% from shear" is 90.3% of crossings / 98.2% of bodies; "up−dn = 1 per level" witnessed at one threshold only).
