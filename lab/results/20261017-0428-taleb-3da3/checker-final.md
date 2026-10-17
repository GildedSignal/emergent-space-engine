Working...
Check complete. Deliverables: `lab/results/20261017-0428-taleb-3da3/check.md` written, and the author's page corrected in place (three checker-attributed additions; nothing else in the run folder touched).

**Grade: silver.**

**Reproduced (regen exit 0, my own runs):**
- P1 bit-for-bit: digests identical across arms and to the dossier at S0/S2/S3 (49f5fc2b…, f0695d29…, 5bf2c3f5…). The certificate claim is machine-confirmed.
- S3 mechanism: walls 74.1/109.9/175.1 s (author 73.9/133.5/189.4 — same ordering), merges/splits 1111/71, 608/237, 1783/993 (author 1136/72, 598/252, 1735/919), one region everywhere, rollbacks 8/8/9, never recurring.
- Instrument and surgery verified: tax.rs byte-identical to the prior gold's except the `arm()` naming; alloc.rs delta is exactly `ES_CAP`; default-off is shipped verbatim.

**Where the dossier overstates:** the "2.3–3.6× wasted ops in every paired run" headline is draw-fragile — my regen drew 1.30× (cap16 0.33×) and shipped's own within-arm spread is 0.56–2.06M (3.7×). The kill survives on walls + churn (the dossier pre-hedges this itself), the number doesn't. S2 shipped also drew escal_max 512 (9 rollbacks) vs the table's 256 — the acknowledged one-draw noise.

**My adversarial cases:** (1) margin 0.5 — all arms finish, digests equal, shipped latches E=2¹⁷ wedge-free (extends "no reachable ruin" far above the wiki's 2⁶–2⁸ band); (2) frames at 1,408 — no player-visible separation (closes the author's admitted gap with a nil); (3) **28,160 bodies, outside the author's range** (their own commented stretch): cap64 finished 57.2 s (6,902 regions) while shipped DNF'd 300 s in the same back-to-back window — the exact quiet-heavy regime the author named as the hole and did not run. One confounded draw (my clean-load rerun is void — my own process-group teardown killed it), but it bounds the "killed / not adoptable / the caps prolong" verdict to the conflict-wave regime, and the prior box's ~149 s shipped datum was razor-thin against its own timeout with no region count recorded.

**Why silver, not gold:** P2/P3 failed on the letter of "held-out predictions held", and the general kill verdict is one controlled experiment — the author's own archipelago probe, now with a first counter-datum — from settled. Why not lead: the scoped claim is fully reproduced, closes the page's named open direction 1 in its regime, and is adoptable as "ship nothing" today.
