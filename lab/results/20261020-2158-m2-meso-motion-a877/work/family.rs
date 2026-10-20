//! The family certificate (lab run 20261020-2158-m2-meso-motion-a877).
//!
//! Question: do the members of a same-(E,L) family (one orbit, phase offsets — a ring fleet
//! at any spread, a formation at tiny spread) fire IDENTICAL integer kicks, so the whole
//! family rides one binding and one event per epoch? The kick path is `step.rs::kick`:
//! `a = force::acceleration(0, x, secs, tide)` at the body's own position, `dv = a·h`, then
//! the sigma-delta `quantize` against the velocity word. Members separated by δx along the
//! arc see accelerations differing by δa ≈ H·δx (H the kick sources' tidal tensor; the
//! origin's fall is x-independent and cancels). Their streams stay bit-identical iff the
//! accumulated differential, the carry difference D(t) = ∫δ(a_kick)dt, never crosses one
//! quantum of the shared word — then fired `dvq` never differs, (E,L) move together, and
//! the memo key is shared forever.
//!
//! Instruments, on the plane's own scene numbers (the star μ=1; Giant: μ = 2⁻¹⁰ on a circle
//! at a = 5.263e8 root, the root doll; and Home: a family in Home's doll, whose kick source
//! is the shipped `parent_tide` — the star's full differential pull):
//!  1. `census`: δa(δx) against the analytic μ/d³ tensor.
//!  2. `growth`: the carry difference D(t) over 30 synodic periods (bounded? secular? chaos?),
//!     at belt radii and the interior p:q resonances.
//!  3. `split`: the exact shipped `quantize` rule on both members' dv at the kick cadence, at
//!     the shipped 61-significant-bit word and at a family word of 11 fraction bits (the memo
//!     code's own width): differing firings and the first differing tick.
//!
//! cargo run --release -p emergent-universe --example family
use emergent_space::events::kicks::parent_tide;
use emergent_space::orbit::Scalar;
use emergent_universe::force::{acceleration, Secondary};
use emergent_universe::num::{from_f64, to_f64};
use std::f64::consts::TAU;

/// The star's GM in root units (one root unit = GM_sun/c² = 1.477 km).
const MU_STAR: f64 = 1.0;
/// Giant: the plane's third planet, mass 2⁻¹⁰ of the star.
const MU_P: f64 = 0.0009765625;
/// Its circle (the plane's Giant: periapsis 5e8, e = 1/20, so a = 5e8/(1−e) = 5.263e8).
const SEP: f64 = 526_315_789.4736842;
/// Giant's sphere of influence, the changeover's scale: sep·(μ/3)^(1/3).
const EDGE: f64 = 36_231_572.0;
/// Home's mass (2⁻¹⁸ of the star), for the child-doll family.
const MU_HOME: f64 = 3.814697265625e-6;

/// One astronomical unit in root units (scenario::AU).
const AU: f64 = 101_300_000.0;

/// A body on a circle of radius `rad` (phase 0 at t = 0): its state at time t.
fn circle(rad: f64, mu: f64, t: f64) -> ([f64; 2], [f64; 2]) {
    let n = (mu / rad.powi(3)).sqrt();
    let (s, c) = (n * t).sin_cos();
    ([rad * c, rad * s], [-rad * n * s, rad * n * c])
}

/// The shipped kick acceleration in the ROOT doll at `x`: Giant's pull minus the origin's
/// fall (the star's pull is the drift, not a kick; the root doll has no parent tide).
fn accel_root(t: f64, x: [f64; 2]) -> [f64; 2] {
    let (pos, vel) = circle(SEP, MU_STAR, t);
    let sec = Secondary { gm: from_f64(MU_P), pos: [from_f64(pos[0]), from_f64(pos[1])], vel: [from_f64(vel[0]), from_f64(vel[1])], edge: from_f64(EDGE) };
    match acceleration(0, [from_f64(x[0]), from_f64(x[1])], &[sec], None) {
        Ok(a) => [to_f64(a[0]), to_f64(a[1])],
        Err(e) => panic!("acceleration refused: {e:?} at t={t} x={x:?}"),
    }
}

