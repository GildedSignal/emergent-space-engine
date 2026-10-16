# Dossier — 20261016-1740-quant-1250 (quant lens)

**Claim.** The scan's answer half carries an angular certificate on the tube's own knot table
(`ES_SCAN_CERT`, `work/patch.diff`): it kills 66–80% of candidates (89–91% of bound cycles) at
0.2–0.46 µs each with **bit-identical outcomes on every flight run** (10 ladder flights plus 12
scripted flights × 4 schedules, certificate-on finder ≡ certificate-off ≡ brute reference),
cutting the per-answer bill 2.2–2.8× and the burn backlog 13–26× at N=300 and 10⁴ — but the
latch's freeze at the plane's own N=1000 burn survives (held 580→491), because the drain gates
on the **worst** answer (scan_ns running max), which the unkillable Passage readouts still set.

**Bottleneck.** scan-queue open direction 1 (cdf0's priced cure: "an angular certificate on the
key … at ~10–20 ns a candidate, no readout"; success "S < b/2"). The certificate exists now and
is measured; it deletes 66–80% of the answer's readouts, but it is a **2–3× lever on the latch,
not the ~100× one hoped**: the phase arc costs 20–45× cdf0's pricing, and Passages (planets,
moons, fleet members, ships in transit) carry no bound cycle to certify.

| N flight | answers | mean µs off→on | reads/hit off→on | kills/cands | cert ns/cand | digest |
|---|---|---|---|---|---|---|
| 300 coast | 193 | 764→333 | 266→70.5 | 25073/34091 (74%) | 296 | identical |
| 300 burn | 1348 | 508→212 | 48.6→16.8 | 68249/104194 (65%) | 213 | identical |
| 1000 coast | 193 | 1871→659 | 481→94.6 | 49511/61622 (80%) | 460 | identical |
| 1000 burn | 1342 | 776→345 | 73→17.7 | 118396/156190 (76%) | 386 | identical |
| 10⁴ coast | 193 | 764→314 | 267→66.6 | 25649/34172 (75%) | 293 | identical |
| 10⁴ burn | 1346 | 362→187 | 46.2→14.0 | 69093/99113 (70%) | 197 | identical |
| 10⁵ coast | 193 | 752→315 | 267→66.6 | 25649/34172 (75%) | 292 | identical |

(The two flights are different regimes, not a label slip: **coast** is the few-answer flight —
193 answers, the memo reuses everything, and at the plane's N its captures fall back 95%
(183/193, cdf0's census confirmed) so each answer reads the whole doll, 319 reads an answer at
N=1000; **burn** is the many-answer flight — 1,342–1,348 answers, the thrust rebinds mint new
scans, fallback 20–26% of captures — and the one that piles the backlog.)
- Held backlog under burn (`held_max`): N=300 **508→19** (26×), 10⁴ **199→15** (13×), but
  N=1000 **580→491**: there the burn's captures still fall back (414/2123) and the worst early
  answer — the whole-doll candidate list, 61% of whose surviving reads are Passages the
  certificate cannot touch (23,233 of 37,794 non-cycle reads on the burn arm at N=1000) — sets
  `scan_ns`'s high-water above room/2, and the drain freezes for good (scan_ns decays only
  1/64 a served answer, and a frozen drain serves none). The mean is under b/2 at every rung;
  the latch's own gate (`universe.rs:1190`, `2·max(scan_ns, 0.75 ms)`) is a running **max**.
  Coast answers (the heaviest, 481 reads/hit at N=1000) fall 1871→659 µs mean; the coast
  backlog was already 1 (the answers fit) and stays 1.
- Frame p99 under burn also improves: 10.85→9.39 ms (N=300), 10.82→9.18 (10⁴), 11.13→10.98
  (1000). Refusals 0 everywhere; `frames over 12 ms`: 1000 burn 2→1.
