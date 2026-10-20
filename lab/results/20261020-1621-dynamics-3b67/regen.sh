#!/usr/bin/env bash
# Regenerates every dossier number for 3b67: rebuilds the harness (the runner applies
# work/patch.diff before this runs; identical to work/c644.patch, applied here only if
# missing), flies the two tail arms to H=98304 (2x c644's horizon, ~6.5 min/arm
# concurrently on the lab box), analyzes, decimates the large TSVs.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
RUN=lab/results/20261020-1621-dynamics-3b67
git apply --check "$RUN/work/patch.diff" 2>/dev/null && git apply "$RUN/work/patch.diff" || true
cargo build --release --example beltewalk
B="${CARGO_TARGET_DIR:-target}/release/examples/beltewalk"
cd "$RUN/work"
rm -rf flights; mkdir flights; cd flights
"$B" --horizon 98304 --seed 1 --thermal 0     --out B2_cold_s1 > B2.log 2>&1 &
"$B" --horizon 98304 --seed 2 --thermal 4096 --out C2_th_s2  > C2.log 2>&1 &
wait
cd ..
python3 analyze_tail.py flights/B2_cold_s1 492 63461214 > analysis_B2.json
python3 analyze_tail.py flights/C2_th_s2  498 88881906 > analysis_C2.json
# rattle concentration (per-body incidence from the last stride; ct counts both bodies
# of a pair, so pair-contacts/ch = sum/2)
python3 - <<'EOF'
import math
Q=1<<20
for arm in ("B2_cold_s1","C2_th_s2"):
    snaps={}
    for line in open(f"flights/{arm}.snap.tsv"):
        f=line.split(); t,bid=int(f[0]),int(f[1]); snaps.setdefault(t,{})[bid]=(int(f[3]),int(f[4]),int(f[5]))
    ts=sorted(snaps); last,prev=ts[-1],ts[-2]
    rates={b:(snaps[last][b][0]-snaps[prev][b][0])/128 for b in snaps[last]}
    tot=sum(rates.values())
    hot=[b for b,r in rates.items() if r>1]
    rq=lambda b: math.hypot(snaps[last][b][1],snaps[last][b][2])/Q
    hot_r=sorted(rq(b) for b in hot)
    print(arm,"pair-contacts/ch",round(tot/2),"| bodies>1c/ch:",len(hot),
          "carrying",round(100*sum(rates[b] for b in hot)/tot,1),"% |",
          "hot median r",round(hot_r[len(hot_r)//2],2),"q | frac hot<2.1q",
          round(sum(1 for r in hot_r if r<2.1)/len(hot),3))
EOF
# keep the run folder under the 5 MB/file cap
for f in B2_cold_s1 C2_th_s2; do awk 'NR%16==1' flights/$f.global.tsv > flights/$f.global.decim.tsv; done
rm -f flights/B2_cold_s1.global.tsv flights/C2_th_s2.global.tsv flights/B2_cold_s1.snap.tsv flights/C2_th_s2.snap.tsv
echo "--- headline numbers ---"
python3 - <<'EOF'
import json
for arm in ("B2", "C2"):
    d = json.load(open(f"analysis_{arm}.json"))
    print(arm, "reproduces-prefix", d["prefix"]["reproduces"],
          "| tail deaths", d["tail_fit"]["deaths_tail"],
          "| lam_e5", d["tail_fit"]["lam_e5"], "r2", d["tail_fit"]["r2"],
          "| halflife", d["tail_fit"]["halflife_ch"],
          "| late ct/ch", d["standing"]["mean_ct_ch_last8k"],
          "| alive_end", d["windows"][-1]["alive_end"],
          "| ke ratio", d["ke_in"]["ratio"],
          "| late deaths n", d["late_deaths"]["n"],
          "frac<30q", d["late_deaths"]["frac_core_lt30q"],
          "frac<10q", d["late_deaths"]["frac_core_lt10q"])
    for w in d["windows"][-6:]:
        print("   win", w["w"], "deaths", w["deaths"], "haz_e5", w["hazard_e5"],
              "ct/ch", w["contacts_per_ch"], "alive", w["alive_end"], "n_in", w["n_in_end"])
EOF
