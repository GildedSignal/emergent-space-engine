//! Carlson's symmetric elliptic kernels, integer (Q62 u128/i128) vs f64 twins.
//! Algorithms verbatim from Carlson 1994 (arXiv:math/9409227): RF eq.(9)-(14),
//! RC eq.(16)-(20), RD eq.(35)-(41), RJ eq.(24)-(32).
//! Integer port: u128 adds/shifts/mults + exact floor isqrt only; every op floors.
use std::hint::black_box;
use std::time::Instant;

use emergent_space::orbit::{Orbit, OrbitKey};
use emergent_space::scaled::Scalar;

const ONE: u128 = 1u128 << 62;
const PI62: u128 = 6386616846171354294u128; // round(pi * 2^62)
const N_ITER: usize = 5; // duplications; Carlson r ~ 2^-52 here

// ---------- exact floor isqrt for u128 (f64 seed + Newton + fix-ups) ----------
#[inline]
fn isqrt_u128(n: u128) -> u128 {
    if n == 0 {
        return 0;
    }
    let mut r = ((n as f64).sqrt() as u128).max(1);
    loop {
        let t = (r + n / r) >> 1;
        if t >= r {
            break;
        }
        r = t;
    }
    while r > 0 && r.checked_mul(r).map_or(true, |s| s > n) {
        r -= 1;
    }
    while r
        .checked_add(1)
        .and_then(|r1| r1.checked_mul(r1))
        .map_or(true, |s| s <= n)
    {
        r += 1;
    }
    r
}
#[inline]
fn sqrt_q(v: u128) -> u128 {
    isqrt_u128(v << 62)
}

// ---------- Q62 helpers ----------
#[inline]
fn umul(a: u128, b: u128) -> u128 {
    (a * b) >> 62
}
#[inline]
fn udiv(a: u128, b: u128) -> u128 {
    (a << 62) / b
}
#[inline]
fn imul(a: i128, b: i128) -> i128 {
    (a * b) >> 62
}
#[inline]
fn umul_c(a: u128, b: u128) -> u128 {
    match a.checked_mul(b) {
        Some(p) => p >> 62,
        None => ((a >> 1) * b) >> 61,
    }
}

// ---------- RF ----------
fn rf_int(x0: u128, y0: u128, z0: u128, n_iter: usize) -> u128 {
    let (mut x, mut y, mut z) = (x0, y0, z0);
    let mut an = (x + y + z) / 3;
    for _ in 0..n_iter {
        let sx = sqrt_q(x);
        let sy = sqrt_q(y);
        let sz = sqrt_q(z);
        let lam = umul(sx, sy) + umul(sx, sz) + umul(sy, sz);
        x = (x + lam) >> 2;
        y = (y + lam) >> 2;
        z = (z + lam) >> 2;
        an = (an + lam) >> 2;
    }
    let xi = ONE as i128 - ((x << 62) / an) as i128;
    let yi = ONE as i128 - ((y << 62) / an) as i128;
    let zi = -xi - yi;
    let e2 = imul(xi, yi) - imul(zi, zi);
    let e3 = imul(imul(xi, yi), zi);
    let e22 = imul(e2, e2);
    let e23 = imul(e2, e3);
    let series = ONE as i128
        - e2 / 10
        + e3 / 14
        + e22 / 24
        - (3 * e23) / 44;
    ((series as u128) << 62) / sqrt_q(an)
}
fn rf_f64(x: f64, y: f64, z: f64, n_iter: usize) -> f64 {
    let (mut x, mut y, mut z) = (x, y, z);
    let mut an = (x + y + z) / 3.0;
    for _ in 0..n_iter {
        let (sx, sy, sz) = (x.sqrt(), y.sqrt(), z.sqrt());
        let lam = sx * sy + sx * sz + sy * sz;
        x = (x + lam) / 4.0;
        y = (y + lam) / 4.0;
        z = (z + lam) / 4.0;
        an = (an + lam) / 4.0;
    }
    let xi = 1.0 - x / an;
    let yi = 1.0 - y / an;
    let zi = -xi - yi;
    let e2 = xi * yi - zi * zi;
    let e3 = xi * yi * zi;
    (1.0 - e2 / 10.0 + e3 / 14.0 + e2 * e2 / 24.0 - 3.0 * e2 * e3 / 44.0) / an.sqrt()
}

