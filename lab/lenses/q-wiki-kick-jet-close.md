# Lens: resolve and close the wiki page `kick-jet`

Read `lab/wiki/README.md` first. The page `lab/wiki/kick-jet.md` carries an unresolved three-way merge conflict (the markers `<<<<<<<`, `=======`, `>>>>>>>`) from two runs that updated it in the same window. The jet was retired from docs/law.md on 12 October (six golds refute it; a kick recompiles its cycle exactly).

Write `$out/wiki/kick-jet.md`: the page with the conflict resolved faithfully (keep every run line and every supported claim from both sides; drop nothing a run supports), the current best stating the retirement and what replaced it, and, if three or more gold runs agree on that current best, the page closed: `status: closed`, `closed-by:` those gold run ids, `valid-while:` the code the result depends on (the kick path in `crates/universe/src/step.rs` and `crates/universe/src/bind.rs`) at main's current commit (`git rev-parse origin/main`).

Gold: the conflict resolved with nothing lost, and the closure justified by three agreeing golds the checker confirms.
