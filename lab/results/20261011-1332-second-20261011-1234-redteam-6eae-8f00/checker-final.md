Working...
The pyc regeneration is a bytecode-cache side effect of my in-place `diag.py` verification run (compiled from the author's own final source; no record content affected — the original 14:13 cache was stale against the final 14:23 source and is not recoverable either way). I'm disclosing it here rather than touching the folder further. The check is complete.

## Check complete: `Grade: silver`

**Reproduction (clean tree, /tmp scratch, no patch to apply):** all four scripts regenerate their JSONs **bit-for-bit** — `view_images.py` (270 s), `ladder.py` (360 s), `bands.py`, `diag.py`. `bands.json` is also identical to the original run's shipped record; `view_images.json` differs from it in `control_weak_field` only, exactly as claimed. The repaired control: bend 0.0203041, h-converged, vs the Schwarzschild 3PN series 0.0202999 → **2.09×10⁻⁴ relative**; the "0.018 = 6h" quantization diagnosis is exact, and the original code confirms the born-below-escape-cut defect.

**Held-out:** predictions.md (14:02) precedes every output (14:08–14:27). V1, V2, L1, L2, J1–J3 held. L3–L5 and L7 **missed by 5–100×** (one direction, root-caused to the first checker's 180/π unit artifact — which this run caught: their absolutes = the author's × 57.2958, verified by my instrument). Honest, but the gold bar reads "the held-out predictions held".

**Attack (independent DOP853 instrument, own event/bisection machinery):**
1. Aligned validation case matches exactly (141.111°, μ 0.2117, rel_k1 0.001392).
2. Off-aligned exterior emitters: partner rels 0.119/0.238/0.507 at φ_e 2.0/2.4/2.8, windings ≤ 0.0018; the 100M band edge [1.78, π] confirmed on **both** sides (φ_e=1.5 → 0.0121 invisible; φ_e=2.5 → 0.0948 visible).
3. The scope attack — interior emitters (r_e < r_o), which the run never tests and its first-crossing instrument **cannot represent**: 8 geometries including r_e near the photon sphere. The k=0 pair remains the only visible structure; no winding approaches 1/50; near tangency the direct image is squeezed and the mirror partner can be brightest. The conclusion survives — on the checker's evidence, not the run's.

**The one experiment for gold:** the geometry ladder — all-crossings instrument, sweep (r_o, r_e) including r_e < r_o, thresholds 1/50 and 1/100, band fractions and cutoff as functions of geometry rather than one emitter radius per observer radius.

**What the author missed:** the r_e dimension entirely (never varied, interior emitters structurally invisible to the shipped instrument); "direct always brightest" fails near interior tangency; the 1/100 margin is only 1.11× at 3.2M; the band fractions conflate r_o with a changing r_e/r_o ratio; branch cost still unmeasured.

`check.md` written to the run folder; nothing else in it changed (the disclosed pyc cache aside). No git operations performed.
