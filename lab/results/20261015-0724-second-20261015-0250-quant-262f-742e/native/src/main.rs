//! The checker's one experiment to gold (run 20261015-0250-quant-262f, check.md):
//! one Rust arm, one box, three timings at true belt keys — (a) the shipped
//! compile per promotion, (b) a native scalar closed-readout loop, (c) the native
//! batched loop including per-body coefficient setup — plus the value checks the
//! author skipped (batched vs scalar vs Simpson of the shipped `node()` integrands,
//! analytic-slope FD check, the wider e/p grid, 1e7 promotions).
//!
//! Channel formulas are 262f's Simpson-verified SCALAR forms, used verbatim by every
//! arm (scalar, SoA batch, AVX2 batch): adv = (CH·F − 2u)/q; τ = dnum·CH·I2;
//! t = tnum·CH/(1−2q)·(aa·Π(n3) + bb2·I2 + gg·Π(−n4)). The 262f factor-2 slip was a
//! second transcription of these; here there is exactly one.
//!
//! Carlson kernels are Boost's (ellint_rf/ellint_rj, general duplication path,
//! 7th-order tails) ported verbatim; the AVX2 kernels are 4-wide masked ports of the
//! same loops (outlier |En| lanes serviced by the identical scalar closed form).

use emergent_space::orbit::{Orbit, OrbitKey, Scalar};
use std::arch::x86_64::*;
use std::time::Instant;

const AU: u64 = 101_300_000;
const PI_2: f64 = std::f64::consts::FRAC_PI_2;

// ---------------------------------------------------------------- RNG (splitmix64)
struct Rng(u64);
impl Rng {
    fn next(&mut self) -> u64 {
        self.0 = self.0.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    }
    fn unit(&mut self) -> f64 {
        (self.next() >> 11) as f64 / (1u64 << 53) as f64
    }
}

// ------------------------------------------------ Carlson kernels, scalar (Boost port)
#[inline]
fn rf(x: f64, y: f64, z: f64) -> f64 {
    let mut xn = x;
    let mut yn = y;
    let mut zn = z;
    let mut an = (x + y + z) / 3.0;
    let a0 = an;
    let c = (3.0 * f64::EPSILON).powf(-1.0 / 8.0);
    let mut q = c * (an - xn).abs().max((an - yn).abs()).max((an - zn).abs());
    let mut fn_ = 1.0f64;
    for _ in 0..64 {
        let root_x = xn.sqrt();
        let root_y = yn.sqrt();
        let root_z = zn.sqrt();
        let lambda = root_x * root_y + root_x * root_z + root_y * root_z;
        an = (an + lambda) / 4.0;
        xn = (xn + lambda) / 4.0;
        yn = (yn + lambda) / 4.0;
        zn = (zn + lambda) / 4.0;
        q /= 4.0;
        fn_ *= 4.0;
        if q < an.abs() {
            break;
        }
    }
    let xx = (a0 - x) / (an * fn_);
    let yy = (a0 - y) / (an * fn_);
    let zz = -xx - yy;
    let e2 = xx * yy - zz * zz;
    let e3 = xx * yy * zz;
    (1.0 + e3 * (1.0 / 14.0 + 3.0 * e3 / 104.0)
        + e2
            * (-1.0 / 10.0 + e2 / 24.0 - 3.0 * e3 / 44.0 - 5.0 * e2 * e2 / 208.0 + e2 * e3 / 16.0))
        / an.sqrt()
}

/// RC(1, 1+e) closed form (Boost ellint_rc1p_imp), e > -1.
#[inline]
fn rc1p(e: f64) -> f64 {
    if e == 0.0 {
        1.0
    } else if e > 0.0 {
        let s = e.sqrt();
        s.atan() / s
    } else {
        let arg = (-e).sqrt();
        (arg.ln_1p() - (-arg).ln_1p()) / (2.0 * arg)
    }
}

#[inline]
fn rj(x: f64, y: f64, z: f64, p: f64) -> f64 {
    let mut xn = x;
    let mut yn = y;
    let mut zn = z;
    let mut pn = p;
    let mut an = (x + y + z + 2.0 * p) / 5.0;
    let a0 = an;
    let mut delta = (p - x) * (p - y) * (p - z);
    let q0 = (5.0 / f64::EPSILON).sqrt().sqrt().sqrt()
        * (an - x)
            .abs()
            .max((an - y).abs())
            .max((an - z).abs())
            .max((an - p).abs());
    let mut fmn = 1.0f64;
    let mut rc_sum = 0.0f64;
    let series_limit = f64::EPSILON.cbrt().sqrt();
    for _ in 0..64 {
        let root_x = xn.sqrt();
        let root_y = yn.sqrt();
        let root_z = zn.sqrt();
        let root_p = pn.sqrt();
        let dn = (root_p + root_x) * (root_p + root_y) * (root_p + root_z);
        let mut en = delta / dn;
        en /= dn;
        let term = if en.abs() < series_limit {
            1.0 + en
                * (-1.0 / 3.0
                    + en * (1.0 / 5.0 + en * (-1.0 / 7.0 + en * (1.0 / 9.0 + en * (-1.0 / 11.0)))))
        } else {
            rc1p(en)
        };
        rc_sum += fmn / dn * term;
        let lambda = root_x * root_y + root_x * root_z + root_y * root_z;
        an = (an + lambda) / 4.0;
        fmn /= 4.0;
        if fmn * q0 < an {
            break;
        }
        xn = (xn + lambda) / 4.0;
        yn = (yn + lambda) / 4.0;
        zn = (zn + lambda) / 4.0;
        pn = (pn + lambda) / 4.0;
        delta /= 64.0;
    }
    let xx = fmn * (a0 - x) / an;
    let yy = fmn * (a0 - y) / an;
    let zz = fmn * (a0 - z) / an;
    let pp = (-xx - yy - zz) / 2.0;
    let e2 = xx * yy + xx * zz + yy * zz - 3.0 * pp * pp;
    let e3 = xx * yy * zz + 2.0 * e2 * pp + 4.0 * pp * pp * pp;
    let e4 = (2.0 * xx * yy * zz + e2 * pp + 3.0 * pp * pp * pp) * pp;
    let e5 = xx * yy * zz * pp * pp;
    let series = 1.0 - 3.0 * e2 / 14.0 + e3 / 6.0 + 9.0 * e2 * e2 / 88.0 - 3.0 * e4 / 22.0
        - 9.0 * e2 * e3 / 52.0
        + 3.0 * e5 / 26.0
        - e2 * e2 * e2 / 16.0
        + 3.0 * e3 * e3 / 40.0
        + 3.0 * e2 * e4 / 20.0
        + 45.0 * e2 * e2 * e3 / 272.0
        - 9.0 * (e3 * e4 + e2 * e5) / 68.0;
    fmn / (an * an.sqrt()) * series + 6.0 * rc_sum
}

