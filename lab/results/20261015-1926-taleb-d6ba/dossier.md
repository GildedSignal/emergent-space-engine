# Dossier — 20261015-1926-taleb-d6ba (taleb)

## Claim

The seam adoption candidate's never-demote residue is censused on the belt and it is **a wave
pulse, not a standing class and not a leak**: at depth (48k–96k game-s ≈ 2–4 kick-settle
periods) the belt's pinned compiled arcs collapse to **8.6 B/body in the variant** (57 in the
seam) against **1,449–1,569 shipped**, current bindings demote to ~0 (3 Live of 10,045),
**plunges mint zero at every depth flown** (the open worry is empty on the plane's scenes),
and dead bodies hold ≈1 arc per death (~700 B, a priced constant). What the seam does not
delete is the **settle wave's transient**: just after a wave, history holds ~711 B/body of
retired Live arcs, which prune drains within the keep window (present at the 20k cut, gone by
48k) — and the belt's memory term at depth is the **record stack** (`bytes_per_body`
980–1,317 across arms and cuts while pinned arcs swing 8.6 → 711), not the arcs.

## Bottleneck

Memory per live body at 10⁹ (the board's first and fourth live questions). 3dc8 closed the
passage half of the seam and named what stayed open: "plunges alone … and the boundary-
rebinding half of the standing arcs (not kick-settled, so never demoted)". Both are now
measured on the belt, with the instrument that was missing: a census of **every retained
binding of every body** (current vs history, alive vs dead, by trajectory class) plus
**mint-cause counters at the apply site**. The expected gain is not compute but the deletion
of a worry and the correction of the adoption sentence's numbers: the seam's belt standing
store at depth is ~8.6 B/body (the page's "962 B/body" was a mid-pulse, 20k-cut reading), so
at 10⁹ the seam+variant's arc term is ~9 MB, not ~1 GB, and what remains is the record stack
— the already-named wall (760f), now measured with the arcs deleted underneath it.

## Evidence

All numbers from `regen.sh` (build + frozen private binary + `matrix.sh`), flights in
`flights/*.txt`; Linux x86 8-vCPU box — orders of magnitude only, per the lab rules. The
patch is 3dc8's seam + demote-passages verbatim (fetched from its branch, applied to main)
plus this run's instrument: `examples/arc_pin.rs` (the census), `bind.rs::note_mint`/
`lazy_mint_counters` and one call at the `apply` mint site (`universe.rs:652`). The 10⁴ burn
20k variant arm reproduces 3dc8's published counters exactly (passage demotions 1,957,
promotions 44,890) — the merged instrument does not perturb the flight.

**The depth ladder (10⁴ coast seed 1 unless noted; pinned = Live compiled arcs in current +
history, alive + dead):**

| arm | cut | current Live / demoted | pinned B/body | bpb_engine | demotions | promotions |
|---|---|---|---|---|---|---|
| ctl | 20k | 10,048 / 0 | 1,449 | 1,697 | 0 | 0 |
| ctl | 20k (burn) | 10,048 / 0 | 1,569 | 1,748 | 0 | 0 |
| seam | 20k | 21 / 10,027 | 711 | 1,016 | 41,053 | 804,941 |
| variant | 20k | 3 / 10,045 | 656 | 1,009 | 41,402 | 839,887 |
| seam | 48k | 18 / 10,028 | 57 | 1,015 | 93,200 | 1,989,722 |
| variant | 48k | 2 / 10,044 | **8.6** | 1,008 | 94,518 | 2,078,952 |
| variant | 96k | 1 / 10,045 | **8.6** | 980 | 177,774 | 4,186,911 |
| variant | 20k (burn) | 3 / 10,045 | 656 | 1,059 | 42,144 | 669,884 |
| variant | 48k (burn) | 2 / 10,044 | **8.6** | 1,317 | 93,991 | 2,542,157 |
| variant, 10⁵ | 20k | 3 / 100,045 | 670 (mid-pulse) | 993 | 131,402 | 929,887 |
| variant, seed 3 | 48k | 2 / 10,049 | **6.6** | 1,010 | 107,349 | 2,124,569 |

**The class census at depth (variant, 48k):** nokick-mint arcs 2 per 10⁴ bodies; plunges 0
(also 0 at 20k/96k coast, 20k/48k burn, and in every comet arm); dead bodies 30, holding 10
Live arcs (~700 B each ≈ 20 kB total, constant per death, tracking `lost`); history segments
hold the pulse (at 20k: ~700 B/body of retired Live arcs; at 48k: pruned to ~9). The mint
counter: **every** apply mint in every arm carried `kick.len > 0` (`kickless = 0` at all
cuts) — there is no kick-less mint class on the belt at all; opens and boundary settles demote
with their kick.

**The pre-settle artifact (why the worry looked real):** at a 5k cut — before the first kick
settle (~26k game-s ≈ one belt period; the attached level-0 kick's `len` ≈ 5.35e9 ticks) — 97%
of current bindings are Live (9,791/10,049): bodies are **born Live and demote at their first
kick settle**. Any census (or rss reading) taken before the first settle reads the shipped
state. The comet arms show the same artifact and do NOT close the comet floor: mixed 1,000
comets at a 1.2k cut hold 522/1,052 kick-held Live current passages (21 kB/body pinned), and
star-grazers at 4,800 game-s — 3dc8's checker's depth — still hold 252/533 Live current
passages (22.5 kB/body pinned, 61,458 passage demotions already paid): the comet's first
settle (~28k game-s) is past every comet cut flown here or in 3dc8, so the comet-class floor
**at depth is unmeasured** — the missing experiment is a ≥ 30k comet cut (where most comets
are past the root loss radius and their arcs retire with them).

**The re-mint bill at depth (unchanged, f55d's story):** promotions are linear in depth with
no cap (96k: 4.19M cycle at p50 3.7 µs + 147k passage at 316 µs ≈ 113 s of compile inside a
96k-game-s flight); `mints = demotions` exactly at every cut (177,774 = 177,774 at 96k).

## Predictions

Pre-registered in `predictions.md` after the 5k smoke only. **P1 held, stronger than
registered**: the collapse went to 8.6 B/body at 48k (registered < 20% Live fraction and
< 250 B/body; measured 0.02% and 8.6), and it holds on the held-out seed (6.6), on burn
(8.6 at 48k) and at 96k (8.6). **P2 held**: residue classes are bounded (nokick 2–3 per
10⁴, plunges 0, history pruned); no class grows with depth. **P3 held** on the belt: dead
arcs track the loss count at ~1 arc/death. **P4 split**: the belt half held (variant ≈ seam:
656 vs 711 at 20k, 8.6 vs 57 at 48k — the delta is the passage history pulse); the comet
half **FAILED as registered** — I had written "the collapse is real there" from 3dc8's
checker's rss reading, but the census at stargraze 4,800 still reads 252/533 Live currents:
rss collapse (held scans deleted) is not arc collapse, and no comet cut flown reaches the
comet's first settle (~28k game-s). One more registration error: I expected the pulse
history-bounded at ~250 B/body at 20k; the 20k cut landed mid-pulse (711 B/body) — the pulse
peak, not the floor, is the worst instant.

## What would make it wrong

The census reads the store at one canonical cut per flight; a pulse shorter than the cut
grid could hide a higher peak (the 20k reading bounds it at ~ctl's standing ≈ 1.4 kB/body
only if the pulse cannot exceed one arc per body — true: each body retires at most the one
arc it stood). Plunges mint zero **on the plane's scenes**; a scene that mints plunges (a
fall into the star or a planet from a stirred belt) would reopen the class — priced per arc
at `Plunge::retained_bytes()` until then. Both comet arms (mixed 1.2k, stargraze 4.8k) are
pre-settle and say nothing about the comet floor at depth; until a ≥ 30k comet cut is flown,
the comet-class residue must be budgeted at its pre-settle worst (~22 kB/body) — the census
instrument (`arc_pin`) is what that flight should carry.

## Cost of adopting, and fit with PRINCIPLES

Nothing to adopt: the seam patch is 3dc8's, unchanged; this run adds the census instrument
(`arc_pin`, ~200 lines, example + two counters) that any later seam flight should carry. The
adoption sentence it corrects: the seam's belt floor is ~9 B/body at depth **with a wave
pulse ≤ ~0.7 kB/body transient** — at 10⁹ that is ~9 MB standing + a wave-front pulse, so
the arc term leaves the 8 GB arithmetic and the record stack (~1 kB/body = 1 GB at 10⁹) is
the belt's memory term, as 760f said. Fit: "Store the generator, not the generated" (the
census shows the belt's generated arcs are, at depth, exactly the transient the generator
replaces) and "Errors never compound" (the residue is a pulse that prune drains, not a
monotone term — the leak hypothesis is dead on the flown domain).

## The lens

The Taleb lens went hunting a leak (ruin first) and found a pulse: the honest worst case is
the wave instant (~2× shipped standing), not the floor, and the run's main deliverable is a
bound with the floor, the peak and the drain rate separated. What the lens may have missed:
the promotion bill (f55d's territory) is the seam's real cost at depth and is only cited, not
re-priced here; and the 10⁵ arm bounds N-scaling of the floor but not of the pulse's drain
time at larger N.
