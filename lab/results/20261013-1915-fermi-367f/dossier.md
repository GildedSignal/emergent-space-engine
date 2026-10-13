# Dossier — 20261013-1915-fermi-367f

**Claim.** On the shipped plane the first N-walls are the compact fleet frame itself — it
leaks members superlinearly (rate ∝ N^1.4, its own advance ∝ N^1.9) and every leak is a
sticky promotion of 486–585 µs and ~8.3 kB that never demotes — so the plane tops out at
~10³ members at flying pace (rtf 100 collapses between 400 and 1,500, both seeds), an
order below the walk-tier wall (~0.1 µs/body → ~5×10⁴), and the shipped promotion is
3000× the compact member it leaves and unbounded in memory: at 10⁹, sticky promotion
alone grows ~15 MB/game-s even in the quiet belt regime (8 GB in ~9 game-minutes), so the
smallest promotion must be ephemeral, shared-shape and census-gated, not cheaper.

**Bottleneck.** The board's top item (bodies in the flyable engine, 28 vs 10⁹): the lab's
two named questions — which term breaks first as the plane grows, and the smallest
promotion between a compact body and a live one. Gain: orders the N ladder's fixes (the
integrator's gate N1 is in flight on `wt/nladder`); deletes the premise that the walk
tier or memory is the plane's first wall, and any plan to reach 10⁹ by making the
promotion cheaper rather than ephemeral.

**Evidence** (shipped code + the probe patch: `--members` clamp lifted, RSS + the 24
`prof` counters added to `universe --bench`; every run ≤ 60 s, shared Linux/x86
i7-4790-class, orders of magnitude only; the patch drops the report's `digest` field —
`digest_at_cut` and its settle still run; inputs are seed-deterministic):

```
cargo build --release -p xtask --features emergent-universe/prof
xtask universe --bench --seconds 8 --rtf 100 --members {48,400,1500}   # 4 s at 4000
xtask universe --bench --seconds 8 --rtf 1    --members {48,400,1500,4000}
xtask universe --bench --seconds 8 --rtf 100 --members {400,1500} --seed 3
python3 analyze.py    # ladder-table.txt
```

The ladder (`ladder-table.txt`, full JSONs in `data/`):

| pace | members | rtf med | engine p50 | worst CPU | events/s | leavers | fleet item | handout |
|---|---|---|---|---|---|---|---|---|
| 100 | 48 | 100 | 0.07 ms | 6.7 ms | 407 | 43 | 25 µs | 585 µs |
| 100 | 400 | 100 | 2.2 ms | 10.2 ms | 1,871 | 375 | 43 µs | 486 µs |
| 100 | 1500 | **0.0** | 5.1 ms (cap) | 26.0 ms | 1,622 | 1,355 | 239 µs | 486 µs |
| 100 | 4000 | **0.0** | 5.5 ms (cap) | 71.9 ms | 357 | 2,163 | 18.6 ms | 492 µs |
| 1 | 400 | 1.0 | 0.08 ms | 3.2 ms | 61 | 0 | 51 µs | — |
| 1 | 1500 | 1.0 | 0.22 ms | 13.3 ms | 103 | 232 | 362 µs | 519 µs |
| 1 | 4000 | **0.0** | 5.0 ms (cap) | 62.0 ms | 200 | 2,163 | 4,311 µs | 526 µs |

- **Break order, flying pace:** rtf holds at 400 (engine p50 2.2 ms of the 5 ms budget),
  collapses at 1,500 (449/480 overflow frames); seed 3 reproduces (holds 400, collapses
  1,500, events/s 1,625/1,172 vs 1,871/1,622). The binding term is the event stream,
  ∝ N: ~0.041 events/member/game-s in the battle regime, kicks 182–231 µs + handouts
  ~490 µs each.
- **The compact frame leaks superlinearly.** At rtf 1 (battle fully resolved) the leak
  rate is 0 at 400, 1.9×10⁻² at 1,500, 6.8×10⁻² per member per game-s at 4,000 — ∝
  N^~1.4, total leavers/s ∝ N^~2.4; a 10⁵-member frame would empty in game-milliseconds.
  The fleet's own advance per item: 14 → 51 → 362 → 4,311 µs (rtf 1) ≈ **N^1.9** — the
  plane's dense pocket is quadratic in itself, independent of the live side.
