Working...
Everything verified and clean: worktrees removed, lab-3 tree untouched (only `lab/results/`), run folder 220 KB with patch, logs, probes, predictions (written 01:34, before every decisive run), and dossier.

**Summary of the run:**

- **Baseline re-measured on the unfixed patch** (before any fix): at β 0.9/0.99 the author's P6 scene has 52/200 members' keys silently at the unsheared doll tick — checker 2's defect, exactly; the state-made planet's readout leaves its integer word at t = 2²⁰ there (2²¹ at β 0.5).
- **The fix** (+118 lines over the original patch, applies clean to `70f27a9`): `root_offset` propagates the centre-readout refusal (was `else { break }`); `compute_key` returns `Res<Option<Tick>>` so the same-family `.ok()?` swallows propagate and `Ok(None)` means only "no next event"; a refused key lands in a per-entity `key_fault`, visible as `key_fault_of(e)`, entity unscheduled.
- **The named experiment, done**: β 0.9/0.99 → 148/200 keyed at the shear image (worst miss 0.496/0.498 ≤ 0.5 tick), 52/200 refused with recorded faults, zero silently unsheared, one history per member under every schedule.
- **The record regenerates**: β 0.5 P6 bit-identical (4447 events, offsets (−8314, 6002)); the identity control archived with the exact quoted numbers (member 1 off −110.523964, pair tied — the original run left `run.log` empty); B13 identical; B17 the same 60.0 s timeout; plane byte-identical (Moon −25); suite 57 green (author's 56 + the new test), 1 known-ignored. All five held-out predictions held.

**The claim, in one sentence:** a doll event whose root image cannot be computed (its centre's or its own readout past the integer word) is now refused loudly — a recorded per-entity fault, the entity standing unscheduled — so at β 0.9/0.99 every member's key is either its shear image to the rounding (148/200) or a recorded refusal (52/200, zero silently unsheared) while β 0.5's record, every gate and the plane stay bit-identical: a relativistic doll now orders its events correctly with no silent corner.
