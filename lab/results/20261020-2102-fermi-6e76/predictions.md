# Predictions (written before the backtrace arm and the fix arm)

Context: od 6(a)/6(b) of budget-1e9. 5f76's census counts, per player item, TWO doubling-ladder
array builds (one capped at exactly 57,344 B, one dying by rung 3 ≈ 23–29 KB of traffic) plus
~225 sub-2-KiB calls; it cannot name them. The candidates read from source before the run:
`encounter.rs::capture`'s `candidates: Vec<(usize, Binding, Scalar)>` (built with `Vec::new()` +
push), `radial.rs::candidates`' `ids: Vec<u32>` (+ its `collect()` into `Vec<usize>`), the held
`Scan` (`Arc<Scan>` holding those candidates), and the ships the player's item pulls (their
`step::process` scratch, nested in the player's scope by the instrument's rule).

## P1 — the capped ladder's site
The ladder whose terminus is exactly 57,344 B is **`encounter.rs::capture`'s `candidates`
vector** (the (usize, Binding, Scalar) tuples; ~352–366 B/entry ⇒ ~160 entries at the cap).
Kill bar: the top backtrace signature at sizes ≥ 28,656 B points anywhere else.

## P2 — the short ladder's site
The rung-1-to-3 ladder (dies ≤ ~13 KB) is **`radial.rs::candidates`' `ids` build**
(`Vec<u32>` unbounded-clone + bin extends, then the `Vec<usize>` collect). Kill bar: its
signature is absent from the 2–16 KB sampled events, or P1's site owns both ladders.

## P3 — the sub-2-KiB calls
The ~225 sub-2-KiB calls per player item (~1.4 per pulled body) come from the **pulled ships'
own items** (`step::process` and its re-plan), not from the player's scan itself. Kill bar: a
backtrace census at 0.5–2 KiB showing the scan's sites dominate. (Cheap to sample alongside;
secondary.)

## P4 — the burn chains
Under burn, the past-cap chains (to 3,670,016 B) grow **the same site as P1** (the cap is
coast-conditioned by the doll's population, not a code constant). Kill bar: the 3.7-MB
reallocs carry a different signature than the coast cap.

## P5 — the one-line fix (od 6(b))
`with_capacity` at the P1 site with the radial candidate count as the bound (the count is known
before the tuple build begins: `near`'s length) **halves the player term** (193.4 → ≤ 130
KB/item; 5f76's "halves" claim) and deletes the capped ladder's reallocs (~330k/flight → the
cap rung's share). Kill bar: the patched player term stays > 150 KB/item, or the ladder's top
persists at 57,344 B.

All five are falsifiable by the size-tagged backtrace census (coast + burn) and the patched
A1 rerun. No number above was tuned on any backtrace output; the site priors come from reading
the source only.
