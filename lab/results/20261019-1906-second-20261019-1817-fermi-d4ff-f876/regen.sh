#!/usr/bin/env bash
# Regenerates every number in dossier.md from shipped constants (beltlib.py
# ports the scenario.rs genesis verbatim; no engine code changed).
# Total wall ~11 min (brute configs run in parallel; 8 vCPU box).
set -e
cd "$(dirname "$0")/work"
python3 mc.py 16000000 8 > mc_prod.json &
MC=$!
python3 brute.py 1e5 100000 2.0e4 11 > brute_1e5.json &
B1=$!
python3 brute.py 3e4 100000 2.5e5 11 > brute_3e4a.json &
B2=$!
python3 brute.py 3e4 100000 2.5e5 23 > brute_3e4b.json &
B3=$!
python3 brute.py 1e4 100000 1.0e6 11 > brute_1e4.json &
B4=$!
wait $MC $B1 $B2 $B3 $B4
python3 kinetic.py > kinetic.json
python3 - <<'EOF'
import json
rows = []
for f in ["brute_1e5.json", "brute_3e4a.json", "brute_3e4b.json", "brute_1e4.json"]:
    r = json.load(open(f))
    rows.append({k: r[k] for k in
                 ("d_root", "M", "T_game_s", "events",
                  "gamma_per_root_per_game_s_at_1e9", "mean_event_dv_km_s")})
json.dump(rows, open("brute_ladder.json", "w"), indent=1)
EOF
python3 ledger.py > ledger.json
echo "=== adopted gamma and ledger ==="
python3 -c "import json; d=json.load(open('ledger.json')); print('Gamma =', d['adopted_gamma_per_root_per_game_s'], '+/-', d['gamma_stat_sys_band']); print('TP bar =', d['tp_bar_events_per_game_s_100km'], 'contacts/s =', d['contacts_per_game_s_1e9'], '+cores =', d['stream_row_addition_cores_today'])"
