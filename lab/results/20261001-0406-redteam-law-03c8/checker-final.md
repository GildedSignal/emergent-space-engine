Working...
Check complete. `lab/results/20261001-0406-redteam-law-03c8/check.md` written — **Grade: silver**.

**What I reproduced (all matched):**
- `e1_moving_lens.py`: +335.9% head-on / −56.4% transverse at β=0.9, +10.6% at β=0.1; β=0 sanity passes. Cross-checked with an independent closed form: head-on is exactly √((1+β)/(1−β))−1, transverse exactly 1/γ−1.
- `e4c_tide_layer.py`: all five cases — prograde moon at τ_apo=0.0784<τ₀ escapes in 35 parent orbits, e settles 0.10 at 0.45 R_H, held-out 0.42/0.30 quiet.
- Code/text: `TubeEvent`=96 B (4×i128 `Residual` charged by ENVELOPE.md itself), `regime()`→Dense for resonance, `resonant()` p,q≤8, B14 classification-only with chaotic exclusion, B15 medians, B3 static, no resonance or memory gate, B9's 64 crossings = e≤0.6 exactly (135.9/244.4 at e=0.9/0.99).

**My adversarial cases:** ejection robust to start anomaly and tighter tolerance; 0.35 R_H quiet (failure is boundary-local); retrograde 0.49 and 0.60 R_H stay bound — τ₀ is wrong in both directions, a point the author missed. Novelty clean against HISTORY/git (H0203's resonance finding is the complementary physics, correctly cited).

**Why not gold:** one pre-registered prediction failed and was reported as held — the transverse error is second order in β (−β²/2; −0.5% at β=0.1, below B3's bar, against the predicted 10–20%), and the dossier's "E1: held" cites only the head-on number. The gold-making experiment: measure the law's *faithful* averaged tide layer (orientation retained, `apply` semantics) against truth below τ₀ — attack 2's honestly-voided decisive half. The gate corrections themselves are adoptable now on the reproduced evidence.
