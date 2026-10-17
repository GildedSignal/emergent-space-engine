#!/usr/bin/env python3
"""20261017-0005-fermi-25ce — the 10^9 schedule (calendar) priced.

Forms priced (predictions.md P1-P4):
  (a) explicit per-body pending-event entries;
  (b) due-ordered materialisation (ring / causal-order layout);
  (c) per-frame rescan of the compressed store (nothing stored, phases derived);
  (d) group cursors per (doll, step, phase-class), stagger quantised to classes.

All engine constants are cited page constants (see dossier.md); nothing here re-measures
shipped binaries (the plane does not link on Linux without a patch; this is a float
replica in the lab's standing practice).

Usage: python3 fermi_calendar.py [--quick]
"""
import argparse
import math
import time

import numpy as np

# ---- cited constants (dossier.md "Anchors") -----------------------------------
INTERVAL_GS = 28_141.5          # game-s per belt event interval, measured (3294; e7ef 28,144)
RATE_SHIPPED = 3.55e-5          # events/body/game-s, measured stream (3294; 4c22 4.02e-5)
RATE_COMPOSED = 4.44e-6         # after BELT_SPLIT x8 + 61% delete (98cb, interval-measured)
EVENT_US_M1 = 29.3              # us per stream event on the M1 (4093/e7ef anchor)
EVENT_US_X86 = 50.0             # this class of box (4093)
RTF = 100.0                     # flying pace (4093)
FPS = 60.0
CORES = 4.0
MEM_GB = 6.0                    # budget (e7ef's composition frame)
BW_M1 = 60e9                    # B/s, the board's M1 number
N9 = 1e9
PHASE_LOCKED_BITS = (21, 40)    # program classes, measured (e7ef composition)
ID_BITS = math.ceil(math.log2(N9))
PHASE_BITS = math.ceil(math.log2(INTERVAL_GS))   # tick-resolution due within the interval


def splitmix64(x: np.ndarray) -> np.ndarray:
    """Vectorised splitmix64 finaliser (the shipped stagger is 'hash(id)-derived')."""
    x = x.astype(np.uint64, copy=True)
    for shift, const in ((30, 0xBF58476D1CE4E5B9), (27, 0x94D049BB133111EB), (31, 0x23E6D1C2D3A0B49F)):
        x ^= (x >> np.uint64(shift))
        x = (x * np.uint64(const)) & np.uint64(0xFFFFFFFFFFFFFFFF)
    x ^= (x >> np.uint64(33))
    return x


def frames_per_interval(interval_gs: float) -> float:
    gs_per_frame = RTF / FPS
    return interval_gs / gs_per_frame


def batch_budget() -> float:
    frame_s = 1.0 / FPS
    return CORES * frame_s / (EVENT_US_M1 * 1e-6)


