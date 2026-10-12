Grade: silver

**Abstract (for the integrator).** Author claims the plane engine pays a hidden per-frame O(N) tick: every `advance` runs `rekey` (deadline sqrt + heap set per entity) even at zero events — 215 µs/frame at 1k quiet bodies rising superlinearly to 37 ms at 64k — invisible to B10's exponent gate; deleting it the naive way (tick-keyed calendar) collapses the quiet frame to ~0.1 µs flat through 256k but breaks cross-schedule digest identity, so the pass is also an undocumented repair. I reproduced everything: baseline A=B=C=`645d0367…` bit-for-bit, quiet 237 µs→34.9 ms unpatched / 0.10–0.11 µs patched flat, patched digests `e107/ebaa/6931` exactly. My fleet-free control is bit-identical to baseline under the patch (leak localized to the fleet), and frame schedules under-resolve catastrophically (2,927/245 vs 73,372 kicks at the same cut). Adopt now: the requirement "quiet-frame cost flat in N" + the diagnosis; the deletion itself needs one more run.

## Reproduction (clean tree, `git apply work/patch.diff`)

- **Unpatched quiet** (my run / author): 237 / 865 / 3,925 / 34,934 µs per frame at n = 1k/4k/16k/64k (author 215/971/7,088/37,436); same superlinear shape (147× cost for 64× bodies; author 174×); `events=0` printed on every row — the zero-event claim is honest.
- **Unpatched digest** (cut 9e10): A=B=C=`645d0367d54b951b4f165ec1ea638a56fb4f650eb4592d7b6b2beac1e8c99204`, matching `work/digest-before.txt` exactly (wall 21.5 s, rss 333 MB).
- **Patched quiet** (`--include=crates/universe/src/universe.rs`): 0.11/0.10/0.10/0.11/0.11 µs at n=1k…256k, rss ~494 MB at 256k. Author's one 0.47 µs outlier at 64k did not reappear — noise, conclusion unaffected.
- **Patched digest**: `e1078737…`, `ebaa6ae7…`, `6931638f…` — bit-for-bit `digest-after2.txt`. The patch (which includes the `resolve_body` requeue) is the second cut, as the dossier says.
- **Predictions timing**: file mtimes order `digest-before` (−11 m) → `predictions.md` (−10 m) → `digest-after` (−5 m) → `digest-after2` (−4 m): written before the decisive (patched) runs, after the baseline. No git evidence exists (results are untracked); mtimes are consistent with the claim.

## Adversarial cases (mine; the example gained a `[cut]` arg, stats prints, and fixed `restricted` params)

1. **Alternate cut 6e10.** Unpatched: still A=B=C (`ca3a5250…`) — schedule-independence is not a one-cut artifact. Patched: three new distinct digests; divergence is systematic.
2. **The discriminator the author left broken.** `restricted(1_000, …)` panicked because `mu` is `mu_log2` (tests pass `-10`); the author's `1000` means a planet of 2¹⁰⁰⁰ stellar masses — a parameter error, as they said. With the test suite's params (mu_log2=-10, sep=5.27e8, ships at 1.5–2.6 Hill radii, cut = 3 periods, 11,628 kicks): **patched R = R2 = `d3dffd24…` = the unpatched baseline, bit-for-bit.** The core rewrite (tick-keyed calendar + requeue at resolution sites) is sound on fleet-free scenes; the leak is exactly where the author pointed — the fleet/handout machinery.
3. **Stats, not just digests** (cut 9e10, patched): A resolves 73,372 kicks / 103,511 ship items / 76 slices / 4 handoffs; B resolves 2,927 kicks / **1 slice / 0 handouts**; C 245 kicks / 3 slices. Same at 6e10 (A 49,129 vs B 1,946 vs C 158; unpatched all three 49,069). After frame-based schedules the patched engine's final `settle(cut)` does **not** converge to the canonical cut — the battle freezes. The digest divergence is dominated by under-resolution, not merely "a different commit interleaving."

## Novelty, quotes, gates (all verified)

- `docs/HISTORY.md`, the board and the taste log have no prior measurement of the per-frame `rekey` cost (0 hits). Not known, not tried.
- The Calendar doc quote is real (`crates/space/src/events/calendar.rs:6-7`: sift-down "dominated the calendar's cost at a million bodies").
- B10 (docs/law.md): "fitted exponent ≤ 1.1" on frozen scenes — a linear per-frame term passes it. The claim "B10 cannot catch it" is correct.
- docs/law.md "Ties": "The queue's key is (time, smallest body id, kind)…" — verbatim, and the shipped queue is deadline-keyed, so code and law already disagree; the patch moves toward the law. Note this cuts both ways: the correct fix's digests may legitimately differ from `645d0367…`; what must hold is cross-schedule identity.
- Unpatched digests agree even when slice counts differ (104/97/105 at 6e10): the fleet's internal slicing was already schedule-free in bits — the patched breakage is new.

## Why silver, not gold

The finding (the tick, its B10-blindness, the 10⁵× headroom) is real, reproduced and novel, and prediction (1) held (~300,000× on my 64k row). But gold requires the held-out predictions to hold and adoption within one step: the decisive prediction (2) failed — the author's own pre-registered kill of the patch — and the named fix (i)–(iii) is insufficient as written (below). What exists for adoption is a requirement and a diagnosis, not the deletion.

**The one experiment that would make it gold:** complete the fleet side of the deletion — requeue at every calendar *touch* (including `resolve_fleet`'s early return `else { return }`, which currently drops the fleet entity from the calendar unrequeued), and a cap semantic whose canonical cut still converges under any frame/budget schedule — then show three-schedule digest identity (against `645d…` or a re-frozen canonical digest per law.md "Ties", stated in advance) at flat ~0.1 µs quiet frames to 256k. My `restricted` scene is the non-fleet control; it already passes.

## What the author missed

1. **A second O(N) per-frame term in the same pass:** the deadline-keyed `advance` loop itself drains the whole calendar every quiet frame (the defer scan pops every entity, computes `deadline_of` again, requeues). The patch deletes both; the headline attributes the cost to `rekey` alone, so the "rekey alone ≥ 1 s/frame at 10⁶" extrapolation overstates that one function.
2. **Under-resolution, not just interleaving:** schedules B/C don't merely commit the battle in a different order — they leave it 97–99.7 % unresolved after the same canonical `settle` (1–3 slices vs 76). Mechanism: `resolve_fleet`'s early return drops the entity from the calendar, and the per-frame `rekey` was quietly resurrecting it every `advance`; fix (i) "requeue at every resolution site" does not cover non-resolution early returns. The diagnosis is right in location, incomplete in mechanism.
3. **The discriminator was a 30-second fix** (`mu` is `mu_log2`; `tests/motion.rs` has working params). Leaving it unrun cost the run its own confirmation; the "prime suspect" language was weaker than the evidence the author could have had.
4. Minor: the first-cut digest (`digest-after.txt`) I accepted as reported (the final patch, which is what matters, reproduces bit-for-bit); the `restricted` mode's unused `threads` arg and the stale `usage` line are trivial.
