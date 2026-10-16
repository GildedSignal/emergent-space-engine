Grade: silver

The allocator's rollback escalation (`escalation *= 2`, alloc.rs:1410) is a verified one-way global ratchet: Newtonian conflicts fire at ignition then self-quench, and the latch holds frozen through 80,000 chronons (2.35× the author's horizon) while outcome digests stay bit-identical across arms (every run, both horizons). Novel — no wiki page or H entry measures rollback/AIMD dynamics. But the headline tax is overstated: the 77–90 vs 1–2 avoided-merge contrast is law-confounded (the decay arm at escalation 1.0 on the same Newtonian scene still pays ~54/stage; ratchet-attributable ≈ ×1.5), and my flight of the author's own named next experiment (frames harness, 60 Hz, rates 15k/30k) shows no shipped-vs-decay deadline-miss separation at 44 bodies. Adoption: 10 lines, default-off, digest-safe; value is hygiene until a frames/bigger-scale tax is measured.

## Reasons

**Reproduced (regen.sh exit 0, plus my own runs):**
- Mechanism verified in shipped code: `escalation *= 2.0` (alloc.rs:1410), initialized 1.0 (1851), consumed only by `speed_factor` = `margin·sab·E + (E−1)` (544) — never reduced anywhere. No decay exists. ✓
- Newtonian battery: conflicts at ignition only, then zero rollbacks forever; escalation frozen at a power of 2 through stage 17 **and my 40-stage run (80k chronons)**. ✓
- Digest invariance: shipped / ES_DECAY=1 / ES_DECAY=0 arms bit-identical (`964ee2e0…`/`74db660c…` at 17 stages; `aa59960d…` at 40 stages, both arms). The certificate moves scheduling, never results. ✓
- Decay arm: escalation back at 1.0 by stage 2, conflicts still fire when real. ✓
- Predictions: P1, P3, P4, P5 held; P2 half-held (latch yes; the author reported no region collapse, P6 honestly replaced). predictions.md predates the patch and the runs (file order in the folder). ✓
- Novelty: grep over `lab/wiki/` (31 pages) and docs/HISTORY.md finds the mechanism's *existence* (H2443 "rollback scoped to conflicting lineages", H2541 AIMD strides) but no measurement of its dynamics. First measurement. ✓
- Instrument: public API only (`run_to`/`Report`/`outcome`), ES_DECAY default-off. ✓

**Adversarial cases (mine):**
1. **Determinism (3 identical shipped runs):** the latch exponent is a sample from a nondeterministic process — stage-1 rollbacks 1/1/2, frozen escalation 2.0/2.0/4.0, late regions 33/33/9, late avoided 47/47/81; digests identical every time. The fix phase saw 4 rollbacks → ×16. The dossier headline "measured frozen at ×4 after two conflicts" presents one sample as the fact; it survives as "frozen at 2^k forever".
2. **Sub-stride relativistic geometry (the author's flagged-untested regime):** cells 200 units apart, targets 100 units from the cannon path — **zero rollbacks, escalation 1.000 throughout**. The relativistic quench holds even inside the one-stride window; no geometry under `Law::Relativistic` latches the ratchet at all yet.
3. **The frames harness (the author's own named next experiment, not flown by them):** 60 Hz, 1 s, rates 15k/30k chronons/s, 3 reps per arm — deadline misses shipped [1,1,1]/[5,8,1] vs decay [1,1,1]/[7,1,1]; acceleration drops [1,1,1]/[3,5,1] vs [1,1,1]/[4,1,1]. Noise-dominated, **no measurable tax where the player feels it** at 44 bodies.

**Why silver, not gold:**
- The permanent-tax magnitude — the dossier's cost claim — is overstated by a law/scene confound: on the *same* Newtonian scene the decay arm (escalation 1.0) still pays ~54 avoided/stage vs ~72–85 latched, so the ratchet-attributable tax is ~×1.5, not the ~×50 implied by "77–90 vs 1–2" (that baseline changes the law too; my zero-conflict relativistic close scene pays 28–105/stage while settling). My frames flight then finds no player-visible cost at all. The mechanism finding stands; the priced cost does not.
- The dossier and the proposed page state the latch exponent ("frozen at 4.0", "2 rollbacks at ignition", "4→32 regions") without the nondeterminism disclosure that fix-final.md itself carries. In one of my runs the partition sat at 9 regions for ~6 stages — the author's own P2 "collapse toward few" sometimes manifests, so even the re-fine claim is one sample.
- The decay arm's own cost is unpriced in the dossier: re-opening the conflict window refires conflicts (regen: 6 rollbacks / 10,832 wasted ops at stage 1 vs 2 / 5,656 shipped) — the mirror trades rollbacks for margin, worth stating before adoption.

**The one experiment to gold:** a tax that survives its surface — frames-mode (or ≥10⁴-body batch) comparison, latched vs decayed, over enough reps to beat the run-to-run noise, on a scene where the relativistic law actually fires conflicts (or the honest conclusion that the tax is nil and the fix is pure hygiene — also adoptable, also publishable). Pair it with per-region escalation, since the global halving mirrors the global doubling's wrong locality.

**What the author missed:** the nondeterminism (their fix phase caught it but the dossier and page were not updated); the same-scene decay baseline that deflates the tax by ~30×; the frames flight they named as decisive; the decay arm's rollback cost; and that no relativistic geometry tried — including my closest — ever latches the ratchet, which makes the shipped-vs-decay question moot for every scene measured so far.

Page corrected in place where it overstated (latch exponent, tax magnitude, added the frames result and the decay arm's cost); see `wiki/allocator-ratchet.md`.