/// The shipped kick acceleration in HOME's doll at offset `o` from Home (the star's full
/// differential pull, `parent_tide`; Home's own pull is the drift).
fn accel_home(t: f64, o: [f64; 2]) -> [f64; 2] {
    let (c, _) = circle(AU, MU_STAR, t);
    let cs = [from_f64(c[0]), from_f64(c[1])];
    match parent_tide(from_f64(MU_STAR), cs, [from_f64(o[0]), from_f64(o[1])]) {
        Ok(a) => [to_f64(a[0]), to_f64(a[1])],
        Err(e) => panic!("parent_tide refused: {e:?} at t={t} o={o:?}"),
    }
}

/// The full field (drift + kicks) in the root doll.
fn total_root(t: f64, x: [f64; 2]) -> [f64; 2] {
    let r = (x[0] * x[0] + x[1] * x[1]).sqrt();
    let g = -MU_STAR / (r * r * r);
    let a = accel_root(t, x);
    [a[0] + g * x[0], a[1] + g * x[1]]
}

/// The full field in Home's doll: the drift about Home plus the star's tide.
fn total_home(t: f64, o: [f64; 2]) -> [f64; 2] {
    let r = (o[0] * o[0] + o[1] * o[1]).sqrt();
    let g = -MU_HOME / (r * r * r);
    let a = accel_home(t, o);
    [a[0] + g * o[0], a[1] + g * o[1]]
}

type Field = fn(f64, [f64; 2]) -> [f64; 2];

/// One RK4 step of the full field.
fn step(t: f64, x: [f64; 2], v: [f64; 2], h: f64, f: Field) -> ([f64; 2], [f64; 2]) {
    let (x1, v1) = (x, v);
    let a1 = f(t, x1);
    let (x2, v2) = ([x[0] + v1[0] * h / 2.0, x[1] + v1[1] * h / 2.0], [v[0] + a1[0] * h / 2.0, v[1] + a1[1] * h / 2.0]);
    let a2 = f(t + h / 2.0, x2);
    let (x3, v3) = ([x[0] + v2[0] * h / 2.0, x[1] + v2[1] * h / 2.0], [v[0] + a2[0] * h / 2.0, v[1] + a2[1] * h / 2.0]);
    let a3 = f(t + h / 2.0, x3);
    let (x4, v4) = ([x[0] + v3[0] * h, x[1] + v3[1] * h], [v[0] + a3[0] * h, v[1] + a3[1] * h]);
    let a4 = f(t + h, x4);
    (
        [
            x[0] + h / 6.0 * (v1[0] + 2.0 * v2[0] + 2.0 * v3[0] + v4[0]),
            x[1] + h / 6.0 * (v1[1] + 2.0 * v2[1] + 2.0 * v3[1] + v4[1]),
        ],
        [
            v[0] + h / 6.0 * (a1[0] + 2.0 * a2[0] + 2.0 * a3[0] + a4[0]),
            v[1] + h / 6.0 * (a1[1] + 2.0 * a2[1] + 2.0 * a3[1] + a4[1]),
        ],
    )
}

/// The kick field only (for the split instrument's quantize inputs).
fn kick_root(t: f64, x: [f64; 2]) -> [f64; 2] {
    accel_root(t, x)
}
fn kick_home(t: f64, o: [f64; 2]) -> [f64; 2] {
    accel_home(t, o)
}

/// The sigma-delta of `step.rs::quantize`, verbatim: `dv` in velocity units, the carry in
/// 2⁻¹⁶ of the quantum 2^`exp`.
fn quantize(dv: [Scalar; 2], exp: i16, carry: [i64; 2]) -> ([i64; 2], [i64; 2]) {
    let mut out = [0i64; 2];
    let mut rem = carry;
    for c in 0..2 {
        let inc = dv[c].fixed(16 - exp as i32).expect("dv fixed");
        let total = carry[c] as i128 + inc;
        out[c] = (total / 65536) as i64;
        rem[c] = (total % 65536) as i64;
    }
    (out, rem)
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mode = args.get(1).map(|s| s.as_str()).unwrap_or("all");
    if mode == "all" || mode == "census" {
        census();
    }
    if mode == "all" || mode == "growth" {
        growth();
    }
    if mode == "all" || mode == "split" {
        split();
    }
}

