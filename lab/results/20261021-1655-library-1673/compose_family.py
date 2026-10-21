#!/usr/bin/env python3
"""The family's ledger, composed from page-cited constants and shipped code literals.

No flight: every input is a published measurement (wiki page, run id) or a literal in the
tree (grep-verified below). Cloud arithmetic; orders of magnitude only.
"""
import math, re, subprocess, sys, os

W = print
def band(x, y): return f"{x:.3g}–{y:.3g}"

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

# ---- 0. code literals, grep-verified from the tree (fails loudly if the tree moves) ----
def lit(path, pat):
    txt = open(os.path.join(ROOT, path)).read()
    m = re.search(pat, txt)
    assert m, f"literal not found: {path}: {pat}"
    return m

r_lat_line = lit("crates/universe/src/scenario.rs", r"let r_lat: i64 = (4_740 \* Q);")
moon_line  = lit("crates/universe/src/scenario.rs", r"periapsis: Scalar::raw\(260_000, 18\)")
members_line = lit("crates/universe/examples/tail.rs", r"unwrapor\(48\)|\.unwrap_or\(48\)")  # shipped members default
fleet_q = lit("crates/universe/src/fleet.rs", r"pub const Q: i64 = 1 << 20;")
W(f"# code literals verified: r_lat={r_lat_line.group(0)!r} moon={moon_line.group(0)!r} Q={fleet_q.group(0)!r}")
W(f"# shipped plane default members = 48 (scenario.rs examples; tail.rs default 48)")

# ---- constants (page-cited) ----
ROOT_KM   = 7000 / 4740            # scenario.rs:265 "7,000 km: 4,740 root units"
AU_KM     = 1.496e8
AU_ROOT   = AU_KM / ROOT_KM
MOON_R    = 260_000                # scenario.rs:192
LOCALS_MAX = 2/3 * MOON_R          # scenario.rs:324-326 "out to two thirds of the Moon's distance"
KILL_R    = 15_000                 # 033c: word dead as a child-doll representation above ~1.5e4 root
DEATH_PER_DECADE = 110             # 033c: rate law h/q ∝ r², 110× per decade
# fork anchors (033c + checker): radius root -> first-fork kicks
FORK_ANCHORS = [(4_740, 682, 3367, 0.16), (15_000, 69, 69, None), (47_400, 3, 5, 38.5), (150_000, 1, 20, None), (250_000, 1, 1, None)]
BELT_FORK_KICKS = (554, 13_512)    # 033c: three arms, dx 1e4–1e5
BELT_FORK_ORBITS = (35, 845)
H_PER_ORBIT = 16                   # 033c/f867: h = P/16
# dynamics (game-s)
MU_E, R_E = 3.986e14, 7_000e3      # LEO: 7,000 km radius (scenario.rs:265)
T_LEO = 2*math.pi*math.sqrt(R_E**3/MU_E)
T_BELT = math.sqrt((2.5**3)) * 3.156e7   # 2.5 AU about a solar-mass star, seconds
# events and costs
BELT_FLOOR_EV = 21.9               # f867: events/body/belt-orbit at the floor (both combs); 99d7 composed 16.2
LEO_CADENCE   = 16                 # cbe6: 16/orbit floor unit (the conjunction)
EVENT_BUDGET  = 4e6                # 3aec: rtf 100 = 4e6 events/wall-s
KICK_US  = (35.1, 35.4)            # 6faa: made kicks
REBIND_US = 58.0                   # board (20 Oct): the fit that remains
WORD_US  = 4.4                     # kick-jet: fit_key 4.4 µs (the word-update class)
# bytes (page-cited)
STAND_B   = (2432, 2452)           # a990: standing B/body at 1e5–1e6
PLATEAU_B = 5060                   # b30b via 6793: post-first-kick plateau
CACHE_B   = 1171                   # GPT 3bb7e9d9 (HANDOFF 19 Oct): shared table cache at 1e6
COMPACT_PL_BITS = (21, 40)         # HANDOFF scoreboard: phase-locked belt
COMPACT_DR_BITS = 126              # HANDOFF scoreboard: driven belt worst
GOAL_B    = 6                      # HANDOFF scoreboard: 10⁹ in ~6 GB
MINT_B    = 2100                   # 225d: the mint ~2.1 KB/binding
W_BYTES   = (8, 16, 32)            # the member word: offset + w11 dv residual (a877's quantities), banded
FLEET_F   = 48                     # the plane's Armada (shipped default)
VERIFY_F  = 400                    # cf2a's coherent verify fleets
HORIZON_GAME_S = 1200 * 100        # a990 checker's longest arm: 1,200 s wall at rtf 100

