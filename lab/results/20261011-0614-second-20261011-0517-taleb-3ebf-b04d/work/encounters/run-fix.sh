#!/bin/sh
# usage: run-fix.sh  — regenerates fix.jsonl (each stage a separate process, <= 60 s each;
# stage wall times in the record). Std only, 4 threads, well under the 2 GB budget.
cd "$(dirname "$0")"
{
  echo "# machine: $(hostname) 8 vCPU; load: $(cut -d' ' -f1-3 /proc/loadavg); mem avail: $(grep MemAvailable /proc/meminfo | awk '{print $2}') kB"
  echo "# utc: $(date -u +%FT%TZ)"
  /tmp/fix-target/release/fix c
  /tmp/fix-target/release/fix b
  /tmp/fix-target/release/fix a q
  /tmp/fix-target/release/fix a 1e-4
  /tmp/fix-target/release/fix a 1e-3
  /tmp/fix-target/release/fix a 1e-2
  /tmp/fix-target/release/fix a k
} > fix.jsonl
echo "wrote fix.jsonl: $(grep -c '"part"' fix.jsonl) records"
