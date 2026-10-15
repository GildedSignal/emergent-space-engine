#!/usr/bin/env python3
"""Parse wavetrain logs: wave windows, the memory trajectory at each wave, catalogue, history, lag.

Fixed in 7dc6 (the 4af4 shipped copy crashed: "'%.0f-%.0f' % s" with s a *list* raises
TypeError, masked by `|| true` in regen.sh — the run's own script could not regenerate its
wave tables). Two changes: tuple() in the window formatter, and hist_sample=a/b parsed into
hist_a/hist_b so the census numerator regenerates too. Wave-table extras (width, spacing,
peak/median ratio) added for the long-train arms; detection rule unchanged (kicks > mult x
median sample; merge gap 750 game-s)."""
import re
import sys


def parse(path):
    w, h, head, end = [], [], {}, {}
    for line in open(path):
        if line.startswith(("wavetrain", "train:", "end:", "digest:")):
            head.setdefault(line.split(":")[0], line.strip())
        if line.startswith("w:"):
            d = dict(kv.split("=") for kv in line[2:].split())
            w.append({k: (v if k == "game_s" else float(v)) for k, v in d.items()} | {"game_s": float(d["game_s"])})
        if line.startswith("h:"):
            d = dict(kv.split("=") for kv in line[2:].split())
            row = {}
            for k, v in d.items():
                if "/" in v:  # hist_sample=2858/4106 -> numerator, denominator
                    a, b = v.split("/")
                    row[k + "_a"], row[k + "_b"] = float(a), float(b)
                else:
                    row[k] = float(v)
            h.append(row)
    return w, h, head


def waves(w, mult=10.0, gap=750.0):
    """Wave windows: samples whose kick rate exceeds mult x the median sample's."""
    rates = sorted(x["kicks"] for x in w)
    med = rates[len(rates) // 2]
    hot = [x for x in w if x["kicks"] > mult * max(med, 1.0)]
    spans, cur = [], None
    for x in hot:
        if cur and x["game_s"] - cur[1] <= gap:
            cur[1] = x["game_s"]
        else:
            cur = [x["game_s"], x["game_s"]]
            spans.append(cur)
    return spans, med


def at(w, t):
    return min(w, key=lambda x: abs(x["game_s"] - t))


def main(path):
    w, h, head = parse(path)
    spans, med = waves(w)
    print(f"{len(w)} w-samples, {len(h)} h-samples; median sample kicks {med:.0f}")
    print(f"wave windows (game-s): {['%.0f-%.0f' % tuple(s) for s in spans]}")
    if not spans:
        print("no wave windows above threshold: the train has dissolved into the steady stream")
        return
    pre = min(w[2:8], key=lambda x: x["kicks"])
    print(f"\npre-wave-1 quiet point: game_s={pre['game_s']:.0f} rss={pre['rss']:.0f} cat={pre['cat']:.0f}")
    prev_b = None
    for k, (a, b) in enumerate(spans, 1):
        win = [x for x in w if a - 250 <= x["game_s"] <= b + 250]
        post = min((x for x in w if x["game_s"] > b + 1500), key=lambda x: abs(x["game_s"] - (b + 2500)))
        extra = "" if prev_b is None else f"  spacing_from_prev={a - prev_b:.0f}"
        print(
            f"wave {k}: {a:.0f}-{b:.0f} width={b - a:.0f}{extra}"
            f"  peak_kicks/sample={max(x['kicks'] for x in win):.0f} ({max(x['kicks'] for x in win) / max(med, 1):.1f}x med)"
            f"  lag_peak={max(x['lag'] for x in win):.3f}"
            f"  max_ms_peak={max(x['max_ms'] for x in win):.2f}"
            f"  over_peak={sum(x['over'] for x in win):.0f}"
        )
        print(
            f"   post(+{post['game_s'] - b:.0f}): rss={post['rss']:.0f} hwm={post['hwm']:.0f} cat={post['cat']:.0f}"
            f" held={post['held']:.0f} lag={post['lag']:.3f}"
        )
        prev_b = b
    # monotonicity verdict between waves
    posts = []
    for a, b in spans:
        posts.append(min((x for x in w if x["game_s"] > b + 1500), key=lambda x: abs(x["game_s"] - (b + 2500))))
    for i in range(1, len(posts)):
        d = posts[i]["rss"] - posts[i - 1]["rss"]
        print(f"rss delta wave {i + 1} vs wave {i}: {d:+.0f} MB")
    # after the last wave: is anything still above threshold?
    tail = [x for x in w if x["game_s"] > spans[-1][1] + 2000]
    if tail:
        print(f"tail after last window: {len(tail)} samples, max kicks/sample {max(x['kicks'] for x in tail):.0f}"
              f" ({max(x['kicks'] for x in tail) / max(med, 1):.1f}x med), rss {tail[0]['rss']:.0f} -> {tail[-1]['rss']:.0f}")
    print("\nh-census (bytes/body, h2, hmax, refusals, dead):")
    for x in h:
        hs = f"{x.get('hist_sample_a', -1):.0f}/{x.get('hist_sample_b', -1):.0f}" if "hist_sample_a" in x else "-"
        print(
            f"  game_s={x['game_s']:.0f} bpb={x['b_per_body']:.0f} hist={hs} h2={x.get('h2', -1):.0f} hmax={x.get('hmax', -1):.0f}"
            f" hsum={x.get('hsum', -1):.0f} ref={x.get('refusals', -1):.0f} dead={x.get('dead', -1):.0f} enc={x.get('enc', -1):.0f}"
        )
    for k, v in head.items():
        print(v[:400])


if __name__ == "__main__":
    main(sys.argv[1])
