//! The relativistic bounce: the speed limit under extreme mass ratios, exact 4-momentum of
//! the rule, an independent centre-of-momentum check, the Newtonian limit, both arithmetic
//! paths, and exact ledgers with bounded carries over a million collisions.
use emergent_lattice::{
    law::{self, Body, Response},
    relativity::{self, four_momentum},
    worlds::Rng,
};
use num_bigint::BigInt;

const Q: i64 = 1024;

fn ball(id: u64, x: [i64; 2], k: [i64; 2], mass: i64) -> Body {
    Body { id, x, k, mass, radius: Q, response: Response::Bounce, residual: 0, rev: 0 }
}

fn inside(k: [i64; 2]) -> bool {
    (k[0] as i128).pow(2) + (k[1] as i128).pow(2) < (Q as i128).pow(2)
}

/// Random approaching pair at contact distance with velocities inside the light cone.
fn pair(rng: &mut Rng, vmax: i64, mmax: i64) -> [Body; 2] {
    loop {
        let ang = rng.range(0, 6283) as f64 / 1000.0;
        let d = [((2 * Q) as f64 * ang.cos()).round() as i64, ((2 * Q) as f64 * ang.sin()).round() as i64];
        let ka = [rng.range(-vmax, vmax), rng.range(-vmax, vmax)];
        let kb = [rng.range(-vmax, vmax), rng.range(-vmax, vmax)];
        let a = ball(1, [0, 0], ka, rng.range(1, mmax));
        let b = ball(2, d, kb, rng.range(1, mmax));
        if inside(ka) && inside(kb) && law::dot(law::sub(b.x, a.x), law::sub(kb, ka)) < 0 {
            return [a, b];
        }
    }
}

fn bounce(p: &[Body; 2]) -> ([Body; 2], [[i64; 2]; 2]) {
    let mut bodies = p.clone();
    let mut carry = [[0i64; 2]; 2];
    let mut wm = [0i128; 2];
    relativity::resolve(Q, &mut bodies, &mut carry, &[(0, 1)], &[false, false], None, &mut wm);
    (bodies, carry)
}

#[test]
fn nothing_massive_reaches_c() {
    let mut rng = Rng(1);
    let mut newtonian_breaks = 0;
    for _ in 0..20_000 {
        // Heavy fast bodies hitting light ones: Newtonian bounces exceed c here.
        let mut p = pair(&mut rng, Q * 9 / 10, 1);
        p[0].mass = 1 << rng.range(0, 12);
        let (out, _) = bounce(&p);
        assert!(inside(out[0].k) && inside(out[1].k), "{p:?} -> {out:?}");
        let mut n = p.clone();
        let mut wm = [0i64; 2];
        law::resolve(&mut n, &[(0, 1)], &[false, false], None, &mut wm);
        newtonian_breaks += (!inside(n[0].k) || !inside(n[1].k)) as u32;
    }
    assert!(newtonian_breaks > 1000, "the fixture must stress the limit ({newtonian_breaks} Newtonian violations)");
}

#[test]
fn the_rule_conserves_four_momentum_exactly_and_keeps_mass_shells() {
    let mut rng = Rng(2);
    let mdot = |x: &[BigInt; 3], y: &[BigInt; 3]| &x[0] * &y[0] - &x[1] * &y[1] - &x[2] * &y[2];
    for _ in 0..5_000 {
        let p = pair(&mut rng, Q - 1, 1 << 10);
        let (pa, pb) = (four_momentum(p[0].mass, p[0].k, Q), four_momentum(p[1].mass, p[1].k, Q));
        let (na, nb, t) = relativity::exact_outcome(pa, pb, law::sub(p[1].x, p[0].x)).expect("approaching pairs exchange");
        let (ba, bb) = (pa.map(BigInt::from), pb.map(BigInt::from));
        for i in 0..3 {
            assert_eq!(&na[i] + &nb[i], &t * (&ba[i] + &bb[i]), "4-momentum component {i}");
        }
        assert_eq!(mdot(&na, &na), &t * &t * mdot(&ba, &ba), "mass shell a");
        assert_eq!(mdot(&nb, &nb), &t * &t * mdot(&bb, &bb), "mass shell b");
        // Future-directed: energies keep the sign of T·E.
        assert!((&na[0] * &t) > BigInt::from(0) && (&nb[0] * &t) > BigInt::from(0));
    }
}

