# Dossier — 20261011-1814-spacex-a110 (SpaceX lens)

## Claim

The co-orbital phase-neighbour certificate (gold 20261006-0346-taleb-09b5,
adopted into the encounters design; build `b-coorbital-cert`) is a
zero-eccentricity-noise statement: with any injection e-noise, fleet
encounters move to an epicyclic channel that mean-motion (synodic)
conjunction machinery cannot even enumerate — rank-4 at a certificate epoch
catches 100% of encounters at σ_e = 0 but 56% at σ_e = 0.03 — so the
certificate and the design's conjunction timing both need an epicyclic term
before `b-coorbital-cert` is built.

## Bottleneck

The board's top scaling risk: "candidate pairs per body grow with N;
candidate work must track real encounters" (focus item 6; HANDOFF "Risks to
attack first", first entry). The gain at stake is not a speedup but avoiding
a false certificate being built and frozen: a tier that silently drops 44%
of a real fleet's encounters is a missed-contact bug at 10⁶ ships (the gold
itself killed the window tier for exactly this class of reason).

## Evidence

All commands run from `lab/results/20261011-1814-spacex-a110/` on the lab
Linux box (8 vCPU, load ~1, 15 GB RAM, python3/numpy 1.26). Each command
≤ 10 s. The instrument is direct Kepler integration of 2D swarms (no mutual
gravity — the same model class as r8's encounters work: candidates are orbit
overlap, encounters are close conjunctions).

1. **The epicyclic channel exists and dominates fleet encounters.**
   `python3 probe2.py` (packed convoy of 256 slot ships, a-noise 1e-4,
   b = 3e-3 of a, T = 8 orbits, births excluded):
   σ_e = 0 → 39 encounters (8 orbits), partner rank-at-epoch max 3;
   σ_e = 0.003 → 535 encounters, rank max 7;
   σ_e = 0.01 → 542, rank max 11;
   σ_e = 0.03 → 536, rank max 21.
   Encounter count jumps ~14× the moment e-noise is nonzero: those are
   epicyclic conjunctions. A dispersed ring shows the same rank decay
   (frac≤4: 1.00 → 0.54). Rank-4 is exactly right for e = 0 and decays
   roughly linearly in σ_e.

2. **Synodic enumeration cannot see the channel (falsification of my own
   first instrument, and of any timing built on mean motions).** My event
   engine (`probe.py`, mean-longitude crossings + Newton refinement) reports
   **0** encounters on ring n=256, σ_a=1e-3, σ_e=0.03, T=2 where
   integration finds **125** (at dt=0.25 it finds only 57 — the epicyclic
   passes are fast, another way the channel hides from coarse synodic
   thinking); a pair verified by integration to close to 1.7e-4 has no
   event at all. Mechanism (verified): relative *true*
   ±2√(e_i²+e_j²) every orbit, so pairs with |Δλ_mean| inside that band
   align **twice per orbit**; the synodic model places their first meeting
   1/|Δn| ≈ 500 orbits away. The channels trade rather than add: circular
   ring 116 encounters (synodic: |Δa| < b at alignment, ~97% of alignments)
   vs σ_e = 0.03: 125 total ≈ 8 synodic (e-spread spoils the radial match)
   + ~117 epicyclic. **I retract every column of probe.py's sweep table**
   (results.json): it measured only the synodic channel. The analytic
   Binet-cone pair count stands: in co-orbital swarms the cone passes
   ~all pairs (4095 of 4096 partners), confirming the gold's window-tier
   kill, independent of the broken engine.

3. **Rank-at-epoch is the right operational metric** (defined and pre-
   registered in predictions.md before the decisive run): at the instant of
   an encounter the partner is trivially your angular neighbour; what a
   certificate can promise is which partners were within rank k *when it
   was built*. The e-noise numbers in item 1 are that metric.

## Predictions

