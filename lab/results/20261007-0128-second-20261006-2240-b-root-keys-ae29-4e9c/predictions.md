# Predictions (written before the fix and the decisive runs; only the baseline probe has run)

The change: the second checker's named experiment. `Ctx::root_offset`'s silent `else { break }` on a
centre-readout refusal becomes a propagated `Refused`; `Universe::compute_key` returns
`Res<Option<Tick>>` (the same-family `.ok()?` swallows — the body's own readout, the handout's words,
the fleet's origin — propagate too); a refused key is held in a per-entity `key_fault` beside
`root_key`, visible as `key_fault_of(e)`, and the entity is not scheduled — never silently keyed at
the unsheared doll tick, never conflated with "no next event".

Measured baseline (probe, unmodified patch, before any fix): β 0.5 — 200/200 members readable, worst
image miss 0.500; β 0.9 and 0.99 — 148/200 readable, **52/200 keys silently at the unsheared doll
tick** (the centre's readout refuses first at t = 2²⁰ there, at 2²¹ for β 0.5; the blind members'
first kicks sit past the boundary).

## Held out (not tuned on)

1. **The named experiment (β 0.9 and 0.99, the author's scene at 200 members):** every member's
   next-event key is **either** the shear image recomputed in floats to ≤ 0.5 tick (where the
   centre's readout works) **or** `horizon_of == None` with a recorded `key_fault`; exactly the
   oracle-blind members are the refused ones (52 of 200 at each β — the baseline count), and **no**
   member's key sits silently at its doll tick where the oracle is blind. The readable members'
   whole histories stay identical under 1 and 4 threads and both make orders, and they step
   (events > 148).
2. **β 0.5 P6 unchanged:** worst image miss 0.500, key offsets (−8314, 6002), 4447 events per
   schedule — bit-identical to the author's `p6-out.txt` (no β 0.5 scene reaches a refusal path, so
   the fix is inert there).
3. **The identity-key control** (`root_offset` forced to `Ok(0)`): both P6 tests fail with member 1
   off about −110.52 and the pair tied at 16,384 — the falsifiability control, archived this time
   (the original run left `run.log` empty).
4. **Gates and suite:** no gate, plane or suite scene reaches a key refusal (every doll centre is a
   bound-orbit body whose readout is unbounded), so B13's detail line stays identical (60/64, worst
   ΔE/ΔL 2.12e-2, the same 9 replaced draws), the suite stays green, and the plane example prints
   Moon −25, Skimmer +1, others 0, battle tick 5,000,000 — byte-identical to the author's log.
   Held-out risk I accept: a suite body whose **own** next-event readout leaves its word would have
   been silently dropped by the patched version inside a self-consistent digest; the loud refusal
   would expose it as a stuck entity and move that digest. That would be a finding to report, not a
   failure of the fix.
5. **B17** still FAILs by timeout near 60 s on this box both ways (it cannot be exercised here; the
   M1 re-measures, per the lab rules).
