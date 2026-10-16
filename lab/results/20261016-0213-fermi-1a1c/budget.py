#!/usr/bin/env python3
"""The 10^9 budget of the flyable plane (merged main), assembled. Fermi lens run 20261016-0213-fermi-1a1c.

Every constant is either measured by this run's flights (raw/*.txt, this Linux box — orders of
magnitude only) or an M1 anchor quoted from artifacts/runs/nladder/ladder.txt (after2, 14 Oct)
and the lab wiki, with the run id named in the table. The laws are stated per term; the script
prints each term's break-N (where it first crosses its budget) and its gap at N = 10^9.

Machine model (HANDOFF, the M1): 8 GB unified (~6 GB usable for the sim; gate N1 uses 4 GiB),
~4 sustained cores for the engine, frame budget 12 ms x 60 fps = 0.72 core of engine time, rtf 100.
"""
import re, sys, json, pathlib

R = pathlib.Path(__file__).parent
raw = R / "raw"

def ladder_line(path):
    txt = path.read_text()
    m = re.search(r"^ladder: (.*)$", txt, re.M)
    if not m:
        return None
    d = {}
    for kv in m.group(1).split():
        k, _, v = kv.partition("=")
        d[k] = v
    return d

def worst_frames(path):
    txt = path.read_text()
    m = re.search(r"worst frames \(frame, ms, events, lag s\): (.*)", txt)
    if not m:
        return []
    return [tuple(float(x) for x in t) for t in re.findall(r"\((\d+), ([\d.]+), (\d+), ([\d.]+)\)", m.group(1))]

def belt_first(path):
    txt = path.read_text()
    m = re.search(r"belt: \d+ bodies, first item \(game s\) min (\d+) p01 (\d+) p50 (\d+) p99 (\d+) max (\d+)", txt)
    return [float(m.group(i)) for i in (1, 2, 3, 4, 5)] if m else None

# ---- this run's flights (Linux box, shared; orders of magnitude) ----
short = {n: ladder_line(raw / f"short_n{n}.txt") for n in (1000, 10000, 100000)}
wave = {n: ladder_line(raw / f"wave_n{n}.txt") for n in (10000, 100000)}
worst = {n: worst_frames(raw / f"wave_n{n}.txt") for n in (10000, 100000)}
bf = {n: belt_first(raw / f"belt_first_1e{n}.txt") for n in (4, 5)}

rows = {}
for n, d in short.items():
    if d:
        rows[f"short_{n}"] = dict(b_per_body=float(d["b_per_body"]), build_us=float(d["build_s"]) / float(d["bodies"]) * 1e6,
                                   p50_ms=float(d["p50_ms"]), p99_ms=float(d["p99_ms"]), max_ms=float(d["max_ms"]),
                                   ev_b_gs=float(d["events_per_body_gs"]), view_ms=float(d["view_ms"]))
