Grade: silver

The claim: the silent high-β key fallback (52/200 members keyed at the unsheared doll tick when the centre's readout leaves its word) is now a loud per-entity `key_fault`, the entity standing unscheduled. The baseline defect reproduces bit for bit on the archived original patch. The fix itself, however, is **missing from the record**: `work/patch.diff` is 0 bytes, so the dossier's commands cannot run as shipped. I rebuilt the fix from the dossier's spec (~50 lines) and it achieves the claim with the author's exact numbers — 148/52, 943/928 events, faults recorded, β 0.5 bit-identical, control exact, B13 and the plane identical, suite green. Real, cheap, on-goal; adopt only after the patch is re-emitted and re-run from `git apply`.

## Reasons

**The record's one hole, found first.** `work/patch.diff` is **0 bytes** (verified `wc -c`; the dossier calls it "+118 lines, applies clean to main, verified" — an empty patch applies clean vacuously). The shipped test's source is likewise absent; only the original run's test is archived (`work/orig/rootkeys-test.rs`). The author worked in a `rootkeys2-wt` worktree (paths in `work/gates-B13after.txt`), removed it, and the harness snapshot of lab-3 captured nothing. No stash, branch or dangling commit carries the fix (I checked `git stash`, `git fsck --unreachable`: only other runs' artifacts). Every number below that depends on the fix was therefore verified on **my independent reconstruction**, not the author's code.

**Baseline (reproduced exactly, on the record's own patch).** Clean worktree of `70f27a9` + `git apply work/orig/patch.diff`, then `work/rootkeys_probe.rs` as `tests/rootkeys_probe.rs`: β 0.5 — 200/200 readable, worst miss 0.500, 0 silent; β 0.9 and 0.99 — 148 readable (0.499/0.498), **52/200 keys silently at the unsheared doll tick** — identical to `work/probe-baseline.txt` line for line. `work/refusal_domain.rs` as an example: first cartesian refusal at 2²¹ (β 0.5), 2²⁰ (β 0.9/0.99) — as claimed.

**The reconstruction (checker's, from the dossier's spec).** `state_of` propagated in `root_offset` (the `else { break }` → `?`), `compute_key → Res<Option<Tick>>` with every swallow propagated, `key_fault` beside `root_key`, `key_fault_of(e)`, refused → `Tick::MAX` + fault at both write sites. Results, all matching `work/p6-out.txt`: β 0.9/0.99 — 148 keyed at the shear image (worst 0.499/0.498 ≤ 0.5), 52 refused with recorded faults, zero silently unsheared, one history per member under 1 and 4 threads, **943/928 events after the settle — the author's exact counts**; faults persist (stuck, as the dossier says). β 0.5 P6 **bit-identical**: 4447 events, worst 5.00e-1, offsets (−8314, 6002), 1/4/8 threads. Adversarial β 0.999 (mine): invariant holds, 148/52, worst 0.495.

**The control, exact.** `root_offset` forced to `Ok(0)`: P6 member 1 off **−110.523964** (`key 301056 tick 301056 image 110.523963560`), the order pair **tied at 16,384** — precisely `work/control-identity.txt` and the author's quoted numbers; restored, 3/3 pass.

**Gates, plane, suite.** B13 on the reconstruction: detail line **identical** to `work/gates-B13after.txt` (60/64, worst ΔE/ΔL 2.12e-2, the same 9 replaced draws at the same radii; 18.9 s vs the author's 15.3 s, shared box). The plane example: **byte-identical** (Moon −25, Orbiter 0, Skimmer +1, You 0, battle tick 5,000,000). Full suite green on the reconstruction, 1 known-ignored (the only failure in my tree was my own leftover baseline probe, which by construction expects the unfixed code — not the author's). B17 not re-run: the author's log shows the box's 60.0 s timeout with matching machine_state timestamps; the M1 re-measures per the lab rules.

**Timing.** `predictions.md` (01:34, per mtimes) predates every decisive log (probe 01:37, gates 01:39–01:40, suite/p6 01:44). It quotes the baseline numbers while the saved `probe-baseline.txt` is 3 minutes younger — a re-run after writing, consistent with its own text ("only the baseline probe has run"); the decisive experiment (the fix's behaviour) was genuinely held out. All five predictions held where checkable (5 = B17 cited, not re-run).

**Novelty.** This is the direct execution of the original run's named gold experiment (its check2: "make the centre-readout failure loud… every member's key must then either equal its shear image to 0.5 tick or the refusal must be recorded"). No HISTORY entry or doc implements a loud key refusal; the `key_fault` idiom is new. Correctly framed as an assigned closure, not a discovery.

**Goal fit.** PRINCIPLES 13: "basically we don't want errors that can compound that's the goal" — a wrong canonical key is the one error the queue cannot recover from, and it was silent. It obeys the law's own idiom (a refusal is recorded, the body stands). Zero per-event cost (the fault path runs only on refusal; every gate, β 0.5 and the plane identical). No compute gain — this closes a correctness hole in the root-clock key (HANDOFF's simultaneity-across-dolls item), which is what the second-author run was for.

**Why silver, not gold:** the deliverable itself — the patch — is not in the record, so nothing about the fix can be reproduced *from the run folder*; the taste log's standing rule (results the shipped code cannot regenerate) forbids gold on that alone. Why not lead: the work is demonstrably real — the logs carry full harness output from the (now deleted) worktree, and my from-spec reconstruction hits the author's exact event counts (943/928), which a fabricated record would not survive.

## The one experiment that would make it gold

Re-emit the actual patch (original + the fix, with the shipped `rootkeys` test) into `work/patch.diff` and re-run the named experiment in a clean tree from `git apply` alone. One trap for whoever re-emits: the propagated centre-readout refusal arrives as `Error::Space` ("state outside the integer word"), not `Error::Refused` — a fault recorder that matches only `Refused` drops it silently (my first attempt did exactly that, reproducing the original bug in new clothes).

## What the author missed

- **`work/patch.diff` is empty** — the run's one deliverable; the dossier's "applies clean (verified)" is vacuously true of an empty file, and the shipped test's source went with the deleted worktree.
- **`run.log` is empty again**, exactly as check2 flagged on the original run (the control was archived separately, which was the substance of that flag).
- The stuck entity has no recovery path within a run, and the fleet/handout arms of `compute_key` now refuse loudly but are exercised by no test — both named honestly in the lens section, and both real.
- Minor: at β 0.999 the refused set stays 52 (geometry, not β) — the invariant scales; no new corner appears.
