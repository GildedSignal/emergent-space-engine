Working...
**Grade: gold** — written to `check2.md`, blind to the first checker.

**Verification performed:**
- **Reproduction, three independent ways:** runner's regen (exit 0); my re-derivation of the author's window numbers from raw logs (9/18 fires, 2,295 RB, 9 m≠0 = the fires, `out=` 0/2,295, 950 D=0, 18 D=16 lines = 2 per fatal certify); my own fresh sweep (4 fires, all D=16=viol, `out=` 0/548). Raw fire mechanics spot-checked line-by-line: PRE → FIRE → the untouched shipped assert panicking with its original message.
- **Provenance:** `finpol.rs` byte-identical to 01e7's branch; `race.rs` byte-identical to fd35's patch; alloc.rs delta vs fd35 is 37 lines, all print-only (`out=`/`mo`).
- **Predictions:** mtime ordering verified (pilot 18:32 → predictions 18:33 → sweep 18:35); P1–P6 all held; kill criteria pre-written, none triggered.
- **Six adversarial cases, two outside the author's domain:** 2× N (480 bodies, equality law held on 894 RB), double rate **fired** (D=viol exact, armed preceded), batch driver **fired** (D exact, adjacent), window 32 (17 armed D=32 lines, 0 fires — armed ≠ incidence confirmed), drift and wave scenes clean. 19 total fires across all executions, zero invariant failures on ~2,300 further RB events.
- **Numbers that differ** (recorded in check2.md): all raced/schedule-moved counts — regen rollbacks 1300/1283 vs quoted 565/558, h_nosab 13 armed vs 14–15, RB events 852 vs 906, s13 gap 8 vs 9 — invariants identical everywhere.

**One page correction** (in place): "which is WHY D is exact" overstated containment as derivation — now reads "why D never misses (containment); its exactness is the measured equality, derivation still open (direction 7)".

**Not gold-closing the topic:** fd35 still awaits its grade; this is one gold on the page.

Scratch cleaned; only `check2.md` and the wiki correction touched; no git operations.
