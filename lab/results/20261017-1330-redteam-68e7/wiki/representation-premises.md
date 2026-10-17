topic: representation-premises
status: open
closed-by:
valid-while:
updated: 20261017-1330-redteam-68e7

# The premises of docs/representation.md: a census against the record

## Current best
**The design doc teaches three dead letters and one unmeasured cost, and its perturbation
premise is refuted ~700× by shipped code, deterministically: the kick resolver costs a
median 34.8 µs (p99 53–63 over three runs) for plane bodies and 203.3–203.7 µs (p99
399–408) for handed-out members against the doc's "~50 ns each" (L114), and the memo the
cheap path needs hits 0.0% exactly (2262 rebinds, 2262 distinct keys) while the only
repeating key (the quantized 12+12-bit memo, 98.0% here) is the one law.md refuses (it
re-rounds every kick, a random walk) (20261016-1207-redteam-12db, `xtask universe
--kick-bench`, runs digest-identical, shared x86 — orders of magnitude; the M1 record:
43–52.8 µs c01c/0c44, 75–160 µs on the board, and the same refutation at gold grade:
**75.6 µs vs a 42–56 ns floor, ~1,800×, exact memo 0%** — 20261011-1729-components-b063,
the closest prior, measured six days before this census; leaver medians are
pace-dependent, 162–365 µs across the checker's arms — seeds 7/42, rtf 100–3000: 14,219
rebinds, zero exact reuse, made 34.6–35.4 µs, refused 0).** The premise is squeezed from
both sides: exact keys never repeat, the repeating key is not the law — so "a kick
updates the cycle by a multiply-add" (L67) has no shipped fast path and cannot get one
from memoization ("derivative prediction never substitutes for authoritative rebinding",
crates/space/ENVELOPE.md; the jet retired by three golds, law.md L36).

The census, ranked by player visibility (the rest of this page's standing record):

1. **Kicks/derivatives (L67, L114): REFUTED** (above; no rung exists for per-kick cost —
   B9/B10 gate counts and exponents, the §7 ladder has no kick-cost falsifier).
2. **View at the past light cone (L56-59): letter dead, physics holes open — NOW GUARDED
   IN COST AND PRESENCE by r6, created and executed (20261017-1018-redteam-13c6):
   PASS for the shipped memo-carrying gather (rows 38400/38400, median 2.0
   readouts/emitter, p99 2.92 on stream content at β 0.5–0.9999, observers β 0–0.9,
   60 Hz rtf 100); the no-memo cold path KILLED (median 3.66, p99 6.0, 12/38400
   emitters silently dropped — checker's correction: the drops are root_state read
   failures at ticks the from-the-present walk probes (emitters 32/33 at frames
   118–119; an independent bisection fails the same rows; warm resolves them), not
   64-iteration exhaustion on racing crossings);
   "any cache, however stale or foreign" KILLED as a cost claim (poisoned caches:
   same rows, p99 5.13); the amnesiac-memo negative fails as required. The historical
   1.5 clamp (4570) does not separate — at 60 Hz × rtf 100 a 0.999c closing stream
   races through its approach inside one frame (dt_e/dT = 10³): physics kills that
   negative. Checker's correction:
   r6's named hole closed by the checker at the frozen scale itself: an independent
   bisection oracle agrees with warm's ticks on 23,170/23,170 post-light rows
   (bracket violations 0.07% at eps 1e-3; at ~10⁶ root units 35,578/35,578, 0.13%)
   — the author's "40% of identically-correct rows fail from ±1–2 ticks of f64
   noise" was the pre-light tick-0 fallback fraction (15,230/38,400 = 39.7%), a
   semantics bug in the withdrawn oracle, not a noise floor: tick exactness is
   freezable at game scale now. Checker's domain facts: at rtf 10 nothing
   separates (cold passes every bar; the amnesiac negative passes → VOID);
   at rtf 1000 warm itself drops 20.9% of rows; on a 360-frame window at the same
   cadence warm fails its own presence bar (0.986, drops from frame 178); at
   β 0.6 cold/amnesiac still fail (separation is not confined to β ≳ 0.9); warm
   holds at β 0.99999 and N=512. Cold-seed weakness prior: 0fe0 (12 Oct) already
   had "cold seeds leave the bracket at β ≥ 0.9".**
   100% of azimuths at r_o 100–3.2 M, 20261011-1234-redteam-6eae); no time-transfer law
   (flat light-time off 2–176° within ~50 M, 20261011-0924-redteam-5977, gold);
   deflection key broken for rotating dolls (20261010-2052-redteam-8be2, gold).
