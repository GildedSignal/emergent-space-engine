#!/usr/bin/env python3
"""The registered analysis: window rules + band checks from predictions.md, applied mechanically.
Arms: A' = 5e4 seed1 (ap_off_50k / ap_on_50k), B = 3e4 seed2 (b_off_30k_s2 / b_on_30k_s2),
C = the 1e5 wall (a_off_100k, and c_on_100k if flown)."""
import re, sys

R = "lab/results/20261019-1817-second-20261019-1656-quant-88e9-3eb3"

def series(path):
    out = []
    for ln in open(path):
        m = re.match(r"probe gs=(\d+) rss_mb=(\d+) hwm_mb=(\d+) held=(\d+) mints=(\d+) answers=(\d+) "
                     r"expired=(\d+) hist_gt1=(\d+) hist_total=(\d+) hist_max=(\d+) kicks=(\d+)", ln)
        if m:
            out.append([int(x) for x in m.groups()])
    return out

GS, RSS, HWM, HELD, MINTS, ANS, EXP, GT1, HIST, HMAX, KICKS = range(11)

def win(pts, a, b):
    """points with a <= gs <= b (values interpolated at the edges is unnecessary: registered
    windows are probe-aligned by construction; we take probes inside)."""
    return [p for p in pts if a <= p[GS] <= b]

def deltas(pts, col):
    return pts[-1][col] - pts[0][col], pts[-1][GS] - pts[0][GS]

def bursts(pts, thresh_per_5k, min_gap=50000):
    """intervals [gs_start, gs_end] whose per-5k hist gain >= thresh; merged when adjacent,
    and split when a gap > min_gap carries no qualifying interval. Returns list of (start, end)."""
    iv = []
    for i in range(len(pts) - 1):
        d = pts[i + 1][HIST] - pts[i][HIST]
        span = pts[i + 1][GS] - pts[i][GS]
        if span > 0 and d * 5000.0 / span >= thresh_per_5k:
            iv.append((pts[i][GS], pts[i + 1][GS], d))
    if not iv:
        return []
    merged = [[iv[0][0], iv[0][1], iv[0][2]]]
    for s, e, d in iv[1:]:
        if s - merged[-1][1] <= 5000:
            merged[-1][1] = e
            merged[-1][2] += d
        else:
            merged.append([s, e, d])
    return [(m[0], m[1], m[2]) for m in merged]

def report(name, pts, a, b):
    w = win(pts, a, b)
    if len(w) < 2:
        print(f"  {name}: NO WINDOW [{a},{b}] (probes {pts[0][GS]}..{pts[-1][GS]})")
        return None
    dh, span = deltas(w, HIST)
    dk, _ = deltas(w, KICKS)
    dr, _ = deltas(w, RSS)
    out = dict(name=name, a=w[0][GS], b=w[-1][GS], span=span, dh=dh, dk=dk,
               slope=dh / span * 1000, stream=dk / span * 1000, closure=dh / dk if dk else 0.0,
               rss_slope=dr / span * 1000, rss_end=w[-1][RSS], gt1_end=w[-1][GT1])
    print(f"  {name}: window [{out['a']},{out['b']}] span {span} gs | hist slope {out['slope']:.0f}/1k gs | "
          f"stream {out['stream']:.0f}/1k gs | closure {out['closure']:.4f} | rss slope {out['rss_slope']:.2f} MB/1k | "
          f"rss@end {out['rss_end']} MB | gt1@end {out['gt1_end']}")
    return out

ok = lambda cond: "PASS" if cond else "FAIL"

print("== Rung A' (5e4, seed 1): share law OFF=3242 ON=1687 ratio=1.922 ==")
off = series(f"{R}/work/ap_off_50k.log")
on = series(f"{R}/work/ap_on_50k.log")
bo = bursts(off, 15000)   # belt waves over locals (~7.3k/5k)
bn = bursts(on, 15000)
print(f"  OFF belt-wave bursts (>=15k/5k hist): {[(s, e) for s, e, _ in bo]}")
print(f"  ON  belt-wave bursts (>=15k/5k hist): {[(s, e) for s, e, _ in bn]}")
wa = report("OFF W_OFF", off, 18000, 108000)
w1s = bn[0][0] if bn else 110000
on_end = min(w1s - 2000 + 225100, on[-1][GS])
wb = report(f"ON W_ON (wave1@{w1s})", on, w1s - 2000, on_end)
if wa and wb:
    sr = wa["slope"] / wb["slope"]
    kr = wa["stream"] / wb["stream"]
    print(f"  A'1 OFF stream in [2920,3570]: {wa['stream']:.0f} -> {ok(2920 <= wa['stream'] <= 3570)}")
    print(f"  A'2 ON  stream in [1520,1860]: {wb['stream']:.0f} -> {ok(1520 <= wb['stream'] <= 1860)}")
    print(f"  A'3 closures >= 0.90: OFF {wa['closure']:.4f} -> {ok(wa['closure'] >= 0.90)}; "
          f"ON {wb['closure']:.4f} -> {ok(wb['closure'] >= 0.90)}")
    print(f"  A'4 slope ratio in [1.70,2.15] (S=8 falsifier >=4, share-dead <1.70): {sr:.3f} -> {ok(1.70 <= sr <= 2.15)}")
    print(f"  A'5 stream ratio in [1.73,2.11]: {kr:.3f} -> {ok(1.73 <= kr <= 2.11)}")
    # diagnostic: matched-window ratio (registered as a non-test)
    md = report("ON matched-diag", on, wa["a"], wa["b"])
    if md:
        print(f"  (diagnostic, not a test) matched-window slope ratio OFF/ON: {wa['slope']/md['slope']:.3f}")