# ---- T1: the domain map (033c's death law + the plane's populations) ----
W("\n== T1 domain map: word lifetime per population (measured anchors + r² law) ==")
W(f"root unit = {ROOT_KM:.4f} km; AU = {AU_ROOT:.4g} root; belt 2–3 AU = {2*AU_ROOT:.3g}–{3*AU_ROOT:.3g} root (root doll)")
for r, lo, hi, dis in FORK_ANCHORS:
    W(f"  r={r:>7} root ({r*ROOT_KM/1000:7.1f} kkm): first fork {lo}–{hi} kicks" + (f", steady disagree {dis}%" if dis else ""))
rate_at = lambda r: FORK_ANCHORS[0][1] * (r/4_740)**2 * DEATH_PER_DECADE/ (10**2)  # not used; anchors quoted directly
for name, r in [("fleet lattice (LEO)", 4_740), ("Home/Moon locals max", LOCALS_MAX), ("L4/L5 locals", MOON_R)]:
    ratio = r / KILL_R
    W(f"  {name}: r = {r:,.0f} root = {ratio:.1f}× the 15,000 kill radius -> "
      + ("IN domain (kill unproven, steady rate favours family)" if r == 4_740 else "DEAD domain (word forks in 1–20 kicks)"))
W(f"  P1: locals max {LOCALS_MAX:,.0f} vs kill {KILL_R:,}: ratio {LOCALS_MAX/KILL_R:.1f}x (>=11 predicted); "
  f"L4/L5 ratio {MOON_R/KILL_R:.1f}x")

# ---- T2: bytes per body, by route and population ----
W("\n== T2 bytes/body: family (B+F*w)/F vs compact vs cache ==")
def fam(B, F, w): return (B + F*w)/F
for B, tag in [(STAND_B[0], "standing 2,432"), (CACHE_B, "with table cache 1,171"), (PLATEAU_B, "plateau 5,060")]:
    for F in (FLEET_F, 64, VERIFY_F, 2_700, 10_000):
        row = " ".join(f"w{w}:{fam(B,F,w):7.2f}B" for w in W_BYTES)
        W(f"  {tag:22s} F={F:<6} {row}")
W(f"  compact phase-locked: {COMPACT_PL_BITS[0]/8:.2f}–{COMPACT_PL_BITS[1]/8:.2f} B; driven worst {COMPACT_DR_BITS/8:.2f} B; goal <= {GOAL_B} B")
W(f"  family floor at F->inf is w itself: {W_BYTES[0]}–{W_BYTES[2]} B -> misses {GOAL_B} B alone at every w (P2 first half)")
best_fam = fam(CACHE_B, 10_000, 8)
W(f"  best family arm (cache, F=1e4, w=8): {best_fam:.2f} B vs compact phase-locked worst {COMPACT_PL_BITS[1]/8:.2f} B: "
  f"compact wins {best_fam/(COMPACT_PL_BITS[1]/8):.1f}x at the belt (P2)")
W(f"  driven comparison: family (cache,F=400,w=8) {fam(CACHE_B,400,8):.2f} B vs compact driven {COMPACT_DR_BITS/8:.2f} B: "
  f"family {'wins' if fam(CACHE_B,400,8)<COMPACT_DR_BITS/8 else 'loses'} {max(fam(CACHE_B,400,8),(COMPACT_DR_BITS/8))/min(fam(CACHE_B,400,8),(COMPACT_DR_BITS/8)):.2f}x")
# blended 10^9 row: (1-f)*compact_pl + f*route <= 6 B
W("  blended 10^9 row: driven share f with compact_pl=5 B cap and route R:")
for tag, R in [("compact driven 15.75", 15.75), ("family (cache,F=400,w=16)", fam(CACHE_B,400,16)), ("family (cache,F=1e4,w=8)", fam(CACHE_B,10_000,8))]:
    f_max = (GOAL_B - COMPACT_PL_BITS[1]/8) / (R - COMPACT_PL_BITS[1]/8)
    W(f"    route {tag:28s} R={R:5.2f} B -> closure iff f <= {f_max*100:.1f}%")

# ---- T3: the fork bill vs the stream saving at the belt ----
W("\n== T3 fork bill at the belt (worst recurring cadence, dearest handler) ==")
for F in (16, VERIFY_F, 2_700):
    saving = BELT_FLOOR_EV * KICK_US[0] * (1 - 1/F)          # µs per body per orbit
    worst_bill = (1/BELT_FORK_ORBITS[0]) * REBIND_US          # 1 fork per 35 orbits, 58 µs rebind
    cheap_bill = (1/BELT_FORK_ORBITS[1]) * WORD_US
    W(f"  F={F:<5} stream saving {saving:7.1f} µs/B/orbit; fork bill {cheap_bill:.4f}–{worst_bill:.3f} µs/B/orbit "
      f"= {100*worst_bill/saving:.3f}% of saving (P3 bound 0.3%)")

