//! H_live of a program-stored belt: the bits per body the shipped store (Shelf: blocks + scar
//! layer) must add as the belt drifts under secular precession (Giant's Laplace-Lagrange tide +
//! Schwarzschild), and per encounter scar. Physics in floats (exploration); outcomes integer:
//! bytes of the store, quanta of the ω column (u32 turns).
//!
//! Anchor: the plane's system (scenario.rs): Sun-mass star, belt a ∈ [2, 3.5] AU, Giant
//! (Jupiter) at 5.2 AU with mass 2^-10 of the star. The belt's (E, L) keys are law-native
//! (Key::darwin over the pop.rs domain); only ω drifts, so the key distribution affects only
//! the base cost, which is subtracted.

use emergent_shipmem::shelf::{Kind, Shelf, Ship};
use emergent_space::Key;
use std::f64::consts::TAU;

const N: usize = 65_536;
const BANDS: usize = 256;
const A_LO: f64 = 2.0;
const A_HI: f64 = 3.5;
const A_G: f64 = 5.2;
const MU_G: f64 = 9.765625e-4;
const R_G_SUN_M: f64 = 1477.0;
const AU_M: f64 = 1.496e11;
const SIGMA_E: f64 = 0.05;
const W_QUANT: f64 = TAU / 4_294_967_296.0;
const MID_PERIOD_S: f64 = 4.56 * 3.156e7;
const RTF: f64 = 100.0;

struct R(u64);
impl R {
    fn u64(&mut self) -> u64 {
        self.0 = self.0.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    }
    fn f64(&mut self) -> f64 {
        (self.u64() >> 11) as f64 / 9_007_199_254_740_992.0
    }
}
/// Laplace coefficient b_{3/2}^{(1)}(α) = (1/π)∫₀^{2π} cosψ/(1+α²−2αcosψ)^{3/2} dψ,
/// 2048-point midpoint rule (α < 1: no singularity). At α = 0.385 it is ≈ 1.6.
fn laplace(alpha: f64) -> f64 {
    let m = 2048usize;
    let mut sum = 0.0;
    for k in 0..m {
        let psi = TAU * (k as f64 + 0.5) / m as f64;
        sum += psi.cos() / (1.0 + alpha * alpha - 2.0 * alpha * psi.cos()).powf(1.5);
    }
    2.0 * sum / m as f64
}
/// Apsidal advance per orbit (rad): GR 6πGM/(c²a(1−e²)) + Giant's first-order free precession
/// (π/2)μα b(α), with its e² correction at coefficient c2 (order unity; the swept c2 isolates it).
fn advance(a: f64, e: f64, c2: f64) -> f64 {
    let gr = 6.0 * std::f64::consts::PI * R_G_SUN_M / (a * AU_M * (1.0 - e * e));
    let alpha = a / A_G;
    let ll = 0.5 * std::f64::consts::PI * MU_G * alpha * laplace(alpha) * (1.0 + c2 * e * e);
    gr + ll
}

struct Belt {
    a: Vec<f64>,
    e: Vec<f64>,
    ships: Vec<Ship>,
    /// advance per orbit (rad), precomputed: full (a, e, c2=1); a-only (e=0); band-common.
    adv_full: Vec<f64>,
    adv_a: Vec<f64>,
    adv_band: Vec<f64>,
}

