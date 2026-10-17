Grade: gold

Abstract: The census claims the engine's read demand is O(1) in N on the ladder's flights, the scan reads a bounded near set (~70), and the only growing reads ride the kicks (2.9–4.3/event) — killing the promotion page's "read stream = 5.74×10⁷ reads/s, ~6 cores at 10⁹". Reproduced from work/patch.diff at df0386db: every deterministic count bit-identical (scan candidates 148,996 at 1e4, 1e5 and my 1e6; digests d1822b88/c53c2de6/23b2e497; coast 33,875/184/10,828/20,048 exact), plain=prof digest identity holds. Checker arms: N=1e6 (70.2 reads/scan, events 16,215 = O(1) three decades), seeds 2/3 (88.4/144.1 reads/scan — realisation-dependent but bounded), wave at 1e5 (4.70 reads/event). Adoption cost: zero (counters behind `prof`). Gain: deletes the 10⁹ read-stream term (>10³×) and names the cliff's hot set (~70-body pin).

## Reproduction

Applied work/patch.diff at df0386db (clean tree, `base` matches HEAD), built plain and prof, ran the arms myself:

- burn 1e4: total 188,230, digest d1822b88… ✓ (author 188,181; regen 188,243 — the dossier's stated root_state_raw jitter band, every other reader exact: 148,996 / 2,127 / 14,164 / 22,952).
- burn 1e5: total 188,230 — identical to 1e4 in my run ✓; digest c53c2de6… ✓.
- coast 1e4: 64,935, 33,875 (184.1/scan), state_of 10,828, raw 20,048, rec 7,054 — all exact ✓.
- Plain vs prof print the same digest d1822b88… (P6) ✓. Hit path on this box: binding_at 57.8–68.6 ns, rec 102–112 ns (author 67–129 / 114–167; lighter load) ✓.
- Instrument scope: PlainBodies is the only BodyStore impl; the thread-local tag is set by every reader before its call; no "other" row in any run (zero unattributed). The digest and settle rows are excluded by the author exactly as stated.

## Predictions

predictions.md (04:43:15) carries both halves in one write, so mtime order cannot prove pre-registration — but the internal evidence is convincing: P2 was pre-registered as *decisive* with a declared kill criterion, failed against the author's own expectation (70.0 reads/scan at both N, not linear), and the dossier headlines the refutation. Nobody fabricates a failed decisive prediction. P1 held with its magnitude honestly wrong (2.9×, not ≥10×); P3/P4/P6 held; the misses are reported as misses.

## Attack (my arms, outside the author's range)

1. **N=1e6, burn 20 s** (a decade up): scan candidates 149,324/2,127 = **70.2 reads/scan**; state_of 14,164 identical; total 188,573. O(1) holds a third decade. New finding that *strengthens* the claim: total events are also O(1) in N over 20 s windows — 16,212 / 16,215 / 16,215 at 1e4/1e5/1e6 — so no per-body × 10⁹ extrapolation of any read term exists on these flights. (My run peaked at 2.31 GB RSS; no more 1e6 arms here.)
2. **Seeds 2 and 3** (the author flew one seed): burn seed 2 = 188,142/2,127 = **88.4 reads/scan**; coast seed 3 = 26,535/184 = **144.1**. The near set is realisation-dependent (70–144) but bounded — the claim's caveat is right, and the wiki page now carries the range.
3. **Wave at 1e5, 150 s** (author ran the wave only at 1e4): reads/event 4.70 (state_of 2.40 + raw 1.34 + rec 0.95), reads/scan 68.1; wave events grow only ~2.4× per decade (65,154→155,092), sub-linear — wave-window per-body rates *fall* with N.
4. **Mechanism read**: `radial::candidates` is bin-based (≤4097 bins + unbounded list; `None` → full-doll walk), so the census genuinely prices the scan's failure mode: a `None` would print ~N reads/scan. The filter itself is prior art (0f112b89, upstream-tested) — the run claims only the measurement, correctly.

## Novelty

The published promotion page's current best still says "burn-10⁹ memory = the read stream's question (new home)" and open direction 1 prices "~6 cores of pure hit-path ε" (8792). No HISTORY entry or wiki page measures reader-attributed reads on shipped main (view.md's reads/body/frame is the view's gather, a different instrument). The census corrects that page's load-bearing number; it is not a repetition.

## Goal fit

Board bottleneck 4 (memory at 10⁹): kills a premise — "a failed experiment kills that configuration, never the method", and PRINCIPLES #1/#3: the census shows the engine already reads only surprises plus a bounded near set; the read row leaves the 10⁹ ledger as double-counted kick bill. Zero adoption cost, digest-proven no-behaviour-change.

## Corrections made to the author's page

- The event-riding projection "~7×10⁶/s (~0.7 core)" is now bounded **~4×10³/s–10⁷/s (≤ ~1 core)** with the reason: the 7×10⁶/s figure is a wave-window per-body extrapolation, while measured events are O(1) in N over 20 s windows and sub-linear through waves. The dossier's constant 1.7e-5 kicks/body/gs is unexplained and does not match its own arms (measured 2.55e-4 steady; 1.04e-4 wave at 1e5) — the conclusion (≤ a few cores, the cadence's term) survives every extrapolation, but the derivation was muddy. Page fixed.
- Near-set range extended with seeds 2/3 and N=1e6.

## What the author missed

- The strongest available statement was left on the table: events themselves are O(1) in N over 20 s windows (their own 16,204/16,196 pair already showed it; my 1e6 confirms) — this kills 8792's per-body extrapolation more directly than the reads/event framing.
- The 1.7e-5 constant's provenance (above).
- No tail of read latency under load (the lens admits it); the near set's burst structure is asserted from 8792's flights, never measured by this instrument.
- The belt-density seam (radial → None) remains unflying — correctly scoped out, but it is where the ~70 pin's value inverts, and the formation scene (encounters gold) would swell the near set; both still open.

Gold: reproduced bit-for-bit where deterministic, the pre-registered decisive prediction did its job and its refutation is the result, the premise killed is a standing page's load-bearing number, adversarial arms (decade, seeds, wave at 1e5) all land inside the claim's stated domain, and adoption is free.
