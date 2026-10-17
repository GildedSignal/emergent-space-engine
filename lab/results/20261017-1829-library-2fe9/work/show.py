import json, re, sys
books = json.load(open("readwise_books.json"))
theme = sys.argv[1]
themes = {
 "hot_loop_micro": r"inner loop|micro|nanosecond|microsecond|cycl|cache line|memory bandwidth|vectoriz|SIMD|assembl|machine code|branchless|bit trick|integer",
 "exactness": r"exact|rounding error|floating point|precision|deterministic|reproducib",
 "speed_vs_right_repr": r"fast.*(wrong|right)|right.*(representation|question)|representation|change of variable|water|fish",
}
p = re.compile(themes[theme], re.I)
for bid, b in books.items():
    for h in b["highlights"]:
        t = h["text"]
        if p.search(t):
            print(f"[{b['author']} — {b['title']} @{h['loc']}]\n{t}\n")