// ------------------------------------------------ per-body setup (GE with pivoting)
fn solve(mut m: [[f64; 4]; 4], b: [f64; 4]) -> [f64; 4] {
    let mut x = b;
    for col in 0..4 {
        let mut piv = col;
        for r in col + 1..4 {
            if m[r][col].abs() > m[piv][col].abs() {
                piv = r;
            }
        }
        m.swap(col, piv);
        x.swap(col, piv);
        let d = m[col][col];
        for j in col..4 {
            m[col][j] /= d;
        }
        x[col] /= d;
        for r in 0..4 {
            if r != col && m[r][col] != 0.0 {
                let f = m[r][col];
                for j in col..4 {
                    m[r][j] -= f * m[col][j];
                }
                x[r] -= f * x[col];
            }
        }
    }
    x
}

fn solve3(mut m: [[f64; 3]; 3], b: [f64; 3]) -> [f64; 3] {
    let mut x = b;
    for col in 0..3 {
        let mut piv = col;
        for r in col + 1..3 {
            if m[r][col].abs() > m[piv][col].abs() {
                piv = r;
            }
        }
        m.swap(col, piv);
        x.swap(col, piv);
        let d = m[col][col];
        for j in col..3 {
            m[col][j] /= d;
        }
        x[col] /= d;
        for r in 0..3 {
            if r != col && m[r][col] != 0.0 {
                let f = m[r][col];
                for j in col..3 {
                    m[r][j] -= f * m[col][j];
                }
                x[r] -= f * x[col];
            }
        }
    }
    x
}

/// Per-body constants: the squared-pole 4x4 and t-channel 3x3 partial fractions
/// (262f/cd6e), solved per body exactly as the numpy bench's np.linalg.solve.
#[derive(Clone, Copy)]
struct Ctx {
    n3: f64,
    mg: f64,
    n4: f64,
    tnum: f64,
    dnum: f64,
    ch: f64,
    pinv: f64,
    q: f64,
    a: f64,
    m: f64,
    q0: f64,
    q1: f64,
    c1: f64,
    kap: f64,
    aa: f64,
    bb2: f64,
    gg: f64,
}

fn ctx_new(k: f64, q: f64) -> Ctx {
    let eta = 1.0 - k;
    let n3 = 2.0 * eta;
    let a = 1.0 - 2.0 * q * (4.0 * k - 1.0);
    let m = 4.0 * q * (1.0 - k) / a;
    let mg = -m / (1.0 - m);
    let n4 = 2.0 * q * n3 / (1.0 - 2.0 * q);
    let tnum = (k * (1.0 - 2.0 * q) * (1.0 + 2.0 * q * (1.0 - 2.0 * k))).sqrt();
    let dnum = (k - q * (3.0 * k * k + eta * eta)).sqrt();
    let ch = 2.0 / (a * (1.0 - m)).sqrt();
    let pinv = 1.0 / (1.0 - 2.0 * q);
    let n = -n3;
    let big = mg;
    let c4 = solve(
        [
            [1.0, 0.0, 1.0, 1.0],
            [2.0 * n, 1.0, n, -n - 2.0 - 2.0 * big],
            [n * n, 2.0 * n, 0.0, 3.0 * big],
            [0.0, n * n, 0.0, big * n],
        ],
        [1.0, 0.0, 0.0, 0.0],
    );
    let c3 = solve3(
        [
            [1.0, 1.0, 1.0],
            [n4 - n3, n4, -2.0 * n3],
            [-n3 * n4, 0.0, n3 * n3],
        ],
        [1.0, 0.0, 0.0],
    );
    Ctx {
        n3,
        mg,
        n4,
        tnum,
        dnum,
        ch,
        pinv,
        q,
        a,
        m,
        q0: c4[0],
        q1: c4[1],
        c1: c4[2],
        kap: c4[3],
        aa: c3[0],
        bb2: c3[1],
        gg: c3[2],
    }
}

/// The one channel definition (262f's Simpson-verified scalar forms).
#[inline]
fn channels(u: f64, c: &Ctx) -> (f64, f64, f64, f64) {
    let s = u.sin();
    let co = u.cos();
    let s2 = s * s;
    let c2 = co * co;
    let s3 = s2 * s;
    let w2 = 1.0 - c.mg * s2;
    let w = w2.sqrt();
    let v = 1.0 - c.n3 * s2;
    let f = s * rf(c2, w2, 1.0);
    let pi_n3 = f + (c.n3 / 3.0) * s3 * rj(c2, w2, 1.0, 1.0 - c.n3 * s2);
    let pi_mn4 = f + (-c.n4 / 3.0) * s3 * rj(c2, w2, 1.0, 1.0 + c.n4 * s2);
    let e_ch = f - (c.mg / 3.0) * s3 * rj(c2, w2, 1.0, 1.0);
    let i2 = c.q0 * f + c.q1 * (f - e_ch) / c.mg + c.c1 * pi_n3 + c.kap * s * co * w / v;
    let adv = (c.ch * f - 2.0 * u) / c.q;
    let tau = c.dnum * c.ch * i2;
    let t = c.tnum * c.ch * c.pinv * (c.aa * pi_n3 + c.bb2 * i2 + c.gg * pi_mn4);
    let slope = 2.0 * c.tnum / ((c.a * (1.0 - c.m * c2)).sqrt() * v * v * (1.0 - 2.0 * c.q * v));
    (adv, t, tau, slope)
}

/// Scalar promotion: cold start + Newton (analytic slope) + final read.
fn promote_scalar(c: &Ctx, t_true: f64, iters: &mut u32, u_out: &mut f64) -> (f64, f64) {
    let (_, t_half, _, _) = channels(PI_2, c);
    let mut u = PI_2 * (t_true / t_half);
    *iters = 0;
    let (mut adv, mut t, mut tau, mut slope) = channels(u, c);
    for _ in 0..60 {
        let du = (t_true - t) / slope;
        u = (u + du).clamp(1e-12, PI_2 - 1e-12);
        *iters += 1;
        let r = channels(u, c);
        adv = r.0;
        t = r.1;
        tau = r.2;
        slope = r.3;
        if du.abs() < 1e-13 {
            break;
        }
    }
    *u_out = u;
    (adv, tau)
}

// ---------------------------------------------------- adaptive Simpson reference
fn simpson_rec(
    f: &dyn Fn(f64) -> f64,
    a: f64,
    b: f64,
    fa: f64,
    fm: f64,
    fb: f64,
    whole: f64,
    eps_leaf: f64,
    depth: u32,
) -> f64 {
    let m = 0.5 * (a + b);
    let lm = 0.5 * (a + m);
    let rm = 0.5 * (m + b);
    let flm = f(lm);
    let frm = f(rm);
    let left = (m - a) / 6.0 * (fa + 4.0 * flm + fm);
    let right = (b - m) / 6.0 * (fm + 4.0 * frm + fb);
    if depth == 0 || (left + right - whole).abs() <= 15.0 * eps_leaf {
        return left + right + (left + right - whole) / 15.0;
    }
    simpson_rec(f, a, m, fa, flm, fm, left, eps_leaf / 2.0, depth - 1)
        + simpson_rec(f, m, b, fm, frm, fb, right, eps_leaf / 2.0, depth - 1)
}

