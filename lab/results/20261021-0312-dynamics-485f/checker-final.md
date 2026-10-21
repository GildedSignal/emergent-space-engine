Working...
Check complete. Tree restored to as-found (`?? lab/results/` only), adversarial artifacts outside the repo in `/tmp/adv485f`.

## Verdict: `Grade: gold` — written to `lab/results/20261021-0312-dynamics-485f/check.md`

**Reproduction** — Clean tree, applied `work/patch.diff` myself; the runner's independent regen re-flew both arms (402 s + 128 s) with matching digests (`98fd7fe0…`/`bbbca241…`). Every dossier number traces to the regenerated TSVs: 293,013,197/78,952,779 contacts, dead 567/507, peak res_max 1,562,838 at t=15,872, per-body α=0.029 (r²=0.005), station ratio 1.130, crowd median 42 partners, top pair 0.02%. Verified in source that `take_kept_events` is digest-neutral and the measured object is the shipped `resolve` verbatim.

**Predictions** — Registered before the decisive arms; P1 refuted and reported as refuted, P2/P5/P6 held, P3/P4 split honestly. The instrument worked.

**Attack (outside the author's domain)** — Parameterized harness, three arms:
- seed 5: α=0.033 — same attractor;
- uniform **m=64**: α=−0.003, ceiling ×64 (5.9×10⁷, still 2^34 headroom) — the 2m|k| mechanism's mass scaling holds exactly;
- **4× central μ** (~2× speeds, 118 M contacts): α=−0.01, ceiling 4.1×10⁶, crowd median 217 partners.

**Corrections made to the author's page in place** (550 → 85 lines, current best 6 ≤ 15): the "frozen band {570k,708k,826k}" letter is contradicted by the TSVs — cold1's post-transient res_max is dominated by ~1.0M with excursions to 1.24M, constant only over the final 16k ch, and therm2's global max 1,090,915 is mid-run (t=42,496); now stated as heavy-tailed bounded oscillation. The PRINCIPLES-13 sentence is scoped equal-mass against contact-carry's contrast refutation. Also recorded: therm2's "±q/256" label is actually ±4 quanta, and the "113,678 at t=70k" provenance nit.

**Why gold** — components-4643 precedent: a certificate that kills a direction (carry overflow watch / retirement protocol; per-pair clump compilation) and prices what remains, adoptable in one step (narrow carry fields; per-crowd response unit). Named leftover flown, mechanism identified and confirmed quantitatively out-of-sample. The one open regime left: a mixed-mass storm between equal-mass (attractor) and 1000:1 contrast (walk).
