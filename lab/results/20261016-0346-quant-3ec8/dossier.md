# Dossier — 20261016-0346-quant-3ec8 (Quant)

**Claim.** `plan_clock` reads the body's own synchronised state up to three times per plan (the
birth's `pt_exp` read, the projection's `readout`, the drift fit's `readout`); serving all three
from **one** `readout` cuts the birth pass **6.05–7.43 µs/body (18.2–22.2%)** and the whole birth
rail **42.4–43.7 → 35.8–37.4 µs/body (−14.5%)**, with the universe digest **byte-identical** at
every (N, seed) flown and the OFF arm digest-identical to pristine main.

**Bottleneck.** Board #1: bodies in the flyable engine (10⁶ vs 10⁹). The birth pass
(`Universe::start`'s tick-0 replan+apply) is 76–78% of the 42–44 µs/body birth rail (404b) and
~6 of the ~8 M1-core-hours of a 10⁹ fill. This is d31c's named next rung ("one readout serves
`plan_clock`'s two `readout` calls"), the top item of nladder's open directions after the shared
planets readout. Not a 10×: the readouts were ~20% of the pass, and this deletes the redundant
two-thirds of them. It composes with d31c's shared planets readout (disjoint terms: d31c unified
the *secondaries* read; this unifies the body's *own-state* reads).

**Evidence** (this box: the lab's Linux i7-4790, 8 vCPU; orders of magnitude per the lab rules;
`ab.jsonl`, 18 flights, arms interleaved A/B in one binary via `ES_ONE_READ`):

| N | seed | pass off µs/B | pass on µs/B | cut | build off→on µs/B |
|---|---|---|---|---|---|
| 10⁴ | 1 | 33.14 | 26.54 | 6.60 (19.9%) | 43.5→37.4 |
| 10⁴ | 7 | 32.13 | 25.71 | 6.42 (20.0%) | 42.5→36.3 |
| 3×10⁴ | 1 | 32.34 | 25.83 | 6.51 (20.1%) | 42.4→35.8 |
| 3×10⁴ | 7 | 32.51 | 25.77 | 6.74 (20.7%) | 42.6→35.8 |
| 10⁵ | 1 | 33.47 | 26.04 | 7.43 (22.2%) | 43.5→36.5 |
| 10⁵ | 7 | 32.54 | 26.34 | 6.20 (19.0%) | 42.7→36.4 |
| 3×10⁵ | 1 | 33.38 | 26.43 | 6.95 (20.8%) | 43.7→36.5 |
| 3×10⁵ | 7 | 33.23 | 27.18 | 6.05 (18.2%) | 43.3→37.3 |

- Digests byte-identical between arms at all 8 configs (8 distinct digests across configs —
  deterministic); peak RSS identical to ±0.05% (672 MB at 3×10⁵, under the 2 GB budget).
- **Pristine ≡ OFF**: a binary built from unpatched main (same bench file) digests `3c02e035…`
  (10⁴ s1) and `6338ec25…` (3×10⁵ s7) — equal to the OFF arm's. The OFF path is shipped verbatim.
- Anchors reproduced on this box: shipped pass 32.1–33.5 µs/body (d31c: 32.8–33.9); build rail
  42.4–43.7 (404b: 42–44); requeue+rekey ≤ 0.099 µs/body (404b: ≤ 0.1).
- Mechanism: only doll-0 ships (`on_clock()`) plan through `plan_clock` — the belt, the 12
  haulers, the player; the ~300 locals and the plane's doll≠0 ships use `plan_interval` and are
  untouched (their share dilutes the whole-pass cut; on belt bodies alone the cut is ~2 readouts
  ≈ 6.8–7.6 µs). A `readout` is the tube walk (pure: `Binding::readout`, bind.rs:160), the same
  ~3.2–3.7 µs/channel object b8fc priced at 4.0–5.4 µs on the plane mix.
- Suite: `cargo test --release -p emergent-universe` green with the patch in (result in
  `tests.txt`).

**Reproduce** (≤ 15 min): `bash lab/results/20261016-0346-quant-3ec8/regen.sh` — applies
`work/patch.diff` if needed, builds (main + pristine), flies the matrix, prints the table rows
and the digest equalities.

**Predictions** (`predictions.md`, written before the decisive run): P1 identity — **held**
(8/8 configs). P2 cut 6–8 µs/body, whole-pass −15–22% — **held** (6.05–7.43, 18.2–22.2%). P3
flat in N and held-out seed 7 within ±15% — **held** (all cuts inside 6.05–7.43, spread ±10%
around ~6.6). P4 requeue/rekey ≤ 0.1 µs/body, locals untouched — **held** (0.099 max; digest
identity implies the untouched terms produce identical state).

- Suite: `cargo test --release -p emergent-universe --lib --bins --tests` green with the patch
  in (`tests.txt`). Note: `cargo test -p emergent-universe` **cannot** build on Linux as shipped
  — `examples/nladder.rs:26` links `proc_pid_rusage` (a macOS libproc symbol) — a pre-existing
  platform break in the integrator's N-ladder example, not this patch (untouched files; the
  link error is in the example alone).

**What would make it wrong.** The exactness rests on `readout(t)` being pure and nothing moving
the binding between the three reads — both checked in code (bind.rs:160; between the reads only
`ext::constants` (reads other bodies) and `self.rec.ext` writes happen), and the digest equality
is the direct test at every config flown. Not flown: in-flight re-plans (handoffs, decisions)
and the thrusting path — `kick_clock`'s post-burn `project(t)` (line ~698) still reads once more
per thrusting kick (its state *was* mutated by the kick, so it cannot share `plan_clock`'s read;
the honest hoist there needs the post-rebind state, a separate rung). A digest at a canonical
cut *after* flight (not just tick 0) would close that; the tick-0 digest is what `start` leaves.

**Cost of adopting.** ~15 lines in `step.rs` (`project` split into `project` + `project_at`;
`plan_clock` reads once and passes `&st`), no API change, default arm = shipped verbatim (the
`ES_ONE_READ` gate can be deleted on adoption: the ON path is the proposal). PRINCIPLES #1
("The cheapest compute is compute not done. Delete before optimizing") and #16 (cheapest
arithmetic) — this is deletion of a repeated pure computation, not a new approximation; #2
exactness untouched (integers decide: the digest).

**The lens (what Quant may have missed).** An HFT eye prices redundant reads immediately but
underweights law-surface risk: `plan_clock` is on the clock law's critical path, and the reuse
is only safe because `readout` is pure *today* — if a future change makes `readout` memoize or
mutate, the silent sharing becomes a bug. The comment in the patch says so. Also missed by
construction: per-readout variance (I report per-config means over interleaved arms, not p99 of
individual readouts — the cut is a difference of large counts, so tail noise mostly cancels).
