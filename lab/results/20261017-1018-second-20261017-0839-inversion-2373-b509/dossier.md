# Dossier — 20261017-1018-second-20261017-0839-inversion-2373-b509 (second author)

## Claim

The checker's named experiment is done: the conjunction calendar — already shipped as
`tier::arm_pair` (`dioph.rs` first-hit, returning `(armed, due)` with `due` = slack) — is
measured on fleet populations, and it is sound and deletes the window sweep (1.01–1.16 µs
per pair against the exact check's 57.9 µs at interval horizon and 416.5 µs at the
8-interval rebuild horizon), moving the keys-fleet ceiling **F* from ~100 (sweep) to
6,463 (L = 100; 3,232 at L = 25; F = 10³ fits the 4-core budget at 0.95–3.8 cores)** — but
the fleet term does **not** drop under 4 cores at F = 10⁴–10⁵ at φ = 1, because what
remains is the population's own conjunction flow: trains (da = 1e-4) fire 6.8–9.4 M
close-conjunction checks per interval per F = 10⁴ fleet (50,731 cores; F* ≈ 89), the
belt-quantum kick creates 17 (keys) / 1,924 (train) undelayable firings per kick (~2,500
cores at belt kick rates, any F), and the real-event rate itself (γ = 1.97 in F, 910
events/body/interval at F = 6400 = 455× the belt's 2) caps any certificate. The missing
10⁹ ledger row closes with numbers on both sides: a certificate term (calendar, slack,
standing contacts: F* = 3.2–6.5 k) and a population term (firings ∝ φ·F²·da, kick-created
events ∝ kick rate) that no representation deletes — they are the surprises.

## Bottleneck

Board item 2 (encounter work at 10⁹), continuing 2373 (silver). The checker's "one
experiment to gold": "measure the run's own proposed fix … composed at 10⁹ — if the fleet
term drops under the 4-core budget at F = 10³–10⁵, that is the 10× move and closes the
missing ledger row with a number". Answer: it drops under at 10³ (1,300–5,400× below the
sweep at sound horizons), and the row closes anyway — with the firing floor, not a passing
grade, at 10⁴–10⁵.

## Evidence

Instrument: `crates/encounters/examples/fleetcal.rs` (+ fleetk from 2373, both in
`work/calpatch.diff`, print-only, zero shipped lines). Decisive seed 20261017 (2373's
own), held-out 777; pilots seed 7 disclosed. Reproduce: `bash regen.sh` (~10 min).
`work/fleetcal-20261017.jsonl`, `work/composed.txt`.

**Soundness (the gates):** calendar events ≡ `group_events` events — dropped 0, added 0 —
on keys and train fleets, both seeds (12,300/12,925 events at 20261017). Negative
controls drop: safety 0.9 → 1,289; safety 0.5 → 6,492; halved reach → 59. The instrument
can fail; K1/K2 did not fire.

**The arm test** (`carm`, keys F = 5,000, horizon one interval 28,141.5 gs): 1.02 µs/pair
(2.0 Dioph steps/pair) vs the exact check 58.8 µs/pair at that horizon and 416.5 µs at
8 intervals — the sweep price 2373 composed (3.24 µs) was measured at a 1-orbit horizon no
sound 8-interval rebuild can use: their 36/383/4,502 cores understated the shipped sweep
(5,143/54,777/644,177 at interval horizon; 4,620/49,212/578,731 every-8) by 129–143×.

**Keys fleets (capability = birth constant, standing contact):** armed pairs 54 / 4,775 /
477,050 at F = 10³/10⁴/10⁵ — and 4,708 at σ_e = 1e-3 vs 4,775 at 1e-2 (ρ-driven, not
σ_e-driven; K3 held) — while the sweep window shrinks 10× at 1e-3. One-period capability:
27–51 µs/armed pair. A perpetual pair re-evaluated at interval horizon costs **31.6 ms**
(102,757 exact evals — the shipped exact machinery walks every orbit of horizon per
standing pair): standing contacts must be stored state. Calendar birth (window arm pass +
one-period capability) composed at φ = 1: 0.95/10.1/118 cores (L = 100), 3.80 at F = 10³
L = 25 → **F* = 6,463 (L = 100), 3,232 (L = 25)** against the sweep's ~100.

