import re
R = "lab/results/20261019-1656-quant-88e9"
def series(p):
    out = []
    for ln in open(p):
        m = re.match(r"probe gs=(\d+) rss_mb=(\d+) hwm_mb=(\d+) held=(\d+) mints=(\d+) answers=(\d+) expired=(\d+) hist_gt1=(\d+) hist_total=(\d+) hist_max=(\d+)", ln)
        if m:
            out.append([int(x) for x in m.groups()])
    return out
def fit(pts, a, b, col):
    xs = [p[0] for p in pts if a <= p[0] <= b]; ys = [p[col] for p in pts if a <= p[0] <= b]
    n = len(xs); mx = sum(xs)/n; my = sum(ys)/n
    return sum((x-mx)*(y-my) for x, y in zip(xs, ys))/sum((x-mx)**2 for x in xs)*1000
def at(pts, g, col):
    lo = max((p for p in pts if p[0] <= g), key=lambda p: p[0]); hi = min((p for p in pts if p[0] >= g), key=lambda p: p[0])
    return lo[col] if lo[0] == hi[0] else lo[col] + (hi[col]-lo[col])*(g-lo[0])/(hi[0]-lo[0])
def kickrate(p):
    for l in open(p):
        if l.startswith("ladder:"):
            return float(re.search(r"kicks_per_body_gs=(\S+)", l).group(1))
off = series(f"{R}/work/off_200k.log"); on = series(f"{R}/work/on_260k.log")
ko, kn = kickrate(f"{R}/work/off_200k.log"), kickrate(f"{R}/work/on_260k.log")
print(f"OFF hist slope/1k = {fit(off,140000,245000,8):.0f}  (kick stream/1k gs {ko*30028*1000:.0f})  rss slope = {fit(off,140000,245000,1):.2f} MB")
print(f"ON  hist slope/1k = {fit(on,140000,245000,8):.0f}  (kick stream/1k gs {kn*30028*1000:.0f})  rss slope = {fit(on,140000,245000,1):.2f} MB")
print(f"slope ratio = {fit(off,140000,245000,8)/fit(on,140000,245000,8):.2f}x   rss ratio = {fit(off,140000,245000,1)/fit(on,140000,245000,1):.2f}x")
print(f"RSS@245k: OFF {at(off,245000,1):.0f} MB  ON {at(on,245000,1):.0f} MB   hist@245k: OFF {at(off,245000,8):.0f}  ON {at(on,245000,8):.0f}")
print(f"hist@174k OFF {at(off,174000,8):.0f} (f80a OFF 241,552); gt1@174k {at(off,174000,7):.0f} (f80a 30,064)")
print(f"channel-1 control held@245k: OFF {at(off,245000,3):.0f}  ON {at(on,245000,3):.0f}")
print(f"B/binding RSS = {(at(off,245000,1)-at(on,245000,1))*1e6/(at(off,245000,8)-at(on,245000,8)):.0f}")
