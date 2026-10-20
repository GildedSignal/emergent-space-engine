# Check2 — 20261020-1116-second-20261020-1002-inversion-0a46-8365 (blind to checker 1)

Grade: gold

**Abstract.** The checker-named gold experiment inverts 0a46's lever: the 3× cost alternation is the comb's PAYLOAD, not the served path. Each belt ship's clock (27.9k gs) emits a kick comb and a boundary comb half a period apart (step.rs:717-718), ~105k kicks and ~105k boundaries alternating every 13.9k gs. Coast proves it — player-class flat 0.46 s, walls 5.6/1.6 — at 45.6 µs/kick vs 8.6 µs/boundary (honest solve 45.3 vs 5.9 = 7.7×). A ≥4k birth stagger kills the freeze (703–1231 → 40 ms) at an identical kick stream; phase spread cannot equalize walls (bands 1.7–2.0×). 1e9 re-priced: ~12.8 h kick + ~2.4 h boundary comb per period. Adoption: re-pricing and lever-kill now; the stagger a priced prophylaxis.

## Reproduction

`regen.sh` exit 0 (runner), re-flown fresh, no CSV reuse; I verified the tree was restored after (patch absent, `birth_stagger_ticks` grep 0) and that the binary at `lab-target-2` is the patched build (escsv smoke, class order [planet,moon,ship,player,fleet]). Every **count** regenerates from the work/ CSVs, re-derived independently:

