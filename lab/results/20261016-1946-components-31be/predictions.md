# Predictions (pre-registered before the decisive run)

Question: what is the sound yield of a mean-longitude band certificate on the belt-bin
scan answer, measured on the shipped flights (component: the player scan's candidate
tier, `crates/universe/src/radial.rs` + `encounter.rs::Scan::compute`)?

The certificate (necessary condition, sound by construction): a pair can hit only if
their mean-longitude difference `Δλ̄(0) + (n_j − n_p)·t` for t ∈ [0, h] comes within
`νmax(e_j) + νmax(e_p) + δ_ang` of a whole turn, where νmax(e) = max_M |ν(M) − M|
(≈ 2e + O(e²)) and δ_ang = (2^10·reach + (|v_j|+|v_p|)h)/r. Everything from the read
state; the probe pays the shipped 4 µs read per candidate to measure the distribution.

Cases NOT tuned on (held out): belt bodies at the band edges (1/10 and 9/10 through the
belt id range), the after-flight ticks, and the second seed.

1. **Encounters in the probed belt windows = 0** at every N (3999's zero-encounter
   finding): the answer's true candidate set is empty, so the answer's floor is 0 reads.
2. **Angular pass fraction ∈ [3%, 10%]** at belt e (Rayleigh σ_e ≈ 0.07, redrawn ≤ 0.4):
   ≈ E[2·νmax(e)]/2π + sweep ≈ 2·(2·0.09)/2π ≈ 5.7%, if phases are uniform. The sound
   per-body certificate family then cannot clear the 2.5 ms bar at 10⁵ (0.05·10⁵ × 4.2 µs
   ≈ 21 ms + N × cert cost).
3. **Per-read cost 4.0–5.0 µs** (cdf0's 4.5–8.5 µs band, belt body reader), so the
   in-belt answer ≈ N × per-read (3999's 415 ms at 10⁵ regenerates within 20%).
4. **The gap distribution is uniform in longitude** (the birth program scatters phases):
   if instead it is structured (phases correlated with radius), the pass fraction will
   sit outside [3%, 10%] and the phase-rank route reopens.
5. **Soundness control**: every real hit found by the exact predicate (the player's own
   Home-doll scans after a flight, where cdf0 measured 46–481 reads/hit) passes the
   angular cut — hits_passed = 0 violations.

Kill criteria: if encounters > 0 in a probed belt window, the "empty answer" framing
dies and the run reports their angular structure instead; if the pass fraction exceeds
15%, the fat certificate is worthless in-belt and the run says so (the population-level
answer is then the only route, with a measured ceiling).
