#!/usr/bin/env python3
"""Measured control (was arithmetic in the author's dossier): the two news
mechanisms as real integer-array code, same event schedule, ops counted and
timed. No physics here -- this isolates the machinery the lens chooses
between.

  cursor design (the lens's build): per (body, source) a next-arrival
    integer; every kick tests all N*S entries. State: N*S words.
  cell design (the claim): per (cell, source, depth) a version ring; each
    news wave (epoch) tests cells*S entries; a kick reads its own cell's
    merged register inside the field fetch it already does (0 extra tests).
    State: cells*S*D words + one static lag table (rings^2*spokes int16,
    shared by the whole doll, c-independent).
"""
import numpy as np, time

M_RING, N_SPOKE, R0, R1 = 16, 128, 0.7, 50.0
RINGS = int(np.floor(M_RING * np.log2(R1 / R0))) + 1     # 99
CELLS = RINGS * N_SPOKE                                   # 12,672
S, D = 10, 4                                              # sources, ring depth

print(f"doll: {RINGS} rings x {N_SPOKE} spokes = {CELLS} cells; S={S} sources, depth {D}")
print(f"{'N':>9} {'cursor words':>13} {'cell words':>11} {'cell+tab words':>14} "
      f"{'state x':>8} {'tests/kick x':>12} {'cursor ms':>10} {'cell ms':>7}")
for N in (2**16, 2**20, 2**23):
    cursor = np.random.default_rng(1).integers(1, 2**31, size=(N, S), dtype=np.int32)
    cbuf = np.empty((N, S), dtype=bool)
    ringh = np.random.default_rng(2).integers(1, 2**31, size=(CELLS, S), dtype=np.int32)
    snew = np.random.default_rng(3).integers(1, 2**31, size=S, dtype=np.int32)
    rbuf = np.empty((CELLS, S), dtype=bool)
    now = np.int32(2**30)
    # time 20 sweeps each (kick sweep vs epoch sweep)
    t0 = time.perf_counter()
    for _ in range(20): np.less_equal(cursor, now, out=cbuf)
    t_cur = (time.perf_counter() - t0) / 20
    t0 = time.perf_counter()
    for _ in range(20): np.not_equal(ringh, snew[None, :], out=rbuf)
    t_cell = (time.perf_counter() - t0) / 20
    cur_w = N * S
    cell_w = CELLS * S * D
    tab_w = RINGS * RINGS * N_SPOKE // 2                  # int16 -> 4-byte words
    print(f"{N:>9} {cur_w:>13,} {cell_w:>11,} {cell_w+tab_w:>14,} "
          f"{cur_w/(cell_w+tab_w):>8.1f} {(N*S)/(CELLS*S):>12.1f} "
          f"{t_cur*1e3:>10.2f} {t_cell*1e3:>7.3f}")
print("\nwords = 4-byte int32 (table int16). A kick reads its cell's merged")
print("register inside the field fetch; epochs are the news waves (>=1 apart).")
