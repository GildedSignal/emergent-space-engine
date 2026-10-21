Working...
Check complete. **Verdict: silver** — written to `lab/results/20261021-1655-redteam-1ae8/check.md`.

**What held (reproduced independently):**
- Fresh rerun of `peters.py` is bit-identical (`peters_out.json`, same md5); every dossier number matches the log row by row.
- My closed-form circular oracle (no RK4 anywhere) reproduces every circular headline to 3 digits: +8.80/+3.97/+1.55/+0.44/+0.23/+0.08/+0.01% at ν = 0.25. The kill at the doll's licensed edge is oracle-exact.
- Rung gap verified: no inspiral/GW arm in any of the 14 rung files.
- Adversarial arms *strengthened* the kill: at e₀ = 0.99 the error is −26.4% at 65M, catastrophic at 30M (Δa/a = 25, p_end = −2897M), and −1.6% even at 200M — the far-field survival is circular-only. Sub-cycling doesn't rescue the kick: 32 kicks/cycle still −1.8% at the worst cell.

**Why silver, not gold:**
1. **Physics error:** "ν = 0.5 (equal mass, unlicensed by 97b0)" is wrong twice — ν = m₁m₂/M² ≤ 0.25 with equality *at* equal mass, and 97b0 swept ν ∈ {0.01, 0.1, 0.25}, the whole physical range. Attack #2 (the license hole) collapses; the central kill survives on the ν = 0.25 (= equal mass) rows.
2. **Arithmetic slip:** the 0.1% license bar is p̄₀ ≈ 91M, not the dossier's 230M (that's the 0.01% bar), and 230M is not regenerable from the run's code.
3. **Novelty:** the conclusion is already on record — `law.md:36` (adopted 12 Oct): "Inspiral is not a jet: Peters' a(t) is its generator", plus df81's gold line. New here is the sampling-channel isolation (exact rates + exact recompile per cycle still fails — the escape the jet retirement left open), the |Δt/t| ≈ 3.9·q₀ law, the typed r17-inspiral bars.

**Gold-making experiment:** measure the cure (Peters generator, pericentre-refined) against the same oracle over the plane extended to e₀ 0.99, freeze r17, fix the bar arithmetic — one run.

I corrected the proposed wiki page in place (ν label, ν-domain of the quantum, 230M→91M, e 0.99/sub-cycle arms, law.md context); budgets hold (131 lines, current best 13). My adversarial evidence lives in `checker_adversarial.py`/`.log` in the run folder; nothing else touched.
