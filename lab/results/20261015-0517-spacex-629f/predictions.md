# Predictions — 20261015-0517-spacex-629f (written before the decisive matrix)

Disclosed smoke before this file: N=1000 coast 12,000 game-s, three arms (control / lazy / lazy+cache256).
Digest `ab742740…` identical across the three; 20.3 promotions/demotion; 62% cache hit at 256. Nothing below
was tuned on anything bigger than that smoke.

The decisive matrix (each arm = one flight, same frames and presented times, cap 75 s):
10⁴ coast s1, 10⁴ burn s1, 10⁵ coast s1, 10⁴ coast s7 — each as control (lazy=0), lazy (lazy=1, cache=0),
lazy+cache (lazy=1, cache=1024). Held-out beyond them: 10⁴ coast s13, 2×10⁵ coast s1.

Kill criterion: any digest inequality control-vs-lazy (same arm) → demote-after-kick is NOT outcome-free on
this build; the configuration dies, the record stands as the kill.

1. **Seam-off = shipped:** all four control digests reproduce the scout's recorded baselines bit for bit
   (`f8b52855…` 10⁴ coast s1, `44d6a9b5…` 10⁴ burn s1, `2109a2e0…` 10⁵ coast s1, `a92b4b37…` 10⁴ coast s7 —
   scout 760f's record, b9ae-confirmed). If any differs, my seam changes outcomes when OFF and everything
   below is VOID.
2. **The certificate:** digest control = digest lazy on every arm, including the two held-out ones.
3. **The bill:** demotions ≥ 90% of kicks (cycles demote; passages/plunges do not); promotions per demotion
   in [8, 25] (b9ae's no-retention range; I demote at kick-apply, so I expect the high end).
4. **The cache (b9ae's named missing experiment, bounded form):** at capacity 1024 — hit rate ≥ 60%,
   compiles per demotion ≤ 5, wall(frame) strictly below the no-cache lazy arm on every arm, and
   lazy+cache/control wall ratio ≤ 1.3 on the coast arms. Standing memory stays the control's or below
   (the cache holds ≤ 1024 mints ≈ ≤ 1 MB against a 67 MB knot store at 10⁵).
5. **Memory:** knots standing fall by the demoted fraction (demoted slots keep none); rss at 10⁵ falls
   ≥ 25% vs control (b9ae measured −31%); `catalogue_live` at 10⁵ falls from ~bodies+48 toward ~10².
6. **Cache-invariance of the digest:** cache=1024 digests equal cache=0 digests (a mint cache cannot change
   outcomes; if it did, that is a seam bug and a kill).
7. **Held-out:** seed 13 and 2×10⁵ hold 2 (digest equality) with no new refusal; the 2×10⁵ arm's demoted
   fraction and rss fraction match the 10⁵ arm's within a few points (the seam is scale-free in N).
