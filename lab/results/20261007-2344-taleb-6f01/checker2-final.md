Working...
**Verdict written: `Grade: gold`** → `lab/results/20261007-2344-taleb-6f01/check2.md`

**Reproduction** — `work/patch.diff` empty; `cert.py` alone in a clean tree reproduces all three sweeps (pilot, wscan, escan) **bit-for-bit** (physics-identical; only wall-clock `seconds` differ). Every dossier table matches its JSON; both controls behave (aligned-gold 149 contacts / 0 miss / max rank 3; wide-belt 100% M-miss).

**Adversarial attacks (4, two on axes the author never measured):**
1. Fresh seed D=0.5: 73.0% vs 72.0% — ±5 pp holds, λ = 0.
2. Registered held-out k-formula: holds at k=2 (88.1 vs 91.6%), **fails at k=8 (43.4% vs 66.5%, 23 pp)** — conservative direction (over-predicts miss, so the S≲k gate errs to the cone tier, never silently drops); demotes the side-formula, not the claim.
3. Window-drift term (asserted, unmeasured): da=5e-4 aligned → S=6.75>4, λ-rank cracks at 16.1%, brute agrees — Δn·W confirmed.
4. Truth-finder independence where the certificate fails: the author's brute evidence covered only the aligned pilot and random subsamples are vacuous (0 contacts in 200 pairs); my directed non-adjacency attack (425 extra λ-close pairs) found **0 shadowed contacts** — instrument sound.

**Novelty/goal** — HISTORY.md through H0215 has nothing bounding the co-orbital certificate (the gold lives only in the taste log, unbounded); the gate lands in law.md's Binet representation and closes a silent 90%+ contact drop on the queued `b-coorbital-cert` build — principles 13, 4, 9, 24 all honored; 10⁶ arithmetic verified (2.51e-5 rad).

Missed by the author (named in check2.md): the k=8 deviation, the vacuous brute design, mirror-tuple inflation of `contact_pairs` (143 tuples vs 75 unordered pairs — fractions unbiased), the by-construction phase-density field, and the unreported wide-belt λ prediction miss (50% vs ~97%).
