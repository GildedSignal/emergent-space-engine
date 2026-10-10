Grade: gold

**Abstract.** Claim: the co-orbital gold's premise fails on breakup clouds — an exact null plane in
Binet space, so the cone tier retains 99.99999% of pairs (37 TiB at 10⁶ fragments), element
triggers can't see it, phase neighbours churn (rank-4 misses 46% at N=4000, 97% in the blob),
while a shared-focus epoch-stream sort covers at-P encounters at ~3 checks each, flat in N.
Reproduced bit-identically; my adversarial cases (σ=0.05, e≈0.5–0.67 eccentric parents, tighter
belt) strengthened it (retention exactly 100%, rank-4 misses 75–92%). Gain: deletes quadratic
pair state for plane populations and re-routes the queued b-coorbital-cert build. Adoption:
focus-epoch streams plus a cone-probe trigger; the at-Q residue (14–39%) stays open.

1. **Reproduction.** `python3 breakup.py` in a clean copy: exit 0, 11.4 s, <200 MB; results.json bit-identical to the stored one except `load` and `runtime_s`. Every table number in dossier.md matches results.json exactly (I checked all 17 rows, including 7,997,999/7,998,000; 3744/8219 = 45.6%; churn 0.99/0.91/0.35; work/encounter 3.0/3.0/3.0/4.1/2.9; Q-shares 14.5/27.3/60.4/37.0/38.9%). The 37 TiB and 14.5–139 core-days rows follow arithmetically from 5×10¹¹ pairs at 80 B/pair and 2.5–24 µs/pair, and mirror the gold's own 40 TB accounting.

2. **Prediction record.** predictions.md (17:18:19) predates the final breakup.py (17:28:59) and results.json (17:31:57); patch.diff is empty (no repo edits). Held: P2 (plane residual 3.3e-16), P4 (zero at-P misses, flat ~3 checks/encounter), P3's formation control (67,796 encounters, 0 misses, max rank 2 — the gold's scene reproduced) and adjacency (median 1, max 6). Missed and honestly reported: P1's belt bound (16.8% vs <10%), P3's mixed-age magnitude (46% vs >80%; the blob phase hit 96.6%), P5 (cloud is 13–57× tighter than belt, not belt-like), P6 (0.14–0.39×, not within 2). No kill criterion triggered. The honest misses cut against tuning: a leaked prediction file would have them right. The physics correction of v1→v2 (d_min ≈ v0·|Δt|, churn not rank growth) is disclosed inline and is itself part of the result.

3. **Adversarial cases (mine, /tmp/chk/adv.py and follow-up).**
   - σ=0.05 (50× the author's dispersion), N=2000: cone retention exactly 1,999,000/1,999,000; plane residual 4.4e-16; rank-4 misses 92%; epoch stream 2.65 checks/encounter. The Kepler validation of the analytic window degrades to 33% max rel err on d (vs 0.4% near-circular) — still ≪ b, so encounter membership flips only in a thin band at the threshold.
   - Bound eccentric parents (breakup at periapsis of e=0.2, v=1.22; at apoapsis of e=0.5, v=0.577; fragments e≈0.5 and 0.67): retention exactly 100%, plane residual 4–9e-16, epoch stream 2.9–3.0 checks/encounter with v-scaled window, rank-4 misses 75–84%. The author's caveat (ii) resolves in favour of the claim: the mechanism is exact away from the tested regime and the certificate failure worsens.
   - Tighter belt (awidth=0.05): retention 55.0% — the dossier's parenthetical "55%" is real, though not regenerable from breakup.py as shipped (see missed).
   - 3D (argued, not run): all fragment planes share only the line P–primary, so pairs share exactly P; second crossings are codimension-2. Retention-100% holds a fortiori and the at-P stream covers ~all encounters — the fix is stronger in the 3D the game actually runs.
   - Controls on both sides hold: formation (the gold's scene) 0 misses; belt 16.8% (not ~100%, so the kill criterion for the inversion did not fire).

4. **Novelty.** docs/law.md (encounters, 30 September) documents the Binet cone as the crossing condition — known. New here: the null-plane corollary (a single-point population lies on a plane whose normal is null, so the cone retains everything — the filter is structurally blind to the game's most common concentrated scene), the phase-churn kill of the rank-4 certificate outside formations, the cone-probe trigger, and the epoch-stream-at-focus certificate. No HISTORY entry or doc mentions breakup clouds (grep over docs/ and lab/: only this run). It attacks the real queued spec (lab/lenses/b-coorbital-cert.md: rank-4 at O(n·k) with a dimensionless concentration trigger), not a strawman — the brief's test scenes (gold scenes + dense ring) contain no breakup cloud, exactly the gap this run exposes.

5. **Goal fit.** The board's top scaling risk (5 October): candidate pairs per body grow with N; candidate work must track real encounters. This run shows the cone tier cannot reduce candidates for plane populations (100% retention, exact) and that real at-P work is trackable at 3 checks/encounter — 10⁶ fragments go from 5×10¹¹ pair-state to O(N log N) sorts per fraction of an orbit. PRINCIPLES 32 ("under the right representation many symmetries can appear"): the null plane is the symmetry, found by changing the question; principle 33: the cloud resolves at its focus, not in pairwise space. "A failed expectation is not a failed method": the run kills the certificate's domain, not the encounters design — and hands it the focus representation.

**What the author missed.**
- The 55% tighter-belt number is not emitted by breakup.py; "both reported" overstates (results.json holds only 16.8%). I regenerated it (55.0% at awidth=0.05), so the number stands, but the shipped code does not regenerate it — the exact defect that sank earlier silvers.
- "0 misses at every N" for the epoch stream is structural (the truth is the same stream); its independent validation is P7 only, and the window error's growth with dispersion/eccentricity (0.4% → 33%) was unmeasured until I ran it.
- "Misses 46% of real encounters" should read "of at-P encounters"; over all encounters (including at-Q) it is ≥ ~33% at N=4000. Direction unaffected.
- The at-Q stream's possible concentration (θ_Q = 2·atan2(ΔW,ΔV), noted then dropped) is the obvious next probe: if Q directions cluster for breakup clouds, a second focus stream closes most of the 14–39% residue and the certificate becomes complete; the author measured the share but not the clustering.
- 3D was flagged but not run; the analytic argument (and my reading of it) says it strengthens both the kill and the fix.