/// δa across members: measured against the analytic tide tensor.
fn census() {
    println!("census: scene star(μ=1) + Giant(μ=2^-10, circle a={SEP:.3e} root, SOI {EDGE:.3e}); Home doll: family about Home, kick = parent_tide(star)");
    for &(name, r_au) in &[("1AU", 1.0), ("belt2.5", 2.5)] {
        let r = r_au * AU;
        let t = 0.0;
        let (pos, _) = circle(SEP, MU_STAR, t);
        let d = ((pos[0] - r) * (pos[0] - r) + pos[1] * pos[1]).sqrt();
        let x = [r, 0.0];
        let a0 = accel_root(t, x);
        println!(
            "census: {name} r={r:.3e} planet-distance {d:.3e} kick|a| {:.3e} (μ_P/d² = {:.3e}), analytic H_G = μ_P/d³ = {:.3e} root⁻²",
            (a0[0] * a0[0] + a0[1] * a0[1]).sqrt(),
            MU_P / (d * d),
            MU_P / d.powi(3)
        );
        for &dx in &[1.0f64, 1e3, 1e6, 1e8] {
            let ar = accel_root(t, [x[0] + dx, x[1]]);
            let at = accel_root(t, [x[0], x[1] + dx]);
            let dr = ((ar[0] - a0[0]).powi(2) + (ar[1] - a0[1]).powi(2)).sqrt();
            let dt = ((at[0] - a0[0]).powi(2) + (at[1] - a0[1]).powi(2)).sqrt();
            println!("census: {name} δx={dx:.0e} root: |δa| radial {dr:.3e} ({:+.2}×μ/d³), transverse {dt:.3e}", dr / (MU_P / d.powi(3)));
        }
    }
    // Home's doll: the tide of the star across a family about Home at rho.
    for &rho in &[1e5f64, 1e6, 5e6] {
        let t = 0.0;
        let o = [rho, 0.0];
        let a0 = accel_home(t, o);
        for &dx in &[1e3f64, 1e5] {
            let ar = accel_home(t, [o[0] + dx, o[1]]);
            let at = accel_home(t, [o[0], o[1] + dx]);
            let dr = ((ar[0] - a0[0]).powi(2) + (ar[1] - a0[1]).powi(2)).sqrt();
            let dt = ((at[0] - a0[0]).powi(2) + (at[1] - a0[1]).powi(2)).sqrt();
            println!(
                "census: home rho={rho:.0e} δx={dx:.0e} root: |δa| radial {dr:.3e} ({:+.1}×M/r³ = {:.3e}), transverse {dt:.3e}",
                dr / (1.0 / AU.powi(3)),
                1.0 / AU.powi(3)
            );
        }
    }
}

