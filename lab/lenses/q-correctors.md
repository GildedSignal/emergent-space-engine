# Lens: fewer kicks per orbit (symplectic correctors), a directed question

The plane's motion law (docs/law.md, "Perturbed motion"; crates/universe/src/step.rs) is a Wisdom–Holman split: an exact compiled drift plus kicks at a fixed step in the drift's phase. A kick costs about 24 µs on the M1 (`cargo run --release -p xtask -- universe --kick-bench`); making each one cheaper gained only 8%. The lever is fewer kicks per orbit at the same behaviour.

**Question:** do symplectic correctors (Wisdom, Holman and Touma 1996; WHFast, Rein and Tamayo 2015) or a higher-order split (Laskar and Robutel's SABA/SBAB, 2001) let the plane take 4× or more fewer kicks per orbit with unchanged behaviours: bounded Jacobi error with no secular growth, the apsidal precession of moons (law.md B14), resonance (B17)?
- Build a float replica of the plane's split in your folder, in Python or Rust (never edit the crates), on the plane's scene: one star, planets, a moon, ships. Held out: a moon at e = 0.3, and a close planet pass.
- Report kicks per orbit against each behaviour for each scheme, and the step ratio at which each breaks.
- Correctors act only on what is observed. Say whether that fits our rule that observation is a pure function of the state.
- Say whether each scheme stays exact in integers (a kick is a sum; a corrector is a map).

Gold: a measured cut of 4× or more in kicks per orbit, at unchanged behaviours, with its integer path named.
