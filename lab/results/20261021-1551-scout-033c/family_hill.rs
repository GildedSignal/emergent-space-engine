// The child-doll family certificate vs the Fermi lattice's linear tide (formation-family od 4).
// f64 mirror of the shipped kick formulas, verbatim structure:
//   force.rs::pull            gm*(xj-x)/|xj-x|^3
//   events/kicks.rs::parent_tide  pull(centre+offset) - pull(centre)   (full differential, never linear)
//   force.rs::origin_fall     cancels exactly between same-doll members (uniform vector)
// The doll's dominant body is the compiled geodesic (shared tube, zero differential) - force.rs's own split.
// Word: w11 (a877), quantum q = 2^-11 * v_body, sigma-delta carry at 2^-16 q (step.rs::quantize's scheme).
// Units: root (GM_star = 1, c = 1). Constants: scenario.rs (Home 2^-18, Giant 2^-10, Cinder 2^-21,
// Moon 2^-24 periapsis 260000 e 1/20; belt 2-3 AU; fleet lattice radius 4740).
use std::f64::consts::TAU;

#[derive(Clone, Copy)]
struct Planet { gm: f64, a: f64, e: f64, w: f64, m0: f64 }

fn kepler(p: &Planet, t: f64) -> (f64, f64) { // position in the star's frame
    let n = TAU / (TAU * (p.a * p.a * p.a).sqrt());
    let mut m = p.m0 + n * t;
    m %= TAU;
    let mut e = m;
    for _ in 0..40 { e -= (e - p.e * e.sin() - m) / (1.0 - p.e * e.cos()); }
    let xp = p.a * (e.cos() - p.e);
    let yp = p.a * (1.0 - p.e * p.e).sqrt() * e.sin();
    let (sw, cw) = (p.w.sin(), p.w.cos());
    (xp * cw - yp * sw, xp * sw + yp * cw)
}

fn pull(gm: f64, xj: (f64, f64), x: (f64, f64)) -> (f64, f64) {
    let (dx, dy) = (xj.0 - x.0, xj.1 - x.1);
    let r2 = dx * dx + dy * dy;
    let k = gm / (r2 * r2.sqrt());
    (dx * k, dy * k)
}
fn parent_tide(mass: f64, centre: (f64, f64), off: (f64, f64)) -> (f64, f64) {
    let a = pull(mass, (centre.0 + off.0, centre.1 + off.1), (0.0, 0.0));
    let o = pull(mass, centre, (0.0, 0.0));
    (a.0 - o.0, a.1 - o.1)
}

// The doll's kick field at x (doll frame), minus the dominant body's geodesic.
// star doll: secondaries = planets. home doll: secondary = moon, tide = star.
fn field(doll: u8, x: (f64, f64), t: f64, home: &Planet, giant: &Planet, cinder: &Planet, moon: &(f64, f64, f64, f64)) -> (f64, f64) {
    let mut a = (0.0, 0.0);
    if doll == 0 {
        for p in [cinder, home, giant] {
            let pj = kepler(p, t);
            let q = pull(p.gm, pj, x);
            a = (a.0 + q.0, a.1 + q.1);
        }
    } else {
        let hp = kepler(home, t);
        let mp = (hp.0 + moon.0, hp.1 + moon.1); // moon rel->root
        let q = pull(2f64.powi(-24), mp, (hp.0 + x.0, hp.1 + x.1)); // x is Home-frame; pull is frame-covariant
        let tt = parent_tide(1.0, hp, x);
        a = (q.0 + tt.0, q.1 + tt.1);
    }
    a
}

fn moon_rel(t: f64) -> (f64, f64, f64, f64) { // (x,y in Home frame, and unused) Kepler a=273684 e=0.05
    let a = 260000.0 / 0.95;
    let n = 1.0 / (a * a * a / 2f64.powi(-24)).sqrt();
    let m = 0.7 % TAU + n * t;
    let mut e = m;
    for _ in 0..40 { e -= (e - 0.05 * e.sin() - m) / (1.0 - 0.05 * e.cos()); }
    let xp = a * (e.cos() - 0.05);
    let yp = a * (1.0f64 - 0.0025).sqrt() * e.sin();
    (xp, yp, 0.0, 0.0)
}

// sigma-delta word (step.rs::quantize): dv in quanta, carry at 2^-16 q; out = whole quanta.
fn word(dv: (f64, f64), carry: &mut (f64, f64)) -> (i64, i64) {
    let t0 = carry.0 + dv.0 * 65536.0;
    let t1 = carry.1 + dv.1 * 65536.0;
    let o0 = (t0 / 65536.0).trunc();
    let o1 = (t1 / 65536.0).trunc();
    *carry = (t0 - o0 * 65536.0, t1 - o1 * 65536.0);
    (o0 as i64, o1 as i64)
}

struct ArmOut { xi_mean: f64, xi_p99: f64, first_fork: u64, disagree: u64, h_eff: f64, lat_xi_mean: f64, lat_first: u64 }

