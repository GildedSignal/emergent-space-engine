Grade: silver

**Abstract.** Claim: the law's whole `NoBoundOrbit` gap (plunge, direct capture, near-radial, γ≈2000, photon capture) compiles into the same ψ-panel tube as bound cycles via u = u₁ + ρsin²ψ on the cubic's one real root, with the horizon crossing finite and smooth in Kerr–Schild time v. Reproduced exactly: both scripts regenerate every printed number. Independently confirmed by my own forward r-space oracle (no cubic, no ψ, v from t+r*): 1e-12–1e-13 on C/D/E/F plus new adversarial cases E=1.05·0.999L_c and E=10⁶·0.99L_c; the near-critical Δφ continues exactly +3.256 rad/decade to k=7 (their flagged mp40 kink is their instrument, as they guessed). Gain: capture becomes one compiled object, ~2000× per sample over re-integration, deleting the refusal class. Cost: the `b-plunge-tubes` Rust build on this representation.

## Reproduction

`python3 plunge_falsifier.py` (1.9 s) and `python3 plunge_cost.py` (1.3 s), 8-vCPU runner, load ~2: all physics numbers identical to `run-output.txt`; timings same order (compile 0.57 ms, readout 3.13 µs, DOP853 7.21 ms). `patch.diff` empty — no tree edits, as a scout run should be. `predictions.md` mtime precedes the final script edits and output, consistent with pre-registration plus their two disclosed post-run bug fixes (φ orientation, spurious 1/L), both visible in the code comments.

## My attacks (independent of the author's harness)

1. **Forward r-space oracle** (DOP853 in (r, φ, t); v = t + r + 2ln(r/2−1); no u-cubic, no ψ): C/D/E/F at 3.8e-13–1.7e-12 (r), v at 1.7e-9 — the EF-time identity (1+L²u²)/(E+√F) ≡ (E−√F)/(1−2u), which I also re-derived by hand, is confirmed end to end. The author's DOP853 v-equation shares this identity with the tube; my t+r* path does not.
2. **Adversarial cases of my own:** E=1.05, L=0.999L_c: 9.2e-13. E=10⁶, L=0.99L_c (γ far past their 2000): 1.4e-12. E=0.97 near-critical from apoapsis (k=4): independent u-space quadrature agrees 3.2e-8 (Δφ) / 3.1e-7 (Δτ); A and B likewise (1.1e-7 / 4.2e-7) — the residual is my start-point at a sqrt singularity; their backward-from-horizon oracle design avoids it and had 1e-11 there.
3. **Near-critical kink resolved (their open flag).** u-space 50-digit quadrature with splits at a±20b: Δφ(k=5,6,7) = 17.3290, 20.5854, 23.8417; differences 3.2564, 3.2563 — the log slope continues exactly (hand-derived asymptotic √2·ln 10 ≈ 3.2563). Their mp40 reference collapsed at k≥6, precisely the instrument limit they flagged. True 512-panel errors are 4.2e-7 / 1.8e-4 / 7.4e-3 (k=5/6/7): the conclusion (panel growth ∝ winding, log-cheap) stands; their k=5–7 error column was ~2 orders pessimistic, being measured against the collapsing reference.
4. **P3 table regenerated** (its script is missing from `work/`, see defects): pair-b relerr 9.653e-13 → 8.036e-9 (k=4…8) matches `run-output.txt` exactly; u₁ sits at 0–2 ulp at every k. Genuine, regenerable in ten lines.
5. **Photon near-critical** b = b_c(1−10⁻⁴): 512 panels hold 1.8e-11 vs my independent quad — same failure mode as the massive case, nothing new breaks.

## Novelty

`docs/HISTORY.md` logs "plunge orbits have no tube" as an open limitation; `b-plunge-tubes` is queued and untouched. The bound-cycle Darwin compile exists (`space-darwin16-v1`, law.md §2); the one-real-root sin²ψ variant, the finite-v horizon anchor and the photon-capture tube are new here. Sources are honestly graded (UNVERIFIED marks where due).

## Goal fit

Deletes the `NoBoundOrbit` refusal class (HANDOFF risk "Orbits with no tube"; queue item 3), feeds law.md §7's existing horizon clause verbatim, and B4/B19. "Store the generator, not the generated"; "Exact means deterministic and reproducible"; one cubic's root patterns instead of orbit categories. Fit is direct.

## Why silver, not gold — the record, not the physics

- **P4 was substituted, not held.** The prediction: "bracket + Newton in ψ… < 20 µs". The shipped 3.08 µs times a *linear-interpolation* readout whose accuracy I measure at **6.2e-6** vs the oracle — six orders below the table's 1e-12. My 3-iteration Newton: 36.5 µs at 1.2e-7 (implementation-limited). The dossier marks P4 ✓ and headlines "exact to 1.3×10⁻¹⁰ … with O(1) readout at 3 µs", conflating table accuracy with readout accuracy; the swap is undisclosed. The ~2000×-per-sample conclusion survives any honest readout, but the shipped number does not measure the predicted mechanism, and "independent of winding" was never swept (case C only).
- **One headline table has no script.** `run-output.txt` lines 23–29 (the P3 pair-precision result) are produced by nothing in `work/`. I regenerated it and it is genuine (exact match k≥4), but as shipped the code cannot regenerate a reported result — the lab's historical gold-killer.
- **Two prose numbers are wrong.** "the pair coalesces as b ∝ δ": it is b ∝ √δ (their own table steps by √10 per decade; verified). "L_c→3√3E confirmed to 2×10⁻⁹": the measured deviation at E=2000 is 3.95e-8, twenty times their claim.
- Hygiene note: `plunge_falsifier.py` writes `plunge_main.json` into `work/`, so my reproduction overwrote its six per-case `compile_ms` timing floats (physics fields are deterministic and unchanged; the authoritative record is `run-output.txt`). Checkers should copy `work/` out before running — or the script should write elsewhere.

## The one experiment to gold

Re-measure the readout honestly: bracket + Newton-in-ψ (or Hermite) timing **and** accuracy across a winding sweep at |1−L/L_c| ≥ 10⁻³, targeting the table floor; ship the missing P3 script; fix the two prose numbers (b ∝ √δ, 3.95e-8); restate the near-critical panel-error column against a split-point reference. Nothing else is open: the physics is verified from three independent directions (their backward ODE oracle, my forward r-space oracle, my u-space quadratures), and my resolution of their flagged k=6–7 kink removes their last stated uncertainty.

## What the author missed

- The readout accuracy/cost distinction above — the only claim in the dossier my numbers contradict.
- The mp40 reference could be repaired with split points around the coalescence; they flagged the kink and stopped one step short of answering it.
- Absorption at a star *surface* (u_stop < 1/2, the `b-plunge-tubes` build's actual case) is untested, though the table trivially truncates there; the horizon anchor alone does not cover planets.
- Kick-arrival mid-plunge forces a recompile per kick; 0.55 ms float is measured, the integer path unknown (they disclosed this).
