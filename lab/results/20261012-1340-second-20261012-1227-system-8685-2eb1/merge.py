import glob, os
# merge split truth parts: keep one header, order by seed
for name, pat in [("belt-truth64.csv","belt-truth-s*.csv"), ("belt-truthfine64.csv","belt-truthfine-s*.csv"),
                  ("enc-truth64.csv","enc-truth-s*.csv"), ("enc-truthfine64.csv","enc-truthfine-s*.csv")]:
    parts = sorted(glob.glob(os.path.join("work/parts", pat)))
    rows = []
    for p in parts:
        lines = open(p).read().splitlines()
        rows.extend(lines[1:])
    rows.sort(key=lambda l: int(l.split(",")[2]))
    with open(os.path.join("work", name), "w") as f:
        f.write("config,variant,seed,kicks,solves,varpi_rate,e_rate,jacobi_max,a_end,e_end,ejected_at_sample,nfit\n")
        f.write("\n".join(rows) + "\n")
    print(name, len(rows), "seeds from", len(parts), "parts")