// One arm: family of 2 members at arc dx on a circular orbit r in the doll; K kicks of h.
// family fork: quantized words of (h*a_m) vs (h*a_ref) disagree.
// lattice fork: quantized words of (h*a_m) vs (h*a_ref + h*J*s) disagree (J from the centre, eps=1 root).
fn arm(doll: u8, r: f64, dx: f64, home: &Planet, giant: &Planet, cinder: &Planet, k_max: u64) -> ArmOut {
    let gm_doll = if doll == 0 { 1.0 } else { 2f64.powi(-18) };
    let n = (gm_doll / (r * r * r)).sqrt();
    let h = TAU / n / 16.0; // the board's own-orbit floor (kick-cadence cbe6)
    let v = (gm_doll / r).sqrt();
    let q = 2f64.powi(-11) * v;
    let th0 = 0.3;
    let mut c_r = (0.0, 0.0); // family: ref's carry
    let mut c_m = (0.0, 0.0);
    let mut c_lr = (0.0, 0.0); // lattice: prediction's carry
    let mut c_lm = (0.0, 0.0);
    let (mut first_fork, mut first_lat, mut disagree) = (0u64, 0u64, 0u64);
    let (mut s_xi, mut s_lat, mut s_heff, mut cnt) = (0.0f64, 0.0f64, 0.0f64, 0u64);
    let mut xis: Vec<f64> = Vec::new();
    let dth = dx / r;
    for k in 0..k_max {
        let t = k as f64 * h;
        let th = th0 + n * t;
        let pos = |a: f64| (r * a.cos(), r * a.sin());
        let x0 = pos(th);
        let xm = pos(th + dth);
        let mr = moon_rel(t);
        let a0 = field(doll, x0, t, home, giant, cinder, &mr);
        let am = field(doll, xm, t, home, giant, cinder, &mr);
        let d = (am.0 - a0.0, am.1 - a0.1);
        let xi = (d.0 * d.0 + d.1 * d.1).sqrt() * h / q;
        s_xi += xi; s_heff += (d.0 * d.0 + d.1 * d.1).sqrt() / dx; xis.push(xi); cnt += 1;
        // lattice: Jacobian at the family centre
        let e = 1.0f64;
        let fpx = field(doll, (x0.0 + e, x0.1), t, home, giant, cinder, &mr);
        let fmx = field(doll, (x0.0 - e, x0.1), t, home, giant, cinder, &mr);
        let fpy = field(doll, (x0.0, x0.1 + e), t, home, giant, cinder, &mr);
        let fmy = field(doll, (x0.0, x0.1 - e), t, home, giant, cinder, &mr);
        let j00 = (fpx.0 - fmx.0) / (2.0 * e); let j10 = (fpx.1 - fmx.1) / (2.0 * e);
        let j01 = (fpy.0 - fmy.0) / (2.0 * e); let j11 = (fpy.1 - fmy.1) / (2.0 * e);
        let s = (xm.0 - x0.0, xm.1 - x0.1);
        let lin = (j00 * s.0 + j01 * s.1, j10 * s.0 + j11 * s.1);
        let res = (d.0 - lin.0, d.1 - lin.1);
        let xi_lat = (res.0 * res.0 + res.1 * res.1).sqrt() * h / q;
        s_lat += xi_lat;
        // words
        let wr = word((h * a0.0 / q, h * a0.1 / q), &mut c_r);
        let wm = word((h * am.0 / q, h * am.1 / q), &mut c_m);
        if (wm.0 != wr.0 || wm.1 != wr.1) && first_fork == 0 { first_fork = k + 1; }
        if wm.0 != wr.0 || wm.1 != wr.1 { disagree += 1; }
        let pl = (h * (a0.0 + lin.0) / q, h * (a0.1 + lin.1) / q);
        let wlr = word(pl, &mut c_lr);
        let wlm = word((h * am.0 / q, h * am.1 / q), &mut c_lm);
        if (wlm.0 != wlr.0 || wlm.1 != wlr.1) && first_lat == 0 { first_lat = k + 1; }
    }
    xis.sort_by(|a, b| a.partial_cmp(b).unwrap());
    ArmOut { xi_mean: s_xi / cnt as f64, xi_p99: xis[(cnt as usize * 99 / 100)], first_fork, disagree, h_eff: s_heff / cnt as f64, lat_xi_mean: s_lat / cnt as f64, lat_first: first_lat }
}

fn main() {
    let home = Planet { gm: 2f64.powi(-18), a: 99_300_000.0 / 0.98, e: 0.02, w: 0x9000_0000u32 as f64 / 2f64.powi(32) * TAU, m0: 0x2000_0000u32 as f64 / 2f64.powi(32) * TAU };
    let giant = Planet { gm: 2f64.powi(-10), a: 500_000_000.0 / 0.95, e: 0.05, w: 0xC000_0000u32 as f64 / 2f64.powi(32) * TAU, m0: 0xA000_0000u32 as f64 / 2f64.powi(32) * TAU };
    let cinder = Planet { gm: 2f64.powi(-21), a: 35_600_000.0 / 0.9, e: 0.1, w: 0x3000_0000u32 as f64 / 2f64.powi(32) * TAU, m0: 0x5000_0000u32 as f64 / 2f64.powi(32) * TAU };
    let k = 1u64 << 17;
    println!("domain,r_root,dx_root,xi_mean,xi_p99,first_fork,disagree_frac,h_eff_mean,lat_xi_mean,lat_first_fork");
    let au = 101_300_000.0;
    let arms: Vec<(&str, u8, f64)> = vec![
        ("star1AU", 0, au * 1.0), ("star1.3AU", 0, au * 1.3),
        ("belt4to1", 0, au * 2.06), ("belt3to1", 0, au * 2.533), ("beltplain", 0, au * 2.8),
        ("home4740", 1, 4740.0), ("home47400", 1, 47400.0), ("home150000", 1, 150000.0),
    ];
    for (name, doll, r) in &arms {
        for dx in [1e3, 1e4, 5e4, 1e5, 5e5, 1e6] {
            let o = arm(*doll, *r, dx, &home, &giant, &cinder, k);
            println!("{},{},{:.0e},{:.3e},{:.3e},{},{:.4},{:.3e},{:.3e},{}",
                name, r, dx, o.xi_mean, o.xi_p99, o.first_fork, o.disagree as f64 / k as f64, o.h_eff, o.lat_xi_mean, o.lat_first);
        }
    }
}
