//! The smallest promotion, priced in miniature (components lens, 20261014-2336-components-70c3).
//!
//! Shipped wave kick (crates/universe/src/step.rs kick/kick_clock): read the exact integer state
//! (the compiled tube's turn·decode), evaluate the secondary's tide, sigma-delta `quantize` the dv,
//! add integer quanta — then REBIND: a fresh `Orbit::compile` per kick (1.00 compiles/kick, eb2d;
//! 59-76 µs/kick in-wave incl. attendants, b30b; +2.6-2.7 KB standing mint, ladder break 2).
//!
//! The floor side, built here: the belt body as a compact row of u32 element words plus exact
//! i64 drift accumulators and sigma-delta carries (the B18b row is 31 B; this probe carries four
//! channels + carries = 48 B), kicked WITHOUT compiling anything. One kick = readout (Kepler
//! Newton from the row) + the secondary's differential pull + the exact element update + four
//! sigma-delta quantizations. Two error disciplines on the SAME kick stream, both with feedback:
//!   CARRY: base words + whole-quanta drift applied at readout (one rounding channel, exact Σ);
//!   REQUANT: the row itself re-rounded each kick (the refuted quantized-memo style).
//! Truth: an unrounded f64 twin under identical kicks.
//!
//! Calibration to the shipped stream (a669, checker-confirmed): |dv| p01 ~ 2.4e3 velocity quanta,
//! dL/L ~ 2.1e-7 a kick, 2^7 kicks per 88-day secondary period (the doll's cadence, cf45).
//!
//! rustc -O -o mini mini.rs && ./mini
use std::f64::consts::PI;
use std::time::Instant;

const N_COST: usize = 100_000; // bodies in the cost loop
const N_ERR: usize = 4_096; // bodies in the error loop
const AU: f64 = 1.495978707e11;
const DAY: f64 = 86400.0;
const MU_STAR: f64 = 1.32712440018e20;
const P2: f64 = 88.0 * DAY; // the doll's shortest secondary
const A2: f64 = 1.0 * AU;
const MU2: f64 = MU_STAR * 1.0e-4;
const KPW: f64 = 128.0; // kicks per wave (2^7)
const STEP: f64 = P2 / KPW;
const TAU: f64 = 2.0 * PI;
const SD: f64 = 65536.0; // sigma-delta sub-quantum units, the shipped quantize discipline (2^-16)
const Q32: f64 = 4294967296.0;

struct Rng(u64);
impl Rng {
    fn u64(&mut self) -> u64 {
        let mut x = self.0;
        x ^= x >> 12;
        x ^= x << 25;
        x ^= x >> 27;
        self.0 = x;
        x.wrapping_mul(0x2545F4914F6CDD1D)
    }
    fn f(&mut self) -> f64 {
        (self.u64() >> 11) as f64 * (1.0 / 9007199254740992.0)
    }
}

/// Full element state (a in AU, e, periapsis w rad, phase m0 rad: M(t) = m0 + n·t).
#[derive(Clone, Copy)]
struct El {
    a: f64,
    e: f64,
    w: f64,
    m0: f64,
}

/// The compact row: four u32 element words, four i64 whole-quanta drift words, four i64 carries.
#[derive(Clone, Copy)]
struct Row {
    base: [u32; 4], // a (Q32 of the 1 AU span from 2), e (Q32 of 0.4), w, m0 (Q32 of TAU)
    drift: [i64; 4],
    carry: [i64; 4],
}
const ROW_BYTES: usize = 16 + 32 + 32;

fn to_row(s: El) -> Row {
    Row {
        base: [
            (((s.a - 2.0) / 1.0) * Q32) as u32,
            ((s.e / 0.4) * Q32) as u32,
            ((s.w / TAU) * Q32) as u32,
            ((s.m0 / TAU) * Q32) as u32,
        ],
        drift: [0; 4],
        carry: [0; 4],
    }
}

impl Row {
    /// CARRY discipline: base + whole-quanta drift, angles via wrapped add.
    fn read(&self) -> El {
        let d = |i: usize| self.drift[i] as f64 / Q32; // drift holds whole quanta of the word
        El {
            a: 2.0 + self.base[0] as f64 / Q32 + d(0),
            e: self.base[1] as f64 / Q32 * 0.4 + d(1) * 0.4,
            w: self.base[2] as f64 / Q32 * TAU + d(2) * TAU,
            m0: self.base[3] as f64 / Q32 * TAU + d(3) * TAU,
        }
    }
}

