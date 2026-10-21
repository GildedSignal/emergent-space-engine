Working...
Check complete. `lab/results/20261021-0312-system-15d7/check.md` written — **Grade: silver** — and the tree restored to as-found (clean except `lab/results/`).

**What I verified:**

- **Reproduction** (runner's `regen.sh` + my own code reading): every dossier number matches — digest `f9af771e…`, 1,267,977 combs / 510,004 clock-stepped, fires 0 crash / 0 leave / 18 handoff (all `release` in doll 2), kick-surface 0, plunge suite 2-passed/0-fires. Shipped-code claims all check out: `boundary_clock` = two certificates + `anchor = t`, no handoff arm (step.rs:751-770); `kick_clock` checks planets' + doll surfaces (688-701); the digest hashes `r.anchor` (universe.rs:1327) and the ramp's `lead` reads it (738) — the anchor is law-visible as claimed.
- **Predictions** pre-registered (mtime order) and held; P3's first branch honestly reported; controls on both sides.
- **Three adversarial cases of my own, all holding**: seed 7 at 3×10⁴ (200k gs), N=10⁵ (outside the author's range), N=3×10³ seed 3 — zero clock fires in every one.
- **Novelty**: fire census + derivation are new (a31c priced the comb, never counted fires); one overstatement — the anchor's digest cost was already named by a31c.

**Why silver, not gold**: nothing is deleted or flown — the derivation is unimplemented, the row's gain stays a31c's 1.2×. Gold is one flight away: build the deletion (kick-written anchor, per-kick `E<0` gate, digest re-freeze), re-fly the census, plus one E→0/assist adversarial arm.

**Corrections made to the author's page**: it was invalid as written — placeholders had replaced the 32 Refuted entries, directions 3-10, and all prior run lines, and three standing current-best lines were dropped unsuperseded. Rebuilt from base `fa431e16` with the census folded in: 181/300 lines, current best 15/15, one line per run. Also flagged: two stray `fires.txt` files shipped in the patch, no seed ensemble in the author's own run, and the belt-phase mechanism being over-determined (both apsides ≫ surface).
