Working...
All verified: space 50/50, universe 54/54 tests green, digests bit-identical on all eight scenes, instrumentation reverted, patch in `work/`.

**Claim.** On the shipped per-kick path, deleting `TubeEvent::bind`'s redundant state reconstruction (the exact event state the caller already holds) plus word-width divisions in `fast_quad` cuts ns/kick by 6–19% across eight scenes with bit-identical tube streams — and the same measurement prices the kernel at ~1.2× its per-node arithmetic floor (cos 44 ns + shape 44 ns + divisions 51 ns per node), showing that further ≥2× gains at bit-identity are not in the kernel: the lever for ns/event is nodes per kick (shape-table reuse across kicks), a law-level decision.
