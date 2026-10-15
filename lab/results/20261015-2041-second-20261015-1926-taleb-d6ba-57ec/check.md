Grade: silver

**Abstract.** The checker's named gold experiment, flown as a depth ladder on d6ba's frozen patch (digest-identical to every published anchor): the comet class is **standing** — 100 Live passages byte-identical (2,558,720 B, 10,570 panels) at 32k and 48k, 18.1 kB/alive, one arc (22.2–25.6 kB) per live dense-kicked comet at 28 kicks/ks where the drained belt takes 0.196, only the record stack growing (474→710 records/body); shipped ctl is linear ruin (2.134 GB pinned, 0 demotions, 67× rss at digest parity). Belt floor re-measured N-constant: 86,944 B total, byte-identical at 10³/10⁴/10⁵ (10³ is my probe) → ~87 kB at 10⁹, not ~9 MB nor ~9 GB. Silver only because P1/P4 failed as registered and the registered 96k depth has never survived to a record. Adoption cost: a sentence, no code.

## Reproduction (complete)

The runner's `regen.sh` exited 0; every row in `regen-matrix.log` equals the dossier digit-for-digit (1,569.3/1,748; 656.1; 8.6 and 0.9 with pinned_total 86,944 byte-identical across 10⁴ and 10⁵; 15,089.6 / 15,032.2 / 9,498.2 / 12,125,140.1). Digest identities all verified against the published record: belt-48k `f8b52855…` = d6ba's; 10⁵-48k `2109a2e0…` = 1d52's anchor; ctl-burn-20k `5caeb1b6…64c451` = e0f9's; comet 32k variant = ctl (`32ef5b00…`). Derived numbers recomputed: dead 85,224/30 = 2,841 B/death; promote ratio 837,697/126,098 = 6.64 at p50 607 µs; kicks/ks 135,485/100/48 = 28.2 and 94,518/10,076/48 = 0.196; mixed 1,109,824/50 = 22.2 kB; the 32k "112 kick-minted-live" decomposes exactly (100 passages + 12 transient cycle arcs, gone by 48k). The ctl arm's 2.134 GB never-freed store and rss 2,817 MB are in its flight file.

## Adversarial (three of my own, frozen binary, two beyond the author's domain)

1. **Belt 10³ coast 48k (below the flown range):** `pinned_total_B 86,944` — byte-identical at a third N; per-body 80.8 keeps falling, bpb_engine 1,149 sits inside the quoted 993–1,317 band. The N-constant floor reading is confirmed, and it kills *both* prior 10⁹ projections (d6ba's ~9 MB and d6ba's checker's 9 GB per-body scaling).
2. **Stargraze 100 @ 48k, seed 2 (one seed in the record):** the standing class is seed-stable — 100 Live passages, byte-identical 2,558,720 B, same 10,570 panels, 17.8 kB/alive, kick-minted-live = 100 exactly, 30.5 kicks/ks/comet, demoted-records 710.7/body (seed 1: 710), nokick 3 arcs/1,720 B, plunges 0.
3. **Stargraze 100 @ 96k (the registered P1/P2 depth, past the flown range): killed by the box at ~1,430 s CPU with only the header flushed — inconclusive.** No surviving 96k comet record exists anywhere: the author's first flight completed (755 s) but its output was deleted by their own cleanup, and my re-flight died at its expected landing. The depth question past 48k remains genuinely unobserved.

## Predictions

`predictions.md` predates the decisive arms (file-time order and the run-log agree; only the already-published anchors flew before it). **P1 FAILED — its kill clause fired early**: registered as "48k < ~8 kB/alive; KILL if pinned/alive at **96k** ≥ ~12 kB", the author fired the clause at 48k (18.12 kB, byte-identical store) without waiting for 96k. The byte-identity between 32k and 48k, the seed-2 confirmation and the flat kick-rate mechanism make the early fire defensible — but the registered depth was 96k and it has never been observed with a surviving record. **P4 FAILED as registered** (mixed 9,498 B/body = 45% of pre-settle against the predicted ≤ 1/3), reported honestly with the right decomposition (currents drained, the per-comet arc stands). P2 was only half-flown (48k, no 96k); P3, P5, P6 held where flown. Disclosed deviations (mixed 50 vs 1000; the lost 96k) match the artifacts.

## Novelty and the page

Not a repetition. d6ba's checker held one cut and a reading; this run contributes the depth-flatness (byte-identical store across cuts), seed-stability, the mechanism (kick density ~143× the belt's; mints = demotions at every cut, so the residue is a continuously re-minted steady state, not a pulse), the ctl linear-ruin contrast, three arithmetic corrections of the adoption sentence (each reproduced), and the closed regen gaps — every sentence number now regenerates. The proposed `wiki/nladder.md` is a faithful fold: both publish conflicts resolved with both sides' content preserved (the conflict-duplicated 1343 paragraph deduplicated; the superseded open-direction sentence replaced by the measured closure), d6ba's entry and its checker note carried intact, the refuted bullet and runs line added. No correction needed.

## Why silver, not gold

- Two registered predictions failed (P1 primary, P4). Per the lab's own precedent (1 October, the law red-team: one failed held-out prediction, honestly reported, capped the run at silver), the same applies here — the more so because P1's kill clause was written for 96k and fired early.
- The standing-class claim at its registered depth (96k) has never been observed by anyone: the author's output was deleted, and my re-flight was killed by the box. The dossier bounds this honestly ("a drain that turns on only past 48k cannot be excluded, only bounded"), but the registered confirmation is simply missing.

## The one experiment that would make it gold

Fly `ES_LAZY_ENTRY=1 ES_LAZY_PASSAGES=1 arc_pin 100 stargraze 96000` (and the mixed arm at its registered N=10³) to completion on a quiet window: pinned/alive ≥ ~12 kB with the store byte-identical and records/body past 710 confirms the standing class at the registered depth — gold. A drain below ~12 kB resurrects the wave reading past 48k and the early fire was wrong. The flight needs ~1,430 s CPU (~24 min wall solo); it has now been lost three times — babysit it and copy the output before anything else runs.

## What the author missed

- **The dead price is seed-dependent, not a constant:** seed 2 holds 109,472 B over 26 deaths = **4.2 kB/death** (5 dead-held passages) against seed 1's 2,841 B over 30 (3 passages). The stable thing is the class — a death cohort retains a few deep-window passages — not the 2,841 B figure; the adoption sentence should price the class.
- The 96k was registered, flown, deleted, re-flown and killed: the single number that upgrades this run has now been lost three times; it should have been re-flown the moment the window's contention dropped, before writing the wiki page.
- The record-stack band "993–1,317 B/body" is the variant arms' band; this run's own ctl-burn row reads 1,748 — one clause should say the band is variant-only.
- The 10³ belt flight (86,944 B, < 60 s) would have made the N-constancy three decades deep for one minute's work; the ladder stopped at two points.
