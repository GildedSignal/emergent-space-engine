import json, re, sys

docs = json.load(open("readwise.json"))
themes = {
    "setup": r"setup|changeover|switching cost|switch cost|batch",
    "bottleneck": r"bottleneck|constraint|throughput|theory of constraints|goldratt|little'?s law",
    "buffer": r"buffer|slack|redundanc|inventory|queue",
    "two_systems": r"system 1|system 2|fast thinking|slow thinking|cheap",
    "barbell": r"barbell|layered|layering|convex|optionality|middle ground",
    "algorithm": r"the algorithm|delete .{0,30}part|best part is no part|accelerate|automate|requirement",
    "machines": r"machines|computers|computing|punch|ibm",
    "circles": r"smaller circles|circle",
    "probes": r"probe|swarm|sensor|bandwidth|signal",
    "tail": r"tail|p99|worst case|extreme|variance|smooth",
    "amortize": r"amortiz|over time|frequent|rarer|rarely|often enough",
    "simplify": r"simplify|simplest|too complex|complexity is|essential",
}
for name, pat in themes.items():
    rx = re.compile(pat, re.I)
    out = []
    for d in docs:
        for h in d.get("highlights", []):
            t = h.get("text", "")
            if rx.search(t):
                out.append((d.get("title", "?")[:48], (d.get("author") or "?")[:24], t.strip().replace("\n", " ")))
    with open(f"q_{name}.txt", "w") as f:
        for ti, au, t in out:
            f.write(f"[{ti} -- {au}]\n{t}\n\n")
    print(name, len(out))
