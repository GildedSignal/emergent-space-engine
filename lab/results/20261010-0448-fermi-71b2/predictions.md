# Predictions (written before any run in this folder)

Question: at 10⁹ bodies on one M1, which budget term breaks first — bytes per body, kick events per game-second × ns per kick, or distinctions (H_live) per game-second — and by how many orders?

Held-out cases (not tuned on; the repo's own numbers are the priors, not the fits):

- P1 kick cost: `--kick-bench` median per-kick cost on this Linux/x86 box lands within 5–60 µs
  (the M1 measured 29 µs, H0210). Cloud/x86 may differ by ~2×, not more.
- P2 plane footprint: `--bench` reports bytes_per_body between 16 B (the Tube) and ~100 B;
  the scene holds 10³–10⁶ bodies, and kicks dominate the event count.
- P3 shape reuse: distinct exact ShapeKeys ≈ distinct kicks (the 5 Oct correction: 0% exact-memo
  hits on distinct kicks), while the law's quantized 12+12-bit key collapses them 3–30×.
- P4 belt encounters: `emergent-encounters verify` gives ≤ 10⁻⁴ real encounters per body per
  orbit at belt scale, with ≥ 100 units of candidate work per real encounter.
- P5 budget verdict (the derivation, fixed before measuring):
  - memory: 16 B tubes × 10⁹ = 16 GB, ~2.7× over the ~6 GB usable: half an order, NOT binding
    once populations hold (~0.13 bit/body → ~16 MB);
  - compute: at 1 AU, 32.5 kicks/orbit, ~29 µs/kick, rtf 100 → ~3 core-seconds per real second
    (call it borderline on 4 P-cores); critical semi-major axis a* ≈ 0.5–1 AU today,
    a* ≈ 3–6 AU with the 12.6× slack skin; rtf 10³ or dense inner belts break it by 1–2 orders;
  - H_live: bounded at belt scale (kicks are common-mode, land on shared quantized keys;
    encounter-created distinctions ~10⁰–10² bits/s per 10⁹ bodies); unbounded only in
    contact-rich frames (battles) and along the player's light cone.
- P6 claim check: the board's "10⁹ orbiting bodies would need about 190 cores" (29 Sep) overstates
  by ~2 orders at belt scale under today's event law (steps → kicks + compiled drift), but the
  number returns for short-period orbits: it is a radius-and-rtf statement, not a body-count one.
