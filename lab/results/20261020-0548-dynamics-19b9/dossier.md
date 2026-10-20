# Dossier — 20261020-0548-dynamics-19b9

**Claim.** The V1 contact law's energy carry (`Body.residual`) is a bounded attractor at
storm scale — through 288M contacts the per-body ledger stays at O(the payback quantum
2|k|) independent of contact exposure, the net debt stays ≤ 3.4×10⁻⁶ of kinetic energy,
the exact identity ΣE − ΣR = const holds to the unit, and the `i64` panic channel keeps
42 bits of headroom — so PRINCIPLE 13's contact-side mechanism is certified at the most
violent scene the engine flies, and no residual-bound gate is needed.

**Bottleneck.** c644's named leftover #1 (the contact carry ledger through the storm),
on the belt decision path: whether a contact-collisional belt compounds hidden rounding
debt (a gate the engine would lack) or holds (certification). Not a 10× cost mover: a
danger-elimination run — it deletes the "residual-bound gate" candidate from the fix
list and closes the panic-channel question with a measured margin.

**Evidence.** Harness `crates/lattice/examples/beltledger.rs` (e3b7/c644's genesis and
tide verbatim; new measurement only: per-chronon ledger tallies, per-stride |R|
quantiles, per-epoch per-body dumps, `--notide` identity mode; two read-only accessors
added to `Chronon`: `take_kept_events` (c644's, verbatim) and `carries`). Arms: B cold
seed 1, H = 98304 (2× c644's horizon, 288,352,399 contacts); C thermal seed 2, H = 49152
(88,881,906 contacts); E cold seed 1, H = 16384 `--notide` (2,504 contacts, no gravity);
D thermal seed 1, H = 8192 `--pass`. Regenerate: `bash regen.sh` (~9 min).

- **Digest cross-check (the accessors are inert):** C reproduces c644's C bit-for-bit —
  digest `0845a045c1b68a0908b72ec031336f1454dff357f944397ec5151c3053c066df`, 88,881,906
  contacts; D reproduces c644's D (`dec06d27…`, 456,370).
- **P1 envelope HELD:** maxAbsR(t) < 16·maxk(t)+32 at every stride sample of every arm;
  the binding ratio is maxAbsR/(2·maxk) = 1.366 (B) / 1.325 (C) — the ledger never
  leaves ~1.4× the payback quantum of the fastest body, and the ratio shows no trend
  (B's per-epoch values oscillate 0.63–3.53 from t = 8192 to 98304 while cumulative
  contacts grow 14×).
- **P2 no-walk HELD:** cross-sectional slope log(1+|R|) ~ log(1+ct) at the final epoch:
  0.159 (B, n = 273 live) / 0.028 (C, n = 302) — both far under the 0.25 bar (a walk
  gives 0.5). Exposure spans ct = 18 … 2.23×10⁶ per body; Spearman(|R|, ct) = 0.22/0.09,
  Spearman(|R|, own |k|) = 0.04/0.04. What sets a body's |R| is neither its contact
  count nor its speed: it is the recent pair geometry (the pair-level minimisation
  leaves each pair sum within the candidate spread, and partners churn).
- **P2b HELD:** |ΣR| < 1e-4·KE everywhere; max fraction 3.4×10⁻⁶ (B) / 1.9×10⁻⁶ (C);
  ΣR_final = 3,655,060 (B, cold) / −450,074 (C). Gross Σ|R| = 3.7×10⁷ / 2.9×10⁷: the
  ledger is 97% self-cancelling across bodies (per-body positions ~±10⁵, net ~10⁶).
- **P5 instrument HELD:** D (Pass): R ≡ 0, C ≡ 0 identically. E (no tide): ΣE_true − ΣR
  constant to the unit at every one of 16,384 chronons (E_true = Σ⌊2Q²γ⌋, computed
  exactly as the crate's `four_momentum_v1`; the naive 2Q²+k² form is wrong at belt
  speeds — the γ corrections are ~1.2×10⁷ per body at |k| = q/16 — and my first check
  used it and "failed"; unit-level isolation: `iso_ledger` agrees, 200k random batches).
- **P6 HELD:** max |residual| ever = 1,933,736 (42 bits of i64 headroom); max |momentum
  carry| = 6,601,368 ≈ 3.1 quanta of 2Q (40 bits). Since the law caps |k|² < Q², the
  envelope law caps |R| ≲ 2.8×10⁶ forever: the `expect("energy carry fits i64")` channel
  is unreachable while the envelope holds.
- **P4 (id-sink) REFUTED — honest miss:** Spearman(id, R) = 0.044/0.037 ≈ 0: the
  join-the-lower-id rule does not sort debt onto low ids. (My first analysis run had an
  index bug that read the clamp column as R and reported −0.23; corrected before any
  conclusion, both outputs preserved in git history of this folder.)
- **Byproduct (c644's leftover #3, half):** B's live count 308 (t = 49152) → 273
  (t = 98304): the core's evaporation tail continues past 49k at ~35 deaths per 49k ch
  (~2.5×10⁻⁶/ch per live body by epoch-average), while the contact rate holds ~4,700/ch.

**Predictions.** `predictions.md` was written before the flights (one 2048-ch format
smoke disclosed there). Verdicts: P1 held, P2 held (0.16/0.03 vs the 0.25 bar), P2b
held, P5 held both arms, P6 held, P4 refuted (directional prediction, wrong sign≈0).

**What would make it wrong.** The envelope law is measured, not proven: a scene with
higher |k| at contact time (near-c flybys, γ ≫ belt values) could widen the per-contact
spread and the ratio; the momentum-carry identity (Σp − ΣC, walls aside) was not
verified to the unit (only its magnitude measured); `Response::Stop` bodies void the
ledger identity (k zeroed, no residual entry) and were not exercised; the attractor is
verified on one law (RelativisticV1), two scenes, three seeds. Cost of adopting: zero —
this certifies the shipped mechanism; the only adoption is recording the envelope
constant (1.4×2·maxk) and the headroom margin in the belt's notes. Fit: PRINCIPLES 13
("basically we don't want errors that can compound that's the goal") — the carry is the
law's anti-compounding instrument, and it is measured not to compound through 288M
contacts; and 21 ("rough first, refine when a certificate could break") — the
certificate did not break, so no refinement is bought.

**The lens.** The attractor/installation framing found the Σ-Δ structure (pair-level
error diffusion with a restoring force) and predicted the right invariants (pair-sum
bounded by the candidate spread; exposure-independence). What it missed: the id-flow
prediction (P4) — the lens expected a sorting pressure where the diffusion has none;
and the sign convention of the ledger (E − R, not E + R) cost one instrument iteration
caught only by flying the no-tide control.
