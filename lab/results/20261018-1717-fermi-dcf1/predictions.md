# Predictions (written before any flight; the build is running, nothing has flown)

The question: is taleb-2403's fence-sizing inference sound at the next unflown rung? The inference
rescales acf2's coast byte law (bytes_touched = λ·game_s·(K+38)·224 B, 8 GB at 687 game-s at 10⁶) by
the burn multiplier 13.5× to "≈ 51 game-s to 8 GB at 10⁶ under continuous L8". Its own checker's
10⁵ burn arm (held 705, footprint 237→274 MB) sits ~3 orders below the retained bytes that law
implies per held scan ((K+38)·224 B = 22.4 MB × 705 = 15.8 GB), so the inference's retention term is
in tension with the only flown burn point. I fly the unflown interior rung K = 3×10⁵ (the 10⁶ build
alone is ~2.4 GB, over this window's 2 GB process cap; 3×10⁵ builds at ~0.7-0.9 GB) and adjudicate
which term the burn wall is made of there: retention (memory) or service (CPU).

Two hypotheses, separated by ~3 orders of magnitude in the RSS slope per game-second:

- **H_A (the inference's law holds under burn):** every mint retains (K+38)·224 B ≈ 67 MB at
  K = 3×10⁵ until answered; burn arrivals λ ≈ 0.7/game-s distinct; starved frames answer almost
  nothing → RSS slope ≈ 47 MB/game-s, the process crosses ~1.9 GB within ~25 game-s (≈ 0.25 wall-s
  at rtf 100) after the first burn mint, and is killed. The 51-game-s wall at 10⁶ then stands.
- **H_B (light retention under burn, the checker's 10⁵ reading):** the per-mint retained bytes
  collapse (answers in idle time, transient held peaks), RSS slope ≤ 0.5 MB/game-s, the flight
  survives 6 s of wall time with held growing to hundreds; the wall is then CPU/service, not
  memory, and the fence's sizing must be re-derived from the service law, not the byte law.

Cases not tuned on: none — no flight at any K has been run by me at the time of writing. The
controls (10⁴ coast, 10⁵ burn) are flown first only to reproduce the page's anchors, not to fit
anything.

## Point predictions

1. **λ (coast, K = 3×10⁵):** 0.05-0.06 held-scan mints per game-s (K-flat per 2403's checker at
   10⁴→10⁵).
2. **λ ratio (burn/coast, K = 3×10⁵):** distinct-rate ratio in [10×, 17×] (robust ratio 12.8-13.2
   at 10⁴-10⁵); the burn slope's implied mint rate is 0.5-1.2/game-s under H_A.
3. **RSS slope (burn, K = 3×10⁵):** the decisive number. H_A: 30-70 MB/game-s (process killed
   within the flight). H_B: < 0.5 MB/game-s (survives). I predict **H_A at coast and H_B's slope
   magnitude under burn is wrong by ≤ 10× if the checker's 10⁵ reading generalizes; my own Fermi
   estimate (below) says H_A's slope should appear but saturate at the SCAN_BACKLOG cap** — i.e.
   held climbs to 2048 and stays, RSS then flat, frames pay forced answers. The clean kill: if the
   slope is neither ≥ 10 MB/game-s nor accompanied by held → 2048 pinning, the page's law is
   missing a term at this K.
4. **held_max (burn, K = 3×10⁵):** reaches the SCAN_BACKLOG cap 2048 and pins there (arrivals
   0.7/game-s, service starved by the 12 ms budget at ~7 µs/member × 3×10⁵ members ≈ 2.1 s of work
   per full answer — no, per-answer cost is the compare form ~0.5 ns/member ≈ 0.15 ms, so idle
   drain CAN answer several per frame; prediction: held oscillates well under 2048, 50-800).
5. **Frames (burn, K = 3×10⁵):** p99 engine ms > 12 (over budget) in most burn frames; the
   presented game-s still reach ≥ 70% of target (frame_to presents anyway, per the 10⁵ before-table
   lag 1.667 s over 2,000 game-s ≈ 0.08% starvation).
6. **Coast slope (K = 3×10⁵):** if H_A's retention holds at coast, 0.05 × 67 MB ≈ 3.4 MB/game-s —
   the coast flight must be cut short (≤ 3 s wall) to stay under the cap; if the coast flight stays
   flat instead, the (K+38)·224 retention law itself fails at this K and the 687-game-s/10⁶ wall
   claim dies with it.
7. **Build:** 3×10⁵ builds in 6-12 s at ~0.7-0.9 GB (1e6: 30 s, 2.4 GB, linear per the before
   table).

## Fermi estimate behind prediction 3 (written before the flights)

Per burn game-second at K = 3×10⁵: arrivals ≈ 0.7 mints × 67 MB = 47 MB/game-s minted. Service: the
idle drain pays answers when the frame has margin; a burn frame at 3×10⁵ runs near/over its 12 ms
budget (the before-table: 10⁵ burn p50 13.1 ms; the per-frame item cost scales with window walks
~O(K) capture at ~190 ns/body ≈ 57 ms per capture at 3×10⁵ — the capture alone busts the budget
every mint). So arrivals are unattended: retention accumulates at ~47 MB/game-s until either the
byte wall (1.9 GB at ~25 game-s post-burn-start) or the 2048-scan cap (at 0.7/game-s ≈ 2,900 game-s
— the byte wall arrives first by 2 orders). Under H_A the flight dies at ~25-30 game-s of burn;
under H_B it survives. The two are not tunable into each other; the flight decides.