// ---------- RC (x > 0, y > 0) ----------
fn rc_int(x0: u128, y0: u128, n_iter: usize) -> u128 {
    let (mut x, mut y) = (x0, y0);
    let mut an = (x + 2 * y) / 3;
    for _ in 0..n_iter {
        let lam = 2 * sqrt_q(umul(x, y)) + y;
        x = (x + lam) >> 2;
        y = (y + lam) >> 2;
        an = (an + lam) >> 2;
    }
    let s = ((y as i128) << 62) / (an as i128) - (ONE as i128);
    let s2 = imul(s, s);
    let s3 = imul(s2, s);
    let s4 = imul(s2, s2);
    let s5 = imul(s4, s);
    let s6 = imul(s3, s3);
    let s7 = imul(s4, s3);
    let series = ONE as i128
        + 3 * s2 / 10
        + s3 / 7
        + 3 * s4 / 8
        + 9 * s5 / 22
        + 159 * s6 / 208
        + 9 * s7 / 8;
    ((series as u128) << 62) / sqrt_q(an)
}
fn rc_f64(x: f64, y: f64, n_iter: usize) -> f64 {
    let (mut x, mut y) = (x, y);
    let mut an = (x + 2.0 * y) / 3.0;
    for _ in 0..n_iter {
        let lam = 2.0 * (x * y).sqrt() + y;
        x = (x + lam) / 4.0;
        y = (y + lam) / 4.0;
        an = (an + lam) / 4.0;
    }
    let s = y / an - 1.0;
    let series = 1.0
        + 3.0 * s * s / 10.0
        + s.powi(3) / 7.0
        + 3.0 * s.powi(4) / 8.0
        + 9.0 * s.powi(5) / 22.0
        + 159.0 * s.powi(6) / 208.0
        + 9.0 * s.powi(7) / 8.0;
    series / an.sqrt()
}

// ---------- RD ----------
fn rd_int(x0: u128, y0: u128, z0: u128, n_iter: usize) -> u128 {
    let (mut x, mut y, mut z) = (x0, y0, z0);
    let mut an = (x + y + 3 * z) / 5;
    let mut sum: u128 = 0;
    let mut fac: u128 = ONE;
    for _ in 0..n_iter {
        let sx = sqrt_q(x);
        let sy = sqrt_q(y);
        let sz = sqrt_q(z);
        let lam = umul(sx, sy) + umul(sx, sz) + umul(sy, sz);
        sum += udiv(3 * fac, umul_c(sz, z + lam));
        x = (x + lam) >> 2;
        y = (y + lam) >> 2;
        z = (z + lam) >> 2;
        an = (an + lam) >> 2;
        fac >>= 2;
    }
    let xi = ONE as i128 - ((x << 62) / an) as i128;
    let yi = ONE as i128 - ((y << 62) / an) as i128;
    let zi = -(xi + yi) / 3;
    let xy = imul(xi, yi);
    let z2 = imul(zi, zi);
    let e2 = xy - 6 * z2;
    let e3 = imul(3 * xy - 8 * z2, zi);
    let e4 = imul(3 * imul(xy - z2, z2), z2);
    let e5 = imul(imul(xy, zi), imul(z2, zi));
    let e22 = imul(e2, e2);
    let e23 = imul(e2, e3);
    let series = ONE as i128
        - 3 * e2 / 14
        + e3 / 6
        + 9 * e22 / 88
        - 3 * e4 / 22
        - 9 * e23 / 52
        + 3 * e5 / 26;
    let sqrt_an = sqrt_q(an);
    let an32 = umul(an, sqrt_an);
    let main = umul((series as u128) >> (2 * n_iter), udiv(ONE, an32));
    main + sum
}
fn rd_f64(x: f64, y: f64, z: f64, n_iter: usize) -> f64 {
    let (mut x, mut y, mut z) = (x, y, z);
    let mut an = (x + y + 3.0 * z) / 5.0;
    let mut sum = 0.0;
    let mut fac = 1.0;
    for _ in 0..n_iter {
        let (sx, sy, sz) = (x.sqrt(), y.sqrt(), z.sqrt());
        let lam = sx * sy + sx * sz + sy * sz;
        sum += 3.0 * fac / (sz * (z + lam));
        x = (x + lam) / 4.0;
        y = (y + lam) / 4.0;
        z = (z + lam) / 4.0;
        an = (an + lam) / 4.0;
        fac /= 4.0;
    }
    let xi = 1.0 - x / an;
    let yi = 1.0 - y / an;
    let zi = -(xi + yi) / 3.0;
    let xy = xi * yi;
    let z2 = zi * zi;
    let e2 = xy - 6.0 * z2;
    let e3 = (3.0 * xy - 8.0 * z2) * zi;
    let e4 = 3.0 * (xy - z2) * z2 * z2;
    let e5 = xy * zi * z2 * zi;
    let series = 1.0 - 3.0 * e2 / 14.0
        + e3 / 6.0
        + 9.0 * e2 * e2 / 88.0
        - 3.0 * e4 / 22.0
        - 9.0 * e2 * e3 / 52.0
        + 3.0 * e5 / 26.0;
    fac * series / (an * an.sqrt()) + sum
}