/// Independent formulation in floating point: boost to the centre-of-momentum frame, where
/// the rule must be a mirror reflection of each spatial momentum along the boosted normal.
#[test]
fn centre_of_momentum_frame_sees_a_mirror_bounce() {
    let mut rng = Rng(3);
    for _ in 0..5_000 {
        let p = pair(&mut rng, Q * 95 / 100, 64);
        let (pa, pb) = (four_momentum(p[0].mass, p[0].k, Q), four_momentum(p[1].mass, p[1].k, Q));
        let d = law::sub(p[1].x, p[0].x);
        let (na, _, t) = relativity::exact_outcome(pa, pb, d).unwrap();
        let f = |v: &BigInt| v.to_string().parse::<f64>().unwrap();
        let tf = f(&t);
        let pa2: Vec<f64> = na.iter().map(|v| f(v) / tf).collect();
        let (pt, n0) = ([(pa[0] + pb[0]) as f64, (pa[1] + pb[1]) as f64, (pa[2] + pb[2]) as f64], [0.0, d[0] as f64, d[1] as f64]);
        let beta = [pt[1] / pt[0], pt[2] / pt[0]];
        let b2 = beta[0] * beta[0] + beta[1] * beta[1];
        let g = 1.0 / (1.0 - b2).sqrt();
        let boost = |v: &[f64]| -> [f64; 3] {
            let bp = beta[0] * v[1] + beta[1] * v[2];
            let e = g * (v[0] - bp);
            let s = if b2 > 0.0 { (g - 1.0) * bp / b2 - g * v[0] } else { 0.0 };
            [e, v[1] + s * beta[0], v[2] + s * beta[1]]
        };
        // The lab normal N = (d·P/E, d) is orthogonal to P; in the CM frame it is spatial.
        let dp = d[0] as f64 * pt[1] + d[1] as f64 * pt[2];
        let nn = boost(&[dp / pt[0], n0[1], n0[2]]);
        let (a0, a1) = (boost(&pa.map(|v| v as f64)), boost(&pa2));
        let scale = a0[0].abs().max(1.0);
        assert!(nn[0].abs() <= 1e-9 * (nn[1].abs() + nn[2].abs()), "normal not spatial in CM: {nn:?}");
        let n2 = nn[1] * nn[1] + nn[2] * nn[2];
        let proj = (a0[1] * nn[1] + a0[2] * nn[2]) / n2;
        let mirror = [a0[0], a0[1] - 2.0 * proj * nn[1], a0[2] - 2.0 * proj * nn[2]];
        for i in 0..3 {
            assert!((mirror[i] - a1[i]).abs() <= 1e-9 * scale, "component {i}: mirror {mirror:?} rule {a1:?}");
        }
    }
}

/// At low speed the rule must land within one lattice quantum (plus O(β²)) of the exact,
/// unrounded Newtonian outcome. (The rounded Newtonian law is not the reference here: its
/// momentum lattice lcm(m_a, m_b)/Q moves a light body in steps of up to 4 quanta.)
#[test]
fn low_speeds_reduce_to_the_newtonian_bounce() {
    let mut rng = Rng(4);
    let mut worst = 0f64;
    for _ in 0..20_000 {
        let p = pair(&mut rng, Q / 64, 4);
        let (r, _) = bounce(&p);
        let d = law::sub(p[1].x, p[0].x);
        let w = law::sub(p[1].k, p[0].k);
        let (ma, mb) = (p[0].mass as f64, p[1].mass as f64);
        let j = 2.0 * ma * mb / (ma + mb) * law::dot(d, w) as f64 / law::dot(d, d) as f64;
        let exact = [
            [p[0].k[0] as f64 + j * d[0] as f64 / ma, p[0].k[1] as f64 + j * d[1] as f64 / ma],
            [p[1].k[0] as f64 - j * d[0] as f64 / mb, p[1].k[1] as f64 - j * d[1] as f64 / mb],
        ];
        for i in 0..2 {
            for c in 0..2 {
                worst = worst.max((r[i].k[c] as f64 - exact[i][c]).abs());
            }
        }
    }
    // β ≤ 1/64 · √2: the relativistic target moves by far less than 0.1 quantum.
    assert!(worst < 1.1, "relativistic bounce is {worst} quanta from the exact Newtonian outcome at v ≤ c/64");
}