- era payload: burn kicks 105,780/6,131/104,930/5,905, boundaries 5,924/105,565/6,020/102,954; coast the mirror image — the dossier table to ±0.1% (draws, disclosed).
- coast split: odd-era cn2 9.23 s / 202,475 kicks = **45.6 µs/kick**; even-era 1.79 s / 208,949 boundaries = **8.57 µs** — the dossier's 45.9/8.6 exactly; even-boundary count 208,949 digit-for-digit.
- arrivals 0.400/0.717/0.415/0.702/0.373/0.737/0.393/0.695 ev/body — exact vs 0a46's record (P5 held).
- crest concentration 49% → 37% (4k) → 16% (14k); kick rate 4.889e-5 identical in M1/S1/S2 ladder lines; anchor 822.1 ms, inside 811–948; freeze kill regenerates (703 → 39.6 ms max; worst frame 703 ms carries k=14,325, it2=0, cn3=702 — the nested-pull signature).
- mechanism in code, verified: `step.rs:717-718` inserts `Boundary` at `t+full/2`, `Kick` at `t+full` (the half-period comb); `universe.rs:770` (`pull_ships` inside the player's `resolve_body`) with `:799-803` timing the whole call into `cost_ns[class]` — the CSV's cn[3]/it[3] accounting is as claimed.

## Adversarial arms (mine, three, two outside the author's grid)

1. **`ES_STAGGER_GS=28000`, burn 1e5** — the payload-interleave prescription the dossier names but never flew. Result: payload mix **k-frac 0.50 in every 2k bin** from gs 28k, arrivals flat ~20.2k/bin, walls flat at 0.72 s/bin across gs 42–58k (**1.06×** max/min; S2 bands 1.72×, S1 ~3.7×), freeze dead (40.9 ms), repay bumps still at 34–40k as claimed. Constructive confirmation: interleave, not phase width, equalizes cost — a mixed bin prices at the mean of the bands, the payload law's fingerprint. (Side effect, disclosed mechanism: a 28k first-interval stretch defers ~a comb per ship out of the 60k window — kick rate 4.269e-5 in-window; steady-state rate unchanged.)
2. **coast + stagger 14k** (author staggered burn only): arrivals flat, walls still band **1.98×** (kick-band 1.02 vs boundary-band 0.51 s/bin at identical arrivals 20,356 vs 20,253). Payload banding is structural and per-ship, on the cleanest scene.
3. **seed 2, burn, no stagger**: comb alternation reproduces exactly (106,890/7,421/106,261/7,261 kicks; 6,893/106,536/7,364/104,222 boundaries), walls 5.7/2.4/5.7/1.7 s, freeze 734 ms with it2=0/cn3=733, onset at the same gs ≈ 14.0–14.2k. Seed-robust.

All three arms land inside the run's story; none breaks it; one (the 28k interleave) completes it.

## Predictions

P1 held (cn3 carries 85% of era1−era2 wall on the re-flight too: 2.8 of 3.3 s). P2 refuted on its main branch, branch B held — that refutation **is** the finding (the coast carrier is cn2, 5.2× at flat cn3), honestly reported. P3 split exactly as the dossier says, and the failures regenerate (S1 max bin 0.547 > 0.50 bar; concentration 1.33× < 2×; walls 3.7× > 1.6×). P4 held on events (−2.4%/−12.6%) and identical kick rate; the wall half does not regenerate (below). P5 held exactly.

Pre-registration provability: the folder is untracked and regen overwrote the first-draw CSVs (both disclosed), so file-time proof is gone. The evidence it was genuine is the reported failures against pre-set numeric bars — you do not post-hoc register bars your data then misses.

## Corrections (page fixed in place; none touch the mechanism)

1. **8.6 µs/boundary is contaminated.** It attributes ALL even-era cn2 to boundaries, but even eras carry ~6k kicks at ~45 µs (~30% of the even-era cost). The honest 4-era least-squares on coast gives **45.3 µs/kick vs 5.9 µs/boundary = 7.7×** — the true split is larger than the quoted 5.3×. The error direction favors the claim; 1e9 boundary-comb bill ≈ 1.6–2.4 h either way.
2. **S2's walls are not flat.** "(flat + repay bumps)" overstates: gs 26–58k bands **1.72×** (kick-band 1.05 vs boundary-band 0.61 s/bin) at flat arrivals, 1.98× on my coast arm. Consistent with the mechanism (a 14k spread separates payloads into alternating 14k bands, it does not interleave), but the gloss was wrong.
3. **"−17% total wall" does not regenerate.** Re-flown ladder wall_s: M1 37.2, S1 38.3, S2 37.3 s — ±0%. The first draw's 45.0 s carried the heavier 1231-ms freeze chain. The regenerable gains are the worst-frame kill (17–30×) and the identical stream; the p99 is unchanged (16.7 vs 15.5/16.5 ms — the repay channel owns it, as the dossier itself says).
4. **Era-1's 86 µs/nested-kick is a draw.** Re-flight: 54 µs (3.48 s/64,333) vs era-3's 63 µs — the first-kick-rebind reading ([INFERENCE], flagged as such) is unsupported on this draw.
5. Boundary share: 49.7% burn / 50.7% coast on regen — the author already corrected 46% in the page.

## Novelty and goal fit

No HISTORY entry holds a kick/boundary payload split (nearest: 0a46, whose "3× served-path lever" this run inverts; birth-stagger's element-error bill is a different question — accuracy, not arrival cost). ca63's 13.2 h/wave is re-identified as the kick comb, with a new ~2.4 h boundary-comb term (at 1e9, ~50% of stream events carrying no kick — PRINCIPLES #3: "Compute only surprises": 105k certificates per comb that nobody reads). "Make era 1 serve like era 2" dies as a scheduling lever — no scheduler can buy a payload split. Board #1 (bodies in the flyable engine) and #12 (the p99; freeze 17–30× kill at zero stream cost). Fit with #19: the alternating-cost mystery was two combs wearing one arrival envelope — the fix was the representation, not the schedule.

## Grade rationale

Reproduced (every count; walls disclosed draws, counts bit-structure); pre-registered with the failures carrying the finding; the held-out domain extended by three fresh arms, all confirming, one constructively completing the prescription; moves the top board bottleneck by re-pricing the 1e9 wave (12.8 h + 2.4 h alternating, forever) and killing a wrong premise that was about to misdirect scheduling work; adoptable now as a record correction, with the stagger a priced one-step prophylaxis. The five corrections above are reporting-level, not mechanism-level.

## What the author missed

- The 28k interleave arm: the prescription was named and one flight from proof — flown here, it works (k-frac 0.50/bin, walls 1.06×).
- The honest least-squares solve (would have strengthened 5.3× to 7.7×).
- The S2 banding (k and bo per bin were in the CSV; summing them per bin shows the 14k spread separates rather than interleaves).
- The −17% wall claim needed the ±same-box re-flight the author's own P4 discipline demands for walls.
- Domain still one scene at one N per arm (seed 2 and coast-stagger added here; the payload split at other N rests on 0a46's checker's µs/ev alternation at 5e4/1.5e5, consistent but not decomposed).
- Memory: the author's arms peak 1.95–1.99 GB against the 2 GB kill line — closer than the dossier admits; mine (1.95 GB) survived.