- **Adversarial rtf 1000 burn (the horizon, and the digest's own domain):** at the 12 ms
  budget both arms are starved (worst lag 16.7 s, 515 vs 346 frames behind) and reach
  different presented ticks — the digests differ (21e03f… vs b1a7ef…), the off-arm frozen at
  the SCAN_BACKLOG cap (held 2048, 242 answers served) while the on-arm served 1,615 (held
  973): a **schedule artifact, not a certificate failure**. Control: the same flight on a
  200 ms budget (0 frames behind, 0 held, identical events/frame in both arms) gives
  identical digests (c7183b59…). The digest is cut-invariant, not starvation-invariant;
  starved wall-paced flights compare different universes (the r2/r3 criterion lesson, met
  here by the control on both sides).
- `frame_digest -- 3`: all 12 scripted flights × 4 schedules agree in every arm, and the
  certificate-on finder's digests equal the **brute** reference (every body read, no filter):
  the certificate never dropped an encounter the exact predicate would have kept, on 48
  schedule-digests plus 10 ladder digests. `cargo test --release -p emergent-space -p
  emergent-universe` with the patch: 32 suites ok, 0 failed (lib, bins, doc-tests).

**The certificate** (`crates/universe/src/encounter.rs`, `angle_arc`/`cannot_meet`; the knot
table in `crates/space/src/orbit.rs`): a bound tube's polar angle at the scan's tick lies in
the knot panel its rem-time falls in (ψ monotone in time, mirror on the inbound leg), widened
by the residual/turn/rounding slack `eps_off`, the unknown within-cycle advance `e_adv =
2|advance| + 4e-3`, and 1e-9 float slack; the pair can meet within `near` only if the arc's
distance from the player's exact readout angle, minus the most angle the two can sweep over h
(v/r at each's smallest reachable radius), still fits the chord bound `2·asin(near/2r_min)`.
Every widening is against the cut, the radial window's own rule (radial.rs:10-11): a float only
ever drops a pair that cannot meet, so outcomes cannot depend on it. Non-Cycle tubes
(Passage/Plunge, the unbounded set) and symbolic circles are always read.

**Predictions** (`predictions.md`, written before the decisive runs): bit-identity **held**
(10/10 ladder flights, 48/48 schedule-digests, brute equality); the "~10× answer cut" **held**
(2.2–2.8×) but my "85–95% kills" was right only among cycles (89–91%), not overall (66–80%
— Passages); reads/hit landed 14–95 against my 5–40 (burn rungs above it); "latch reopens at
the plane's N" **half-held**: means reopen it, the max-gate at N=1000 burn does not; held-out
N=300/10⁴/10⁵ behaved as predicted (kill ≥ 65%, digests identical). cdf0's 10–20 ns/candidate
pricing is off by 20–45×: the panel scan plus `range_of`/`period`/`advance` Scalar getters cost
~0.2–0.46 µs.

**What would make it wrong.** A widening gap in the arc: the advance convention (per half-cycle
vs per cycle — absorbed by the 2× slack in `e_adv`), the weak branch's zeroed q (absorbed by
the 4e-3), the inbound mirror, or the offset/turn slack. All flights run agree bit for bit,
including the brute reference, but a stronger-field doll than the plane's (q ≫ 2⁻¹⁸, large
per-cycle advance) is untested; there `e_adv` grows with the advance and the certificate
weakens toward no-op (safe, not tight). Adoption cost: the patch is additive (one readout-side
float table in `Orbit`, one pure filter in `Scan::compute`); the capture half, the fallback rule
and the answer's Passage reads are untouched — the remaining latch work.

**Fit with PRINCIPLES.** "Compute only surprises" (P3): the certificate reads the phase the
tube already owns (the knot table is compiled once per orbit, P6 "store the generator"); "a
cheap exact bound in front of it" was already the file's own note (encounter.rs:58-60); "no
outcome depends on a float" (radial.rs:11) — same rule, carried to the angle. What it does not
yet do: delete the capture fallback (P1: the N-relative `bodies/4 + 64` rule still walks every
body at the plane's N) — that, plus a max-based scan_ns estimate, is the named next experiment.

**The lens** (quant): priced the cure before building, froze the falsifiable claim (digest
identity) first, measured both arms with the control embedded in one binary. What the lens may
have missed: tail physics — I reported means per answer, but the latch is decided by the running
max; a market lens underweights that a queue's service rule is only as open as its worst
customer. The 10–20 ns pricing I inherited from the page was a quote, not a measurement; the
real cost is Scalar-getter-bound, an integer-arithmetic question, not a cache-line one.
