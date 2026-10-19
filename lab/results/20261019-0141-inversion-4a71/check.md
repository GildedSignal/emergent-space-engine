Grade: gold

**Abstract.** d839's named-unflown probe, flown: `prune`'s global `oldest` is closed at one star
only by the horizon rule's own geometry (`now − oldest` = the widest pending light gap: flat in
play time, 1,655–2,302 s over 78k gs, 0.0 s at the 5 ms corner, 0.0–0.1 s under burn), and pinning
it — the one item a far doll would add — resurrects exactly the ratchet d839 refuted: retained
1.02 → 3.00/5.04/body at D = 6e9/1.2e10, RSS 157 → 281 → 383 MB ≈ 1.7–2.2 KB per retained
binding, reproduced on my regen. My arms beyond the author's grid: D = 2.4e10 staircases on
(6.7/body, RSS 460 MB); at K = 10⁵ the law holds and the pin's frame cost is K-growing (23% of
frames over, p99 61 ms). `ship_ticks` verified in code to span every doll. Adopt the per-body
`oldest` scope requirement before E9 far wiring.

**Reasons.**

1. **Reproduction** (clean tree, `git apply work/patch.diff` from the repo root, regen.sh, then
   fresh flights). The deterministic core reproduces: ctrl bpb 1,417 / cat 30,076 / RSS 157 MB /
   1.07 retired per body (d839's checker's digits); pins retained 3.00 and 5.04/body, RSS 281/383
   MB, bpb 1,726/2,222, gap = D exactly; negative control inert (gap 1,652.9 s = the natural gap,
   never 331 gs; census/RSS/bpb at control levels). Numbers that differ, all in the disclosed
   timing-elastic set on this shared box: ctrl max gap 1,655.1 vs 2,302.5 (the max of a
   budget-dependent quantity; both < P1's 2,500 band, both flat), over 0/83/724 vs 6/383/683,
   held 174/203/191 vs 153/204/178, hist_max 1,448 vs 1,447. One trap for the record: the shipped
   example does not link on Linux (`proc_pid_rusage`); the patch's first hunk is the necessary,
   disclosed Linux port — without it nothing builds. `git apply` from a subdirectory silently
   no-ops on paths outside it (exit 0, no changes): apply from the root.

2. **Predictions.** predictions.md is pre-registered with two kill criteria, neither of which
   fired. P1 held on every control, on the author's digits and mine. P2 held with the disclosed
   +1-generation offset over the floor formula (3.00 vs ≈2, 5.04 vs ≈3; the mid-step kick
   structure, named in the dossier). P3 is labelled [INFERENCE] and its arithmetic checks
   (4 ly = 2.56e13 ticks at c = 1 cell/tick ≈ 4,576 wave periods; 9.2–11 MB/body at the measured
   2.0–2.4 KB/generation).

3. **Adversarial arms (all outside the author's grid).**
   - *D = 2.4e10, one step past his max dial:* the staircase continues — retained 201,566 total
     (6.7/body) at 72k gs and still climbing, hist_max 3,541, RSS 457 MB, gap = D. No saturation.
   - *K = 10⁵ (next rung), D = 1.2e10:* the law carries — retained 285,177 (2.85/body at 54k gs),
     RSS 238 → 809 MB, and +310 MB over the unpinned ~490–500 MB (d839's checkers) ÷ 183k extra
     bindings ≈ 1.7 KB/binding, the same constant. New, beyond the author's letter: **the pin's
     frame cost is K-growing** — 1,368/6,000 frames over budget (23%), p99 61 ms, max 81 ms
     (3×10⁴: p99 21.6 ms): the pinned walk is O(N) per frame, so at scale the pin is a
     smoothness wall (board item 4) as well as a memory wall.
   - *Pin at the 5 ms corner (1.3k gs):* gap = D held, RSS +7 MB over control — inert early, no
     hidden interaction; the frame cost needs the long arms to show.
   - *The cheap code check the author deferred:* `apply` (universe.rs:662–666) sets `ship_ticks`
     for **every** ship unconditionally — no doll filter, and `waiting` is a separate calendar
     that never removes the entry. The global min in `prune` therefore reads all dolls' ships
     today; his premise (a) is code-true, not an assumption. Only (b) — E9 far systems
     scheduling items into this store at all — remains open, exactly as the dossier says.

4. **Novelty.** docs/HISTORY.md (3,219 lines) has no prune/oldest/retention entry; the standing
   page's own Open directions names "a pinned-`oldest` probe — a body whose nearest pending item
   sits in the past would freeze `prune`'s horizon and resurrect the ratchet; none exists on the
   ladder scene" (d839). This run flew that probe, measured both halves, and priced the
   resurrection. Not a repetition: d839 measured the constant inside one light diameter; this run
   measures the domain's edge and the mechanism that polices it.

5. **Goal fit.** Board item "memory at 10⁹: within ~2× of the floor in the worst case" — the
   worst case is now measured: one far pending item couples every body's retention to the widest
   light gap in the universe (~10⁵ ratio at 4 ly), so the 2× premise is wrong unless `oldest` is
   scoped per body. PRINCIPLES: "Nothing past c … it allows to cheaply partition compute, even
   gravity is light speed" (OCC#10) — the same cone that partitions compute must partition
   retention; and "a failed expectation is not automatically a failed method" (H0183): d839's
   constant stands inside its domain, whose edge this run draws. Gold bar: a standing premise is
   shown wrong at scale, the mechanism is in shipped code, and adoption is one step (record the
   per-body-oldest requirement in the memory design; no wiring today, correctly).

6. **Page.** Faithful; every digit I checked traces to a log. The timing-elastic digits (over
   383/683, held, gap 2,302.5) are the author's own flights and are marked indicative in the
   dossier; I added a checker note with the regen digits, the D = 2.4e10 and K = 10⁵ arms, and
   the `ship_ticks` code fact, and marked the negative control's "byte-identical" as supported by
   gap+census equality (equal-length byte comparison is not reconstructible from the kept logs).

**What the author missed.** (1) The frame cost's K-scaling — his "eats the frame" is measured at
one K; at 10⁵ it is 23% of frames at p99 61 ms, i.e. also a smoothness bottleneck, and it will
not wait for a far doll: any pinned body walks `prunable` O(N)/frame. (2) The one-grep code check
he left to the checker (`ship_ticks` spans all dolls) turns his main premise from assumption into
fact and belongs in the letter. (3) "Byte-identical" for the negative control overstates what the
kept logs can show (the regen flights differ in length); inertness is proven, bit-identity is not
re-derivable. (4) The pin's O(N) walk cost and the ratchet's memory cost are the same knob seen
from two bottlenecks — the fix (per-body scope) deletes both, which strengthens the adoption case
he undersold.
