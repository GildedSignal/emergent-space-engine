#!/usr/bin/env python3
"""The 10^9 budget, anchors separated by population (run: python3 fermi_belt.py).

Corrects run 20261007-1106-fermi-443e's one mixing error (kicks vs doll bindings, found by its checker)
and adds the belt-with-handoffs anchor that run lacked. Every line regenerates from printed anchors:

  plane (inner, hlive 3600 1 400, this run's regeneration, bit-identical to the author's .bin):
    615 distinct bindings / 28 bodies / 3600 game-s = 6.10e-3 bindings/body/game-s   <- the anchor
    13.00 B/event varint (104 bits/event), reabsorption 1.09/hour
  belt (hlive_belt 1000 1 1 2048 96, this run; seed 2 within 0.5%):
    309,980 bindings / 1096 ships / 3.742e8 game-s = 7.551e-7 bindings/body/game-s
    350,288 kicks + 96 handoffs -> 8.535e-7 engine events/body/game-s (kicks/binding 1.1)
    3.39 B/event varint (27.1 bits/event) on the same-doll path; handoff re-reference 50 bits/event
    reabsorption 1.05 over one planet orbit = 3.74e8 game-s (~12 game-years); seed 2: 1.04
    wall 49.7 us/engine event; bytes/body 1,682 after prune (unpruned history ~0.5-2.5 KB/binding,
    run-length dependent: a 5-orbit attempt passed 1.5 GB at ~600k bindings on 1,096 ships)
  machine (M1, from HANDOFF): 8 GB, ~60 GB/s. 1 game-second = 1 real second.
"""
BW = 60e9  # B/s
N = 1e9

# ---- anchors (do not edit: they are printed by the commands above) -----------------------------
rate_inner = 615 / 28 / 3600          # doll bindings/body/game-s, plane inner scale
b_inner = 13.00                       # B/event varint
rate_belt = 309980 / 1096 / 3.742e8   # doll bindings/body/game-s, belt at 5.2 AU
ev_belt = (350288 + 96) / 1096 / 3.742e8  # engine events (kicks+handoffs)/body/game-s
b_belt = 3.39                         # B/event varint, same-doll path
b_handoff = 50 / 8                    # B per handoff re-reference (50 bits, doll-change path)
rate_handoff = 96 / 1096 / 3.742e8    # handoffs/body/game-s (one per crosser per run)
us_belt = 49.7                        # us per engine event, settle wall (Linux x86, order only)

print(f"{'term':52s} {'1e9 bodies':>16s} {'budget':>10s}")
for name, rate, b in [
    ("H_live creation, inner (6.10e-3 b/s, 104 bits)", rate_inner, b_inner),
    ("H_live creation, belt (7.55e-7 b/s, 27 bits)", rate_belt, b_belt),
    ("H_live creation, belt engine events (kicks+ho)", ev_belt, b_belt),
    ("handoff re-references, belt", rate_handoff, b_handoff),
]:
    mb = N * rate * b
    print(f"{name:52s} {mb:>13.4g} B/s {BW:.0e} B/s  {BW/mb:>9.0f}x under")
print()
fill = 8e9 / (N * rate_inner * b_inner)
print(f"zero-reabsorption fill of 8 GB, all-inner: {fill:.0f} game-s (measured ratio 1.09/h -> bounded)")
fill_b = 8e9 / (N * rate_belt * b_belt)
print(f"zero-reabsorption fill of 8 GB, all-belt:   {fill_b:.2e} game-s (measured 1.05/12y -> bounded)")
print()
for label, us in [("belt, measured 49.7", us_belt), ("belt, plane's 12", 12.0)]:
    cores = N * ev_belt * us * 1e-6
    print(f"belt event compute at {label} us: {cores:.3f} core.s per game-s")
cores_in = N * rate_inner * 12e-6
print(f"inner binding compute at 12 us (the board's '190 cores' cadence): {cores_in:.0f} core.s per game-s")
print()
print(f"stored today, belt steady cache 1,682 B/body: {1682*N/1e12:.2f} TB -> {1682*N/8e9:.0f}x over 8 GB")
print(f"stored today, plane 1-hour cache 9,846 B/body: {9846*N/1e12:.2f} TB -> {9846*N/8e9:.0f}x over 8 GB")
print(f"belt program floor 0.126 bit/body: {0.126*N/8/1e6:.2f} MB -> {8e9/(0.126*N/8):.0f}x under 8 GB")
print(f"unpruned binding history today (belt instrument): ~0.5-2.5 KB/binding, run-length dependent")
