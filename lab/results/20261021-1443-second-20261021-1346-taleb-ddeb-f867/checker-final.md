Working...
Check complete. **Grade: silver** — written to `check.md`, with the author's wiki page corrected in place.

**What reproduced (clean tree, patch applied):** the `beltc` control matches cbe6's gold record to the digit (same worst-J vector, kicks 19,772); ddeb's census defaults regenerate 115.41/78×; the zone ladder (4.8e-8 → 2.2e-5 at step 4, super-quadratic break at step 3), zero deaths/refusals, Δe step-independent per ship — all as claimed, predictions pre-declared the branch that fired.

**My adversarial flights (all held):** 800 planet periods (8× the flown horizon — zone worst 2.6e-5, no walk); the never-flown q=3 zone 5:2 via a temporary class (2.6e-5 PASS at step 4, fails at 3 — the "conservative extrapolation" is now measured); e-tail at 400P/seed2 (9.0e-5, the thin margin the author flagged); zone-width ×0.33–×3 flat.

**Why not gold:** the headline constant is one octave off, and it is load-bearing. The engine counts **~33 kicks/Giant-period at the step-4 dial** (my probe: 329 kicks/10 planet-periods/one ship, `stats.kicks` counts kick events only; the `period` constant verified exact in ticks; cbe6's own 19,772/100P/6 ships = 32.95 agrees). The "16/GP ≈ 8/conjunction" label — cbe6's, inherited by ddeb and this run — describes the *failing* step-3 dial. The dossier's own evidence prints 32.3–33.5 and calls it a re-confirmation of 16. Corrected composition: **≈21.9 events/body/belt-orbit → ≈410×** (not 838×), and the page's adoption sentence Δs = 2⁻⁴·P_G would fly the failing dial — the certified constant is **2⁻⁵**. The retraction of ddeb's 78× survives untouched (the PASS/FAIL ladder is dial-based; ddeb's bill was 256/own-orbit-dominated). The one step to gold needs no new flight: a 5-line edit giving `beltcensus`'s hardcoded clean class the same dial, then relabel.

Tree left as found (probe files removed, patch reversed); nothing committed or pushed.
