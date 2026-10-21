# Dossier — 20261021-1655-redteam-1ae8

## Claim

The design's only gravitational-wave mechanism — "inspiral by Peters' formula" applied as **kicks on
E and L once per radial cycle** (docs/representation.md L67) — fails by type in the plunge band the
player watches: merger time off by 0.23–1.6% at the doll's own licensed edge (p̄ = 65M), tens of
percent inside 30M, and at e₀ ≥ 0.9 the last kick jumps *through* the plunge band (final semi-latus
as low as −0.90M: the merger is fabricated in 1–3 cycles where the truth takes 11–26). No rung in
`lab/rungs/` has any inspiral arm.

## Bottleneck

Off-board (a premise red-team, guarding principles 2/13/29): the letter's error model promises "at
most one floor unit per event, carried forward so that it never compounds" (L60). The inspiral kick
violates it by type: the per-cycle quantum is ~0.2·p at the 6M handover **for every trajectory,
start-independent**, so no certificate that keeps the kick has an operating point in the band where
binaries merge — the tens of cycles that are the spectacle. What it deletes: the kick form of the
inspiral entirely; the record's named cure (df81's "Peters' generator") becomes mandatory and now
has measured bars.

## Evidence

Float falsifier `peters.py` (pure Python, 50 s single core, this folder; raw table in
`peters_out.json`). Truth: Peters' (1964) own orbit-averaged rates da/dt, de/dt integrated
continuously (RK4, dt = P/128, stop-time interpolated). Letter: the same rates applied once per
radial cycle at cycle start (zero-order hold — exactly "kicks on E and L" per cycle; the (a,e) ↔
(E,L) map is a bijection, so no extra channel). This isolates the kick-vs-generator question from
the multiply-add jet already killed by df81/6164/ee08. Stop (both arms): p = a(1−e²) ≤ 6M, the
plunge handover band. Controls: C1 circular truth vs Peters' closed form = 7.5e−8 (prediction bar
1e−9; secant-interpolated stop, disclosed — still 10⁴× below the smallest kill below); C2 truth
P/128 vs P/1024 = 5e−8…1e−10; C3 the negative control (letter at 15M circular) differs by 8.8% > 1%.

Held-out plane p̄₀ ∈ {15,20,30,50,65,100,200}M × e₀ ∈ {0,0.3,0.6,0.9} × ν ∈ {0.25, 0.5}, nothing
tuned (M = 1, G = c = 1):

- **At the doll's licensed edge (p̄₀ = 65M, ν = 0.25):** merger time +0.23% (e₀ = 0), +0.07%
  (e₀ = 0.6), **−1.62% (e₀ = 0.9; 505 cycles vs the truth's 514.8 — 10 wrong orbits)**. Sign flips
  with eccentricity: late for e₀ ≤ 0.6 (stale weak rate), early for e₀ = 0.9 (stale F(e) as it
  collapses).
- **Inside 30M:** −34.6% (15M, e₀ 0.9; 3 cycles vs 11.5), −27.8% (20M), −11.0% (30M);
  +8.8% (15M circular), +4.0% (20M), +1.6% (30M).
- **Type kill (plunge fabrication):** max single-kick Δa/a = 1.07 at 15M/e₀0.9/ν0.25 — the final
  kick drives the semi-latus to **−0.90M** (through zero). At ν = 0.5: one kick ends the binary
  from 15M/e₀0.9 (cyc_l = 1). Final-kick Δa/a is 0.16–0.22 for **every** row regardless of start:
  the quantum at the 6M handover has no certificate that keeps the kick.
- **The law (measured, circular, both ν, 15–200M):** |Δt/t| = 3.5–4.0 × q₀, with the per-cycle
  quantum q₀ = (128π/5)·ν·(M/p̄₀)^{5/2} at start. The e₀ = 0.9 channel is ~7× stiffer (stale-F
  amplification). License bars: 0.1% ⇒ p̄₀ ≳ 230M circular at ν 0.25 (outside the EOB license,
  65M); at e₀ = 0.9 even 1% fails at 65M. ν = 0.5 (equal mass, unlicensed by 97b0) roughly doubles
  everything (16.6% at 15M circular).
- The cycles-to-merger error diverges from the time error at high e (15M/e0.9: −73.9% cycles vs
  −34.6% time): the chirp/phase channel the player perceives is worse than the clock channel.

Reproduce: `python3 lab/results/20261021-1655-redteam-1ae8/peters.py` (≤ 60 s), or `./regen.sh`.

## Ranked attacks on docs/representation.md (the lens deliverable)

1. **Inspiral-by-Peters-as-kicks (L67) — killed above.** Rung that should have caught it: **none**.
   r1 gates the conservative cycle only (precession, periods, ISO, capture); r3 v3 gates the EOB
   map, handoffs, assists — no GW arm anywhere. Proposed `r17-inspiral` (behaviour type): merger
   time and cycles-to-merger within 1% of the continuously integrated Peters rates over
   p̄₀ ∈ {15…65}M × e₀ ∈ {0…0.9} at ν ∈ {0.25, 0.5}; type bar: no kick may cross the 6M handover
   band (max single-kick Δp/p < 1); positive control: the closed-form circular merger time; negative
   control: the per-cycle letter at 20M/e₀0.9 (fails by 27.8%). The record's cure (df81's Peters
   *generator*, e.g. the exact circular a(t) = a₀(1−t/t_c)^{1/4}, refined per cycle) is confirmed
   necessary and now has bars.
