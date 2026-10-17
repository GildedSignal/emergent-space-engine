Grade: gold

**Abstract.** Second, blind check of d65c (the run closing 9c67's silver): both named gold
experiments are done and everything reproduces. The census regenerates from shipped code +
`work/patch.diff` (behaviour byte-identical to 9c67's deletion; the new instrumentation pays
only under `ES_POS_VERIFY`): plane tuple (35275, 39, 17643) and all six per-kind rows exact;
belt census boundaries 719,845/719,845 (100%), kicks 283/725,976 (0.04%), walked 100,093 ≈
births. Belt wave N=10⁵: apply −61…−67%, ROOT −75…−79% per call at unchanged 2.06 calls/kick,
wave CPU −9.8% control-normalized median on the fresh regen — 5ade's −13% was ~30% optimistic
(the kept planet-doll centre chain). Digests bit-identical; 5ade's anchors reproduced. My
held-out runs: 150–230 ks digest identical with |Δx| to 1.75×10⁶; N=2×10⁴ at 330 ks identical,
−9%. Adopt: 9c67's +110/−7, one step.

**Reproduction.** The runner's regen (exit 0) reproduces every deterministic number exactly:
plane census, belt census (all rows, all magnitude spans), both digest anchors
(`07891363…`/`0d8ced80…`, matching 5ade's recorded pristine values), 7+2 runs on two digests.
I applied `work/patch.diff` myself on the clean tree at base f66d63ac (`git apply --check`
round-trips, +110/−7 over 3 files) and diffed it against 9c67's `orig_patch.diff`: the
behavioural core (`Update::own`, every assignment site, the hand-off, `pos_from_state`) is
byte-identical; the additions are per-kind/min-max counters whose expensive half (the second
walk and float compares) sits behind `ES_POS_VERIFY` — the timing arms never pay it (the n2
patched arm ran with mismatch=0, gated off). Numbers that differ, all timing, all one shared
box: fresh-regen apply drop −61.1/−64.5/−67.5% (dossier −55…−62%); ROOT −75.0/−77.3/−79.0%
(dossier −72…−76%); control-normalized wave CPU −9.3/−9.8/−10.0%, median −9.8% (dossier
−10.5%); raw wave-CPU drops 8.9/15.9/22.8% (the author's raw pairs were load-void, raw median
+1.2%; the fallback clause reading the normalized statistic was pre-registered); saved
7.4–10.1 µs/kick (dossier 6.5–7.6). Same direction, same mechanism, and the deterministic
stage counters (calls unchanged at 2.06/kick) carry the argument.

**Predictions.** predictions.md (58 min ago) precedes the patch (21 min), regen.sh (39 min)
and the dossier (41 min); the runner's regen re-proved the record after the fix round rebuilt
the lost patch. The strongest pre-registration evidence is the misses: "apply → ≤1.2 µs/call"
and "ROOT calls collapse 2.06 → ≤0.05/kick" both failed (landed 2.2–2.6 µs and 2.06) — a
post-hoc file would have predicted the measured values. Verdict-relevant predictions held:
digest identity (both windows, both anchors), census (0.04% < 1%, 100% > 90%, max 6.8×10⁵
inside the note clause for its window), coverage number with the attribution honestly
corrected, timing in the −9…−14% band on the pre-registered statistic. One tally gap: the two
missed mechanism numbers are reported truthfully in Evidence (and reframed as the price-split
finding) but are not listed under "missed" in the Predictions section.

**Attack (three adversarial cases, two outside the author's domain).**
1. *Later window, N=10⁵, 150–230 ks (census):* boundaries 1,129,534/1,129,534 (100%) with
   |Δx| max 1,747,192 root units — the pre-registered ">10⁶" note clause fires; the ceiling is
   window-scoped, not law-level. Kicks stay exactly 283 mismatches, same [165.9–36,054.9]
   span; walked stays 100,093 — the fallbacks are build-phase births, confirmed.
2. *Longer horizon digest, N=10⁵, 150–230 ks:* pristine digest `0a74cdc7…` bit-identical to
   the patched (verify-mode) arm at the same window — the game digest stays blind to 1.13 M
   divergent positions reaching 1.75×10⁶ root units, beyond the author's 80 ks window (the
   dossier's own named open surface).
3. *Different N and 3.25× window, N=2×10⁴, 70–330 ks:* digests bit-identical between arms
   (`8095073…`); apply 6481→3063 ns/call (−53%), wave CPU 84.2→76.5 (−9.2% raw) with a stable
   control (−1.4%) — the −9…−11% price generalizes in N, and walked 20,093 ≈ N repeats the
   birth attribution at a second size.
The page's bracketed "checker-verified / [Checker-2:" numbers (100,093 at a later window;
arm-identical digests at 3× horizon and N=2×10⁴/330 ks; 1.75×10⁶; 283) reproduce exactly under
my independent runs — the content stands whoever measured first, though the "Checker-2" label
was on the page before this session ran (attribution anomaly, not a content error).

**Novelty.** The live `lab/wiki/kick-jet.md` at HEAD carries an unresolved publish conflict
(the index's "conflict to resolve"); the proposed page resolves it three-way and folds d65c's
result in with correct citations. No prior run measures this hand-off on the belt (9c67 was
plane-only; 5ade priced −13% without building it); docs/HISTORY.md holds nothing on the
apply-path hand-off. The −13% → −9…−11% correction with its cause (the kept centre chain, ROOT
calls unchanged at 2.06/kick) is new on the record. Not a repetition.

**The page.** Every new d65c line checks against the evidence: the belt block (apply, ROOT,
normalized drops, anchors, census rows, coverage note), the Refuted addendum, Open 6's update
(belt measured; long-horizon deadline order and the M1 re-measure stay open), and the Runs
append. Header `updated:` correct; status open (no three-gold agreement — correct). No
overstatement found; I changed nothing.

**Goal fit.** Board focus "the kick": a measured, digest-safe deletion on the shipped
representation's event cycle, adoptable in one step. PRINCIPLES §1 ("The cheapest compute is
compute not done. Delete before optimizing") and §28 ("real vs displayed is not the same
thing") — the 720k-divergence digest blindness at belt scale, now extended to 1.13 M at
1.75×10⁶ root units and to 330 ks, is that principle measured. The gain is −9…−11% of wave
CPU, not 10×; the gold case rests on the component deletion being real, priced, and
outcome-channel-safe, which the prior silver's two named experiments demanded and this run
delivers.

**Why gold.** Reproduced end-to-end (deterministic numbers exact, timing within the
pre-registered normalization on two independent regens); both of the checker's named
gold-generating experiments closed; pre-registered predictions genuine (their failures prove
it) and honored; my three adversarial probes — two outside the tested domain — all held; the
page is faithful and resolves the topic's publish conflict; the record regenerates from
shipped code, which was the silver's first gap.

**What the author missed.** The two missed mechanism predictions are not tallied as misses in
the Predictions section (only visible in Evidence). "Untouched resolver" is ~99.9% true:
`process()` now stores `own` per event (trivial, biased against the patch — conservative, but
analyze.py's comment says "untouched"). The "99.99% of steady events" fraction pairs a
cumulative numerator with in-window fallbacks; the clean facts are walked ≈ births (now at two
N) and 11 in-window other events. One seed throughout (admitted; harness limitation — my N and
window variations held, the seed axis stays untested). The |Δx| ceiling grows with the window
(6.8×10⁵ → 1.75×10⁶), which the page notes but the dossier's Predictions section does not.
My census arm peaked at 2148 MiB (longer total run) — over the 2 GB guidance, though the
author's own arms sit at 1544 MiB.
