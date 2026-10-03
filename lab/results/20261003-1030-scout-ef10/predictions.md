# Predictions — 20261003-1030-scout-ef10 (written BEFORE the decisive sweep)

Tuning so far (allowed, not held out): e=0.2 cases, both masses, orders 3/5/7/11, n∈{4,8,16}.
Held out below: e=0.6 in the sweep grid was never run; e=0.4 and e=0.85 never run; the
corrupt3 control never run. The oracle (n=128, order 5) is the reference for `prec`.

System: test particle, primary M=1, secondary m2 ∈ {0.3, 0.01} on a prescribed circular
orbit a_out=4.5 (P_out/P_in ≈ 8.37). WH DKD map: exact universal-variable Kepler drift +
tidal kicks (direct+indirect). Gates: prec_rel ≤ 1% (B1 flavour) AND max relative Jacobi
error ≤ 1e-4 (B12 flavour), over 600 orbits, output each orbit.

- P1 (binding gate): precession passes (≤1% of oracle) for every config at n≥4; the
  binding gate is always dCJ. The plain map's precession bias is tiny because outputs are
  phase-locked near periapsis.
- P2 (the savings, m2=0.3): plain needs n*=32 to pass dCJ≤1e-4 (1.9e-4 at n=16 fails);
  best corrector passes at n*=16 → savings 2x. e=0.6 same or slightly higher demand.
- P3 (the savings, m2=0.01): plain n*=8 (3.5e-5 passes; 3.1e-4 at n=4 fails); best
  corrector n*=8 at e=0.2 (order-7 at n=4 is 2.0e-4, fails) → savings 1x at e=0.2,
  possibly 2x at e=0.6.
- P4 (fixed-n reduction): at n=8, correctors cut dCJ 5–8x vs plain (both masses);
  orders 5,7,11 within 2x of each other (saturation at coarse steps).
- P5 (high-e held out, e=0.85): pericentre tides dominate; plain needs n≥32; corrector
  gain shrinks to ≤2x; fit residual grows far above the e=0.2 value (0.15 rad).
  No encroachment on the secondary (min separation 2.65 > its Hill sphere), so no
  encounter/instability blow-up: gates still pass eventually at high n.
- P6 (controls): corrupt3 (wrong inv sign) is worse than plain at every (n,e,m2);
  it must fail wherever plain fails and also at some points where plain passes.
- P7 (error type): dCJ stays bounded (oscillation, no secular walk) for plain and
  corrected at n≥8 over 600 orbits: dCJ_last < dCJ_max, both ≪ orbit-count × anything.

If P2/P3 come in at 2x or less, the dossier grades itself silver: real, cheap, adoptable,
but not a 10x bottleneck move in the coarse-step regime the engine cares about.