# ---- T4: the event ledger's regime split (belt vs fleet) and the family's row ----
W("\n== T4 events: where one population dominates the total ==")
belt_rate = BELT_FLOOR_EV / T_BELT          # events/body/game-s
leo_rate  = LEO_CADENCE / T_LEO
W(f"  belt: {BELT_FLOOR_EV} ev/B/{T_BELT:.3g} s = {belt_rate:.3g} ev/B/game-s;  LEO: 16/{T_LEO:.0f} s = {leo_rate:.3g} ev/B/game-s "
  f"-> LEO is {leo_rate/belt_rate:.3g}x the belt's per-body rate")
for share in (0.01, 0.05, 0.10):
    rate = 1e9*(share*leo_rate + (1-share)*belt_rate) * 100   # events/wall-s at rtf 100
    W(f"  10^9 with {share*100:>4.0f}% fleet share: {rate:.3g} ev/wall-s vs budget {EVENT_BUDGET:.1g} = {rate/EVENT_BUDGET:.2f}x")
F = 10_000
for share in (0.01, 0.05, 0.10):
    rate = 1e9*(share*leo_rate/F + (1-share)*belt_rate) * 100
dis = 0.16/100
per_body_shared = (1 + dis*(FLEET_F-1))/FLEET_F
W(f"  fire collapse at the plane's own F={FLEET_F} (disagree {dis*100:.2f}%): fires/B/interval = 1/F + disagree = {per_body_shared:.4f} "
  f"-> {1/per_body_shared:.1f}x (P4 second half, >=40 predicted)")

# ---- T5: the fleet certificate vs every flown horizon ----
W("\n== T5 certificate lifetimes vs horizons ==")
cert_orbits = (FORK_ANCHORS[0][1]/H_PER_ORBIT, FORK_ANCHORS[0][2]/H_PER_ORBIT)  # fleet anchors 682–3,367 kicks
W(f"  belt certificate: {BELT_FORK_ORBITS[0]}–{BELT_FORK_ORBITS[1]} orbits = {BELT_FORK_ORBITS[0]*T_BELT:.3g}–{BELT_FORK_ORBITS[1]*T_BELT:.3g} game-s")
W(f"  fleet certificate at 4,740: {cert_orbits[0]:.0f}–{cert_orbits[1]:.0f} LEO orbits = {cert_orbits[0]*T_LEO:.3g}–{cert_orbits[1]*T_LEO:.3g} game-s")
horizon_orbits = HORIZON_GAME_S / T_LEO
W(f"  longest flown horizon {HORIZON_GAME_S:.1g} game-s = {horizon_orbits:.1f} LEO orbits -> margin {cert_orbits[0]/horizon_orbits:.2f}–{cert_orbits[1]/horizon_orbits:.1f}x (P4 first half, >=2 predicted)")
W(f"  belt certificate vs the 10^9 ledger's own horizon T* = 3.37e7 game-s (e29c): {BELT_FORK_ORBITS[0]*T_BELT/3.37e7:.0f}x over it")

# ---- quote verification (P5) ----
W("\n== P5: quote byte-identity against the cached fresh export ==")
LESSONS = [
 ("Egan, Diaspora",
  "it required a profound myopia of scale and similarity to believe that everything beyond this shallow layer could be ignored"),
 ("Munger, The Revised Psychology of Human Misjudgment (Farnam Street)",
  "To a man with only a hammer every problem looks pretty much like a nail."),
 ("Taleb, 20 Aphorisms (Farnam Street)",
  "The more frequently you look at data, the more noise you are disproportionally likely to get (rather than the valuable part called the signal); hence the higher the noise to signal ratio."),
 ("Housel, The Psychology of Money",
  "Growth is driven by compounding, which always takes time. Destruction is driven by single points of failure, which can happen in seconds, and loss of confidence, which can happen in an instant."),
 ("Taleb, The Black Swan",
  "In Extremistan, inequalities are such that one single observation can disproportionately impact the aggregate, or the total."),
]
corpus = open(os.path.join(HERE, "quotes.txt")).read()
ok = 0
for src, q in LESSONS:
    hit = q in corpus
    ok += hit
    W(f"  [{ 'OK ' if hit else 'FAIL'}] {src}: {q[:60]}...")
W(f"  P5: {ok}/5 byte-identical")
sys.exit(0 if ok == 5 else 1)
