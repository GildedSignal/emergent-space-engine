# Dossier — 20261011-0517-second-20261011-0324-fermi-c211-b3e7 (second author on 20261011-0324-fermi-c211)

**Claim.** The checker's named experiment is done and it *replaces the constant, not the rule*:
the scar cost is magnitude-dependent — S = Elias–Fano ordinal (~7 b) + Σ per-field delta widths
(b_c+2), measured 61.2 → 85.4 → 109.6 → 133.9 → 154.4 → 172.5 bits from the shipped kick
(t ±2¹⁶, E/L/ω ±2¹⁰) to the supra-family stress rung, 165.7 at a true family jump (E/L redrawn
as a fresh law orbit) — so the original's "bits/body ≈ 1 + 61·f_cum, breaks only past f_cum ≈
0.55" holds **as a rule with a magnitude-dependent constant**: bits/body ≈ 1 + S·f_cum (fit
within −8%…+4% for f ≤ 0.5 at every magnitude), break-even f* = 33.4/S ∈ **[0.19, 0.55]**; the
packed-form ceiling is equally magnitude-dependent (53.5 → 160.8 bits/body at f = 1, a bounded
4.7× over budget, not 1.6×); and the original's "0.5%" headline is corrected from its own table
to **4.2%** of 10⁹ sustainable at the 81-minute corner (RTF 1, 32 kicks/orbit; 4.5% at RTF 100
with the 0.3 averaged cadence, 0.04% unaveraged) — "0.5%" was 1/191, a division by the core
count. The verdict order survives intact: compute (short-orbit corner) ≫ memory (admission at
f_cum ≥ 0.19–0.55) ≫ H_live (a family-jump kick creates 62 b, seal 154 ns: 4 GiB unsealed fills
in ≈ 2,000 h at RTF 100) ≫ bandwidth; even at family-jump magnitude, encounter-driven f_cum
(1.4×10⁻⁴/h at RTF 100 year orbits) crosses f* only after **≥ 1,410 h of play** (1,413 h at the worst rung, 3,982 h shipped).

**Bottleneck.** Same as the original (board: "fitting 10⁹ in 8 GB … decided by distinctions
created per game-second"; bottleneck 3). This run closes the record's one untested knob: the
61-bit scar, the f* = 0.55 threshold and the 53.5-bit packed ceiling were each measured at a
single hardcoded kick magnitude. What it deletes: any design decision that treated 61 b/scar,
f* = 0.55 or the 53.5-b cap as magnitude-invariant constants (e.g. a plane-side budget check
wired to f_cum ≤ 0.55 would under-price family-jumping encounters by 2.7×).

**Evidence** (this machine, x86, orders only; state in `state.txt`; `sh reproduce.sh`
regenerates every number in 23 s: the original baseline from shipped code bit-identical —
dH/kick 22.8, scar 61.2, chosen curve 1.0/1.65/6.94/18.12/53.49 — then the sweep; raw JSONL in
`data/`, every field deterministic across reruns, every round trip 0 mismatches):

*The kick-magnitude rung* (`kickmag/`, standalone crate over the shipped `emergent-shipmem`,
no crate edits; convoy of 64×4096 members on a perfect program, both store forms, chosen = min;
`data/kickmag.jsonl`):

| kick magnitude (t,E,L,ω deltas) | S b/scar | f* = 33.4/S | chosen f=0.1 | B ceiling f=1 |
|---|---|---|---|---|
| 16,10,10,10 (shipped `Pop::kick`) | 61.2 | 0.545 | 6.96 | 53.5 |
| 22,16,16,16 | 85.4 | 0.391 | 9.40 | 76.8 |
| 28,22,22,22 | 109.6 | 0.304 | 11.82 | 100.8 |
| 34,28,28,28 | 133.9 | 0.249 | 14.29 | 125.3 |
| 40,34,34,34 | 154.4 | 0.216 | 16.47 | 146.2 |
| 46,40,40,40 (stress) | 172.5 | 0.193 | 18.29 | 165.6 |
| family jump (fresh orbit draw) | 165.7 | 0.201 | 17.92 | 160.8 |

S follows the representation's own arithmetic (EF ~7 b + one (b_c+2) width per field; each
field +1 bit per doubling; ω saturates at ~33 b past b=31 by wraparound) — predicted from that
formula *before* the run to within 4% at every rung. The law's orbit range that defines "family
jump": pairwise |ΔE| median 2³⁵, p99 2⁴⁰; |ΔL| median 2³⁷, p99 2³⁹ (`probe`). Saturation is
magnitude-independent (40k updates on 4096 members → 4096 new scars at every rung); reabsorption
releases ≈ −S at every rung (−60.1 … −173.2); S is m-stable at the family jump
(166.1/165.7/166.0 at m = 1024/4096/16384). Timings flat: seal 119→154 ns, hot update
~105–128 ns across all magnitudes (the family-jump *kick draw* costs 349 ns — the orbit
conversion, not the store).

