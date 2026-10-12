#!/usr/bin/env bash
# Regenerates every number in dossier.md for run
# 20261012-1621-second-20261012-1524-fermi-4b55-09a1.
# ~4.5 min total on the lab's shared 8-vCPU runner; every process < 200 MB.
set -e
cd "$(dirname "$0")"

# 1. The decisive record: brute-force SOI truth, controls, sign-fixed Newton,
#    and the 10^9 headline table (one code path).   [46 s]
python3 soi_truth.py | tee soi_truth_log.txt

# 2. The original run's scripts, unchanged, kept as evidence and for the
#    P1/P2/P4/P5 numbers the dossier cites. They regenerate their stored
#    JSONs bit-for-bit (verified; diffed again here).   [139 s + 75 s]
cp orig/h_live_results.json /tmp/regen-hl.json
cp orig/crosscheck_results.json /tmp/regen-cc.json
( cd orig && python3 h_live_fermi.py > /dev/null )
( cd orig && python3 crosscheck.py  > /dev/null )
diff orig/h_live_results.json   /tmp/regen-hl.json
diff orig/crosscheck_results.json /tmp/regen-cc.json
echo "originals regenerate bit-for-bit"

# 3. Reconciliation: the superseded values vs the adopted truth.
python3 - <<'EOF'
import json
cc = json.load(open("orig/crosscheck_results.json"))
st = json.load(open("soi_truth_results.json"))
hl = json.load(open("orig/h_live_results.json"))
print(f"as-shipped Newton (sign bug):   {cc['soi']['transits_per_body_per_orbit']:.3e}/body/orbit")
print(f"stale h_live JSON (1st bug):    {hl['P3_soi']['transits_per_body_per_orbit']:.3e}/body/orbit (superseded)")
print(f"brute-force truth (adopted):    {st['table_1e9']['truth_rate_per_body_per_orbit']:.3e}/body/orbit")
print(f"stale headline H_live:          {hl['P5_scale_table']['H_live_rebind_bits_per_s']:.1f} bits/s (superseded)")
print(f"reconciled H_live total:        {st['table_1e9']['H_live_total_bits_per_s']:.1f} bits/s "
      f"(rebind {st['table_1e9']['H_live_rebind_bits_per_s']:.1f} + "
      f"player {st['table_1e9']['H_live_player_bits_per_s']:.0f} + "
      f"contact {st['table_1e9']['H_live_contact_bits_per_s']:.2f})")
EOF
echo "regen complete"
