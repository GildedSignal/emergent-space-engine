#!/usr/bin/env python3
"""One-shot tightening of over-length claims in table.py (≤ 20 words)."""
from pathlib import Path

P = Path(__file__).resolve().parent / "table.py"
FIX = {
    "The frame-budget knee sits between RTF dips and deadline hitches; no session-level scheduling discipline moves it — the lever is engine-side.":
        "The frame-budget knee sits between RTF dips and hitches; no session-level scheduling discipline moves it — the lever is engine-side.",
    "Hitch risk is unsizable from bench percentiles: matched streams hide an 11.5× spread in the hourly worst frame; the gate needs the tail exponent.":
        "Hitch risk is unsizable from bench percentiles: matched streams hide an 11.5× hourly-worst spread; the gate needs the tail exponent.",
    "Holds on the shipped record: the event stream is fat-tailed (Hill α̂ ≈ 1.27); bench p99.9 underestimates the hourly worst 4.5–6.8×.":
        "Holds on the shipped record: the event stream is fat-tailed (Hill α̂ ≈ 1.27); bench p99.9 underestimates the hourly worst 4.5–6.8×.",
    "Fast-forward ceiling is 3–4×10³ game-s per wall-s, set by live surprise rate, not frame cost; the budget binds first at 10⁴×.":
        "Fast-forward ceiling is 3–4×10³ game-s per wall-s, set by live surprise rate, not frame cost; budget binds at 10⁴×.",
    "Frozen gates never sample the strong field; there Binet m16 fails its own 1% on near-circular massive precession (+9.6% at 7M).":
        "Frozen gates never sample the strong field; there Binet m16 fails its 1% on near-circular massive precession (+9.6% at 7M).",
    "The aging law holds (Δϖ̇⁻¹ scaling); the rebuild-cadence fix is refuted — the misses are fold events needing per-passage exact Δϖ.":
        "The aging law holds (Δϖ̇⁻¹ scaling); the rebuild-cadence fix is refuted — misses are fold events needing per-passage exact Δϖ.",
    "The Darwin compiler is within ~1.5× of its bit-identical floor; the next 10× is cross-compile reuse (the shape memo), not arithmetic.":
        "The Darwin compiler is within ~1.5× of its bit-identical floor; the next 10× is cross-compile reuse (the memo), not arithmetic.",
    "The kick is compile-bound (63% fresh compile); trivial shape reuse is worth 1.5%; the quantized-cell jet is worth a measured ~4.4×.":
        "The kick is compile-bound (63% fresh compile); trivial shape reuse buys 1.5%; the quantized-cell jet buys a measured ~4.4×.",
    "Five Readwise lessons wired to the queued decisions; the shock-asymmetry trigger reproduced r9's τ₀ (its moon measurement later died — broken Kepler layer).":
        "Five Readwise lessons wired to queued decisions; the shock-asymmetry trigger reproduced r9's τ₀ (its moon measurement died — broken Kepler layer).",
    "The contact law is Poisson-smooth per chronon but the Fano factor grows with N (1.2 → 30.5); the law itself has zero energy drift.":
        "The contact law is per-chronon Poisson-smooth but the Fano factor grows with N (1.2 → 30.5); zero energy drift.",
    "The resonance gate is an untested state switch: true reach ≈ 1.9× the tolerance at e 0.005; one chirp leaves 33–69% irreversible error.":
        "The resonance gate is an untested state switch: reach ≈ 1.9× the tolerance at e 0.005; one chirp leaves 33–69% irreversible error.",
    "Under 32× load the frame wall holds but delivery stalls silently (zero new game time from 4× members); the digest is invariant.":
        "Under 32× load the frame wall holds but delivery stalls silently (zero new game time from 4× members); digest invariant.",
    "Inside the real load range stalls start at 2×; the frozen service gate (rtf_low1_median ≥ 1 at 4×) kills the shipped service.":
        "Inside the real load range stalls start at 2×; the frozen service gate (rtf_low1_median ≥ 1 at 4×) kills shipped service.",
    "The fired kick is 25× above its floor: rebind 68%, shared secondaries 27%, forces 6%; an integer-band evaluator is 8–10× cheaper.":
        "The fired kick is 25× above its floor: rebind 68%, shared secondaries 27%, forces 6%; an integer evaluator is 8–10× cheaper.",
    "The SEM step is killed on the v2 clock: 44–58% of steps admit no solution (one-signed residual); closing K exactly is impossible.":
        "The SEM step is killed on the v2 clock: 44–58% of steps admit no solution; closing K exactly is impossible.",
    "Compile price is a measured law: 0.73 µs per knot, knots ≈ 6 + 15.4·log₂(r_a/r_p); leavers (e 0.94) carry the tail.":
        "Compile price is a measured law: 0.73 µs per knot, knots ≈ 6 + 15.4·log₂(r_a/r_p); leavers (e 0.94) carry the p99.",
    "The engine's capacity knee sits ~20× above the flying point; the readout is two-thirds of frame; burns collapse the RTF tail 100×.":
        "The capacity knee sits ~20× above the flying point; the readout is two-thirds of frame; burns collapse the RTF tail 100×.",
    "Sound admissibility (sweep-extended radii, alias completion) closes two cancelling holes; the window misses zero of 1,857 fires at 11–126× less wall.":
        "Sound admissibility (sweep-extended radii, alias completion) closes two cancelling holes; zero of 1,857 fires missed, 11–126× less wall.",
    "The compiler is within 3–4% of its bit-identical floor; exact cos is a serial chain worth 33%; near-separatrix rebinds cost ~1 ms.":
        "The compiler is within 3–4% of its bit-identical floor; exact cos is a serial chain worth 33%; near-separatrix rebinds ~1 ms.",
    "The clock-path regime split (orbit-permitted Δs, refining-only) is built and gated: 4.7–7.8× fewer kicks; B17 passes where the uniform cut fails B13.":
        "The clock-path regime split (orbit-permitted Δs, refining-only) is built and gated: 4.7–7.8× fewer kicks; B17 passes, uniform cuts fail B13.",
    "A lock judge separates order-1 interiors cleanly but earns no freeze at e0 0.02 (zero order-≥2 lock); deleting the detector is refuted.":
        "A lock judge separates order-1 interiors cleanly but earns no freeze at e0 0.02 (zero order-≥2 lock); detector deletion refuted.",
    "The NoBoundOrbit gap compiles into the ψ-panel tube: honest readout at the table floor, 0.53 µs/sample, winding-independent; the '3 µs' number retires.":
        "The NoBoundOrbit gap compiles into the ψ-panel tube: honest readout at the table floor, 0.53 µs/sample, winding-independent.",
    "10⁹-in-8GB is decided by the hot terms: 6.9 KB live per body, N_hot ≈ 1.3–2.7×10⁴ at rtf 100; cold populations are free by horizon.":
        "10⁹-in-8GB is decided by hot terms: 6.9 KB live per body, N_hot ≈ 1.3–2.7×10⁴ at rtf 100; cold free by horizon.",
    "The coupled 2×2 Floquet chart matches 144/144 truth bands (Q 2¹² shifts edges ≤ 0.03 steps); averaging misses 127, the scalar 142.":
        "The coupled 2×2 Floquet chart matches 144/144 truth bands (Q 2¹² shifts ≤ 0.03 steps); averaging misses 127, scalar 142.",
    "Binet cells survive every r1 criterion held out, but the coordinate-time period band fails from e ≈ 0.85 (1.9% at 0.99).":
        "Binet cells survive every r1 criterion held out, but the coordinate-time period band fails from e ≈ 0.85 (1.9%).",
    "The belt's live store is log-bounded (~1 bit per time-octave); a cold belt at 41.7 bits fits 8 GB; only concentrated 3-dof regions break.":
        "The belt's live store is log-bounded (~1 bit per time-octave); cold at 41.7 bits fits 8 GB; only concentrated 3-dof breaks.",
    "The Binet band coefficient makes stability a property of the band: a phantom stable shelf inside the true ISCO; r1's criterion is blind.":
        "The Binet band coefficient makes stability a property of the band: a phantom shelf inside the true ISCO; r1's criterion is blind.",
    "No phantom shelf in the shipped law (7,203 exact-rational adjudications, none wrongly parked); live mirror defect: 1.5% of near-rim bound states refused Range.":
        "No phantom shelf in the shipped law (7,203 exact-rational adjudications, none wrongly parked); live defect: 1.5% of near-rim bound states refused.",
    "Shipmem reabsorption measured with a real packed store: coarse 0.6–1.1% of a core (kill line 20%); the exact side dies on CPU too.":
        "Shipmem reabsorption measured with a real packed store: coarse 0.6–1.1% of a core (kill line 20%); exact dies on CPU too.",
    "Exact i64 fast paths for the visit predicates cut contact cost 11–16%, bit-identical; the rest is the neighbour loop (43%) and calendar (16%).":
        "Exact i64 visit-predicate fast paths cut contact cost 11–16%, bit-identical; the rest is the neighbour loop (43%) and calendar (16%).",
    "The union sort is eternal only on period-quantized fleets (19×); the honest number is 9.6× at a-spread 1e-4; the cross-group tier works.":
        "The union sort is eternal only on period-quantized fleets (19×); the honest number is 9.6× at spread 1e-4; cross-group tier works.",
    "Peters-flux (E,L) drift is adoptable inside B11's domain at the 1% bar; the kill line is crossed only outside it; handoff = separatrix.":
        "Peters-flux (E,L) drift is adoptable inside B11's domain at the 1% bar; the kill line is crossed only outside it.",
    "The kick is 84% compile; the cost is panel count (~140 per kick) times a flat ~200 ns/node; no arithmetic hotspot.":
        "The kick is 84% compile; the cost is panel count (~140 per kick) times a flat ~200 ns/node; no hotspot.",
    "Extended Darwin variables (cosh phase, root-structure classification) cover plunge and near-radial sectors at bound-orbit panel cost, ending in exact terminal events.":
        "Extended Darwin variables (cosh phase, root-structure classification) cover plunge and near-radial sectors at bound-orbit panel cost, with exact terminal events.",
    "Extended Darwin holds on the fixed integer cut layout: the near-separatrix valley is oracle-verified to 1e-6 at ≤ 75 panels; in-valley kicks hold.":
        "Extended Darwin holds on the fixed integer cut layout: the near-separatrix valley oracle-verified to 1e-6 at ≤ 75 panels.",
    "The overflow design holds past capacity, but a per-frame budget floor scales with the universe: 428 bodies silently deliver 0.00× at 0.2 ms.":
        "The overflow design holds past capacity, but a budget floor scales with the universe: 428 bodies silently deliver 0.00× at 0.2 ms.",
    "'One clock, one queue' needs no container: a counting scan reproduces the heap's stream exactly at 2.7–3.1× lower ns/event, zero container memory.":
        "'One clock, one queue' needs no container: a counting scan reproduces the heap's stream exactly, 2.7–3.1× cheaper, zero container memory.",
    "Candidate-tier cost collapses onto one number κ = σ_e·ā/Δa (frac = 4.27κ, half-point 0.20); the belt's dynamics drive κ through it.":
        "Candidate-tier cost collapses onto one number κ = σ_e·ā/Δa (frac = 4.27κ, half-point 0.20); the belt drives κ through it.",
    "The strong-field delay rows were correct (the corrections were under-convergence); real corruption at r_e ≥ 20; the image-resolved memo reaches the floor, 1,900× margin.":
        "The strong-field delay rows were correct (the corrections were under-convergence); real corruption at r_e ≥ 20; the memo reaches the floor.",
    "The 60 Hz frame breaks at M* ≈ 700–1,000 members; the breaker is the unbudgeted readout (gather 55–63%), not the budgeted engine.":
        "The 60 Hz frame breaks at M* ≈ 700–1,000 members; the breaker is the unbudgeted readout (gather 55–63%), not the engine.",
    "An f64-seeded exact isqrt (−28% kernel) plus one CSE cut the compile 4–6%; the rest is division-bound; no 10× inside bit-identity.":
        "An f64-seeded exact isqrt (−28% kernel) plus one CSE cut the compile 4–6%; the rest is division-bound; no 10×.",
    "Churn switches on between eps_eff 0.008 and 0.025 in the bar's envelope; the static resonance flag is dead; kicks own the (E,L) drift.":
        "Churn switches on between eps_eff 0.008 and 0.025 in the bar's envelope; the static resonance flag is dead.",
    "All remaining compile divisions to word-size buy only ~3%: the cost is diffuse (~60% outside the node kernel); structural reuse is the lever.":
        "All remaining compile divisions to word-size buy only ~3%: the cost is diffuse (~60% outside the node kernel); reuse is the lever.",
    "The kick is 82% exact recompilation at the x86 floor; lazy shape tables are blocked by Orbit::state's cycle-count division needing the full period.":
        "The kick is 82% exact recompilation at the x86 floor; lazy shape tables are blocked by Orbit::state's cycle-count division.",
    "The frame wall holds to rtf 1000; delivery floors at ~10×; the budget knee is 10 ms on this box; the readout owns the median frame.":
        "The frame wall holds to rtf 1000; delivery floors at ~10×; the budget knee is 10 ms; the readout owns the median frame.",
    "The 845 MB at 4,000 members is unpruned rebind history (~10 kB per ship-kick; settle bypasses the prune) on a ~19 kB construction marginal.":
        "The 845 MB at 4,000 members is unpruned rebind history (~10 kB per ship-kick; settle bypasses the prune) on ~19 kB construction.",
    "A one-quantum perturbation propagates via contact-frame cascades (quantum-blind, contained); peers have zero coupling; doll geometry is an instant global channel.":
        "A one-quantum perturbation propagates via contact-frame cascades (quantum-blind, contained); peers have zero coupling; doll geometry is instantly global.",
    "Levi-Civita z = u² serves the conic singular set exactly, event cost depth-independent; the stepping fallback is 18–93× worse.":
        "Levi-Civita z = u² serves the conic singular set exactly at depth-independent event cost; the stepping fallback is 18–93× worse.",
}

src = P.read_text()
n = 0
for old, new in FIX.items():
    if old in src:
        src = src.replace(old, new)
        n += 1
P.write_text(src)
print(f"replaced {n}/{len(FIX)}")
