# Run 20261019-1817-system-c7a6 — system lens: the demand side of the history retention

## Claim

The burn-mode memory ratchet's fuel — the retention law's `keep = 2·light_distance + 2²⁶` — is
supplied for a reader that reads at most **one** light leg (the view's retarded crossing), and on
the ratchet's own scene (headless: every bench, replay and gate flight) for **no reader at all**:
over a 197,644-game-s burn at 3×10⁴ bodies, the store served 7,266,323 `binding_at` calls of which
20,413 (0.28%) touched history, the deepest **5,273 game-s** (constant; the coast control reads
5,271) — while the median body's `keep` grew to **105,316 game-s** and the stock to 272,314
segments (9.07/body): the ratchet is ≥ 92% unread stock, and the second light leg of the rule is
read by nobody on any arm.

## Bottleneck

Memory at 10⁹ (the board's list; HANDOFF's scoreboard row "memory per body", ~10^2.6 gap). Today's
five runs (4447, e181, 527a, b911, f80a) all attacked the ratchet from the **supply** side (fences,
freezes, TTLs). This run measures the **demand** side for the first time: what the history store is
actually asked for, per call site, against what the law pays to keep. The expected gain: deleting
the unread term is not an optimisation but a deletion (principle 1); headless, `keep` can drop from
O(c·t) to a constant with no observable change, which deletes channel 2 of the ratchet outright in
every non-observer context (replays, benches, gates, the recorder) and halves it in the game.

## Evidence (all numbers from `work/*.log` via `work/census_sum.py`; regen: `regen.sh`, ~4 min)

Scene: the shipped `nladder` example, 3×10⁴, seed 1, rtf 2000, 12 ms — f80a's own arm class.
Instrument: a print-only census inside `PlainBodies::binding_at` (off = shipped bits), tagging the
two deep-capable sites (VIEW = the past-light-cone gather; SCAN = a held scan's capture; everything
else — ramp walk-backs, rebinds, handoffs, clock sources — one bucket), plus `probe_keep_ticks`
(the exact `keep` expression) and the retention stock. 1 game-s = 4.9255 µs; the doll interval is
28,141.5 game-s (checked against the record).

- **A — the ratchet scene, headless** (`armA_burn.log`, 197,644 game-s, RSS 1,042 MB): reads
  7,266,323; history 20,413 (0.28%); 3.45×10⁻⁶ history reads per body per game-s. Deepest read of
  the whole flight **5,272.9 game-s** (once, at the ramp site, gs 84,670; the scan site's bursts
  peak at 151–155 game-s; most windows read zero history at all). Supply meanwhile: keep_med
  2,792 → 105,316 game-s (linear, ≈ 2β·t with β ≈ 0.27); stock 272,314 segments on 30,043 bodies
  (9.07/body — f80a's own digits reproduced: saturation at the first kick wave, 8.03/body at 174k).
  **keep_med/deepest-read = 20.0× at the end, growing linearly; ≥ 92.5% of the retained segments
  were never read once in the entire flight** (20,413 reads, worst case one segment each, vs
  272,314 retained).
- **B — the view gathers** (`armB_view.log`, every 900 frames): the view is the one deep reader:
  121k–178k history reads per gather, look-back p50 49,518 game-s at gs 178k — matching the
  gather's own emitter ages (p50 43,097, max 45,590 game-s = one light leg, `viewcensus` lines).
  The ratchet is unchanged (272,268 segs, RSS 1,044 MB): the view's demand adds nothing to the
  supply-driven retention. Deepest census read 93,445 game-s = Newton's first eval from a
  15-wall-s-stale guess (the instrument's cadence), beyond one leg only by that slack.
- **D — the view at the game's cadence** (`armD_view.log`, gather every 60 frames, 79,879 game-s):
  the lawful demand is the crossing itself: ages p50 4,623→4,934, max 6,079→7,292 game-s at
  gs 50–58k against keep_med 8,265–12,906 there — **keep covers the deepest lawful read at
  1.7–2.2×, and that factor is exactly the rule's own 2·** (one leg read, two paid). Reads deeper
  than age+cadcence-gap are warm-guess probing (one emitter's search stuck at a fixed ~21.3k tick
  for ~30k game-s, ~2 reads per gather; probing a pruned region returns None and the view
  brackets down — demand-shaped, not law-shaped).
- **C — coast control** (`armC_coast.log`, 189,582 game-s): deepest read **5,271.3** game-s — the
  same constant as the burn's 5,272.9; stock flat at 30,506 segs (the locals), RSS 167 MB. The
  demand side is play-phase-independent; only the supply differs (keep_med 2,792 vs 105,316).

## Predictions (`predictions.md`, written before the first flight)

- P1 held on every clause except one number: ≥99% current-binding ✓ (99.72%); deepest ≤ 8×10⁴ ✓
  (5.3×10³, flat); keep/deepest ≥ 4× at 150k ✓ (measured 11.8× at 159k); the letter's "keep
  passes 3×10⁵ game-s" **failed** — I misestimated the recession (β ≈ 0.27, not ~1); keep_med
  reaches 1.05×10⁵ at 197k. The ratio clause is unaffected (it is what the claim needs).
- P2 held: the view reads at ≈ the emitter age (one leg), never beyond it by more than the
  gather-cadence slack; the second leg is read by nobody on any arm. The "within one interval"
  letter failed at my artificial cadences (stale-guess probing overshoots the interval; arm D at
  the game's cadence brings it back to ≈ one frame).
- P3 held, exactly: 5,272.9 (burn) vs 5,271.3 (coast) — the same demand constant.
- P4 held with 4 orders of margin: 3.45×10⁻⁶ history reads/body/game-s against a stock of 9
  segments/body and growing.

## What would make it wrong

- **A reader this census cannot see**: it counts every `binding_at` call in the process (the store
  itself is instrumented, not the call sites), so a missed reader would have to bypass the store —
  `bindings_of` (the radial rebuild) is the only history path not counted, and it is a writer-side
  sweep, not a read demand.
- **Gravity as news** (law.md, designed, not built): retarded source reads at `t − ld(i,j)` —
  bounded by the doll diameter for the belt, but at two stars `ld(i,j)` can reach `ld(i)+ld(j)`;
  the 2·ld(i) rule covers exactly the antipodal worst case of that future reader, keyed on the
  wrong quantity (the pair's distance, not twice the body's own). Until it is built, the census
  stands: today's engine has no two-leg reader. The adoption should key that margin to the
  reader's pair distance when the reader exists, not to every body forever.
- **The view's None-probing**: a pruned region makes `crossing` bracket down to tick 0 for an
  emitter whose history is gone; today that is silent and rare (the stuck-tick emitter), but a
  keep shorter than one leg would make emitters vanish from the view (a behaviour, not a refusal).
  The in-game floor is one leg + the Newton slack; headless there is no floor at all beyond the
  5.3×10³ s constant.

## Cost of adoption, and fit with PRINCIPLES

Headless (replays, benches, gates, the recorder): `keep = constant` (measured: 5.3×10³ s + margin
≈ the 2²⁶ term × 16) deletes channel 2 with zero observable change — prune is forget-only, so no
digest can move (b911 already proved stronger freezes digest-neutral). In the game: `keep =
ld + 2²⁶` halves the slope; the deeper cut is the lens's unification — **the retention (an
interval supply, O(c·t)) and the view's crossing (a point demand, one tick per body per frame,
already memoised as `ViewCache`'s guess, and regenerable from the exact key per 5465's gold) are
the two sides of one mechanism**: hold or regenerate the crossing binding per emitter instead of
retaining the interval, and retention returns to O(1) in play time — channel 2 dies by demand,
not by freeze, and with it the f80a/e181/527a line of fences. "Less is more… Delete before
optimizing" (principle 1); "Nothing is evolved that can be derived when looked at (clocks,
redshift, views)" (principle 3) — the retained interval is exactly an evolved view cache.
Adoption is a law-visible change only through the view (an emitter whose crossing is dropped must
be re-derived, not silently skipped); it is the integrator's call where that lands (view.rs vs
body.rs).

## The lens

What it may have made me miss: the system lens reads the ratchet as one mechanism (view demand ×
interval supply) and can under-weight the genuinely hard case — the antipodal mutual retarded
read above, and the recorder/replay contract (if a replay ever re-gathers the view at a past tick,
the demand becomes the whole interval again; the census says today's replays never do). Also:
single scene (one star, one seed, one rung 3×10⁴), Linux/x86, orders of magnitude only; the
5,273 s demand constant is empirical, not derived — its mechanism (credit's level walk-back × the
2²⁶ margin) is named but not proven here.