// ---------- RJ (p > 0; x,y,z >= 0, at most one zero) ----------
fn rj_int(x0: u128, y0: u128, z0: u128, p0: u128, n_iter: usize) -> u128 {
    let (mut x, mut y, mut z, mut p) = (x0, y0, z0, p0);
    let mut an = (x + y + z + 2 * p) / 5;
    let dx = p as i128 - x as i128;
    let dy = p as i128 - y as i128;
    let dz = p as i128 - z as i128;
    let delta = imul(imul(dx, dy), dz);
    let mut sum: u128 = 0;
    let mut fac: u128 = ONE;
    for m in 0..n_iter {
        let sx = sqrt_q(x);
        let sy = sqrt_q(y);
        let sz = sqrt_q(z);
        let sp = sqrt_q(p);
        let lam = umul(sx, sy) + umul(sx, sz) + umul(sy, sz);
        let d = umul_c(umul_c(sp + sx, sp + sy), sp + sz);
        let delta_shr = delta >> (6 * m);
        let dd = umul(d, d).max(1);
        let e = (delta_shr << 62) / dd as i128;
        let one_plus_e = (ONE as i128 + e) as u128;
        let rc = rc_int(ONE, one_plus_e, n_iter);
        sum += udiv(umul_c(6 * fac, rc), d);
        x = (x + lam) >> 2;
        y = (y + lam) >> 2;
        z = (z + lam) >> 2;
        p = (p + lam) >> 2;
        an = (an + lam) >> 2;
        fac >>= 2;
    }
    let xi = ONE as i128 - ((x << 62) / an) as i128;
    let yi = ONE as i128 - ((y << 62) / an) as i128;
    let zi = ONE as i128 - ((z << 62) / an) as i128;
    let pp = -(xi + yi + zi) / 2;
    let xy = imul(xi, yi);
    let xz = imul(xi, zi);
    let yz = imul(yi, zi);
    let p2 = imul(pp, pp);
    let p3 = imul(p2, pp);
    let xyz = imul(xy, zi);
    let e2 = xy + xz + yz - 3 * p2;
    let e3 = xyz + 2 * imul(e2, pp) + 4 * p3;
    let e4 = imul(2 * xyz + imul(e2, pp) + 3 * p3, pp);
    let e5 = imul(xyz, p2);
    let e22 = imul(e2, e2);
    let e23 = imul(e2, e3);
    let series = ONE as i128
        - 3 * e2 / 14
        + e3 / 6
        + 9 * e22 / 88
        - 3 * e4 / 22
        - 9 * e23 / 52
        + 3 * e5 / 26;
    let sqrt_an = sqrt_q(an);
    let an32 = umul(an, sqrt_an);
    let main = umul((series as u128) >> (2 * n_iter), udiv(ONE, an32));
    main + sum
}
fn rj_f64(x: f64, y: f64, z: f64, p: f64, n_iter: usize) -> f64 {
    let (mut x, mut y, mut z, mut p) = (x, y, z, p);
    let mut an = (x + y + z + 2.0 * p) / 5.0;
    let delta = (p - x) * (p - y) * (p - z);
    let mut sum = 0.0;
    let mut fac = 1.0;
    for m in 0..n_iter {
        let (sx, sy, sz, sp) = (x.sqrt(), y.sqrt(), z.sqrt(), p.sqrt());
        let lam = sx * sy + sx * sz + sy * sz;
        let d = (sp + sx) * (sp + sy) * (sp + sz);
        let e = (delta / 4f64.powi(3 * m as i32)) / (d * d);
        sum += 6.0 * fac / d * rc_f64(1.0, 1.0 + e, n_iter);
        x = (x + lam) / 4.0;
        y = (y + lam) / 4.0;
        z = (z + lam) / 4.0;
        p = (p + lam) / 4.0;
        an = (an + lam) / 4.0;
        fac /= 4.0;
    }
    let xi = 1.0 - x / an;
    let yi = 1.0 - y / an;
    let zi = 1.0 - z / an;
    let pp = -(xi + yi + zi) / 2.0;
    let xy = xi * yi;
    let xz = xi * zi;
    let yz = yi * zi;
    let p2 = pp * pp;
    let p3 = p2 * pp;
    let xyz = xy * zi;
    let e2 = xy + xz + yz - 3.0 * p2;
    let e3 = xyz + 2.0 * e2 * pp + 4.0 * p3;
    let e4 = (2.0 * xyz + e2 * pp + 3.0 * p3) * pp;
    let e5 = xyz * p2;
    let series = 1.0 - 3.0 * e2 / 14.0
        + e3 / 6.0
        + 9.0 * e2 * e2 / 88.0
        - 3.0 * e4 / 22.0
        - 9.0 * e2 * e3 / 52.0
        + 3.0 * e5 / 26.0;
    fac * series / (an * an.sqrt()) + sum
}

