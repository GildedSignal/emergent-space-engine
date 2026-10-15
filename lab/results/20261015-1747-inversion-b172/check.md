Grade: silver

**Abstract.** Claim: the twice-checked "no bounded cap serves burn" law is the uniform belt's geometry — the same flight concentrated into co-orbital formations holds 1.014×dem at cap 4,096 (N/24) where the belt needs 131,072. Everything reproduces bit-exact (runner regen; belt anchors = f55d's published branch digests/ratios; my 12 flights all digest-identical), and the collapse holds beyond the domain: K=1 mega-fleet 1.004, seed 5 1.016, N=2×10⁵ 1.011. But my 48k probe falsifies the adoption claim: the formation reads 29.3×dem at cap 4,096 (belt 48.5), compile 28.6 s, and its depth knee is the mint bill exactly (273,200 → 1.000, 0 evictions). The revival lasts under one wave period (~27k game-s); adopt a small cap only for concentrated sub-wave episodes. Not gold as claimed.

## Reproduction

- The runner's `regen.sh` exited 0 with "anchors + identity OK"; every dossier number regenerates (7.226/6.953/1.000, 1.244/2.997, 810,531 = 1,528,451−717,920, fills 1.66 M vs 617 k, promote 4.72 s vs 0.54 s; walls differ only in noise: 23.2 vs 23.3, 13.3-13.7 vs 13.4-14.4).
- I applied `work/patch.diff` to a clean tree myself. The instrument is f55d's verbatim with the scene knob env-gated (`scenario.rs::ladder_ship_form`; locals and the belt branch are `ladder_ship` verbatim; when unset, nothing changes). Belt ctl digests `5caeb1b6…` (10⁴) and `d3542eea…` (10⁵) equal f55d's, verified against its published branch (`git show origin/claude/lab-…-f55d:…/dossier.md`).
- Scene-invariance of the control re-confirmed on new arms: kicks 132,278 / opens 100,471 / demotions 130,187 identical on belt, K=100, K=10 and K=1; seed 5's bill 132,755 equals f55d's belt seed-5 bill.

## Predictions

Pre-registration is credible (mtime order: `predictions.md` 17 m before `fly.sh` 14 m before first flights; the registered "lives, weakly" diverges honestly from the outcome "lives, strongly"; the P3 razor miss is disclosed). Two defects: **P1's hit-fraction clause failed and was not reported** — registered "cap 4,096 holds ratio ≤ 1.5 with hit fraction ≥ 0.85", actual hit fraction 0.786 (484,189/616,250); and `author-final.md` says "26 flights" where the battery writes 23 arms. P2, P4 held exactly.

## Adversarial (all outside the author's domain; all digest-identical to their scene ctl; seed/N/cut/K axes)

1. **K=1 (one 10⁵ mega-fleet — the author's own named counter-example):** cap 4,096 → 1.004 (130,669/130,187), 13.1 s, rss 375 MB. The collapse is stronger at K=1 than K=100.
2. **Seed 5, K=100:** 1.016 (134,845/132,755).
3. **N=2×10⁵, K=100, matched cut:** 1.011 at cap 4,096 (N/49). The matched-cut collapse extends a decade in N.
4. **Depth, 48k game-s (the un-flown arm — decisive):** formation cap 4,096 → **29.3×dem** (7,928,202/270,979), cap 16,384 → 28.6; belt at the same cut/cap → 48.5 (13,133,609); formation promote compile 28.6 s (0.54 at 20k), wall 84.7 s vs ctl 41.2 s (+106%). And the formation's 48k knee is the mint bill again: cap 273,200 holds exactly 1.000 with 0 evictions. **The dossier's registered expectation ("extra promotions track evicted re-reads, which stay window-local at any depth") is falsified**: past one wave period the wave recurrence re-imposes f55d's one-demotion-wave reuse distance, scene-invariantly. The mechanism sentence ("reuse distance = the kick window's population, not N") is refuted in its general form; it describes one wave only.

## Novelty

Genuine: the published page's open direction 4 named this exact falsifier "unmeasured"; no prior run varied scene geometry on the seam (0619/f55d varied N, seed, cut, coast/burn only); the 20261006 encounters gold used co-orbital concentration against a different bottleneck (the pairwise tier). This run is the first measurement of geometry on the knee, and its belt arms regenerate the record exactly.

## The page

Corrected in place: a checker bracket under the run's entry (depth numbers, K=1/seed/N confirmations); the Refuted line scoped to "the matched cut only… the sentence stands at depth in every scene"; open direction 5(a) marked measured-and-failed with the corrected adoption horizon. The "a few MB at 10⁹" sentence must carry the one-wave-period horizon.

## Goal fit

Moves the board's memory/live-bodies seam by correcting the record's law, and the work honours PRINCIPLES: "behaviours matter, not continuum fidelity" (promotion floor as the behaviour, bit-identity as the certificate) and "A failed expectation is not automatically a failed method: diagnose which one broke" — the diagnosis here (the wave recurrence) is exactly what the next run needs. But gold asks for held-out predictions held and adoption within one step: the headline adoption claim ("a bounded burn cap revives for exactly the fleet/battle workloads the game wants", "~1.4 TB ⇒ a few MB") is falsified at two wave periods — a battle is a long-horizon workload, and shipping the small cap would cost 29× promotions, ~50× compile and 2× wall at 48k. The dossier itself pre-offered silver on this arm; I flew it, and it broke.

## The one experiment that would make it gold

Land the depth arms in the run's own regen battery (my probes live in `/tmp/checker-b172/`, not regenerable from the run folder) and re-scope the claim to what is now fully measured: *the knee is the re-read reuse distance — concentration collapses it within one wave period (≤ N/24), the horizon's mint bill re-imposes it at every depth and scene* — with the adoption rule split (small cap for concentrated sub-wave episodes; mint-bill cap otherwise). The matched-fills control (diffuse-but-clumped belt) would additionally pin the intra-wave mechanism.

## What the author missed

- **Deep play** — the named open edge, registered with the wrong expectation, and it inverts the adoption claim (above).
- The P1 hit-fraction clause failed silently (0.786 vs ≥ 0.85 registered).
- The read stream is not scene-invariant (617 k fills vs the belt's 1.66 M at identical demotions) — disclosed in the lens section, but the wiki headline's "the same event stream" phrasing could mislead; the fills asymmetry is part of what concentration changes, and the matched-fills control that would separate volume from locality was named but not flown.
- The mechanism sentence rested on two K values plus an inference; one depth flight (mine) killed its general form — the cheapest falsifying test was the depth arm, and it was left unflown while 23 matched-cut arms flew.
