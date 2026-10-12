# Kerr compiler review receipt

Base a838a284a27a6813434362cc2adfde946d2085db; branch wt/cx-b-kerr-compiler. No merge or commit.

Integer signed-spin Kerr cycles, fate classification, clocks, frame dragging, Penrose splits, photons, windowed passages and plunges. Shared cycles are indexed by the unchanged 16-byte Tube. A doll stores one spin. Spin and constants in compiled generators are immutable.

59 tests passed; nine new tests cover direct Hamiltonian vectors, Boyer–Lindquist metric/invariants, direct windowed integration, critical capture, ISCO, negative energy, spin reflection/Lense–Thirring, memo identity, observation purity and zero-spin bit identity. Each test binary finished within 0.46 s. No frozen judge, threshold or previous evidence changed.

Integration limit: the native Kerr catalogue is additive; the game motion resolver and Kerr Fermi tides are not integrated. Horizon/infinity arrival clocks are deliberately absent. Full exponent-range Kerr weak-field qualification is not claimed.

The first probe exposed an atan argument outside its documented range. The second passed B19 criteria 2–6 but refused some strong prograde cycles because the other quadratic root was negative. Algebraic positive-root selection fixed it; small-spin discriminants are factored before evaluation. Failed logs are retained beside this receipt.

## Exact before and after gate lines

### before

```text
G1 PASS advance per cycle: 256/256 within 1e-2, worst 6.60e-4 [0.06 s]
G2 PASS radial periods: 256/256 within 1e-3, worst 5.50e-4 [0.06 s]
G3 PASS deflection: 64/64 within 1e-2, worst 6.40e-12 [0.01 s]
G4 PASS capture: 0 of 10 misclassified [] [0.00 s]
G5 PASS long run: 32/32 seeds over 10000 cycles (0 short), worst growth E 0.000 L 0.000 (limit 0.2), worst shape drift 0.00e0 (limit 1e-2) [0.12 s]
G6 PASS prograde: 256/256 advances positive [0.00 s]
B16 PASS moving lenses: 256/256 judged seeds within 1e-2 of the boosted Kerr-Schild geodesic (head-on 64/64, transverse 64/64, oblique 128/128), worst 3.14e-8, beta up to 0.90; oracle converged on 256 of 256 (its two runs agree to 2.1e-8, needs 1e-6) [0.05 s]
B19 FAIL rotating holes: [1 FAIL] cycles (1536 orbits: chi 0.5/0.9/0.998 x prograde/retrograde x 256, p from 1.1x the separatrix to 1000, e < 0.7): advance within 1e-2 in 0/6 cells pass, failing (cell, seeds ok of 256): ["0.5+ 0", "0.5- 0", "0.9+ 0", "0.9- 0", "0.998+ 0", "0.998- 0"] (fewest ok 0, worst inf), periods within 1e-3 in 0/6 cells pass, failing (cell, seeds ok of 256): ["0.5+ 0", "0.5- 0", "0.9+ 0", "0.9- 0", "0.998+ 0", "0.998- 0"] (fewest ok 0, worst inf); oracle converged to 8.3e-16; [2 FAIL] fates, exactly as the oracle (0/1680): circular 0/48, E=1 capture 0/24, bound/plunge 0/48, photons 0/24, dense capture 0/1536; first misclassified ["0.5+ r=3.2901", "0.5+ r=4.0444", "0.5+ r=4.1953", "0.5+ r=4.2707", "0.5+ r=4.4216", "0.5+ r=5.1759"]; [3 FAIL] frame dragging: 379 tubes inside the ergosphere, answered 0, dphi/dt > 0 in 0, rates within 1e-6 in 0 (worst inf); outside it static 0/96 and ZAMO 0/96 clocks within 1e-12 (worst inf); no static clock inside 0/48; [4 FAIL] Penrose: negative-energy tubes answered 0/85 inside the ergosphere, refused 0/73 forged outside it; splits inside: conserved 0/27, energy gained 0/27, equal to the oracle within 1e-6 0/27 (canonical []); outside: no gain, conserved and right 0/27; [5 FAIL] light (384 impacts, |b| from 1.05 b_c to 300, both senses): deflection within 1e-2 in 0/6 cells pass, failing (cell, seeds ok of 64): ["0.5+ 0", "0.5- 0", "0.9+ 0", "0.9- 0", "0.998+ 0", "0.998- 0"] (fewest ok 0, worst inf); [6 FAIL] chi = 0: 170 answers, the law's Schwarzschild digest 59d54de0f9ead66f, its Kerr(0) digest prograde c7ee2b6319a52a25 retrograde c7ee2b6319a52a25 (first difference: cycle p=378.146 e=0.253) (170 unanswered); oracle against mpmath: 285 values, worst relative difference 2.2e-13 (the thresholds above are 1e-2, 1e-3, 1e-6 and 1e-12) [0.07 s]
```