/// The growth instrument: the carry difference D(t) = ∫δ(a_kick)dt over 30 synodic periods,
/// for a family of one orbit at a phase offset (δx0 = 1 root along the arc).
fn growth() {
    // radii: 1 AU, mid-belt, and the interior p:q resonances with the planet (a ∝ (q/p)^(2/3)).
    let pg = (SEP * SEP * SEP / MU_STAR).sqrt() * TAU;
    let mut rows: Vec<(String, f64)> = vec![
        ("1AU".into(), AU),
        ("2.06AU".into(), 2.06 * AU),
        ("belt2.5".into(), 2.5 * AU),
        ("2.82AU".into(), 2.82 * AU),
    ];
    for &(p, q) in &[(2u32, 1u32), (5, 2), (7, 3), (3, 1)] {
        let a_res = SEP * (q as f64 / p as f64).powf(2.0 / 3.0);
        rows.push((format!("res{p}:{q}"), a_res));
    }
    let n_syn = 30.0;
    for (name, r) in rows {
        let pf = (r * r * r / MU_STAR).sqrt() * TAU;
        let syn = (1.0f64 / pf - 1.0 / pg).abs().recip();
        let horizon = syn * n_syn;
        let h = pf / 720.0;
        let v = (MU_STAR / r).sqrt();
        // The family member: the SAME orbit at a phase offset dphi (δx = r·dphi along the arc).
        // A position offset at equal velocity would be a different orbit (Kepler shear), not a family.
        let dphi = 1.0 / r;
        let (s, c) = dphi.sin_cos();
        let (mut xr, mut vr) = ([r, 0.0], [0.0, v]);
        let (mut xm, mut vm) = ([r * c, r * s], [-v * s, v * c]);
        let mut t = 0.0;
        let mut per_syn_d: Vec<f64> = Vec::new();
        let mut cur_max_d = 0.0f64;
        let mut max_d_total = 0.0f64;
        let mut max_dx = 0.0f64;
        let (mut d0, mut d1) = (0.0f64, 0.0f64);
        let steps = (horizon / h) as usize;
        for k in 0..steps {
            let ar = accel_root(t, xr);
            let am = accel_root(t, xm);
            d0 += (am[0] - ar[0]) * h;
            d1 += (am[1] - ar[1]) * h;
            let d = (d0 * d0 + d1 * d1).sqrt();
            cur_max_d = cur_max_d.max(d);
            max_d_total = max_d_total.max(d);
            let (nxr, nvr) = step(t, xr, vr, h, total_root);
            let (nxm, nvm) = step(t, xm, vm, h, total_root);
            xr = nxr;
            vr = nvr;
            xm = nxm;
            vm = nvm;
            t += h;
            let dx = ((xm[0] - xr[0]).powi(2) + (xm[1] - xr[1]).powi(2)).sqrt();
            max_dx = max_dx.max(dx);
            if (k + 1) as f64 * h >= (per_syn_d.len() as f64 + 1.0) * syn {
                per_syn_d.push(cur_max_d);
                cur_max_d = 0.0;
            }
        }
        let n = per_syn_d.len();
        let first = per_syn_d[..n.min(3)].iter().cloned().fold(0.0f64, f64::max);
        let last = per_syn_d[n - 3..].iter().cloned().fold(0.0f64, f64::max);
        let mid = per_syn_d[n / 2];
        let ratio = if mid > 0.0 { last / mid } else { f64::INFINITY };
        println!(
            "growth: {name} a={r:.4e} P_f={pf:.3e} syn={syn:.3e} ({n_syn:.0} syn = {} orbits) | δx0=1 root along-arc: carry-diff max|D| first3syn {first:.3e}, mid {mid:.3e}, last3syn {last:.3e}, last/mid {ratio:+.2}×, overall max {max_d_total:.3e} c; max|δx| {max_dx:.3e} root (Kepler repetition check)",
            (horizon / pf) as i64
        );
    }
    // Home's doll: the family about Home, the star's tide the kick.
    for &rho in &[1e5f64, 1e6, 5e6] {
        let pf = (rho * rho * rho / MU_HOME).sqrt() * TAU;
        let syn = (AU * AU * AU / MU_STAR).sqrt() * TAU; // Home's year
        let horizon = syn * 8.0;
        let h = pf / 720.0;
        let v = (MU_HOME / rho).sqrt();
        let dphi = 1.0 / rho;
        let (s, c) = dphi.sin_cos();
        let (mut xr, mut vr) = ([rho, 0.0], [0.0, v]);
        let (mut xm, mut vm) = ([rho * c, rho * s], [-v * s, v * c]);
        let mut t = 0.0;
        let (mut max_d, mut max_dx) = (0.0f64, 0.0f64);
        let (mut d0, mut d1) = (0.0f64, 0.0f64);
        let steps = (horizon / h) as usize;
        for k in 0..steps {
            let ar = accel_home(t, xr);
            let am = accel_home(t, xm);
            d0 += (am[0] - ar[0]) * h;
            d1 += (am[1] - ar[1]) * h;
            max_d = max_d.max((d0 * d0 + d1 * d1).sqrt());
            let (nxr, nvr) = step(t, xr, vr, h, total_home);
            let (nxm, nvm) = step(t, xm, vm, h, total_home);
            xr = nxr;
            vr = nvr;
            xm = nxm;
            vm = nvm;
            t += h;
            let dx = ((xm[0] - xr[0]).powi(2) + (xm[1] - xr[1]).powi(2)).sqrt();
            max_dx = max_dx.max(dx);
            if k % 10_000_000 == 0 && k > 0 {
                break; // guard: keep the run bounded
            }
        }
        println!(
            "growth: home rho={rho:.0e} root P_f={pf:.3e} ({} orbits over {:.1} Home years) | δx0=1 root: carry-diff max|D| {max_d:.3e} c; max|δx| {max_dx:.3e} root",
            (horizon / pf) as i64,
            horizon / syn
        );
    }
}

