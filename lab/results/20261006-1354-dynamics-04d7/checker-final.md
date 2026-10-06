Working...
Check complete. `check.md` written; only that file added to the run folder.

**Grade: silver** — a strong one, one named experiment from gold.

**What I did:**
- **Reproduced exactly.** Ran all four dossier command tiers in a clean scratch copy (empty patch, nothing else touched): all 12 `data/*.json` files are **bit-identical** to the author's — every snapshot and stat — and `analyze.py` regenerates every quoted number (finals 147.4–150.7 work / 39.9–42.6 behav, slopes 2.75–3.16 and 1.92–2.37 with the quoted r², rw/kick 0.998–0.999, λ pinned at 83 bits, refit table 20.1→37.4, distinction rates 0.049/0.0025, tier encounter counts). Zero differing numbers.
- **Predictions audit.** `predictions.md` (14:06) precedes all decisive data (14:07–14.13); pilot disclosed; N=300→200 switch disclosed in the run log. Held: P1-behav, P2, P4, P6, P7, P5-work. Failed: **P5-behav (11–12 orbits vs predicted 10²–10³)**, P3-gamma, P1-work slope — all disclosed honestly, but the gold bar's "held-out predictions held" is not met.
- **Four adversarial cases:** fresh-seed gm=0 controls (exact zero); gm=3e-7 = 2× hot (plateau holds at 44.9/153.6, no runaway, da_max 0.057); half density (crossing 11–12 → 18 orbits, kick rate halves as claimed); ×4 coarser quantum (→ 36 orbits). The law survives; the scaling is slightly sublinear (measured 1.5×/3× vs ideal 2×/4×).
- **Novelty:** first endogenous measurement of the quantity docs/plane.md names as the decider for 10⁹-in-8 GB; the crate ships only a static "62 bits per kick"; components-98bc measured the birth floor and synthetic churn.
- **Why silver, not gold:** the central pre-registered horizon failed by ~1.5 orders (in the direction that strengthens the premise-kill, disclosed) and the headline crossing sits on one side of an author-disclosed 3× codec bracket. Gold path: run the shipped `Program::seal` block codec on these trajectories with a pre-registered crossing, plus bound the stirred-census fraction.
