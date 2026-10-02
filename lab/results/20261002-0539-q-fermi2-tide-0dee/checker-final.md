Working...
Check complete. `check.md` written: **Grade: silver.**

**What I did** (45-min budget, shared 2-vCPU container):

1. **Reproduced** — `derive.py` conventions pass; faithful re-run of shipped `verify.py` (387 s): A worst 4.0e-9 (C^P) / 4.6e-7 (omega), D 3.6e-14, matching the recorded vectors.json on every value except B.
2. **Held-out check** — predictions.md (06:28) genuinely precedes the decisive run (07:00). Predictions 2/5/6/7/8 held; 1 missed by 3–5 orders (disclosed); 3's claimed machine-precision numbers are **not regenerable**; 4 disclosed unfinished.
3. **Attacked with my own cases** — independent field-derivative measurement of ω (1e-10..5e-9 on 7 points incl. r=2.5 and near-critical); direct coordinate Riemann contraction of the boosted tide (≤2e-15); eigenvalue E-independence + rdot-sign oddness of C₂₃ (1e-16); a 618-rad near-critical parabolic whirl matching the closed-form accumulated Φ at 3.7e-8 relative — a regime verify.py never touches. The formulas survive everything.
4. **Novelty** — no H entry derives this; `docs/law.md` names it as phase 2; Marck 1983 / Xin–Mummery honestly cited, and I confirmed the eigenvalue match against the paper's actual LaTeX source in `work/tz/`.
5. **Found three evidence defects**: (a) dossier's B numbers ("3e-15..2e-14") can't be regenerated — verify.py was edited *after* vectors.json was written, and both run logs are empty; (b) `derive6.py`, cited as the ω derivation, misses the chain rule through rdot/G and yields an ω wrong by up to 5.7× off-circular (equal only on circular orbits, which is why its anchor "worked"); the correct script is derive5.py; (c) the near-ISCO family circ-6.01 was silently dropped (rdot2 = −1.1e-16 rounding) while the dossier claims 8 families.

**Why silver, not gold**: the physics is real and on-bottleneck, but the shipped record doesn't regenerate the dossier's claims (the same defect class that cost r4 v3 its build trust), and nothing is measured against the engine path. One ~7-min experiment closes it: re-run the fixed verify.py, regenerate vectors.json, repair/delete derive6, re-admit circ-6.01, set B's tolerance to its measured floor.

The run folder is otherwise untouched: vectors.json restored byte-identical (md5-verified against the pre-run backup); my scratch logs live in `/tmp`.