fn quad(f: &dyn Fn(f64) -> f64, a: f64, b: f64, eps_rel: f64) -> f64 {
    let fa = f(a);
    let fb = f(b);
    let m = 0.5 * (a + b);
    let fm = f(m);
    let whole = (b - a) / 6.0 * (fa + 4.0 * fm + fb);
    // total-tolerance scheme: relative to the interval value, split across width
    let eps_total = eps_rel * whole.abs().max(1e-290);
    let eps_leaf0 = eps_total * 0.5; // root splits into 2 halves
    simpson_rec(f, a, b, fa, fm, fb, whole, eps_leaf0, 30)
}

/// Simpson of the shipped node() integrands (orbit.rs:314-343), over [0, 2u].
fn channels_simpson(k: f64, q: f64, u: f64) -> (f64, f64, f64) {
    let eta = 1.0 - k;
    let tnum = (k * (1.0 - 2.0 * q) * (1.0 + 2.0 * q * (1.0 - 2.0 * k))).sqrt();
    let dnum = (k - q * (3.0 * k * k + eta * eta)).sqrt();
    let hi = 2.0 * u;
    let f_adv = |th: f64| {
        let a = 6.0 * k + 2.0 * eta * th.cos();
        let d = 1.0 - q * a;
        let root = d.sqrt();
        a / (root * (1.0 + root))
    };
    let f_t = |th: f64| {
        let cs = th.cos();
        let x = k + eta * cs;
        let d = 1.0 - q * (6.0 * k + 2.0 * eta * cs);
        tnum / (d.sqrt() * x * x * (1.0 - 2.0 * q * x))
    };
    let f_tau = |th: f64| {
        let cs = th.cos();
        let x = k + eta * cs;
        let d = 1.0 - q * (6.0 * k + 2.0 * eta * cs);
        dnum / (d.sqrt() * x * x)
    };
    (
        quad(&f_adv, 0.0, hi, 1e-15),
        quad(&f_t, 0.0, hi, 1e-15),
        quad(&f_tau, 0.0, hi, 1e-15),
    )
}

// ------------------------------------------------------------------- AVX2 kernels
#[inline]
unsafe fn splat(v: f64) -> __m256d {
    _mm256_set1_pd(v)
}
#[inline]
unsafe fn abs4(v: __m256d) -> __m256d {
    _mm256_andnot_pd(_mm256_set1_pd(-0.0), v)
}
#[inline]
unsafe fn max4(a: __m256d, b: __m256d) -> __m256d {
    _mm256_max_pd(a, b)
}
#[inline]
unsafe fn store4(v: __m256d) -> [f64; 4] {
    let mut o = [0f64; 4];
    _mm256_storeu_pd(o.as_mut_ptr(), v);
    o
}
#[inline]
unsafe fn mul(a: __m256d, b: __m256d) -> __m256d {
    _mm256_mul_pd(a, b)
}
#[inline]
unsafe fn add(a: __m256d, b: __m256d) -> __m256d {
    _mm256_add_pd(a, b)
}
#[inline]
unsafe fn sub(a: __m256d, b: __m256d) -> __m256d {
    _mm256_sub_pd(a, b)
}
#[inline]
unsafe fn div(a: __m256d, b: __m256d) -> __m256d {
    _mm256_div_pd(a, b)
}

unsafe fn rf4(x: __m256d, y: __m256d, z: __m256d) -> __m256d {
    let mut xn = x;
    let mut yn = y;
    let mut zn = z;
    let mut an = mul(splat(1.0 / 3.0), add(add(x, y), z));
    let a0 = an;
    let c = splat((3.0 * f64::EPSILON).powf(-1.0 / 8.0));
    let mut q = mul(c, max4(max4(abs4(sub(an, xn)), abs4(sub(an, yn))), abs4(sub(an, zn))));
    let mut fn_ = splat(1.0);
    for _ in 0..64 {
        let rx = _mm256_sqrt_pd(xn);
        let ry = _mm256_sqrt_pd(yn);
        let rz = _mm256_sqrt_pd(zn);
        let lambda = add(add(mul(rx, ry), mul(rx, rz)), mul(ry, rz));
        an = mul(splat(0.25), add(an, lambda));
        xn = mul(splat(0.25), add(xn, lambda));
        yn = mul(splat(0.25), add(yn, lambda));
        zn = mul(splat(0.25), add(zn, lambda));
        q = mul(splat(0.25), q);
        fn_ = mul(splat(4.0), fn_);
        let conv = _mm256_movemask_pd(_mm256_cmp_pd(q, abs4(an), _CMP_LT_OQ));
        if conv == 0xF {
            break;
        }
    }
    let xx = div(sub(a0, x), mul(an, fn_));
    let yy = div(sub(a0, y), mul(an, fn_));
    let zz = sub(splat(0.0), add(xx, yy));
    let e2 = sub(mul(xx, yy), mul(zz, zz));
    let e3 = mul(mul(xx, yy), zz);
    // Boost tail verbatim: 1 + E3*(1/14 + 3*E3/104) + E2*(-1/10 + E2/24 - 3*E3/44 - 5*E2^2/208 + E2*E3/16)
    let tail_inner = add(
        add(
            sub(splat(-1.0 / 10.0), mul(e3, splat(3.0 / 44.0))),
            sub(mul(e2, splat(1.0 / 24.0)), mul(mul(e2, e2), splat(5.0 / 208.0))),
        ),
        mul(mul(e2, e3), splat(1.0 / 16.0)),
    );
    let numerator = add(
        add(splat(1.0), mul(e3, splat(1.0 / 14.0))),
        add(mul(mul(e3, e3), splat(3.0 / 104.0)), mul(e2, tail_inner)),
    );
    div(numerator, _mm256_sqrt_pd(an))
}

