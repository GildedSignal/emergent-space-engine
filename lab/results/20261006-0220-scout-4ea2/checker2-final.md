Working...
Check complete. `lab/results/20261006-0220-scout-4ea2/check2.md` written: **Grade: silver.**

What I did, in evidence:

**Reproduced**
- Plane: `PLANE_TRACE=1 … behave --law plane --gates B13` → 60/64, worst ΔE 1.26e0, 9 replaced — exactly the dossier. Trace: 64 ships; 62 with handoffs=1–2 (kicks 89–427, events 161–644); the two failing-class ships (kicks=2/handoffs=0, kicks=113/handoffs=0/opens=6) match verbatim.
- Falsifier: rerun is **byte-identical** to the author's JSON (diff 0 lines). Every pass count in the table matches; scene constants verified against `restricted.rs`/`assist.rs`.

**Held-out + adversarial (my own)**
- Fresh seed 777001 (the author invites fresh draws): L3@1.5 **66/66**, worst 6.6×10⁻³ — stronger than the author's 59/60; L1 0/66.
- Deep-and-slow corner (q∈[1.2,3] R_p at the v∞ floor): 13/13, worst 1.3×10⁻³.
- Resolution probe: at the 1/64 rule errors are already 10⁻⁵–10⁻⁴ and flat to 1/4096 — the interior is not the cost, as claimed.
- Novelty: H0214 froze B13 and the live HANDOFF reads "near-parabolic cadence"; this run corrects that premise (L1 fails 0/60 at all eccentricities; the 1.5·SOI door is the second load-bearing knob) and closes m-meso-motion's "deep flybys still fail" condition in float.

**Why silver, not gold:** nothing in the shipped code changed (`patch.diff` empty — the plane still fails B13 today), the integer-composition risk is unmeasured, and only 2 of the 4 B13 failures are attributed by the trace. The one experiment to gold: wire the 1.5·SOI analytic door into the integer plane and get 64/64.

Folder left as found (author's JSON restored — bit-identical anyway — `__pycache__` removed; `check.md` never read).
