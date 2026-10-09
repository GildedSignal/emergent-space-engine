#!/usr/bin/env bash
# Fetch the full Readwise export (paged) and cache it as one JSON per page.
set -u
OUT="$(dirname "$0")/readwise-pages"
mkdir -p "$OUT"
cursor=""
page=0
while : ; do
  page=$((page+1))
  if [ -n "$cursor" ]; then
    url="https://readwise.io/api/v2/export/?pageCursor=${cursor}"
  else
    url="https://readwise.io/api/v2/export/"
  fi
  curl -s --max-time 90 -H "Authorization: Token ${READWISE_TOKEN}" "$url" -o "$OUT/page-$page.json"
  # next cursor is a URL-safe token; extract with jq
  cursor=$(jq -r '.nextPageCursor // empty' "$OUT/page-$page.json")
  echo "page $page -> cursor: ${cursor:-<none>}"
  [ -z "$cursor" ] && break
  [ "$page" -ge 80 ] && { echo "page cap"; break; }
  sleep 0.3
done
echo "done, pages: $page"
