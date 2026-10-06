# Predictions (written before the decisive held-out runs)

Tuning/validation already done (not held out): belt eps=1e-4 kappa=0.3 s=4 reproduces q-skin's
published failure bit-for-bit on the old binary (skin 29 missed, naive 102, always 0 of 159;
us/kick 3462 vs always 3151). The width-term binary did not finish that case in 300 s
(always: 38 s) — the cost explosion at large s is already a measured outcome, disclosed here
before the held-out cases below.

The width term: Skin-mode windows are built at rho_eff = rho + 1.5 * s * rmax^2 (a total Binet
drift bounded by the trigger's s moves positions by at most sqrt(2)*s*rmax^2), Cross linear
shortcut disabled, so every window is the rigorous conservative-advancement hull at rho_eff.

Held-out cases (not yet run): belt eps=1e-6 (the plane's kick size, the skin's target regime),
s in {4, 16}; fleet eps=1e-4 s=4; ring truth-check at eps=1e-4 s=4 (control, both sides).

1. **Soundness.** The width-term skin misses 0 events vs `always` on belt eps=1e-6 at s=4 and
   s=16, and on fleet eps=1e-4 s=4, with 0 false. The ring truth-check shows 0 missed for
   both `always` and the new `skin` against the independent dense truth. If any miss > 0
   appears, the width term as derived is wrong or incomplete (another drift channel exists),
   and I report where it leaks.
2. **Cost at the plane regime (decisive for the lever).** belt eps=1e-6 s=4: setups/kick stays
   near the old skin's 14.9 (the trigger logic is unchanged; window width does not affect
   trigger rate), checks/kick grows roughly with the window inflation factor
   (rho_eff/rho ~ 20-25 on the belt) from the old ~0.2/kick, and us_pass grows accordingly;
   I predict total us/kick stays below `always`'s ~3300 (the old skin's whole margin came from
   killing setups at 189/kick to ~15/kick, worth ~1600 us/kick; the pass inflation eats part
   of it but not all). If us/kick exceeds `always`, the width term kills the skin's economy
   even at the plane regime and the lever is dead as built.
3. **s-tradeoff flattens.** At eps=1e-6, s=16 is still exact for the new skin (bigger budget,
   bigger rho_eff), with us/kick within ~3x of s=4's; the old skin's s=16 was unsound territory
   (never published as exact). No prediction on which of {4,16} is cheaper; both measured.
4. **Fleet.** Full-section-heavy: the width term scales the Full pad linearly in rho_eff;
   I predict 0 missed (old skin was already 0 there) and us/kick within 3x of the old skin's
   14.6k... measured, not assumed; the fleet's clustered Binet points make near-tangential
   crossings common, which is exactly what the width term was built for.
5. **Kill criteria.** (a) any miss > 0 on any held-out case kills the width term as derived;
   (b) us/kick > always's on belt eps=1e-6 s=4 kills the skin-with-width as the encounters
   lever at the plane regime, leaving only smaller s (narrower skins) as the design space.
