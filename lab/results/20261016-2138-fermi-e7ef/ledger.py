#!/usr/bin/env python3
"""The 10^9 closing ledger, assembled from measured constants (every one cited).

Fermi lens: which 10^9 term breaks first, and is the scoreboard's kick-cost row
(75-160 us vs a 42-55 ns floor, gap 10^3.3) on the critical path?

Units: cores = CPU-seconds per wall-second at rtf 100 (1 wall-s = 100 game-s),
budget 4 cores (the M1's performance cores). Pure arithmetic, deterministic.
"""
import json

# ---- anchors (each cited to its run/page) -----------------------------------
N = 1e9                     # the goal's bodies
RTF = 100.0                 # the player's flying pace (4093, 2ae0)
BUDGET = 4.0                # M1 performance cores (scoreboard frame; encounters page)
FRAME = 0.72                # s of compute per s of wall at 60 fps x 12 ms (4093's clamp ceiling)
RATE = 3.55e-5              # fired kicks /body/game-s, invariant in seed and N (a9d7, gold; spread 3.3-3.6e-5)
C_X86 = 50e-6               # s per stream event, this box class (4093: 50-52 us; c01c 43-52.8)
C_M1 = 29.3e-6              # s per event, M1 anchor (1051's wall-ladder constants)
INTERVAL = 28141.5          # game-s, the belt's kick interval, the doll grid (3294 measured; 4093)
SPLIT = 8.0                 # legal cadence cut, regime-split measured on the integer plane (7f97, silver)
DEL_FROZEN = 0.385          # belt bodies deleted by the hybrid, frozen resonance exclusion (1a46: 274/712)
DEL_WIDE = 0.61             # same with the exclusion widened to B17's libration width (1a46: 434/712)
SECULAR = (15.0, 60.0)      # secular-certificate kick cut, extrapolated, unmeasured on shipped code (5030)
FLOOR_NS = (42e-9, 56e-9)   # the exact-refit kick floor (b063, gold)
B_LEAVER = 75.6e-6          # kick before the retired search (b063); b583 halves the leaver class

# encounters (cores at 10^9, flying pace, contiguous belt, averaged cadence)
ENC_BASE = (1.65e3, 8.2e3)      # the cube's contiguous+averaged cell (1738)
ENC_GATE = (1.0/24.0, 1.0/14.0) # quantum-gate ceiling 14-24x (277d, silver)
ENC_ROUTE = (0.03, 0.6)         # birth-constant routing (f0a2, awaiting grade)

# memory at 10^9 against the ~6 GB / 48-bit budget (scoreboard)
MEM_BUDGET_BITS = 48.0
MEM = {  # bits/body and where from
    "compact store, phase-locked belt (measured alone)": (21.0, 40.0),
    "3-field sorted floor (0820 gold)": (61.6, 62.1),
    "4-field exact floor, phase carried (0820 gold)": (125.5, 126.1),
    "driven-belt worst (fc48/d0ea family)": (126.4, 126.4),
}
SHIPPED_LIVE_B = (4850.0, 5060.0)  # B/body plateau (b30b)
HOT_KB, HOT_N = 6.9e3, (1.3e4, 2.7e4)  # hot body bytes and hot count at rtf 100 (a11b/ba64)

def stream_cores(cost, cadence_cut=1.0, delete_frac=0.0, secular=None):
    """Cores for the belt kick stream at N, rtf 100."""
    cores = N * RATE * cost * RTF * (1.0 / cadence_cut) * (1.0 - delete_frac)
    if secular:
        cores /= secular
    return cores

def required_cost(budget=BUDGET, cadence_cut=1.0, delete_frac=0.0, secular=None):
    """The per-kick cost that exactly fills `budget` cores, given the levers."""
    denom = N * RATE * RTF * (1.0 / cadence_cut) * (1.0 - delete_frac)
    if secular:
        denom /= secular
    return budget / denom

rows = []

def note(s):
    rows.append(s)
    print(s)

