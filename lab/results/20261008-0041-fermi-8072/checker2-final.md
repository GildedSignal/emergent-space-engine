Working...
Check complete. `check2.md` written to the run folder; nothing else there touched (all my experiments ran in `/tmp/check2`).

**Verdict: gold.**

What I did and found:

**Reproduction** — clean tree, empty patch, every dossier command rerun from scratch (A1/A2/B/C/D, walls 170–341 s). All four stored snapshot sets are **bit-equal** to my reruns, and the shipped `analyze.py` regenerates every headline number: f_chaos 12.5% (48% in the 2:1 band), 100% birth-cell scarring, P3 KS(a) 0.0305 vs noise 0.0225, scatter 17/19/21, forced vector 0.001→0.043. I regenerated both controls independently (no-Jupiter: exactly 0.0; dt-refinement: dt-independent).

**Predictions** — mtime-verified pre-registration (00:48 vs decisive runs 00:57–00:59). P2 and the decisive P3 held on every metric; P1 held after the disclosed marker redefinition; P4's gap-growth arm failed and was reported honestly with the right diagnosis. Undisclosed: the run is 25% short of the pre-registered 95 kyr horizon.

**My attacks** — fine-bin histograms and resonance-band counts pass within the true-vs-true noise band; a full hotter-belt pipeline (σ_e = 0.1, fresh seed, 71 kyr) also passes globally (KS 0.0185/0.0205, f_chaos 17.5 vs 17.0%). Two boundary findings the author missed: a directional 2:1-band e-bias in re-programmed belts (+10–13% mean e, consistent across both scenes) and a ~2σ inner-edge deficit from the smoothed histogram — "indistinguishable" holds at global one-point level only. One artifact defect: `metrics.json`'s `f_chaos_series` field is stale (unreachable from the shipped code), though the code itself regenerates the quoted flatness.

**Gold because** it measures the named-unmeasured H_live bottleneck, kills the birth-program+scars premise for belts (100% scarring by 1.5 kyr), converts the 10⁹-in-8 GB plan from 16 GB (fails) to ~2 GB / tens of MB, and is adoptable in one shipmem spec step.
