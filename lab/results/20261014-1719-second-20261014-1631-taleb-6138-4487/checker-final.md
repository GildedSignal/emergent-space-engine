Grade: goldCheck complete. **Grade: gold** — written to `check.md`, with the abstract for the integrator, full reasons, and the author's misses.

**What I did:**

1. **Reproduced** from the runner's regen + my own runs: 2×10⁵ arms (fixed 85.1/83.1 ms vs pristine 1,211; evmax 24.5k→333; wave region 11.94 ms), `frame_digest` 8×4 identical pristine = fixed = forced (re-run independently), the core eb25 certificate `ae06c773…` equal to the digit at 21,000 game-s, and the disclosed 11,473-event mid-drain gap **exact** (469,621 − 458,148).
2. **Chased the one discrepancy**: the regen's 3×10⁵ arm (535.5 ms vs claimed 123.8) was box load — its worst frames are early 0–5-event frames with evmax still 333. Re-run quiet: **122.99 ms, 1,705 MB, seam-bound — the dossier's numbers exactly**.
3. **Four adversarial cases**: seed 3 (outside the author's seeds — post-drain digest bit-identical, pristine monster 1,789 ms), `NLADDER_HOLD=0` (every pull through the Waiting path — digests identical at *both* cuts, the strongest proof of the capture logic's order-equivalence), the 5×10⁴ onset pair (fix harmless; the second seam pre-exists on shipped main), and the quiet-box 300k rerun.
4. **Novelty/goal fit**: H0218 still lists the wave as open; 6138 named the fix, this run built and certified it — ~14× worst frame at 2×10⁵, the unbudgeted item deleted, one-patch adoption (PRINCIPLES #12, #13, #19 quoted in check.md). Patch applies cleanly to `9fcae60f`.
5. **Page**: faithful, conflict legitimately resolved (both blocks kept); I added two checker notes (hold-0/seed-3 confirmations; the seam binds from 5×10⁴) — it nowhere overstates.

**Recorded against it**: F3's kill letter tripped (disclosed; the seam diagnosis verified per H0183), `regen.sh` destroys the A-side of its own pristine A/B, the 3×10⁵ number is quiet-box-conditional, `run.log` is empty, and rung writers must compare digests at cuts, never event counts. Working tree left pristine; my evidence is in `check_raw/`.
