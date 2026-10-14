#!/usr/bin/env python3
"""One wall: per-class bind census from `universe --bench --features prof` JSONs.

Stages as printed by prof::NAMES (crates/universe/src/prof.rs), mapped by prefix:
  fit = bind_surface's first bind_in (kicks, hand-outs), fit2 = the coarser re-fit retry,
  process = a resolved ship/player item (p_kick/p_decide nest inside it),
  f_adv = the fleet's own item (contains f_run), handout = the promotion (h_bind inside).
`stats` is a Debug string in the shipped report; parsed here.

Columns: D = process+handout+f_adv+p_decide (every item that carries events);
bind = fit+fit2 (the whole bind_surface wall); bind%D = the one-wall share;
fit2%bind = the retry's share of the bind; hbind%ho = the bind's share of a hand-out;
us/fit = mean µs per first bind; ev/m/gs = events per member per game-second.
"""
import json, sys, glob, os, re

PREFIX = [("rekey", "rekey"), ("position", "root"), ("apply", "apply"), ("requeue", "requeue"),
          ("process", "process"), ("fit:", "fit"), ("take_due", "take_due"), ("prune", "prune"),
          ("encounters: capture", "encounters"), ("encounters: held", "scans"),
          ("item: kick (Wisdom", "p_kick"), ("item: kick (clock", "p_kick_clock"),
          ("item: kick at a changeover", "p_kick_sub"), ("item: boundary", "p_boundary"),
          ("item: open", "p_open"), ("item: crash", "p_crash"), ("decision", "p_decide"),
          ("fleet: battle", "f_run"), ("fleet: advance", "f_adv"), ("hand-out (", "handout"),
          ("hand-out: pull", "h_pull"), ("hand-out: bind", "h_bind"),
          ("hand-out: first", "h_replan"), ("fit again", "fit2")]

def stage_map(report):
    m = {}
    for row in report.get("prof_stages", []):
        s = row["stage"].strip()
        for pre, key in PREFIX:
            if s.startswith(pre):
                m[key] = (row["ms"], row["calls"])
                break
    return m

def dbg_stats(s):
    out = {}
    for k in ["kicks", "opens", "boundaries", "handoffs", "lost", "refused", "slices",
              "encounters", "decisions", "leavers", "dissolved"]:
        mm = re.search(k + r": (\d+)", s)
        if mm:
            out[k] = int(mm.group(1))
    return out

def main(files):
    print(f"{'run':22s} {'m':>6s} {'sd':>2s} {'rtf':>4s} | {'D_ms':>7s} {'bind_ms':>7s} {'bind%D':>6s} "
          f"{'fit2%b':>6s} {'hbind%ho':>8s} {'us/fit':>6s} {'ev/m/gs':>7s} {'kicks':>6s} {'ho':>5s} {'ovf':>4s} {'fixed_ms':>8s}")
    for f in sorted(files):
        try:
            r = json.load(open(f))
        except Exception as e:
            print(f"{os.path.basename(f):22s} unreadable: {e}")
            continue
        m = stage_map(r)
        st = dbg_stats(r["stats"])
        fit, fitc = m.get("fit", (0, 0))
        fit2 = m.get("fit2", (0, 0))[0]
        bind = fit + fit2
        ho_ms, ho_calls = m.get("handout", (0, 0))
        hbind = m.get("h_bind", (0, 0))[0]
        # every item class that carries events
        denom = (m.get("process", (0, 0))[0] + ho_ms + m.get("f_adv", (0, 0))[0]
                 + m.get("p_decide", (0, 0))[0])
        gs = r["frames"] * r["rtf_target"] / 60.0
        mm = re.search(r"m(\d+)", os.path.basename(f))
        members = int(mm.group(1)) if mm else 0
        ev = sum(st.get(k, 0) for k in ["kicks", "opens", "boundaries", "handoffs", "slices",
                                        "encounters", "decisions"]) + st.get("leavers", 0)
        evrate = ev / members / gs if members and gs else 0
        usfit = 1000.0 * fit / fitc if fitc else 0
        fixed = m.get("rekey", (0, 0))[0] + m.get("requeue", (0, 0))[0] + m.get("take_due", (0, 0))[0]
        print(f"{os.path.basename(f):22s} {members:>6d} {r['seed']:>2d} {r['rtf_target']:>4.0f} | "
              f"{denom:>7.1f} {bind:>7.1f} {100*bind/denom if denom else 0:>5.1f}% "
              f"{100*fit2/bind if bind else 0:>5.1f}% {100*hbind/ho_ms if ho_ms else 0:>7.1f}% "
              f"{usfit:>6.1f} {evrate:>7.4f} {st.get('kicks',0):>6d} {st.get('leavers',0):>5d} "
              f"{r['rtf']['overflow_frames']:>4d} {fixed:>8.0f}")
        if "--verbose" in sys.argv:
            for k, (ms, c) in sorted(m.items(), key=lambda kv: -kv[1][0]):
                if ms > 0:
                    print(f"    {k:12s} {ms:10.1f} ms {c:8d} calls {1000*ms/c if c else 0:8.1f} us/call")
            print("    by kind:", [(c['kind'], c['items'], round(c['us_per_item'], 1)) for c in r["engine_cost_by_kind"]])
            print("    digest:", r["digest"][:16], "bodies:", r["bodies"])

if __name__ == "__main__":
    main([a for a in sys.argv[1:] if not a.startswith("--")] or glob.glob("work/m*.json"))
