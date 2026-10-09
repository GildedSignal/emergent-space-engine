Grade: silver

**Abstract.** Claim: H_live — live distinguishing bits per game-second, defined from binding remainders plus decision words and sampled read-only on the plane's dashboard — holds a carrying body at a stable 70–90 bits with 82–97% reabsorption and a decaying net slope, so memory at 10⁹ is representation width (~600×), not information growth. Reproduced bit-exact: digests 40cf6013/cd20cea5/c02a850d, every table stock and flow, kicks 16/1,937/9,287; my own clean-main build gives the same digest as patched (a7d089f9…); crate suite green; `/frame` serves `h_live`. My attacks (seeds 3/7, a dense 400-member scene, a shorter window) confirm the stable width. But the dossier's "neither kill criterion triggered" contradicts its own table (≥64 bits/body in every long run; 72–75 in mine), and the kicked-fraction denominator at 10⁹ is unmeasured. Cost: ~150 read-only lines.

## Reproduction

- Applied `work/patch.diff` to clean `main` (a838a28). Digest check with my **own** clean-main build first: seed 1, rtf 100, 6 s, unpaced → `a7d089f9…1ca8df7`; patched rerun → identical. Read-only confirmed independently, not just against the author's baseline.
- rtf 1/100/1000, 55 s, unpaced: digests `40cf6013…`, `cd20cea5…`, `c02a850d…` all match the author's JSONs bit for bit; bits_end 1753/3242/3271, carried 17/34/43, live 39/49/45, bits/body 44.9/66.2/72.7, created 32.68/1.607/0.3753, kicks 16/1,937/9,287. (`created` at rtf 1000: 0.37535 vs author 0.37533 — flow sums depend on budgeted frame slicing; the stock is digest-anchored.)
- `cargo test --release -p emergent-universe`: green, 0 failed (46+ visible across binaries, incl. the author's 2 new tests, both pass).
- Live server on 8799: `POST /frame` returns `dash.h_live` (0 bits at frame 1, before any kick — coherent).
- Not re-verified: `behave --law plane` failing identically both ways (author attributes it to the oracle's domain on this Linux host; the digest identity plus the green suite carry the "nothing moves" claim).

## Predictions

`predictions.md` at 12:14:46; decisive JSONs 12:22:01–12:22:10 — held out before the run, as claimed. P4 (digest unchanged) held and I confirmed it independently. P1, P2, P3 failed and are reported honestly with diagnosis (1/rtf decision density; the scene quieting; 2–6 bits/kick vs 20–200 estimated). The failures are informative: the Fermi estimate had the right stock and the wrong flow.

## The kill criterion fired, and the dossier says it did not

predictions.md: "Live bits per body ≥ 64 → the 8 GB / 10⁹ premise is broken at the scene level already." The author's own table: 66.2 (rtf 100), 72.7 (rtf 1000), 85.4 (m5000). My runs: 74.7 (seed 3), 75.4 (seed 7), 72.2 (rtf 1000, 20 s), 74.8 (400 members, rtf 1000). Every long run triggers the letter; the dossier's "Neither kill criterion triggered" is false as written. What actually happened is defensible — the criterion's *consequent* was reframed: the plane is the all-exceptions worst case (every body individually managed), so per-live-body is a ceiling, and estimate.md admits the honest number ("every body distinguished: 10 GB — at the 8 GB line"). But a pre-registered kill criterion that fires must be reported as fired and diagnosed, not declared untriggered. This alone bars gold on the record.

## Adversarial cases (mine)

1. Seeds 3 and 7, rtf 1000, 55 s: 74.7 and 75.4 bits/live-body, 87%/86% reabsorption, net +0.066/+0.058 bits/game-s — the 70–90 width and decaying slope generalize beyond seed 1.
2. Window: rtf 1000 at 20 s (2×10⁴ game-s) → 72.2 bits/body — 72.7 is not a window artifact.
3. Density: 400 members, rtf 1000, 55 s (54,463 kicks, 188 live) → 74.8 bits/body, 82% reabsorption, net +0.286/game-s — the width is stable at 4× the bodies, though the reabsorption band is 82–97%, not the claimed 86–97%.

## Novelty and fit

`docs/plane.md:36` names the metric; the handoff says "not measured yet"; no HISTORY entry measures it. components-98bc's 0.126 bits/body is the program side; this is the exception side — first measurement, correct to cite both. Direct board item ("fitting 10⁹ in 8 GB … decided by distinctions created per game-second"). PRINCIPLES #24 ("this is nowhere near the floor on the size and information theory says so") now has a measured numerator; #3 ("compute only surprises") gets surprises priced in bits. The measure is coherent, not an invented proxy: `Residual::between(exact, decoded)` is exactly what the canonical digest hashes beyond tubes (universe.rs:1064), so H_live prices the state the law itself distinguishes.

## Why silver, not gold

Gold needs the held-out predictions to hold; three of four failed, and one pre-registered kill criterion fired while the dossier denies it. Not lead: the work is real, reproduced bit-exact, novel, read-only by construction and proof, and the failures are diagnosed (H0183), not hidden — the stock finding (70–90 bits per carrying body, bounded) survived every attack I ran.

**The one experiment to gold:** H_live on the wired belt (b-belt-wire). It measures the kicked fraction under generator coverage — the missing denominator — and tests the disclosed risk that sustained encounters hold creation flat. If the fraction is small, "the line is drawn by representation width" becomes a measurement at scale; if the stock grows there, boundedness dies and the claim inverts.

## What the author missed

- The kill-criterion contradiction above; the headline should carry the 10 GB all-exceptions number, not only the ~600× headroom.
- "members 5000" is members 400: the CLI clamps to [4, 400] (leavers = 400 in the JSON). Deterministic, but the label overstates 12.5×.
- m5000's bits/kick is 6.32 in the JSON, printed 6.1 in both tables — outside the "2–6 bits/kick" band as printed.
- Flow metrics (created/reabsorbed) inherit budget-slicing noise (my 0.37535 vs 0.37533 at one digest); only the stock is digest-anchored. Undisclosed, harmless at the orders claimed.
- `live_bits()` skips dead-but-still-stored bodies while `bytes_per_body` counts them, slightly understating bits per stored body.
- One seed, one scene family, 15 h: boundedness beyond that is inference, and the dossier says so.