3. **Binet cells "the primary in-cell solution" (L32): replaced 30 September by the Darwin
   compilation** (law.md L20: the band map's tangents carry a first-order slope error in
   every turning cell); research rehabilitation partial with four broken instrument
   channels (→ binet-cells).
4. **Two-body doll 1PN, ν only in the energy map (L37): SURVIVES** (r3 v3: precession
   1024/1024, periods 632/632, assists 64/64; B11) — licensed domain now measured:
   p̄ ≳ 65M at ν ≤ 0.25 (→ handoff, 97b0).
5. **Dense ≡ sparse (L70): SURVIVES in the lab** (tie rule 20261005-0543-redteam-6254,
   batch rule, locality licence, B8) — unguarded in the field (→ replay-gate); **NOW
   GUARDED BY AN EXECUTED RUNG ON LINUX: r5 created, frozen and PASSES
   (20261017-1330-redteam-68e7) — the dense order is not only Metal: its CPU arm
   (`Chronon`) is portable, the shipped `engine/tests/identity.rs` suite runs 9/9 on
   this Linux box (435.76 s, debug), and the r5 rung (frozen at
   `lab/results/20261017-1330-redteam-68e7/r5-dense-order.md`) holds 20/20 identical
   Outcomes (10 scenes × threads 1, 4; the frozen s0–s7 ladder plus two held-out
   draws: 2500 and 3000 bodies; 116,874 contacts, kicks and live carries in every
   scene), the both-shifted positive control agrees 10/10, and the one-order-late
   negative breaks 10/10. Only the GPU arm (`MetalChronon`, macOS-gated) stays with
   an M1-side run. Bonus, orders of magnitude only (shared box, release): the sparse
   event core beats lockstep 0.27 s vs 7.54 s at 2500 bodies and 0.84 s vs 10.80 s at
   3000, equal only on the epoch-1 storm scene.**
   Checker's domain facts (20261017-1330 check): identity holds beyond the rung's frozen
   domain — 4000 bodies (27,957 contacts, epochs 513), horizon 8192 (epochs 1025), a
   q 256 / div 4 / k 9 near-storm (epochs 2049, 7085 contacts), and cross-thread pairing
   the rung never gated (lockstep t1 ≡ sparse t4 and t4 ≡ t1, lockstep t1 ≡ sparse t8 at
   all three scenes); the epoch shift changes each order's outcome, so the negative is a
   law change, not a no-op. The checker's full regen reproduced metrics byte-identically
   (identity 1.0/1.0, late 0.0, contacts 116,874; suite 9/9 at 463 s debug).
6. **Undisturbed ≈ 0 (L113): SURVIVES by rate, not by cost** (a4ed gold: belts pass 10⁹ at
   10× real time; but fire rate 1.000, one rebind per doll interval, 20261015-0724-system-3294).

## Refuted

- **"A kick updates the cycle by a multiply-add" as a cost claim** (representation.md L67 +
  L114): three golds killed the jet (20261006-1249-redteam-4978,
  20261008-1757-second-…-0ccd-b33f, 20261012-1227-second-…-4808-d617, via law.md L36), and
  **the same refutation was already measured at gold grade: 75.6 µs vs a 42–56 ns floor,
  ~1,800×, exact memo 0% (20261011-1729-components-b063)**; the census run regenerates it on
  shipped code (34.8 µs median, exact memo 0.0%) — the doc still teaches it.
