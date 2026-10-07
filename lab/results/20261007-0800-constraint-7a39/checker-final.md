Working...
Check complete. `check.md` written; tree restored to main (only `check.md` added to the run folder).

**Grade: silver.**

What I did and found:

- **Reproduced the core**: applied `patch.diff` to a clean tree. Wire-byte identity test passes; digests identical on seed 1, on my held-out seed 7, and on m480; `view_json` p50 0.216→0.0007 ms (share 16%→0.07%; m480 50%→0.3%); engine 4–5% of frame, confirming the premise correction.
- **Refuted the headline**: the 4.6× frame-p50 cut doesn't survive a matched side-by-side (mine: 1.05→0.81 ms, 1.3×). The author's baseline was uniformly ~3× slower *including the engine* — machine state, not allocator pollution; my gather is unchanged (0.709→0.707 ms), contradicting the dossier's "tree churn charged to the gather" story.
- **Found an undisclosed regression**: the patch deletes `Session::step`'s `u.input` call — proven live that six `keys=1` POSTs leave `keys:0`, no burn. The player cannot steer; the digest-blind bench hid it. Five-line fix, but not adoptable as shipped.
- **Predictions discipline held** (mtime 08:08:48 vs decisive runs 08:14:24); behave-gate host anomaly reproduced and correctly not adjudicated; novelty clean (`60d8b54` only split the dashboard timings).

Gold path: re-add input, re-measure interleaved A/B, one live steering check.