fn make_belt(seed: u64) -> Belt {
    let mut rng = R(seed);
    let mut a = Vec::with_capacity(N);
    let mut e = Vec::with_capacity(N);
    let mut ships = Vec::with_capacity(N);
    let (mut af, mut aa, mut ab) = (Vec::with_capacity(N), Vec::with_capacity(N), Vec::with_capacity(N));
    let mut t: u64 = rng.u64() >> 16;
    for i in 0..N {
        let band = i * BANDS / N;
        let bc = A_LO + (A_HI - A_LO) * (band as f64 + 0.5) / BANDS as f64;
        let half = (A_HI - A_LO) / BANDS as f64;
        let ai = bc + (rng.f64() - 0.5) * half;
        a.push(ai);
        let p_m = 2000.0 + 6000.0 * (band as f64 + rng.f64()) / BANDS as f64;
        let p_raw = (p_m * 65536.0) as u32;
        let u = rng.f64();
        let ei = (SIGMA_E * (-2.0 * (1.0 - u).ln()).sqrt()).min(0.55);
        let e30 = (ei * (1u64 << 30) as f64) as u32;
        let k = Key::darwin(p_raw, e30).or_else(|_| Key::darwin(p_raw, 0)).unwrap();
        let w = rng.u64() as u32;
        t += ((rng.u64() >> 50).max(1)) << 6;
        let kind = rng.u64() >> 62; // 0..3, ~1.6 bits
        let s: Ship = [t & ((1 << 48) - 1), kind, k.energy.get(), k.angular.get(), w as u64, 0, 0, 0];
        ships.push(s);
        e.push(ei);
        let adv_full = advance(ai, ei, 1.0);
        let adv_a = advance(ai, 0.0, 0.0);
        let adv_band = advance(bc, 0.0, 0.0);
        af.push(adv_full); aa.push(adv_a); ab.push(adv_band);
    }
    Belt { a, e, ships, adv_full: af, adv_a: aa, adv_band: ab }
}

fn build(belt: &Belt) -> (Shelf, Vec<u32>) {
    let mut sh = Shelf::new(5, 128, vec![[0, 1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 0, 5, 6, 7]], false);
    let mut members = belt.ships.clone();
    sh.add_group(&mut members, Kind::Slot { grid: 0 });
    let mut handles = Vec::with_capacity(N);
    for bi in 0..sh.blocks.len() {
        for s in 0..sh.blocks[bi].n as usize {
            handles.push(((bi as u32) << 8) | s as u32);
        }
    }
    assert_eq!(handles.len(), N);
    (sh, handles)
}

/// Drifted ω (u32 turns) after T orbits for body i under variant's rate model.
fn drifted(belt: &Belt, i: usize, t_orbits: f64, variant: u8) -> u32 {
    let rate = match variant {
        0 => belt.adv_full[i], // per-body a and e, e² correction on
        1 => belt.adv_band[i], // common per band
        _ => belt.adv_a[i],    // per-body a, no e dependence
    };
    let dquanta = (rate * t_orbits / W_QUANT).round() as i64;
    let w0 = belt.ships[i][4] as u64;
    ((w0 as i64 + dquanta).rem_euclid(1 << 32)) as u64 as u32
}

