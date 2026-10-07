#!/usr/bin/env python3
"""Fermi budget at 1e9 bodies, anchored on the shipped plane measured on this box (2026-10-07).

Measured anchors (lab/results/20261007-1843-fermi-1feb/work/):
  bench rtf100 s20  members=48 : 6791 events / 2000 game-s / 71 bodies; belt-like (kicks+opens+boundaries) 2146
  bench rtf100 s15  members=400: 22834 events / 1500 game-s / 417 bodies; belt-like 11563
  kick-bench rtf100: made median 35.2 us, leavers median 90.1 us, p99 449 us; exact memo hit rate 0.0
  bytes_per_body today: 5067 B (plain store, no population programs)
Constants from the docs: tube 16 B (law.md); smooth-belt program 0.126 bits/body (gold components-98bc);
M1: 8 GB, ~60 GB/s, 4P+4E cores (~6 effective threads), board headline "~190 cores for 1e9 at today's rates".
"""
M = dict(
    k_belt = 11563/1500/417,          # belt-like events per body per game-s (400 members; 48 gives 0.0151)
    k_hot  = 22834/1500/417,          # with the fleet battle slices included
    us_kick_today = 87.5,             # all-kicks median, this box (recompile on every kick)
    us_kick_designed = 3.0,           # law.md jet+re-anchor: 0.05 compiles/kick x ~35 us + kick ~1 us
    N = 1e9,
    bytes_body_today = 5067,
    bits_program = 0.126,             # per body, smooth belt
    ram_bits = 4e9*8,                 # half of 8 GB for body state
    bw_GB_s = 60.0,
    bytes_per_event = 256,            # tube + plan item + queue + memo touch, bracket 128-512
    threads = 6,                      # M1 4P+4E effective
)
g = lambda **kw: {**M, **kw}

def compute(m, k, us):
    ev = m['N']*k                      # events per game-second at 1e9
    core_s = ev*us/1e6                 # core-seconds per game-second
    rtf_max = m['threads']/core_s      # wall keeps up with game at this rtf (full tilt)
    return ev, core_s, rtf_max

def report(name, m, k, us):
    ev, cs, rtf = compute(m, k, us)
    print(f"{name:34s} {ev:9.3g} ev/game-s {cs:8.3g} core-s/game-s  rtf_max(M1~6thr)={rtf:8.3g}")
    return ev, cs, rtf

print("== Term C: compute at 1e9 (events/s x cost) ==")
report("hot scene, today's 87.5us kick", M, M['k_hot'], M['us_kick_today'])
report("hot scene, designed 3us kick", M, M['k_hot'], M['us_kick_designed'])
report("belt-like only, today", M, M['k_belt'], M['us_kick_today'])
report("belt-like only, designed", M, M['k_belt'], M['us_kick_designed'])
# board's headline check: cores for rtf 1, hot + today
ev, cs, _ = compute(M, M['k_hot'], M['us_kick_today'])
print(f"  board check: hot+today needs {cs:.3g} core-s per game-s -> {cs/M['threads']:.3g} 'cores' at 6 threads (board said ~190)")

print()
print("== Term M: memory / H_live ==")
print(f"today's store   : {M['bytes_body_today']:.4g} B/body x 1e9 = {M['bytes_body_today']*M['N']/1e15:.3g} PB  ({M['bytes_body_today']*M['N']/8e9:.3g}x the 8 GB)")
print(f"plain tubes only: 16 B x 1e9 = 16 GB = {16e9/8e9:.1f}x the 8 GB (no programs, no scars)")
print(f"belt programs   : 0.126 bits/body x 1e9 = {M['bits_program']*M['N']/8/1e6:.4g} MB per billion")
budget_bits_body = M['ram_bits']/M['N']
print(f"state budget    : {budget_bits_body:.4g} bits/body total; minus program floor -> ~{budget_bits_body-M['bits_program']:.4g} bits/body for live distinctions")
for scar_bits in (16, 64):
    for name, k in (("hot", M['k_hot']), ("belt-like", M['k_belt'])):
        create = k*scar_bits                       # bits/body/game-s created
        fill_s = (budget_bits_body-M['bits_program'])/create
        churn = create*M['N']/8/1e6                # MB/game-s the allocator must reabsorb at steady state
        print(f"  scar {scar_bits:2d} bits, {name:9s}: create {create:8.3g} bits/body/game-s; fills the budget in {fill_s:8.3g} game-s; steady-state reabsorption {churn:8.3g} MB/game-s")

print()
print("== Term B: bandwidth at 1e9 ==")
for name, k in (("hot", M['k_hot']), ("belt-like", M['k_belt'])):
    gb_game_s = M['N']*k*M['bytes_per_event']/1e9
    for rtf in (1, 10, 100):
        print(f"  {name:9s} rtf {rtf:3d}: {gb_game_s*rtf:8.3g} GB/s wall  ({gb_game_s*rtf/M['bw_GB_s']*100:8.3g}% of 60 GB/s)", end="")
    print()
