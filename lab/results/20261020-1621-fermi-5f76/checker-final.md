Working...
Check complete. `check.md` written; the author's wiki page corrected in place (two overstatements); nothing else in the run folder touched; tree left as the runner had it (patch applied, `lab/results/` untracked).

**Grade: silver.**

- **Reproduced:** runner's `regen.sh` exit 0, every dossier number regenerates (A1 193.4 KB/item, 11.35 KB/kick, 3.7 KB/ship-item; A2–A5 within the declared jitter). I re-derived the census independently from the raw logs — the two-array-build arithmetic closes exactly (108.8 KB capped ladder + ~23 KB short + 57.4 KB small ≈ 193.4).
- **Predictions:** pre-registered with kill bars; P1–P5 held, P6 half-held, disclosed by the author.
- **My three adversarial arms:** (1) K=3×10⁵ — outside the author's range: the player law holds (195.1 KB/item, top 57,341 ≈ exact) but the ship marginal keeps rising, **3.88 KB/kick**, so the 10⁹ band top is **54%**, not 42%; (2) seed 3 at K=10⁵: law and rise reproduce (199.4; 3.11); (3) **burn**: 311 KB/item, realloc 92%, ladders past the cap to 3,670,016 B — 8994's chains reproduced, and the law's coast scope drawn.
- **Not gold:** no 10× move, no deletion, no dead premise — both decision rows stand as 8994 left them; this hardens their base. Gold step named: the backtrace naming the two arrays (turns the census count into a deletable `with_capacity` target) plus the saturation arm at 10⁶.
