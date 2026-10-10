# Predictions — the plane's capacity ladder (written before the ladder runs)

Question: as the fleet's population `N` scales on the shipped plane (`xtask universe --bench`),
which stage binds first at 60 Hz, where does per-member cost leave the cache-resident regime,
and where does the frame's own size rule end the dense order?

Machine: i7-4790 (Haswell), 1 MiB L2 per core, 8 MiB L3 shared, load ~2.3 (shared box).
All numbers are orders of magnitude for the M1; the digest, not the timing, is exact.

- **P1 (cache cliff).** The fleet's epoch-kick pass is O(N) over its members' hot state
  (motions + carries). I predict per-member engine cost is flat in N up to roughly the L2
  crossing (N·bytes_per_body ≈ 1 MiB, so N of order 10⁴) and rises by ≥1.5× per member once
  past it, with a second step near the L3 crossing (N of order 10⁵) if the pass still dominates.
- **P2 (which stage binds).** The view gather iterates every body each frame and the view JSON
  serialises every seen emitter. I predict the frame's cost order at large N is
  view_json ≥ view_gather > engine, and that the first stage to cross 16.7 ms unpaced is the
  readout (gather + JSON), at N between 10³ and 10⁴ — the plane's capacity today is capped by
  the readout, not the engine.
- **P3 (the extent wall).** The frame hands members out beyond |x| ≤ r_p/32 ≈ 148Q lattice
  units; the battle grid's side alone is 5·√(N/2)·Q plus a 20Q half-gap. I predict the in-frame
  ladder effectively ends near N ≈ 1024–1300: at N = 2048 the first anchors hand members out
  (leavers appear; the fleet may dissolve), so beyond the wall the run measures a mixed
  frame+tubes regime, not a denser frame.
- **P4 (threads).** At a fixed N the kick pass chunks over threads with identical bits: I
  predict the same digest at threads 1 and 4, and the fleet's per-frame engine cost falling
  by ≥2× at 4 threads when N is large enough for the pass to dominate.
- **P5 (rtf).** Engine work per presented frame grows with game-time advance per frame (∝ rtf:
  epochs fire per game time), while the view is per-frame work independent of rtf. I predict at
  rtf 100 the engine (fleet kicks) binds before the readout even at N = 1024.
- **P6 (controls).** Same seed/members/seconds twice: identical digest. Paced vs unpaced at
  rtf 1: identical digest (the budget moves work, never outcomes). Different members: different
  digest. If any of these fails, the harness is broken and the run is VOID.

What would make me wrong: if the sparse event core skips idle members (contacts rare at these
sizes), the epoch kick may be the only O(N) term and P1 moves; if the gather's Newton iteration
dominates per body, P2's order flips to gather > json at small N.

## Postscript (disclosed)
The first ladder (sweep.sh, `n*.json`) was voided by an instrument artifact: `--members` is
clamped to 400 in `xtask/src/universe/mod.rs:32`, so every rung above 400 measured the same
university (identical digests gave it away). The clamp was lifted to 2^21 and the decisive
ladder is sweep2.sh (`m*.json`, `r*.json`), run after these predictions were written. P1 was
held as untestable (the extent wall binds three orders below the cache cliff); P4's speedup
failed (digest held, no gain) — both reported in the dossier.
