//! The relativistic response (`es-lattice-relativistic-v0`, Julien 25 September 2026:
//! "beyond c = 1 means paradoxes"). Positions, velocities, predicates and walls are the
//! lattice law's; only the bounce changes. Nothing massive can reach c: every outcome is a
//! lattice velocity with |k|² < Q², by construction.
//!
//! **Exact rule.** Each body carries a fixed-point 4-momentum
//! (E, p) = (m·Γ(k)·Q, m·Γ(k)·k) with Γ(k) = ⌊F·Q/√(Q² − |k|²)⌋ ≈ F·γ, exact integers.
//! A contact with separation d reflects both 4-momenta in the Minkowski hyperplane
//! orthogonal to N = (d·P, E_tot·d) (P the pair's total 4-momentum):
//!
//! p' = p − 2 (p·N)/(N·N) N.
//!
//! N·P = 0, so the total 4-momentum is conserved exactly; reflections preserve each
//! Minkowski norm, so each outgoing vector is on its mass shell and inside the light cone.
//! In the centre-of-momentum frame N is purely spatial, so this is the elastic bounce off
//! the (boosted) line of centres. At low speed it reduces to the Newtonian impulse
//! 2·m_a·m_b/(m_a+m_b)·(d·w)/|d|²·d. Everything is rational: no square root enters the rule.
//!
//! **Lattice.** The exact outgoing velocity Q·p'/E' is rational. Each body's candidates
//! are the floor/ceil lattice points around it that lie strictly inside the light cone
//! (truncation toward zero always does). Among the candidate pairs, the rule picks the one
//! that minimises |owed + e|², where e is the 4-momentum rounding error (energy, px, py) and
//! owed the pair's carry. It never keeps both velocities when the exact exchange is nonzero.
//! The error joins the lower id's carry: energy in `residual`, momentum in the momentum
//! carry. The ledgers are exact: ΣE(final) − ΣE(initial) = Σresidual, and
//! Σp(final) − Σp(initial) + wall momentum = Σcarry.
use crate::law::{dot, sub, Body, Container, Response, World};
use num_bigint::BigInt;

/// Fixed-point scale of γ: 2^16. At Q = 1024 the smallest kinetic step (|k| = 1) is
/// m·F/(2Q) = 32 units, well above Γ's flooring error of one unit.
pub const F: i128 = 1 << 16;

/// Γ(k) = ⌊F·Q/√(Q² − |k|²)⌋ (floor of a square root of a floor is exact). |k|² < Q².
pub fn gamma(k: [i64; 2], q: i64) -> i128 {
    let q2 = q as i128 * q as i128;
    let s = q2 - (k[0] as i128 * k[0] as i128 + k[1] as i128 * k[1] as i128);
    assert!(s > 0, "massive body at or beyond c: |k|² ≥ Q²");
    (((F * F * q2) / s) as u128).isqrt() as i128
}

/// Fixed-point 4-momentum (E, px, py) in units of F·Q·m·c.
pub fn four_momentum(m: i64, k: [i64; 2], q: i64) -> [i128; 3] {
    let g = m as i128 * gamma(k, q);
    [g * q as i128, g * k[0] as i128, g * k[1] as i128]
}

fn add3(a: [i128; 3], b: [i128; 3]) -> [i128; 3] {
    [a[0] + b[0], a[1] + b[1], a[2] + b[2]]
}

/// The exact outcome scaled by T = N·N: (T·p_a', T·p_b', T). None when the pair exchanges
/// nothing (p_a·N = 0) or d = 0. Big integers: the reference for [`targets`].
pub fn exact_outcome(pa: [i128; 3], pb: [i128; 3], d: [i128; 2]) -> Option<([BigInt; 3], [BigInt; 3], BigInt)> {
    let b = |v: i128| BigInt::from(v);
    let p = add3(pa, pb);
    let a = b(d[0]) * b(p[1]) + b(d[1]) * b(p[2]);
    let n = [a.clone(), b(p[0]) * b(d[0]), b(p[0]) * b(d[1])];
    let mdot = |x: &[BigInt; 3], y: &[BigInt; 3]| &x[0] * &y[0] - &x[1] * &y[1] - &x[2] * &y[2];
    let (pa_b, pb_b) = (pa.map(b), pb.map(b));
    let t = mdot(&n, &n);
    let s = mdot(&pa_b, &n);
    if s == BigInt::from(0) || t == BigInt::from(0) {
        return None;
    }
    let two_s = &s * 2;
    let na = std::array::from_fn(|i| &t * &pa_b[i] - &two_s * &n[i]);
    let nb = std::array::from_fn(|i| &t * &pb_b[i] + &two_s * &n[i]);
    Some((na, nb, t))
}

