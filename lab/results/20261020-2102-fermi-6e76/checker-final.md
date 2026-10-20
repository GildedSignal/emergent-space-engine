Working...
Check complete. **Grade: silver** — written to `lab/results/20261020-2102-fermi-6e76/check.md`, with a checker block appended to the proposed wiki page.

**What I did:**

1. **Diagnosed the runner's regen failure**: `work/patch.diff` ships every file byte-duplicated (8 diff sections, 4 unique), so `git apply` rejects it from a clean tree — the fix phase's "verified exit 0" only exercised regen.sh's already-applied branch. Deduplicated, applied, ran regen.sh unmodified: **exit 0, 79 s, every dossier number regenerates** (193.4→179.7 KB/item, −11.6% reallocs, families A/B exact, micro-test 5,472→11,616, third site `body.rs:141`).

2. **Three adversarial arms, one outside the author's range**: K=10⁵ coast (next decade) holds at −7.1%; seed 2 holds at −5.8%; **burn** — never flown by the author — is safe (reallocs −7.8%, kicks/events **bit-identical** between shipped and fixed arms: direct proof capacity is not semantics). Determinism calibration (two identical fixed runs → identical counts) confirms the small coast kick deltas are budget coupling, not the fix.

3. **Novelty**: clean — the page's od 6(a) asked exactly for this instrument; nladder's b911 knows the `Scan.candidates` type but not the attribution, growth law, or the 95.7% filter die-off that decides which fix is legal.

4. **Predictions**: pre-registered with honestly wrong priors (448-B tuples vs guessed 352-366; reserve-exact vs guessed doubling) — P1/P2 held, P5 refuted the "halves" premise, **P4 (burn chains' site) never ran**.

**Why silver, not gold**: the shipped regen path is broken exactly per the taste log's "cannot regenerate" class, and P4 is undecided. Both steps to gold are named in check.md — minutes of packaging, plus naming the past-cap chains, which my seed-2 coast run shows is reachable without the burn crash (16 chains at mean 114,688 B on coast). Tree left clean; nothing committed or pushed.