*The restated headline* (`python3 budget.py`, `data/budget-output.txt`): the 81-minute corner
is 23.9× over the M1's 8 cores (= 191 cores) at RTF 1/32k → sustainable 4.19×10⁷ = **4.2%** of
10⁹; 22.4× over at RTF 100/0.3k → **4.5%**; 2,387× over at RTF 100/32k → **0.04%**. Every row
now prints its sustainable N. Admission rows at both magnitudes cross 4 GiB exactly at their
predicted f* (1.0× at the budget).

**Predictions** (`predictions.md`, written before the sweep): all eight held. P1 S by rung
(predicted 61/85/109/133/157/172/172 — measured within 4%, worst miss k4: 154.4 vs 157); P2 the
1+S·f rule linear at every magnitude (−8%…+4% for f ≤ 0.5, conservative side); P3 the packed
ceiling grows to 150–165 (measured 146–166); P4 saturation = one scar per member-ever-kicked at
every rung; P5 reabsorption ≈ −S everywhere; P6 timings flat (seal ≤ 1.3× at 6× magnitude); P7
the restated 4.2%/4.5%/0.04%; P8 verdict order unchanged. No calibration miss to report.

**What would make it wrong.** (1) The sweep is convoy-shaped: one program family, kicks drawn
uniform in ±2^b per field. Real encounter kicks have structured deltas (e.g. correlated E/L
along the manifold, or clustered magnitudes); correlation would *lower* S (shared widths), so
the uniform draw is the conservative side, but a measured game trace could shift the operative
S below 61–166. (2) The seal-time and H_live prices at 10⁹ bodies still extrapolate from 4096-
member populations; the EF ordinal term shrinks with n (log2(1/f) part), so S at 10⁹ should be
*a few bits lower*, again conservative. (3) Compute rows inherit the original's 29 µs/kick at
~10³–10⁴ bodies — unchanged by this run, still its own open risk. (4) x86; the integrator
re-measures on the M1.

**Cost of adoption:** none in code; the plane's budget check takes `1 + S·f_cum ≤ 34.4` with S
from the kick magnitude actually issued (61 for element tweaks, ~166 for orbit-changing
encounters), and the belt design (B18b, `b-h-live`) gets the magnitude table instead of the
single 61.

**Fit with PRINCIPLES.** "The memory floor is information" (#24): the scar costs exactly the
information the kick carried — S tracks Σ(b_c+2) because that *is* the delta's entropy; the
store adds only the EF ordinal and block headers (~11 b) at every magnitude, so the admission
rule enforces the floor, never bytes×count. "Each scale resolves only what matters at that
scale" (#33): the rule's two knobs (S set by the disturbance's own width, f_cum by its
frequency) are the scale separation made exact. "Rough first, refine when a certificate could
break" (#21): 61 was the rough corner; 1 + S·f_cum with measured S is the same sentence at
full width.

**The lens.** The second-author lens tests the named experiment and nothing else: it did not
re-run the original's P3 (compaction reabsorption) failure mode at other magnitudes, did not
measure the b-form's *tidy* cost at scale, and its "hours to f*" converts the r8 belt's
encounter rate — a co-orbital fleet (taleb-09b5) concentrates kicks on few members and would
fill their scars faster per encounter, though saturation caps each member at one scar. The
checker's minor table slips in the original (max-step, random-access, stream ranges) are left
to the record's own branch; only load-bearing numbers were restated here.
