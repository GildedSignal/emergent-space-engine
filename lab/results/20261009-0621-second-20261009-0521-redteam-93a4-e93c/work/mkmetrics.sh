#!/bin/sh
# Regenerates metrics.json for rung-r-news.md from shipped code (news2.c).
# 16 runs, each <= 30 s on 1 core; total ~3 min. Prints the metrics as it goes.
set -e
cd "$(dirname "$0")"

f() { sed -n "s/.*t\/P_T= *$2\.00.*$1= *\([^ ]*\).*/\1/p"; }

cfg() { # cfg <name> <law> <noSJ>
  o30=$(./news2 0.3 5 0.001 "$2" 30 "$3" D 3 10 30 1)
name="$1"
  o4=$(./news2 0.3 5 0.0001 "$2" 30 "$3" D 3 10 30 1)
  o100=$(./news2 0.3 5 0.001 "$2" 100 "$3" D 10 30 100 1)
  o5=$(./news2 0.3 5 0.00001 "$2" 30 "$3" D 3 10 30 1)
  b30=$(printf '%s\n' "$o30" | f maxdE 30)
  b100=$(printf '%s\n' "$o100" | f maxdE 100)
  m30=$(printf '%s\n' "$o100" | f maxdE 30)
  hill=$(printf '%s\n' "$o100" | f hillmin 100)
  b4=$(printf '%s\n' "$o4" | f maxdE 30)
  b5=$(printf '%s\n' "$o5" | f maxdE 30)
  grow=$(awk -v a="$b100" -v b="$m30" 'BEGIN{printf "%.3f", a/b}')
  sl=$(awk -v a="$b30" -v b="$b5" 'BEGIN{printf "%.4f", (log(a)-log(b))/2/log(10)}')
  echo "$name: b30=$b30 b100=$b100 grow=$grow slope=$sl hill=$hill" >&2
  J="$J  \"$name\": {\"hill_min_ratio\": $hill, \"read_bound_30\": $b30, \"read_bound_100\": $b100, \"read_growth_100_30\": $grow, \"mu_slope\": $sl},\n"
}

J="{\n"
cfg tube 1 0
cfg tube-carlip 2 0
cfg naive-retarded 0 0
cfg freefall-tube 1 1
J=$(printf "$J" | sed '$ s/,$//')
printf "$J\n}\n" > metrics.json
cat metrics.json