# ---- P3: the memory arithmetic ------------------------------------------------
def p3_memory():
    print("== P3: the schedule's forms at 10^9 ==")
    b = batch_budget()
    print(f"frame event budget: {CORES:.0f} cores x {1000/FPS:.2f} ms / {EVENT_US_M1} us"
          f" = {b:,.0f} events/frame")
    ent = ID_BITS + 24 + 3, ID_BITS + 16 + 27          # (id, due, packed link) .. (id, due, ptr)
    for lo, hi in (ent,):
        print(f"(a) explicit per-body entries: {lo/8:.1f}-{hi/8:.1f} B/body"
              f" -> {N9*lo/8/1e9:.1f}-{N9*hi/8/1e9:.1f} GB  (budget {MEM_GB:.0f} GB):"
              f" {'BUSTS' if N9*lo/8/1e9 > MEM_GB else 'fits'}")
    ring_idx = ID_BITS + PHASE_BITS
    print(f"(b) due-ordered ring index: id {ID_BITS} b + phase {PHASE_BITS} b ="
          f" {ring_idx} b/body -> {N9*ring_idx/8/1e9:.2f} GB on top of the program store;"
          f" inlined (phase+program) {PHASE_BITS + PHASE_LOCKED_BITS[0]}-"
          f"{PHASE_BITS + PHASE_LOCKED_BITS[1]} b ->"
          f" {N9*(PHASE_BITS+PHASE_LOCKED_BITS[0])/8/1e9:.1f}-"
          f"{N9*(PHASE_BITS+PHASE_LOCKED_BITS[1])/8/1e9:.1f} GB but phase sorting destroys"
          f" the birth-compressible classes (0.126-2.4 b)")
    shannon_perm = (math.lgamma(N9 + 1) / math.log(2)) / 8 / 1e9  # log2(N!) bytes, GB
    print(f"    Shannon floor of any due-ordering of distinguishable bodies:"
          f" log2(N!) = {shannon_perm:.1f} GB")
    classes = N9 / b
    for mult, tag in ((1, "global"), (100, "x100 doll/step/cell fan-out")):
        gb = classes * 4 * mult / 1e9
        print(f"(d) cursors, >= N/budget = {classes:,.0f} classes x 4 B ({tag}):"
              f" {gb*1e3:.1f} MB = {100*gb/MEM_GB:.2f}% of {MEM_GB:.0f} GB")
    return b


# ---- P4: independent ledger cross-check ---------------------------------------
def p4_ledger():
    print("== P4: ledger cross-check (independent re-derivation) ==")
    for name, rate, interval in (("shipped", RATE_SHIPPED, INTERVAL_GS),
                                 ("composed (split x8 + 61% delete)", RATE_COMPOSED, INTERVAL_GS * 8)):
        ev_per_gs = rate * N9
        cores_m1 = ev_per_gs * RTF * EVENT_US_M1 * 1e-6
        cores_x86 = ev_per_gs * RTF * EVENT_US_X86 * 1e-6
        per_interval = rate * interval  # events/body/interval (must be ~1)
        print(f"{name}: rate {rate:.3e} ev/B/gs x 10^9 = {ev_per_gs:,.0f} ev/gs;"
              f" {cores_m1:.1f} cores M1 / {cores_x86:.1f} x86 at rtf {RTF:.0f};"
              f" rate x interval = {per_interval:.3f} ev/B/interval")


# ---- P1: rescan cost (form c) --------------------------------------------------
def rescan_pass(ids: np.ndarray, j: int, due_lo: int, due_hi: int) -> int:
    """One streaming pass: hash -> phase class -> due-in-window filter.

    Streams in 2^20 chunks (memory-bounded; the engine would stream the same way).
    """
    hits = 0
    for s in range(0, ids.size, 1 << 20):
        c = ids[s : s + (1 << 20)]
        h = splitmix64(c)
        phase = (h >> np.uint64(64 - j)).astype(np.int64)
        hits += int(np.count_nonzero((phase >= due_lo) & (phase < due_hi)))
    return hits


def p1_rescan(sizes):
    print("== P1: per-frame rescan of the compact store (form c) ==")
    budget_s = 1.0 / FPS
    for n in sizes:
        ids = np.arange(n, dtype=np.uint64)
        j = 12  # 4096 classes; window = a few classes (a frame's share)
        best = None
        for _ in range(5):
            t0 = time.perf_counter()
            hits = rescan_pass(ids, j, 0, 4)
            dt = time.perf_counter() - t0
            best = dt if best is None else min(best, dt)
        ns_per_body = best / n * 1e9
        gb = n * 8 / 1e9
        print(f"N={n:>10,}: {best*1e3:8.2f} ms/pass ({gb:.2f} GB store),"
              f" {ns_per_body:5.2f} ns/body, hits={hits:,};"
              f" at 10^9: {ns_per_body*1e9*1e-9:.1f} s = {ns_per_body*1e9/budget_s:,.0f}"
              f" frames of budget -> {'DEAD' if ns_per_body * 1e9 > budget_s else 'alive'}")
    bw = 8 / (BW_M1 / N9 / 1e9 * 1e9)  # bytes-bound floor at M1 bandwidth
    print(f"bandwidth floor (M1 {BW_M1/1e9:.0f} GB/s, 8 B/body): {N9*8/BW_M1:.2f} s/pass"
          f" = {N9*8/BW_M1/budget_s:,.0f} frames of budget -> DEAD regardless of compute")


