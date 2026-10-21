#!/usr/bin/env python3
"""The 1e9 single-doll era ledger at cbe6's measured belt floor (the desynchronised grid).

Every input is a published, page-cited constant; no flight. The composition answers the
board's top macro row (kicks per body, ~1e3 at stake): what the desynchronised grid buys
on the ledger, what bar the class census must freeze, and which terms cadence cannot touch.

Citations (wiki pages, run ids):
  [NL]  lab/wiki/nladder.md  (0a46, 8365, 9ed1: rate/payload/era; a2c0, 20f2, a31c: the era ledger)
  [KC]  lab/wiki/kick-cadence.md (cbe6: the floor; 7076: the fine class; 67be: resonance)
  [BD]  lab/board.md (~9,000 kicks/belt-orbit plane-scene anchor; the focus row)
  [SG]  shipped code: crates/universe/src/ext.rs:146 constants(ctx, d, t, except, kicks_log2)
        — the clock constants are per body; kicks_log2 is one global dial.
"""
YR = 3.156e7  # game-s per year (1 game-s = 1 s)

# --- shipped / measured inputs -----------------------------------------------------------
lam_ship   = 4.889e-5      # kicks/body/gs, plane belt 1e5-3e5      [NL 0a46/8365/9ed1]
kick_us    = 45.5e-6       # payload per kick (45.3-45.9 us)        [NL 8365]
era_gs     = 27.9e3        # one doll era in game-s                 [NL]
era_budget = 69.75         # s of wall budget per era at 1e9        [NL a2c0/20f2]
kick_h     = 12.75         # kick-comb h/era at 1e9 = 658x          [NL a2c0/20f2/8365]
bnd_h      = 2.4           # boundary comb h/era (cheap payload)    [NL 8365]
walk_h     = (2.15, 6.02)  # capture ALL-walks h/era                [NL a0a1/20f2]
ans_h      = 1.19          # scan answers h/era                     [NL]
board_orbit= 9.0e3         # kicks per belt orbit, one doll-wide Ds  [BD]
floor_conj = 8             # kicks per governing synodic conj. PASS [KC cbe6]
floor_fail = 4             # kicks per conjunction FAIL (1.8e-4)    [KC cbe6]
fine_orbit = 256           # B13 encounter class, per own orbit     [KC 7076]
# cbe6's belt scene: belt 2-3 AU, planet Jupiter-class (6.2-9 Hill), belt orbit ~3.95 yr,
# synodic S ~5.93 yr, planet period ~11.86 yr; "16 per planet period = 5 per belt orbit
# = 8 per conjunction" is one rate ~1.3/yr. [KC cbe6]
belt_orbit_yr, S_cb6_yr, P_planet_yr = 3.95, 5.93, 11.86
S_77d_yr = 0.227           # synodic of a 77.24-d forcing (P_D) against a 3.95-yr belt [NL P_D]

def x(h): return h*3600/era_budget     # h/era -> multiples of the era budget

print("== The shipped ledger (1e9, single doll, belt-dominated) [NL]")
print(f"   kick comb {kick_h} h/era = {x(kick_h):.0f}x   walks {walk_h[0]}-{walk_h[1]} h = "
      f"{x(walk_h[0]):.0f}-{x(walk_h[1]):.0f}x   answers {ans_h} h = {x(ans_h):.0f}x")
tot = (kick_h+walk_h[0]+ans_h, kick_h+walk_h[1]+ans_h)
print(f"   total {tot[0]:.2f}-{tot[1]:.2f} h = {x(tot[0]):.0f}-{x(tot[1]):.0f}x "
      f"(boundary +{bnd_h} h = +{x(bnd_h):.0f}x separate [a31c: buys only 1.2x])")

print("\n== P1: the desync headroom R = lam_ship * S / floor_conj")
R_lam = lam_ship * (S_cb6_yr*YR) / floor_conj                 # anchor a: measured rate, cbe6's S
lam_orbit = board_orbit / (belt_orbit_yr*YR)                  # anchor b: board's per-orbit count
R_orb = lam_orbit * (S_cb6_yr*YR) / floor_conj
floor_rate = floor_conj / (S_cb6_yr*YR)
print(f"   floor rate {floor_rate:.2e}/B/gs (= {floor_conj/S_cb6_yr:.2f}/yr); "
      f"R(a: lam_ship) = {R_lam:.0f}   R(b: board 9,000/orbit) = {R_orb:.0f}   band [{1.0e3:.1e}, {1.8e3:.1e}]")
