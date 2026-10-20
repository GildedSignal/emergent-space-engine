# Predictions (written before the decisive arms)

Question, inverted: cc9d (this lens, 3 h ago) named the wall (the player's root item legally
pulls the whole belt's due ships past the budget) and the cheap fix ("extend the 766-770
budgeted-stream pattern to root"). What does that fix break? The pull exists so the player's
scan reads every ship of its doll **at its tick**; leaving the root's ships to the queue lets a
scan capture a binding whose due item (due before the scan's tick) is still unapplied — a read
the schedule, not the law, decides.

Arms: `ES_ROOT_SHIPS_TO_QUEUE=1` gates `universe.rs`'s root pull off (off = shipped, verified:
ladder_digest OFF digests match `artifacts/runs/nladder/ladder_digests_before.txt` exactly on
the first cases). `ES_FIX_PROBE` counts, per captured scan candidate, whether the body's next
item is due before the scan tick (a stale read).

- **P1 (the burst is the bypass, not the mass).** nladder 10⁵ burn rtf 1000, ~18 s wall: OFF
  max_ms in the record's band (0.8–0.95 s, one player item); **ON max_ms ≤ 60 ms**, over ≈ 0,
  and the wave drains at the budget instead: lag_s(ON) > lag_s(OFF) by ≥ 1 s.
- **P2 (the fix is a law change, measured).** ladder_digest ON: at least one case's digest
  differs from OFF (I predict the belt-crossing L10 cases, where the player is in the star's
  doll among the belt and scans meet the wave), and/or the four schedules disagree
  ("SCHEDULE DEPENDENCE FOUND") — the shipped instrument's own criterion for bookkeeping.
- **P3 (the change is the scan's, not the bodies').** kicks per case identical ON vs OFF
  (bodies read only sources; order does not move them); any digest difference is the scan
  chain.
- **P4 (safety).** refusals 0, dead unchanged, alive(player) true in every arm; no hang.
- **P5 (mechanism).** probe: OFF stale = 0 everywhere; ON stale > 0 only in the wave window,
  with stale_max a double-digit fraction of the doll's captured candidates at the peak scan.

Kill criteria for my own reading: ON max_ms > 200 ms at 10⁵ (the gulp survives the gate —
mechanism wrong); any OFF digest mismatch vs the record (instrument broken → VOID); a hang or
a crash in ON (the gate is unsound as written).

Held out (not tuned on): the 2×10⁵ rung (cc9d's headline), the key-mashing ladder_digest
cases, and ladder_digest's through-the-wave coast cases.
