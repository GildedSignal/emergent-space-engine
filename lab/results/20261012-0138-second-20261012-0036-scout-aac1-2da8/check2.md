Grade: silver

**Abstract.** Claim: the checker's named experiment (census vs window 60→600, angle-based libration classifier, second potential P2/A2) upgrades the galaxy-doll kill to a design number — sustained churn switches on between eps_eff = eps·A(r_CR) ≈ 0.008 (0–0.5%) and ≈ 0.025 (27–35%), band pattern-locked to the bar envelope; the 60-period census is unreliable both ways. Reproduced: both 60p populations regenerate **bit-identically** from shipped code; every dossier number re-derived independently from the stored JSONs; probe-orig.json md5-verified byte-copy. My attacks strengthen it: seed 9999 (32.5%/0.0%), held-out eps=0.02 cell (eps_eff 0.0165 → 10.0%, monotone), eps=0 control (0 walkers, max dL 2×10⁻⁹). But I found a sign error in probe2.py's d2phi: the shipped OLR (3.744; true 3.579) is wrong, so "correction (c)" wrongly rejects the original's correct 3.57, and circular rows' OmR is ~16% off. Cost to adopt: one-line fix + rerun (classes immune: 1/209 changes) + one third potential.

**Reproduction.**
- `python3 drive.py regen-p1-s03 / regen-p2-s03` (shipped probe2.py, exact stored seeds): 209/209 classifier dicts identical per population, E0/L0/Tr identical. The original run's "results the shipped code cannot regenerate" defect is fixed.
- `python3 analyze.py` reproduces every dossier number from the stored JSONs; I recounted classes independently (not via analyze.py): P1 e03 600p walk 0.349, lib 0.053, median walker dL 0.530, bins 5/15/26/53%, P1 e10 0.665, P2 e03 0.000 at 600p (9.1% at 60p on the short file) — all match.
- data/probe-orig.json: md5 `36f78247…` equals `git show origin/claude/lab-20261012-0036-scout-aac1:…/data/probe.json` — byte-copy verified.
- Part A corrections (a), (b), (d), (e) verified against that record: walker bins 8/42/51%, H2 band [1.8,2.8), eval 384× per period (23038× per 60-period block; compile 687×), nfail=19 = the de=0 double roots.
- nfail=0 in all 11 populations and in all 7 of my fresh runs.

**Predictions.** Content pre-registered: the classifier spec in predictions.md matches the shipped code line for line (k* rounding, R̄≥0.5, dL>5% via decile medians, window prefixes). W1, W2, W5, W6 held; W3 failed and the failure is correctly carried as the mechanism (band tracks eps·A(r), not corotation); W4 honestly reported censored with the sub-threshold super-linear growth. Caveat: the claimed file-time proof (01:41:57) is not verifiable — appending outcomes (02:27) destroyed the mtime — but the first data is 01:49 and the failed-prediction content is genuine. Process defect from the original run is substantially fixed.

**Adversarial cases (mine).**
1. *Zero-bar control* (eps=0, 60p): 0 walkers, max dL 2.0×10⁻⁹ — the walker class cannot be classifier or integrator noise.
2. *Seed sensitivity* (seed 9999, full 600p): P1 e03 walk600 32.5% (vs 34.9%), median walker dL 72.5%; P2 e03 walk600 0.0% again. Both headline numbers seed-stable.
3. *Held-out intermediate cell* (P1 eps=0.02 → eps_eff 0.0165, never run by the author): walk600 10.0%, band [1.97, 3.8] — monotone between 0.5% (0.008) and 34.9% (0.025). The switch-on bracket is confirmed on a cell the ladder lacked.
4. *Threshold sweep* dL ∈ {2,5,10}%: P1 e03 38/35/33%, P2 e03 2/0/0%, P2 e10 33/27/23% — structure threshold-robust as claimed.
5. **The d2phi sign error.** Line 22: `GM*(2*r*r - B*B)/…` should be `GM*(B*B - 2*r*r)/…` (second derivative of −GM/√(r²+B²)). Independent brentq and a corrected rerun agree: P1 OLR = **3.579** (shipped 3.744), two ILRs at 0.099/0.679 (shipped 0.170), P2 OLR = 3.691 (shipped 3.928); corotation radii unaffected. Impact quantified by rerunning the headline population with the fix: walk600 74/209 vs 73/209, lib 11/209 identical, 1/209 orbit changes class (a de=0 row at the dL threshold). The census and design number are immune (walk is dL-driven; all librators are k*=0, so their R̄ never uses OmR_m; eccentric rows compile OmR by quadrature, which does not touch d2phi). Not immune: the resonance table, the band-edge label "[CR−0.6, OLR+0.06]" (true edge: OLR+0.22), the circular rows' OmR0 (median 16%, max 28% error — W5's nfail=0 still holds with the correct κ²), and dossier correction (c), which is itself wrong: the original dossier's 3.57 was correct.

**Novelty.** HISTORY ends at H0215; no prior entry covers bar-driven migration, galaxy-scale dolls, or churn censuses. This is the faithful execution of the original run's named experiment (its check.md asks exactly this), not a duplicate. The angle classifier, the sustained-band-vs-envelope lock, and the eps_eff ladder are new.

**Goal fit.** Board: "fitting 10⁹ in 8 GB" / cost-at-a-billion. The census is the surprise-rate measurement that sizes the doll's re-anchor tier — PRINCIPLES 3 ("Compute only surprises"), 33 ("each scale resolves only what matters at that scale; eps·A(r) is that significance, measured"). Floats only; nothing canonical touched.

**The one experiment for gold.** Apply the one-line d2phi fix, regenerate the resonance table and the census (expected: walk fractions unchanged, per my fix-run), and add one third potential with an intermediate eps_eff cell to separate the threshold from the resonance-density change — the author's own named gap, which my eps=0.02 run only half covers (same potential). Republish with the corrected OLR (restoring the original's 3.57).

**What the author missed.**
- The d2phi sign flip, and the meta-failure inside it: "correcting" the original's correct 3.57 to 3.744 by trusting one's own unverified helper — the exact publish-without-checking failure this second run existed to repair. A numerical second difference or SymPy check would have caught it.
- W5's closed form ships wrong OmR on every de=0 row (κ² inflated by 2GM(2r²−B²)/(r²+B²)^2.5); "nfail=0" is true but the compiled frequencies are not.
- "File times prove ordering" overstates: the outcomes-append destroyed the mtime; only content-based evidence remains.
- Trivial: "after the first eight populations" — nine data files (01:49–02:04) predate the 02:06 edit.