/// Rational velocity target (numerators, denominator > 0) for both bodies, in 1/Q units.
type Target = ([i128; 2], i128);

fn norm(num: [i128; 2], den: i128) -> Target {
    if den < 0 { ([-num[0], -num[1]], -den) } else { (num, den) }
}

/// Exact targets Q·p'_s/E' for both bodies. Checked i128 first (typical contacts fit);
/// the big-integer path gives the same exact rationals when anything would overflow.
pub fn targets(pa: [i128; 3], pb: [i128; 3], d: [i128; 2], q: i64) -> Option<(Target, Target)> {
    fast_targets(pa, pb, d, q).unwrap_or_else(|| slow_targets(pa, pb, d, q))
}

/// Outer None: overflow (use the exact slow path). Inner None: no exchange.
fn fast_targets(pa: [i128; 3], pb: [i128; 3], d: [i128; 2], q: i64) -> Option<Option<(Target, Target)>> {
    let p = add3(pa, pb);
    let a = d[0].checked_mul(p[1])?.checked_add(d[1].checked_mul(p[2])?)?;
    let n = [a, p[0].checked_mul(d[0])?, p[0].checked_mul(d[1])?];
    let mdot = |x: [i128; 3], y: [i128; 3]| -> Option<i128> {
        x[0].checked_mul(y[0])?.checked_sub(x[1].checked_mul(y[1])?)?.checked_sub(x[2].checked_mul(y[2])?)
    };
    let t = mdot(n, n)?;
    let s = mdot(pa, n)?;
    if s == 0 || t == 0 {
        return Some(None);
    }
    let two_s = s.checked_mul(2)?;
    let side = |pv: [i128; 3], sign: i128| -> Option<Target> {
        let c = |i: usize| t.checked_mul(pv[i])?.checked_sub(two_s.checked_mul(n[i])?.checked_mul(sign)?);
        let (e, x, y) = (c(0)?, c(1)?, c(2)?);
        Some(norm([x.checked_mul(q as i128)?, y.checked_mul(q as i128)?], e))
    };
    Some(Some((side(pa, 1)?, side(pb, -1)?)))
}

fn slow_targets(pa: [i128; 3], pb: [i128; 3], d: [i128; 2], q: i64) -> Option<(Target, Target)> {
    let (na, nb, _) = exact_outcome(pa, pb, d)?;
    // Reduce each target to the floor/ceil information we need without leaving big
    // integers: the velocity itself is below Q in magnitude, so Q·x/E fits i128 after an
    // exact division into integer part and remainder sign.
    let one = |v: &[BigInt; 3]| -> Target {
        let (mut e, mut x, mut y) = (v[0].clone(), &v[1] * q, &v[2] * q);
        if e < BigInt::from(0) {
            e = -e;
            x = -x;
            y = -y;
        }
        // Represent x/e as (2·floor + frac_flag)/2: numerator and denominator 2 keep
        // floor and ceil exact (frac_flag = 1 iff x is not a multiple of e).
        let half = |x: &BigInt| -> i128 {
            let fl = floor_big(x, &e);
            let exact = &fl * &e == *x;
            let f = i128::try_from(fl).expect("|velocity| < Q");
            2 * f + if exact { 0 } else { 1 }
        };
        ([half(&x), half(&y)], 2)
    };
    Some((one(&na), one(&nb)))
}

fn floor_big(n: &BigInt, d: &BigInt) -> BigInt {
    let (qt, r) = (n / d, n % d);
    if r != BigInt::from(0) && ((r < BigInt::from(0)) != (*d < BigInt::from(0))) { qt - 1 } else { qt }
}

/// Floor/ceil lattice points around a target that lie strictly inside the light cone, in a
/// fixed order (floor-floor, floor-ceil, ceil-floor, ceil-ceil). Never empty: truncation
/// toward zero is one of them and |trunc| ≤ |target| < Q.
pub fn candidates(t: Target, q: i64) -> Vec<[i64; 2]> {
    let (num, den) = t;
    let fl = |v: i128| v.div_euclid(den) as i64;
    let ce = |v: i128| (-(-v).div_euclid(den)) as i64;
    let q2 = q as i128 * q as i128;
    let mut out: Vec<[i64; 2]> = Vec::with_capacity(4);
    for x in [fl(num[0]), ce(num[0])] {
        for y in [fl(num[1]), ce(num[1])] {
            let c = [x, y];
            if !out.contains(&c) && (x as i128 * x as i128 + y as i128 * y as i128) < q2 {
                out.push(c);
            }
        }
    }
    debug_assert!(!out.is_empty());
    out
}

