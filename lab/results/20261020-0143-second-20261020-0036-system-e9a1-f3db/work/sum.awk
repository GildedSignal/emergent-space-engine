#!/usr/bin/awk -f
# One row per arm: the worst frame, its worst player item's decomposition, pull census, kick totals.
# Usage: awk -f sum.awk <arm>.err  (reads player_item, pull_wave, frame_items lines)
BEGIN { maxpull = 0; maxfleet = 0; maxitem = 0; rootcalls = 0; rootpulled = 0; rootmax = 0; childcalls = 0; childpulled = 0; maxships = 0; worstframe = "" }
/^player_item/ {
  for (i = 1; i <= NF; i++) {
    split($i, kv, "=")
    if (kv[1] == "pull_ms") pull = kv[2]+0
    else if (kv[1] == "fleet_ms") fleet = kv[2]+0
    else if (kv[1] == "ho_ms") ho = kv[2]+0
    else if (kv[1] == "scan_ms") scan = kv[2]+0
    else if (kv[1] == "proc_ms") proc = kv[2]+0
    else if (kv[1] == "t") t = kv[2]
    else if (kv[1] == "fleet_kicks") fk = kv[2]+0
  }
  if (pull > maxpull) { maxpull = pull; wp = sprintf("t=%s pull=%.1f fleet=%.3f ho=%.3f scan=%.3f proc=%.3f fleet_kicks=%d", t, pull, fleet, ho, scan, proc, fk) }
  if (fleet > maxfleet) maxfleet = fleet
  if (ho > maxho) maxho = ho
  if (scan > maxscan) maxscan = scan
  if (proc > maxproc) maxproc = proc
  totfk += fk
}
/^pull_wave/ {
  for (i = 1; i <= NF; i++) { split($i, kv, "="); if (kv[1] == "pulled") p = kv[2]+0; if (kv[1] == "children_only") co = kv[2] }
  if (co == "false") { rootcalls++; rootpulled += p; if (p > rootmax) rootmax = p; if (p > 0) rootpos++ }
  else { childcalls++; childpulled += p; if (p > 0) childpos++ }
}
/^frame_items/ {
  match($0, /by_class=\[[0-9, ]*\]/); bc = substr($0, RSTART+10, RLENGTH-11); gsub(/ /, "", bc); split(bc, b, ",")
  ships = b[3]+0; players = b[4]+0
  match($0, /ns=[0-9]+/); ns = substr($0, RSTART+3, RLENGTH-3)+0
  if (ns > maxitem) { maxitem = ns; wf = $0 }
  if (ships > maxships) { maxships = ships; ws = $0 }
}
END {
  printf "worst_player_item: %s\n", wp
  printf "max fleet_ms=%.3f ho_ms=%.3f scan_ms=%.3f proc_ms=%.3f | nested fleet_kicks_total=%d\n", maxfleet, maxho, maxscan, maxproc, totfk
  printf "pulls: root calls=%d (>0: %d) pulled_total=%d max=%d | child calls=%d (>0: %d) pulled_total=%d\n", rootcalls, rootpos+0, rootpulled, rootmax, childcalls, childpos+0, childpulled
  printf "worst_frame_item: %s\nmax_item_ns=%d\nships_frame: %s\n", wf, maxitem, ws
}
