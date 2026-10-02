# predictions.md (written before the full-scene decisive run)

Controls already run (machinery): static-frame Riemann check exact; tetrad constraints 4e-15;
oracle pair-difference tide matches the einsum's axis rotation; member ICs refit from the
reconstruction (the U=u construction carries a co-rotating drift n|x|, measured and absorbed).
Kernel table measured so far (r=6, r=3.1 circular): naive kernel differs from oracle tide by
2.3x (r=6) and 21.9x (r=3.1); einsum-projected tensor matches the axis but is short on the
radial eigenvalue by ~1.56x (r=6) and ~3.9x (r=3.1).

Predictions for the decisive run (full scene set, not yet run):

P1 (validity domain). With any kernel that matches the oracle tide's axis rotation, member
error at the phase-1 extent rule (x/Rcurv = 0.018, i.e. r_p/32) stays below 2% of current
separation up to the tau10 horizon, at every radius including r=3.1M and the eccentric
r_p=6.5M scene: the linear-tide frame does not break by extent anywhere. Held-out: the exact
numbers at r=3.1 and the eccentric scene.

P2 (naive kernel). L2 (phase-1's Newtonian-form kernel with a relativistic readout) exceeds
10% member error within the tau10 horizon for every scene with r <= 20M, and stays under 2%
at r=1000M. Held-out: the crossing radius (I predict between 20M and 100M, since the kernel
error at r=1000 is not measurable at print precision).

P3 (averaged kernel). L3 (median eigenvalues + linear axis-rate fit) stays within 1.3x of L1's
error on circular scenes (it is exact for them by construction) and exceeds 3x L1's error on
the eccentric scene (the periapsis eigenvalue spike is dropped). Held-out: the eccentric ratio.

P4 (battle lifetime, "a large fraction of an orbit"). The tau10 horizon (separation x10) is
under 0.35 of an orbit for every circular scene regardless of radius (shear is scale-free in
the Newtonian limit); GR strong-field corrections shorten it further at r=3.1 (predict
tau10/T < 0.25 there). No battle lasts a large fraction of an orbit: the frame's dissolution
by shear is physics, not representation failure.

P5 (epoch cost). Under the axis-turn rule (2^-8 rad per epoch), epochs per orbit from the
TRUE tensor axis rate are within 2x of phase-1's measured 1600-3200 at all radii (the axis
does rotate at order n); the epoch count concentrates at periapsis on the eccentric scene
(predict: > 60% of epochs in the 20% of the orbit nearest periapsis).

P6 (plunge). The plunge scene's origin crosses r=2.05M; the tau at which Rcurv(tau) falls
below the extent rule is derivable from the compiled tube alone (r(tau) readout), so the
dissolution tick is compile-time knowledge, zero surprise cost. Held-out: how much of the
plunge scene the members survive before reconstruction fails.

P7 (the einsum kernel discrepancy). The radial-eigenvalue shortfall of the einsum-projected
tensor (1.56x at r=6) shows up as L1 member error growing roughly linearly with the axis
turn (a wrong-amplitude tide mispumps the epicycle); I predict L1 err_max in [5%, 40%] at
r=6 within tau10, i.e. the projected-tensor formula needs fixing before E9 freezes, but its
axis structure is right.
