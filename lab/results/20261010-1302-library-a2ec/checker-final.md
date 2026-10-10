Working...
Check complete. `lab/results/20261010-1302-library-a2ec/check.md` written; nothing else in the run folder touched (reproduction and adversarial scripts ran in `/tmp/check-a2ec/`).

**Grade: silver.**

**What held under reproduction and attack:**
- Exact reproduction: `python3 work/probe.py` → wall 17.6 s (author: 17.5 s), every dossier number matches `probe-out.json` cell for cell. `predictions.md` (13:11) provably precedes the probe (13:13:27→13:13:45). All five quotes verbatim in the 4,580-highlight export. Empty `patch.diff` — no tree edits.
- Predictions honestly scored by the author (P2 half-fail and P4 VOID disclosed, not hidden).
- Held-out generalizations I added *support* the mechanism: at e = 0.3/0.6 the gate beats a same-count clock 2–5× on both metrics (~1.6× vs a parity-interpolated clock, versus mere parity at the toy's e = 0.05), and q is a true dial (count ∝ q^-0.5, error ∝ q).

**What keeps it from gold:**
- Measured gain is 2–2.8× with no behaviour parity — not the 10× bar; nothing is deleted.
- The certificate's own compute is unpriced: the per-event 128-point orbit scan makes the policy ~30× slower than the whole fixed-32 clock as shipped. Caching the bound once per orbit fixes it (3.5×, behaviour unchanged) — one line the author never measured.
- The "one experiment away" composition fails in its natural cheap form: a Simpson window-averaged kick is 6–24× *worse* at equal cadence (the endpoint kick's leapfrog-like error structure matters, not phase sampling). Only H0190's orbit-average remains open, and that is the named gold experiment.

The direction is known (H0212, q-cadence queued), but the per-body Encke-style certificate with measured oracle tightness (1.65×) is new — a legitimate candidate rule for the q-cadence rung, not adoptable code.
