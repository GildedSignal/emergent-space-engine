Grade: gold

Second author on bd4b flew the checker's named gold experiment: per-class span coverage of
the minted arc. Reproduced bit-for-bit (digests b42da477…/8c242b02…, refused 0, mints
23/137, kinds [23,0,0]/[55,82,0], 12.5 KB/mint; span section identical, only µs timings
drift). Cycles walk 10⁻³ of the compiled arc (coverage medians 0.04–0.23%), passages ~60%
of ψ but 12–15% of panels; never-read 85–98.5% per class; the 448-knot tail is cycle-class,
446/448 unread. The lazy-compile CPU lever is killed (step_for reads period()/duration()
full-arc sums — I verified in step.rs:75, orbit.rs:676); the store lever is sized near-total
on the kicked classes. My held-out seeds 4–5 and a 50 s arm (147 re-mints) hold the
structure. Adoption cost: none new — 0757/b9ae flew the memory side; this sizes and
justifies it. Two premises killed, the page's open directions 1–2 closed.

## Reasons

**Reproduction.** Applied `work/patch.diff` at base caa2a43b (its `base-patch.diff` is
bit-identical to bd4b's committed patch; the extension is print-only census code). All four
arms regenerate: default seed 1 digest b42da477294f7619 / replay a693ac68cbc7fb46; m400
seed 1 digest 8c242b023e8b79e4 / replay 0de3a82c1926a83d; refused 0 everywhere; mints
23/137, kinds [23,0,0] and [55,82,0], 12,465 B/mint — equal to bd4b's stored record on its
branch (I compared against `origin/claude/lab-20261020-1116-system-bd4b`), so the census is
print-only over the shipped law. Every dossier number matches the JSONs: made-cycle
coverage medians 0.228/0.117/0.112%, member-cycle 0.042/0.108/0.05% (max 3.4%), passage
0.619/0.582/0.606 of ψ; never-read shares 85–87 / 97–98.5 / 85–88% (seed 1: 152/175,
5,388/5,480, 10,516/12,333); release overhang ~0.12% of ψ, release_capped 0 on all seeds;
tail rows 448→446 (cov 5.0e-7), 257→256, 196→194; seeds 2–3 same shape. One lab-hygiene
note: the shared CARGO_TARGET_DIR held the first checker's probe binary; I verified its
JSON path is identical to the patch-only build (span and digests equal; the runner's
patch-only regen at 12:46 agrees), so two independent builds confirm the numbers.

**Predictions.** predictions.md (mtime 54 min at session start) predates the decisive JSONs
and the dossier; P1–P4 and a kill criterion are pre-registered. P2 held (≥30% predicted,
85–88% measured). P1 and P3 failed informatively and are reported as failures — and the
failures are the result: the belt's one-kick-per-period sets only the level-0 cadence, the
nested plan rebinds a fresh mint after ~10⁻³ of the arc, and the 2× release overhang is
~0.1% of ψ. The kill criterion (both ≈ 0 never-read) did not trigger. One soft spot: P4 is
reported "held (cycle-class) and sharpened", but its other half ("never-read ≈ 0") failed
like P1; the number is disclosed, so this is generous phrasing, not concealment.

**Attack (three adversarial cases, two outside the author's range).**
1. Held-out seeds 4 and 5 (author flew 1–3): structure identical — made 86.9/85.7%,
   member-cycle 98.3/98.4%, member-passage 86.8/85.3% never-read; coverage medians in the
   same classes; tails 208→207 (5.2e-5) and 292→291 (8.2e-6). Holds.
2. Window 30→50 s (3× the mints, 415, with 147 re-mints): medians unchanged
   (member-cycle 4.2e-4, passage 0.607, never-read 0.985/0.852); the 448-knot tail recurs
   (446 unread). The re-mints also exercise the plan control the author said was "never
   exercised": observed re-mint vs estimated close differs by 7–18% of the walk
   (anti-conservative for never-read, immaterial at 10⁻³ coverage). The dossier's "no body
   was minted twice inside a 30 s window" is in fact wrong — my 30 s seed-2/3 reruns show
   re-mints (bodies 49–51; 43, 55) — but the bounded error leaves every conclusion intact.
3. Members 1200: bit-identical to m400 — the bench clamps `--members` to (4, 400)
   (xtask/src/universe/mod.rs:40), so a decade-up fleet case cannot be flown on this
   instrument; the author's "≤ 400 members" domain line is the bench's hard cap, honestly
   drawn.

**The CPU-lever kill, code-verified.** `step_for` (crates/universe/src/step.rs:75) reads
`c.period()` / `p.duration()` for every binding it intervals, and `period()` returns
`increments[1]` (crates/space/src/orbit.rs:676) — a running sum the compile produces by
traversing the whole arc. A compile covering only the walked 10⁻³ span cannot answer it.
The mechanism claim is correct as stated.

**Novelty.** The published mint-knots page's open direction 1 names exactly this
measurement ("the traversed fraction", scoped by the first checker to per-class SPAN
coverage), and direction 2 (the tail's class); docs/HISTORY.md holds no prior span-coverage
measurement. This run closes both: the CPU half of the span lever is dead (premise wrong),
the store/readout half is sized near-total on the kicked classes (generalizing 0757's gold
bounded cache and b9ae's standing knots from the nladder population), f9b4's thinning is
graded (panels sit in the never-walked outer bands), and bd4b's keys-only retention is
priced. Precedent: components-4643 was gold for exactly this shape — kill one lever,
size another, nothing new to build.

**Page.** The proposed wiki page folds the result in faithfully; every number on it traces
to the JSONs (including the "12–15% in panels" read share = 100 − never-read). I added one
bracketed note with my held-out confirmation and the bench's member cap.

**Goal fit.** Decides work on the board's two worst rows (kick 75–160 µs vs ~50 ns; memory
per body). PRINCIPLES: "Compute only surprises" (3) — 85–98.5% of the mint is pre-computed
reading that never happens; "Store the generator, not the generated" (6). Canonical
outcomes are the integer digests, bit-identical; floats only priced µs/knots, orders of
magnitude only, as the lab requires.

## What the author missed

- The "no body was minted twice inside a 30 s window" claim is false (seeds 2–3 have
  re-mints; 50 s has 147); the control was exercisable and its answer (≤18% of the walk,
  either direction bounded by 2×) belongs in the dossier's wrong-if section.
- P4's never-read half failed, same mechanism as P1; "held and sharpened" understates that.
- The bench's `--members` clamp at 400 is never stated as the reason the fleet arm stops
  there; a decade-up case needs a different instrument (the ladder), not this census.
- The ψ-coverage of passages (~60%) is a fast-coordinate artifact near the turning point;
  the panel share (12–15% read) is the honest number and the page is right to lead with it,
  but a time-domain coverage would have closed the reading note instead of flagging it.
