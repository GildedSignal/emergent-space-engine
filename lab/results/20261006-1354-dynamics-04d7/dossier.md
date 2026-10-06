# Dossier — 20261006-1354-dynamics-04d7 (lens: dynamics and attractors)

**Claim.** The belt's birth program does not survive its own stirring: at the repo's
belt-0 encounter density the exact program+scar store crosses the 10⁹-realistic 16
bits/body line within **11–12 orbits** at the coarse behaviour quantum (36–39 with an
entropy-floor codec) and within **one orbit** at working precision; the store then
saturates (λ shear wraps to uniform; a/e diffusion keeps paying ~2 bits/body per
doubling) at **≈40 bits/body** (behav) / **≈150** (work) — so 10⁹ stirred bodies cost
5 GiB at player resolution and the program form survives only via epochal re-birth,
which the measured schedule prices at 20 bits (T=20 orbits) to 34 bits (T=200).

**Bottleneck.** Board focus item 5, verbatim: "fitting 10⁹ in 8 GB (population programs
plus scars), decided by distinctions created per game-second". components-98bc measured
the birth floor (0.126 bits/body) and scars under *synthetic fixed* churn, and listed
"scar churn under real encounter rates" as unmeasured. This run measures it endogenous:
the distinction rate is not a constant — it is ~0.18 bits/body/orbit at orbit 20 and
decays ∝ 1/t (0.049 at 60–200, 0.0025 at 600–1980), because the belt is a sub-diffusive
(log-growing) source, not a linear tap. What it deletes: any memory design that assumes
the birth program holds for the game's lifetime; what it prices: the re-birth epoch.

## Evidence (commands ≤ 60 s except the three mild long runs, 51–71 s each; Linux x86,
8 vCPU, load 2.3, 2.0 GB RSS total; Python 3.12; all in `work/`)

Simulator: `belt_sim.py` is 20261006-1029-dynamics-6875's checker-reproduced belt, byte
for byte (first order in e, GM=1, impulse = rotation of v_rel, exact event times, no
ticks). New layer `scar_bits.py`: the belt is born as its program (frozen birth
elements); a scar is the body's exact quantized difference from it, costed with the
shipped codec's structure (Elias–Fano ordinals, 2+log₂(n/k) bits; zigzag-gamma value
rows) and bracketed by an entropy-floor model (log₂(m+1)+1). Sub-quantum deviation is
free and accumulates exactly (principle 6). λ is stored as the wrapped epoch-0 phase
mismatch; the reader propagates with the true n(a), so shear is derived, not stored.

```
cd lab/results/20261006-1354-dynamics-04d7/work
for s in 0 1 2; do python3 scar_bits.py --gm 0   --orbits  200 --n 200 --seed $s --snap-every 20 --out data/gm0_s$s.json;   done  # 0.3 s
for s in 0 1 2; do python3 scar_bits.py --gm 5e-8 --orbits 2000 --n 200 --seed $s --snap-every 20 --out data/mild_s$s.json; done  # 51-71 s each
for s in 0 1 2; do python3 scar_bits.py --gm 1.5e-7 --orbits 800 --n 200 --seed $s --snap-every 20 --out data/hot_s$s.json;  done  # 38 s parallel
for s in 0 1 2; do python3 scar_bits.py --gm 5e-8 --orbits  60 --n 200 --seed $s --snap-every  1 --out data/early_s$s.json;  done  # 3 s
python3 analyze.py gm0 mild hot
```

Tiers match 1029-dynamics-6875 (gm 0 / 5e-8 / 1.5e-7; kicks 0 / ~0.76 / ~1.0 per body
per orbit; encounters 3–7 / 40–54 / 24–29 per seed window; control drift exactly 0).

- **Control (gm=0): bpb ≡ 0.000, k = 0, deviations exactly 0** at every snapshot, all
  seeds (P2): the frozen belt *is* its program, and the instrument's zero.
- **Ruin horizons (mild tier, the belt-realistic one), 3 seeds:**
  - work quanta (27-bit a over the band, 12-bit e, 44-bit t_p): 36–47 bits/body at
    orbit **1**; 16 bits crossed before the first snapshot; ≈116 by orbit 16.
  - behav quanta (q = ρ = 1e-3 in a, e; ρ/a in λ): 8 bits at orbit 4, **16 bits at
    orbit 11–12** (gamma) / **36–39** (entropy-floor). f_scarred saturates as
    1−e^{−0.2·t}: k = 0.17 at orbit 1, 0.91 at 8, 1.00 by 32.
- **Saturation, not unbounded growth:** hot and mild converge to the same place
  (147.4–147.5 and 149.9–150.7 at work; 39.9–40.0 and 42.0–42.6 at behav). Decomposition
  (hot s0, work): λ column saturates at ~83 bits = wrapped-uniform by orbit ~80
  (incompressible against a *fixed* program); a column 36.5→41.8 (20→780 orbits) tracks
  the diffusing spread (da_p90 3.9e-3→2.2e-2); e columns 7→12 each. Late slope
  +2.7–3.2 bits/doubling (work, r² 0.98), +1.9–2.4 (behav, r² 0.97): the *rate*
  decays ∝ 1/t but never reaches zero inside the window.
