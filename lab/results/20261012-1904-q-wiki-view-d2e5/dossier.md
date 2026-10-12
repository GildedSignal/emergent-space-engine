# Dossier — 20261012-1904-q-wiki-view-d2e5 (compiler, topic: view)

## Claim

The view page is compiled: 22 of the 28 runs in the cluster stand on `wiki/view.md` — the view's physics is measured wrong three ways near a compact mass (no time-transfer law, one-argument deflection key, "crosses once"), every refutation converges on the same one-step memo fix, the kinked-tube premise survives on shipped code, and on the plane the view path (not the engine) is the frame constraint with the display re-splat as the only over-budget component.

## Bottleneck

Not a compute bottleneck: memory. The wiki exists so runs stop rediscovering what earlier runs found (Julien, 12 October). Before this page, `view` was a seed — the cluster's 5 golds (the largest gold count of any uncompiled topic) were unreadable without opening dossiers. Expected gain: the integrator and the next author read one page instead of 28 branches; the converged memo fix (delay(b) + (b, sense|Q) + k=0 pair) is now actionable as one item. What it deletes: rediscovery.

## Evidence

Every line on the page cites its run id; every number was read from that run's `check.md` (first 120 words and body) on its `claude/lab-<id>` branch, and for the 5 golds, the conflicting pairs, and every number listed in `predictions.md` §6, from the `dossier.md` beside it. The three ungraded runs (70b0, 9096, a616: checkers died on 429/deadline, verified in their `checker-final.md`) appear on the page only as run lines and as findings explicitly marked "(ungraded)" inline (70b0's ramped-readout decomposition and rtf sweep; a616's newborn-image claim); no Current-best number rests on an ungraded run without that mark, and 9096 is filed under gravity-news below. Design-letter anchors verified on the tree: `docs/law.md` §Observation ("Positions are gathered at the observer's past light cone. Lensing takes deflection(b) from the doll's memo"), `docs/representation.md:57` ("crosses … once"), and H0183 (the oracle gains Shapiro). Cross-page handoffs honoured: `efb2`'s aliasing line (pointed here by the high-gamma page) is cited with its checker's contamination caveat.

Reproduce (≤ 2 min, no build):

```
cd lab/results/20261012-1904-q-wiki-view-d2e5 && sh regen.sh
```

regenerates the grade roster (28 runs: 5 gold, 20 silver, 3 missing), re-extracts the five least-certain numbers of `predictions.md` §6 from the runs' own branches, and diffs the page's run lines against the branches (see regen.sh output; exit 0 = every citation resolves).

## Predictions

`predictions.md`, written before the page. Held: the timing runs agree in kind with one refined artifact (P2); the 6eae→8f00 supersession is recorded as resolved (P3); no like-for-like cost contradiction exists (P4); grades are exactly 5 gold / 20 silver / 3 missing (P5); all five held-out numbers trace (P6, verified while compiling; regen.sh re-extracts them). Miss: P1's split arithmetic double-counted 8202 (kept view-primary with probe B noted for frame-cost) and placed 0fe0 off-page — the actual page carries 22 run lines (20 graded, incl. 0fe0 cross-cited for its Newton-iterations and no-view-gate findings, plus the 2 ungraded leads) and files 6 runs under other topics below. Held in kind, count off by two judgment calls, both disclosed.

## What would make it wrong

A sampled claim that does not trace to its run's branch (the checker samples five); or a later gold refuting one of the five golds compiled here — the page's current best would then follow that gold, per the weighing rule. Adoption cost: none (a page; publishing is `lab/wiki.py apply`'s three-way merge). Fit with PRINCIPLES: "maybe we need a karphaty style wiki where the current best and directions are clear and not missed to update" (Julien, 12 October) — this is that, for the view; and principle 30 ("what really matters is navigation, knowledge and dynamics those need to be perfect") is why the timing hole leads the page.

## The lens (compiling, and what it may have made me miss)

A compiler reads checkers' abstracts first and dossiers only where the abstract is not enough; a wrong number inside a dossier that its checker did not flag would pass me too. The integrator's keyword clustering is the cluster's boundary — a view-relevant run outside the 28 (e.g. the parents 4588 and 4b27, or efb2's own runs) reaches this page only through its child's check or another page's handoff, so the page may undercount the cost family's lineage. Timings are Linux/x86 shared-box: orders of magnitude only, as the lab rules say.

