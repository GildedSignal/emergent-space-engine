# Predictions (written before the decisive runs, 2026-10-11)

The estimates below are derived only from repo numbers (board, law.md, H0190, r8 v2, components-98bc)
and the M1 envelope (10^10 simple ops/s, ~60 GB/s, 8 GB unified). The decisive runs are
`xtask universe --bench --rtf 100 --seconds 15 --unpaced` and `xtask galaxy --bench --ships 1e9 --tubes 1e6`,
on this shared Linux x86 box (orders of magnitude only).

## Held-out cases (not tuned on)

1. **Plane bench, events:** events_per_second in [5e2, 5e4]; per-event CPU cost 1–100 µs
   (the plane recompiles an orbit on ~99% of kicks — the memo finding — so a kick today
   should sit near the compile cost, 10–100× above a table-hit kick).
2. **Plane bench, memory:** bytes_per_body today in [40, 600] B (target tube: 16 B; program
   floor: ~0.13 bit/body). If it is above ~64 B, the plane is ≥ 4× off the B18 envelope.
3. **Galaxy scene, 1e9 ships / 1e6 tubes:** builds in < 60 s, under 1 GB RAM, at
   ≥ 10^7 ships/s instantiation; compiled cycles < 10^5 (cycle memo shared across a family).
4. **The 190-cores headline (board, bottleneck 3):** re-derivable as
   N · e · rtf / P · t_event ≈ 10^9 · 32 · 1 / 5.4e3 · ~30 µs ≈ 190 core-seconds/second.
   Prediction: the headline is consistent (within 10×) with **rtf = 1**, 32 kicks/orbit,
   hour-period bodies, ~10–30 µs per kick. At rtf = 100 it understates the need by 100×;
   with averaging (0.3/orbit) and a 100 ns kick it overstates it by ~10^4×. The headline is
   scene-conditioned, not a property of the engine.
5. **Which term breaks first at 10^9, rtf 100, belt-like population (P ≥ 1.6e8 s):**
   compute utilization ≤ 10^-3 (events/s ≈ 10^3), bandwidth idle; the binding term is
   **memory as live distinctions (scars)**: at ~10 bits per scar, the 4 GiB state budget
   holds ~3.4e9 scars ≈ 3 per body. If every body scars once per orbit, the universe's
   session is ~3 orbits long. Prediction: H_live equilibration (sub-quantum encounters not
   scarring) is what separates a bounded universe from a 3-orbit one.

## What would make the estimate wrong

- If the plane's real per-event cost is < 1 µs today (then the recompile share is already
  gone) or > 300 µs (then the bench scene is not kick-dominated and my decomposition of
  where_the_time_goes is wrong).
- If galaxy at 1e9 needs > 2 GB or > 60 s (then instantiation, not events, is the first wall).
