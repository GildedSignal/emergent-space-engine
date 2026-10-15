# Predictions (written before the decisive flights)

The claim under test (today's consensus, twice gold-checked: 20261015-1615-quant-0619 and
20261015-1615-second-…-f55d): **the burn knee is the cumulative demotion count ≈ N; no
bounded cap serves burn; a fixed cap degrades with N.** Its named, unmeasured falsifier
(b0ed's checker, nladder page open direction 4): *a co-orbital-concentrated scene whose
burn re-reads are temporally local would collapse the knee below demotions and revive a
bounded burn cap.*

Scene: the ladder's population with the belt replaced by K co-orbital formations (K=100
and K=10), each a tight clump (±0.5° phase/angle, ±0.1% semi-major axis, e Rayleigh σ
0.005), formations spread over [2.2, 3.0) AU. Same seed, same counts, same flight
(`burn`, cut 20,000 game-s, rtf 1000, seed 1). Instrument: f55d's patch verbatim
(ES_LAZY_ENTRY/ES_RETAIN/ES_RETAIN_MAX + counters) + my scene edit, env-gated
(`ES_LADDER_FORM=K`), so the belt arms are bit-for-bit the record's.

## P1 — the kill test (falsifier lives / dies)

Metric: the **razor cap** (the smallest cap with `evictions = 0`, knee ≤ that cap; f55d's
razor: cap = bill−1 evicts exactly 1), and the promotion ratio `promotions/demotions` at
fixed caps.

- **Falsifier LIVES if** at 10⁵/K=100 the razor cap is ≤ ~35,000 (offset + a few × N/K)
  where the belt needs 130,187 — i.e. the knee stops tracking N — AND cap 4,096 holds
  ratio ≤ 1.5 with hit fraction ≥ 0.85.
- **Falsifier DIES if** the formation's demotions ≈ belt's demotions (N + offset, within
  ±3%) AND every cap below demotions/4 shows ratio ≥ 3. Then the no-cap law is
  scene-independent and the cure stays "delete the reads".
- My expectation, registered before flying: **it lives, weakly** — knee collapses toward
  (offset + N/K), because a kick's position walk reads its formation, not the belt; but
  the +30k prefix (the plane's own reads) stays, so the win is bounded by the offset.

## P2 — identity (the certificate, must hold in every arm)

- Belt ctl digest at 10⁵ burn 20k seed 1 = `d3542eea702e6f22…` (f55d's, unchanged by my
  edit — my edit must not touch the belt path).
- Every seam arm (retain-global, capped) on the formation scene prints the formation ctl
  digest bit for bit. Any mismatch voids the run (VOID, not a physics result).

## P3 — K-scaling (if P1 lives)

Razor cap at K=10 ≈ razor cap at K=100 + 9,000 (offset shared, N/K term ×10): the knee
tracks formation size, not N. If both K sit at the same razor as the belt, P1's collapse
was luck, not mechanism.

## P4 — the scene must stay flyable

Refusals 0, lost bodies only where the belt loses them (28), wall ≤ ~90 s a flight at
10⁵. If the formation scene explodes (encounter work under concentration — the
encounters gold's warning), I drop to 10⁴ and disclose; the knee contrast is then
N = 10⁴ vs the belt's 40,960-knee arm of 0619.
