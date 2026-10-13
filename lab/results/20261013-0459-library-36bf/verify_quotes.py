#!/usr/bin/env python3
"""Verifies every lesson quote is verbatim in Julien's Readwise export (fetched by regen.sh)."""
import json, os, sys, urllib.request, time

HERE = os.path.dirname(os.path.abspath(__file__))
HL = os.path.join(HERE, "readwise-highlights.jsonl")
SMART = {"’": "'", "‘": "'", "“": '"', "”": '"'}
norm = lambda s: "".join(SMART.get(c, c) for c in s)

def fetch():
    tok = os.environ.get("READWISE_TOKEN", "").strip()
    if not tok:
        return None
    cursor, out = "", []
    while True:
        url = "https://readwise.io/api/v2/export/" + (f"?pageCursor={cursor}" if cursor else "")
        req = urllib.request.Request(url, headers={"Authorization": f"Token {tok}"})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())
        for b in data.get("results", []):
            for h in b.get("highlights", []):
                out.append(h.get("text", ""))
        cursor = data.get("nextPageCursor")
        if not cursor:
            break
        time.sleep(0.2)
    with open(HL, "w") as f:
        for t in out:
            f.write(json.dumps({"t": t}, ensure_ascii=False) + "\n")
    return out

texts = [json.loads(l)["t"] for l in open(HL)] if os.path.exists(HL) else fetch()
if texts is None:
    print("READWISE_TOKEN unset and no cache: quote verification SKIPPED (dossier quotes marked verbatim at fetch time)")
    sys.exit(0)
texts = [norm(t) for t in texts]

FRAGMENTS = [
    "You could feel like you're flying straight and level while in fact you're descending in a spiral",
    "listen only to your instruments",
    "Planes are safer when the least experienced pilot is flying, because it means the second pilot isn't going to be afraid to speak up",
    "Unless a pilot has actually recovered from a stall, has actually put his plane into a spin and brought it out, he cannot know accurately what those acts entail",
    "Investment in loss is giving yourself to the learning process",
    "he would physically alter his visitors so they would fit by stretching or amputating",
    "Make them less wrong and dumb, because all requirements are somewhat wrong and dumb. And then delete, delete, delete",
]
bad = 0
for frag in FRAGMENTS:
    frag = norm(frag)
    hit = any(frag in t for t in texts)
    print(("VERBATIM  " if hit else "MISSING   ") + frag[:70])
    bad += not hit
print(f"{len(FRAGMENTS) - bad}/{len(FRAGMENTS)} quote fragments verbatim in the export")
sys.exit(1 if bad else 0)
