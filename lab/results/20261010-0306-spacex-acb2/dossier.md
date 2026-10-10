# Dossier — 20261010-0306-spacex-acb2 (SpaceX lens): H_live measured from encounter physics

**Claim.** A belt's live distinction rate H_live is set by its mass and its live velocity
quantum, not its body count (N-independent in the sub-quantum regime:
R = corr·1.7·M_belt·σ_e /(W·⟨v_rel⟩·q_v), corr = 2.2 measured), so 10⁹ bodies fit 8 GB
iff the belt's live quantum q_v ≥ ~1e-6·v_K (3 cm/s at 1 AU — 370× below the strongest
kick any player could observe), while the tube-key quantum 2⁻³² breaks the budget by
~2.4×10³ and per-body scarring at B18b scale (2²⁰–2²³) already costs 161–1,290
bits/body/hr — dense belts cannot be run as individuals-with-scars at any quantum; the
aggregate (population + secular) regime is forced, and this run gives the numbers that
decide when a body must leave its program and how often the program must be re-fit.

**Bottleneck.** Board: "fitting 10⁹ in 8 GB … decided by distinctions created per
game-second"; HANDOFF: "H_live … not measured yet". This run supplies the missing number
and its law. What it deletes: per-body scar machinery as a *belt* mechanism (the shipmem
scar layer is for opt-out bodies, fleets and battles, not for dense belts — the encounters
opt-out must be triggered by a dimensionless rate, not left as a default); and any worry
that body count itself drives live memory.

**Evidence** (planar belt, star M*=1, a∈[1,1.02] (W=0.02), e~Rayleigh(σ_e), N=1e4
reference; truth = conjunction-centred exact-Kepler Monte Carlo over Δa bins, min
distance over one synodic period with 4-round zoom; controls: planted blunt sampler
undercounts 10× (0.0003 vs 0.0030), widest bins return P=0; machine idle, load 0.31):

| measured | cold σ_e=0.01 | hot σ_e=0.1 |
|---|---|---|
| Λ(ρ=1e-4) /body/orbit | 0.402 | 0.219 |
| Λ(ρ=1e-3) /body/orbit | 4.23 | 1.94 |
| ρ exponent (3 points) | 1.02 (1.11/0.94 halves) | — |
| ⟨v_rel | encounter⟩ v_K | 0.0106 | 0.132 |

- Closed form (derivable, post-hoc): **Λ = 0.85·N·ρ·min(σ_e,W)²/(σ_e·W)** — 6% off cold,
  22% off hot. Encounter rate is conjunction-geometry-limited (each neighbour pair
  conjunctions once per synodic period regardless of speed): hotter ⇒ *fewer* close
  passes (wider radial spread), Λ ∝ ρ¹.
- Kick tail: per-body kick δv = 2m/(b_min·v_rel); the exact integral over measured (b,v)
  gives **2.2× the independence product** in the tail (lingering near-twins deliver
  small b and small v together; 36 events, σ≈0.4).
- Design table — scar bits per body per hour of play at rtf 100 (scar = 336 bits per
  encounter = 2 bodies × 168; budget 64 bits/body = 8 GB/10⁹):

| M_belt | q_v | 2²⁰ | 2²³ | 10⁹ | verdict |
|---|---|---|---|---|---|
| 1e-7 | 2.33e-10 (tube key) | 161 | 1.29e3 | 1.54e5 | BREAKS |
| 1e-7 | 1e-6 | 67 | 67 | 67 | marginal |
| 1e-7 | 1e-5 | 6.7 | 6.7 | 6.7 | FITS |
| 1e-5 | 1e-4 | 67 | 67 | 67 | marginal |

  The tail rows are N-independent (P7: mass, not count). Minimum live quantum for the
  10⁹ belt, 1 hr at rtf 100: **q_v* = 1.05e-6·v_K (3.1 cm/s at 1 AU) for M_belt=1e-7;
  1.05e-4 (3.1 m/s) for M_belt=1e-5** — systematic ×2 from corr.
- Program re-fit cadence (scars die when the program is re-fit; scarred fraction
  R·T_refit < 0.38): at q=1e-5, M=1e-7 → re-fit every ≤ 79 sim-days ≈ 2.6 real hours at
  rtf 100 — idle-time work, consistent with shipmem's "cheaper form chosen in idle time".
- Player floor: strongest 1-in-400 encounter kick at M=1e-7 is 11 m/s (0.0112 km/s);
  q_v* = 3 cm/s — nothing player-differentiable is erased (principle: "the floor is what
  the player can differentiate").

**Commands** (from `work/`, each ≤ 10 s, regenerate the saved outputs bit-identically —
verified): `python3 probe_hlive.py hlive_raw.json` then `python3 post_hlive.py`
(outputs: `hlive_raw.json`, `post_final.txt`, `hlive_post.json`).

**Predictions** (predictions.md, written before the decisive run): P1 rate ✓ (4.23 in
[1,15]); P2 ρ-exponent ✓ (1.02 in [0.85,1.2]); midpoint check ✓ (1.11/0.94). P3 hot rate
✗ — 1.94 against [10,150]: my kinetic formula (rate ∝ v_rel) is wrong in a sheared
disk; conjunction geometry rules; diagnosis above. P4 b-uniformity marginal (0.372 vs
[0.4,0.6], n=86). P5 ✗ at its one informative point: exact = 2.2× product (> 30% band) —
a real correlation, now measured and folded in. P6 design numbers ✗ both ways (161 vs
"<6" at 2²⁰; M=1e-5 same as 1e-7, not ">200"): I had not internalized that at these N
the belt sits in the all-crossings regime where mass does not matter yet. P7 ✓
structurally (table rows collapse in N). Three of seven held; every failure is diagnosed
and none invalidates the measurement (the truth side never used the failed models).

**What would make it wrong.** (1) Planar only: inclinations add a dimension — rates move
by O(1) factors, the ρ¹ law, the tail structure and the N-invariance survive; the 3D
check is the next rung. (2) Pairwise independence weakens when Λ ≳ 1/body/orbit (2²³ at
this geometry is already a dense gas — there the aggregate treatment is not just cheaper,
it is the only meaningful description). (3) corr = 2.2 measured at one point → ×2
systematic on q_v*. (4) Scar accounting assumes a scar is *replaced*, not appended; if
scars accumulate per body, multiply everything by the scar lifetime. (5) Belt geometry is
my spec (W=0.02, σ_e=0.01), not B18b's exact one — plug the real belt into the closed
form. Cost of adopting: none in code — it is one formula and four numbers; it sizes the
live quantum per belt, the encounters opt-out threshold, and the re-fit cadence. Fit:
"The memory floor is information" (#24); "influences below one quantum accumulate" (#6) —
this run measures exactly where that accumulation starts paying; "each scale resolves
only what matters at that scale" (#33) — the quantum is the knob.

**The lens.** SpaceX delete-first found the deletion (per-belt scars), but it measured a
sterile belt: no planets (resonant pumping from a Jupiter would add a deterministic
secular term — zero bits, but it moves bodies toward the opt-out boundary), no player, no
fleets. The co-orbital concentration case (gold 20261006-0346) is exactly the regime my
table says is impossible as individuals — the two results agree, but the fleet case needs
its own H_live number. The lens also never asked whether the plane's *current* belt
spends scar writes today: that is one `xtask universe --bench` measurement away and
belongs to the directed b-h-live build.
