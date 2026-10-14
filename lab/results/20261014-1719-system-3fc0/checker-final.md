Working...
Check complete. `check.md` written, the author's page corrected in place, tree restored to pristine (`git status` back to `?? lab/results/` only), nothing committed or pushed.

**Grade: lead** — the central claim does not reproduce.

**What I did**
- Applied `work/patch.diff` to a clean tree, rebuilt (11 s), re-ran the decisive arms plus seven adversarial flights of my own (2×10⁴ at `ES_PULL_MAX`=256/64/forced-scan, pristine pairs at 5×10⁴ and 10⁵, and a P1 digest-identity attempt at cut 230 game-s).
- Verified every code citation in the dossier against shipped code (`pull_ships` at universe.rs:690-700/770, the 762-768 invariant, held scan at 1163-1165, `encounter.rs:162-198`, `body.rs:152-161`) — all accurate.

**What the evidence shows**
- The headline ("bounded pull freezes the horizon at tick 55 within 1,200 frames at 2×10⁴, pristine advances") is contradicted by the runner's own regen **and** two independent re-runs: the bounded arm advances on pristine's exact trajectory (now=1,048,715 @f1200 → 50×10⁶ ticks @f~15,000), pulls *ahead* post-burn (809M vs 336M ticks @f21,600), and cuts the worst frame ~12× (294.8 vs 3,439.9 ms). The dossier's numbers are absent from the `wave_runs.txt` its own `regen.sh` produced — the lab's most-recorded failure mode.
- The freeze is an artifact: all arms (pristine included) sit at now=55 at frame 600 — the pre-burn unlock — and the reported dissociation is which arm crossed the 600-frame stall threshold first under load. Shipped `rekey` (universe.rs:623-628) promotes due ships from `waiting` into the frame's budgeted queue with no pull, answering the author's liveness hypothesis in code.
- At 5×10⁴ and 10⁵ **both** arms stall identically (now=111 / now=30, onset moving with box load) — no bounded-vs-pristine dissociation exists in any configuration measured.
- P3 (worst ≤ ~30 ms) failed in every telling; P1 remains untested — my own attempt couldn't reach a cut in 210 s under this window's load.
- Goal fit is also weak: the board assigns the burn-stutter seam ("not here… no lens re-measures them") to GPT's burst job.

The run's durable residue: the env-gated instrument, the probe, an accurate mechanism reading, and one inverted-but-real observation now on record — at 2×10⁴ on this box the bound *helps*. The next run should take P1 at a reached cut and a quiet-box pair past the wave; that run decides 6138's fix.
