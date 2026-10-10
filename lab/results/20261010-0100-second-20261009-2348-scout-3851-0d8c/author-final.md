Second-authThe record is complete and self-consistent. Final verification summary:

**Regeneration** (`run.log`, exit 0): `run-all.sh` → `val.json` (5-case validation, ~20 s) → 6 sweep files (17–51 s each, 12 cases) → `analysis.txt` (13 s). All numbers in `dossier.md` print from `analyze2.py`. `predictions.md` (02:01) predates every results file (02:11–02:14).

**Key cross-checks**: closed-form chart vs exact tetrad transport: dΛ/w ≤ 2.7×10⁻¹⁵, dω ≤ 4.2×10⁻⁶; circular Δψ = −5.960256 vs analytic −2π√(1−3u) = −5.960753; circular monodromies match `expm` to 1.2×10⁻¹⁴; band-peak growth matches an independent `solve_ivp` integration to 10⁻⁶.

**Results**: chart = coupled truth on 144/144 bands (≤ 0.026 grid steps); Q=2¹² fixed-point quantization shifts edges ≤ 0.026 steps; the averaged law misses 127/144 bands and overstates ruin speed 1.8–3.6×; avg+kinematics is a third wrong answer (misses 124/144, peak errors to 93%); the scout's frozen scalar certificate misses 142/144; channel 2 develops real bands at e=0.6 (to 0.253/orbit — P6 failed as worded); no rotation-confined gaps (P8 failed as worded) — both failures reported in `predictions.md`/`dossier.md`.

**Claim (one sentence):** On the full 2×2 coupled Fermi-frame member tide — both in-plane channels, the shear Λ₁₃ = −3γu_φu_r·w/N², and the geodetic precession ω — the closed-form Floquet chart reproduces the exact-transport truth on 144/144 bands with quantization-free edges (≤ 0.03 grid steps at Q = 2¹²), while orbit averaging misses 127/144 bands with 1.8–3.6× wrong ruin speeds and the scout's frozen scalar certificate misses 142/144, so the coupled monodromy chart — one 4-column quantized table per (E, L) tube plus one monodromy per member — is the certificate the engine can adopt.