- **The Hashlife memo premise as an operating fast path** ("identical invariants share one
  memoized cycle"): exact_hit_rate 0.0 at 2262 rebinds, digest-stable (the census run;
  checker's held-out arms seeds 7/42, rtf 100–3000: 14,219 rebinds, zero reuse), after 0/203,017
  (20261010-1544-system-97ce) and 0/3,225 (20261013-2005-quant-7055); the quantized
  alternative is a refused law change (law.md L36; taste log 5 Oct).
- **"Each visible tube crosses the observer's past light cone once"** (6eae, silver):
  2–4 images near masses.
- **The cold no-memo gather as a row-complete fallback** ("every crossing found from
  scratch", view.rs): 12/38400 emitters dropped at β 0.999–0.9999 Toward, deterministic —
  checker: root_state read failures at ticks the from-the-present walk probes (an independent
  bisection fails the same rows; warm resolves them), not budget exhaustion; killed by r6
  (20261017-1018-redteam-13c6).
- **"Any cache, however stale or foreign" as a cost claim** (view.rs doc, representation.md
  §2 "shortcuts… add speed, never error"): true for the view's rows, false for its cost —
  stale/foreign caches pay p99 5.13 vs the kept cache's 2.92 (20261017-1018-redteam-13c6).
- **"r5 remains uncreated and cannot be created in this lab … `lattice-metal`'s dense order
  is `#[cfg(target_os = "macos")]` and compiles to a stub on Linux — an M1-side run owns
  it"** (13c6's blocker, this page before this run): a category error — the dense order is
  "CPU, or Metal on the GPU" (law.md L50), and the CPU arm (`Chronon`) is portable; the
  shipped identity suite runs 9/9 on Linux and the created r5 rung PASSES 20/20 with its
  negative breaking 10/10 (20261017-1330-redteam-68e7). What is Mac-only is the GPU arm.

## Open directions
1. **The integrator's one-pass amendment of representation.md** (no code): strike L67/L114
   for the recorded 43–160 µs and rebind-per-kick; relabel Binet cells as research;
   annotate "crosses once" (the "mark r5 uncreatable off-Mac" clause is dead — see
   Refuted). Until then every new reader is
   seeded with refuted premises (principles 10 and 19, applied to the document).
2. **Commit r6** (`lab/results/20261017-1018-redteam-13c6/r6-view.md`, frozen hash
   recorded, checker silver): the view's cost and presence are now guardable mechanically
   at rtf 100; the next rung is exactness, and the checker's bisection oracle already
   certifies warm's ticks 23,170/23,170 at the frozen scale — no smaller scene needed —
   plus bars that the negative fails at every cadence and a window past frame 178.
3. **Adopt r5 into `lab/rungs/`** (`lab/results/20261017-1330-redteam-68e7/r5-dense-order.md`,
   frozen before execution, PASS): the CPU arm is done and guardable on any box; what
   remains M1-side is only its GPU extension (`MetalChronon` configs and
   `metal_identity.rs`'s scenes, same criteria).
4. The EOB strong-field flank: closed by 97b0's oracle (→ handoff); the merger scene's
   licence below p̄ ≈ 12M still wants an NR-calibrated EOB.

## Contradictions

None. The doc's provisional status ("DRAFT … supersedes nothing until the falsifiers in §7
have run") is kept beside the census: the letter is refuted, the status line was honest
about it; both stand.

## Runs
- 20261016-1207-redteam-12db (silver): premise census; kick cost 34.8 µs vs the doc's
- 20261017-1018-redteam-13c6 (silver): r6 created, frozen and executed — PASS for the
- 20261017-1330-redteam-68e7 (awaiting grade): r5 created and PASSES on Linux — dense≡sparse 20/20, the "uncreatable here" blocker refuted; GPU arm stays M1-side
