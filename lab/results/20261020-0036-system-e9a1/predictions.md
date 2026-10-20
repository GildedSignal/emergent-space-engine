# Predictions (written before the decisive flights)

Probe: `ES_CONE_PROBE=1`, print-only (env-gated eprintln in `Scan::compute` and `Universe::pull_ships`; off = shipped bits). Scenes: the shipped nladder arms, seed 1, rtf 1000, 12 ms budget, 20 s wall: `100000 burn`, `100000 coast` (control), `200000 burn` (held-out rung).

The claim under test: the scan's read set (candidates held per scan) and the pull that feeds it (ships materialized before the player's item) are one object bounded by the pair's own light cone over the scan's interval: `|d| > |w| + near` proves no encounter (triangle inequality on the same linear relative motion the predicate tests).

- **P1 (the read set at the wall's rung):** in the burn arms' root-doll scans, median candidates/scan ≥ 5×10⁴ (the belt: the radial apsidal filter passes it; cf. 7b6f's scan_cand_max ≈ N).
- **P2 (the certificate covers it):** skip_cert fraction ≥ 99.9% of candidates in those scans, at 10⁵ and at 2×10⁵.
- **P3 (never-miss, exactness):** VIOLATION lines = 0 in every arm. A single encounter inside the skipped set falsifies the certificate and the whole unification.
- **P4 (the margin is wide):** min_slack_near (the closest any rejected pair comes to the cone, in units of the encounter radius 2¹⁰·reach) ≥ 10³ in the burn arms.
- **P5 (the pull is the same object):** root pull waves (`children_only=false`) carry pulled ≥ 10³ per player item around the first kick wave (cc9d's gulp), while the same flight's cone passers per scan (cands − skip_cert) ≤ 10². The pull/cone ratio ≥ 10³: almost everything the pull materializes, the scan provably never reads.
- **P6 (coast control):** in coast the player stays in Home's doll: no large `children_only=false` pulls; cone_scan cands ≤ 10³ (the locals), and skip_cert ≥ 90% there too.

Failure handling: P3 failing kills the claim outright. P2/P4 failing on the letter but not the direction (say 95% or slack 30) downgrades the deletion factor but not the unification; P1 failing means the wall's candidates are not the belt and the page's afff reading extends to the wall rungs unchanged.
