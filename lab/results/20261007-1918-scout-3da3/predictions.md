# Predictions (written before the decisive run, 2026-10-07)

Cases below were NOT tuned on (the smoke runs touched N=10^3 and 10^6 at eps=1e-6
totals only; everything else is held out).

1. **Total far-field news traffic is independent of N at fixed profile** (stars
   fixed at 1024, ships 10^3..10^6 at fixed total mass): fitted exponent of
   total_rate vs N within +-0.05 of 0.0. Star share > 0.9 everywhere.
2. **Per-body news at the goal scale** (N=10^6): ratio to the body's own kick
   cost (nu=8/orbit) < 0.05. But at N=10^3 the same ratio is > 1 (news-dominated
   small universes) — the crossover sits near N ~ 10^4.
3. **Quantum sweep** (eps = 1e-4, 1e-6, 1e-8 at N=10^6): traffic grows as
   1/eps^2 while below the granularity cap, then flattens once most shells
   saturate at one news per source orbit; I expect a factor ~10^2..10^4 rise to
   1e-8 and NOT the full 10^8 (cap binds for the inner shells).
4. **Memory**: sliding-window (MVCC/GVT) live events at N=10^6, eps=1e-6 <
   10^3 events (< 10 KB); naive pairwise append after one 44-Myr unit > 10^12
   events (> 10 TB). The ratio is the answer to OC#50.
5. **Cascade controls**: a 1-sigma star kick's news arrives spread over ~galaxy
   crossing times (peak < 5e4 per unit time); a 100x kick (a struck star)
   compresses arrivals into < 0.05 units with peak ~ 10^5..10^6 per unit time —
   a spike of bounded area (~the number of consumer cells), not a herd that
   grows with N.

**Kill criteria** (pre-registered): if (1) the exponent exceeds 0.2, or (2) at
N=10^6 the per-body ratio exceeds 1 (news costs more than the kicks it
replaces), the candidate representation is dead as the answer to OC#50 and the
wall is real at the news representation. If (4) sliding memory exceeds 10^8
events, adoption inside 4 GiB fails on its own terms.
