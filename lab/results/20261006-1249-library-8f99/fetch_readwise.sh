#!/usr/bin/env bash
# Fetch the full Readwise export (books + highlights), cache compactly.
set -euo pipefail
OUT="${1:-readwise.json}"
TMP="$OUT.pages"
: > "$TMP"
cursor=""
pages=0
while : ; do
  if [ -n "$cursor" ]; then
    resp=$(curl -s -G -H "Authorization: Token $READWISE_TOKEN" \
      --data-urlencode "pageCursor=$cursor" "https://readwise.io/api/v2/export/")
  else
    resp=$(curl -s -H "Authorization: Token $READWISE_TOKEN" "https://readwise.io/api/v2/export/")
  fi
  echo "page $pages: $(printf '%s' "$resp" | jq '.results | length') books" >&2
  printf '%s\n' "$resp" >> "$TMP"
  pages=$((pages+1))
  cursor=$(printf '%s' "$resp" | jq -r '.nextPageCursor // empty')
  if [ -z "$cursor" ]; then break; fi
done
jq -s '{books: ([.[].results[]?] | map({user_book_id, title, author, category})),
        highlights: ([.[].results[].highlights[]?] | map({book_id, text}))}' "$TMP" > "$OUT"
rm -f "$TMP"
echo "saved $OUT: $(jq '.books | length' "$OUT") books, $(jq '.highlights | length' "$OUT") highlights, $(wc -c < "$OUT") bytes"
