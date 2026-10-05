Working...
Check complete. `check.md` written to the run folder (only file changed; no commits, no pushes).

**Grade: silver.**

**What reproduced (clean tree, empty patch.diff):**
- `probe_c_boundary.py` bit-for-bit (all 48 rows incl. 0.00745/0.0255/0.349/6.32; 6 s), `probe_a_flybys.py` (held-out ΔE 0.155–0.932 = claimed 0.16–0.98; κ=0.5; κ-flat medians), pair leg exactness 3.02e-15.
- Pre-registration holds by file times (predictions 21:37:50 < scripts 21:58+ < artifacts); `run.log` empty, so mtimes are the only ordering evidence.
- All arithmetic claims verify (conjunction rate 0.494–0.725, belt census 5.35 r_H, plane 64×29 µs).

**What did not survive attack:**
- **The named gold experiment fails.** I ran the dossier's own refinement path on the held-out flybys: Strang substeps make it *worse* (0.58→0.97), Picard second-order tails change nothing. The 1% gate is not one refinement away in that scene; the live suspect is the author's third (scene construction — truth plunges 10–30% deeper than constructed, b_real/q = 0.68–0.90).
- **The t\*<w hole:** the author's own artifact contains dv/U = 6.32 at U/v_H = 10 — inside the selector's event domain — from a clamped, off-centre window when the conjunction falls within one window of channel entry. Undisclosed; "never blows up" is contradicted by their own JSON. Matters operationally: doll-edge handoffs and spawns deliver bodies with less than w of lead.
- **Best-case presentation:** quoted impulsive range (0.75–2.7%) covers only 2 clean rows; my independent 26-case sweep gives typical 1–15%. The impulse control is degenerate (b→0 → 1e13–1e16) on half the rows; honest multiplier is 4–15×.
- **Record gaps:** selftest worst is 5.06e-08 not 1.4e-11 (claimed median never printed by shipped code); full event as shipped costs ~2.5 ms/body (tails unbatchable, broadcast bug), not ~6 µs — only the batched Kepler core hits 7.8 µs; prediction 4 was scripted but never run.

**Real and kept:** the boundary being in U/√(μ_p/b) rather than b/r_H is genuinely measured (same b, U swept: three orders of error spread), the exact pair leg is verified, and the event-as-executed-encounter is novel against HISTORY, law.md and the Opus memo (which leaves close encounters to the doll). The gold experiment is redefined in the check: B13's flyby list on natural-entrance scenes with second-order tails and window re-centring — probe_c's clean 0.75–2.7% suggests that can pass.
