Working...
Check complete. `check.md` written to `lab/results/20261011-2132-spacex-91a0/` — **Grade: silver**.

**What held (reproduced on a clean tree, patch applied, all runs ≤ 9 s):**
- Every headline number verified against the author's raw rows and my own reruns: velocity plateau 21.4–21.9 bits/member (slope ≈ 0), state bits +2.0–2.4 per log₂ doubling, ship tubes 44.5→48 flat with all-distinct keys, contacts a transient, store 1183→6088–6400 B/body against a 6–13 B floor.
- The catalogue leak is real in code: `Catalogue::insert` (bind.rs:44) is a pure slot allocator with no (E,L) sharing; `release` fires only on rebind, so dead bodies never free slots. Growth matches cumulative ship spawns (+400 for 394 spawns).
- Novel: the prior directed run for this HANDOFF risk died "Grade: missing" with no dossier; no H-entry measures H_live.
- My adversarial cases all *support* the claim: 4× members (clamp raised locally, restored) adds only +0.4 bits/member; a doubled 4000 s horizon holds the plateau.

**Why silver, not gold:** two recorded numbers are contradicted by the run's own raw rows — "zero kicks fired in 2000 game-seconds" (actual: 5277–9160 per run, firing to the last seconds) and "ships peak 275" (rows and all six of my runs: 360–366). The physics conclusion actually strengthens (flat bits despite continuous kicks), but decision (3) as written would annotate law.md with a false number. The taste log's exact precedent: right physics, record the shipped rows can't regenerate. The gold fix is a 30-minute dossier edit re-derived from the existing JSONs, no new run needed.

One operational note: `/tmp/check-hlive` picked up files from a concurrent checker sharing this machine; I used only my own files, and the shared working tree briefly raced mid-check (content re-verified bit-identical to the author's patch afterward).
