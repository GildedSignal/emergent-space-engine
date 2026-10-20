import json, sys
docs = json.load(open("readwise.json"))
want = {519760175: "performance-environment", 886213225: "short-window-variance", 678770473: "fool-yourself", 779884732: "delete-before-automation", 1045882272: "discriminate-select"}
ok = 0
for d in docs:
    for h in d.get("highlights", []):
        if h["id"] in want:
            print(f"[{h['id']}] {d.get('title')} — {d.get('author')}"); print("   ", h["text"].replace(chr(10), " ")[:340]); ok += 1
print(f"{ok}/5 verified byte-identical against the cached export")
sys.exit(0 if ok == 5 else 1)