- **Bulk, not tail:** da_p90 ≤ 1.8e-2 and da_max ≤ 3.6e-2 at orbit 1980 (birth band
  0.5 wide) — no scatterers; the cost is the ensemble's own decorrelation (P6).
- **Seal work does not decay:** rowwrites/kicks = **1.00** in every stirred run — every
  kick rewrites a quantized row at behav; the sub-quantum grace is only ~10–20 kicks
  (principle 6 buys orbits, not centuries at this density).
- **Re-birth schedule (mild s0, bits at refit interval T):** T=20 → 20.1/13.7,
  T=60 → 27.1/17.5, T=200 → 34.0/21.2, T=1000 → 37.4/23.1 (gamma/floor). Refit cost is
  one inference pass; components-98bc measured block inference at ~0.4 µs/body —
  ~0.4 s at 10⁹ per epoch, in idle time (principle 17).
- **Census arithmetic:** 10⁹ at 40 bits/body = 5.0 GB (4.7 GiB) of the 8; at 16 bits = 2 GiB.
  Stirred-belt census ≤ ~4×10⁸ if tubes/catalogues/view get half the machine; dormant
  regions keep the 1.3×10⁻⁴ bits/body program form.

## Predictions (`predictions.md`, written before the sweep; pilot disclosed inside)

Held: P1's law (log-family, neither flat nor linear; behav slope 1.9–2.4 inside the
predicted 0.5–2.5); P2 (control exactly zero); P4 (λ carries 52–56% ≥ 50%); P6; P7
(rw/kick 1.00 ≥ 0.5); P5's work half (working precision ruins < 10² orbits).
Failed: **P5's behav half — the 16-bit crossing is at ~11–12 orbits, not 10²–10³**:
I underestimated f_scarred's saturation (0.2/orbit) and how early shear crosses ρ/a.
P3 holds only in the floor model (79 ≤ 121); the literal gamma reading (147 > 121)
failed because zigzag-gamma pays 2× entropy — the real block codec (FORZ around the
median) sits inside the bracket, which is why both models are reported everywhere.
P1's work slope (2.7–3.2) also sits outside my band for the same 2× reason.

## What would make it wrong

The kick rate is the repo's belt-0 convention (0.75 kicks/body/orbit at the 4e-3
overlap margin); a sparser belt stretches every horizon ∝ 1/(kick rate) — but then the
game has no encounters either, so the horizon-vs-density trade is the design input, not
a refuge. The horizon also scales linearly in the quantum (t_× ≈ q_λ/(0.2·kicks/orbit
… measured: ~12 orbits at q=ρ): a coarser player quantum buys time linearly, memory
logarithmically. The scar cost model is not the shipped codec; crossings move 3× between
the bracket's sides (11 vs 36), so the adoption decision needs one run of the real
`Program::seal` on these trajectories — the law (saturation at ~40/~150, log growth,
λ-wrapping) is robust to it. First order in e (inherited; e ≤ 0.052 in window). N=200
at fixed band = fixed density; per-body curves carry to 10⁹ at the same density, and
the census arithmetic assumes belts dominate the body count. The re-birth pass is
assumed to reabsorb scars into a fresh program without changing behaviours — that is a
law change B18b must judge (tails, equidistribution), not a free operation.

## Cost of adoption, fit with PRINCIPLES

Design inputs, no code: (1) **the scar quantum must be the behaviour quantum** — working
precision ruins the only store form that fits the machine within one orbit (147→40
bits); (2) **re-birth epochs are mandatory** for stirred belts at 10⁹-scale census:
refit on the measured schedule (T=20–200 orbits holds 20–34 bits) as an idle-time
inference pass; (3) **the store's form should switch by the stirring number** (kicks
per body per quantum-crossing time), the same regime logic as the encounters gold —
dormant regions stay program-only. Fit: "Store the generator, not the generated" (6) —
measured: the generator alone buys ~a dozen orbits at encounter-rich density;
"influences below one quantum accumulate" (6) — the grace is real but ~10–20 kicks;
"the memory floor is information" (24) — after stirring, the floor *is* the state;
"the simulation decides" (22) — the distinction rate is the belt's own dynamics, and it
decays as 1/t; "rough first, refine when a certificate could break" (21) — the re-birth
epoch is exactly that refinement schedule.

## The lens (what dynamics made me miss)

An attractor lens reads "saturation" as safety; here the saturation *level* (40 bits at
player resolution) is itself over the machine line — the attractor is the ruin. The
codec bracket (gamma vs entropy floor) moves the headline crossing 3×; a checker must
re-run with the shipped codec before the number is quoted. And the game-time mapping
decides urgency, not the orbit count: 12 orbits is 30 hours of play for a 90-minute-orbit
scene but 17 game-years for the a=1.25 AU belt — the census question (how much of the
10⁹ is stirred at all) is the real gate, and this lens did not measure it.