print(f"   P1 {'HELD' if 1.0e3 <= R_lam and R_orb <= 1.8e3 and 1.0e3 <= R_orb else 'CHECK'}: "
      f"both anchors in [1.0e3, 1.8e3]")

print("\n== P2: the kick row at the floor (payload constant per event [0c44; 98cb flat at /8])")
for name, R in (("a", R_lam), ("b", R_orb)):
    print(f"   anchor {name}: kick comb {x(kick_h):.0f}x -> {x(kick_h)/R:.3f}x "
          f"({kick_h*3600/R:.1f} s/era; margin {1/(x(kick_h)/R):.1f}x)")
print(f"   P2 {'HELD' if max(x(kick_h)/R_lam, x(kick_h)/R_orb) <= 0.6 else 'MISSED'}: <= 0.6x")
print(f"   below the floor is not a lever: {floor_fail}/conjunction FAILS B12 [cbe6]")

print("\n== P3: the census bar (fine class 256/orbit, B13 [7076])")
lam_fine = fine_orbit / (belt_orbit_yr*YR)
for name, lam in (("a", lam_ship), ("b", lam_orbit)):
    allowed = lam / x(kick_h)                       # rate that keeps the kick row <= 1x
    f = (allowed - floor_rate)/(lam_fine - floor_rate)
    print(f"   anchor {name}: allowed {allowed:.2e}/B/gs -> f_fine <= {100*f:.2f}%")
print("   P3 HELD if band within [1.5%, 3.5%]; resonance class excluded (cadence-blind, 67be)")

print("== P4: the scene bar (which forcing governs the closure)")
S_bar_gs = floor_conj * x(kick_h) / lam_ship             # gs; = 8 * 658 / lam_ship
S_bar_yr = S_bar_gs / YR
R_77 = lam_ship * (S_77d_yr*YR) / floor_conj
print(f"   closure iff governing S >= {S_bar_gs:.3e} gs = {S_bar_yr:.2f} yr; "
      f"at 77-d forcing S={S_77d_yr} yr: R = {R_77:.0f} -> kick row {x(kick_h)/R_77:.0f}x over")
print(f"   P4 {'HELD' if 3.0 <= S_bar_yr <= 4.0 and x(kick_h)/R_77 >= 10 else 'MISSED'}")

print("== P5: the wall moves; the ledger does not close")
kick_post = (x(kick_h)/max(R_lam, R_orb), x(kick_h)/min(R_lam, R_orb))
post = (kick_post[0] + x(walk_h[0]) + x(ans_h), kick_post[1] + x(walk_h[1]) + x(ans_h))
print(f"   post-desync total {post[0]:.0f}-{post[1]:.0f}x  (kick row {kick_post[0]:.2f}-"
      f"{kick_post[1]:.2f}x; walks {x(walk_h[0]):.0f}-{x(walk_h[1]):.0f}x + "
      f"answers {x(ans_h):.0f}x unchanged)")
print(f"   cut vs shipped: {x(tot[1])/post[1]:.1f}-{x(tot[0])/post[0]:.1f}x total; "
      f"scan channel is cadence-invariant -> the tier's row [b57f], not cadence's")

print("== P7: wt/cadence's 4-steps-per-period vs cbe6's floor, at the conjunction unit")
conj_per_period = 2.0     # cbe6 scene: 2 conjunctions per planet period (11.86/5.93)
print(f"   cbe6 PASS = 16/planet-period = 8/conjunction; FAIL = 8/planet = 4/conjunction")
print(f"   wt/cadence 4/Cinder-period = {4/conj_per_period:.0f}/conjunction if Cinder-period "
      f"holds 2 conjunctions -> at/below the FAILING point; must reconcile before any belt merge")



print("\n== Memory (one line, no claim beyond composition)")
print("   cadence-invariant here: the plateau is steady state per body (b30b 4.85-5.06 kB/B),")
print("   not churn; desync is CPU-only on this ledger. Live-set churn (~1 in-flight gen/kick)")
print("   falls with R; the 2.4 kB/B standing anchors do not [live-residency].")

print("\n== Adoption shape [SG ext.rs:146]")
print("   constants(ctx, d, t, except, kicks_log2): per-body clock constants behind ONE global")
print("   dial -> the desync is a policy change (kicks_log2 per class), not an algorithm.")
