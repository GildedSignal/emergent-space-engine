#!/usr/bin/env python3
"""Second tightening pass for table.py (≤ 20 words)."""
from pathlib import Path

P = Path(__file__).resolve().parent / "table.py"
FIX = {
    "Holds on the shipped record: the event stream is fat-tailed (Hill α̂ ≈ 1.27); bench p99.9 underestimates the hourly worst 4.5–6.8×.":
        "Holds on the shipped record: the event stream is fat-tailed (Hill α̂ ≈ 1.27); bench p99.9 misses the hourly worst 4.5–6.8×.",
    "Five Readwise lessons wired to queued decisions; the shock-asymmetry trigger reproduced r9's τ₀ (its moon measurement died — broken Kepler layer).":
        "Five Readwise lessons wired to queued decisions; the shock-asymmetry trigger reproduced r9's τ₀ (its moon measurement died: broken layer).",
    "The resonance gate is an untested state switch: reach ≈ 1.9× the tolerance at e 0.005; one chirp leaves 33–69% irreversible error.":
        "The resonance gate is an untested state switch: reach ≈ 1.9× the tolerance at e 0.005; one chirp leaves 33–69% error.",
    "Inside the real load range stalls start at 2×; the frozen service gate (rtf_low1_median ≥ 1 at 4×) kills shipped service.":
        "Inside the real load range stalls start at 2×; the frozen service gate (rtf_low1_median ≥ 1 at 4×) kills it.",
    "The fired kick is 25× above its floor: rebind 68%, shared secondaries 27%, forces 6%; an integer evaluator is 8–10× cheaper.":
        "The fired kick is 25× above floor: rebind 68%, shared secondaries 27%, forces 6%; an integer evaluator is 8–10× cheaper.",
    "Compile price is a measured law: 0.73 µs per knot, knots ≈ 6 + 15.4·log₂(r_a/r_p); leavers (e 0.94) carry the p99.":
        "Compile price is a measured law: 0.73 µs per knot, knots ≈ 6 + 15.4·log₂(r_a/r_p); leavers (e 0.94) carry p99.",
    "The capacity knee sits ~20× above the flying point; the readout is two-thirds of frame; burns collapse the RTF tail 100×.":
        "The capacity knee sits ~20× above the flying point; the readout is two-thirds of frame; burns collapse the RTF tail.",
    "The compiler is within 3–4% of its bit-identical floor; exact cos is a serial chain worth 33%; near-separatrix rebinds ~1 ms.":
        "The compiler is within 3–4% of its bit-identical floor; exact cos is a serial chain worth 33%; near-separatrix rebinds cost milliseconds.",
    "10⁹-in-8GB is decided by hot terms: 6.9 KB live per body, N_hot ≈ 1.3–2.7×10⁴ at rtf 100; cold free by horizon.":
        "10⁹-in-8GB is decided by hot terms: 6.9 KB live per body, N_hot ≈ 1.3–2.7×10⁴ at rtf 100; cold free.",
    "The belt's live store is log-bounded (~1 bit per time-octave); cold at 41.7 bits fits 8 GB; only concentrated 3-dof breaks.":
        "The belt's live store is log-bounded (~1 bit per time-octave); cold at 41.7 bits fits 8 GB; concentration breaks it.",
    "The Binet band coefficient makes stability a property of the band: a phantom shelf inside the true ISCO; r1's criterion is blind.":
        "The Binet band coefficient makes stability a band property: a phantom shelf inside the true ISCO; r1's criterion is blind.",
    "No phantom shelf in the shipped law (7,203 exact-rational adjudications, none wrongly parked); live defect: 1.5% of near-rim bound states refused.":
        "No phantom shelf in the shipped law (7,203 exact-rational adjudications, none wrongly parked); live defect: 1.5% of near-rim states refused.",
    "Shipmem reabsorption measured with a real packed store: coarse 0.6–1.1% of a core (kill line 20%); exact dies on CPU too.":
        "Shipmem reabsorption measured with a real packed store: coarse 0.6–1.1% of a core (kill line 20%); exact dies too.",
    "The union sort is eternal only on period-quantized fleets (19×); the honest number is 9.6× at spread 1e-4; cross-group tier works.":
        "The union sort is eternal only on period-quantized fleets (19×); honest number 9.6× at spread 1e-4; cross-group tier works.",
    "The overflow design holds past capacity, but a budget floor scales with the universe: 428 bodies silently deliver 0.00× at 0.2 ms.":
        "The overflow design holds past capacity, but a budget floor scales with the universe: 428 bodies silently deliver 0.00×.",
    "The strong-field delay rows were correct (the corrections were under-convergence); real corruption at r_e ≥ 20; the memo reaches the floor.":
        "The strong-field delay rows were correct (the corrections were under-convergence); real corruption at r_e ≥ 20; memo reaches floor.",
    "The 60 Hz frame breaks at M* ≈ 700–1,000 members; the breaker is the unbudgeted readout (gather 55–63%), not the engine.":
        "The 60 Hz frame breaks at M* ≈ 700–1,000 members; the breaker is the unbudgeted readout (gather 55–63%).",
    "All remaining compile divisions to word-size buy only ~3%: the cost is diffuse (~60% outside the node kernel); reuse is the lever.":
        "All remaining compile divisions to word-size buy only ~3%: the cost is diffuse (~60% outside the node kernel); reuse remains.",
    "The frame wall holds to rtf 1000; delivery floors at ~10×; the budget knee is 10 ms; the readout owns the median frame.":
        "The frame wall holds to rtf 1000; delivery floors at ~10×; the budget knee is 10 ms; readout owns the median frame.",
    "The 845 MB at 4,000 members is unpruned rebind history (~10 kB per ship-kick; settle bypasses the prune) on ~19 kB construction.":
        "The 845 MB at 4,000 members is unpruned rebind history (~10 kB per ship-kick; settle bypasses prune) on ~19 kB construction.",
}
src = P.read_text()
n = 0
for old, new in FIX.items():
    if old in src:
        src = src.replace(old, new)
        n += 1
P.write_text(src)
print(f"replaced {n}/{len(FIX)}")
