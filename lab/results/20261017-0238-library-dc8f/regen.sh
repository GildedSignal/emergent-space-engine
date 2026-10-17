#!/usr/bin/env bash
# Regen for 20261017-0238-library-dc8f (library lens). No build needed:
# every number is source-derived arithmetic from published wiki numbers,
# plus the cached Readwise export. Runtime ~10-20 s with cache, ~1 min with a fetch.
set -euo pipefail
cd "$(dirname "$0")"

# 1. Highlights cache (fetch only if the token is set and the cache is absent).
if [ ! -s cache/export-1.json ] && [ -n "${READWISE_TOKEN:-}" ]; then
  cursor=""; i=0
  while :; do
    i=$((i+1))
    curl -s -m 60 -H "Authorization: Token $READWISE_TOKEN" \
      "https://readwise.io/api/v2/export/?pageCursor=$cursor" > "cache/export-$i.json"
    cursor=$(jq -r '.nextPageCursor // empty' "cache/export-$i.json")
    [ -z "$cursor" ] && break; [ $i -gt 40 ] && break
  done
fi
[ -s cache/export-1.json ] || { echo "NO CACHE and no READWISE_TOKEN: cannot verify quotes" >&2; exit 1; }

# 2. Rebuild the highlight index and book list.
jq -r '.results[] as $b | $b.highlights[] | [$b.title, $b.author, .text] | @tsv' \
  cache/export-*.json > work/highlights.tsv
jq -r '.results[] | [.title, .author, (.highlights|length), .category] | @tsv' \
  cache/export-*.json | sort -u > work/books.tsv
echo "highlights indexed: $(wc -l < work/highlights.tsv)  distinct books: $(wc -l < work/books.tsv)"

# 3. Verify every dossier/lesson quote verbatim against the cache (exit 1 on any miss).
fail=0
while IFS= read -r q; do
  [ -z "$q" ] && continue
  if ! grep -qF -- "$q" work/highlights.tsv; then echo "QUOTE MISS: $q"; fail=1; fi
done <<'EOF'
Delete any part or process you can. You may have to add them back later. In fact, if you do not end up adding back at least 10% of them, then you didn’t delete enough.
The only rules are the ones dictated by the laws of physics. Everything else is a recommendation.
The learning principle is to plunge into the detailed mystery of the micro in order to understand what makes the macro tick.
The more uncertainty, the more role for optionality to kick in, and the more you will outperform.
The first principle is that you must not fool yourself—and you are the easiest person to fool.
EOF
[ $fail -eq 0 ] && echo "all 5 quotes verbatim: OK"
[ $fail -eq 1 ] && exit 1

# 4. The decisive arithmetic (prints the dossier's tables, writes work/derived.json).
python3 rekick_arith.py