# ---- P2: the class dial (form d) -----------------------------------------------
def p2_classes(n=1_000_000, seed=1):
    """The class dial on the composed cadence: spread N dues over one interval.

    Mean batch/frame is fixed by cadence (mu = N/frames); classes only bound the
    maximum. A frame receives ~K/F classes spread round-robin on the frame grid;
    as K/F grows the per-frame sum CLT-tightens around mu.
    """
    print(f"== P2: quantised phase classes at N={n:,} (one composed interval) ==")
    frames = int(frames_per_interval(INTERVAL_GS * 8))   # composed: split x8
    mu = n / frames
    bar = batch_budget() * n / N9
    ids = np.arange(n, dtype=np.uint64)
    h = splitmix64(ids + np.uint64(seed * 7919))
    print(f"frames/interval={frames:,}  mean events/frame={mu:,.1f}  bar={bar:,.1f}"
          f"  (at 10^9: mu={N9/frames:,.0f} vs bar {batch_budget():,.0f}"
          f" = {N9/frames/batch_budget():.2f}x the 4-core bar, the known overage)")
    for tag, kf in (("comb (K=1)", 0.0), ("K=512 (pre-registered)", -512.0), ("K=F/10", 0.1),
                    ("K=10F", 10.0), ("K=100F", 100.0)):
        if kf == 0:
            print(f"{tag:10s}: whole population due in one frame ({n:,} vs bar {bar:,.0f})"
                  f" -> FAILS (the measured comb/crest, 4c22/9e75)")
            continue
        if kf < 0:
            j = 9  # the pre-registered arm: 512 classes, class size ~N/512
        else:
            j = max(1, (int(frames * kf) - 1).bit_length())   # hash buckets >= K
        slots = 1 << j
        phase = (h >> np.uint64(64 - j)).astype(np.int64)
        cc = np.bincount(phase, minlength=slots)
        fb = np.bincount(phase % frames, minlength=frames)
        mem9 = slots * 4 / 1e9
        print(f"{tag:10s}: K={slots:>9,} (class~{n/slots:7.1f}, max class"
              f" {cc.max():7.0f} = {cc.max()/(n/slots):4.2f}x mean); frame batch"
              f" mean={fb.mean():7.1f} p99={np.percentile(fb, 99):7.1f}"
              f" max={fb.max():7.1f} ({fb.max()/fb.mean():5.2f}x mean) vs bar {bar:,.0f}"
              f" -> {'FAILS' if fb.max() > bar else 'holds'}; 10^9 cursors {mem9*1e3:6.1f} MB"
              f" ({100*mem9/MEM_GB:.2f}% of {MEM_GB:.0f} GB)")
    # concentration over independent seeds at the working point K=10F
    j = max(1, (int(frames * 10) - 1).bit_length())
    mx = []
    for s in range(8):
        hh = splitmix64(ids + np.uint64((s + 7) * 7919))
        fb = np.bincount((hh >> np.uint64(64 - j)).astype(np.int64) % frames,
                         minlength=frames)
        mx.append(fb.max() / fb.mean())
    mx = np.array(mx)
    print(f"concentration, 8 seeds at K=10F: max/mean {mx.min():.3f}-{mx.max():.3f}"
          f" (prediction <= 1.25; CLT sigma of a frame sum ~"
          f" {math.sqrt(n/frames)/(n/frames):.3f} of mean)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    a = ap.parse_args()
    p3_memory()
    p4_ledger()
    p1_rescan([1_000_000] if a.quick else [1_000_000, 10_000_000])
    p2_classes()
