Working...
**Grade: gold** — written to `lab/results/20261007-0842-inversion-0a7a/check.md`.

**Reproduced bit-for-bit** in a clean tree (`git apply work/patch.diff`, author's build command): s0-control (churn 46/86, ev 601/807, ratio 69.15, 64 encounters), s1-e005 (churn 199/302.5, 50 encounters, NaN work as disclosed), cone-s0/s1 (19900/19900 cone pairs, 0 missed, O(n²) control). Predictions pre-registered 12 minutes before the decisive runs; the kill-carrying calls (P2, P3, P4) held, the two failures disclosed.

**My three adversarial cases:**
1. The author's dead nc=800 point, now measured: churn/nc flat at ≈0.20 across nc = 200→1600 (46/79/158/344) — the [INFERENCE] ∝ n_c claim is confirmed; per-orbit watch events ∝ n_c² against encounters ∝ n_c.
2. The gold's own λ-uniform corner: churn 0 at nc=200 (the gold's corner was genuinely safe — the author honest about it), rising 0→4→16 at nc = 200→800→3200. The violating regime swallows the gold's corner before 10⁶ on both λ distributions.
3. The author's named next experiment, adjudicated against them: all 50 real encountering pairs at σ_e=0.005 get windows and are found 50/50 by the shipped tier 2. The dossier's "sections() emits zero windows" misread `ev` (numeric-window evals; analytic Cross windows cost 0). Tier-2 blindness is refuted — a side-anomaly, honestly parked as unadjudicated, not load-bearing.

**Why gold:** it shows a premise of an adopted gold is wrong (O(n·k) with rebuild-on-overtakes; "~300 MB, setup falls 10⁵×" at 10⁶) on the board's top scaling risk, reproduced and pre-registered, adoptable in one step (add 2e·n_c/σ_λ to the b-coorbital-cert trigger; budgets per orbit) before that build lands. Reservations recorded — the 69× is the aggressive reading (charitable gives 9–17×, still past the ≥3× threshold), the 0.9 TB constant doesn't reconstruct (conclusion robust at 0.9–3 TB), and "the gold's own control" conflates the gold's two scenarios in the claim sentence only. Tree restored clean; nothing else in the run folder touched.
