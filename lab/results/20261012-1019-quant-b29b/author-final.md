Working...
The run is complete: predictions pre-registered, ladder measured (N = 12 → 120,000), reproduction command verified, dossier and probe written to `lab/results/20261012-1019-quant-b29b/`.

**Claim:** the plane's frame budget bounds events but not the schedule — `Universe::advance`'s unconditional `rekey` plus the defer/requeue drain is an unbudgeted Θ(N log N) fixed tier that already costs 38 % of a 16.7 ms frame at 12,000 root entities and 133 ms (8× the whole frame) at 120,000 with zero events resolved, capping the frame at N ≈ 1.5–6×10⁴ entities (five orders below 10⁹) unless deadlines become lazy or bodies collapse into fewer queue entities.
