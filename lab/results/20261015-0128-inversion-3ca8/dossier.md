# Dossier — 20261015-0128-inversion-3ca8 (inversion lens)

**Claim.** The shipped dense-order contact law's chaotic ensemble statistics deviate from
the continuum by 15–45% in a relativistic Fermi-pump gas (one 1000:1 heavy at β 0.6, 64
light tracers, T = 2²⁰ chronons), and the deviation is **Q-independent** (identical at
Q = 2¹⁶, 2¹⁸, 2²⁰) while state rounding alone is innocent and every single contact is the
continuum impulse to 1e-5 — so finer quantization does **not** heal the dense order's
statistics, and no exactness certificate (digest, ledger, per-contact residual) can see
the gap.

**Bottleneck.** Failure path "a law that compounds error into false behaviour classes"
(the inversion list's #1): until now measured only on an abstract map (standard map,
20261014-2248-redteam-5cad) and two-body contacts (contact-carry). This is the first
measurement on the shipped dense order's own many-body machinery. It does not move a cost
bottleneck by 10×; it prices a Truth risk (behaviour classes, not error size — principle 2)
and refutes the "finer Q heals it" adoption path for free.

**Evidence.** All numbers from `cargo run --release -p emergent-lattice --example shadow`
on shipped main + `work/patch.diff` (adds `crates/lattice/examples/shadow.rs`; no library
file touched). Four arms: `engine` (shipped `Chronon`, `Law::RelativisticV1`), `float`
(a twin of the same per-chronon loop — same bin predicate, same advance/walls/respond
order, same id-order sequential impulses, same consumed/revision rule — with continuum
f64 state and the exact analytic SR disc impulse), `grid` (twin + state rounded to the
1/Q grid after every chronon), `micro` (single-contact direct comparison through
`law::respond` vs the analytic impulse). Metrics in γ; "trapped" = γ > 2.

- **Instrument validated three ways.** (i) Pre-contact: engine and float identical to the
  printed digit (neg scene, T = 2⁹–2¹¹: γ 1.00005 / heavy 1.25000 both arms). (ii) Single
  contact through `law::respond`, head-on, light incoming at β 0, 0.97, 0.999 (γ to 82):
  engine 0.882021/0.998036/0.999926 vs analytic 0.882021/0.998036/0.999926 — agreement to
  ~1e-6, both relativistic laws, every Q. (iii) Control-pos (equal masses, β 0.05, where
  contact-carry measured per-contact exactness 1.4×10⁻⁶): contacts 4452 vs 4375 (+1.8%),
  per-light contacts 130 = 130, final γ p50 1.00005 vs 1.00004, p90 1.00014 vs 1.00019,
  max 1.00091 vs 1.00090. The twin sees 2% where the law is exact.
- **Control-neg (the known ledger-walk case, 1000:1 β 0.6, one light):** both arms pump to
  the ceiling (engine γ 150.8 max 251.0; float γ 186.6 max 250.6; both dwell ~1.03–1.04×10⁶
  of 1.05×10⁶ chronons); engine contacts 499 vs 542 (−8%), heavy drained less (β 0.422 vs
  0.342). Same behaviour class; the quantization shifts the pump's rate ~10–20%, not its
  class. (My pre-registered ≥2× expectation here **missed** — the Fermi pump is real
  physics, and the contact-carry ledger walk does not translate into a class error.)
- **Decisive arm (pump, 3 seeds), engine vs float:** trapped-at-end 45/53/52 vs 59/56/60
  of 64 (engine 0.76–0.95×); dwell-γ2 totals median 0.794/0.798/0.807 vs
  0.958/0.954/0.956 ×10⁶ (0.83×); heavy retains 2–8× more kinetic energy (final heavy γ
  1.00033/1.00064/1.00425 vs 1.00006/1.00001/1.00124); contacts 0.96×; final γ p50 0.85×;
  **max continuous dwell above γ2: 102/122/108 vs 21/20/19 ×10³ chronons — 5.3–5.7×
  longer in the engine at every seed** (stickier individual traps while fewer bodies end
  trapped); final γ p90 1.28×, max γ tail noisy (0.5–1.6×).
