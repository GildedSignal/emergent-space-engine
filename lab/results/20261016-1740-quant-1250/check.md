Grade: silver

**Abstract.** The angular certificate (`ES_SCAN_CERT`) is real, conservative and cheap, and its
deterministic core reproduces exactly: kills 68249/104194 at N=300 burn — bit-identical to the
dossier's own counters — reads/hit 48.6→16.8, per-answer cost 2.2–2.8×, and certificate-on ≡
certificate-off ≡ brute on every scheduled flight, on fresh seeds (`SEED_ADD=100`) and a 3.3×
longer horizon. cdf0's 10–20 ns/candidate pricing is really 0.2–0.5 µs (loaded: to 0.58), and the
drain's max-gate at N=1000 burn survives as reported. Not gold on the record: "~10× answer cut
held (2.2–2.8×)" is a miss labelled held; "12 scripted flights/48 digests" is 8/32; "bit-identical
everywhere" — the dossier's own regen prints DIGEST-DIFFERS on 4/8 wall-paced rungs under load;
the 26× N=300 backlog cut regenerates as 1.1× loaded (10⁴'s 13× reproduces). Adoption: additive,
env-gated, one step.

**Reproduced** (patch applied by me on a clean tree at a523ace9, built 22 s):
- `regen.sh` (runner, exit 0) and my own runs agree on every deterministic cell: kills/cands
  25073/34091 (300 coast), 49511/61622 (1000 coast), 69093/99113 (10⁴ burn); reads/hit 70.5, 94.6,
  14.0 — the dossier's numbers exactly. My N=300 burn: kills **68249/104194**, answers 1348,
  candidates 104194 — all three identical to the dossier's table, digests equal across arms.
- `frame_digest 3`: 8 flights × 4 schedules agree in all three arms; `finder == brute` (diff
  empty). The dossier/wiki say **12 flights / 48 digests — the harness runs 8/32** (regen's own
  `grep -c` prints 8).
- Adversarial, outside the author's range: (a) `SEED_ADD=100` — 8 fresh universes, cert ≡ brute;
  (b) `frame_digest 10` — 3.3× the horizon (deeper `adv·cycles` accumulation), cert ≡ brute;
  (c) the 200 ms relaxed controls at N=300/1000 and rtf 1000 — all digest-identical across arms.
- Mechanism anchors check out: `SCAN_BACKLOG = 2048` (universe.rs:79), the drain gate
  `room < 2·max(scan_ns, 0.75 ms)` (universe.rs:1190) with 1/64 decay (1205) — a running max, as
  the dossier reads it. `range_of` widens `lo` inward by the residual and caps speed at 4·v_peri,
  so the chord bound's inputs are genuinely conservative.

**Where the record fails to regenerate.** On this shared machine, `regen.sh` prints
DIGEST-DIFFERS on the 4 wall-paced rungs N=300/1000 (off/on answers 191/193 at 300 coast — the
served-schedule itself diverges under starvation), while N=10⁴/10⁵ print identical. My own 12 ms
runs (lighter load) were all identical, including the rtf-1000 starved pair; same-arm repeats are
stable. So: the certificate was never caught changing an outcome — every unstarved control and
every scheduled digest is identical — but "bit-identical outcomes on every flight run" is a
machine-load statement, not a property, and the table's "identical" column does not regenerate
here. Likewise held_max N=300 burn: author 508→19 (26×), regen 549→489 (1.1×), mine 60→21 (2.9×);
10⁴ reproduces (250→19, 13×). Prediction 2's magnitude ("per-answer cost falls ~10–20×") was
missed (2.2–2.8×) yet is filed as held; prediction 4's "kill ≥ ~80%" regenerates as 65–76%
overall and is restated as "kill ≥ 65%". Predictions themselves were pre-registered (mtime 17:56
vs dossier 18:14) and their misses are mostly disclosed — the mislabels are the defect.

**Novelty.** cdf0 (20261016-1120) priced the angular cut and named its success bar; nobody had
built it. `ce694696` (13 Oct) carried a different, non-shipped bound on the pair predicate
(linear relative motion), not a phase-arc cut on the knot table; HISTORY has no prior angular
certificate. The page folds the result and its two premise corrections (cost 20–45× off; means do
not reopen a max-gated latch) into Refuted/Open correctly — I fixed the flight count, the digest
claim and the N=300 backlog number in place.

**Goal fit.** P3 "compute only surprises" and P6 "store the generator": the knot table is
compiled once per orbit and the certificate reads phase the tube already owns. It moves scan-queue
open direction 1's answer half (measured 2.2–2.8×, not the hoped ~10×) and shows cdf0's pricing
premise wrong — but the direction's success bar (the drain reopened at the plane's N) is **not**
met, and the author says so.

**The one experiment for gold.** The Passage half: a passage-side ψ certificate (or Passage
exclusion from the candidate set) plus deletion of the capture fallback's `bodies/4 + 64` walk,
then re-measure the latch's **worst** answer at N=1000 burn under load — held_max → ~0 with
digests identical closes direction 1's bar.

**What the author missed.** The record items above — the lab's standing silver pattern ("results
the shipped code could not regenerate"), here in the digest column, the flight count, one
"held" label and one restated bar. No test guards the certificate itself: all its conservatism
evidence is flight digests; a direct property test (randomized tubes × ticks × windows:
`cannot_meet` true ⇒ the exact predicate also rejects) would pin the strong-field domain (q ≫
2⁻¹⁸, where the weak branch's zeroed q makes `advance()` an underestimate and `e_adv`'s 4e-3
slack unjustified — untested, and correctly named as the claim's domain edge). The chord bound's
soundness silently leans on `near ≪ r_min` (true by ~10⁶ in the plane; at `near ≥ 2·r_min` the
clamp makes α = π and kills stop, so the pathological band self-neutralises — worth one line in
the certificate's doc, not a hole).

Checker's runs: /tmp/check1250/ (this machine, Linux/x86, orders of magnitude only). Tree left
clean; nothing outside `check.md` and `wiki/scan-queue.md` touched in the run folder.
