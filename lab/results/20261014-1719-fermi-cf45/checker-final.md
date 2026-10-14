Working...
Check complete. **Grade: gold**, written to `lab/results/20261014-1719-fermi-cf45/check.md`.

**What I did:**

- **Reproduced bit-identically**: applied `work/patch.diff` to a clean tree, re-ran the instrument (seed 1, N=4000) — every physics number matches `cadence-4000.txt` (kicks +101,624, events +205,339, belt events/body 4.00, all percentiles); only wall-time digits differ. Re-derived every `compose.py` product by hand (8.2/1.07/0.10/0.0039 cores; 148×/242×/14×/0.54×; wave 26×).
- **Verified the mechanism in code**: `on_clock()` = doll-0 ships (`step.rs:601`); belt ships are `Kind::Ship`, `doll: 0` (`scenario.rs:261, 343`) → `plan_clock` → `ext::constants`, whose documented law is Δs = 2⁻ᵏ·P_D/f′. P_D = 77.24 d is Kepler-consistent (Cinder 0.3515 AU, e 0.1, star ≈ 1.28 M☉); ladder.txt's 88 d is the wrong constant.
- **Four adversarial cases, all held**: N=20000 seed 5 (5× the author's largest N, fresh seed — identical constants); `step_log2=5` → interval exactly 4× (1.126×10⁵ s), verifying the dial anchor on shipped code rather than extrapolation; first-event probe (events/body 0.01→1.00 between 13.3 and 15.3 ks, matching interval/2 and taleb-6138's independent wave window); 1738's 457× cadence axis shown to sit inside the own-period law's 427–853×, so it inherits the correction.
- **Novelty**: the bare mechanism was on record (ladder.txt, kick-cadence page), but the live wiki carried effb's opposite, "code-verified" 2⁷/P_own law feeding the 10⁹ ledger and 1738's cube — this run measures, arbitrates the contradiction, corrects the constant (77.24 d, +14%), and recomposes. A premise correction of a load-bearing number, adoptable at zero code cost.
- **Predictions**: genuinely pre-registered (the misses prove it); the law-discriminating ones (P2/P3/P6/P7) held decisively; P4's +39% octave miss, P1's 88-d miss (which *is* the finding), and the locals bug are all disclosed.
- **Page**: one overstatement corrected in place — the 3071/7497 roster reproductions are now marked "a code-path reading, not re-measured". The inherited 7f99/6138 conflict markers left standing for adjudication, as the wiki rules require. Scratch files removed; tree as found.
