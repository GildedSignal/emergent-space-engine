Working...
Check complete. `check2.md` written; tree restored to pristine (`lab/results/` untracked only, as found); `check.md` never read.

**Grade: gold.**

**What I did:**
- **Reproduced** from the dossier's commands on a clean tree with `work/patch.diff` applied: walks 1123→42 (seed 7 rtf 100), 4224→42 (rtf 1000), floors 42/147/438, deadline error med 2.06e3 / max 2.07e6 ticks (0.36% of the 5.72e8 light distance), digests and views asserted equal in all 8 configurations; engine mean −27.7 µs matching the 26.7 µs walk-tax arithmetic, median flat at rtf 100 and −87 µs at rtf 1000. Full crate suite: 56/56 (57 with my probe).
- **Predictions** verified as pre-dating the decisive run (file-time order). 5/7 held; the two falsifications — the median drop and the deadline error's relative form — are reported honestly, and the first *is* the deliverable: the parent silver's "46% of the median engine frame" was a mean-per-frame tax read against a median frame.
- **Attacks (all held):** a 1200-frame flight with four intermediate settle cuts (digests/views equal at every cut, walks 2591→42, max error flat, not compounding); held-out seed 11 (equal, 1180→45); floor extremes 1e2/1e10 (530/42 walks — the re-anchor path demonstrably fires); default-path bit identity against the unpatched tree on seed 11 (digest `6f1e0866…` identical both sides); confirmed the carry is not vacuous.
- **Novelty:** parent run designed the carry; nothing in HISTORY builds/measures it or corrects the unit. This is the named experiment, executed.

Gold because: independently reproduced on held-out and adversarial cases, the experiment is done rather than one away, adoption is one owner-step (move `pos`/`pos_v`/`pos_t` out of the lab flag), and it deletes a component (26–100× on the scheduler's per-event readout walk) with zero canonical cost while correcting a wrong premise on the record. Flagged in the check: the dossier's absolute µs come from a repeat not in `run-log.txt` (drops agree); β→1 with events remains the stated gap; the 42 first-event anchors and the gather's own readout cost are the named next deletions.
