# Dossier — 20261011-1917-fermi-b946

**Claim.** At 10⁹ bodies on the 8 GB M1 the binding term is memory capacity, not
compute or bandwidth: the tube store and any per-body event queue are already 3.2×
over the usable 5 GB, while compute and bandwidth clear by 3–5 orders of magnitude
once the two already-measured levers (kick-setup 12.5×, tide averaging 114×) are
applied — the board's "about 190 cores at today's rates" re-derives as 175 (all
bodies in LEO, raw 29 µs kicks) and dissolves to ~0.1 core with those levers.

**Bottleneck.** Board item 3 ("Cost at a billion... about 190 cores. We need 10–100×
less") and the handoff's unmeasured risk "distinctions per game-second (H_live)
decide whether 10⁹ fit in 8 GB". The estimate moves the item from "compute, 10–100×
short" to "capacity, and already within reach": the compute ask is met on paper by
measured constants (12.5 × 114 ≈ 1.4×10³), so the work that would hunt another 100×
of event speed is deletable; what remains is the memory design (programs + scars +
sublinear queue), with a measured cadence target. Expected gain: refocus of the
scale effort, one component class deleted (per-body kick handling at belt scale).

**Evidence** (all commands ≤ 60 s; Linux/x86 shared host, orders of magnitude only;
machine state in `machine-state.txt`, load 0.6):

- Encounter rate (the H_live creation input), `emergent-encounters steady`,
  truth-checked hits per body per orbit (`steady.jsonl`):
  - n=1000, σ_e=0.01, ρ=1e-3, a∈[1,1.5], 20 orbits: **0.0207** (414 hits).
    r8 v2's belt-0 truth (board: "427 encounters" / 20 orbits / 1000 bodies) gives
    0.0214 on another seed: reproduced independently.
  - n=3000 (3× density): **0.0579** = 2.80× — linear in n (n σ v at fixed volume).
  - ρ=1e-4 (÷10): **0.0020** = ÷10.35 — rate ∝ ρ^1.01, one pinned dimension, not ρ².
    This confirms the quasi-periodic conjunction-chain geometry the r8 design
    (continued fractions) assumes; a smooth two-free-component model would give ρ².
  - `steady_work_per_encounter` 1.3–1.6 checks per hit: the certificate's promise
    (work tracks real encounters) is visible in the same data.
- Budget arithmetic, `budget.py` → `budget-out.txt` (constants cited in-file):
  - **Compute.** Belt scale (P≈4×10⁷ s): 0.024 cores today, 2×10⁻³ after the setup
    fix, 2×10⁻⁴ averaged — ≥ 4 orders of margin. LEO worst case: 175 cores today
    (= the board's 190), 14 after the setup fix, **0.12 with averaging**. Encounter
    discovery at 10⁹, fixed density, 100× rtf, 10⁴ ops/encounter: 5×10⁻⁵ cores.
  - **Bandwidth.** Events clear (764 ev/s at 100× rtf vs 9.4×10⁸ ev/s cap). One full
    read pass over 10⁹ bodies: 1.07 s; per 16.7 ms frame the budget is **1 byte per
    body** — any per-frame full sweep is 64× over. "No ticks" (PRINCIPLES #14) is a
    bandwidth law, not a preference.
  - **Capacity.** 5 GB usable = 40 bits/body at 10⁹. Tubes (16 B): 16 GB, **3.2×
    over**. Program store (0.126 b/body, gold components-98bc): 16 MB, **317×
    margin**. One pending event per body: 16 GB, **3.2× over** → the queue must be
    sublinear in N; at 0.1-orbit lookahead the in-flight queue is 33 MB. **Clears.**
  - **H_live scar arithmetic** at the measured rate: 0.0207 scars/body/orbit × 128
    bits = 2.65 bits/body/orbit created; unreabsorbed, the 40-bit budget fills in
    **15 orbits ≈ 20 game-years** at a=1.2 AU; holding scars under 10 % of budget
    needs **recompilation each ~1.5 orbits (~2 game-years)** per belt. Growth at
    100× rtf is 828 B/s — the cost that decides is the *recompile*, not the traffic.

**Predictions** (`predictions.md`, written before the run): P2 held (2.80× vs 3×
predicted, inside ±30 %); P3 held (ρ exponent 1.01 vs predicted [0.7, 1.3]); P1
**missed 15× low** (predicted [0.3, 5] hits/body/orbit, measured 0.0207). Per P7,
the failed term is my conjunction pre-factor, not the structure: I counted ~5.4
close conjunctions per orbit over partners within the full Rayleigh radial spread,
but at σ_e=0.01 nearly all bodies sit at e≈0.01 (spread ~0.015, not 0.03), and the
two-dimensional closest-approach condition removes most of the rest; the exponents
(the falsifiable part) held exactly. P4–P6 (the budget verdict) are arithmetic on
measured constants and came out as stated.

**What would make it wrong.** (a) The 5 GB usable figure or 40 bits/body budget
(the approved plan's 4 GiB/20 GiB budgets change it by ×0.8–4, not the verdict).
(b) Encounter rate at the game's real density and ρ: mine is belt-0's config; a
10× denser belt multiplies scar creation 10× and the recompile cadence divides by
10 — measurable with the same command. (c) The assumption that a recompiled program
reabsorbs scars at near-constant bits/body: if the program family's cost grows with
scatter (B18b's open question), the steady state lands at the mixed-belt entropy,
not 0.126 bits — that is the named next experiment. (d) LEO compute "clears" only
with H0190's averaging, measured for tide kicks in hierarchical setups; a fleet
concentrated in low orbits without averaging is 14 cores (3.5× over).
**Cost of adopting:** none in code — it deletes a fear and aims the scale work at
memory (B18b, recompile cost, sublinear queue) instead of event speed.
**Fit with PRINCIPLES:** #1 "The cheapest compute is compute not done"; #6 "Store
the generator, not the generated"; #14 "no ticks" — now a measured bandwidth law;
#24 "The memory floor is information-theoretic" — the 40 bits/body budget and the
2.65 bits/body/orbit creation rate make it a number, not a slogan.

**The lens.** Fermi estimates anchor exponents but not pre-factors (P1 missed 15×
even with the exponents right); the absolute rates here are grounded in the belt-0
reproduction, so the budget inherits only that config's density and ρ. I did not
measure the recompile cost or the program family's growth under scatter — the two
numbers that decide whether reabsorption is real; and a parallel probe
(`hlive-probe` in the shared target dir) may be measuring H_live in-engine this
window, which would ground (c) better than this estimate can. The M1's 60 GB/s and
1e10 ops/s are the board's figures, not measured here.