### after

```text
G1 PASS advance per cycle: 256/256 within 1e-2, worst 6.60e-4 [0.04 s]
G2 PASS radial periods: 256/256 within 1e-3, worst 5.50e-4 [0.04 s]
G3 PASS deflection: 64/64 within 1e-2, worst 6.40e-12 [0.01 s]
G4 PASS capture: 0 of 10 misclassified [] [0.00 s]
G5 PASS long run: 32/32 seeds over 10000 cycles (0 short), worst growth E 0.000 L 0.000 (limit 0.2), worst shape drift 0.00e0 (limit 1e-2) [0.11 s]
G6 PASS prograde: 256/256 advances positive [0.00 s]
B16 PASS moving lenses: 256/256 judged seeds within 1e-2 of the boosted Kerr-Schild geodesic (head-on 64/64, transverse 64/64, oblique 128/128), worst 3.14e-8, beta up to 0.90; oracle converged on 256 of 256 (its two runs agree to 2.1e-8, needs 1e-6) [0.05 s]
B19 PASS rotating holes: [1 PASS] cycles (1536 orbits: chi 0.5/0.9/0.998 x prograde/retrograde x 256, p from 1.1x the separatrix to 1000, e < 0.7): advance within 1e-2 in 6/6 cells pass (fewest ok 256, worst 1.2e-12), periods within 1e-3 in 6/6 cells pass (fewest ok 256, worst 1.5e-11); oracle converged to 8.3e-16; [2 PASS] fates, exactly as the oracle (1680/1680): circular 48/48, E=1 capture 24/24, bound/plunge 48/48, photons 24/24, dense capture 1536/1536; [3 PASS] frame dragging: 379 tubes inside the ergosphere, answered 379, dphi/dt > 0 in 379, rates within 1e-6 in 379 (worst 1.4e-14); outside it static 96/96 and ZAMO 96/96 clocks within 1e-12 (worst 1.9e-16); no static clock inside 48/48; [4 PASS] Penrose: negative-energy tubes answered 85/85 inside the ergosphere, refused 73/73 forged outside it; splits inside: conserved 27/27, energy gained 27/27, equal to the oracle within 1e-6 27/27 (canonical ["chi=0.5 r=1.933 v=0.6: E_out +0.4196 for E_in +0.3989", "chi=0.9 r=1.718 v=0.6: E_out +0.7461 for E_in +0.6911", "chi=0.998 r=1.532 v=0.6: E_out +0.8498 for E_in +0.7599"]); outside: no gain, conserved and right 27/27; [5 PASS] light (384 impacts, |b| from 1.05 b_c to 300, both senses): deflection within 1e-2 in 6/6 cells pass (fewest ok 64, worst 4.4e-11); [6 PASS] chi = 0: 170 answers, the law's Schwarzschild digest 59d54de0f9ead66f, its Kerr(0) digest prograde 59d54de0f9ead66f retrograde 59d54de0f9ead66f; oracle against mpmath: 285 values, worst relative difference 2.2e-13 (the thresholds above are 1e-2, 1e-3, 1e-6 and 1e-12) [0.21 s]
```

Sampled per-process RSS peaks (100 ms sampling; 2 GiB kill guard): tests 193040 KiB; release build and gates 451792 KiB. Machine thermal/power/load/swap records are in both gate logs.
