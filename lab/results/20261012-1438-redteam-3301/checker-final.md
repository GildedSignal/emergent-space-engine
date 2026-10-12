Working...
Check complete. `check.md` written; nothing else in the run folder touched; all reproduction and adversarial work ran in `/tmp/check-repro`. No git commands.

**Grade: gold.**

**What was verified:**
- **Reproduction:** `python3 falsifier.py` → metrics.json identical to the author's across all 20 scenes × 15 fields (0 diffs), 11.2 s; the 23.3° headline reconfirmed by my independent bisection truth and angle code.
- **Predictions:** mtime order clean (predictions 14:44 → falsifier 14:57 → metrics 14:59). P1/P2/P3/P5 held; P4/P6 missed and honestly reported.
- **Four adversarial cases:** (1) B0.99@3 converges at 36 iterations (deadline overrun), B0.995@10 genuinely diverges even at cap 64; (2) failures identical from TOL 1e-7 to 1e-3 — not a tolerance artifact; (3) the proposed bracketed fix verified at p99 5 / max 12 evals, zero error; (4) the first-sight cascade is killed by a 2-eval fixed-point acquisition seed — but mid-run slope-dip caps persist, so the core finding stands against the best seeding.
- **Documentary claims:** all citations verified verbatim (representation.md lines 32/57/78/116/129–130; law.md lines 20/35/49/53/67/70/88; H0210–H0213). `lab/rungs/` has no r5 and no r6; H0211 confirms the plane implements exactly the attacked line; H0213's only gather measurement was steady-state cache readouts. Novel against HISTORY and the gates.

**Gold rationale:** a written design premise the plane already implements is shown wrong on core game scenes, with a verified one-step adoptable fix — while uniqueness ("crosses once") survives, correctly narrowing the kill to the solver line.

**Flagged for the integrator:** the author's proposed r6 criterion "p99 ≤ 4" is unpassable by their own fix (measured p99 = 5) — freeze it at 5 or the rung VOIDs; and the dossier's "no self-healing" is contradicted by its own table (heals at frame 11).
