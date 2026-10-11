# Dossier — 20261011-1102-second-20261011-0924-library-9834-5c16 (second author on 20261011-0924)

**Claim.** The checker's named gold experiment is done: under real kicks at the plane's
rate (κ=0.3/body/orbit, eps=1e-6, slack-skin quantum s=4·eps_u), the original's
three-number record does **not** hold — its retrigger period (the phase-error quantum,
measured 13/263/449 synodic intervals at ρ=1e-4/2e-3/5e-3) is the same order as the
slack-skin period, so with the record's own scan-based window construction charged,
amortized work per interval is **0.05–0.89× the plain per-interval scan** (a 1.1–20×
loss, rising to 96× at eps=1e-4) and work per real encounter is 43k–3.97M evals against
scanning's 38k — the 33–146× claim inverts under real kicks; what survives is a
different certificate (exact per-kick anchors + closed-form conjunction-longitude
arcs), which wins 18–23× on work but is **not proven zero-miss** anywhere that hits
exist, because at belt eccentricities (e up to 0.08) the relative longitude rate
reverses (94–100% of pairs) and the hit set is genuinely 2D.

**Bottleneck.** The board's top scaling risk (candidate work must track real
encounters); the open premise of the silver: "the retrigger rate is the element-change
rate — exactly what the slack-skin rung must measure, and if it exceeds the return
times the win inverts." Measured: it does.

**Evidence** (Linux x86, 8 vCPU, load shared; every number regenerates from
`python3 probe2.py A B C D E F G` in this folder, ~156 s total (deterministic: re-running any config reproduces every field bit-for-bit except wall time; seeds via crc32), 1 core, < 200 MB;
results2.json holds all aggregates and per-pair records; probe0.py is the original's
script, unchanged, for reference).

