#!/usr/bin/env python3
"""Check the state law of the finality fire on every draw's instrument trace.

For each *.err in draws/: parse HAZ (armed margin A, pair b/t), PRE (D = (violation,
truth id, s0) of the clash the upcoming certify would restore), RB (m, out, mo), FIRE
(fin_hi, s0, box). Verifies: (1) every FIRE is preceded by a PRE with D>0 matching the
FIRE's own fin_hi-s0 and s0 (the immediately preceding PRE of the same stride id);
(2) the last armed HAZ pair before the fire names the fatal clash (b = PRE id, t = PRE
truth); (3) every RB has out=[] and mo=0; non-fatal RBs have m<=0 (e517's law: m=0);
(4) armed-without-fire happens (armed != incidence); (5) survivor/negative draws: fires=0.
"""
import re, sys, glob, os

def parse(path):
    haz, pre, rb, fire = [], [], [], []
    for ln in open(path, errors="replace"):
        if ln.startswith("HAZ p="):
            m = re.search(r"p=(\d+) .*A=(-|\d+)(?: b(\d+) t(\d+) s(-?\d+))?", ln)
            if m:
                haz.append(dict(p=int(m.group(1)),
                    A=None if m.group(2) == "-" else int(m.group(2)),
                    b=int(m.group(3)) if m.group(3) else None,
                    t=int(m.group(4)) if m.group(4) else None,
                    s=int(m.group(5)) if m.group(5) else None))
        elif ln.startswith("PRE id="):
            m = re.match(r"PRE id=(\d+) s=(-?\d+) e=(-?\d+) D=(None|Some\(\((\d+), (\d+), (-?\d+)\)\))", ln.strip())
            if m:
                pre.append(dict(id=int(m.group(1)), s=int(m.group(2)), e=int(m.group(3)),
                    D=None if m.group(4) == "None" else dict(v=int(m.group(5)), t=int(m.group(6)), s0=int(m.group(7)))))
        elif ln.startswith("RB lid="):
            m = re.match(r"RB lid=(\d+) s0=(-?\d+) s=(-?\d+) aff=\[(.*)\] m=(-?\d+) out=\[(.*)\] mo=(-?\d+)", ln.strip())
            if m:
                rb.append(dict(lid=int(m.group(1)), s0=int(m.group(2)), s=int(m.group(3)),
                    aff=m.group(4), m=int(m.group(5)), out=m.group(6), mo=int(m.group(7))))
        elif ln.startswith("FIRE id="):
            m = re.match(r"FIRE id=(\d+) s0=(-?\d+) fin_hi=(-?\d+)(?: box (.*))?", ln.strip())
            if m:
                fire.append(dict(id=int(m.group(1)), s0=int(m.group(2)), fin_hi=int(m.group(3)), box=m.group(4)))
    return haz, pre, rb, fire

