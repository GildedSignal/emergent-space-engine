#!/usr/bin/env python3
"""Analysis of results.json: T-exponents per payload order, jerk-linearity,
controls, beta-scaling, channel test (delta-v vs delta-x)."""
import json, math, sys

R = json.load(open(sys.argv[1] if len(sys.argv)>1 else "results.json"))
def get(**kw):
    def m(r):
        return all(r[k] == v if isinstance(v, str) else abs(r[k]-v) < 1e-18 for k, v in kw.items())
    return [r for r in R if m(r)]

def slope(xs, ys):
    n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
    sxy=sum((x-mx)*(y-my) for x,y in zip(xs,ys)); sxx=sum((x-mx)**2 for x in xs)
    return sxy/sxx if sxx else float('nan')

print("== 1. T-exponents (log scar vs log T), per case/beta/order ==")
for case in ("A_const_burn","B_burn+jerk","C_pure_jerk"):
    for beta in (0.003,0.03,0.3):
        row=[]
        for order,rn,lbl in ((1,"ret","O1"),(2,"ret","O2"),(3,"ret","O3"),(1,"now","now1")):
            pts=sorted([(r["Tf"],r["per_rebind"]) for r in get(beta=beta,case=case,order=order,readout=rn)])
            xs=[math.log(p) for p,_ in pts]; ys=[math.log(max(y,1e-300)) for _,y in pts]
            row.append("%s %.3f"%(lbl,slope(xs,ys)))
        print("%-13s b=%.3f  slopes: %s"%(case,beta,"  ".join(row)))

print("\n== 2. absolute scars at T=P/64 ==")
for case in ("A_const_burn","B_burn+jerk","C_pure_jerk"):
    for beta in (0.003,0.03,0.3):
        vals=[]
        for order,rn,lbl in ((1,"ret","O1"),(2,"ret","O2"),(3,"ret","O3"),(1,"now","now1")):
            m=get(beta=beta,case=case,order=order,readout=rn,Tf=1/64.0)
            vals.append("%s %.3e"%(lbl,m[0]["per_rebind"] if m else float('nan')))
        print("%-13s b=%.3f  %s"%(case,beta,"  ".join(vals)))

print("\n== 3. jerk-linearity (case C, O2, T=P/64): scar(C_x0.5)/C, /C_x2 ==")
for beta in (0.003,0.03,0.3):
    c1=get(beta=beta,case="C_pure_jerk",order=2,Tf=1/64.0)[0]["per_rebind"]
    ch=get(beta=beta,case="C_x0.5",order=2,Tf=1/64.0)[0]["per_rebind"]
    c2=get(beta=beta,case="C_x2",order=2,Tf=1/64.0)[0]["per_rebind"]
    print("b=%.3f  half/full=%.3f  double/full=%.3f"%(beta,ch/c1,c2/c1))
print("== 3b. a-linearity (case A, O1, T=P/64) ==")
for beta in (0.003,0.03,0.3):
    c1=get(beta=beta,case="A_const_burn",order=1,Tf=1/64.0)[0]["per_rebind"]
    ch=get(beta=beta,case="A_x0.5",order=1,Tf=1/64.0)[0]["per_rebind"]
    c2=get(beta=beta,case="A_x2",order=1,Tf=1/64.0)[0]["per_rebind"]
    print("b=%.3f  half/full=%.3f  double/full=%.3f"%(beta,ch/c1,c2/c1))

print("\n== 4. free-fall control (no thrust): O1 scar at T=P/64 ==")
for beta in (0.003,0.03,0.3):
    f=get(beta=beta,case="F_freefall",order=1,Tf=1/64.0)[0]
    a=get(beta=beta,case="A_const_burn",order=1,Tf=1/64.0)[0]
    print("b=%.3f  freefall %.3e  vs const-burn %.3e  (ratio %.2e)"%(beta,f["per_rebind"],a["per_rebind"],f["per_rebind"]/a["per_rebind"]))

print("\n== 5. beta-scaling of O1 scar (case A, T=P/64) and C(beta^2/2 * dv/v) ==")
ref=[]
for beta in (0.003,0.03,0.3):
    m=get(beta=beta,case="A_const_burn",order=1,Tf=1/64.0)[0]
    C=m["per_rebind"]/((beta*beta/2.0)*(m["dv_mid"]/beta))
    ref.append(C); print("b=%.3f  scar %.3e  C=%.3f"%(beta,m["per_rebind"],C))
print("C spread across beta: %.2f"%(max(ref)/min(ref)))

print("\n== 6. step-size control (case A anchor, O1) ==")
c1=get(case="conv_h1024",order=1)[0]["per_rebind"]; c4=get(case="conv_h4096",order=1)[0]["per_rebind"]
print("h=P/1024: %.4e   h=P/4096: %.4e   ratio %.4f"%(c1,c4,c1/c4))

print("\n== 7. now1 readout: per-rebind slope in T, and TOTAL scar per orbit (cadence test) ==")
for beta in (0.003,0.03,0.3):
    pts=sorted([(r["Tf"],r["per_rebind"]) for r in get(beta=beta,case="A_const_burn",order=1,readout="now")])
    xs=[math.log(t) for t,_ in pts]; ys=[math.log(max(s,1e-300)) for _,s in pts]
    tot=[(t, s/t) for t,s in pts]   # per-rebind * n_windows(=P/T) = total scar per period
    print("b=%.3f  per-rebind slope %.3f   total/P at T=P/256..P/8: %s"%(
        beta, slope(xs,ys), " ".join("%.2e"%(s) for _,s in tot)))

print("\n== 8. O2/O1 floor check (case A) and sign control (case C) ==")
for beta in (0.003,0.03,0.3):
    r=[]
    for Tf in (1/256.0,1/64.0,1/8.0):
        o1=get(beta=beta,case="A_const_burn",order=1,Tf=Tf)[0]["per_rebind"]
        o2=max(get(beta=beta,case="A_const_burn",order=2,Tf=Tf)[0]["per_rebind"],1e-300)
        r.append("T=P/%d: %.1e"%(round(1/Tf),o1/o2))
    print("b=%.3f  %s"%(beta,"  ".join(r)))
    cp=get(beta=beta,case="C_pure_jerk",order=2,Tf=1/64.0)
    cn=get(beta=beta,case="C_neg",order=2,Tf=1/64.0)
    print("        sign control: |C+|/|C-| = %.3f (1 = clean sign flip)"%(
        cp[0]["per_rebind"]/max(cn[0]["per_rebind"],1e-300)))

print("\n== 9. the adoption row: scar at kick-like cadence T=P/32, case B (burn+jerk) ==")
for beta in (0.003,0.03,0.3):
    row=[]
    for order,rn,lbl in ((1,"ret","O1"),(2,"ret","O2"),(3,"ret","O3"),(1,"now","now1")):
        m=get(beta=beta,case="B_burn+jerk",order=order,readout=rn,Tf=1/32.0)
        row.append("%s %.2e"%(lbl,m[0]["per_rebind"] if m else float('nan')))
    print("b=%.3f  %s"%(beta,"  ".join(row)))