# ---- P3/P4: the stream ledger and the redundancy ---------------------------
note("# The belt kick stream at 10^9, rtf 100 (cores; budget 4)")
configs = [
    ("shipped cadence, today's kick (x86 50us)", dict(cost=C_X86)),
    ("shipped cadence, today's kick (M1 29.3us)", dict(cost=C_M1)),
    ("shipped cadence, kick at the 42-56ns floor (b063)", dict(cost=49e-9)),
    ("8x regime-split cadence only (7f97), 50us", dict(cost=C_X86, cadence_cut=SPLIT)),
    ("8x + frozen-exclusion delete 38.5% (1a46)", dict(cost=C_X86, cadence_cut=SPLIT, delete_frac=DEL_FROZEN)),
    ("8x + widened delete 61% (1a46+RES)", dict(cost=C_X86, cadence_cut=SPLIT, delete_frac=DEL_WIDE)),
    ("8x + widened delete + secular 15x (extrapolated, 5030)", dict(cost=C_X86, cadence_cut=SPLIT, delete_frac=DEL_WIDE, secular=SECULAR[0])),
    ("8x + widened delete + secular 60x (extrapolated, 5030)", dict(cost=C_X86, cadence_cut=SPLIT, delete_frac=DEL_WIDE, secular=SECULAR[1])),
]
for name, kw in configs:
    note(f"  {name:58s} {stream_cores(**kw):8.2f} cores")

note("")
note("# Required per-kick cost to fit 4 cores (vs the 42-56 ns floor)")
for name, kw in [
    ("shipped cadence", dict()),
    ("8x split", dict(cadence_cut=SPLIT)),
    ("8x + delete 38.5%", dict(cadence_cut=SPLIT, delete_frac=DEL_FROZEN)),
    ("8x + delete 61%", dict(cadence_cut=SPLIT, delete_frac=DEL_WIDE)),
    ("8x + delete 61% + secular 15x", dict(cadence_cut=SPLIT, delete_frac=DEL_WIDE, secular=SECULAR[0])),
]:
    rc = required_cost(**kw)
    note(f"  {name:34s} {rc*1e6:8.1f} us  = {rc/49e-9:7.0f}x the 49ns floor midpoint")

note("")
note("# The crest (genesis phase-lock), clamp law t = N*C/0.72 (4093)")
for n, c in [(1e6, C_X86), (3e5, C_X86), (1e9, C_X86), (1e9, C_M1)]:
    t = n * c / FRAME
    note(f"  N={n:.0e} cost={c*1e6:.1f}us: {t:,.0f} s of clamped delivery per {INTERVAL:,.0f}-s interval"
         f"{' (measured 69 s at 10^6 x86, 4093)' if n == 1e6 else ''}")
note("")
note("# Self-consistency of the anchors")
note(f"  rate x interval = {RATE*INTERVAL:.4f} kicks/body/interval (the law: one kick per body per")
note(f"  doll-grid interval; belt_first on this box: belt p50 14072 x 2 = {14072*2} s vs {INTERVAL} s recorded)")
note(f"  the closure product: cost/cadence_cut x (1-delete) <= {required_cost()*1e6:.2f} us at shipped")
note(f"  cadence — today's {C_X86*1e6:.0f} us needs a x{C_X86/required_cost():.0f} lever, not x{C_X86/49e-9:.0f} to the floor")


note("")
note("# Encounters at 10^9, contiguous belt, averaged cadence (cores)")
g_lo, g_hi = ENC_BASE[0]*ENC_GATE[0], ENC_BASE[1]*ENC_GATE[1]
note(f"  cube cell (1738):                {ENC_BASE[0]:.0f}-{ENC_BASE[1]:.0f}")
note(f"  + quantum gate (277d, silver):   {g_lo:.0f}-{g_hi:.0f}   -> closes? {g_lo <= BUDGET}")
note(f"  + birth-constant routing (f0a2, awaiting grade): {ENC_ROUTE[0]}-{ENC_ROUTE[1]}  -> closes? {ENC_ROUTE[1] <= BUDGET}")