unsafe fn rj4(x: __m256d, y: __m256d, z: __m256d, p: __m256d) -> __m256d {
    let mut xn = x;
    let mut yn = y;
    let mut zn = z;
    let mut pn = p;
    let mut an = mul(splat(0.2), add(add(add(x, y), z), mul(splat(2.0), p)));
    let a0 = an;
    let mut delta = mul(mul(sub(p, x), sub(p, y)), sub(p, z));
    let q0 = mul(
        splat((5.0 / f64::EPSILON).sqrt().sqrt().sqrt()),
        max4(
            max4(max4(abs4(sub(an, x)), abs4(sub(an, y))), abs4(sub(an, z))),
            abs4(sub(an, p)),
        ),
    );
    let mut fmn = splat(1.0);
    let mut rc_sum = splat(0.0);
    let limit = splat(f64::EPSILON.cbrt().sqrt());
    for _ in 0..64 {
        let rx = _mm256_sqrt_pd(xn);
        let ry = _mm256_sqrt_pd(yn);
        let rz = _mm256_sqrt_pd(zn);
        let rp = _mm256_sqrt_pd(pn);
        let dn = mul(mul(add(rp, rx), add(rp, ry)), add(rp, rz));
        let mut en = div(delta, dn);
        en = div(en, dn);
        let series = add(
            splat(1.0),
            mul(
                en,
                add(
                    splat(-1.0 / 3.0),
                    mul(
                        en,
                        add(
                            splat(1.0 / 5.0),
                            mul(
                                en,
                                add(
                                    splat(-1.0 / 7.0),
                                    mul(en, add(splat(1.0 / 9.0), mul(en, splat(-1.0 / 11.0)))),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        );
        let small = _mm256_movemask_pd(_mm256_cmp_pd(abs4(en), limit, _CMP_LT_OQ));
        let mut term = series;
        if small != 0xF {
            let e = store4(en);
            for lane in 0..4 {
                if small & (1 << lane) == 0 {
                    let v = splat(rc1p(e[lane]));
                    term = match lane {
                        0 => _mm256_blend_pd(term, v, 0b0001),
                        1 => _mm256_blend_pd(term, v, 0b0010),
                        2 => _mm256_blend_pd(term, v, 0b0100),
                        _ => _mm256_blend_pd(term, v, 0b1000),
                    };
                }
            }
        }
        rc_sum = add(rc_sum, mul(div(fmn, dn), term));
        let lambda = add(add(mul(rx, ry), mul(rx, rz)), mul(ry, rz));
        an = mul(splat(0.25), add(an, lambda));
        fmn = mul(splat(0.25), fmn);
        let conv = _mm256_movemask_pd(_mm256_cmp_pd(mul(fmn, q0), an, _CMP_LT_OQ));
        if conv == 0xF {
            break;
        }
        xn = mul(splat(0.25), add(xn, lambda));
        yn = mul(splat(0.25), add(yn, lambda));
        zn = mul(splat(0.25), add(zn, lambda));
        pn = mul(splat(0.25), add(pn, lambda));
        delta = div(delta, splat(64.0));
    }
    let xx = div(mul(fmn, sub(a0, x)), an);
    let yy = div(mul(fmn, sub(a0, y)), an);
    let zz = div(mul(fmn, sub(a0, z)), an);
    let pp = mul(splat(0.5), sub(splat(0.0), add(add(xx, yy), zz)));
    let e2 = add(
        sub(add(mul(xx, yy), mul(xx, zz)), mul(splat(3.0), mul(pp, pp))),
        mul(yy, zz),
    );
    let e3 = add(
        add(mul(mul(xx, yy), zz), mul(splat(2.0), mul(e2, pp))),
        mul(splat(4.0), mul(mul(pp, pp), pp)),
    );
    let e4 = mul(
        add(
            add(
                mul(splat(2.0), mul(mul(xx, yy), zz)),
                mul(e2, pp),
            ),
            mul(splat(3.0), mul(mul(pp, pp), pp)),
        ),
        pp,
    );
    let e5 = mul(mul(mul(xx, yy), zz), mul(pp, pp));
    // Boost tail verbatim:
    // 1 - 3E2/14 + E3/6 + 9E2^2/88 - 3E4/22 - 9E2E3/52 + 3E5/26 - E2^3/16
    //   + 3E3^2/40 + 3E2E4/20 + 45E2^2E3/272 - 9(E3E4 + E2E5)/68
    let s1 = sub(splat(1.0), mul(e2, splat(3.0 / 14.0)));
    let s2 = add(s1, mul(e3, splat(1.0 / 6.0)));
    let s3 = add(s2, mul(mul(e2, e2), splat(9.0 / 88.0)));
    let s4 = sub(s3, mul(e4, splat(3.0 / 22.0)));
    let s5 = sub(s4, mul(mul(e2, e3), splat(9.0 / 52.0)));
    let s6 = add(s5, mul(e5, splat(3.0 / 26.0)));
    let s7 = sub(s6, mul(mul(mul(e2, e2), e2), splat(1.0 / 16.0)));
    let s8 = add(s7, mul(mul(e3, e3), splat(3.0 / 40.0)));
    let s9 = add(s8, mul(mul(e2, e4), splat(3.0 / 20.0)));
    let s10 = add(s9, mul(mul(mul(e2, e2), e3), splat(45.0 / 272.0)));
    let series = sub(s10, mul(add(mul(e3, e4), mul(e2, e5)), splat(9.0 / 68.0)));
    add(
        mul(div(fmn, mul(an, _mm256_sqrt_pd(an))), series),
        mul(splat(6.0), rc_sum),
    )
}

// ------------------------------------------------------------ SoA batch state
struct SoA {
    n: usize,
    k: Vec<f64>,
    q: Vec<f64>,
    n3: Vec<f64>,
    mg: Vec<f64>,
    n4: Vec<f64>,
    tnum: Vec<f64>,
    dnum: Vec<f64>,
    ch: Vec<f64>,
    pinv: Vec<f64>,
    a: Vec<f64>,
    m: Vec<f64>,
    q0: Vec<f64>,
    q1: Vec<f64>,
    c1: Vec<f64>,
    kap: Vec<f64>,
    aa: Vec<f64>,
    bb2: Vec<f64>,
    gg: Vec<f64>,
    u: Vec<f64>,
    u_t: Vec<f64>,
    t_true: Vec<f64>,
    t: Vec<f64>,
    slope: Vec<f64>,
    adv: Vec<f64>,
    tau: Vec<f64>,
    du: Vec<f64>,
    active: Vec<bool>,
    iters: Vec<u8>,
}

impl SoA {
    fn new(k: Vec<f64>, q: Vec<f64>, u_t: Vec<f64>) -> Self {
        let n = k.len();
        let mut s = SoA {
            n,
            k,
            q,
            n3: vec![0.0; n],
            mg: vec![0.0; n],
            n4: vec![0.0; n],
            tnum: vec![0.0; n],
            dnum: vec![0.0; n],
            ch: vec![0.0; n],
            pinv: vec![0.0; n],
            a: vec![0.0; n],
            m: vec![0.0; n],
            q0: vec![0.0; n],
            q1: vec![0.0; n],
            c1: vec![0.0; n],
            kap: vec![0.0; n],
            aa: vec![0.0; n],
            bb2: vec![0.0; n],
            gg: vec![0.0; n],
            u: vec![0.0; n],
            u_t: u_t.clone(),
            t_true: vec![0.0; n],
            t: vec![0.0; n],
            slope: vec![0.0; n],
            adv: vec![0.0; n],
            tau: vec![0.0; n],
            du: vec![0.0; n],
            active: vec![true; n],
            iters: vec![0; n],
        };
        // untimed: mint the promotion inputs (target times at the drawn phases),
        // via the verified scalar arm.
        for i in 0..n {
            let c = ctx_new(s.k[i], s.q[i]);
            s.t_true[i] = channels(u_t[i], &c).1;
            s.u[i] = u_t[i];
        }
        s
    }

    /// Timed setup pass: per-body coefficient solves + constants.
    fn setup(&mut self) {
        for i in 0..self.n {
            let c = ctx_new(self.k[i], self.q[i]);
            self.n3[i] = c.n3;
            self.mg[i] = c.mg;
            self.n4[i] = c.n4;
            self.tnum[i] = c.tnum;
            self.dnum[i] = c.dnum;
            self.ch[i] = c.ch;
            self.pinv[i] = c.pinv;
            self.a[i] = c.a;
            self.m[i] = c.m;
            self.q0[i] = c.q0;
            self.q1[i] = c.q1;
            self.c1[i] = c.c1;
            self.kap[i] = c.kap;
            self.aa[i] = c.aa;
            self.bb2[i] = c.bb2;
            self.gg[i] = c.gg;
        }
    }

    fn ctx_at(&self, i: usize) -> Ctx {
        Ctx {
            n3: self.n3[i],
            mg: self.mg[i],
            n4: self.n4[i],
            tnum: self.tnum[i],
            dnum: self.dnum[i],
            ch: self.ch[i],
            pinv: self.pinv[i],
            q: self.q[i],
            a: self.a[i],
            m: self.m[i],
            q0: self.q0[i],
            q1: self.q1[i],
            c1: self.c1[i],
            kap: self.kap[i],
            aa: self.aa[i],
            bb2: self.bb2[i],
            gg: self.gg[i],
        }
    }

    /// ufunc-style batched channel pass (scalar kernels over SoA arrays).
    fn channels_pass(&mut self) {
        for i in 0..self.n {
            let c = self.ctx_at(i);
            let (adv, t, tau, slope) = channels(self.u[i], &c);
            self.adv[i] = adv;
            self.t[i] = t;
            self.tau[i] = tau;
            self.slope[i] = slope;
        }
    }

    /// 4-wide AVX2 batched channel pass (scalar sin/cos per lane; no vector libm).
    #[target_feature(enable = "avx2")]
    unsafe fn channels_pass4(&mut self) {
        let n4pad = self.n & !3;
        let mut i = 0;
        while i < n4pad {
            let load = |v: &Vec<f64>| _mm256_loadu_pd(v.as_ptr().add(i));
            let n3 = load(&self.n3);
            let mg = load(&self.mg);
            let n4c = load(&self.n4);
            let tnum = load(&self.tnum);
            let dnum = load(&self.dnum);
            let ch = load(&self.ch);
            let pinv = load(&self.pinv);
            let q = load(&self.q);
            let ac = load(&self.a);
            let mc = load(&self.m);
            let q0 = load(&self.q0);
            let q1 = load(&self.q1);
            let c1 = load(&self.c1);
            let kap = load(&self.kap);
            let aa = load(&self.aa);
            let bb2 = load(&self.bb2);
            let gg = load(&self.gg);
            let uv = load(&self.u);
            let ua = store4(uv);
            let mut sa = [0f64; 4];
            let mut ca = [0f64; 4];
            for l in 0..4 {
                sa[l] = ua[l].sin();
                ca[l] = ua[l].cos();
            }
            let s = _mm256_loadu_pd(sa.as_ptr());
            let co = _mm256_loadu_pd(ca.as_ptr());
            let s2 = mul(s, s);
            let c2 = mul(co, co);
            let s3 = mul(s2, s);
            let w2 = sub(splat(1.0), mul(mg, s2));
            let w = _mm256_sqrt_pd(w2);
            let v = sub(splat(1.0), mul(n3, s2));
            let f = mul(s, rf4(c2, w2, splat(1.0)));
            let pi_n3 = add(
                f,
                mul(
                    mul(mul(n3, splat(1.0 / 3.0)), s3),
                    rj4(c2, w2, splat(1.0), sub(splat(1.0), mul(n3, s2))),
                ),
            );
            let pi_mn4 = add(
                f,
                mul(
                    mul(mul(n4c, splat(-1.0 / 3.0)), s3),
                    rj4(c2, w2, splat(1.0), add(splat(1.0), mul(n4c, s2))),
                ),
            );
            let e_ch = sub(
                f,
                mul(
                    mul(mul(mg, splat(1.0 / 3.0)), s3),
                    rj4(c2, w2, splat(1.0), splat(1.0)),
                ),
            );
            let i2 = add(
                add(
                    mul(q0, f),
                    div(mul(q1, sub(f, e_ch)), mg),
                ),
                add(
                    mul(c1, pi_n3),
                    div(mul(mul(mul(kap, s), co), w), v),
                ),
            );
            let adv = div(sub(mul(ch, f), mul(splat(2.0), uv)), q);
            let tau = mul(mul(dnum, ch), i2);
            let t = mul(
                mul(mul(tnum, ch), pinv),
                add(add(mul(aa, pi_n3), mul(bb2, i2)), mul(gg, pi_mn4)),
            );
            let slope = div(
                mul(splat(2.0), tnum),
                mul(
                    mul(
                        _mm256_sqrt_pd(mul(ac, sub(splat(1.0), mul(mc, c2)))),
                        mul(v, v),
                    ),
                    sub(splat(1.0), mul(splat(2.0), mul(q, v))),
                ),
            );
            _mm256_storeu_pd(self.adv.as_mut_ptr().add(i), adv);
            _mm256_storeu_pd(self.t.as_mut_ptr().add(i), t);
            _mm256_storeu_pd(self.tau.as_mut_ptr().add(i), tau);
            _mm256_storeu_pd(self.slope.as_mut_ptr().add(i), slope);
            i += 4;
        }
        for j in n4pad..self.n {
            let c = self.ctx_at(j);
            let (adv, t, tau, slope) = channels(self.u[j], &c);
            self.adv[j] = adv;
            self.t[j] = t;
            self.tau[j] = tau;
            self.slope[j] = slope;
        }
    }

    /// Batched Newton after setup: cold pass + iterating passes + final read.
    fn newton(&mut self, avx: bool) -> u32 {
        for i in 0..self.n {
            self.u[i] = PI_2;
            self.active[i] = true;
            self.iters[i] = 0;
        }
        unsafe {
            if avx {
                self.channels_pass4();
            } else {
                self.channels_pass();
            }
        }
        for i in 0..self.n {
            self.u[i] = PI_2 * (self.t_true[i] / self.t[i]);
        }
        let mut passes = 0u32;
        for _ in 0..60 {
            unsafe {
                if avx {
                    self.channels_pass4();
                } else {
                    self.channels_pass();
                }
            }
            passes += 1;
            let mut any = false;
            for i in 0..self.n {
                if self.active[i] {
                    let du = (self.t_true[i] - self.t[i]) / self.slope[i];
                    self.du[i] = du;
                    self.u[i] = (self.u[i] + du).clamp(1e-12, PI_2 - 1e-12);
                    self.iters[i] += 1;
                    if du.abs() < 1e-13 {
                        self.active[i] = false;
                    } else {
                        any = true;
                    }
                }
            }
            if !any {
                break;
            }
        }
        unsafe {
            if avx {
                self.channels_pass4();
            } else {
                self.channels_pass();
            }
        }
        passes
    }
}

// ------------------------------------------------------------------ belt keys
/// scenario.rs ladder_ship belt lane: a uniform in [2,3) AU at Q8, e Rayleigh(0.07)
/// re-drawn at 0.4, p = a(1-e) at Q8. Returns (p_q8, e_q48).
fn belt_draw(rng: &mut Rng) -> (u64, u64) {
    let a_q8 = ((2 * AU) << 8) + (rng.next() % ((AU as u64) << 8));
    let mut e = 1.0f64;
    while e > 0.4 {
        let u1 = rng.unit().max(1e-18);
        e = 0.07 * (-2.0 * u1.ln()).sqrt();
    }
    let e_q48 = ((e * ((1u64 << 48) as f64)) as u64).min((1u64 << 48) - 1);
    let p_q8 = a_q8 - (((a_q8 as u128 * e_q48 as u128) >> 48) as u64);
    (p_q8, e_q48)
}

fn kf(e_q48: u64) -> f64 {
    1.0 / (1.0 + e_q48 as f64 / (1u64 << 48) as f64)
}

fn black_box<T>(x: T) -> T {
    std::hint::black_box(x)
}

fn median(v: &mut [f64]) -> f64 {
    v.sort_by(|a, b| a.partial_cmp(b).unwrap());
    v[v.len() / 2]
}

fn run_grid() {
    println!("\n== value: wider grid (the promise 262f dropped) ==");
    let es = [0.001, 0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99, 0.999];
    let ps = [7.0, 100.0, 1e4, 1e6, 1e8];
    let us = [
        std::f64::consts::FRAC_PI_8,
        std::f64::consts::FRAC_PI_4,
        3.0 * std::f64::consts::FRAC_PI_8,
        PI_2 - 1e-3,
    ];
    let (mut g_adv, mut g_t, mut g_tau) = (0f64, 0f64, 0f64);
    let mut worst = String::new();
    let mut worst_t = String::new();
    let mut g_iters = 0u32;
    let mut g_uerr = 0f64;
    for &e in &es {
        for &p in &ps {
            for &u in &us {
                let k = 1.0 / (1.0 + e);
                let q = 1.0 / p;
                let c = ctx_new(k, q);
                let (a0, t0, tau0, _) = channels(u, &c);
                let (a1, t1, tau1) = channels_simpson(k, q, u);
                let rt = (t0 - t1).abs() / t1.abs();
                let rtau = (tau0 - tau1).abs() / tau1.abs();
                let radv = (a0 - a1).abs() / a1.abs();
                if rt > g_t {
                    g_t = rt;
                    worst_t = format!("e={} p={} u={:.6} (t {:+.6e} simp {:+.6e})", e, p, u, t0, t1);
                }
                if rtau > g_tau {
                    g_tau = rtau;
                }
                if radv > g_adv {
                    g_adv = radv;
                    worst = format!("e={} p={} u={:.4}", e, p, u);
                }
                let mut it = 0u32;
                let mut uo = 0f64;
                let _ = promote_scalar(&c, t0, &mut it, &mut uo);
                g_iters = g_iters.max(it);
                g_uerr = g_uerr.max((uo - u).abs());
            }
        }
    }
    println!("grid worst t at: {}", worst_t);
    println!(
        "grid ({} pts): t {:.2e}  tau {:.2e}  adv {:.2e} (worst adv at {})",
        es.len() * ps.len() * us.len(),
        g_t,
        g_tau,
        g_adv,
        worst
    );
    println!(
        "grid newton worst iters: {} (cap 60), worst recovered-u err {:.1e}",
        g_iters, g_uerr
    );
}

fn main() {
    // bisect mode: cargo run --release -- --one k q u
    let args: Vec<String> = std::env::args().collect();
    let grid_only = args.iter().any(|a| a == "--grid");
    if args.iter().any(|a| a == "--trace") {
        let (x, y, z, p) = (1e-6f64, 1.5714285714285714f64, 1.0f64, 1.2666666666666666f64);
        let mut xn = x; let mut yn = y; let mut zn = z; let mut pn = p;
        let mut an = (x + y + z + 2.0 * p) / 5.0;
        let a0 = an;
        let mut delta = (p - x) * (p - y) * (p - z);
        let q0 = (5.0 / f64::EPSILON).sqrt().sqrt().sqrt()
            * (an - x).abs().max((an - y).abs()).max((an - z).abs()).max((an - p).abs());
        let mut fmn = 1.0f64;
        let mut rc_sum = 0.0f64;
        let series_limit = f64::EPSILON.cbrt().sqrt();
        println!("a0={a0:.6} q0={q0:.4} delta={delta:.6e} limit={series_limit:.4e}");
        for it in 0..10 {
            let root_x = xn.sqrt(); let root_y = yn.sqrt(); let root_z = zn.sqrt(); let root_p = pn.sqrt();
            let dn = (root_p + root_x) * (root_p + root_y) * (root_p + root_z);
            let mut en = delta / dn; en /= dn;
            let term = if en.abs() < series_limit { 1.0 } else { rc1p(en) };
            rc_sum += fmn / dn * term;
            println!("it={it} dn={dn:.6} en={en:.6e} fmn={fmn:.6e} rc_sum={rc_sum:.6} an={an:.6}", );
            let lambda = root_x * root_y + root_x * root_z + root_y * root_z;
            an = (an + lambda) / 4.0;
            fmn /= 4.0;
            if fmn * q0 < an { println!("break: {} < {}", fmn * q0, an); break; }
            xn = (xn + lambda) / 4.0; yn = (yn + lambda) / 4.0; zn = (zn + lambda) / 4.0; pn = (pn + lambda) / 4.0;
            delta /= 64.0;
        }
        println!("final rc_sum={rc_sum:.9} => approx {}", 6.0 * rc_sum);
        return;
    }
    if args.iter().any(|a| a == "--rj") {
        // Carlson's published test values: RJ(2,3,4,5)=0.142975796671567544...
        unsafe { std::hint::black_box(()); }
        let cases = [
            (2.0, 3.0, 4.0, 5.0),
            (1e-6, 1.0, 1.0, 1.2666666666666666),
            (0.5, 0.5, 0.5, 2.0),
            (1.0, 2.0, 0.0, 1.0),
            (0.01, 1.0, 1.0, 1.5),
            (1e-6, 1.0000000004, 1.0, 1.2666666666666666),
            (1e-6, 1.5714285714285714, 1.0, 1.2666666666666666),
        ];
        for (x, y, z, p) in cases {
            println!("rj({:>9.6},{:>9.6},{:>9.6},{:>9.6}) = {:.17}", x, y, z, p, rj(x, y, z, p));
        }
        return;
    }
    if args.len() == 5 && args[1] == "--one" {
        let k: f64 = args[2].parse().unwrap();
        let q: f64 = args[3].parse().unwrap();
        let u: f64 = args[4].parse().unwrap();
        let c = ctx_new(k, q);
        let s = u.sin();
        let co = u.cos();
        let s2 = s * s;
        let c2 = co * co;
        let s3 = s2 * s;
        let w2 = 1.0 - c.mg * s2;
        let v = 1.0 - c.n3 * s2;
        unsafe {
            let x4 = _mm256_set1_pd(c2);
            let y4 = _mm256_set1_pd(w2);
            let o4 = _mm256_set1_pd(1.0);
            let rf_s = rf(c2, w2, 1.0);
            let rf_v = store4(rf4(x4, y4, o4))[0];
            println!("rf  scalar {:.17e}  avx2 {:.17e}  diff {:.2e}", rf_s, rf_v, (rf_s - rf_v).abs());
            for (name, p) in [("pi_n3", 1.0 - c.n3 * s2), ("pi_mn4", 1.0 + c.n4 * s2), ("e_ch", 1.0)] {
                let rj_s = rj(c2, w2, 1.0, p);
                let rj_v = store4(rj4(x4, y4, o4, _mm256_set1_pd(p)))[0];
                println!("rj {} (p={:.6})  scalar {:.17e}  avx2 {:.17e}  diff {:.2e}", name, p, rj_s, rj_v, (rj_s - rj_v).abs());
            }
            let f_s = s * rf_s;
            let f_v = s * rf_v;
            println!("f   scalar {:.17e}  avx2 {:.17e}  diff {:.2e}", f_s, f_v, (f_s - f_v).abs());
            let (adv_s, t_s, tau_s, sl_s) = channels(u, &c);
            println!("adv scalar {:.9e}  t {:.9e} tau {:.9e} slope {:.9e}", adv_s, t_s, tau_s, sl_s);
            let (a1, t1, tau1) = channels_simpson(k, q, u);
            println!("simpson adv {:.9e}  t {:.9e} tau {:.9e}", a1, t1, tau1);
        }
        return;
    }
    let load = std::fs::read_to_string("/proc/loadavg").unwrap_or_default();
    let cpu = std::fs::read_to_string("/proc/cpuinfo")
        .unwrap_or_default()
        .lines()
        .find(|l| l.starts_with("model name"))
        .map(|l| l.split(':').nth(1).unwrap_or("").trim().to_string())
        .unwrap_or_default();
    println!("== machine ==");
    println!("cpu: {}", cpu);
    println!(
        "nproc: {}, loadavg: {}",
        std::thread::available_parallelism().unwrap(),
        load.trim()
    );

    // ---------------------------------------------------------------- value checks
    if grid_only {
        run_grid();
        return;
    }

    // ---------------------------------------------------------------- value checks
    println!("\n== value: closed vs Simpson of the shipped node() integrands (belt mix, 200 keys) ==");
    let mut rng = Rng(0xA5A5_1234_0000_0001);
    let (mut mx_adv, mut mx_t, mut mx_tau) = (0f64, 0f64, 0f64);
    let (mut kvs, mut qvs, mut uvs) = (Vec::new(), Vec::new(), Vec::new());
    for _ in 0..200 {
        let (p_q8, e_q48) = belt_draw(&mut rng);
        let u = rng.unit() * PI_2;
        let k = kf(e_q48);
        let q = 1.0 / (p_q8 as f64 / 256.0);
        let c = ctx_new(k, q);
        let (a0, t0, tau0, _) = channels(u, &c);
        let (a1, t1, tau1) = channels_simpson(k, q, u);
        mx_adv = mx_adv.max((a0 - a1).abs() / a1.abs());
        mx_t = mx_t.max((t0 - t1).abs() / t1.abs());
        mx_tau = mx_tau.max((tau0 - tau1).abs() / tau1.abs());
        kvs.push(k);
        qvs.push(q);
        uvs.push(u);
    }
    println!(
        "scalar vs simpson max rel: adv {:.2e}  t {:.2e}  tau {:.2e}",
        mx_adv, mx_t, mx_tau
    );

    // slope FD check
    let mut mx_slope = 0f64;
    for i in 0..50 {
        let c = ctx_new(kvs[i], qvs[i]);
        let u = uvs[i].clamp(1e-4, PI_2 - 1e-4);
        let (_, _, _, slope) = channels(u, &c);
        let h = 1e-6;
        let fd = (channels(u + h, &c).1 - channels(u - h, &c).1) / (2.0 * h);
        mx_slope = mx_slope.max((slope - fd).abs() / fd.abs());
    }
    println!("analytic slope vs FD: max rel {:.2e}  (bar 1e-6)", mx_slope);

    // batched vs scalar (the check that would have caught 262f's factor-2 slip)
    let n_val = 100_000;
    let (mut k2, mut q2, mut u2) = (
        Vec::with_capacity(n_val),
        Vec::with_capacity(n_val),
        Vec::with_capacity(n_val),
    );
    for _ in 0..n_val {
        let (p_q8, e_q48) = belt_draw(&mut rng);
        k2.push(kf(e_q48));
        q2.push(1.0 / (p_q8 as f64 / 256.0));
        u2.push(rng.unit() * PI_2);
    }
    let mut soa = SoA::new(k2.clone(), q2.clone(), u2.clone());
    soa.setup();
    soa.u.copy_from_slice(&u2);
    soa.channels_pass();
    let (mut bt, mut btau, mut badv) = (0f64, 0f64, 0f64);
    for i in 0..n_val {
        let c = ctx_new(k2[i], q2[i]);
        let (a0, t0, tau0, _) = channels(u2[i], &c);
        badv = badv.max((soa.adv[i] - a0).abs() / a0.abs());
        bt = bt.max((soa.t[i] - t0).abs() / t0.abs());
        btau = btau.max((soa.tau[i] - tau0).abs() / tau0.abs());
    }
    println!(
        "soa batch vs scalar  max rel: adv {:.2e}  t {:.2e}  tau {:.2e}",
        badv, bt, btau
    );
    let mut soa4 = SoA::new(k2, q2, u2.clone());
    soa4.setup();
    soa4.u.copy_from_slice(&u2);
    unsafe { soa4.channels_pass4() };
    let (mut at, mut atau, mut aadv) = (0f64, 0f64, 0f64);
    for i in 0..n_val {
        let c = ctx_new(soa4.k[i], soa4.q[i]);
        let (a0, t0, tau0, _) = channels(u2[i], &c);
        aadv = aadv.max((soa4.adv[i] - a0).abs() / a0.abs());
        at = at.max((soa4.t[i] - t0).abs() / t0.abs());
        atau = atau.max((soa4.tau[i] - tau0).abs() / tau0.abs());
    }
    println!(
        "avx2 batch vs scalar max rel: adv {:.2e}  t {:.2e}  tau {:.2e}",
        aadv, at, atau
    );

    // Newton end-to-end on the scalar arm: recovered phase, iteration counts
    let mut counts: Vec<u32> = Vec::with_capacity(n_val);
    let mut uerr: Vec<f64> = Vec::with_capacity(n_val);
    for i in 0..n_val {
        let c = ctx_new(soa.k[i], soa.q[i]);
        let mut it = 0u32;
        let mut uo = 0f64;
        let _ = promote_scalar(&c, soa.t_true[i], &mut it, &mut uo);
        counts.push(it);
        uerr.push((uo - u2[i]).abs());
    }
    counts.sort();
    uerr.sort_by(|a, b| a.partial_cmp(b).unwrap());
    println!(
        "scalar newton: iters median {} worst {} | recovered-u err max {:.1e} p99 {:.1e}",
        counts[n_val / 2],
        counts[n_val - 1],
        uerr[n_val - 1],
        uerr[(99 * n_val) / 100]
    );

    // ------------------------------------------------------------ wider grid
    run_grid();

    // ---------------------------------------------------------------- timings
    println!("\n== timings (belt keys; per promotion; median of reps) ==");
    let reps = 3;

    // (a) shipped compile
    let n_compile = 100_000;
    let mut rng = Rng(0xC0FF_EEBE_EF00_0001);
    let mut ship_keys = Vec::with_capacity(n_compile);
    for _ in 0..n_compile {
        let (p_q8, e_q48) = belt_draw(&mut rng);
        let num = p_q8 as u128 * ((1u64 << 48) + e_q48 as u64) as u128;
        let p_slr = Scalar::raw(num as i128, -56).unwrap();
        ship_keys.push(OrbitKey::bound(p_slr, e_q48).unwrap());
    }
    // untimed prepass: knot stats on 10k keys
    let mut knots = Vec::new();
    let mut compile_err = 0u64;
    for key in ship_keys.iter().take(10_000) {
        match Orbit::compile(*key) {
            Ok(o) => knots.push(o.shape().knots().len()),
            Err(_) => compile_err += 1,
        }
    }
    knots.sort();
    println!(
        "shipped compile: knots p50 {} p99 {} max {} ({} errors / 10k)",
        knots[knots.len() / 2],
        knots[(99 * knots.len()) / 100],
        knots[knots.len() - 1],
        compile_err
    );
    let mut t_compile: Vec<f64> = Vec::new();
    for _ in 0..reps {
        let mut digest = 0i128;
        let t0 = Instant::now();
        for key in &ship_keys {
            let o = Orbit::compile(*key).unwrap();
            digest += o.period().unwrap().fixed(0).unwrap_or(0);
        }
        let dt = t0.elapsed().as_secs_f64();
        black_box(digest);
        t_compile.push(dt / n_compile as f64 * 1e6);
    }
    println!(
        "(a) shipped compile us/promotion: reps {:.2} {:.2} {:.2} | median {:.2}",
        t_compile[0],
        t_compile[1],
        t_compile[2],
        median(&mut t_compile.clone())
    );

    // (b) native scalar
    let n_scalar = 200_000;
    let mut rng = Rng(0xDEAD_1234_0000_0002);
    let (mut sk, mut sq, mut su) = (Vec::new(), Vec::new(), Vec::new());
    for _ in 0..n_scalar {
        let (p_q8, e_q48) = belt_draw(&mut rng);
        sk.push(kf(e_q48));
        sq.push(1.0 / (p_q8 as f64 / 256.0));
        su.push(rng.unit() * PI_2);
    }
    let mut st_true = Vec::with_capacity(n_scalar);
    for i in 0..n_scalar {
        let c = ctx_new(sk[i], sq[i]);
        st_true.push(channels(su[i], &c).1);
    }
    let mut t_scalar: Vec<f64> = Vec::new();
    let mut scalar_iters_worst = 0u32;
    let mut scalar_uerr_max = 0f64;
    for _ in 0..reps {
        let mut digest = 0f64;
        let t0 = Instant::now();
        for i in 0..n_scalar {
            let c = ctx_new(sk[i], sq[i]); // setup inside the timed region
            let mut it = 0u32;
            let mut uo = 0f64;
            let (adv, tau) = promote_scalar(&c, st_true[i], &mut it, &mut uo);
            digest += adv + tau;
            scalar_iters_worst = scalar_iters_worst.max(it);
            scalar_uerr_max = scalar_uerr_max.max((uo - su[i]).abs());
        }
        let dt = t0.elapsed().as_secs_f64();
        black_box(digest);
        t_scalar.push(dt / n_scalar as f64 * 1e6);
    }
    println!(
        "(b) scalar us/promotion: reps {:.3} {:.3} {:.3} | median {:.3} | iters worst {} | u err {:.1e}",
        t_scalar[0],
        t_scalar[1],
        t_scalar[2],
        median(&mut t_scalar.clone()),
        scalar_iters_worst,
        scalar_uerr_max
    );

    // (c)/(d) batched
    let chunk = 1_000_000usize;
    let mk_chunk = |rng: &mut Rng, n: usize| {
        let (mut k, mut q, mut u) = (
            Vec::with_capacity(n),
            Vec::with_capacity(n),
            Vec::with_capacity(n),
        );
        for _ in 0..n {
            let (p_q8, e_q48) = belt_draw(rng);
            k.push(kf(e_q48));
            q.push(1.0 / (p_q8 as f64 / 256.0));
            u.push(rng.unit() * PI_2);
        }
        (k, q, u)
    };
    for avx in [false, true] {
        let name = if avx { "(d) avx2 batch" } else { "(c) soa batch" };
        let mut rng = Rng(if avx { 0x0BAD_C0DE_0000_0003 } else { 0xFACE_B00C_0000_0004 });
        let (k, q, u) = mk_chunk(&mut rng, chunk);
        let mut b = SoA::new(k, q, u);
        let mut times = Vec::new();
        let mut passes_tot = 0u32;
        for _ in 0..reps {
            let t0 = Instant::now();
            b.setup();
            let p = b.newton(avx);
            let dt = t0.elapsed().as_secs_f64();
            passes_tot = p;
            black_box(b.adv[0] + b.tau[0]);
            times.push(dt / chunk as f64 * 1e6);
        }
        let med6 = median(&mut times.clone());
        let mut uerr_real = 0f64;
        let mut it_worst = 0u8;
        for i in 0..chunk {
            uerr_real = uerr_real.max((b.u[i] - b.u_t[i]).abs());
            it_worst = it_worst.max(b.iters[i]);
        }
        // 1e7: ten fresh chunks, aggregate (memory stays at one chunk)
        let mut total7 = 0f64;
        for _ in 0..10 {
            let (k, q, u) = mk_chunk(&mut rng, chunk);
            let mut b7 = SoA::new(k, q, u);
            let t0 = Instant::now();
            b7.setup();
            b7.newton(avx);
            total7 += t0.elapsed().as_secs_f64();
            black_box(b7.adv[0] + b7.tau[0]);
        }
        println!(
            "{} us/promotion: 1e6 reps {:.3} {:.3} {:.3} med {:.3} | 1e7 aggregate {:.3} | newton passes {} iters worst {} | u err {:.1e}",
            name,
            times[0],
            times[1],
            times[2],
            med6,
            total7 / 1e7 as f64 * 1e6,
            passes_tot,
            it_worst,
            uerr_real
        );
    }

    println!("\n== done ==");
}
