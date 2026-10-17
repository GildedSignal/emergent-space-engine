- **Claim:** the belt wave kick's interior is decomposed on shipped code — it is ~8 decode walks plus the
  fit (~95% of the item), and two of the walks are exact duplicates of the kick's own readout, deleted
  bit for bit (−17% on the fired kick, digest-identical everywhere), with a third exact duplicate named
  and priced (apply's position walk, 2.06 walks per kick, another −13%).

- **Bottleneck:** the kick (the scoreboard's widest per-op gap, ~10^3.3; the board's focus item 3), and
  specifically kick-jet's open next lever: "the wave's ~85–93% non-compile attendants". This run is that
  decomposition, on the shipped `kick_clock` path, with the two cheapest exact deletions built and
  A/B'd. Expected gain: 1.2× on the wave cycle now (built), ~1.5× with the named third duplicate; it
  deletes bookkeeping re-derivations, not physics — "nothing is evolved that can be derived when looked
  at" (PRINCIPLES #3).

- **Evidence** (Linux/x86 shared box, 1 thread, unlimited budget, N = 10^5 ladder belt, seed 1; every
  number regenerates from `regen.sh`, raw in `raw/`):
  - **The decomposition** (steady state, waves 2–3, 389,211 fired kicks, off-arm): one fired belt kick
    costs **49.6 µs** inside the item: fit (`bind_surface`: fit_key + compile + word) **20.3 (41%)**,
    **3 source reads** (one planet walk each, `ctx::state_of`) **11.5 (23%)**, the kick's own readout
    4.2 (8%), the bind's decode 3.8 (8%), **the tau pair 7.5 (15%)**, remainder ~2.3 (5%). Around the
    item: boundary 9.3 µs (readout 4.3), apply 6.1 (of which the position walk 5.0, 82%), requeue 0.5.
    Walks + fit ≈ 95% of the item. First wave (102,800 kicks): item 45.8 µs, same shape.
  - **The two exact duplicates, built** (`ES_TAU_CARRY`, default off = shipped bits): the kick reads its
    binding at `t` and throws the orbit state away, then `rebind` walks the same (binding, t) again for
    tau, and walks the binding **at its own anchor** — a value `bind_in`'s decode already computed at
    bind time. The carry hands the kick's decode to the rebind and caches the anchor's proper time in
    the Binding (+~24 B on a ~5 KB record). Result: `W_TAUT` 389,211 → **11** calls, `W_TAU0` → **1**
    (the residuals are hand-out paths with no preceding readout); fired clock kick **49.6 → 41.3 µs
    (−17%)**, Wisdom-Holman kick 41.0 → 32.9 (−20%), whole event cycle **33.5 → 29.5 µs (−12%)**, wave
    CPU 82.0 → 73.6 µs/kick. First wave (where only the hint half can fire, each body's first kick):
    45.8 → 43.1 µs.
  - **Bit-identity:** `Universe::digest()` at the cut identical between arms in both windows
    (`0d8ced80…`, `07891363…`), and all 8 `frame_digest` flights × 4 schedules identical between arms
    (player, locals, burns, encounters — not only the belt). **The off-arm was also diffed against a
    pristine-main build** (`git worktree` at HEAD, `raw/fd_pristine_main.txt`): identical, line for
    line — the patched tree with the gate off is the shipped engine, bit for bit.
  - **The third exact duplicate, named and priced, not built:** `apply`'s position walk
    (`root_state_raw`) re-reads the body's binding at the event tick the resolver just read — for a
    doll-0 body it is the same `binding_at(i,t).cartesian(t)` the kick performed (child dolls add the
    parent chain). Measured **5.0 µs × 2.06 per kick = 10.4 µs/kick (−13% of the cycle)**: carrying the
    resolved state out to `apply` is exact by the same argument as the tau pair.
  - **Source-read memoization is dead on the spread belt:** the (body, tick) census shows repeat share
    **0.029** on the first wave (each body's clock tick is its own), 0.296 in steady state (boundary
    ticks collide more; worst multiplicity 322 — the locals' aligned comb, not the belt). A shared-key
    memo saves ≤ 0.3 × 23% ≈ 7% and only where ticks collide.
  - **Order-of-magnitude pricing at 10⁹** (x86 µs; the M1 re-measures): steady belt ≈ 1.68M kicks/wall-s
    at rtf 100 → ~140 cores at 82 µs/kick; the built carry deletes ~8.4 µs/kick ≈ **17 cores per
    billion**; with the apply-walk carry ~**30 cores (−22%)** — without touching the law, the cadence,
    or a single bit.

- **Predictions:** `predictions.md` was written before the decisive runs. Held: bit-identity (1), the
  tau pair = 1.0 duplicate walk per kick and W_TAUT → 0 / W_TAU0 → first-kick-only (2), both halves zero
  in steady state with −17% on the item (3), walks+fit ≥ 80% of the item (4, measured 95%), the
  apply-walk price (6). **Failed:** the source-repeat share ≥ 0.6 at N = 10^5 — measured 0.029; the
  0.614 I saw at N = 2000 was the locals' comb dominating a small belt, and I carried it into the
  prediction. The memo lever is dead on the spread belt, and the run says so.

- **What would make it wrong:** the carries are exact only because `bind_in` decodes at the bind tick
  with the same `(entry, tube, clock_exp, units)` the walks use — any future change that rebinds a
  Binding without going through `bind_in`/`rebind` (or decodes at a different tick than `event_time`)
  must set `anchor_proper = None` or the cached tau goes stale. The wall-clock shares are one box, one
  seed, load ~1–4; the call counts and digests are deterministic. The `−17%/−13%` are x86 shares; the
  M1's fit is cheaper (compile-only anchor 4.4 µs, c4d3), so the walks' share there is *larger* and the
  deletions should not shrink.
  **Cost of adopting:** ~60 lines, one field on Binding, two call-site gates; no API change; default
  off. **Fit with PRINCIPLES:** "Compute only surprises… nothing is evolved that can be derived when
  looked at" (#3); "the best part is no part" (#17): these are re-derivations of state the engine
  already held in hand at the same tick.

- **The lens (Quant):** latency budgets and duplicate work are its home ground, but it prices stages
  and can undervalue that the fit's 41% is not waste to shave here — it is the compile wall the
  kick-jet program already owns, and a schedule of small exact wins must not crowd out the law-level
  cadence fix (kick-cadence open direction 2: ~5× fewer events) that dwarfs both.

- **Grade proposed: silver** — real, reproduced, digest-identical, but 1.2× built (plus a priced 1.5×
  path), not the 10× gold bar. The named experiment to gold: carry the resolved state into `apply`
  (deleting the position walk, −13%), then re-price the wave on the M1 where the fit's share is halved.
