Grade: silver

**Abstract (for the integrator).** Two probes. (A, a protective kill) the view's per-frame
readout streams from two incommensurate *eccentric* orbits admit no recurrence of order ≤ 96:
one-step error plateaus at ~2–3×10⁻⁵ rad (e 0.3) and ~10⁻¹ (e 0.7), insensitive to order and
fit window — reproduced; single-orbit streams are exact at order = samples/orbit (5×10⁻¹⁴) —
reproduced bit for bit. The torus / cycle memo stands. (B) the frame budget's worst hitch has an
exact integer certificate W* = max window surplus = the worst backlog of *every* work-conserving
schedule (528 = 528, 620 = 620; plus 400 randomized traces, overload and crafted traces: zero
violations either direction), M = W* − C·D decides misses exactly, 26 ms per 10⁵ frames. Design
laws: `id % k` sharding costs 244× p99 (regenerated), a 1-frame handoff +1 p99 frame. Gain:
frozen bounds and a kill, not compute; adoption is one bench function — but on synthetic
arrivals, not the plane's trace.

**Reasons.**

1. **Reproduction.** Both scripts self-contained (numpy only; `work/patch.diff` is empty).
   Run clean in a fresh directory: outputs **bit-identical** to the author's JSONs (7.3 s and
   7.1 s wall, ~214 MB peak — inside every budget). All dossier numbers carried by the shipped
   code match: kmin 12/none, P2a exactness row, Q24 drift 0.119/1.67 units, Newton 3.0→1.0
   (e ≤ 0.3) and 2.1 (e 0.7), never 0; W*/M 528/512 and 620/604, p99 9 vs 24 (2.7×),
   misses 5.87%/6.56%, batched 10/+45%.
2. **Probe A attacks (my own).** Plateau re-measured at k ∈ {16, 64, 96} × fit {1024, 4096}:
   e 0.05 ~1.3–2.5×10⁻⁶, e 0.3 ~2.1–3.0×10⁻⁵, e 0.7 ~0.05–0.10 — the dossier's 5×10⁻⁶/5×10⁻⁵/
   1.6×10⁻¹ are the right orders from an unshipped eval discipline. 6-sinusoid control: 6.1×10⁻¹²
   at k = 12 (claim 2×10⁻¹⁰ ✓). Stronger light-cone coupling (c = 5): still no order ≤ 96 at
   e 0.3 — the kill is robust, not a weak-coupling artifact. **Scope confirmed, and correctly
   claimed:** a commensurate pair (P_o/P_e = 2) reaches 1e-6 at k = 12 (e 0.05) and k = 8
   (e 0.3), and two *circular* incommensurate orbits reach it at k = 12 — so the dossier's
   caveat is true as written, and the kill covers exactly the generic case (eccentric,
   incommensurate). The 3.0-iteration cold Newton matches HANDOFF's "Newton from the last
   frame's crossing" baseline, so the comparison is fair.
3. **Probe B attacks.** Crafted spike trace: W* = 92 = simulated backlog, 76 misses = M.
   Overload (util 1.125): identity survives divergence (50 000 = 50 000). 400 random traces,
   D ∈ {0, 1, 2, 5}: **zero** violations of the backlog identity, of soundness (M ≤ 0 ⇒ no
   miss) and of completeness (M > 0 ⇒ miss) — the certificate is exact, not merely sound.
   `id % 8` strawman regenerated: p99 2198 vs 9 (244.2×), 96.98 % missed (claim 244×, 97 % ✓).
   Certificates: 26 ms at 5×10⁴, 0.13 s at 10⁵ frames (B5 ✓). Multisets: single queue ≡ rotating
   shards **bit-exactly** on both α traces; steal exact at α 2.5, but at α 1.5 it differs on
   10 of 266 930 units — visible as the 6th-decimal miss_frac split in the author's own JSON.
4. **Predictions.** `predictions.md` (15 m before the scripts and outputs, 6 m/2 m) is a real
   pre-registration: mostly *failing* predictions (A1, A4, A5, B3's premise, B4's number),
   each reported as failed in the dossier. For a kill-probe that is the honest shape.
5. **Novelty.** No max-plus / Lindley / network-calculus / Prony / Berlekamp lineage anywhere in
   docs/HISTORY.md or the docs (the polymath scan's monoid messages and the hevc-proxy codec
   sensor are different ideas); the cycle memo (law.md) exists, so probe A's "sequence form of
   the cycle memo" is grounded, and its kill confirms rather than duplicates it.
6. **Goal fit.** Probe A aimed at HANDOFF's measured #2 (view gather 83 % of a light frame) and
   killed its own lens hypothesis instead — protective, residue marginal (3.0→1.0 iterations).
   Probe B gives plane.md's hitch service level a frozen, precomputable integer bound ("gates
   are frozen before the first run") and separates workload-forced hitches from scheduler
   waste. Neither moves compute 10×; both are simulations of structure, not measurements on
   the plane (admitted in the dossier).
7. **Why not gold — the record, not the physics.** Three quoted numbers cannot be regenerated
   by the shipped commands: the plateau values, the 6-sinusoid control, and the 244×/97 %
   strawman (I regenerated all three; they hold). "Identical lateness multisets" is stated for
   shards+stealing but is contradicted for steal at α 1.5 by the run's own JSON. Probe A
   accepts `--seed` but uses no randomness, so the pre-registered "reshuffled seeds" protocol
   is impossible as written. This is precisely the 5 October taste-log failure mode.

**The one experiment that would make it gold.** Anchor the certificate to the plane: dump the
real per-frame arrival trace (integer budget units) from `xtask universe --bench` on a scene
with a fleet battle, compute W* and M inside the bench, and show they separate workload-forced
hitches from scheduler waste on the plane's own trace (battle hand-outs are one budgeted item
per member, 2231928 — a real correlated-arrival test, exactly the model risk the dossier
names). Ship the three missing numbers in the scripts at the same time. Exact, cheap and
load-bearing on the plane's own measurement, it deletes the guesswork behind plane.md's hitch
metrics and is adoptable in one step.

**What the author missed.**

- The record items above (unshipped numbers, the steal overstatement, the dead `--seed`).
- The commensurate/circular scope was *claimed* in "what would make it wrong" but never
  measured by the author; it holds (my §2), and near-commensurability — the resonant pairs of
  B17 — interpolates between the two measured regimes and was not probed at any detuning.
- Probe B's own named risk (correlated single-cause arrivals vs iid bursts) is testable today
  from the plane's battle budget items and was left as a caveat.
- The catalogue's items 3–7 (Zobrist digests for B8, Landen, Sturm, α-stable promotion,
  Paterson–Stockmeyer) are unprobed text; Zobrist-for-B8 is one cheap script and its
  collision audit would have been a second probe in the same window.
- The abstract's "plateau of 5×10⁻⁵ rad at e ≥ 0.3" quietly quotes the e = 0.3 value; at
  e 0.7 the plateau is ~10⁻¹ rad. Same direction, but the headline understates the failure
  it reports.