- **Q-independence:** engine at Q = 2¹⁶ / 2¹⁸ / 2²⁰ (seed 1): trapped 51/55/45, dwell
  totals 801/807/794 ×10³, max dwell 105/110/102 ×10³, p50 γ 3.81/3.79/3.78, contacts
  280.1/279.6/279.2 k — flat, although contact-carry's per-contact ledger error differs
  ~12× between 2²⁰ and 2¹⁶ (3.7×10⁻² vs 0.46 of KE).
- **State rounding is innocent:** `grid` arm (twin + 1/Q state rounding every chronon,
  exact response) at Q = 2²⁰/2¹⁶: contacts 291.3/291.3 k vs float 291.6 k; trapped 63/56
  vs 59; dwell totals 956/955 vs 958 ×10³; max dwell 19.8/18.0 vs 21 ×10³. Rounding the
  state to the law's own grid reproduces the continuum statistics; it does not reproduce
  the engine's.
- **Ledgers exact throughout** (engine residuals finite, no growth blow-up; every engine
  state validated by the law's own `validate` path).

**Predictions** (`predictions.md`, written before the decisive run): control-pos held;
control-neg **missed** (same class, not ≥2×); decisive arm half-held (bulk p50 within
1.5× as predicted; trapped fraction and p90 under 2×; max dwell ≥2× held, 5.3–5.7×);
Q-scaling **missed and inverted** — I predicted coarser Q distorts more; measured
Q-flat, the run's most useful surprise.

**What would make it wrong.** The twin is my code, not shipped code: a structural
difference between my per-pair analytic response and `resolve_law`'s batch behaviour in
*glancing* many-body contacts (my micro checks are head-on only; impact-parameter sweeps
at γ ≥ 10 are the named missing probe), or a semantics slip in walls/consumed ordering
(pos control would have to be blind to it, which the 1–2% agreement makes unlikely but
not impossible). The scene is one geometry (channel 512×4, one heavy) at one contrast and
one β; three seeds only. A checker should rerun `micro` (glancing variants added) and one
pump seed before trusting the 5× dwell number.

**Cost of adopting / consequence.** Nothing to adopt in the engine: the finding **refutes
an adoption path** — "raise Q / re-scale the quantum" will not fix dense-order behaviour
classes (Q-flat), and "round the state to the grid" is exactly innocent. The lever, if the
gap matters at game scale, is the response layer's ensemble behaviour in chaotic gases
(candidates/carry at glancing high-γ contacts), and the instrument that must exist before
any fix is a frozen trapping-statistics rung on the shipped law (5cad's missing rung, now
with a shipped-scene protocol and a validated continuum twin to build it from).

**Fit with PRINCIPLES.** "Compute only surprises… chaos is normal it's just the necessary
interactions happening within a short time" (#3): the dense order is a normal case, so its
*classes* must be right, not just its ledgers. "Errors never compound" (#13) iscertified
by exact arithmetic — this run shows the certificate's blind side: statistics, not sums
(Julien: "we want determinism ≠ realistic trajectories", #20 — here determinism holds and
the statistics still drift). "A test that cannot fail is a control" (#10): every digest
the engine can produce passes while the classes move 15–45%.

**The lens.** Inversion asks where the engine is *guaranteed* to fail and whether we are
doing exactly that: the failure list's #1 (law mints false classes) had zero measurements
on shipped many-body code — now it has one, with the instrument's own failure modes
controlled on both sides. What the lens may have missed: cost-side inversions (the
frame, encounters) and the plane-scale expression of this gap (contact rates in the real
belt are far below this scene's; severity at game scale is unpriced).

## Reproduction

`regen.sh` (≤ 6 min): rebuilds the example and reruns micro, both controls, the decisive
arm (3 seeds, engine/float), the coarse-Q arms and the grid arms; writes raw JSON lines to
`out/`. One process at a time, < 100 MB each.
