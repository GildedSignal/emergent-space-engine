#!/usr/bin/env python3
"""The stacked-build endgame, computed from the fresh census JSONs (nothing hardcoded; run 790b).

Reads work/base_m4000_s1.json (shipped arm: ES_BASELINE_ARM=1 ES_EAGER=1) and
work/st_m4000_s1.json (the stacked arm: 009b word fix + 5eb6/8b43 lazy tier), prints the
measured composite and the two projections the checker's gold bar named:

  - MEASURED: D (process + hand-out + fleet item + decisions) and D+fixed (the frame's whole
    event-class work) on both arms of one binary, same scene, same seed;
  - +MEMO (7055): priced from the memo arm's measured hit rate (st_m4000_s1_memo.json) applied
    to the stacked hand-out bind — the 009b×7055 interaction, measured not assumed;
  - +CARLSON (de99): ×10 priced onto the record's compile share (60-66%, 7055's measurement) of
    the surviving bind — priced, not wired: the kernel delivers the walk's three increments and
    the bind's compile builds the panel grid the readout interpolates, so this factor is an
    upper bound on what wiring could ever give the bind path, not an adoption claim.

Ceiling: the resolved-battle member count at 25% of 4 cores on the stacked slope.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "work")

def stages(path):
    r = json.load(open(path))
    m = {}
    for row in r.get("prof_stages", []):
        m[row["stage"].strip()] = (row["ms"], row["calls"])
    return r, m

def s(m, k):
    return m.get(k, (0.0, 0))[0]

FIT = "fit: bind_surface (kicks, hand-outs)"
FIT2 = "fit again: the coarser word (bind_surface)"
HO = "hand-out (a member made a body)"
HBIND = "hand-out: bind (the member as a tube)"
PROC = "process (whole)"
FADV = "fleet: advance (whole item)"
DEC = "decision"
REKEY = "rekey (all deadlines)"
REQ = "requeue"
TD = "take_due"

def block(path, name):
    r, m = stages(path)
    gs = r["frames"] * r["rtf_target"] / 60.0
    bind = s(m, FIT) + s(m, FIT2)
    D = s(m, PROC) + s(m, HO) + s(m, FADV) + s(m, DEC)
    fixed = s(m, REKEY) + s(m, REQ) + s(m, TD)
    pp = r.get("promo_probe", {})
    print(f"{name:28s} D={D/gs:7.1f} bind={bind/gs:6.1f} ho_bind={s(m,HBIND)/gs:6.1f} "
          f"fixed={fixed/gs:5.1f} D+fixed={(D+fixed)/gs:7.1f} ms/game-s | "
          f"fit2 calls={m.get(FIT2,(0,0))[1]:6d} | digest={r['digest'][:12]} "
          f"bodies={r['bodies']:5d} ovf={r['rtf']['overflow_frames']:3d} worst={r['worst_hitch_ms']:5.1f}ms"
          + (f" | memo compiles={pp.get('compiles')} hits={pp.get('exact_hits')} "
             f"ho_compiles={pp.get('handout_compiles')} ho_hits={pp.get('handout_exact_hits')}" if pp else ""))
    return dict(gs=gs, D=D, bind=bind, hobind=s(m, HBIND), fixed=fixed, r=r, m=m)

base = block(os.path.join(WORK, "base_m4000_s1.json"), "shipped (baseline arm)")
st = block(os.path.join(WORK, "st_m4000_s1.json"), "stacked (word fix + lazy)")
memo = block(os.path.join(WORK, "st_m4000_s1_memo.json"), "stacked + memo (7055)")
base_memo = block(os.path.join(WORK, "base_m4000_s1_memo.json"), "shipped + memo (control)")

print()
gs = st["gs"]
Db, Ds = base["D"] / gs, st["D"] / gs
print(f"measured composite at m4000:            D {Db:.1f} -> {Ds:.1f} ms/game-s "
      f"({100*Ds/Db:.0f}%), D+fixed {(base['D']+base['fixed'])/gs:.1f} -> "
      f"{(st['D']+st['fixed'])/gs:.1f} ({100*(st['D']+st['fixed'])/(base['D']+base['fixed']):.0f}%)")
pp = json.load(open(os.path.join(WORK, "st_m4000_s1_memo.json"))).get("promo_probe", {})
ppb = json.load(open(os.path.join(WORK, "base_m4000_s1_memo.json"))).get("promo_probe", {})
hitrate = (pp.get("exact_hits", 0) / pp["compiles"]) if pp.get("compiles") else 0.0
hitrate_b = (ppb.get("exact_hits", 0) / ppb["compiles"]) if ppb.get("compiles") else 0.0
print(f"7055 memo hit rate:                     shipped+memo {100*hitrate_b:.1f}% vs "
      f"stacked+memo {100*hitrate:.1f}% of {pp.get('compiles')} compiles "
      f"(hand-out {pp.get('handout_exact_hits')}/{pp.get('handout_compiles')})")
# The memo arm's own timing (logging on, so indicative): hand-out bind stacked+memo vs stacked.
print(f"memo's price on the word-fixed bind:    ho_bind {st['hobind']/gs:.1f} -> {memo['hobind']/gs:.1f} ms/game-s "
      f"(shared-box, logging on; order of magnitude)")
for share, tag in [(0.60, "conservative"), (0.66, "high")]:
    carlson = st["bind"] / gs * share * 0.9
    print(f"+ Carlson x10 priced ({tag}, {int(share*100)}%):   D -> {(Ds - carlson):.1f} ms/game-s "
          f"({100*(Ds-carlson)/Db:.0f}% of shipped D; checker's bar: within ~2x of 42.3, i.e. <= 85)")
budget = 0.25 * 4 * 1000.0
for label, D_ms in [("shipped D+fixed", (base["D"] + base["fixed"]) / gs),
                    ("stacked D+fixed", (st["D"] + st["fixed"]) / gs),
                    ("stacked + Carlson(60%) D+fixed", (st["D"] + st["fixed"]) / gs - st["bind"] / gs * 0.6 * 0.9)]:
    print(f"ceiling on {label:26s} {budget/(D_ms/4000.0):10.0f} members (25% of 4 cores)")
