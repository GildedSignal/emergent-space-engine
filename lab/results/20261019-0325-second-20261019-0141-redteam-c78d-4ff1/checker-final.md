Working...
Grade: **gold** — `check.md` written; the author's wiki page corrected in place (one domain condition + a Checker3 block).

**What I did and found:**

1. **Reproduced everything exactly.** Clean tree, empty patch, rung hash verified. All four decisive configs bit-identical to `metrics.json` (26.4 s vs the author's 27 s); my own bisection-path rerun (2 m 40 s) bit-identical to `metrics-check.json`; diagnostics identical; `verdict.py` on my own files → PASS (negative fails 3 bars by 16×/16×/5.8×, positive passes — no VOID/DISPUTED reachable); c78d's base record byte-identical under my own rerun.
2. **Freeze verified:** mtime order rung → hash → predictions → dossier; every frozen-case prediction held (the two misses are diagnostics-scale, disclosed, and one is against the author's own kill expectation — the signature of genuine pre-registration). One caveat noted: `run.log` empty and the instrument's last edit postdates predictions by 6 min.
3. **Doppler typo confirmed in c78d's source** (`cosang` is already v·n̂, then β-multiplied again); the correction is exact SR and moves minima 0.535→0.5227, 0.815→0.7999 as claimed.
4. **Four adversarial arms (fresh seeds):** β 0.99 extends the cure (p99 0.024/0.017, zero false blink); grazing impact 2.8 passes (p99 0.015); **density is the missing axis** — a Gaussian-core fleet breaks the uniform-weight pixel readout at p99 0.21–0.23 (4–5× past the bar), two-clump 0.14/0.36 — page overstated the license, now corrected; sub-planet R_f = 0.5·R_p measures the min(N, pixels) crossover (~80 pixels ≈ N) as the domain line claims.
5. **Novelty:** lab/rungs/ holds r1–r10 only; this is checker2 of c78d's named gold experiment, executed with both its freeze fixes implemented and validated (ratio 0.998–1.000 to R_f = 30·R_p).

Gold stands if the second blind checker agrees; adoption is one commit (`lab/rungs/r11-eclipse-aggregate.md`) plus the page's density clause.