/// Relativistic counterpart of [`crate::law::resolve`]: same batch conventions (bodies
/// sorted by id and advanced to the chronon's end, pairs sorted, wall flags). The pair's
/// 4-momentum error joins the lower id's carry: energy in `residual`, momentum in `carry`.
pub fn resolve(
    q: i64,
    bodies: &mut [Body],
    pairs: &[(usize, usize)],
    walls: &[bool],
    container: Option<&Container>,
    wall_momentum: &mut [i64; 2],
) {
    debug_assert_eq!(walls.len(), bodies.len());
    let before: Vec<[i64; 2]> = bodies.iter().map(|b| b.k).collect();
    let mut k = before.clone();
    let mut owe: Vec<[i128; 3]> = bodies.iter().map(|b| [b.residual as i128, b.carry[0] as i128, b.carry[1] as i128]).collect();
    let mut touched = vec![false; bodies.len()];
    for &(a, b) in pairs {
        if bodies[a].response != Response::Bounce || bodies[b].response != Response::Bounce {
            continue;
        }
        let d = sub(bodies[b].x, bodies[a].x);
        let w = sub(k[b], k[a]);
        if dot(d, w) >= 0 || dot(d, d) == 0 {
            continue;
        }
        let (ma, mb) = (bodies[a].mass, bodies[b].mass);
        let (pa, pb) = (four_momentum(ma, k[a], q), four_momentum(mb, k[b], q));
        let Some((ta, tb)) = targets(pa, pb, d, q) else { continue };
        touched[a] = true;
        let fa: Vec<([i64; 2], [i128; 3])> = candidates(ta, q).into_iter().map(|c| (c, four_momentum(ma, c, q))).collect();
        let fb: Vec<([i64; 2], [i128; 3])> = candidates(tb, q).into_iter().map(|c| (c, four_momentum(mb, c, q))).collect();
        let old = add3(pa, pb);
        let owed = add3(owe[a], owe[b]);
        let unchanged_allowed = fa.len() * fb.len() == 1;
        let mut best: Option<(i128, [i64; 2], [i64; 2], [i128; 3])> = None;
        for (ca, ea) in &fa {
            for (cb, eb) in &fb {
                if !unchanged_allowed && *ca == k[a] && *cb == k[b] {
                    continue;
                }
                let e = [ea[0] + eb[0] - old[0], ea[1] + eb[1] - old[1], ea[2] + eb[2] - old[2]];
                let r = add3(owed, e);
                let score = r[0] * r[0] + r[1] * r[1] + r[2] * r[2];
                if best.as_ref().is_none_or(|(s, ..)| score < *s) {
                    best = Some((score, *ca, *cb, e));
                }
            }
        }
        let Some((_, ca, cb, e)) = best else { continue };
        owe[a] = add3(owe[a], e);
        k[a] = ca;
        k[b] = cb;
    }
    for &(a, b) in pairs {
        for i in [a, b] {
            if bodies[i].response == Response::Stop {
                k[i] = [0, 0];
            }
        }
    }
    if let Some(c) = container {
        for (i, body) in bodies.iter().enumerate() {
            if !walls[i] {
                continue;
            }
            let (lo, hi) = c.inset(body.radius);
            for ax in 0..2 {
                if (body.x[ax] <= lo[ax] && k[i][ax] < 0) || (body.x[ax] >= hi[ax] && k[i][ax] > 0) {
                    let dp = i64::try_from(2 * four_momentum(body.mass, k[i], q)[1 + ax]).expect("wall exchange fits i64");
                    wall_momentum[ax] = wall_momentum[ax].checked_add(dp).expect("wall ledger fits i64");
                    k[i][ax] = -k[i][ax];
                }
            }
        }
    }
    for (i, body) in bodies.iter_mut().enumerate() {
        if touched[i] {
            body.residual = i64::try_from(owe[i][0]).expect("energy carry fits i64");
            body.carry = [i64::try_from(owe[i][1]).expect("momentum carry fits i64"), i64::try_from(owe[i][2]).expect("momentum carry fits i64")];
        }
        if k[i] != before[i] {
            body.k = k[i];
            body.rev += 1;
        }
    }
}

/// Total fixed-point 4-momentum of a world (energy, px, py).
pub fn total(w: &World) -> [i128; 3] {
    w.bodies.iter().fold([0, 0, 0], |t, b| add3(t, four_momentum(b.mass, b.k, w.q)))
}

/// Total carries (energy, px, py). Ledgers: total(end) − total(genesis) = carries, with the
/// wall momentum added to the momentum side.
pub fn carried(w: &World) -> [i128; 3] {
    w.bodies.iter().fold([0, 0, 0], |t, b| add3(t, [b.residual as i128, b.carry[0] as i128, b.carry[1] as i128]))
}
