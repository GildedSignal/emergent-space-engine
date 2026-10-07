Working...
All numbers verified against the regenerated data, clean build, complete run folder. The claim, one sentence:

**A pre-freeze probe of the adopted phase-neighbour certificate (gold 20261006-0346, feeding the pending `b-coorbital-cert` build) shows it is safe only if sorted by true longitude θ with a rank budget k ≈ 2.3·C (C = n·radial-spread/(τa), plus a shear-drift term): a mean-longitude or mean-anomaly sort silently drops 33–60% of real encounters under apsidal spread — including in the gold's own co-orbital corner — and "rank 4" holds only at C ≲ 1.5, with the needed rank growing ∝ n (measured 6→13→24 at n = 300→600→1200, σ_e = 1e-2), making the O(n·k) tier asymptotically O(n²·σ_e) at fixed internal eccentricity.**

Details in `lab/results/20261007-2002-taleb-9fa1/dossier.md`; probe at `crates/encounters/examples/phase_probe.rs`, reproduced by the commands in the run's README (13 s + 22 s, < 100 MB); predictions written before the decisive runs, with two honest misses that are themselves the finding.
