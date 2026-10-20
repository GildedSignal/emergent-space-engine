Working...
Check complete. `check2.md` written; the author's page corrected in place.

**Grade: gold** (blind to checker 1).

**What I did:**
- **Reproduction**: regen exit 0; every count re-derived independently from the re-flown CSVs — era kicks/boundaries ±0.1%, coast payload split 45.6/8.57 µs (dossier's 45.9/8.6 exact), arrivals exact to 3 decimals vs 0a46's record, concentration 49/37/16%, kick rate 4.889e-5 identical across arms, anchor 822 ms in the 811–948 family, freeze kill 703→39.6 ms. Mechanism verified in code: `step.rs:717-718` (Boundary at `t+full/2`, Kick at `t+full`) and `universe.rs:770/799-803` (nested `pull_ships` timed into cn[3]).
- **Three adversarial flights** (two outside the author's grid): (1) **stagger 28000** — the payload-interleave the dossier prescribes but never flew: k-frac 0.50/bin, walls 1.06× flat outside the repay window — constructive completion of the mechanism; (2) **coast+14k**: walls still band 1.98× at identical arrivals — banding is structural; (3) **seed 2**: comb alternation and the nested freeze (734 ms, it2=0) reproduce at the same onset.
- **Corrections** (page fixed, none touch the mechanism): honest 4-era least-squares split is 45.3 vs **5.9** µs = **7.7×** (the quoted 8.6 was contaminated even-era attribution — strengthens the claim); S2's walls are not flat (band 1.72× burn / 1.98× coast); "−17% total wall" does not regenerate (37.2 vs 37.3 s re-flown — first-draw artifact); era-1's 86 µs nested cost is a draw (re-flown 54 µs vs era-3's 63 — the [INFERENCE] first-kick reading unsupported).
- **Novelty**: no HISTORY entry; 0a46's "3× served-path lever" is inverted (no scheduler can buy a payload split), ca63's 13.2 h re-identified as the kick comb with a new ~2.4 h boundary-comb term.

Pre-registration provability was destroyed by regen overwriting the first-draw CSVs (disclosed); the honestly-reported P3 failures against pre-set bars are the evidence it was genuine.
