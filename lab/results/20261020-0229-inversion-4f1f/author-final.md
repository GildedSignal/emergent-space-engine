Run: 202610All deliverables are in place (dossier, pre-registered predictions, regen.sh, the full folded wiki page, the frozen patch and 45 arm logs; spinners dead, no commits).

**Claim:** the 1d47/4063 digest dispute is adjudicated and both sides were mis-attributed — the canonical-cut digest's schedule-independence is broken by the player decision's anchoring, not by the burst-cure gate: with decisions canonically anchored (`schedule`) OFF = ON = one digest on a loaded box (16 same-tick runs, 0 gate flips), while with `input(now)` — the shipped play path (session.rs:119) — the shipped engine itself (no gate, stale = 0) produced six distinct canonical states in six loaded runs, one per delivered decision tick, and `schedule(t)` reproduces `input`'s digest exactly at the same tick, so the tick is the whole channel and the fix is one line of anchoring.
come),
predictions.md (pre-registered; P3's failure is the finding), regen.sh (~11 min; reproduces the
law — canon stability, frame multistability with per-run decision ticks — not the schedule-born
digest multiset), wiki/nladder.md (the page with the conflict resolved and the canonical-input
seam handed back), work/patch.diff (4063's instrument + ES_DECIDE/ES_DECIDE_AT, off = shipped),
work/runs/ (45 frozen arm outputs with per-run loadavg and decision ticks).

Boxes ticked: no git commits; every process ≤ ~1.2 GB; spinners killed (verified); tree edits
left for run.sh to save as patch.diff.