note("")
note("# Memory at 10^9 against the ~6 GB (48-bit/body) budget")
for name, (lo, hi) in MEM.items():
    gb = lambda b: N * b / 8.0 / 1e9
    note(f"  {name:52s} {lo:6.1f}-{hi:6.1f} bits -> {gb(lo):5.2f}-{gb(hi):5.2f} GB  fits? {gb(hi) <= 6.0}")
note(f"  shipped live plateau (b30b): {SHIPPED_LIVE_B[0]:.0f}-{SHIPPED_LIVE_B[1]:.0f} B/body -> "
     f"{N*SHIPPED_LIVE_B[0]/1e9:.0f}-{N*SHIPPED_LIVE_B[1]/1e9:.0f} GB")
note(f"  hot set only (a11b/ba64): {HOT_KB/1e3:.1f} kB x {HOT_N[0]:.0e}-{HOT_N[1]:.0e} = "
     f"{HOT_KB*HOT_N[0]/1e6:.0f}-{HOT_KB*HOT_N[1]/1e6:.0f} MB")
wall = (6.0e9/SHIPPED_LIVE_B[1], 8.0e9/SHIPPED_LIVE_B[0])
note(f"  the ladder's memory wall from the plateau alone: 6-8 GB / {SHIPPED_LIVE_B[0]:.0f}-{SHIPPED_LIVE_B[1]:.0f} B "
     f"= {wall[0]:.2e}-{wall[1]:.2e} bodies (measured 1.2-1.65e6, nladder)")

# ---- verdicts ---------------------------------------------------------------
note("")
note("# Verdicts")
v_req = required_cost(cadence_cut=SPLIT, delete_frac=DEL_WIDE)
note(f"V1 with ONLY measured levers (8x split + widened delete), the kick cost required to fit\n"
     f"   4 cores at 10^9 rtf 100 is {v_req*1e6:.0f} us = {v_req/49e-9:.0f}x the floor: the 42-56 ns floor is\n"
     f"   NOT on the 10^9 critical path (kick cost and cadence are redundant levers).")
note(f"V2 at the floor, even shipped cadence fits: {stream_cores(49e-9):.2f} cores.")
note(f"V3 the graded encounter levers leave 62-571 cores (277d's own composition; recomputed here")
note(f"   {g_lo:.0f}-{g_hi:.0f} from the cube base x 14-24x): the one CPU term whose closing")
note(f"   lever (routing) is ungraded.")
note(f"V4 memory: only the measured phase-locked program class (21-40 bits) fits 6 GB; every generic\n"
     f"   floor busts it; the shipped plateau is {N*SHIPPED_LIVE_B[0]/1e9/6.0:.0f}x the whole budget.")

out = {
    "configs": {n: stream_cores(**kw) for n, kw in configs},
    "required_cost_us": {
        "shipped": required_cost()*1e6,
        "split8": required_cost(cadence_cut=SPLIT)*1e6,
        "split8_del385": required_cost(cadence_cut=SPLIT, delete_frac=DEL_FROZEN)*1e6,
        "split8_del61": required_cost(cadence_cut=SPLIT, delete_frac=DEL_WIDE)*1e6,
    },
    "floor_shipped_cadence_cores": stream_cores(49e-9),
    "crest_s": {"1e6": 1e6*C_X86/FRAME, "3e5": 3e5*C_X86/FRAME, "1e9_x86": 1e9*C_X86/FRAME, "1e9_m1": 1e9*C_M1/FRAME},
    "encounters_cores": {"cube": ENC_BASE, "gated": [g_lo, g_hi], "routed": ENC_ROUTE},
    "memory_gb": {k: [N*v[0]/8e9, N*v[1]/8e9] for k, v in MEM.items()},
    "ladder_wall_bodies": list(wall),
}
with open("ledger.json", "w") as f:
    json.dump(out, f, indent=1)
print("\nwrote ledger.json")
