Working...
Check complete. `check.md` written to the run folder (nothing else touched, no git commands run).

**Grade: silver** — with one important falsification found in the attack.

**What I did:**
- **Verified the record**: every dossier table cell matches its JSON (`summ.py` on all 11 reports); empty `patch.diff`, clean tree, shipped dashboard code (`dash.rs`, `universe/mod.rs`) — all numbers regenerate from the shipped binary.
- **Reproduced 4 cells** (r100, b10, b15, m400) + 2 adversarial (repeat, unpaced) at load 1.4–3.0 vs the author's 0.3.
- **Pre-registration held**: `predictions.md` (9 min old) predates all grid JSONs (3–8 min) and postdates only the disclosed smoke run.

**What reproduced**: readout dominance (gather share 0.61–0.69 everywhere), members→gather scaling, the budget's soft edge (engine max > budget in every run), b15 tail ≥ b10 tail.

**What didn't**: "5 ms 2× too small at 100×" (my runs: 3 overflow frames, low1 = 100), the 540 hitches/hr at b15 (0 hitches, worst 16.0), m400 magnitudes (inverted: 31 hitches, engine max 109 ms = 22× the 5 ms budget).

**The falsification**: identical commands, byte-identical input histories (logged=taken decisions, same ticks, same cut 406050894, seed 1, threads=1) produce **two different canonical digests** (`6ce636fa…` ×6 runs, `56f49416…` ×3), differing by ~2,000 events. That kills the shipped `digest_note` contract, H0213's "one digest over any budget", and the run's claim 5 / P6 — the author's four agreeing runs were one attractor, not proof. Suspect: the wall-derived per-frame target in `frame_to` plus the deferred-work loop changing event *content*. That's an integrator-level engine bug against PRINCIPLES' first law.

**Gold path named**: pin machine state + ≥3 seeds for the frontier, after bisecting the digest flip — the bisect may itself be the gold.
