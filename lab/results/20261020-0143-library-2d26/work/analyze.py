import sys
BUD = 12.0
def load(p):
    rows = []
    for line in open(p):
        f, ms, ev, lag = line.split()
        rows.append((int(f), float(ms), int(ev), float(lag)))
    return [r for r in rows if r[0] >= 60]
def arm(p):
    r = load(p)
    ms = sorted(x[1] for x in r)
    p50 = ms[len(ms)//2]
    onset = next((i for i, x in enumerate(r) if x[1] > 3*BUD), None)
    slack_pre = sum(max(0.0, BUD - x[1]) for x in r[:onset]) if onset else None
    excess = sum(max(0.0, x[1] - BUD) for x in r)
    excess_post = sum(max(0.0, x[1] - BUD) for x in r[onset:]) if onset else 0.0
    slack_all = sum(max(0.0, BUD - x[1]) for x in r)
    # wave window: frames within 3x of onset frame whose ms > budget
    lag = [x[3] for x in r]
    return dict(p50=p50, onset=r[onset][0] if onset else None, slack_pre=slack_pre,
                excess=excess, slack_all=slack_all, lag_max=max(lag),
                lag_onset=lag[onset] if onset else None,
                lag_end=lag[-1], n=len(r), over=sum(1 for x in r if x[1] > BUD),
                ev_max=max(x[2] for x in r), ev_med=ms and sorted(x[2] for x in r)[len(r)//2])
for name, p in [("1e5 burn", "f100000_burn.txt"), ("2e5 burn", "f200000_burn.txt"), ("1e5 coast", "f100000_coast.txt")]:
    a = arm(p)
    cov = f"{a['slack_pre']/a['excess']:.3f}" if a["onset"] and a["excess"] else "-"
    frac = a["excess"]/a["slack_all"] if a["slack_all"] else float("inf")
    pre = f"{a['slack_pre']:.0f}" if a["onset"] is not None else "-"
    lag0 = f"{a['lag_onset']:.1f}" if a["onset"] is not None else "-"
    print(f"{name}: frames {a['n']} p50 {a['p50']:.2f} ({a['p50']/BUD:.2f} of budget) over {a['over']} "
          f"onset_frame {a['onset']} slack_pre {pre} ms excess {a['excess']:.0f} ms "
          f"coverage(slack_pre/excess) {cov} excess/total_slack {frac:.2f} "
          f"lag onset {lag0} max {a['lag_max']:.1f} end {a['lag_end']:.1f} s "
          f"events med {a['ev_med']} max {a['ev_max']}")
    # play-cadence price: at rtf 100 there is no structural cadence deficit, so the amortized
    # wave's player-felt price = the excess drained at budget: lag_s ~= excess/(BUD ms) * (1/60) s of wall
    if a["onset"] and a["excess"]:
        print(f"   play-cadence price: excess {a['excess']:.0f} ms drained at 12 ms/frame = {a['excess']/BUD:.0f} extra frames = {a['excess']/BUD/60:.1f} s of presented-time lag; prepay needs {a['slack_pre']/BUD:.0f} frames of ebb")