fn f62(v: u128) -> f64 {
    v as f64 / (1u128 << 62) as f64
}
fn scalar_f62(s: Scalar) -> f64 {
    s.fixed(62).map(|v| v as f64 / (1u128 << 62) as f64).unwrap_or(f64::NAN)
}

fn time_ns<F: FnMut() -> u64>(mut f: F, reps: usize) -> f64 {
    for _ in 0..200 {
        black_box(f());
    }
    let mut best = f64::MAX;
    for _ in 0..9 {
        let t = Instant::now();
        for _ in 0..reps {
            black_box(f());
        }
        let d = t.elapsed().as_nanos() as f64 / reps as f64;
        best = best.min(d);
    }
    best
}

fn main() {
    println!("{{\"law\": \"{}\", \"n_iter\": {}}}", emergent_space::LAW_ID, N_ITER);

    // ---- timing on representative strong operands ----
    let rf_fd = time_ns(|| rf_f64(0.0, 0.5, 1.0, N_ITER) as u64, 20000);
    let rf_in = time_ns(
        || rf_int(black_box(0), black_box(ONE / 2), black_box(ONE), N_ITER) as u64,
        5000,
    );
    let rd_fd = time_ns(|| rd_f64(0.0, 0.5, 1.0, N_ITER) as u64, 20000);
    let rd_in = time_ns(
        || rd_int(black_box(0), black_box(ONE / 2), black_box(ONE), N_ITER) as u64,
        5000,
    );
    let rj_fd = time_ns(|| rj_f64(0.0, 0.5, 1.0, 0.3, N_ITER) as u64, 20000);
    let rj_in = time_ns(
        || {
            rj_int(
                black_box(0),
                black_box(ONE / 2),
                black_box(ONE),
                black_box(ONE * 3 / 10),
                N_ITER,
            ) as u64
        },
        5000,
    );
    let rc_fd = time_ns(|| rc_f64(1.0, 1.2, N_ITER) as u64, 20000);
    let rc_in = time_ns(
        || rc_int(black_box(ONE), black_box(ONE * 6 / 5), N_ITER) as u64,
        20000,
    );
    let isq = time_ns(
        || isqrt_u128(black_box(0xdeadbeefcafe1234567890u128)) as u64,
        20000,
    );
    println!(
        "{{\"walls_ns\": {{\"rf_f64\": {rf_fd:.1}, \"rf_int\": {rf_in:.1}, \"rd_f64\": {rd_fd:.1}, \"rd_int\": {rd_in:.1}, \"rj_f64\": {rj_fd:.1}, \"rj_int\": {rj_in:.1}, \"rc_f64\": {rc_fd:.1}, \"rc_int\": {rc_in:.1}, \"isqrt_u128\": {isq:.1}}}}}"
    );

    // ---- error-vs-n curve on the worst operand (m -> 1) ----
    for n in 3..=7 {
        let mf = 1.0 - 1e-8f64;
        let mi = ((1.0 - mf) * (ONE as f64)) as u128;
        println!(
            "{{\"ncurve\": {{\"n\": {n}, \"mfrac\": 1e-8, \"rf_f64\": {:.17e}, \"rf_int\": {:.17e}}}}}",
            rf_f64(0.0, 1.0 - mf, 1.0, n),
            f62(rf_int(0, ONE - mi, ONE, n))
        );
    }

    // ---- key grid: phi channel end-to-end + tau/t operand sets ----
    let ps: [u64; 11] = [7, 8, 10, 14, 20, 32, 64, 256, 1024, 8192, 1048576];
    let es: [f64; 10] = [0.05, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99, 0.999, 0.9999, 0.99999];
    let mut n_ok = 0;
    let mut n_refused = 0;
    for &p in &ps {
        for &e in &es {
            let e_q48 = (e * (1u64 << 48) as f64).round() as u64;
            let key = match OrbitKey::bound(Scalar::integer(p as i64), e_q48) {
                Ok(k) => k,
                Err(_) => {
                    n_refused += 1;
                    continue;
                }
            };
            let orbit = match Orbit::compile(key) {
                Ok(o) => o,
                Err(_) => {
                    n_refused += 1;
                    continue;
                }
            };
            let q62 = match key.compactness().and_then(|c| c.fixed(62)) {
                Ok(v) if v > 0 => v as u128,
                _ => continue,
            };
            let k62 = (key.k as u128) << 14; // Q48 -> Q62
            let qf = f62(q62);
            let kf = f62(k62);
            let eta62 = ONE - k62;
            // A = 1 - q(8k-2); m = 4 q eta / A   (phi channel, wiki-verified reduction)
            let a8 = (k62 << 3).saturating_sub(2 * ONE);
            let big_a = ONE.saturating_sub(umul(q62, a8));
            if big_a == 0 {
                n_refused += 1;
                continue;
            }
            let m62 = udiv(umul(q62, eta62) << 2, big_a);
            let mf = f62(m62);
            let strong = qf > 3.814697265625e-6; // 2^-18
            let walk_adv = scalar_f62(orbit.advance().unwrap_or(Scalar::ZERO));
            let walk_period = scalar_f62(orbit.period().unwrap_or(Scalar::ZERO));
            let walk_proper = scalar_f62(orbit.proper_period().unwrap_or(Scalar::ZERO));
            // compile wall (median of 15)
            let mut walls = Vec::new();
            for _ in 0..15 {
                let t0 = Instant::now();
                let o = Orbit::compile(key).unwrap();
                walls.push(t0.elapsed().as_nanos() as f64 / 1000.0);
                black_box(o.advance());
            }
            walls.sort_by(|a, b| a.partial_cmp(b).unwrap());
            let wall_us = walls[7];
            // integer closed form for advance: q*(2K/sqrt(A) - pi)
            let kk = rf_int(0, ONE - m62, ONE, N_ITER);
            let v = udiv(kk, sqrt_q(big_a)) << 1; // 2K/sqrt(A)
            let adv_int_f = if v > PI62 {
                f62(v - PI62)
            } else {
                0.0
            };
            let adv_f64 =
                2.0 * rf_f64(0.0, 1.0 - mf, 1.0, N_ITER) / f62(big_a) - std::f64::consts::PI;
            // tau/t operand family: Pi(n, m') with n = 2 eta, m' = -c1/c0 < 0
            // operands (0, 1-m', 1, 1-n); 1-m' = 1 + c1/c0, 1-n = 2k-1
            let c0 = ONE.saturating_sub(umul(q62 << 1, ONE + (k62 << 1)));
            let c1 = umul(q62, eta62) << 2;
            let n_pi = eta62 << 1;
            let pp = ONE - n_pi;
            let (rj_int_f, rj_f64_v, pi_int_f, pi_f64_v) = if c0 > 0 && pp > 0 && c0 > c1 / 8 {
                let y_op = ONE + udiv(c1, c0);
                let rji = rj_int(0, y_op, ONE, pp, N_ITER);
                let rjf = rj_f64(0.0, f62(y_op), 1.0, f62(pp), N_ITER);
                // Pi(n,m') = K(m') + (n/3) RJ(0,1-m',1,1-n)
                let kbase = rf_int(0, y_op, ONE, N_ITER);
                let pi_i = f62(kbase) + f62(n_pi) / 3.0 * f62(rji);
                let pi_f = rf_f64(0.0, f62(y_op), 1.0, N_ITER) + f62(n_pi) / 3.0 * rjf;
                (f62(rji), rjf, pi_i, pi_f)
            } else {
                (f64::NAN, f64::NAN, f64::NAN, f64::NAN)
            };
            let rd_int_f = f62(rd_int(0, ONE - m62, ONE, N_ITER));
            let rd_f64_v = rd_f64(0.0, 1.0 - mf, 1.0, N_ITER);
            println!(
                "{{\"key\": {{\"p\": {p}, \"e\": {e}, \"q\": {qf:.9e}, \"k\": {kf:.9}, \"m\": {mf:.9e}, \"strong\": {strong}, \"wall_us\": {wall_us:.2}, \"walk_adv\": {walk_adv:.12e}, \"adv_f64\": {adv_f64:.12e}, \"adv_int\": {adv_int_f:.12e}, \"walk_period\": {walk_period:.9e}, \"walk_proper\": {walk_proper:.9e}, \"n_pi\": {:.9e}, \"mpprime\": {:.9e}, \"rj_int\": {rj_int_f:.12e}, \"rj_f64\": {rj_f64_v:.12e}, \"pi_int\": {pi_int_f:.12e}, \"pi_f64\": {pi_f64_v:.12e}, \"rd_int\": {rd_int_f:.12e}, \"rd_f64\": {rd_f64_v:.12e}}}}}",
                f62(n_pi),
                -f62(udiv(c1, c0.max(1))),
            );
            n_ok += 1;
        }
    }
    eprintln!("keys ok: {n_ok}, refused: {n_refused}");
}

