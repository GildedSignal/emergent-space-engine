# Predictions (written before the decisive runs)

Question: the belt's boundary event (`boundary_clock`, step.rs:725) pays a full tube walk
(`readout(t)`, the same decode class the kick pays) once per body per interval to evaluate
two certificates (doll surface, system leave edge) whose inputs — the key's periapsis and
apoapsis — are already carried by the standing entry (`universe.rs:353` computes apoapsis =
p/(2k−1); `radial.rs` ships the same apsidal invariant `[periapsis, apoapsis]` as the
conjunction filter). Hoisting the certificates to the key (a periodic key whose annulus
cannot touch either boundary at a factor-2 margin) should be bit-exact and delete the walk.

Arms: OFF (pristine path), ES_KEY_HOIST=1 (hoist), ES_KEY_HOIST=verify (walk anyway, check
the predicate against the walked r on every boundary).

Cases I did NOT tune on (held out):
1. **Cost (N=1e5 coast, 45 s, rtf 300, `--features prof`):** the shipped `item: boundary`
   stage runs ~8–14 µs/call on this Linux box (8ffc measured 12.6–13.2 µs on the M1 class);
   under the hoist I predict it falls **below 2 µs/call** (the walk is the stage's cost; what
   remains is key field access, two Scalar ops, the anchor write, and `apply`'s overhead
   inside the stage window), i.e. a ≥5× cut of the boundary stage, with `stats.boundaries`
   UNCHANGED (the item still fires; only its work collapses).
2. **Hoist coverage:** on the quiet belt (2–3 AU) and the planet-doll locals I predict
   ≥ 90% of boundaries take the hoist (margins are astronomical: periapsis ~AU against the
   star's surface; apoapsis ~AU against the leave edge). The fallback (walk) population is
   plunges, passages/unbound keys, and any body whose annulus comes within factor 2 of a
   certificate.
3. **Soundness (verify arm):** zero violations — whenever the predicate says "hoist", the
   walked r at the boundary tick satisfies `surface < r < leave`. Any violation kills the
   hoist as unsound (the residual/rounding widening of radial.rs would be the suspect).
4. **Digest parity (ladder_digest, all cases, 4 schedules each):** OFF vs HOIST digests
   **identical**, including the burn and belt-crossing cases (the hoist only skips a pure
   decode; `readout` is `&self`, and `apply`'s position walk is untouched). If any digest
   differs, the hoist is not law-neutral and is killed.
5. **The frame letter:** at N=1e5 the engine p50/p99 per frame moves little (the belt's
   boundary crest at this rtf is spread), but the worst-frame engine ms at the crest frames
   drops by roughly the boundary share of those frames (8ffc: boundaries ≈ kicks in count,
   ~1/5 of event compute); I predict max_ms drops measurably (>10%) in the crest window at
   rtf 300.

Kill criteria: any digest difference (4), any verify violation (3), or a boundary-stage cut
< 2× (1) kills the hoist. Coverage < 50% (2) demotes it to "the locals/belt only" and I
report the fallback census instead of claiming the general cut.
