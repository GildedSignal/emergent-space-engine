Working...
Check complete — `check2.md` written, **Grade: gold**.

**What I did** (clean tree, `work/patch.diff` applied by me, private target dir, removed after):

- **Reproduced**: runner's regen + my own flights agree. Cure 1e5: max 14.4 ms, over 4, mega-frames 0 vs disease 796.7 ms, over 56, mega 11 — the disease's worst frame is exactly cc9d's signature (one player item `[0,0,0,1,0]`, 16,058 nested kicks, 697.6 ms of `item: kick (clock)`).
- **Mechanism verified in source**: the cure streams exactly `pull_ships`' set and order through the same `resolve_entity → resolve_body → requeue` path under the same class-2 budget gate; `digest()` hashes every doll and every body's full trajectory, so "bit-identical" is a full canonical-state identity.
- **Three adversarial arms**: N=4e5 (outside the author's grid) holds at 16.1 ms / 0 mega / 1,432 MB — flat in N where the killed K-law predicts seconds; a 3.3× deeper cut keeps the digest identical (`8835b2b6…`, off/on/naive/ref); rtf 3000 shows the honest boundary (no gulp, but p99 35.3 ms — the wall moves to drain throughput, as the dossier itself predicts).
- **Hygiene exact**: patch applied and shipped tree both 8 passed / 2 failed on the same two `step::tests`.
- **Novelty**: cc9d named this experiment; no cure anywhere in wiki/docs. Page fold-in faithful — no correction needed.

Gold because: reproduced three independent times, pre-registered predictions held (P4's miss pre-written as a reportable branch and disclosed up front), the collapse is 2 orders of magnitude and deletes the K-law term at every rung flown plus the one beyond it, and adoption is one step (default the flag, gate `input()`, re-freeze the corpus). The naive-control weakness is the test's, not the cure's, and the author said so before I found it holds at depth too.
