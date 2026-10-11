# Predictions (written before the decisive run)

Claim under test: the encounter machinery needs **zero per-body state beyond the tube's 16 bytes**
(key index, ϖ, t_p) and **one order** — the doll's store sorted by (key, phase). The Binet cone's
U-axis is the key order (per-key constants U, e, period come from the memo entry), and the
co-orbital phase rank is the within-key phase order. `crates/encounters`' `Body` (80 B/body) plus
its `Sorted` index is a second per-body structure that this deletes.

Quantization for the float replica: a-cells of width (a_hi−a_lo)/1024, e-cells of width
e_range/512. Conservative per-key radial range [a_lo(1−e_hi), a_hi(1+e_hi)].

Cases I have NOT tuned on (held out):

1. **Belt zero-miss (correctness of the conservative key test).** On spread belts
   (my specs at n=600, plus verify-set "c" scenes), every pair of the crate's
   `radial_pairs` truth tier lies in the lattice's key-overlap candidate set:
   **misses = 0** on every spec. If any pair is missing, the conservative cell range is
   wrong and the claim dies.
2. **Inflation.** The lattice's candidate count (key-level overlap, angle-free) is at most
   **~4×** the exact per-body cone count on the same belts (the quantization slack roughly
   doubles each side's reach; the angle-free test adds less than 2× on spread ϖ).
   If it is >10×, the key quantum is too coarse for the cone tier and the unification
   buys noise.
3. **Co-orbital phase rank (the crate's own adversarial spec, not mine).** On
   `coorbital` (n=300, a∈[1,1.0001], 50 orbits) every real encounter (truth, min distance
   < ρ) lies within mean-longitude rank **≤ 8** of its partner at encounter time; I expect
   ≥ 95% within rank 4 (taleb-09b5's number on its own scene). On `equal-period-keys`
   (spread ϖ on 3 keys) I expect the rank rule to **miss** some encounters
   (crossing-ellipse conjunctions between distant phases, birth-fixed by equal periods):
   those need the same-key exact check at key entry, paid once, not per orbit. If the rank
   rule misses nothing there either, the same-key tier is simpler than I claim.
4. **Formation scaling (concentrated workload, the taleb-09b5 regime).** On one-key
   formations (n=2^10..2^14, clustered ϖ, arc of phases, period spread 2×10⁻⁵):
   lattice candidates grow **linearly** in n (~2K·n at K=4, i.e. ~9n pairs), while the
   crate's tier (`radial_pairs`, all pairs overlap) is n(n−1)/2. Work per real encounter:
   lattice constant (~10²), the quadratic tier growing ∝ n (≥16× worse at 2^14 than at
   2^10). If the lattice's zero-miss fails on the formation truth at n=256, the phase-rank
   rule does not survive concentration and the claim dies.
5. **Memory (arithmetic, not run).** Per body beyond the tube: crate 80 B (`Body`) + order
   ≥4 B vs lattice 0 B. At 10⁹ bodies the second structure alone is ~84 GB against an
   8 GB machine; the tube lattice adds nothing (B18's bar: no second full copy).

Kill criteria: any miss in (1) kills the conservative-key claim; a rank blow-up in (3)
kills the co-orbital unification; inflation >10× in (2) makes it not worth adopting.
