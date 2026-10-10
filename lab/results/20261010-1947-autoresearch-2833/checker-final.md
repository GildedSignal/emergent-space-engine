Working...
Check complete. **`check.md` written: Grade: silver.**

**Reproduced (clean tree, patch applied from `work/patch.diff`):**
- Baseline digests match the dossier exactly (seeds 1/2/3 `971e97d7…`/`3dfe2862…`/`d9d33790…`, 6 s `293fceb4…`, `--describe` `3d04f87d…`).
- Interleaved A/B (both binaries pinned, alternating reps to cancel load drift): medians 48.1→43.6 / 47.7→46.2 / 56.7→51.6 µs = −9.4/−3.0/−8.9% (seed 2 load-noisy); per-rep floors 43.1→38.4, 46.2→38.5, 45.5→37.3 µs — the true cut is ≥ the claimed 10%.
- Tests: 104 passed / 0 failed (author recorded 74; suite grew — his count, not greenness, slipped).

**Adversarial cases (mine, beyond the author's):** seeds 4/5/7, 1 s and 6 s durations, and the full-engine 10 s `--bench` on seeds 1 and 3 (allocator + application + gather, not just the resolver) — canonical scene digests identical everywhere, `refused` 0 everywhere. Code review confirms every `Binding` site fills `proper_at_event` from a decode at the same `t` that becomes `event_time`, so the cache is definitionally the recomputed bits. The `replay_digest` change I first flagged as a mismatch is explained: it hashes `{:?}` of the record, which gained a field — not a behaviour change.

**Held out:** `predictions.md` (19:53) predates `measure.py` (19:57) and the patch (20:07); P1 held, P2 honestly measured-unmeasurable and reverted.

**Novelty:** no prior H entry or code (`git log -S` empty); distinct from the killed cross-kick memo (H0212/H0213) — this cache is per-binding, and the bench confirms `exact_hit_rate` 0.0.

**Not gold:** no 10×, deletes nothing; my full-bench frame_cpu p50 moved 0.628→0.626 ms — invisible in the frame tail today. **Missed by the author:** the same waste survives in `view.rs:264` (per-readout recompute, in the gather that is 83% of the frame) and `proper_since`; memory cost is +18 bytes/body measured, not 10; `replay_digest` necessarily false-alarms across the patch; and `decode_orbit` can turn a would-be cartesian-overflow refusal into Ok (never observed, Err→Ok only).

Tree restored clean; only `check.md` added to the run folder.
