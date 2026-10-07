# Root-clock event keys: the silent high-β fallback made loud (second author on 20261006-2240-b)

## Claim

The named experiment is done: a doll event whose root image cannot be computed — the centre's (or the
entity's own) committed readout past its integer word — is now **refused loudly** (a per-entity
`key_fault`, the entity standing unscheduled), never silently keyed at the unsheared doll tick and
never conflated with "no next event"; at β 0.9 and 0.99 every member's key is either its shear image
to ≤ 0.5 tick (148/200) or a recorded refusal (52/200, the exact baseline count), β 0.5's P6 record is
bit-identical, the falsifiability control fails with the author's numbers (−110.523964, the pair
tied), and every gate holds where this box can exercise it — so the original claim ("a relativistic
doll orders its events correctly") now holds without a silent corner.

## Bottleneck

The same as the original run's (HANDOFF's "simultaneity across dolls", law.md's Open): root-clock
event keys. This run removes the defect the second checker found in the corner the feature exists
for: at β ≥ 0.9 the passage-centred doll's own scene made 52/200 members' keys silently revert to
the old wrong convention. No compute gain; what it deletes is a silent failure mode — principle 13's
"basically we don't want errors that can compound" and the law's own rule that every refusal is
recorded.

## Evidence

Machine: the lab's Linux box (8 vCPU, 15 GB, shared; `machine_state` lines in the gate logs),
release builds, worktree of main `70f27a9` + `work/patch.diff` (the original patch plus this fix;
applies clean to main). Every command ≤ 60 s except the suite and B17, noted.

**The baseline defect, re-measured before the fix** (`work/probe-baseline.txt`, source
`work/rootkeys_probe.rs`): the author's P6 scene parameterized by β — β 0.5: 200/200 readable, worst
image miss 0.500; β 0.9 and 0.99: 148/200 readable, **52/200 keys silently at the unsheared doll
tick**. The readout boundary (`work/refusal_domain.rs`): the state-made planet's committed readout
first refuses at t = 2²¹ root ticks (β 0.5) and 2²⁰ (β 0.9/0.99) — "state outside the integer word",
the law's established refusal (bind.rs) — and the 52 members' first kicks sit past it.

**The fix** (`work/patch.diff` against the original, +118 lines): `Ctx::root_offset` propagates the
centre-readout refusal instead of `else { break }`; `Universe::compute_key` returns
`Res<Option<Tick>>` — every read the image needs (the body's own tube, a handout's words, the fleet
origin's state, each chain centre) propagates, and `Ok(None)` means only "no next event"; a refused
key lands in `key_fault` beside `root_key`, visible as `key_fault_of(e)`, and the entity stands
unscheduled.

**The named experiment** (`cargo test --release -p emergent-universe --test rootkeys`,
`work/p6-out.txt`, ~3 s): the new test runs β 0.9 and 0.99 at 200 members under 1 and 4 threads and both
make orders — every member's key is either the float-recomputed shear image to ≤ 0.5 tick (148, worst
miss 0.496/0.498) or `horizon_of == None` with a recorded fault (52, the exact baseline count); no
member is keyed at its doll tick where the centre is unreadable; the readable members step (943/928
events) and every member's whole history is the same record under every schedule. β 0.5's P6 is
**bit-identical** to the author's record: 4447 events per schedule, worst miss 5.00e-1, offsets
(−8314, 6002).

**The control, archived this time** (`work/control-identity.txt`): with `root_offset` forced to
`Ok(0)` all three tests fail — P6 member 1 off **−110.523964** (the author's and both checkers'
number), the order pair tied, and the new high-β test off +395.26 (the unsheared signature) — the
original run left its `run.log` empty; these numbers are now on the record.

**Gates** (`work/gates-B13after.txt`, `work/gates-B17after.txt`): B13's detail line identical to the
author's, both checkers' and clean main's — `60/64 … worst ΔE 2.12e-2 ΔL 2.12e-2`, the same 9
replaced draws at the same radii. B17 `FAIL timeout: 60.0 s`, as after the original patch (this box
cannot exercise it; the M1 re-measures, per the lab rules). The plane example
(`work/rootkey-plane.txt`): Moon −25, Orbiter 0, Skimmer +1, You 0, battle tick 5,000,000 —
byte-identical. The full universe suite (`work/b8-after2.txt`): **57 passed** (the author's 56 plus
the new test) and the same 1 known-ignored, zero failures, 345 s on a shared box — the held-out risk
I named (a suite body silently dropped by the patched version inside a self-consistent digest) did
not materialise. `work/patch.diff` applies clean to a fresh worktree of `70f27a9` (verified).

`predictions.md` was written after the baseline probe, before the fix and every decisive run. Of the
five: 1 (the either-or invariant, 52/200), 2 (β 0.5 bit-identical), 3 (the control's numbers), 4
(B13 identical, plane byte-identical, suite green) and 5 (B17 timeout 60.0 s) — **all held**, and the
held-out risk I named (a suite body silently dropped by the patched version) did not materialise:
the suite is green with the same test set.

## What would make it wrong; the cost; the fit

- **Wrong if** a refused key were reachable in a scene whose centre has an unbounded readout (every
  bound-orbit centre: the plane's dolls, B12/B13/B17) — it is not: the refusal needs a state-made
  passage (or a pruned history) as a doll centre, which only the relaxed `retune` of this patch
  family creates. The refusal is deterministic and the entity stays stuck until the readout word is
  re-derived; that re-derivation is a real follow-up (the checker's option B), not done here.
- **Cost:** ~50 lines over the original patch; zero per-event cost (the fault path runs only on
  refusal; every gate, the plane and β 0.5 are bit-identical).
- **Fit:** principle 13 ("errors never compound… types of errors") — a wrong canonical key is the one
  error the queue cannot recover from, and it was silent; the law's own idiom ("a refusal never
  corrupts a body") is now obeyed by the key: the body stands, visible, with its reason.

## The lens

A second author inherits the frame "make the checker's one experiment cheap and decisive", and I
kept the fix at the refusal boundary rather than re-deriving the readout word (the deeper cure the
checker also named): a doll on a hyperbolic passage at β → 1 will always leave any fixed word, so
the loud refusal is the honest law-level answer, but a real relativistic-travel doll needs the
readout re-derivation before it can fly far. What I may have under-weighted: the stuck entity's
recovery path (today: never, within a run) and the fleet/handout arms of `compute_key`, which now
refuse loudly too but which no test exercises — their refusal cases need a fleet centred on a
passage doll, which the fleet API does not yet build.

## Commands (all from a clean worktree of main `70f27a9` + `git apply work/patch.diff`)

    cargo test --release -p emergent-universe --test rootkeys -- --nocapture   # 3 tests, ~1 s
    cargo test --release -p emergent-universe                                # the suite, ~350 s on this box
    cargo xtask behave --law plane --gates B13                               # ~40 s
    cargo xtask behave --law plane --gates B17                               # ~60 s (timeout on this box)
    cp work/rootkey_plane.rs crates/universe/examples/ && cargo run --release -p emergent-universe --example rootkey_plane  # ~8 s