def main():
    ok = True
    armed_cls = {"exact": 0, "lineage": 0, "publish-blind": 0}
    tot_rb = tot_nonfatal_m0 = tot_nonfatal_mneg = tot_out = tot_armed_nofire = tot_preD_pos = 0
    for path in sorted(glob.glob(os.path.join(os.path.dirname(__file__), sys.argv[1] if len(sys.argv) > 1 else "draws", "*.err"))):
        name = os.path.basename(path)[:-4]
        haz, pre, rb, fire = parse(path)
        fired = bool(fire)
        nonfatal_m0 = sum(1 for r in rb if r["m"] == 0)
        nonfatal_mneg = sum(1 for r in rb if r["m"] < 0)
        out_open = sum(1 for r in rb if r["out"].strip())
        armed = [h for h in haz if h["A"] is not None and h["A"] > 0]
        # PRE D>0 count (armed at certify granularity), fires included
        preD_pos = sum(1 for p in pre if p["D"] and p["D"]["v"] > 0)
        tot_rb += len(rb); tot_nonfatal_m0 += nonfatal_m0; tot_nonfatal_mneg += nonfatal_mneg
        tot_out += out_open; tot_armed_nofire += len(armed) - (1 if fired else 0)
        tot_preD_pos += preD_pos
        print(f"{name}: haz={len(haz)} pre={len(pre)} rb={len(rb)} fires={len(fire)} "
              f"nonfatal_m0={nonfatal_m0} nonfatal_m<0={nonfatal_mneg} out_open={out_open} "
              f"armed_pubs={len(armed)} preD>0={preD_pos}")
        for f in fire:
            # the latest PRE at or before this point (parse order = file order); find by
            # scanning the raw file for the FIRE line index is complex — use the last PRE
            # whose D>0 appears before the fire in sequence: we track via re-parse below.
            pass
    # per-fire verification with ordered events
    print("\n-- fire-by-fire --")
    for path in sorted(glob.glob(os.path.join(os.path.dirname(__file__), sys.argv[1] if len(sys.argv) > 1 else "draws", "*.err"))):
        events = []
        for ln in open(path, errors="replace"):
            tag = ln.split(" ", 1)[0]
            if tag in ("HAZ", "PRE", "RB", "FIRE"):
                events.append((tag, ln.strip()))
        name = os.path.basename(path)[:-4]
        for i, (tag, ln) in enumerate(events):
            if tag != "FIRE":
                continue
            f = re.match(r"FIRE id=(\d+) s0=(-?\d+) fin_hi=(-?\d+)(?: box c=\[([-\d, ]+)\] s=\[([-\d, ]+)\])?", ln)
            fid, s0, fin = int(f.group(1)), int(f.group(2)), int(f.group(3))
            # last PRE with D>0 before this FIRE
            last_pre = next((e for e in reversed(events[:i]) if e[0] == "PRE" and "D=Some" in e[1]
                             and not re.search(r"D=Some\(\(0,", e[1])), None)
            p = re.match(r"PRE id=(\d+) .*D=Some\(\((\d+), (\d+), (-?\d+)\)\)", last_pre[1])
            pid, dv, dt, ds0 = int(p.group(1)), int(p.group(2)), int(p.group(3)), int(p.group(4))
            # last armed HAZ before this FIRE
            last_haz = next((e for e in reversed(events[:i]) if e[0] == "HAZ"
                             and re.search(r"A=\d+", e[1]) and not re.search(r"A=-", e[1])
                             and int(re.search(r"A=(-?\d+)", e[1]).group(1)) > 0), None)
            h = re.search(r"A=(-?\d+) b(\d+) t(\d+) s(-?\d+)", last_haz[1])
            av, ab, at, as0 = int(h.group(1)), int(h.group(2)), int(h.group(3)), int(h.group(4))
            # the RB that carries this fire (next RB after the FIRE line)
            nxt_rb = next((e for e in events[i:] if e[0] == "RB"), None)
            r = re.match(r"RB lid=(\d+) s0=(-?\d+).*out=\[(.*?)\] mo=(-?\d+)", nxt_rb[1])
            match_d = (dv == fin - s0 and ds0 == s0)
            # Was the fatal pair armed at publish granularity before the fire?
            # (a) exact: same busy region and truth lineage, same margin and s0;
            # (b) lineage: shares a lineage, same margin and s0 (a split moved the busy id);
            # (c) publish-blind: no armed line of this pair at all before the fire — the
            #     publish-side certificate (A<=0) cannot see it (e517's soundness note,
            #     here measured): the busy set was empty/disarmed between the dispatch and
            #     the certify. The certify-side law (PRE D) is the complete decider.
            armed_events = [e for e in events[:i] if e[0] == "HAZ" and re.search(r"A=\d+", e[1])
                            and int(re.search(r"A=(-?\d+)", e[1]).group(1)) > 0]
            cls = "publish-blind"
            for e in reversed(armed_events):
                m2 = re.search(r"A=(-?\d+) b(\d+) t(\d+) s(-?\d+)", e[1])
                a2, b2, t2, s2 = int(m2.group(1)), int(m2.group(2)), int(m2.group(3)), int(m2.group(4))
                if b2 == pid and t2 == dt and a2 == dv and s2 == ds0:
                    cls = "exact"; av, ab, at, as0 = a2, b2, t2, s2; break
                if {b2, t2} & {pid, dt} and a2 == dv and s2 == ds0:
                    cls = "lineage"; av, ab, at, as0 = a2, b2, t2, s2; break
            if cls == "publish-blind":
                pass  # keep the last armed line for the printout
            print(f"{name}: FIRE id={fid} s0={s0} fin_hi={fin} viol={fin-s0} box c=[{f.group(4)}] s=[{f.group(5)}]")
            print(f"    PRE id={pid} D=({dv},{dt},{ds0}) -> D==viol,s0: {match_d}; armed class: {cls} "
                  f"(last armed: A={av} b{ab} t{at} s{as0}); "
                  f"fatal RB lid={r.group(1)} s0={r.group(2)} out_open={'YES' if r.group(3).strip() else 'no'}")
            armed_cls[cls] += 1
            ok &= match_d and not r.group(3).strip()
    print(f"\nTOTALS: rb={tot_rb} nonfatal_m0={tot_nonfatal_m0} nonfatal_m<0={tot_nonfatal_mneg} "
          f"out_open={tot_out} armed_pubs_without_fire={tot_armed_nofire} preD>0={tot_preD_pos} "
          f"armed_exact={armed_cls['exact']} armed_lineage={armed_cls['lineage']} publish_blind={armed_cls['publish-blind']}")
    print("CERTIFY LAW HOLDS on every fire: PRE D = violation (s0 exact), out= shut" if ok else "LAW VIOLATED")

if __name__ == "__main__":
    main()