print("== Rung B (3e4, seed 2), matched window [140k,245k] ==")
off2 = series(f"{R}/work/b_off_30k_s2.log")
on2 = series(f"{R}/work/b_on_30k_s2.log")
wb1 = report("OFF", off2, 140000, 245000)
wb2 = report("ON ", on2, 140000, 245000)
if wb1 and wb2:
    sr = wb1["slope"] / wb2["slope"]
    kr = wb1["stream"] / wb2["stream"]
    print(f"  B1 slope ratio in [1.50,2.10]: {sr:.3f} -> {ok(1.50 <= sr <= 2.10)}")
    print(f"  B2 closures >= 0.90: OFF {wb1['closure']:.4f} -> {ok(wb1['closure'] >= 0.90)}; "
          f"ON {wb2['closure']:.4f} -> {ok(wb2['closure'] >= 0.90)}")
    print(f"  B3 stream ratio in [1.43,1.75]: {kr:.3f} -> {ok(1.43 <= kr <= 1.75)}")
    print(f"  B4 OFF slope in [2070,2800]: {wb1['slope']:.0f} -> {ok(2070 <= wb1['slope'] <= 2800)}")

print("== Rung C (the 1e5 wall) ==")
c = series(f"{R}/work/a_off_100k.log")
if c:
    print(f"  C1 OFF(1e5): last probe gs={c[-1][GS]} rss={c[-1][RSS]} (base 238); "
          f"guard tripped at 38640 gs < wave 2 (~44k) -> {ok(c[-1][GS] < 44000)}")

print("== Extension (diagnostic, disclosed post-registration): OFF 5e4 flown to 200k to locate onset ==")
ext = series(f"{R}/work/ap_off_50k_long.log")
for a, b, tag in [(130000, 195000, "waves 6-8"), (140000, 180000, "checker's window")]:
    w = win(ext, a, b)
    dh, span = deltas(w, HIST)
    dk, _ = deltas(w, KICKS)
    dr, _ = deltas(w, RSS)
    print(f"  OFF ext [{w[0][GS]},{w[-1][GS]}] ({tag}): closure {dh/dk:.4f} | slope {dh/span*1000:.0f} | "
          f"stream {dk/span*1000:.0f} | rss slope {dr/span*1000:.2f} MB/1k | rss@end {w[-1][RSS]} MB")

print("== C2: ON(1e5) wall ==")
c2 = series(f"{R}/work/c_on_100k.log")
print(f"  ON(1e5): last probe gs={c2[-1][GS]} rss={c2[-1][RSS]} hist={c2[-1][HIST]} kicks={c2[-1][KICKS]} "
      f"(wave 1 expected ~106k; tripped pre-wave-1: {'YES' if c2[-1][GS] < 100000 else 'no'})")

print("== Onset-corrected A' (POST-HOC, disclosed: same bands, windows moved past the ~130k onset) ==")
wo = report("OFF [130k,190k]", ext, 130000, 190000)
wn = report("ON  [110k,315k]", on, 110001, 315030)
if wo and wn:
    print(f"  slope ratio: {wo['slope']/wn['slope']:.3f} (band [1.70,2.15], share 1.922) -> "
          f"{ok(1.70 <= wo['slope']/wn['slope'] <= 2.15)}")
    print(f"  stream ratio: {wo['stream']/wn['stream']:.3f} (band [1.73,2.11]) -> "
          f"{ok(1.73 <= wo['stream']/wn['stream'] <= 2.11)}")
    print(f"  closures: OFF {wo['closure']:.4f}, ON {wn['closure']:.4f} (>= 0.90) -> "
          f"{ok(wo['closure'] >= 0.9 and wn['closure'] >= 0.9)}")

print("== Rung C decomposition: the 1e5 wall is machinery, not bindings ==")
def guard_gs(path):
    for ln in open(path):
        m = re.search(r"guard: resident over \d+ MB at frame \d+, game (\d+) s", ln)
        if m:
            return int(m.group(1))
    return None

go, gn = guard_gs(f"{R}/work/a_off_100k.log"), guard_gs(f"{R}/work/c_on_100k.log")
for nm, path, g in [("OFF", f"{R}/work/a_off_100k.log", go), ("ON ", f"{R}/work/c_on_100k.log", gn)]:
    s = series(path)
    last = s[-1]
    mach = (last[RSS] - 238) * 1e6 - last[HIST] * 2100
    print(f"  {nm}: guard at {g} gs, last probe rss={last[RSS]} hist={last[HIST]} kicks={last[KICKS]} -> "
          f"machinery (rss - 238MB base - 2.1KB*hist) ≈ {mach/1e6:.0f} MB ≈ {mach/max(1,last[KICKS])/1e3:.1f} KB/kick")
print(f"  wall-life ratio ON/OFF at 1e5 = {gn/go:.2f}x (share-law stream ratio at 1e5: 2.63)")
