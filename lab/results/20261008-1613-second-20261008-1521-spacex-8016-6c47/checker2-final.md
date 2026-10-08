Working...
Check complete. `check2.md` written to the run folder; nothing else touched, no commits made.

## Verdict: **Grade: gold**

**Reproduction (bit-exact).** Clean build from `bench/` (empty `work/patch.diff`, `git status` clean on crates/docs). All four digests on seeds 2–3 match both this run's records and the parent run's `heldout.txt` at commit 5579ff2 — so the jet instrumentation provably doesn't perturb the law's integers. Every recurrence/memo/bit-identity count identical; `jet 2` twice gives the same digest; sweep knot counts identical.

**Held-out.** mtime chain consistent (source 16:25:07 → predictions 16:25:36 → jet-heldout 16:25:41). Items 1, 3–7 held; the one soft miss (weak branch 98.8–99.1% vs predicted 100%) is disclosed as a miss. Kill criteria (≥5%) hit 0% everywhere, including the tuning seed ("0 of 4,367" verified).

**Adversarial cases run.** Fresh seeds 6–7 (structure holds, quantized hits 95.3/95.6%); a 3× horizon at 2,700 frames (0 re-anchors; one single-kick drift at 2.95×10⁻⁴, 2.5× below threshold); an adjacent-key probe over 15,000 smallest possible perturbations.

**The refutation chain, verified in crate source:** `Orbit::from_shape` refuses shape/key mismatch (`Error::Topology`, orbit.rs:526); `QuantizedMemo::get` returns an orbit keyed by the *re-decoded coarsened* key (orbit.rs:885) — reuse replaces the key; the digest hashes `key.periapsis` + `k` + downstream integers (universe.rs:1011). Exact reuse never occurs; coarsened reuse changes the key; the jet's own error law (floor 10⁻⁶) sits ~10 orders above digest-changing ulps while digest identity would need sub-ulp re-anchors — a compile every kick. Speedup and digest identity are mutually exclusive. Fleet never compiles (no `Orbit::compile` in fleet.rs).

**Two honest dents recorded:** prediction 3's "no rounding slack absorbs it" is overbroad (my probe: 33% of adjacent-key period increments *are* bit-equal, though quarter-period reads are 0/15,000 and the plane's drift is ~10⁵ quanta where nothing collides), and the "84–90 → 44–50 µs" bands quote seeds 2–3 only (the 1.9–2.0× ratio holds on every seed).

Gold per the lab's own clause: it shows a premise is wrong (the named gold experiment is unsatisfiable; the 20× prize is not an optimization but a law decision), and it is adoptable in one step — nothing to build.
