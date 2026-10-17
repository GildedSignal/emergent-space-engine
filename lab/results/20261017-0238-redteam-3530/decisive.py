#!/usr/bin/env python3
"""Decisive run: price the two-body doll's comparable-mass strong-field flank (nu = 1/4).
Outputs flank.json + printed tables. Run controls first (must PASS)."""
import json
import math
import eob_flank as E

out = {"controls_passed": None}

# ---- ISCO table: nu x order ------------------------------------------------
isco_rows = []
for nu in [0.0, 0.05, 0.1, 0.25]:
    for order in ["1pn", "2pn", "3pn"]:
        r = E.isco(nu, order)
        if r is None:
            isco_rows.append(dict(nu=nu, order=order, r=None, j=None,
                                  Eb_per_mu=None, Omega=None, x=None,
                                  note="no ISCO: h decreases monotonically to the light ring"))
            print(f"ISCO nu={nu:.2f} {order}: NO ISCO (monotone to light ring)")
            continue
        isco_rows.append(dict(nu=nu, order=order, **r))
        print(f"ISCO nu={nu:.2f} {order}: r={r['r']:.4f} j={r['j']:.4f} "
              f"Eb/mu={r['Eb_per_mu']:.6f} Om={r['Omega']:.6f} x={r['x']:.5f}")
out["isco"] = isco_rows

# doc law ISCO at nu=1/4 through the energy map (the only place nu enters)
u6 = 1.0 / 6.0
j, h, hr, Om = E.circular_at_u(u6, 0.25, "1pn")
map_Eb = (hr - 1.0) / 0.25
out["doc_isco_nu025_map"] = dict(r=6.0, j=j, Eb_per_mu=map_Eb, Omega=Om)
print(f"doc law nu=1/4 at r=6 through the map: Eb/mu={map_Eb:.6f}")

# energy-map pathology at the effective horizon
out["map_horizon"] = dict(nu=0.25, E_real_at_Eeff0=math.sqrt(1 - 2 * 0.25),
                          binding_fraction=1 - math.sqrt(0.5))
print(f"map at E_eff=0, nu=1/4: E_real={math.sqrt(0.5):.4f} "
      f"(binding {100*(1-math.sqrt(0.5)):.1f}% of M c^2)")


# ---- periastron matrix (doc law vs 2PN truth), same turning radii ----------
peri_rows = []
for pN, eN in [(1000, 0.2), (100, 0.2), (40, 0.5), (20, 1e-3), (20, 0.3), (20, 0.6),
               (12, 1e-3), (12, 0.3), (12, 0.5), (8, 1e-3), (8, 0.3)]:
    umin, umax = (1 - eN) / pN, (1 + eN) / pN
    doc = E.periastron(umin, umax, 0.25, "1pn")
    t2 = E.periastron(umin, umax, 0.25, "2pn")
    t2q = E.periastron(umin, umax, 0.25, "2pn", with_Q=True)
    t3 = E.periastron(umin, umax, 0.25, "3pn")  # A at 3PN, D at 2PN: trend check only
    if doc is None or t2 is None:
        print(f"p={pN} e={eN}: no bound orbit through those turning points")
        continue
    adv_doc, adv_t2, adv_t2q = doc - 2 * math.pi, t2 - 2 * math.pi, (t2q or t2) - 2 * math.pi
    rel = (adv_doc - adv_t2) / adv_t2
    relq = (adv_doc - adv_t2q) / adv_t2q
    tol_b11 = 0.01 + 2 * 8 / pN
    row = dict(p=pN, e=eN, adv_doc=adv_doc, adv_2pn=adv_t2, adv_2pn_Q=adv_t2q,
               rel=rel, rel_Q=relq, adv_3pn=(t3 - 2 * math.pi) if t3 else None,
               b11_tol=tol_b11, exceeds_b11_tol=bool(abs(rel) > tol_b11))
    peri_rows.append(row)
    print(f"peri p={pN:5g} e={eN:g}: doc={adv_doc:9.5f} 2PN={adv_t2:9.5f} "
          f"rel={100*rel:6.3f}% (Q: {100*relq:6.3f}%) B11tol={100*tol_b11:.2f}% "
          f"{'EXCEEDS' if abs(rel)>tol_b11 else 'within'}")
out["periastron_nu025"] = peri_rows

# ---- circular binding curve at fixed x (nu=1/4): doc vs 3PN ----------------
circ_rows = []
for u in [0.01, 0.02, 0.04, 0.08, 0.12, 0.16]:
    jd, hd, hrd, Omd = E.circular_at_u(u, 0.25, "1pn")
    j3, h3, hr3, Om3 = E.circular_at_u(u, 0.25, "3pn")
    eb_doc = (hrd - 1) / 0.25
    eb_3pn = (hr3 - 1) / 0.25
    row = dict(u=u, r=1 / u, Eb_doc=eb_doc, Eb_3pn=eb_3pn,
               rel=(eb_doc - eb_3pn) / eb_3pn)
    circ_rows.append(row)
    print(f"circ r={1/u:6.2f}: Eb/mu doc={eb_doc:.6f} 3PN={eb_3pn:.6f} "
          f"rel={100*(eb_doc-eb_3pn)/eb_3pn:6.2f}% (x={Om3**(2/3):.4f})")
out["circular_binding_nu025"] = circ_rows

with open("flank.json", "w") as f:
    json.dump(out, f, indent=1)
print("wrote flank.json")
