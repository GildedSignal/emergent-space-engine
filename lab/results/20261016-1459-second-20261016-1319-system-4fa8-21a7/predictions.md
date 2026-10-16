# Predictions (written before the decisive runs; 2026-10-16, second author on 4fa8)

The checker's named experiment: fly the B13/B14-class legality gates under the chained+stagger
law with shifted boundaries, and re-state the ES_LOCAL_PHASE comparison on the equal-bill basis.
Controls: OFF (patched, default-off; digest already proven bit-identical to pristine main
`6895ce06…` this session) must PASS every gate flown — a frozen gate failing on main means the
instrument is broken, not the arm (VOID). ES_LOCAL_PHASE (4c22's arm, ported verbatim into the
same binary) flies the same cases so the comparison is one instrument, one box, one pass.

Cases never tuned on: none of the B13/B14/B12 seeds have been flown under any shifted-boundary
law before (4c22 priced events only; 4fa8 flew frame statistics only). All of these are held out.

- **P1 (the named experiment, legality).** B13 (64 flybys, ΔE/ΔL within 1% for ≥ 99%) and
  B14 (256 moons, class ≥ 99%, apsidal precession within 10% for ≥ 99%) both PASS under
  `ES_CHAIN=1 ES_LOCAL_STAGGER=1`. Rationale: the chained interval is exactly the law's own step
  (stubs were only ever shorter than nominal, never longer), so per-interval accuracy is the same
  in kind; only kick/boundary ticks shift. Risk I cannot price: encounter timing relative to
  periapsis enters B13's ΔE at the percent level.
- **P2 (the handoff gate, most exposed).** B12 (Jacobi error ≤ 1e-4 over ≥ 20 doll crossings)
  PASSes under chain+stagger, with error of the same order as OFF. A handoff leaves a body
  off-grid; under `aligned` a short stub re-anchors it, under chain it runs a full step from
  wherever it stands — same length as its nominal step, so no accuracy is lost in type. If B12
  FAILs: the cure is illegal for handoffs as it stands (adoption blocked), whatever B13/B14 do.
- **P3 (equal bill, rate).** ES_LOCAL_PHASE's incremental event rate past 1,900 game-s (N=1000
  coast, 5,400 game-s) is within 5% of OFF's 3.17/game-s, and its slice count lands at ≈ 8,300
  (the wiki's direction-3 note: 8,337), i.e. the same one-time fleet-bill as chain+stagger's
  8,300. If phase's rate is materially higher (> +5%), the original "strictly better trade"
  framing survives in its event-rate part.
- **P4 (equal bill, CPU).** Over the same 3,300 dumped frames, phase's total engine ms falls
  within 3% of chain+stagger's (both collapse the comb; the CPU win should be shared, leaving
  parsimony — no phase grid, no stub minting — as the differential).
- **P5 (phase legality).** ES_LOCAL_PHASE also PASSes B12/B13/B14 (same class of law change). If
  it fails where chain+stagger passes, that is a real differential in the chained law's favor.

Kill criteria (frozen here):
- B13 or B14 FAIL under chain+stagger → the cure is illegal as stated; "adopt within one step"
  dies; clean refutation, reported as such.
- B12 FAIL under chain+stagger → adoption blocked at the handoff boundary regardless of P1.
- Any gate FAILs under OFF → VOID, the instrument is broken.

What I expect to confirm unchanged (already on the record, not re-measured): the coast collapse
334→52 itself, the burn partial collapse (328→112), N-flat through 10⁵.

## Amendment (re-frozen before any arm flight, 15:09 UTC, after the OFF/pristine controls)

The instrument reading falsified P1/P2's premise: the legality gates are RED ON MAIN as shipped —
pristine `main` and patched-OFF fail byte-identically (B13 60/64 judged within 1e-2, worst 2.12e-2,
matching HISTORY's own "B13 60/64" validation line; B12's growth exponent reads inf through the
statistic the b12 page records as broken; B14 exceeds behave's frozen per-phase 60 s cap on this
Linux box in every arm). No arm can therefore "pass" these gates; the frozen criterion is
re-declared as the DIFFERENTIAL against OFF on the same box, same binary, same seeds:

- **P1′ (B13, the instrument that separated ES_STAGGER's kill: 0/64 vs off 60/64):** chain+stagger
  holds OFF's own class — judged-within count ≥ 60/64 and worst error within 2× of OFF's 2.12e-2.
  Below 60/64 or worst > 2× ⇒ the cure degrades encounter legality ⇒ adoption dies as stated.
- **P2′ (B12 magnitudes):** chain+stagger's worst |ΔC/C| error stays within one order of magnitude
  of OFF's (both arms' exponent reads inf through the broken statistic, so the magnitude is the
  only honest channel).
- **P5′:** ES_LOCAL_PHASE flies the same gates; the differential between phase and chain+stagger is
  itself a result (equal ⇒ parsimony decides; unequal ⇒ the better law on legality wins).
- B14: unmeasurable on this box (frozen 60 s cap < its runtime in every arm, OFF included) —
  reported as such; the M1 re-measure decides it. Its runtime per arm is still recorded.

P3/P4 (equal-bill rate and CPU) are unchanged — they never depended on the gates' state.
