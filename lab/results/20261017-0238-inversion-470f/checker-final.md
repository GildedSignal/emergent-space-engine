Check complCheck complete. **Grade: gold** — written to `lab/results/20261017-0238-inversion-470f/check.md`, with two in-place corrections to the author's wiki page.

**What I did:**
- **Reproduced**: tree at base `3dc6f62`, probe = print-only + counting `GlobalAlloc`. The runner's regen itself flipped the arms — regenerated 40k flat (44.4 MB) while regenerated r1 **and** r4 grew (live 40→100 MB, 45→105 MB over 6,000 gs): one binary, both shapes, three independent sessions.
- **Verified the preserved instance** number by number: 220,862,318 B / 83,768 allocs at gs 20,000, ~78k-frees bulk drop to 16.1 MB, hwm 206,976 kB retained, all shipped counters flat, heap-tracking and constant mapping count confirmed.
- **Attacked beyond the author's range**: 9 flights under 9-way concurrent load — **9/9 grew** (seeds 1 and 5; N=100 at ~3.9 kB/gs, N=800 at ~29.4 kB/gs to 183 MB by 6,000 gs); 3 flights run alone — 0/3 grew; flat path stable to 60,000 gs. Load/debt is the knob (every flight below ~129M presented ticks grew), not the claimed ~33% coin. Instrument artifact ruled out.
- **Predictions**: pre-registered (timestamps consistent); P2/P4/P5 held, P3's pre-registered failure branch honestly reported.
- **Novelty**: d3fe's standing silver rate is dead on main at 4–7× horizon; 4fa8's unflown arm refuted; the wall-path bimodality appears nowhere else (allocator-ratchet is a different mechanism).

**Numbers that differ** (recorded in check.md): long-run growth is 9.0 kB/gs (the ~11 is the first-6,000-gs window); "~33%" is a quiet-machine artifact; "516 B/body" is a typo for 516 kB/body.

**Page corrections**: frequency marked load-dependent with my counts, 400-member framing extended to N=100/800 (attributed `[checker]`), checker line appended to Runs. My scratch outputs are in `/tmp/checker-470f/`; no commits made.