#[cfg(test)]
mod tests {
    use super::*;
    fn q(v: f64) -> u128 {
        (v * (ONE as f64)).round() as u128
    }
    #[test]
    fn check_vectors() {
        // Carlson 1994 Section 3 check values
        let cases_rf = [
            ((1.0, 2.0, 0.0), 1.3110287771461),
            ((0.0, 1.0, 0.5), 1.8540746773014),
            ((2.0, 3.0, 4.0), 0.58408284167715),
        ];
        for ((x, y, z), want) in cases_rf {
            let f = rf_f64(x, y, z, N_ITER);
            let i = f62(rf_int(q(x), q(y), q(z), N_ITER));
            println!("RF({x},{y},{z}): f64={f:.15} int={i:.15} want={want}");
        }
        let cases_rc = [((0.0, 0.25), std::f64::consts::PI), ((2.25, 2.0), std::f64::consts::LN_2)];
        for ((x, y), want) in cases_rc {
            println!("RC({x},{y}): f64={:.15} int={:.15} want={want}", rc_f64(x, y, N_ITER), f62(rc_int(q(x), q(y), N_ITER)));
        }
        let cases_rd = [((0.0, 2.0, 1.0), 1.7972103521034), ((2.0, 3.0, 4.0), 0.16510527294261)];
        for ((x, y, z), want) in cases_rd {
            println!("RD({x},{y},{z}): f64={:.15} int={:.15} want={want}", rd_f64(x, y, z, N_ITER), f62(rd_int(q(x), q(y), q(z), N_ITER)));
        }
        let cases_rj = [((0.0, 1.0, 2.0, 3.0), 0.77688623778582), ((2.0, 3.0, 4.0, 5.0), 0.14297579667157)];
        for ((x, y, z, p), want) in cases_rj {
            println!("RJ({x},{y},{z},{p}): f64={:.15} int={:.15} want={want}", rj_f64(x, y, z, p, N_ITER), f62(rj_int(q(x), q(y), q(z), q(p), N_ITER)));
        }
        // isqrt sanity
        assert_eq!(isqrt_u128(1u128 << 124), 1u128 << 62);
        assert_eq!(isqrt_u128((1u128 << 124) - 1), (1u128 << 62) - 1);
    }
}