/// Readout: Kepler Newton (e <= 0.4) then (x, v). The only compute a kick needs.
fn readout(s: &El, t: f64) -> ((f64, f64), (f64, f64)) {
    let a = s.a * AU;
    let n = (MU_STAR / (a * a * a)).sqrt();
    let m = s.m0 + n * t;
    let e = s.e;
    let mk = m % TAU;
    let mut ek = mk + e * mk.sin();
    for _ in 0..3 {
        let f = ek - e * ek.sin() - mk;
        ek -= f / (1.0 - e * ek.cos());
    }
    let (ce, se) = (ek.cos(), ek.sin());
    let p = a * (1.0 - e * e);
    let r = p / (1.0 + e * ce);
    let (cw, sw) = (s.w.cos(), s.w.sin());
    let ur = (ce * cw - se * sw, se * cw + ce * sw);
    let ut = (-se * cw - ce * sw, ce * cw - se * sw);
    let k = (MU_STAR / p).sqrt();
    let vr = k * e * se;
    let vt = k * (1.0 + e * ce);
    (
        (r * ur.0, r * ur.1),
        (vr * ur.0 + vt * ut.0, vr * ur.1 + vt * ut.1),
    )
}

/// The exact element update of an impulse at time t: (x,v) -> elements of (x, v+dv).
fn kick_elements_xy(s: &El, t: f64, pos: (f64, f64), v: (f64, f64), dv: (f64, f64)) -> El {
    let (x0, y0) = pos;
    let (vx, vy) = (v.0 + dv.0, v.1 + dv.1);
    let v2 = vx * vx + vy * vy;
    let r = (x0 * x0 + y0 * y0).sqrt();
    let a = 1.0 / (2.0 / r - v2 / MU_STAR);
    let rv = x0 * vx + y0 * vy;
    let c = v2 / MU_STAR - 1.0 / r;
    let ex = c * x0 + rv / MU_STAR * vx;
    let ey = c * y0 + rv / MU_STAR * vy;
    let e = (ex * ex + ey * ey).sqrt();
    let w = ey.atan2(ex);
    // mean anomaly at t on the new orbit (position-continuous), then m0 = M - n'·t
    let f = y0.atan2(x0) - w;
        let ef = 2.0 * ((1.0 - e).max(0.0).sqrt() * (f / 2.0).sin())
        .atan2((1.0 + e).sqrt() * (f / 2.0).cos());
    let mm = ef - e * ef.sin();
    let n = (MU_STAR / (a * a * a)).sqrt();
    let m0 = mm - n * t;
    El { a: a / AU, e, w, m0 }
}

/// The secondary's differential pull over one step (the indirect term is common to the doll).
fn tide(x: (f64, f64), th2: f64) -> (f64, f64) {
    let (x2, y2) = (A2 * th2.cos(), A2 * th2.sin());
    let (dx, dy) = (x2 - x.0, x2 - x.1);
    let d3 = (dx * dx + dy * dy).powf(1.5);
    (MU2 * dx / d3 * STEP, MU2 * dy / d3 * STEP)
}

/// Sigma-delta quantize an element delta into (whole quanta, new carry), channel c of a row.
fn quantize(delta_quanta: f64, carry: i64) -> (i64, i64) {
    let tot = carry as f64 + delta_quanta * SD;
    let whole = tot.div_euclid(SD) as i64;
    (whole, tot.rem_euclid(SD) as i64)
}

fn belt(n: usize, seed: u64) -> Vec<El> {
    let mut rng = Rng(seed);
    (0..n)
        .map(|_| {
            let e = loop {
                let e = 0.07 * (-2.0 * (1.0 - rng.f()).ln()).sqrt(); // Rayleigh scale 0.07, the ladder's belt
                if e < 0.4 {
                    break e;
                }
            };
            El { a: 2.0 + rng.f(), e, w: rng.f() * TAU, m0: rng.f() * TAU }
        })
        .collect()
}

