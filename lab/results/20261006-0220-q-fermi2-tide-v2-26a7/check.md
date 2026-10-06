Grade: gold

**Abstract.** Claim: the Fermi phase-2 tide reference regenerates end to end — `verify.py` v2 writes its own `vectors.json` (18 windows, near-ISO re-admitted), `derive5.py` v2 regenerates `omega_expr2.txt`, and the closed kernel agrees with the red-team's −w(3γ²−1), +w. Reproduced in a clean tree: `python3 verify.py` (15m14s, 56 MB, exit 0) reproduces the author's `vectors.json` **bit for bit** — 18 vectors, 163 checks, the same 4 disclosed failures to full precision; `crosscheck_redteam.py` and `derive5.py` reproduce exactly. My attacks: plunge families down to r≈2.05 pass at the instrument floor; B.frame falls 14.7× per n-doubling (their 4th-order claim); the omega failures are a ~1e-9 round-off floor, not physics. Gain: the E9 freeze input is adoptable without re-derivation; derive6 deleted. Cost: none new (`schwarztide.py` untouched).

**Reasons.**

1. **Reproduction (clean tree, no patch — `work/patch.diff` is empty).**
   - `python3 verify.py`: 15m14s, 56 MB peak RSS, exit 0, "checks passed: 159 / 163". Worst: A 4.001e-9, omega 1.195e-9, B.coord 8.663e-3, B.frame 8.535e-8, C 7.9e4 (diagnostic), D 3.593e-14, X 2.612e-13; B.coord ratio 0.5004. Comparing my `vectors.json` to the author's: **0.0 relative difference on every field** (errors, C_parallel matrices, 163 check values, refinement dict) — bit-identical on the same machine class. The four gated failures reproduce at all printed digits (1.1633842963752237e-09, 1.1952208516970226e-09, 8.535320706263105e-08, 8.036534560614437e-08).
   - `python3 crosscheck_redteam.py` (11 s): formula-level kernel agreement C22/C33 worst 1.30e-13/2.61e-13 (r=1000 round-off), typical 1e-15; static orthonormal Riemann ≤ 7e-18; geodesic-pair (no Riemann code) radfac → 1.4984 (closed 1.5000) at r=6 and → 16.0077 (closed 16.0000) at r=3.1 — the dossier's numbers exactly.
   - `python3 work/derive5.py` (2.3 s): prints omega = E·L·M/(r²(rE²+2M−r)), dΦ/dφ|E=1 = −1/2, and writes `work/omega_expr2.txt` byte-identical to the shipped one. `work/prev/derive5.py` (0dee's) indeed omits Γ^r_rr and differentiates without a chain rule; `derive6.py` is gone from the shipped set.
   - The v2 diff against `base/verify.py` is exactly the six changes the dossier lists; `schwarztide.py` — the module under test — is byte-identical to 0dee's.

2. **Predictions.** File times support pre-registration: predictions.md 02:38:41 → vectors.json 02:54:41 (the 15m55s decisive run) → run.log 02:57. Held: item 3 (circ-6.01/6.02 full windows 11.57/11.60, errors at the circular floor: A 4.7e-16/7.6e-16, B.frame 1.7e-15/2.8e-15), item 4 (the explicitly held-out anchors: radial omega 0, parabolic −1/2, E-independence), item 5 (cross-check, untouched by v2). Missed and disclosed: item 2 (1.2e-9 vs ≤1e-10) and item 1's omega/B.frame sub-claims — see 3; the pre-registered B.coord falsifier (ratio < 0.5 ⇒ gate fails) landed at 0.5004 and was reported as a boundary, not bent.

3. **Attacks (my own).**
   - *Plunge families the set lacks* (E=1.2, L=2 → horizon, no turning): r 5→2.6 errA 2.4e-12, errW 4.2e-12, B.frame 1.6e-14; r 2.6→2.05 (γ large) errA 2.4e-9 (the same instrument floor as the long windows), errW 2.0e-12, B.frame 8.9e-12. The closed forms hold where the author never tested.
   - *B.frame n-refinement* on the failing family: 8.0365e-8 (n=1200) → 5.4504e-9 (n=2400), ratio 14.7 — their 4th-order truncation claim, reproduced to 4 digits.
   - *omega h-scaling below their smallest h* (their admitted inference): Richardson on (5e-4, 2.5e-4) gives 5.8e-10…1.4e-8 — a mixed round-off regime around 1e-9, not clean h⁴. The failures are tolerance placement; a 2e-9 gate is the right placement.
   - *Near-ISO admission*: exact-circular rdot² at 40 digits with float64 inputs is −2.48e-16 (r=6.01), −1.36e-16 (6.02) — round-off on an exact zero, four orders below the relative 1e-12 guard. Admission justified (but see "missed": the −1e-40 story is wrong).
   - *0dee baseline*: the regenerated `base/vectors.json` matches the stored 0dee record bit-identically on A/omega/C_parallel; the stored B.deviation values (0.37–1.06 on all 16 windows) do **not** regenerate (re-run: 1e-5…8.7e-3) — 0dee's record defect was real, and this run is its fix.

4. **Novelty.** docs/HISTORY.md line 3121 queues exactly this work ("the GLM queue (… Fermi phase-2 tide)"); no H entry builds the phase-2 reference. The kernel −w(3γ²−1), +w is the red-team's (21db); what is new here: the X gates against the shipped closed forms, the B.frame machine-precision check, the derivation of record, and the regeneration itself — the exact defect that held 0dee at silver (taste log, 5 Oct: "Most silvers fell short of gold on the record, not the physics").

5. **Goal fit.** Live board item ("the Schwarzschild tide in the Fermi frame, phase 2, after gate E9"). PRINCIPLES: "Certificates need independent, adversarial checks" — the geodesic-pair cross-check uses no Riemann at all and lands on the same kernel; "'Exact' means deterministic and reproducible" — now the record is, bit for bit. Adoptable within one step: two commands, ≤ 16 min, 1 core, < 60 MB.

**What the author missed.**
- The dossier's evidence table says X worst 1.2e-12; the record (and my re-run) say 2.61e-13 — transcription error, conservative direction.
- The "−1e-40 at 40 digits" mechanism (dossier and verify.py comment) is wrong: the residual is float64-input rounding, ~−2.5e-16. The clamp and the relative guard are still correct, for the right reason (exact zero ± input round-off).
- "18 families" is 18 windows over 9 families (shipped: 16 over 7); "near-ISCO … passing every gate" is true of those families but the claim sentence reads wider than the 4 disclosed gated failures.
- omega's "h⁴-structured" residue is only clean above h≈1e-3; below it the error fluctuates (5.8e-10…4.8e-8). The lens note flagged the inference; my measurement settles it as a mixed round-off floor.
- `verify.py` exits 0 regardless of gate status; a freeze consumer must read the `ok` flags in `vectors.json`, not the exit code.
- Still untested (their own disclosure, unchanged): long-arc whirl, the Phi unwrap at radial turning points, and check C's broken launch bookkeeping.
