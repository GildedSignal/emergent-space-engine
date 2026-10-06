Working...
Check complete. `lab/results/20261006-0437-components-2222/check.md` written; tree restored (patch applied → reproduced → reverted; only `check.md` added to the run folder).

**Grade: silver.**

**Reproduced (clean tree, `git apply work/patch.diff`, deterministic fields bit-identical, timings within 5%):**
- Scan: 3.4–4.0 µs/candidate, linear (49 ms at n = 12289, exponent 1.01); 34 µs at the plane's n = 10; 5 ms budget dies at ~1250 members. HANDOFF's "190 µs per item" is stale — the scan is 55× cheaper than the board thought.
- Certificates: 3.3–10 ms per check, 93× the scan at n = 10, break-even ~n = 3000, only 5× better at 12289; cone candidates saturate 886→904.
- Decomposition (my probe): U-window + cone = 243 ns; all cost is per-pair `sections`/`first_hit` re-paid per check — the skin attribution is right.

**Corrections (why not gold):**
1. Of the two "missed encounters", only one is real. Pair 3 is present-inside with **no interior minimum in ±8 windows** (co-orbital monotone drift — minimum in the far *future*, not the past as the dossier says). Pair 18 is **193× outside ρ**; its `contact=true` is a linear-over-step-window phantom of the scan itself (live at `universe.rs:939`), and the certificates were right to report nothing.
2. The discarded belt control was valid: partners 1–3 are inside ρ_true at t (4.9e3/9.0e3/1.3e4 < 1.6e4) — the scan drops inside-reach pairs whose quantized relative motion fails its strict `dw < 0`: a false-negative class of the shipped component.
3. Sound-rho control refutes the rival explanation that the bench's `rho_query` was too small — the miss is genuine window-semantics, and the kill of the "no rewiring" swap stands.

One experiment for gold: fold the geometry classification (present-inside / interior-minimum / linear-phantom / quantized-zero) into `seam.rs` and re-derive the seam contract from it — then the kill deletes the wrong doc-comment for verified reasons.
