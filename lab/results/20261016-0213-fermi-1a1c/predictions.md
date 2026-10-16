# Predictions — 20261016-0213-fermi-1a1c (Fermi lens)

Written BEFORE the flights, from the wiki's constants and the doll-cadence law
(2^7 kicks per Cinder period of 88 d = 7.60e6 game-s => 1.68e-5 kicks/body/game-s),
before any of my own numbers existed. Machine: shared Linux 8 vCPU (i7-4790), orders
of magnitude only; the M1 anchors come from artifacts/runs/nladder/ladder.txt (after2).

P1 (short arms, N=10^3/10^4/10^5 coast, 20 s, budget 12 ms): B/body 2.3–2.8 kB flat
   in N; build 20–50 µs/body; engine p50 coast < 0.15 ms, flat in N (the frame-walk
   fix 0f112b89 holds on Linux too).

P2 (the wave, N=10^5 coast, budget-free, ~160 s wall at rtf 100): the belt's first
   kicks land in one window ~13.0–14.6 k game-s wide ~1.5 k (N-independent); events
   per frame inside the window max 300–450; the frames that carry the wave cost
   20–40 µs per event, so the wave alone crosses the 12 ms frame at N ≈ 2–5×10^5
   (the M1 measured edge is 3×10^5, after2: 1 frame over, max 12.0 ms).

P3 (the wave, N=10^4, same window): max events/frame 25–45 (linear in N), no frame
   over 12 ms anywhere in a budget-free flight.

P4 (composition, checked against the wiki's cf45/ed3a): the doll-law rate
   1.68e-5 kicks/b/game-s UNDER-counts the measured steady plateau (ed3a: ~25
   events/game-s at 3×10^5 = 8.3e-5/b/game-s, boundaries included) by ~4–5×; so the
   steady stream at 10^9, rtf 100, shipped ~30 µs/event, is 50–250 cores — bracketing
   cf45's composed "148× the 0.72-core frame budget" — and fits one core only at the
   b29a key-arm cost (~0.11 µs/event).

P5 (kill criterion): if my measured wave cost is < 10 µs/event (events much cheaper
   than the M1's 29 µs), the wave break-N moves past 10^6, the first breaker becomes
   standing memory, and the dossier must re-rank with the M1 constant instead.
