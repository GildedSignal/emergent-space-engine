# Scout run: the memory the player's causal cone really costs

## The question (one sentence)

How fast does the irreducible LIVE state of the universe grow with play time — the light cone risk ("the light cone keeps growing"; HANDOFF, Risks) — and which mechanism from another field keeps it inside the 4 GiB live / 20 GiB disk budgets for 10⁹ bodies?

Ties to the board: bottleneck "fitting 10⁹ in 8 GB ... decided by distinctions created per game-second" and plane.md's H_live ("this, not the body count, decides whether a billion bodies fits"). The queued b-h-live build wires the MEASUREMENT into the dashboard; nobody owns the SCALING LAW or the storage mechanism. This run derives and falsifies both, and hands b-h-live the number to check against.

## Requirements as numbers (from the goal and PRINCIPLES)

- 10⁹ real bodies, never averaged (PRINCIPLES 6: every body real; board bottleneck 5).
- 8 GB unified memory; live budget 4 GiB; disk 20 GiB; one hour at 30 FPS minimum (approved plan budgets, "open, not dropped").
- Store the generator, not the generated (PRINCIPLES 6): undisturbed orbits cost ~0 (representation.md §6). So the only live bits are SURPRISES: encounters, contacts, decisions.
- Compute only surprises (PRINCIPLES 3): a body's canonical state is its current tube (E, L, epoch) — kicks update it IN PLACE. So memory grows by the COUNT of distinguished bodies, not by the length of their histories. (Errors never compound, PRINCIPLES 13, is what makes history-free state legal.)
- The player is the only seed (PRINCIPLES 5) and influence travels at c: distinctions outside the player's eventual light cone are lazily regenerable; distinctions inside must persist.
- Known anchors: ~0.126 bits/body for an undisturbed smooth belt (components-98bc, gold); ~4 bits per contact collision (H0173); ~1.1 encounter events per body per orbit at r8 belt-0 density; today's Body = 88 bytes.

## The premise to falsify (written as competing hypotheses)

- H_vol: live memory follows the light cone's VOLUME (πc²T² cumulative; inflow 2πc²T grows forever) — "the light cone keeps growing" read literally.
- H_rate: live memory follows the SURPRISE RATE inside the cone (constant after the cone covers the active region, since a finite star system is crossed by light in ~minutes of play at rtf 100), × survival fraction s(ε) of scars above the invariant quantum ε, × bits per surviving scar.
- Lever check: s(ε) and the cycle-memo hit rate decide the coefficient; the cone decides only when it saturates.

Kill criterion: if measured live bits follow neither (e.g. superlinear because scars breed scars — chaos coupling), the representation "state = current tube + surprise log" is wrong and shipmem must store correlations. That would be a premise-kill result (gold-worthy by itself).

## Fermi estimate (before running)

Belt at 2 AU (period ~8.9e7 s), rtf 100 (plane spec): one orbit = 8.9e5 game-seconds. 10⁹ bodies × 1.1 encounters/body/orbit / 8.9e5 s ≈ 1.2e3 encounters/game-second. Each distinguishes ≤2 bodies at ~16 B ⇒ ~40 KB/s ≈ 140 MB per play-hour, × s(ε). At s=1 that is ~28 h to fill 4 GiB; at s=0.1, ~280 h. Battles (contacts at 4 bits × dense rates) are the tail risk, out of this run's scope.