## Runs filed to other topics (6, by topic, for that topic's compiler)

**gravity-news** (light crossing the cone as a channel):
- 20261008-1859-scout-141c (silver): news arrival at one body grows R² under per-(body,source) cursors but +45/octave (∝ log₂ R) with cell-owned shell aggregates of sub-quantum events; off-centre observers keep the log law; a⁻¹ falloff restores ~R². The growing cone is a budget choice of Q, not a wall. ~32 accumulators/cell ≈ 2.6 GB at 10⁷ cells.
- 20261010-1544-scout-c4cb (silver): a doll's far-field gravity as a quantized multipole news channel: 8 reals, 32 bits, 8 samples per innermost-planet period = 256 B/system/P_ref; cost tracks the mass distribution's bandwidth, not body count (16× bodies: error 3.46e-4→1.47e-4). Broken by a comparable-mass inner body (FAIL at rate 8 and 32); dipole-only fails at 24L; far-field only (1.6e-2 inside the cell).
- 20261009-0521-redteam-93a4 (silver): the tube's "gravity is news" read has energy error second order in source kicks (μ-decade ratios ≈ 10², slope 2.0) and bounded with slaved sources (3.3e-7 at μ = 1e-3 over 30 reader orbits); the free-run growth is inter-law source divergence. The frozen kill letter also fires on three un-run in-domain cases (crossing reader, close sources, μ = 1e-2 R = 5).
- 20261010-2220-scout-9096 (missing): ungraded claim — in dyadic content-sized quanta the cone costs amortized Θ(action quanta) per tick at every distance; the wall exists only with flat quanta (Θ(a·log t) per tick) or none (Θ(t) per tick, Θ(t²) total).

**memory-h-live:**
- 20261012-0311-components-5465 (silver): the plane's individual store is 5,186 B/body (600 frames, 71 bodies) = 324× the law's 16-B Tube; zero exact sharing at 200 members; steady state 4,786 B/body at 1,800 frames; the honest packet is ~240 B (Residual 64 + carry 16), so individuals stay ≤ ~3×10⁷ — the price constant b-h-live needs. Compiled trajectories regenerable bit-identically (~32 µs each).

**frame-cost:**
- 20261006-1436-quant-18e5 (silver): the frame budget bounds the queue, not the item — `Budget::spent` is wall-clock, checked between items (universe.rs:808), so one engine item runs 25–30 ms past the 5 ms budget (seed-specific magnitude, mechanism on every run); the unbudgeted view is the majority spender; the paced 2.7–5× tax was a load artifact (1.06× on a quiet box).
- 8202's probe B (same run, view-primary): W* = max window surplus is the exact worst backlog of every work-conserving schedule (528 = 528, 620 = 620; 400 randomized + overload + crafted traces, zero violations either direction); M = W* − C·D decides misses exactly, 26 ms per 10⁵ frames; `id % k` sharding costs 244× p99; a 1-frame handoff costs +1 p99 frame.

**representation/handoff:**
- 20261012-0138-redteam-0fe0 (silver): representation.md red-team (kept off the view page except its two view findings, which are cited there): the B8 lockstep identity survives β 0.999, mass 1000, seed 7, 4 threads and a lone near-c pair; one evidence line was false (no near-c pair contact ever happens in v3 — its own event log says so); "never faced" ignored H0168's 0.88c stepper test; durable: §1 is stale, no view gate exists, one re-anchor gold was single-checked; adopt the flyby scene class for the identity rung.

## The page

`wiki/view.md` in this folder: header kept (`status: open`, `updated:` this run), five sections in order, 22 run lines, every claim cited. Nothing on the page is supported by fewer than one graded run except the two explicitly-marked ungraded leads.
