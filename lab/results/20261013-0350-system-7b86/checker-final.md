Working...
Check complete. Summary of what I did and found:

**Grade: silver** — written to `lab/results/20261013-0350-system-7b86/check.md`.

**Reproduction**: applied `work/patch.diff` myself, ran `quad_slot 8` (~15 s). Every column matches `probe-out.txt`; L15 wobbles exactly as disclosed (no-stor 4→8 from the wall cut). One defect: the dossier's bold L12 figures (e_p99 7.2×10⁻⁶, ev_p99 9.1×10⁻¹²) match **neither the author's own probe-out nor either rerun** (all give 7.92×10⁻⁶ / 1.01×10⁻¹¹), and `regen.sh`'s "expected ≤ 7.2e-6" line contradicts its own output — one row of the taste log's non-regenerable-numbers failure mode.

**Premises verified in shipped code** at `cb16ccb`: `partial`'s fresh `force::field` per read (observe.rs:145), `credit` from kick history, `thrust::owed` exist; all-`Scalar` field arithmetic consistent with the tide-flooring claim; the probe's unit chains and τ-domain are correct.

**Predictions**: pre-registered (mtimes ordered; two failures reported honestly — strong evidence of genuine pre-registration). #1 and #6 held; #3/#4 failed and reported; #5 voided with the wrong-payload bug self-diagnosed.

**Attacks** (my `quad_slot_adv`, since deleted): 16 s decade, 400 members, brake-L15, turn-right, stirred — all hold, e_max ≤ 9.8×10⁻⁶. Two controls mattered: **drop-entirely (e0) ≡ swap error** on these scenes, and a **stale-kick control passes identically** — so the stored-kick *fidelity* half is vacuous in this regime; only the deletion claim earns its keep.

**Page**: corrected in place (7.2→7.9 with provenance, checker findings folded in, untested-domains narrowed). Tree restored to as-found; no commits.

**Why not gold**: the deletion's gain is never measured (inherited from `51bf`; fresh-eval serves ~43% of reads → plausibly ~2×, not 10×), plus the record defect. The one experiment: land the ~35-line deletion (or the simpler tube-alone form e0 validates) and measure the gather's frame share.
