Working...
Check complete: **Grade: silver**, written to `lab/results/20261010-1152-dynamics-ad35/check.md`.

**What I verified**

- **Reproduction (bit-for-bit):** author's scripts, clean tree (`patch.diff` empty; work in `work/`). Reran the decisive scan subset (222 s): all six overlapping rho medians ratio 1.000. Instrument controls pass (drift 1e-16, truth Jacobi 5.3e-11, truth floor ~1e-9). `analyze.py` on `decisive.json` reproduces every quoted aggregate; both held-out JSONs match the dossier to the digit. Refit from raw JSON: rho = 0.533·n⁻²·¹³ vs claimed 0.50·n⁻²·¹¹ (the analyzer's global n⁻²·³⁰ includes the corrupt n=2 rows — fit basis unstated).
- **Predictions:** timestamps + 898 s wall confirm `predictions.md` predates the decisive run. Four predictions died and are reported dead; the corrected law was validated only on pre-declared held-outs. Honest.
- **Four attacks:** e0=0.3 breaks the headline — n=4 corrupts (rho_med **0.83**, worse than n=2) and the exponent degrades to ~−1; at eps 3.1e-3 the e-amplitude error binds before precession (24% at n=4, 10% at n=8 — their own decisive table already shows 11% at mu=0.2/n=4, contradicting "n=4 is the floor"); horizon ×3 stays bounded (no threshold); n=3 corrupt (floor=4 holds inside the domain).
- **Novelty:** q-cadence is queued on the board; no prior cadence-scaling measurement on the kick layer. The n⁻² exponent itself is prior (law.md line 33, Opus memo); the increment is mu/R-independence, no bifurcation, the twin control, and the 4–16–64 disagreement explained as seed noise (measured 3–693×).

**Why silver, not gold:** the 8–16× gain is inferred from the plane's assumed cadence, and the certified domain (circular, off-resonance, e0=0.1) is largely where the design already *averages* kicks (114×, H0190) — cadence governs the non-averaged remainder, which this run excludes. One experiment away: the same scan at belt eccentricities plus one `behave --law plane` run at cadence 8.
