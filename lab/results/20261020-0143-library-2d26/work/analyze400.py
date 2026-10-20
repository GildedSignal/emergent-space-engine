BUD=12.0
rows=[tuple(map(float,l.split())) for l in open("f200000_burn400.txt")]
rows=[r for r in rows if r[0]>=60]
ms=sorted(r[1] for r in rows); p50=ms[len(ms)//2]
on=next(i for i,r in enumerate(rows) if r[1]>3*BUD)
pre=sum(max(0,BUD-r[1]) for r in rows[:on]); exc=sum(max(0,r[1]-BUD) for r in rows)
print(f"rtf400 2e5: frames {len(rows)} p50 {p50:.3f} ({p50/BUD:.3f}) onset_frame {int(rows[on][0])} slack_pre {pre:.0f} ms excess {exc:.0f} ms coverage {pre/exc:.2f} lag_max {max(r[3] for r in rows):.2f} end {rows[-1][3]:.2f}")
cov=lambda K: pre/(exc*(K/2e5)**1.244)
print("composed coverage at rtf400: 1e5 %.1f 3e5 %.2f 1e6 %.2f 1e9 %.1e" % (cov(1e5),cov(3e5),cov(1e6),cov(1e9)))