/// The split instrument: the exact quantize rule on both members' dv at the kick cadence.
fn split() {
    let pg = (SEP * SEP * SEP / MU_STAR).sqrt() * TAU;
    // ---- the root doll --------------------------------------------------------------------
    for &(name, r_au) in &[("1AU", 1.0f64), ("belt2.5", 2.5)] {
        let r = r_au * AU;
        let pf = (r * r * r / MU_STAR).sqrt() * TAU;
        let syn = 1.0f64 / (1.0 / pf - 1.0 / pg);
        let v = (MU_STAR / r).sqrt();
        let ve61 = v.log2().floor() as i16 - 60; // the shipped word: 61 significant bits
        let ve11 = v.log2().floor() as i16 - 10; // a family word: 11 fraction bits
        println!(
            "split: {name} v={v:.4e} c; quantum61 = 2^{} = {:.3e} c; quantum11 = 2^{} = {:.3e} c",
            ve61,
            2f64.powi(ve61 as i32),
            ve11,
            2f64.powi(ve11 as i32)
        );
        for &(step_log2, dx, ring) in &[
            (7u32, 1.0f64, false),
            (7, 1e3, false),
            (7, 1e6, false),
            (7, 0.0, true), // the phase-spread control: +1/8 of the orbit along-track
            (4, 1e3, false),
            (4, 1e6, false),
            (4, 0.0, true),
        ] {
            let kicks_per_period = 1u64 << step_log2;
            let h = pf / kicks_per_period as f64;
            let horizon = syn * 30.0;
            let n_kicks = ((horizon / h) as usize).min(400_000);
            let dphi = if ring { TAU / 8.0 } else { dx / r };
            let (s, c) = dphi.sin_cos();
            let (mut xr, mut vr) = ([r, 0.0], [0.0, v]);
            let (mut xm, mut vm) = ([r * c, r * s], [-v * s, v * c]);
            split_row(name, "root", ring, if ring { r * dphi } else { dx }, step_log2, kicks_per_period, n_kicks, h, syn, &mut xr, &mut vr, &mut xm, &mut vm, &mut t_state(), kick_root, total_root, ve61, ve11);
        }
    }
    // ---- Home's doll -----------------------------------------------------------------------
    for &rho in &[1e5f64, 1e6] {
        let pf = (rho * rho * rho / MU_HOME).sqrt() * TAU;
        let syn = (AU * AU * AU / MU_STAR).sqrt() * TAU;
        let v = (MU_HOME / rho).sqrt();
        let ve61 = v.log2().floor() as i16 - 60;
        let ve11 = v.log2().floor() as i16 - 10;
        println!(
            "split: home rho={rho:.0e} v={v:.4e} c; quantum61 = 2^{} = {:.3e}; quantum11 = 2^{} = {:.3e}",
            ve61,
            2f64.powi(ve61 as i32),
            ve11,
            2f64.powi(ve11 as i32)
        );
        for &(step_log2, dx, ring) in &[(7u32, 1e3f64, false), (7, 1e5, false), (7, 0.0, true)] {
            let kicks_per_period = 1u64 << step_log2;
            let h = pf / kicks_per_period as f64;
            let horizon = syn * 8.0;
            let n_kicks = ((horizon / h) as usize).min(400_000);
            let dphi = if ring { TAU / 8.0 } else { dx / rho };
            let (s, c) = dphi.sin_cos();
            let (mut xr, mut vr) = ([rho, 0.0], [0.0, v]);
            let (mut xm, mut vm) = ([rho * c, rho * s], [-v * s, v * c]);
            split_row("home", &format!("rho{rho:.0e}"), ring, if ring { rho * dphi } else { dx }, step_log2, kicks_per_period, n_kicks, h, syn, &mut xr, &mut vr, &mut xm, &mut vm, &mut t_state(), kick_home, total_home, ve61, ve11);
        }
    }
}