fn main() {
    // ---- calibration: |dv| per kick and element deltas, on the first 4096 rows --------------
    let cal = belt(4096, 0x9E3779B97F4A7C15 ^ 20261014);
    let mut dvs = Vec::new();
    let mut das = Vec::new();
    let mut des = Vec::new();
    for s in &cal {
        let (x, v) = readout(s, 0.0);
        let dv = tide(x, 0.0);
        dvs.push((dv.0 * dv.0 + dv.1 * dv.1).sqrt());
        let s1 = kick_elements_xy(s, 0.0, x, v, dv);
        das.push((s1.a - s.a).abs());
        des.push((s1.e - s.e).abs());
    }
    dvs.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let dv_p01 = dvs[dvs.len() / 100];
    let dv_p50 = dvs[dvs.len() / 2];
    // element quanta per kick, in SD sub-units of the u32 words
    let qa_sd = das.iter().sum::<f64>() / das.len() as f64 / (1.0 / Q32) * SD; // mean |Δa| in SD units
    let qe_sd = des.iter().sum::<f64>() / des.len() as f64 / (0.4 / Q32) * SD;
    println!("calib: |dv| p50 {:+.3e} m/s p01 {:+.3e} (a669 p01 2.4e3 quanta) ; |da| {qa_sd:.1} |de| {qe_sd:.1} SD-units/kick (SD=2^-16 quanta)", dv_p50, dv_p01);

    // ---- the cost loop: CARRY only, one wave over 100k rows --------------------------------
    let mut rows: Vec<Row> = belt(N_COST, 0x9E3779B97F4A7C15 ^ 20261014).into_iter().map(to_row).collect();
    let mut fired = 0u64;
    let mut samples = Vec::new();
    let t0 = Instant::now();
    for k in 0..KPW as i64 {
        let t = k as f64 * STEP;
        let th2 = TAU / P2 * (t + STEP * 0.5);
        let tk = Instant::now();
        for r in rows.iter_mut() {
            let s = r.read();
            let (x, v) = readout(&s, t);
            let dv = tide(x, th2);
            let s1 = kick_elements_xy(&s, t, x, v, dv);
            let da_q = (s1.a - s.a) * Q32; // quanta of the u32 word
            let de_q = (s1.e - s.e) / 0.4 * Q32;
            let dw_q = (s1.w - s.w) / TAU * Q32;
            let dm_q = (s1.m0 - s.m0) / TAU * Q32;
            let (wa, ca) = quantize(da_q, r.carry[0]);
            let (we, ce) = quantize(de_q, r.carry[1]);
            let (ww, cw) = quantize(dw_q, r.carry[2]);
            let (wm, cm) = quantize(dm_q, r.carry[3]);
            r.carry = [ca, ce, cw, cm];
            if wa != 0 || we != 0 || ww != 0 || wm != 0 {
                r.drift[0] += wa;
                r.drift[1] += we;
                r.drift[2] += ww;
                r.drift[3] += wm;
                fired += 1;
            }
        }
        samples.push(tk.elapsed().as_secs_f64() / rows.len() as f64);
    }
    let cost_s = t0.elapsed().as_secs_f64();
    samples.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let ns_p50 = samples[samples.len() / 2] * 1e9;
    println!(
        "cost: {ns_p50:.0} ns/kick p50 (N={}, one wave, CARRY discipline) ; fired {}/{} = {:.3} ; wall {cost_s:.2} s",
        N_COST, fired, N_COST * KPW as usize, fired as f64 / (N_COST * KPW as usize) as f64
    );
    println!("bytes: row {ROW_BYTES} B ; shipped belt body 2,407-2,632 B at birth, ~4,900-5,100 B after wave 1 (ladder) ; ratio {:.0}x-{:.0}x / {:.0}x-{:.0}x",
        2407 / ROW_BYTES, 2632 / ROW_BYTES, 4900 / ROW_BYTES, 5100 / ROW_BYTES);

    // ---- the error loop: CARRY vs REQUANT vs exact, 20 waves, with feedback -----------------
    let n = N_ERR;
    let waves = 20u64;
    let belt0 = belt(n, 0x9E3779B97F4A7C15 ^ 20261014);
    let mut exact = belt0.clone();
    let mut carry: Vec<Row> = belt0.iter().map(|s| to_row(*s)).collect();
    let mut requant: Vec<Row> = belt0.iter().map(|s| to_row(*s)).collect();
    let t_check = (waves as f64) * P2;
    let check = |tag: &str, exact: &[El], carry: &[Row], requant: &[Row]| {
        let mut ec = vec![0f64; 4];
        let mut er = vec![0f64; 4];
        let scale = [1.0 / Q32, 0.4 / Q32, TAU / Q32, TAU / Q32]; // quanta of each channel
        let mut pc = 0f64;
        let mut pr = 0f64;
        for i in 0..exact.len() {
            let c = carry[i].read();
            let r = requant[i].read();
            let (xe, _) = readout(&exact[i], t_check);
            let (xc, _) = readout(&c, t_check);
            let (xr, _) = readout(&r, t_check);
            pc = pc.max(((xc.0 - xe.0).powi(2) + (xc.1 - xe.1).powi(2)).sqrt());
            pr = pr.max(((xr.0 - xe.0).powi(2) + (xr.1 - xe.1).powi(2)).sqrt());
            let ch = [
                (c.a - exact[i].a, r.a - exact[i].a),
                (c.e - exact[i].e, r.e - exact[i].e),
                (ang(c.w - exact[i].w), ang(r.w - exact[i].w)),
                (ang(c.m0 - exact[i].m0), ang(r.m0 - exact[i].m0)),
            ];
            for k in 0..4 {
                ec[k] = ec[k].max(ch[k].0.abs() / scale[k]);
                er[k] = er[k].max(ch[k].1.abs() / scale[k]);
            }
        }
        let (a, b, c, d, e, f) = (ec[0], er[0], ec[1], er[1], pc, pr);
        println!("{tag}: max err, carry/requant:  a {a:.1}/{b:.1} q  e {c:.1}/{d:.1} q  consumer position {e:.3e}/{f:.3e} m  (ratio {f:.0}x)");
    };
    for k in 0..(waves * KPW as u64) as i64 {
        let t = k as f64 * STEP;
        let th2 = TAU / P2 * (t + STEP * 0.5);
        for i in 0..n {
            // exact
            let (x, v) = readout(&exact[i], t);
            let dv = tide(x, th2);
            exact[i] = kick_elements_xy(&exact[i], t, x, v, dv);
            // carry (reads its own drifted state: feedback, as the engine would)
            let sc = carry[i].read();
            let (xc, vc) = readout(&sc, t);
            let dvc = tide(xc, th2);
            let s1 = kick_elements_xy(&sc, t, xc, vc, dvc);
            let d = [
                (s1.a - sc.a) * Q32,
                (s1.e - sc.e) / 0.4 * Q32,
                (s1.w - sc.w) / TAU * Q32,
                (s1.m0 - sc.m0) / TAU * Q32,
            ];
            for c in 0..4 {
                let (w, nc) = quantize(d[c], carry[i].carry[c]);
                carry[i].carry[c] = nc;
                carry[i].drift[c] += w;
            }
            // requant (the row itself re-rounded)
            let sr = requant[i].read();
            let (xr, vr) = readout(&sr, t);
            let dvr = tide(xr, th2);
            let s1 = kick_elements_xy(&sr, t, xr, vr, dvr);
            let d = [
                (s1.a - sr.a) * Q32,
                (s1.e - sr.e) / 0.4 * Q32,
                (s1.w - sr.w) / TAU * Q32,
                (s1.m0 - sr.m0) / TAU * Q32,
            ];
            for c in 0..4 {
                let (w, nc) = quantize(d[c], requant[i].carry[c]);
                requant[i].carry[c] = nc;
                let b = requant[i].base[c] as i64 + w;
                requant[i].base[c] = if c < 2 {
                    b.clamp(0, 0xFFFF_FFFF) as u32 // magnitude words clamp (angles wrap)
                } else {
                    (b & 0xFFFF_FFFF) as u32 // re-round INTO the word (the memo's walk)
                };
            }
        }
        if (k as u64 + 1) % (KPW as u64) == 0 {
            let wno = (k as u64 + 1) / KPW as u64;
            if wno == 1 || wno == 5 || wno == 10 || wno == 20 {
                check(&format!("wave {wno:>2}"), &exact, &carry, &requant);
            }
        }
    }
}

fn ang(x: f64) -> f64 {
    let mut a = x % TAU;
    if a > PI {
        a -= TAU;
    }
    if a < -PI {
        a += TAU;
    }
    a
}
