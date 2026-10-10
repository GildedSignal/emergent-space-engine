# Dossier — the 10⁹ budget, term by term, from today's measured rates

**Claim.** At 10⁹ bodies the M1's wall is not one term: for smooth-belt universes the target fits at rtf 100 once the slack skin lands (kicks 0.24 core-s/real-s, populations ~16 MB), while hot belts (σ_e ≈ 0.1) break **both** remaining terms by ~1 order each (encounter work ~36 core-s/real-s, distinctions ~5 GB per real hour), and the single sharpest open number is **f_scar**, the fraction of kicks that must stay distinct: below ~1% over a 10-hour session or memory grows without bound.

**Bottleneck.** Board item 3 (cost at a billion) and the H_live risk (HANDOFF: "they, not the body count, decide whether 10⁹ fit"). This replaces the stale "190 cores" headline with a radius-and-regime statement, and gives the b-h-live build its pass line (f_scar) and its decisive measurement (quantized-key collapse at belt scale). Expected gain: deletes the undifferentiated "N is the problem" framing; redirects the scale work to two measured levers (skin, scar reabsorption).

**Evidence** (all commands ≤ 60 s, this Linux/x86 box, loadavg 0.73, up 43 d; orders of magnitude only — the integrator re-measures on the M1):

- `cargo run --release -p xtask -- universe --kick-bench --seconds 5` → kick median **48.6 µs**, p99 62.5, 23 distinct kicks, `exact_hit_rate 0.0` **and** `quantized_hit_rate 0.0` (23 distinct quantized 12+12-bit keys) [data/kick-bench.json]. M1 anchor: 29 µs (H0210). Used 29 µs for M1 projections.
- `cargo run --release -p xtask -- universe --bench --seconds 10 --unpaced` → 28 bodies, **1203 B/body**, view gather 72% of frame, rtf 1 [data/bench.json].
- `cargo run --release -p emergent-encounters -- verify a` and `verify d` → real encounters 1.7×10⁻⁴–5×10⁻³ per body per orbit for belt-like σ_e, **7×10⁻²** for the hot belt; 1.4k–17.8k evals per real encounter [data/encounters-a.jsonl, -d.jsonl].
- `python3 budget.py` (this folder) regenerates every number below.

Budget at N = 10⁹, rtf 100, kicks 32.5/orbit (H0190 K1), machine share 4 core-s/real-s:

| a (AU) | today (29 µs) | skin (2.3 µs) | avg 0.3/orbit* |
|---|---|---|---|
| 1.0 | 2.99 | 0.24 | 0.028 |
| 0.25 | 23.9 | 1.90 | 0.221 |
| 0.1 | 94.4 | 7.50 | 0.872 |

Break radius a* (inside it, kicks alone exceed the budget): **0.82 AU today, 0.15 AU with the skin**, 0.036 AU with 0.3 kicks/orbit. *The 0.3/orbit row is the H0190 premise bound, not adoptable: q-secular-v2 killed zero-kick phasors at belt scale.

Memory: today's plane 1203 B/body → 1.2 TB at 10⁹ (**2.3 orders over** the ~6 GB line; though at N = 28 fixed overhead dominates — the marginal byte is unmeasured); raw 16 B tubes → 16 GB (2.7× over); populations 0.126 bit/body (components-98bc) → **15.8 MB**. The term spans 5 orders across representations: it is a choice, and today's plane is the farthest from the line.

H_live: kick rate at 1 AU is 1030/game-s per 10⁹; the measured zero quantized-key reuse says every kick currently lands in a fresh cell → **24.7 KB per game-s = 8.9 GB per real hour at rtf 100** if never reabsorbed. Boundedness condition: **f_scar < 1.1%** (1 GB over 10 h; 6.7% for 6 GB). Encounter distinctions: negligible for smooth belts (0.32 bits/s), but the hot belt's 7×10⁻² /body/orbit gives ~14 kB/game-s → **~5 GB per real hour** — the same disease without any kicks.

Claim check (lens item 3): "10⁹ orbiting bodies would need about 190 cores" (board, 29 Sep) re-derives to **~3 cores at 1 AU, rtf 100** under today's event law — 60× pessimistic at belt scale; 190 cores returns only at a ≈ 0.06 AU (inside the star) or rtf ≈ 6×10³. Any "X cores for 10⁹" without (a, rtf, regime) is underdetermined: cadence spans 3+ orders across radius.

**Predictions** (predictions.md, written before the runs): P1 kick cost 5–60 µs — **held** (48.6). P2 bytes/body 16–100 B — **missed high by 12×** (1203; N = 28 fixed overhead included — the marginal byte is the missing measurement). P3 exact ≈ distinct — **held** (23/23, 0% reuse); quantized collapse 3–30× — **missed** (23/23 distinct; a scattered 28-body scene cannot collapse; the belt-scale case is exactly the open measurement). P4 encounters ≤ 10⁻⁴/body/orbit — **missed low by up to 2×** on belt-like rows (1.7×10⁻⁴–5×10⁻³) and by 700× on the hot belt; work ≥ 100/encounter — **held** (1.4k–17.8k). P5 memory half-order for tubes, populations fine — **held**; compute "~3 core-s at 1 AU today" — **held**; a* ≈ 0.5–1 AU today — **held** (0.82); skin a* ≈ 3–6 AU — **missed** (0.15 AU — I inverted the exponent when writing the prediction; the miss is favourable). P6 190-cores overstated ~2 orders at belt scale — **held** (~60×).

**What would make it wrong.** (1) Kicks at 10⁹ need not be paid in real time if lazily derived — but determinism makes them law, and average throughput must still meet the rate; only the *when* is slack, so the averages stand while the p99 story changes. (2) The 4 core-s machine share and 29 µs are M1 anchors; a 2× error moves a* by ±50%, no order changes. (3) f_scar's 24 B/distinction is the memo-entry scale; tube-table entries could be 8 B, relaxing the threshold 3×. (4) The hot-belt numbers come from the encounters crate's verify belts (ρ up to 10⁻³), not the plane's B18b belts — if B18b belts are cooler, the hot wall is a non-scene. **Cost of adoption:** zero code; the budget table, a*, and f_scar become the scale gates' vocabulary. **Fit with PRINCIPLES:** "The memory floor is information" (24: the f_scar threshold *is* that floor made numeric); "Each scale resolves only what matters at that scale" (33: the wall is a function of a and regime, not N); "Fermi-estimate before building… a wrong estimate still deletes half the solution space" (lens). **The lens:** Fermi sees rates and stocks, not mechanisms — it cannot see whether scar reabsorption is *achievable* (a dynamics question, q-secular-v2's territory), and its shared-box timings hide the M1's thermal behaviour.