/// A mutable holder for the split loop's time (the loop advances t inside).
fn t_state() -> f64 {
    0.0
}

#[allow(clippy::too_many_arguments)]
fn split_row(
    name: &str,
    doll: &str,
    ring: bool,
    dx: f64,
    step_log2: u32,
    kicks_per_period: u64,
    n_kicks: usize,
    h: f64,
    syn: f64,
    xr: &mut [f64; 2],
    vr: &mut [f64; 2],
    xm: &mut [f64; 2],
    vm: &mut [f64; 2],
    t: &mut f64,
    kick: Field,
    total: Field,
    ve61: i16,
    ve11: i16,
) {
    let mut c61 = [[0i64; 2]; 2];
    let mut c11 = [[0i64; 2]; 2];
    let (mut diff61, mut diff11) = (0u64, 0u64);
    let (mut first61, mut first11) = (i64::MAX, i64::MAX);
    let mut sum_q11 = 0u64;
    for k in 0..n_kicks {
        let ar = kick(*t, *xr);
        let am = kick(*t, *xm);
        let dvr = [from_f64(ar[0] * h), from_f64(ar[1] * h)];
        let dvm = [from_f64(am[0] * h), from_f64(am[1] * h)];
        let (qr, nr) = quantize(dvr, ve61, c61[0]);
        let (qm, nm) = quantize(dvm, ve61, c61[1]);
        c61[0] = nr;
        c61[1] = nm;
        if qr != qm {
            diff61 += 1;
            if first61 == i64::MAX {
                first61 = k as i64;
            }
        }
        let (qr1, nr1) = quantize(dvr, ve11, c11[0]);
        let (qm1, nm1) = quantize(dvm, ve11, c11[1]);
        c11[0] = nr1;
        c11[1] = nm1;
        if qr1 != qm1 {
            diff11 += 1;
            if first11 == i64::MAX {
                first11 = k as i64;
            }
        }
        sum_q11 += (qr1[0].unsigned_abs() + qr1[1].unsigned_abs()) as u64;
        let sub = 8;
        for _ in 0..sub {
            let (nxr, nvr) = step(*t, *xr, *vr, h / sub as f64, total);
            let (nxm, nvm) = step(*t, *xm, *vm, h / sub as f64, total);
            *xr = nxr;
            *vr = nvr;
            *xm = nxm;
            *vm = nvm;
            *t += h / sub as f64;
        }
    }
    let kind = if ring { "ring 1/8 orbit" } else { "phase-offset family" };
    println!(
        "split: {name}/{doll} {kind} δx={dx:.3e} step_log2={step_log2} ({kicks_per_period}/orbit) nkicks={n_kicks} ({:.1} syn): differing firings w61 {diff61} (first kick {first61}), w11 {diff11} (first {first11}); mean |dvq|/kick w11 {:.4} quanta",
        n_kicks as f64 * h / syn,
        sum_q11 as f64 / n_kicks as f64
    );
}
