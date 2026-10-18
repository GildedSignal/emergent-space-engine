Grade: gold

**Abstract.** Claim: the u64 `first_hit` port named unpriced by encounters od 1 is a trap — "all section values < 2⁶³" holds yet does not suffice; the naive port returns wrong dues (166–215/100,000 on the shipped belt class; 41% at a=30 AU in my check), and the exact sound form (u64 recursion, u128 compose) wins only 1.42–1.60×, killed by its own pre-registered <2× rule. I reproduced everything bit-exactly from `regen.sh` in a clean tree (census 0/400,000; mismatches 166/180/215/206; sound 0; depths p50 4/2, max 11/7; win 1.59/1.58/1.42/1.42 vs 1.60/1.58/1.42/1.42). Gain: closes the named next lever on the encounter-work bottleneck and prevents a silently-corrupting port from shipping. Cost to adopt: one design-note decision; the sound-port recipe is banked exact.

**Reasons.**

1. **Reproduction.** Clean tree, `git apply work/patch.diff`, `regen.sh` exit 0. Deterministic parts bit-exact against `run-output.txt` (above). Timings within shared-box noise; my u128 p50s (194/196/120/122 ns) sit between the author's (192/193/108/110) and the runner's (213/215/121/123); ratios agree to ≤0.01×. The shipped `dioph` tests pass 2/2 (`regen.log`'s `tail -3` only showed empty trailing test binaries — the claim stands).

2. **Predictions.** `predictions.md` (mtime 22:00) precedes the decisive `run-output.txt` (22:05). The operative pre-registrations held: the soundness census on untuned arms (0/400,000 < 2⁶³) and P5's kill rule, which fired against the author's own 3–8× expectation. P2 (depth) and P3 (price) were falsified and reported as falsified — pre-registration working, not a defect; no number in the claim rests on a failed prediction.

3. **Adversarial cases (mine, one outside the author's range).**
   - *Keyed belts (keys=8, keys=2; author tested keys=0):* trap does not fire (0 mismatches — same-key pairs exit at d=0, cross-key d is structured), sound form exact, win 1.43–1.50×. Depth p50 1–2.
   - *Decade shifts in a:* a=1 AU (m≈2³⁴·⁶): naive wrong on 0.008%, win 1.64×; **a=30 AU (m≈2⁴²): naive wrong on 41.0% of 100,000 calls**, sound form exact (0 mismatches, identical steps), win 1.73×. Outside the author's tested range; the trap is a cliff in a, not a belt curiosity.
   - *Worst-case continued fraction at belt-scale m* (Fibonacci pair, m≈2³⁷·⁷, depth 30 vs ≤11 measured on real arms): win 1.71× — the <2× kill survives the strongest depth attack at belt scale. (Wins >2× exist only at m ≲ 2³² with forced depth — no belt class lives there; natural a=1 arm at 2³⁴·⁶ wins 1.64×.)
   - *Mechanism dissected:* every naive-vs-sound divergence I instrumented is exactly the compose product m·y wrapping u64 (observed products 2⁶⁵·¹ and 2⁶⁶·⁵). The port is verbatim `dioph::min_k`; the tuple collector matches `tier::arm_pair`'s own lines.

4. **Novelty.** e87d's page names this the "next constant lever, named and unpriced"; no HISTORY entry or wiki page prices it. Not a repetition.

5. **Page.** Faithful: the current-best block, the Refuted entry and the Runs entry match the reproduced evidence (I corrected one truncated Runs line in place). Not three-golds-agreeing; topic stays open.

6. **Goal fit.** Closes the named next lever of board bottleneck #2 (encounter work at 10⁹) and refutes a premise on the certificate path: had the next run wired the port from od 1's parenthetical, silently wrong dues would have entered the encounter certificates. PRINCIPLES: "Certificates need independent, adversarial checks"; P13 — a wrapping port breaks exactness where "exact means deterministic and reproducible". Same shape as gold `components-4643` (a named lever killed, nothing to build), plus a refuted premise that one carries.

**Defects found (noted; none load-bearing).** The dossier's threshold arithmetic is off: 2⁶⁴/m at m≈1.4×10¹¹ is ≈1.3×10⁸, not "≈1.3×10¹⁰" — the true port is *more* fragile than stated (consistent with my 41% at a=30). Also m²≈2⁷⁴·¹ not 2⁷⁴·⁴, and the gap to 2⁶³ is ~1.6×10⁵ in a (6.6×10⁷ in pi), not "~10⁷ in a". The measurements, which decide the claim, are exact.

**What the author missed.**
- The corruption rate's steep growth with a (0.2% at 3 AU → 41% at 30 AU): the trap warning deserves to be scoped "any class with pi ≳ 10¹²", not just the belt.
- Whether a wrong k also flips the armed/silent decision at the horizon (`l ≤ lmax`), not merely the due — unmeasured; wrong dues alone already corrupt least-slack order.
- Keys>0 belts were untested by the author; they turn out trap-free, which strengthens the census but for a structural reason (d=0 exits) the page could record.