for n, d in wave.items():
    if d:
        w = worst[n]
        peak_ms, peak_ev = max((x[1] for x in w), default=0.0), max((x[2] for x in w), default=0.0)
        # us/event: from the worst wave frames (ms, events) pairs
        per_event = [ms / ev for (_, ms, ev, _) in w if ev >= 20]
        rows[f"wave_{n}"] = dict(p50_ms=float(d["p50_ms"]), p99_ms=float(d["p99_ms"]), max_ms=float(d["max_ms"]),
                                 peak_ev_frame=peak_ev, peak_ms=peak_ms,
                                 us_event=(sorted(per_event)[len(per_event)//2] * 1e3 if per_event else None),
                                 ev_b_gs=float(d["events_per_body_gs"]), over=int(d["over"]), lag=float(d["lag_s"]),
                                 foot_end_mb=float(d["foot_end_mb"]), b_per_body=float(d["b_per_body"]))
for n, v in bf.items():
    if v:
        rows[f"belt_first_1e{n}"] = dict(min=v[0], p01=v[1], p50=v[2], p99=v[3], max=v[4], width=v[4] - v[0])

# ---- constants: this run (L) and M1 anchors (Q, quoted) ----
b_body_L = rows["short_100000"]["b_per_body"]          # B/body standing, this box
b_body_M1 = 2443.0                                     # Q ladder.txt after2 @1e6
build_us_L = rows["short_100000"]["build_us"]
build_us_M1 = 28.7                                     # Q ladder.txt after2 (28.3-31.5 @1e6)
us_event_L = rows["wave_100000"]["us_event"]                # this box, budget-free wave frames (median of worst-5)
us_event_M1 = 29.3                                          # Q ladder.txt after2 (12.0 ms / 409 events)
W = rows["belt_first_1e5"]["width"]                         # wave window width, game-s (N-independent: 1e4 and 1e5 agree)
peak_ev_1e5 = rows["wave_100000"]["peak_ev_frame"]          # true (budget-free) peak events/frame at 1e5, this run
cinder_s = 88 * 86400
r_doll = 128 / cinder_s                                     # kicks/body/game-s, the doll's own law (ladder.txt)
r_plateau = 8.3e-5                                          # ed3a's measured plateau at 3e5 (25 events/game-s)
r_residue = 4.5e-5                                          # this run: post-wave event residue at 1e5 (~4-5 events/game-s)
view_us_M1 = 13.8                                           # Q ladder.txt after2 warm gather (1,377 ms at 1e5)
scan_b_body = 113.0                                         # Q taleb-51b7: marginal RSS per held scan, B/body
scan_answer_ms_1e5 = 170.0                                  # Q taleb-51b7: 150-190 ms per answer at 1e5
b_post_kick = 475e6 / 1e5                                   # this run: standing B/body after the wave (peak footprint)

# machine (the M1, HANDOFF): 8 GB unified ~6 usable, ~4 sustained cores, 12 ms x 60 fps, rtf 100
RAM, CORES, FRAME, FPS, RTF = 6e9, 4.0, 12e-3, 60.0, 100.0
gpf = RTF / FPS                                             # game-s advanced per wall frame
N = 1e9

# ---- term laws (M1-projected constants; this box's alongside for order-checks) ----
f1_cap_ev = FRAME / (us_event_M1 * 1e-6)                     # events a 12-ms frame can process on the M1 (~410)
wave_peak_break = 1e5 * f1_cap_ev / peak_ev_1e5              # F1-letter break: true peak crosses 12 ms (peak sublinear in N -> upper bound)
wave_peak_1e9_M1 = N / 1e5 * peak_ev_1e5 * us_event_M1 * 1e-6 / FRAME
wave_thru_break = W * gpf * FRAME / (us_event_M1 * 1e-6)     # mean wave work fills the window's frames (lag grows past)
steady = {}
for tag, r in (("doll", r_doll), ("residue", r_residue), ("plateau", r_plateau)):
    cores_M1 = N * r * RTF * us_event_M1 * 1e-6
    steady[tag] = dict(rate_b_gs=r, cores_M1=cores_M1, break_n_4core=N * CORES / cores_M1,
                       cores_thisbox=N * r * RTF * (us_event_L or 49.0) * 1e-6)
mem = dict(break_n_6gb=RAM / b_body_M1, break_n_4gib=4e9 / b_body_M1, break_n_post_kick=RAM / b_post_kick,
           over_1e9=N * b_body_M1 / RAM, over_1e9_post_kick=N * b_post_kick / RAM)
build = dict(core_hours_1e9=N * build_us_M1 * 1e-6 / 3600, break_n_60s=60.0 / (build_us_M1 * 1e-6),
             us_body_thisbox=build_us_L)
scan = dict(break_n_one_held=RAM / scan_b_body, over_1e9=N * scan_b_body / RAM,
            answer_s_1e9=scan_answer_ms_1e5 * 1e-3 * N / 1e5)
view = dict(break_n_16ms=16.7e-3 / (view_us_M1 * 1e-6), over_1e9=N * view_us_M1 * 1e-6 / 16.7e-3,
            us_body_thisbox=rows["short_100000"]["view_ms"] * 1e3 / 1e5)

composed = dict(stagger=16.7, kick_lever=us_event_M1 / 0.11,
                wave_peak_1e9_both=wave_peak_1e9_M1 / 16.7 / (us_event_M1 / 0.11),
                steady_plateau_cores_keyarm=steady["plateau"]["cores_M1"] / (us_event_M1 / 0.11),
                steady_doll_cores_keyarm=steady["doll"]["cores_M1"] / (us_event_M1 / 0.11),
                mem_1e9_gb_driven_floor=N * 126 / 8 / 1e9, mem_1e9_gb_phase_locked=N * 40 / 8 / 1e9)

out = {
    "this_run": rows,
    "constants": dict(us_event_L=us_event_L, us_event_M1=us_event_M1, W_game_s=W, peak_ev_1e5=peak_ev_1e5,
                      f1_cap_ev_M1=f1_cap_ev, b_body_M1=b_body_M1, b_body_thisbox=b_body_L,
                      b_post_kick=b_post_kick, build_us_M1=build_us_M1, build_us_thisbox=build_us_L,
                      r_doll=r_doll, r_residue=r_residue, r_plateau=r_plateau, view_us_M1=view_us_M1),
    "at_1e9": dict(wave_peak=dict(break_n=wave_peak_break, over_budget=wave_peak_1e9_M1),
                   wave_throughput=dict(break_n=wave_thru_break,
                                        over_budget=N * us_event_M1 * 1e-6 / (W * gpf * FRAME)),
                   steady_stream=steady, memory=mem, build=build, scan=scan, view=view,
                   h_live_bits_s=21.0),
    "composed_end_state": composed,
}
(R / "budget.json").write_text(json.dumps(out, indent=1, default=str))

print("constants:", json.dumps(out["constants"], indent=1))
print()
hdr = f"{'term (break-N, M1-projected)':34} {'break-N':>10} {'gap at 1e9':>11}  law / note"
print(hdr); print("-" * len(hdr))
rows_t = [
    ("view gather (page-side)", view["break_n_16ms"], view["over_1e9"], f"warm {view_us_M1} us/body M1 (this box {view['us_body_thisbox']:.1f}), exp 1.0"),
    ("wave, F1 letter (peak)", wave_peak_break, wave_peak_1e9_M1, f"true peak {peak_ev_1e5:.0f} ev/frame at 1e5 budget-free (after2's ~409 was the 12-ms cap); ES_STAGGER /16.7"),
    ("memory, 4 GiB gate", mem["break_n_4gib"], mem["over_1e9"], f"{b_body_M1:.0f} B/body standing; post-first-kick {b_post_kick:.0f} B -> break {mem['break_n_post_kick']:.2g}"),
    ("wave, throughput (lag)", wave_thru_break, N * us_event_M1 * 1e-6 / (W * gpf * FRAME), f"W={W:.0f} game-s, {us_event_M1} us/event M1"),
    ("build (60 s screen)", build["break_n_60s"], build["core_hours_1e9"], f"{build_us_M1} us/body M1 (this box {build_us_L:.1f}); core-h at 1e9"),
    ("steady stream (doll law)", steady["doll"]["break_n_4core"], steady["doll"]["cores_M1"], f"{steady['doll']['cores_M1']:.0f} cores at 1e9 rtf 100 (this box {steady['doll']['cores_thisbox']:.0f})"),
    ("steady stream (residue)", steady["residue"]["break_n_4core"], steady["residue"]["cores_M1"], f"{steady['residue']['cores_M1']:.0f} cores (this box {steady['residue']['cores_thisbox']:.0f}); rate {r_residue:.1e}/b/game-s"),
    ("steady stream (plateau)", steady["plateau"]["break_n_4core"], steady["plateau"]["cores_M1"], f"{steady['plateau']['cores_M1']:.0f} cores (this box {steady['plateau']['cores_thisbox']:.0f}); ed3a rate"),
    ("player scan (one held)", scan["break_n_one_held"], scan["over_1e9"], f"answer {scan['answer_s_1e9']:.0f} s at 1e9"),
]
for name, brk, gap, law in sorted(rows_t, key=lambda t: t[1]):
    print(f"{name:34} {brk:10.3g} {gap:11.3g}  {law}")
print()
print("composed end state (ES_STAGGER 16.7x, kick at b29a key arm 0.11 us):")
print(f"  wave peak at 1e9: {composed['wave_peak_1e9_both']:.2f} x the 12 ms budget")
print(f"  steady stream at 1e9: {composed['steady_doll_cores_keyarm']:.2f}-{composed['steady_plateau_cores_keyarm']:.2f} cores (of ~4)")
print(f"  memory at 1e9: {composed['mem_1e9_gb_driven_floor']:.1f} GB (driven-belt 126-bit floor) / {composed['mem_1e9_gb_phase_locked']:.1f} GB (phase-locked 40 bits) vs 6-8 GB")