Setup: 300 belt pairs (the original's distribution: a∈[0.97,1.03], e≤0.08, Δa∈[0.0008,0.03]),
kicks `a←a(1±eps)` with M continuous (the crate's kick, M-continuity stated), Poisson at
κ=0.3/body/orbit; truth = piecewise-exact Kepler, per-synodic-interval dmin, 48 samples
+ conjunction refinement; uniform work unit = one Kepler-pair evaluation, arithmetic at
1 arith = 0.01 eval (stated; the original conflated phase tests with interval scans).

| config | skin retrigger (intervals) | phase quantum (intervals) | as-stated vs scan | ψ-certificate vs scan |
|---|---|---|---|---|
| A ρ=1e-4, eps=1e-6 | 12.9 | 13.0 (min 5) | **0.049** | 22.6× |
| B ρ=2e-3, eps=1e-6 | 254.8 | 263.2 (min 47) | **0.89** | 18.6× |
| C ρ=5e-3, eps=1e-6 | 581.8 | 449.2 (min 87) | **0.74** | 19.3× |
| D ρ=2e-3, eps=1e-5 | 24.6 | 25.8 (min 8) | **0.099** | 17.9× |
| E ρ=2e-3, eps=1e-4 | 2.2 | 2.0 (min 1) | **0.010** | 18.2× |
| F co-orbital Δa≤0.003 | 28.9 | 30.0 | **0.11** | 7.2× |
| G frozen control (eps=0) | 1 epoch | never (1369) | 5.2× | 24.3× |

- **The retrigger law.** Skin period ∝ ρ/eps (12.9→254.8→581.8 with ρ; 254.8→24.6→2.2 with
  eps), and the frozen θ-record's phase-error quantum tracks it (13.0/263.2/449.2). Both
  quanta are the same physics: a kick moves the rotation number by 1.5·(a/Δa)²·eps,
  amplified 10²–10⁴× for close pairs; the record's slack (window width ∝ ρ) shrinks
  with ρ at the same rate. The frozen control never breaks (phase quantum = full
  epoch) — the instrument is sound.
- **The inversion.** as-stated work per encounter: 43,059 evals (B) vs scanning's
  38,315; 3.97M (E) vs 41,349. At the incumbent's ρ=1e-4 (A) it is 20× worse than
  scanning outright. Even **frozen** (G), honest accounting gives 5.6×, not 33×:
  the original charged ~1 unit per certificate while its own construction is a
  1024×48 scan, and counted a phase test as equal to an interval scan — the
  33–146× was an accounting artifact, before kicks even enter.
- **Two defects in the original record, found while rebuilding it.** (1) Its
  `kepler()` never rotated positions by ϖ, so its belt was effectively
  aligned-pericenter while registering "random ϖ"; the checker's verification shared
  the harness (the memo-artifact lesson again). (2) The "naive forward-scan 6.4×/14×"
  baseline is withdrawn: not derivable from the original's stored outputs (confirmed
  by the first checker; my uniform-unit table replaces it).
- **What actually survives.** Under kicks the strobe is 2D: the relative longitude at
  strobe walks ~±2.9 rad per skin epoch (measured), shifting a θ-window by
  (n1/Δn)·δD — amplified 23–700×. The repair — exact anchors per kick (O(1) arith)
  plus closed-form encounter arcs in conjunction-longitude space ψ = ϖ1+M1−(n1/Δn)D
  (radial gap + impact parameter at each longitude; no Kepler solves; rebuilt on a
  1/128 Binet-cell quantum) — wins 16–24× on work at every config, **but** its
  zero-miss failed everywhere hits existed to check: in C, reversal pairs missed 1323/2817 hits and the
  non-reversal corner is too thin to certify (its few hits were covered in the final
  seed, but 8 pairs cannot establish zero-miss).
  The reversal condition e_max > 0.75·Δa/a holds for 94–100% of the belt: the
  equation-of-center wobble fatens the hit set to 2D (principal conjunction plus
  wobble satellites). The 1D certificate, in either variable, does not cover a
  realistic belt; the record must store a 2D hit set or pay wobble-width false alarms
  (measured: ψ false alarms 21–27% of intervals at B/C).

**Predictions** (predictions.md, written before the decisive run). P2 held (as-stated
< 1× scanning in every kicked config). P5 held (retrigger ∝ ρ/eps, both quanta). P6
held (co-orbital: no 1D win; ψ's 7.4× matches the first checker's number with the
mechanism now named). P1 failed as framed (predicted phase quantum < 25 intervals at
all ρ; measured 229/426 at ρ=2e-3/5e-3 — the slack scales with ρ, so the quantum tracks
the skin period rather than dwarfing it; the inversion stands on the charged
construction, not on a faster retrigger). P3 half-held: the frozen record's phase
quantum never breaks (instrument sound), but my as-stated window at 256 phases misses
25% of frozen hits (resolution floor), so I do not use as_miss as evidence; the
inversion rests on retrigger rates and charged accounting, which are
resolution-independent. P4 failed: the ψ-certificate is not zero-miss where hits exist
— it is a lead, not an adoptable certificate.

**What would make it wrong.** The inversion rests on charging the record's
construction; a window derivable in O(1) from elements would remove that term — but
the measured 2D-ness (reversal wobble, ±2.9 rad relative-longitude walk) is
construction-independent and kills the three-number form regardless. My truth is a
2D coplanar probe with a-only kicks; e/ϖ kicks add V,W Binet drift (same skin
mechanism, untested), and 3D belts, resonant fleets and Hill-regime pairs are outside.
The ψ work-win (16–24×) is arithmetic-dominated (1 arith = 0.01 eval conversion,
stated): if real implementations pay more per anchor update, it shrinks; at 0.1 eval
per kick it is break-even. Adoption cost of the surviving direction: per-pair exact
anchors (two body-shared integrals, O(1)/kick), a 2D hit-set representation with the
wobble geometry, and the Diophantine jump on the per-stretch rotation — no new physics.
Fit PRINCIPLES 14 ("no work for no reason, ticks make no sense to me": the record
tried to delete the scan and the kicks deleted the record) and 19 ("a fix signals the
wrong representation": the θ-window was the wrong variable; the certificate's slack
belongs in the conjunction-longitude/geometry units, and even those go 2D at belt e).

**The lens.** Second authorship pushed me to reproduce first and theorize second; the
reproduction itself found the frame defect and the unit conflation, which no amount of
further analysis of the original's numbers would have. What I may have missed: the
2D hit set may have exploitable structure I did not probe (the wobble satellites sit
near pericenter longitudes — a fat-arc certificate with pericenter-anchored satellites
could restore a 1.5D record); and I ran no resonant or 3D cases. The cheapest decisive
follow-up: wobble-satellite arcs around pericenter longitudes, audited the same way.

Wall time: 0.06 s