2. **The two-body doll's license is missing from the letter (L37).** The record licenses the EOB
   map only at ν ≤ 0.25, p̄ ≳ 65M (97b0); equal-mass binaries — the canonical game spectacle — are
   unlicensed, and my ν = 0.5 rows measure the cost of assuming it anyway (2× the inspiral error).
   Not a type-kill (the 1PN map is analytically ν-exact, conservative); the hole is that no rung
   sweeps ν > 0.25. Rung: none does.
3. **§6's cost table has no GW row.** The inspiral is unbudgeted; my law says a generator must be
   re-derived on a cadence set by q₀ itself (per-cycle inside ~65M at high e), i.e. an inspiralling
   binary is a *live* body with a certificate that shrinks continuously to the merger — the
   "undisturbed ≈ 0" premise does not extend to it. Rung: none.
4. **Thesis 2's shadowing-lemma clause** (a wrong-statistics orbit is a true orbit of nearby ICs)
   fails at non-hyperbolic points — already measured by the separatrix kills (4978: plunge
   fabricated as bound; 2040/9a04: the E-axis failure), and my plunge-band fabrication is another
   instance. On record; cited, not new.
5. **Survivors (worth reporting):** dense ≡ sparse (r5, 506c); undisturbed ≈ 0 for
   non-inspiralling bodies (3294); the ν-in-energy-map at 1PN (r3 v3); Binet cells already
   replaced by the Darwin compilation (r1v2). The premise census's view kills all stand.

## Predictions

`predictions.md`, written before the decisive run. Scored: P2 held (far field +0.01% at 200M;
tested at 200M, not 10⁴M — grid capped for runtime, disclosed); P3 held (+8.80% late at 15M
circular); P4 half-held (sign early ✓, magnitude −1.62% < the predicted 5%); P5 held (the q₀ law,
ratio 3.5–4.0); P6 **missed** (I predicted O(10³) cycles from 20M; the truth is 33.8 — the
inspiral accelerates as a⁴, which makes per-orbit errors *more* visible, not less); P7 held
(−73.9% cycles vs −34.6% time at 15M/e0.9). P1's strictness bar missed (7.5e−8 vs 1e−9, secant
stop), disclosed above.

## What would make it wrong

The truth arm is Peters' own rates, not 2PN/radiation-resolved GR: both arms share that limit, so
the *sampling* kill stands, but the absolute license numbers (65M edge, 6M handover) move with a
better oracle. If the engine hands binaries to the dense order (not the kick layer) well outside
65M, the measured band is unreachable and the attack collapses to a domain note — but then the
letter's clause is dead anyway, since nothing left carries the inspiral. Cost of adopting the
cure: one generator per inspiralling pair (closed form circular, refined at pericentre for e > 0),
re-derived on the q₀ cadence; it deletes the inspiral kick outright.

Fit with PRINCIPLES: "basically we don't want errors that can compound that's the goal" (13) —
per-cycle ZOH is compounded error with a start-independent 0.2 quantum at handover; "a failed
expectation is not automatically a failed method" (9) — this kills the kick *configuration* of the
inspiral, not Peters as the law (the generator keeps it); the rung bar follows " behaviours over
many seeds… judge behaviours and statistics" (20).

## The lens

Premise red-teams overweight exotic cases; I ranked by player visibility, and the winner is exotic
only in mass: binaries with p̄ ≤ 65M are the game's showcase objects. What the lens may have made
me miss: the *rate* of binary formation at game scale (are there any p̄ < 200M pairs at all in the
shipped universe?); a scout should count them before the cure is built. Cloud float, Linux/x86 —
orders of magnitude, exact bars for the integrator alone.