#[test]
fn fast_and_exact_paths_agree() {
    let mut rng = Rng(5);
    for i in 0..20_000 {
        let p = pair(&mut rng, Q - 1, if i % 2 == 0 { 4 } else { 1 << 16 });
        let (pa, pb) = (four_momentum(p[0].mass, p[0].k, Q), four_momentum(p[1].mass, p[1].k, Q));
        let d = law::sub(p[1].x, p[0].x);
        let fast = relativity::targets(pa, pb, d, Q).unwrap();
        let (na, nb, _) = relativity::exact_outcome(pa, pb, d).unwrap();
        for (t, n) in [(fast.0, &na), (fast.1, &nb)] {
            for c in 0..2 {
                let exact_num = &n[1 + c] * Q;
                let (fl_fast, ce_fast) = (t.0[c].div_euclid(t.1), -(-t.0[c]).div_euclid(t.1));
                let e = &n[0];
                let (mut xn, mut xd) = (exact_num.clone(), e.clone());
                if xd < BigInt::from(0) {
                    xn = -xn;
                    xd = -xd;
                }
                let fl = { let (q, r) = (&xn / &xd, &xn % &xd); if r < BigInt::from(0) { q - 1 } else { q } };
                let ce = if &fl * &xd == xn { fl.clone() } else { &fl + 1 };
                assert_eq!((BigInt::from(fl_fast), BigInt::from(ce_fast)), (fl, ce));
            }
        }
    }
}

/// A million sequential collisions among 64 bodies: ledgers exact, carries bounded.
#[test]
fn ledgers_are_exact_and_carries_stay_bounded() {
    let mut rng = Rng(6);
    let n = 64;
    let mut bodies: Vec<Body> = (0..n).map(|i| ball(i as u64 + 1, [0, 0], [rng.range(-300, 300), rng.range(-300, 300)], rng.range(1, 3))).collect();
    let mut carry = vec![[0i64; 2]; n];
    let e0: i128 = bodies.iter().map(|b| four_momentum(b.mass, b.k, Q)[0]).sum();
    let p0: [i128; 2] = [1, 2].map(|c| bodies.iter().map(|b| four_momentum(b.mass, b.k, Q)[c]).sum());
    let mut worst = [0i128; 3];
    let mut worst_early = [0i128; 3];
    let rounds = 1_000_000;
    for round in 0..rounds {
        let i = rng.range(0, n as i64 - 2) as usize;
        let j = rng.range(i as i64 + 1, n as i64 - 1) as usize;
        let ang = rng.range(0, 6283) as f64 / 1000.0;
        let d = [((2 * Q) as f64 * ang.cos()).round() as i64, ((2 * Q) as f64 * ang.sin()).round() as i64];
        if law::dot([d[0] as i128, d[1] as i128], law::sub(bodies[j].k, bodies[i].k)) >= 0 {
            continue;
        }
        let mut pair = [bodies[i].clone(), bodies[j].clone()];
        pair[0].x = [0, 0];
        pair[1].x = d;
        let mut c = [carry[i], carry[j]];
        let mut wm = [0i128; 2];
        relativity::resolve(Q, &mut pair, &mut c, &[(0, 1)], &[false, false], None, &mut wm);
        for (slot, b) in [i, j].into_iter().zip(pair) {
            bodies[slot].k = b.k;
            bodies[slot].residual = b.residual;
        }
        carry[i] = c[0];
        carry[j] = c[1];
        for b in 0..n {
            let v = [bodies[b].residual as i128, carry[b][0] as i128, carry[b][1] as i128];
            for x in 0..3 {
                worst[x] = worst[x].max(v[x].abs());
                if round < rounds / 10 {
                    worst_early[x] = worst_early[x].max(v[x].abs());
                }
            }
        }
    }
    assert!(bodies.iter().all(|b| inside(b.k)));
    let e1: i128 = bodies.iter().map(|b| four_momentum(b.mass, b.k, Q)[0]).sum();
    let p1: [i128; 2] = [1, 2].map(|c| bodies.iter().map(|b| four_momentum(b.mass, b.k, Q)[c]).sum());
    assert_eq!(e1 - e0, bodies.iter().map(|b| b.residual as i128).sum::<i128>(), "energy ledger");
    for c in 0..2 {
        assert_eq!(p1[c] - p0[c], carry.iter().map(|x| x[c] as i128).sum::<i128>(), "momentum ledger {c}");
    }
    // Bounded, not a random walk: the last 90% of the run may not push any carry more than
    // twice past what the first 10% reached (a √n walk would grow about 3×).
    for x in 0..3 {
        assert!(worst[x] <= 2 * worst_early[x].max(1), "carry {x} grew: early {} total {}", worst_early[x], worst[x]);
    }
    eprintln!("worst carries (energy, px, py) {worst:?}, first tenth {worst_early:?}");
}
