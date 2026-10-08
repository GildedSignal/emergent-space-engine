Working...
Check complete. `check.md` written; tree restored; nothing else in the run folder touched.

**Grade: lead** — reproduced exactly, central claim falsified.

What I did:
1. **Reproduction (exact).** Applied `work/patch.diff`, rebuilt, ran the dossier's three commands: digests, bodies, bytes/body and every probe counter identical to the author's JSONs. Ran uninstrumented baselines too — digest neutrality holds at **rtf 1, 10 and 100** (the author verified only 100), and the 192 B `Segment` size regenerates (the saved JSONs lacked the `bytes` field — artifacts predated the patch's last addition).
2. **The falsification.** The probe counts `retire` *appends* — monotone by construction, blind to removal. The shipped plane prunes history every 64 frames (`Universe::prune`, universe.rs:870/967, horizon `2·light_distance + 2²⁶` ≈ 331 gs). All three author points sit inside that horizon. At 2000/2999/5499 gs: totals flat at ≈365 KB while retirements triple (1017→1841); closure check — 1841×192 B of segments alone would overrun the total. The 4 B/body/gs slope was scene-age transient; "8 GB fills in ~2 gs at 10⁹" is dead. The kill test was one `--seconds 55` flag (4 s wall) the author never ran, despite naming this exact hinge in "what would make it wrong".
3. **Other adversarial checks.** Seed 2: rates robust (91.1% recompile, 0.047 events/body/gs, catalogue equilibrium). Probe off-by-one: `emitted_quanta()` drops bucket 18 (876 of 1472 quanta), though "every quantum ≥2⁸" survives since all readable sub-255 buckets are empty. `events_per_second` wall-based claim verified arithmetically.
4. **Novelty.** Recompile ~99% already known (5 Oct taste log); the proposed H_live definition already in plane.md:36 — *including* the "minus reabsorption" term the probe missed. New: the first distinction-rate numbers behind HANDOFF risk #2 — real, but modest, and the premise the dossier claimed to flip is refuted by the shipped code.

The salvage for the next run is recorded in check.md: measure the standing footprint (~4.8–5.2 KB/body flat → ~5 TB at 10⁹), which reframes risk #2 as a constant-cost problem, not a growth-rate one.
