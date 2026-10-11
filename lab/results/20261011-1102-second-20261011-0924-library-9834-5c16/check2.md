Grade: gold

**Abstract.** The second author ran the first checker's named gold experiment: the original's
three-number rotation record (claimed 33–146× over scanning) under real kicks at the plane's
rate. Reproduced bit-for-bit (7/7 configs, 0 field diffs, ~155 s, <200 MB): the retrigger
quantum tracks ρ/eps, amortized as-stated work is 0.010–0.89× scanning in every kicked config
(a 1.1–96× loss), and the frozen control never breaks. Two verified defects in the original:
`kepler()` never rotates by ϖ (code-read confirmed; error O(a·e)=0.08 vs R=2e-3), and the
33–146× counted phase tests while its window cost a 49k-eval scan (frozen honest accounting:
5.2×, reproduced). Cost to adopt: negative — drop the record from the encounters design. My
correction: the surviving ψ direction's "18–24×" collapses to 3.6–4.4× when core-band false
alarms are charged the verification any real system must pay.

**Reasons.**
1. **Reproduction.** `python3 probe2.py A B C D E F G` in a clean copy: every aggregate and
   per-pair field in the author's `results2.json` matches my run exactly (0 diffs excluding
   wall time). Dossier table verified: skin retriggers 12.9/254.8/581.8 intervals at
   ρ=1e-4/2e-3/5e-3; phase quanta 13.0/263.2/449.2; as-stated 0.049/0.89/0.74/0.099/0.010;
   B as-stated 43,059 evals/encounter vs scan 38,315; E 3.97M vs 41,349 (96×); G frozen
   never retriggers (1369), honest 5.2×. Reversal fraction 97–100% ("94–100%" held).
2. **Predictions.** `predictions.md` (mtime 30 min) precedes probe2.py (24 min) and dossier
   (19 min); P1 and P4 failures are disclosed, and the claim rests on P2/P5/P6, which held.
   P5 re-verified adversarially at eps=1e-7 (my J: skin 143 vs ρ/eps prediction 129, within
   its 2× tolerance; inversion 0.54). Honest reporting of failed predictions is itself
   evidence the pre-registration was real.
3. **Attack (five cases of my own).** (a) Two independent runs bit-identical. (b) H —
   circular belt, Δa∈[0.01,0.05], strictly non-reversal: zero hits exist; the non-reversal
   corner is structurally hit-starved, confirming the author's "too thin to certify".
   (c) K — circular belt, Δa∈[0.0008,0.0039], non-reversal **with** 15,965 hits: ψ misses
   zero, false alarms 1.2% of intervals, 14× — the failure boundary is the reversal
   condition, not the kicks; slightly stronger than the author's own demotion. (d) I —
   e≤0.3: reversal failure extends (93/135 hits missed). (e) J — the one hit at eps=1e-7 sat
   on a non-reversal pair and was missed (n=1; a wrinkle on ψ's valid regime, not on the
   inversion).
4. **My accounting correction (the one real defect).** `psi_evals` charges a (S+3)-eval
   verification only to pad-band arrivals; flagged-but-not-hit intervals inside the tight
   arcs ride free. False alarms are 7–27% of intervals; charging them the same verification
   gives scan/ψ = 11.8 (A), 4.4 (B), 3.6 (C), 4.2 (D), 4.4 (E), 3.2 (F), 3.7 (G) — not
   18–24×. This is the same unit-artifact class the author convicted the original of,
   applied to the secondary quantity; the dossier states the FA rates and the 0.1-eval/arith
   sensitivity (I reproduce 4.7–6.9× there) but keeps the 18–23× in the claim sentence.
   Since the author already demotes ψ to "a lead, not an adoptable certificate", this does
   not rescue the original nor change the verdict.
5. **Novelty.** No H entry or doc covers the rotation record under kicks, the
   equation-of-center reversal regime, or conjunction-longitude certificates (searched
   HISTORY for skin/certificate/conjunction/rotation/reversal; nearest are the 6 Oct
   slack-skin gold and r8 v2/v3). The original 0924 run pre-registered the risk ("if it
   exceeds the return times the win inverts"); this run performs the measurement, and finds
   two further defects the first checker's verification shared a harness with.
6. **Goal fit.** Board's top scaling risk (candidate work must track real encounters).
   Shows a premise wrong — PRINCIPLES 9 ("A failed experiment kills that configuration,
   never the method") and 19 ("a fix signals the wrong representation": the θ-window was
   the wrong variable; the slack belongs in conjunction-longitude units, and even those go
   2D at belt e). Adoptable within one step: the integrator drops the three-number record;
   the ψ direction is mapped with its regime boundary measured, not adopted.

**What the author missed.** (1) The free-core-band accounting above: the honest ψ win at
plane configs is ~4×, not 16–24× — worth stating because ψ's survival is the run's
constructive output. (2) The cheap decisive test they proposed and did not run: my K shows
ψ is exactly zero-miss in the non-reversal regime with hits — the certificate is sound
precisely where the belt has almost no pairs, so the design question is a belt-e-scaled
wobble fat-arc, which their "what would make it wrong" already gestures at. (3) e/ϖ kicks
(Binet V,W drift) untested — stated. (4) run.log is empty; pre-registration rests on mtimes
and the disclosed failures, which I accept.