Written before the decisive run (`predictions.md`), with a post-mortem
appended. Prediction 1 was tested by a broken instrument and is void;
prediction 2's direction (spread breaks rank-4) is confirmed on the e-axis
by the brute-force rerun; 3–6 untested (their sweep retracted). The
pre-registered kill criteria therefore never fired — what fired instead was
my own harness check, which is the run's honest lesson (5 October's memo
artifact, again: agreement between event engine and hand analysis was not
independence; both shared the synodic assumption).

## What would make it wrong

- The probe is 2D (the game's plane) and gravity-free between members, both
  as in r8's encounters model; inclination and perturbed precession could
  smear the epicyclic band, but precession rotates the band's phase, not its
  width — the channel survives.
- b = 3e-3 of a (fleet-spacing encounters, ~450 km at 1 AU). Smaller b
  thins both channels together (rate ∝ b), and the rank-at-epoch spread
  comes from the band width in phase (∝ σ_e), not from b.
- n = 256, T = 8 is small; the mechanism is analytic and measured, but the
  rank distributions' tails at fleet scale (10⁶, k needed ~ band width ×
  phase density ≈ 2√2·σ_e·n/2π ≈ 4.5·10³ at σ_e = 0.01) are an estimate,
  not a measurement.
- If the design's certificate rebuilds every orbit (not per epoch), rank-k
  matters less than rebuild cost; the churn to pay is then the epicyclic
  transposition rate (2 per orbit per band partner; band partners per body
  ≈ 4√2·σ_e·n/2π), which for a 10⁶ fleet at σ_e = 0.01 is ~3.6·10⁴
  transpositions per body per orbit — that number, not the synodic swap
  rate, is the phase tier's true steady cost. Estimate, flagged as such.

## Cost of adopting, and fit with PRINCIPLES

Adoption is cheap and belongs inside `b-coorbital-cert` before it is built:
the certificate's neighbour set must span the epicyclic band (k or rebuild
cadence sized by σ_e, a dimensionless number the swarm already carries),
and the timing machinery (r8 v2's continued-fraction next-conjunction,
built on mean motions) must gain the band term or it under-reports
conjunctions by orders of magnitude in fleets. PRINCIPLES: "a fix signals
the wrong representation" (19) — the synodic representation is the wrong
water for co-orbital fleets; principle 32 — the symmetry to exploit is the
oscillation band in true longitude, found by changing representation, not
by paying more compute; principle 2 — the miss here is behavioural
(dropped contacts), not a fidelity nit.

## The lens

SpaceX: question the requirement, then delete. The hidden requirement this
run surfaced is "fleets have e = 0" — no owner, and false (shipmem's own
birth model injects noise). The lens's blind spot cut the other way too:
hardware-rich iteration made me trust a fast analytic engine over slow
integration; the 60-second test budget argues for exactly that, but the
first brute-force cross-check (one command, 0.3 s) is what caught the
false instrument. Run that check before any sweep that reuses this probe.

## Reproduce

```
cd lab/results/20261011-1814-spacex-a110
python3 probe2.py          # items 1 and the rank table; ~7 s total
python3 - <<'EOF'          # item 2: the falsification, 0 vs 125; ~1 s
import numpy as np, probe
rng = np.random.default_rng(99)
a,e,w,M = probe.swarm(rng, 256, 1e-3, 0.03, 'ring'); nn = a**-1.5
T = 2*np.pi*2; b = 3e-3
i,j,t,miss = probe.conj_times(a,e,w,M,nn,T)
print('synodic-engine encounters:', int((miss<b).sum()))   # 0
dt = 0.05; inside = None; cnt = 0
for s in range(int(T/dt)):
    r,th = probe.kepler(a,e,w,np.mod(M+nn*s*dt,2*np.pi))
    X,Y = r*np.cos(th), r*np.sin(th)
    d2 = (X[:,None]-X[None,:])**2 + (Y[:,None]-Y[None,:])**2
    now = d2 < b*b
    if inside is None: inside = np.zeros_like(now)
    cnt += int(np.count_nonzero(np.triu(now & ~inside, 1)))
    inside |= now; inside &= now
print('integration encounters:', cnt)                       # 125
EOF
```

`probe.py` is kept as the falsified instrument plus its retracted sweep
(results.json) — evidence for the mechanism, not a result.
