import json, sys
R = "lab/results/20261014-0450-quant-1845/work"
p = json.load(open(f"{R}/m400-s3-prof.json")); q = json.load(open(f"{R}/m400-s3-pristine.json"))
print(f"identity control m400/s3: prof digest {p['digest'][:16]} == pristine {q['digest'][:16]}: {p['digest']==q['digest']}")
for arm in ["m4000-s3","m1500-s3","m4000-s7"]:
    j = json.load(open(f"{R}/{arm}-prof.json"))
    st = {s["stage"]: s for s in j["prof_stages"]}
    pk = st["item: kick (Wisdom-Holman)"]
    kids = ["  kick: readout + scalars","  kick: secondaries + tide","  kick: force::acceleration",
            "  kick: quantize/burn before the rebind","  rebind non-fit: tau pair, retire, entry clones",
            "  plan_terminal (terminal/impact search)","  kick: word quantize after the rebind"]
    nonbind = sum(st[k]["us_per_call"] for k in kids if k in st)
    bind = pk["us_per_call"] - nonbind
    ki = st["  next_impact bisection"]; kt = st["  plan_terminal (terminal/impact search)"]
    rowf = st["  orbit_state/readout family (wall nests)"]
    ho = st.get("hand-out (a member made a body)"); hr = st.get("  hand-out: first plan (replan)")
    print(f"\n== {arm}: digest {j['digest'][:16]} bodies {j['bodies']} wall {j['wall_seconds']:.1f}s overflow {j['rtf']['overflow_frames']}/{j['frames']}")
    print(f"  fired kick           : {pk['us_per_call']:7.1f} us/call x {pk['calls']}")
    print(f"    bind (by substraction) {bind:7.1f} us  ({100*bind/pk['us_per_call']:.0f}% of the kick)")
    print(f"    impact bisection       {ki['us_per_call']:7.1f} us  ({100*ki['us_per_call']/pk['us_per_call']:.0f}% of the kick; {ki['calls']} searches = {ki['calls']/pk['calls']:.2f}/kick incl. hand-out replans)")
    print(f"    all other terms        {nonbind-ki['us_per_call']:7.1f} us  ({100*(nonbind-ki['us_per_call'])/pk['us_per_call']:.0f}%)")
    print(f"  readout family       : {rowf['us_per_call']:.2f} us/call, {rowf['calls']} calls, {rowf['ms']/1000:.2f} s total (~{ki['us_per_call']/rowf['us_per_call']:.0f} readouts per search)")
    if ho: print(f"  hand-out             : {ho['us_per_call']:.1f} us/call x {ho['calls']} (replan {hr['us_per_call']:.1f} us: the same bisection, once per hand-out)")
