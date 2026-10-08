Working...
Run complete. Predictions were written before the decisive runs (held: 5 of 6; the sixth failed informatively), the record regenerates from `work/patch.diff` + one command, and the universe digest matches the shipped bench's.

**Claim:** on the shipped plane one kick costs ~97 µs median of which 63% is a fresh Darwin compile nobody needs (the physics is 9%), the already-shipped reuse path `Orbit::from_shape` costs 0.46 µs (133× less) but covers only 1.5% of kicks trivially — because the exact shape key changes on 98.5% of kicks while every body stays in one quantized (E,L) cell for its whole sampled life — so the law's unbuilt derivative-offset jet is worth a measured ~4.4× per kick engine-wide, and the cheap shape-reuse version of it is dead.