**Trains (da = 1e-4):** window 36.2 M pairs at F = 10⁴ (reach 2.27 at interval horizon);
9.41 M fire in interval 0, 6.80 M at interval 10 (direct re-arm; the pre-registered K4
fallback — the first-due histogram reading died: in-window passages come in bursts,
consecutive dues one period apart). Each firing 21–34 µs → 50,731 cores at F = 10⁴
(**F* ≈ 89**, ∝ 1/√da); da = 1e-3 refuses (reach 21.3 ≥ π — 2373's H* law) and inherits
the tree ruin. Birth: 0.37–1.47 s/fleet (L-amortized 131–524 cores at 10⁵ fleets).

**Kicks (belt quantum 2⁻²³):** the median pair's due moves < 10⁻³ intervals (slack is
real; row re-arm deferrable — ddue_p90 = 0.0009 iv keys) but the kick **creates** 16.8
(keys) / 1,924 (train) newly-armed pairs per kick — undelayable real events; with slack
ignored the row re-arm is 1.09 ms (keys) / 16.9 ms (train) per kick (worst case 10,229 /
407,058 cores at belt kick rates).

**The event floor:** real contacts grow γ = 1.97 in F (1,600→6,400); 910
events/body/interval at F = 6400 — 455× the belt's own 2; at the stream's ~50 µs/event
that is ~1.6×10⁵ cores at φ = 1: the population, not the certificate.

## Predictions

`predictions.md` written before the decisive run, fitted on pilot seed 7 only. Of 16
bands, 14 hit (P1–P5, P8–P16). Two misses, both disclosed: P7 cap_us 27.5 µs vs [4, 15]
(setup dominates a one-period check — the composition uses the measured 27.5); P10's
steady-rate model died (K4 fired, pre-registered): replaced by direct re-arm at interval
10 before composing. No kill criterion fired except K4's pre-declared fallback.

## What would make it wrong

- **Standing-contact semantics is a design step, not shipped behaviour**: the composed
  keys F* assumes a perpetual pair is evaluated once per lifetime (one-period capability)
  and woken only by kicks; under shipped per-interval re-check semantics a keys fleet pays
  armed×31.6 ms per interval (2.4×10⁸ cores at F = 10⁴) — the 31.6 ms number is measured,
  the choice is the integrator's.
- **L (fleet lifetime) and kick rates are policy**: F* ∝ √L; the kick terms scale with
  φ·(kick rate); quiet fleets (flown, not evolved) delete the kick row.
- **x86 costs**: per-pair µs are this box (orders of magnitude); the ratios (57×, 370×)
  and the F² scalings are unit-free. The M1 re-measures.
- **Subsampling**: F = 10⁵ arms 2,000 rows (6.3 M of 313 M pairs) and scales linearly;
  F ≤ 10⁴ is full. Disclosed in the JSONL (`sampled_pairs`).
- **Composition constants** (interval 28,141.5 gs, rtf 100, split 8, 2
  events/body/interval, 50 µs/event) are the wiki's, same as 2373's.

## Cost of adopting / fit with PRINCIPLES

Nothing to build to close the row: the calendar is already shipped (`tier::arm_pair` on
main); what is missing is wiring (standing-contact state, due-queue as the only waker,
slack-deferred re-arm) — one design step with every constant now measured. The ledger
(kick-cadence 4e2d) regains the encounter row as two terms: certificate (calendar) F* =
3.2–6.5 k at φ = 1, and population (firings, kick-created events) — the latter is a fleet
contract the integrator must state. PRINCIPLES #3 "compute only surprises": the sweep paid
for empty windows every rebuild; the calendar pays exactly the firings — and where the
firings themselves overran the budget (trains at 10⁴), that is the surprise rate, not
waste. #19 "a fix signals the wrong representation": the window was the drowning car for
fleets; the calendar is the boat — but no boat outruns a storm the population itself is
(PRINCIPLES #35: the simplest form that does the most, given the dynamics).

## The lens (second author)

The checker's named experiment was the whole job, and it cut both ways: the fix works
better than 2373 hoped (57× per pair, F* 65× up) and worse than gold wanted (the floor
moves from representation to population — no 10⁵ fleets at φ = 1). What this lens may
have missed: the M1's true per-pair costs; whether the integrator's plane wires
`arm_pair`'s due as slack today (main.rs's kick experiment suggests partially); and the
refused-train tier (da ≥ 4e-4) — untouched, still the tree ruin 2373 measured. Novelty
debts from 2373 are paid here: coorbital-cert's runs (74a1/4ec3/5ffb/c5ab/a110/9a33,
b292/7532) are cited on the page and in the dossier's lineage; rank-0 is reported as a
control; the pred/pairs range and both-sided row are in the record.
