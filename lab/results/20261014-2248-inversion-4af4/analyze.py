#!/usr/bin/env python3
"""Parse wavetrain logs: wave windows, the memory trajectory at each wave, catalogue, history, lag."""
import re
import sys


def parse(path):
    w, h, head, end = [], [], {}, {}
    for line in open(path):
        if line.startswith("wavetrain") or line.startswith("train:") or line.startswith("end:") or line.startswith("digest:"):
            head.setdefault(line.split(":")[0], line.strip())
        if line.startswith("w:"):
            d = dict(kv.split("=") for kv in line[2:].split())
            w.append({k: (v if k == "game_s" else float(v)) for k, v in d.items()} | {"game_s": float(d["game_s"])})
        if line.startswith("h:"):
            d = dict(kv.split("=") for kv in line[2:].split())
            h.append({k: (float(str(v).split("/")[0]) if "/" not in str(v) else 0.0) for k, v in d.items()})
    return w, h, head


def waves(w, mult=10.0):
    """Wave windows: samples whose kick rate exceeds mult x the median sample's."""
    rates = [x["kicks"] for x in w]
    rates.sort()
    med = rates[len(rates) // 2]
    hot = [x for x in w if x["kicks"] > mult * max(med, 1.0)]
    spans, cur = [], None
    for x in hot:
        if cur and x["game_s"] - cur[1] <= 500:
            cur[1] = x["game_s"]
        else:
            cur = [x["game_s"], x["game_s"]]
            spans.append(cur)
    return spans, med


def at(w, t):
    best, bd = None, 1e18
    for x in w:
        d = abs(x["game_s"] - t)
        if d < bd:
            best, bd = x, d
    return best


def main(path):
    w, h, head = parse(path)
    spans, med = waves(w)
    print(f"{len(w)} w-samples, {len(h)} h-samples; median sample kicks {med:.0f}")
    print(f"wave windows (game-s): {['%.0f-%.0f' % s for s in spans]}")
    pre = min(w[2:8], key=lambda x: x["kicks"])
    print(f"\npre-wave-1 quiet point: game_s={pre['game_s']:.0f} rss={pre['rss']:.0f} cat={pre['cat']:.0f}")
    for k, (a, b) in enumerate(spans, 1):
        post = min((x for x in w if x["game_s"] > b + 1500), key=lambda x: abs(x["game_s"] - (b + 2500)))
        print(
            f"wave {k}: {a:.0f}-{b:.0f}  peak_kicks/sample={max(x['kicks'] for x in w if a - 250 <= x['game_s'] <= b + 250):.0f}"
            f"  lag_peak={max(x['lag'] for x in w if a - 250 <= x['game_s'] <= b + 250):.3f}"
            f"  max_ms_peak={max(x['max_ms'] for x in w if a - 250 <= x['game_s'] <= b + 250):.2f}"
            f"  over_peak={sum(x['over'] for x in w if a - 250 <= x['game_s'] <= b + 250):.0f}"
        )
        print(
            f"   post(+{post['game_s'] - b:.0f}): rss={post['rss']:.0f} hwm={post['hwm']:.0f} cat={post['cat']:.0f}"
            f" held={post['held']:.0f} lag={post['lag']:.3f}"
        )
    # monotonicity verdict between waves
    posts = []
    for a, b in spans:
        post = min((x for x in w if x["game_s"] > b + 1500), key=lambda x: abs(x["game_s"] - (b + 2500)))
        posts.append(post)
    for i in range(1, len(posts)):
        d = posts[i]["rss"] - posts[i - 1]["rss"]
        print(f"rss delta wave {i + 1} vs wave {i}: {d:+.0f} MB")
    print("\nh-census (bytes/body, h2, hmax, refusals, dead):")
    for x in h:
        print(
            f"  game_s={x['game_s']:.0f} bpb={x['b_per_body']:.0f} h2={x['h2']:.0f} hmax={x['hmax']:.0f}"
            f" hsum={x['hsum']:.0f} ref={x['refusals']:.0f} dead={x['dead']:.0f} enc={x['enc']:.0f}"
        )
    for k, v in head.items():
        print(v[:400])


if __name__ == "__main__":
    main(sys.argv[1])
