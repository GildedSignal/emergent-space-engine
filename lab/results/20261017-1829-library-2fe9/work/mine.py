import json, re, sys
books = json.load(open("readwise_books.json"))
themes = {
 "speed_vs_right_repr": r"fast.*(wrong|right)|right.*(representation|question)|representation|notation|change of variable|coordinate|reframe|water|fish",
 "delete_simplify": r"delete|delet|simplif|simplest|unnecessary|remove.*before|less is more|no part|subtract",
 "precompute_table": r"precomput|lookup|table|cache|cach|memoiz|amortiz|in advance|ahead of time|preprocess",
 "closed_form_vs_iter": r"closed.form|analytic|formula|equation.*solve|derive|derivation|approximat|iterat",
 "hot_loop_micro": r"inner loop|micro|nanosecond|microsecond|cycl|cache line|memory bandwidth|vectoriz|SIMD|assembl|machine code|branchless|bit trick|integer",
 "measure_tails": r"worst case|tail|p99|percentile|variance.*mean|average.*mislead|load|throttl",
 "batch_amortize": r"batch|bulk|once|pay once|economies of scale|fixed cost|marginal cost",
 "exactness": r"exact|rounding error|floating point|precision|deterministic|reproducib",
}
pat = {k: re.compile(v, re.I) for k, v in themes.items()}
hits = {}
for bid, b in books.items():
    for h in b["highlights"]:
        t = h["text"]
        for k, p in pat.items():
            if p.search(t):
                hits.setdefault(k, []).append((b["title"], b["author"], t, h["loc"]))
for k in themes:
    print(f"### {k}: {len(hits.get(k,[]))}")