- **The promotion (the board's second question), as shipped** (`resolve_handout`, the
  only wired compact→live path): 486–585 µs, **flat in N**; bind 355–421 µs of it with
  the coarser re-fit (`fit2`) firing on 52–63% of handouts (the leaver's word is too
  small for its new tube); replan 100–160 µs. = 2.2 kicks, dearer than the player item
  (208–380 µs). Standing bytes: 8,257 B marginal per promoted body (bytes/body 1,214 →
  8,167), **sticky — no demotion path exists**. Exchange rates: ~3,000× the 22-bit
  compact member, ~145× the 56.8 B packed live floor (42e6). RSS after construction is
  flat (4.7–6.2 MB for 48–4,000 members — the compact side is cheap); peak RSS is all
  promotion history (80 MB at 4,000/rtf 1; 709 MB at 4,000/rtf 100 with 400 game-s of
  it).
- **What does not break first:** the walk tier (rekey 0.10–0.15 µs/body/frame here, at
  the cheap end of the wiki's 0.25–1.1 µs tube slopes — ~5×10⁴ bodies to the 5 ms
  budget) and store memory at these rungs. Both are an order behind the frame's own
  walls.
- **The 10⁹ identity** (measured slopes, not run): belt regime (a9d7's 3.6×10⁻⁵
  events/body/game-s): 3.6×10⁴ events/game-s ⇒ ~8.3 cores of kicks at 231 µs + ~0.95
  cores of promotions at a 5% promotion mix ⇒ **the kick cost, not the promotion, is the
  quiet-belt CPU wall; but sticky promotion grows ~15 MB/game-s ⇒ 8 GB in ~9 game-min**.
  Plane-battle regime (0.041 events/member/game-s, this run): ~10⁴ cores — the battle
  density is a local pocket, 10⁹ cannot live there.

**Predictions** (`predictions.md`, written after the members-48 smoke test only): (1)
rtf-100 collapse between 400 and 1,500 with ship items dominant — **held** (ship 116–248
µs × the most items at every collapsed rung); (2) quiet walk tier linear, crossing 5 ms
at ~8–15×10³ live bodies — **partially held**: linear at 0.10–0.15 µs/body, but never
reached — the frame's leak and quadratic advance collapse the run at 4,000 first; (3)
construction RSS 1–3 kB/member — **wrong**: flat 4.7–6.2 MB total (the compact member is
~0–1 kB; the fleet world's cost is lost in the process floor below ~400 members); (4)
handout flat in N at 1.0–1.5 ms — **held** (486–585 µs, same order); (5) seed 3 within
3×/2× — **held**; (6) kill criterion (events sublinear in N) — not triggered.

**What would make it wrong.** The leak and quadratic fleet-advance slopes are measured at
only two adequately-sampled rungs (1,500, 4,000) on one scene and two seeds — a different
battle geometry (sparser Q, wider lattice) could soften both; the promotion cost could
drop with shape sharing (the catalogue dedup lever) without changing stickiness; the 10⁹
identity extrapolates two event rates measured on different scenes (a9d7's plane, this
battle). Adoption cost: none required to adopt the ordering — it is a measurement; the
design consequence (ephemeral promotion) is a build, and the ladder's fixes should
target the fleet frame's leak and advance before the walk tier. PRINCIPLES fit: "Less is
more… The cheapest compute is compute not done" — a sticky promotion is work that never
ends; "Store the generator, not the generated" — the promoted body re-stores what the
frame already generates; "Each scale resolves only what matters at that scale" — the
battle pocket is one scale, and 10⁹ lives at the belt's.

**The lens (Fermi) may have made me miss:** timing precision (shared box, single runs
per rung — medians only, no seed ensemble at every rung); the frame leak's *cause*
(which rule of `scenes::battle`/the engine's size rule ejects members — a dynamics
question, not a cost question); and everything about what the promotion must carry
information-theoretically beyond the two floors I quoted (56.8 B packed, 22 bits
compact) — the true minimum of an *ephemeral* promotion (shared shape + slot + surprise)
is derived, not measured, at ~2–20 µs and ~80 B.