fn main() {
    let belt = make_belt(0x5EED_0001);
    let (mut sh, _handles) = build(&belt);
    let base = sh.bytes();
    println!("{{\"exp\":\"base\",\"n\":{N},\"bytes\":{base},\"bits_per_body\":{:.3}}}", base as f64 * 8.0 / N as f64);

    // orbits per wall-hour at rtf 100 (mid-belt)
    let orph = 3600.0 * RTF / MID_PERIOD_S;
    let horizons = [2.5e-3_f64, 2.5e-2, 0.25, 2.5, 25.0, 250.0];

    // control: compact with no events must not change bytes
    let st = sh.compact();
    println!("{{\"exp\":\"control\",\"bytes\":{},\"delta_bits\":0,\"repacks\":{}}}", sh.bytes(), st.repacks);
    assert_eq!(sh.bytes(), base, "control: compact alone must not grow the store");

    for variant in 0..3u8 {
        let (mut sh, handles) = build(&belt);
        sh.compact();
        for &t in &horizons {
            for i in 0..N {
                let mut s = belt.ships[i];
                s[4] = drifted(&belt, i, t, variant) as u64;
                sh.update(handles[i], s);
            }
            let st = sh.compact();
            let bytes = sh.bytes();
            // drift statistics in quanta (precomputed rates)
            let mut mn = f64::INFINITY;
            let mut mx = f64::NEG_INFINITY;
            let (mut bmn, mut bmx) = (f64::INFINITY, f64::NEG_INFINITY);
            for i in 0..N {
                let d = belt.adv_full[i] * t / W_QUANT;
                let dc = belt.adv_band[i] * t / W_QUANT;
                mn = mn.min(d);
                mx = mx.max(d);
                if i / (N / BANDS) == BANDS / 2 {
                    bmn = bmn.min(d - dc);
                    bmx = bmx.max(d - dc);
                }
            }
            println!(
                "{{\"exp\":\"secular\",\"variant\":{},\"t_orbits\":{:.4},\"wall_hours\":{:.2},\"bytes\":{},\"bits_per_body\":{:.4},\"max_drift_quanta\":{:.3e},\"spread_quanta\":{:.3e},\"midband_differential_quanta\":{:.3e},\"repacks\":{}}}",
                variant, t, t / orph, bytes,
                (bytes as f64 - base as f64) * 8.0 / N as f64,
                mx, mx - mn, bmx - bmn, st.repacks
            );
        }
    }

    // encounter scars: random kick deltas (pop.rs's kick model) on a fraction f
    for f in [1e-3f64, 1e-2] {
        let (mut sh, handles) = build(&belt);
        sh.compact();
        let mut rng = R(0xD1CE_BEEF);
        let k = (f * N as f64) as usize;
        for j in 0..k {
            let i = (j * N / k.max(1)).min(N - 1);
            let mut s = belt.ships[i];
            let d = |r: &mut R, b: u32| (r.u64() % (2u64 << b)).wrapping_sub(1 << b) as i64;
            s[0] = s[0].wrapping_add(d(&mut rng, 16) as u64) & ((1 << 48) - 1);
            s[2] = s[2].wrapping_add(d(&mut rng, 10) as u64);
            s[3] = s[3].wrapping_add(d(&mut rng, 10) as u64);
            s[4] = s[4].wrapping_add(d(&mut rng, 10) as u64) & 0xFFFF_FFFF;
            sh.update(handles[i], s);
        }
        let st = sh.compact();
        let bytes = sh.bytes();
        println!(
            "{{\"exp\":\"encounter\",\"fraction\":{},\"scarred\":{},\"bytes\":{},\"bits_per_body\":{:.4},\"bits_per_scar\":{:.2},\"repacks\":{}}}",
            f, k, bytes,
            (bytes as f64 - base as f64) * 8.0 / N as f64,
            (bytes as f64 - base as f64) * 8.0 / k as f64, st.repacks
        );
    }

    // the derive-side alternative: rate cells needed so that within-cell drift differences stay
    // below one ω quantum over T (a-dimension already discretised by BANDS bands)
    println!("{{\"exp\":\"rates\",\"note\":\"advance(2.0,0)={:.3e} advance(3.5,0)={:.3e} advance(mid,5sigma_e)={:.3e} rad/orbit\"}}",
        advance(2.0, 0.0, 0.0), advance(3.5, 0.0, 0.0), advance(2.75, 5.0 * SIGMA_E, 1.0));
    for &t in &horizons {
        let gran = W_QUANT / t; // distinguishable rate granularity, rad/orbit
        let a_cells = (advance(2.0, 0.0, 0.0) - advance(3.5, 0.0, 0.0)) / gran;
        let e_cells = (advance(2.75, 5.0 * SIGMA_E, 1.0) - advance(2.75, 0.0, 1.0)) / gran;
        let cells = a_cells * e_cells.max(1.0);
        let bits = cells * (cells.max(2.0)).log2();
        println!(
            "{{\"exp\":\"ratetable\",\"t_orbits\":{:.4},\"wall_hours\":{:.2},\"granularity_rad_per_orbit\":{:.3e},\"cells\":{:.3e},\"table_bits\":{:.3e}}}",
            t, t / orph, gran, cells, bits
        );
    }
}
