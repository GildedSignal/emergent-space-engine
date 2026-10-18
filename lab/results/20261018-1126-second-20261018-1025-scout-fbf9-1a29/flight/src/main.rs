//! The checker-named gold experiment for 20261018-1025-scout-fbf9: fly the due-band
//! per-kick rule on the SHIPPED tier (`Sorted` U-scan → `is_candidate` →
//! `tier::arm_pair`, exactly the path `main.rs::kick` drives) at 10⁹-density cells of
//! 10³–10⁵ occupancy, and measure re-arms/kick. Θ(n) re-arms would kill the toy's
//! window model; the standing/dwell class is audited separately.
//!
//! Scene = the toy's constants: ρ = 1e9/(π(3²−2²)) AU⁻², a = 2.5 AU cells of width
//! W = n/(ρ·2πa), e Rayleigh 0.07 (cap 0.4), reach B = 5×10⁵ m = 3.3423×10⁻⁹ AU
//! (cd3b), interval = P(2.5 AU)/4.43, horizon H = 8 intervals, band = (H+2)
//! intervals, kick = dv/v·|v| at a random anomaly in a random direction (the toy's
//! kick_at, ported; pre/post at the same anomaly). One JSON line per measurement.
//!
//! Due definitions on the same bodies: SHIPPED (arm_pair's first in-window passage,
//! which carries the crate's `ext` arc-traversal slack) and CONJ (analytic first
//! mean-longitude meeting, the toy's constant). The rule is scored twice: re-check
//! iff due < band, and re-check iff armed OR due < band (the ext slack can push an
//! armed pair's min-section due past the band). Every silent→armed violation is
//! additionally run through the exact `pair_events` machinery post-kick.

use emergent_encounters::belt::Rng;
use emergent_encounters::kepler::Body;
use emergent_encounters::method::{pair_events, Stats};
use emergent_encounters::pairs::{is_candidate, Sorted};
use emergent_encounters::tier::{arm_pair, ArmStats};
use std::f64::consts::TAU;
use std::time::Instant;

const GM: f64 = TAU * TAU; // doll units: n = 1 at a = 1
const RHO_AU: f64 = 1e9 / (std::f64::consts::PI * (3.0 * 3.0 - 2.0 * 2.0)); // bodies/AU²
const A_C: f64 = 2.5;
const B: f64 = 5e5 / 1.495978707e11; // cd3b reach, doll units
const SAFETY: f64 = 1.1;
const INTERVAL: f64 = TAU * 3.9528470752103145 / 4.43;
const H: f64 = 8.0 * INTERVAL;
const BAND: f64 = 10.0 * INTERVAL; // (H + 2) intervals

#[derive(Clone, Copy)]
struct El {
    a: f64,
    e: f64,
    pom: f64,
    lam: f64,
}

fn wrap(x: f64) -> f64 {
    (x + std::f64::consts::PI).rem_euclid(TAU) - std::f64::consts::PI
}

/// The toy's make_cell: uniform a over the cell width, Rayleigh e (capped), uniform angles.
fn make_cell(n: usize, seed: u64, sigma_e: f64) -> (Vec<El>, Vec<Body>) {
    let width = n as f64 / (RHO_AU * TAU * A_C);
    let mut r = Rng(seed);
    let mut els = Vec::with_capacity(n);
    for _ in 0..n {
        let u = r.f64();
        let e = (sigma_e * (-2.0 * (1.0 - u).ln()).sqrt()).min(0.4);
        els.push(El {
            a: A_C + (r.f64() - 0.5) * width,
            e,
            pom: TAU * r.f64(),
            lam: wrap(TAU * r.f64()),
        });
    }
    let bodies: Vec<Body> = els.iter().map(|q| Body::new(q.a, q.e, q.pom, q.lam)).collect();
    (els, bodies)
}

fn body_of(q: &El) -> Body {
    Body::new(q.a, q.e, q.pom, q.lam)
}

/// The toy's kick_at: elements of the kicked body at a random anomaly f, dv applied
/// in a random direction, pre/post returned at that same anomaly. Doll units.
fn kick_at(q: &El, dv_rel: f64, r: &mut Rng) -> (El, El) {
    let f = TAU * r.f64();
    let (a, e, w) = (q.a, q.e, q.pom);
    let p = a * (1.0 - e * e);
    let rr = p / (1.0 + e * f.cos());
    let th = w + f;
    let h = (GM * p).sqrt();
    let vr = GM / h * e * f.sin();
    let vt = GM / h * (1.0 + e * f.cos());
    let (ct, st) = (th.cos(), th.sin());
    let pos = [rr * ct, rr * st];
    let vel = [vr * ct - vt * st, vr * st + vt * ct];
    let dv = dv_rel * (vel[0] * vel[0] + vel[1] * vel[1]).sqrt();
    let ang = TAU * r.f64();
    let vel = [vel[0] + dv * ang.cos(), vel[1] + dv * ang.sin()];
    let pre = El {
        a,
        e,
        pom: w,
        lam: wrap(w + anomaly_to_mean(e, f)),
    };
    let rn = (pos[0] * pos[0] + pos[1] * pos[1]).sqrt();
    let v2 = vel[0] * vel[0] + vel[1] * vel[1];
    let a2 = 1.0 / (2.0 / rn - v2 / GM);
    let rv = pos[0] * vel[0] + pos[1] * vel[1];
    let ev = [
        ((v2 - GM / rn) * pos[0] - rv * vel[0]) / GM,
        ((v2 - GM / rn) * pos[1] - rv * vel[1]) / GM,
    ];
    let e2 = (ev[0] * ev[0] + ev[1] * ev[1]).sqrt();
    let w2 = ev[1].atan2(ev[0]);
    let f2 = th - w2;
    let post = El {
        a: a2,
        e: e2,
        pom: w2,
        lam: wrap(w2 + anomaly_to_mean(e2, f2)),
    };
    (pre, post)
}

fn anomaly_to_mean(e: f64, f: f64) -> f64 {
    let e2 = 2.0 * ((1.0 - e).sqrt() * (f / 2.0).sin()).atan2((1.0 + e).sqrt() * (f / 2.0).cos());
    e2 - e * e2.sin()
}

/// Analytic first mean-longitude meeting at/after 0 (the toy's due), or None if Δn = 0.
fn conj_due(ni: f64, nj: f64, dlam: f64) -> Option<f64> {
    let dn = ni - nj;
    if dn == 0.0 {
        return None;
    }
    let x = (-dlam).rem_euclid(TAU);
    Some(if dn > 0.0 { x / dn } else if x > 0.0 { (TAU - x) / (-dn) } else { 0.0 })
}

struct CellOut {
    n: usize,
    seed: u64,
    sigma_e: f64,
    dv: f64,
    kicks: usize,
    reach: f64,
    scanned_per_kick: f64,
    evals_per_kick: f64,
    armed_pre_per_kick: f64,
    band_ship_per_kick: f64,
    band_or_armed_per_kick: f64,
    band_conj_per_kick: f64,
    flips_on: u64,
    flips_off: u64,
    tier1_flips: u64,
    viol_on: u64,
    viol_off: u64,
    viol2_on: u64,
    viol2_off: u64,
    viol_on_post_events: u64,
    viol_on_pre_events: u64,
    standing_pairs: u64,
    standing_armed: u64,
    standing_flips: u64,
    viol_due_med_intervals: f64,
    viol_dn_med: f64,
    due_move_inband_median: f64,
    due_move_all_median: f64,
    us_per_eval: f64,
    hits_truth: u64,
    hits_covered: u64,
}

#[allow(clippy::too_many_arguments)]
fn run_cell(
    n: usize,
    seed: u64,
    sigma_e: f64,
    dv: f64,
    kicks: usize,
    reach: f64,
    truth_check: bool,
) -> CellOut {
    let (els, bodies) = make_cell(n, seed, sigma_e);
    let sorted = Sorted::new(&bodies, reach);
    let mut kr = Rng(seed ^ (n as u64) ^ (dv.to_bits()));
    let targets: Vec<usize> = (0..kicks).map(|q| (q * 97 + 13) % n).collect();
    let mut scanned = 0u64;
    let mut evals = 0u64;
    let mut armed_pre = 0u64;
    let mut band_ship = 0u64;
    let mut band_or_armed = 0u64;
    let mut band_conj = 0u64;
    let mut flips_on = 0u64;
    let mut flips_off = 0u64;
    let mut tier1 = 0u64;
    let (mut viol_on, mut viol_off, mut viol2_on, mut viol2_off) = (0u64, 0u64, 0u64, 0u64);
    let mut viol_on_post = 0u64;
    let mut viol_on_pre = 0u64;
    let (mut stand, mut stand_armed, mut stand_flip) = (0u64, 0u64, 0u64);
    let mut viol_dues: Vec<f64> = Vec::new();
    let mut viol_dns: Vec<f64> = Vec::new();
    let mut move_inband = Vec::new();
    let mut move_all = Vec::new();
    let mut secs = 0.0f64;
    let mut hits_truth = 0u64;
    let mut hits_covered = 0u64;
    let mut ast = ArmStats::default();
    for &i in &targets {
        let (pre_el, post_el) = kick_at(&els[i], dv, &mut kr);
        let pre = body_of(&pre_el);
        let post = body_of(&post_el);
        let (lo0, hi0) = sorted.range(pre.binet()[0], sorted.reach(&pre));
        let (lo1, hi1) = sorted.range(post.binet()[0], sorted.reach(&post));
        let (lo, hi) = (lo0.min(lo1), hi0.max(hi1));
        scanned += (hi - lo).saturating_sub(1) as u64;
        let t0 = Instant::now();
        for &(_, j) in &sorted.order[lo..hi] {
            let j = j as usize;
            if j == i {
                continue;
            }
            let bj = &bodies[j];
            let cand0 = is_candidate(&pre, bj, reach);
            let cand1 = is_candidate(&post, bj, reach);
            if cand0 {
                evals += 1;
            }
            if cand1 {
                evals += 1;
            }
            let (on0, d0) = if cand0 {
                arm_pair(&pre, bj, reach, SAFETY, 0.0, H, &mut ast)
            } else {
                (false, f64::INFINITY)
            };
            let (on1, _d1) = if cand1 {
                arm_pair(&post, bj, reach, SAFETY, 0.0, H, &mut ast)
            } else {
                (false, f64::INFINITY)
            };
            if cand0 {
                armed_pre += on0 as u64;
                band_ship += (d0 < BAND) as u64;
                band_or_armed += (on0 || d0 < BAND) as u64;
                if let Some(tc) = conj_due(pre.n, bj.n, wrap(pre_el.lam - els[j].lam)) {
                    band_conj += (tc < BAND) as u64;
                }
                if pre.period == bj.period {
                    stand += 1;
                    stand_armed += on0 as u64;
                }
            }
            if truth_check && cand0 {
                let mut v = Vec::new();
                let mut st = Stats::default();
                pair_events(&pre, bj, reach, SAFETY, 0.0, H, &mut st, &mut v);
                if !v.is_empty() {
                    hits_truth += 1;
                    hits_covered += on0 as u64;
                }
            }
            if cand0 && cand1 {
                if on0 != on1 {
                    if on1 {
                        flips_on += 1;
                    } else {
                        flips_off += 1;
                    }
                    if !(d0 < BAND) {
                        if on1 {
                            viol_on += 1;
                        } else {
                            viol_off += 1;
                        }
                    }
                    if !(on0 || d0 < BAND) {
                        if on1 {
                            viol2_on += 1;
                            // Forensics: what was the pre state, and does the exact
                            // machinery actually report an event post-kick?
                            viol_dues.push(d0 / INTERVAL);
                            viol_dns.push((pre.n - bj.n).abs());
                            let mut v = Vec::new();
                            let mut st = Stats::default();
                            pair_events(&post, bj, reach, SAFETY, 0.0, H, &mut st, &mut v);
                            viol_on_post += (!v.is_empty()) as u64;
                            let mut v0 = Vec::new();
                            pair_events(&pre, bj, reach, SAFETY, 0.0, H, &mut st, &mut v0);
                            viol_on_pre += (!v0.is_empty()) as u64;
                        } else {
                            viol2_off += 1;
                        }
                    }
                    if pre.period == bj.period {
                        stand_flip += 1;
                    }
                }
                if d0.is_finite() && _d1.is_finite() {
                    let m = (_d1 - d0).abs() / INTERVAL;
                    move_all.push(m);
                    if d0 < BAND {
                        move_inband.push(m);
                    }
                }
            } else if cand0 != cand1 {
                tier1 += 1;
            }
        }
        secs += t0.elapsed().as_secs_f64();
    }
    let med = |v: &[f64]| -> f64 {
        if v.is_empty() {
            f64::NAN
        } else {
            let mut w = v.to_vec();
            w.sort_by(|x, y| x.total_cmp(y));
            w[w.len() / 2]
        }
    };
    CellOut {
        n,
        seed,
        sigma_e,
        dv,
        kicks,
        reach,
        scanned_per_kick: scanned as f64 / kicks as f64,
        evals_per_kick: evals as f64 / kicks as f64,
        armed_pre_per_kick: armed_pre as f64 / kicks as f64,
        band_ship_per_kick: band_ship as f64 / kicks as f64,
        band_or_armed_per_kick: band_or_armed as f64 / kicks as f64,
        band_conj_per_kick: band_conj as f64 / kicks as f64,
        flips_on,
        flips_off,
        tier1_flips: tier1,
        viol_on,
        viol_off,
        viol2_on,
        viol2_off,
        viol_on_post_events: viol_on_post,
        viol_on_pre_events: viol_on_pre,
        standing_pairs: stand,
        standing_armed: stand_armed,
        standing_flips: stand_flip,
        viol_due_med_intervals: med(&viol_dues),
        viol_dn_med: med(&viol_dns),
        due_move_inband_median: med(&move_inband),
        due_move_all_median: med(&move_all),
        us_per_eval: secs * 1e6 / evals as f64,
        hits_truth,
        hits_covered,
    }
}

/// The live anchor: focal bodies kicked, partners sampled at true belt density in
/// ±0.35 AU (amplified reach optional so arming is live), armed list + churn.
fn run_anchor(seed: u64, focals: usize, partners: usize, dv: f64, reach: f64) {
    let (els, _bodies) = make_cell(10_000, seed, 0.07);
    let mut kr = Rng(seed ^ 0xA11CE ^ (dv.to_bits()));
    let band_true = RHO_AU * TAU * A_C * 0.7; // true partner count in ±0.35 AU
    let mut armed_tot = 0u64;
    let mut flips_on = 0u64;
    let mut flips_off = 0u64;
    let mut viol_on = 0u64;
    let mut viol_off = 0u64;
    let mut band = 0u64;
    let mut evals = 0u64;
    let mut ast = ArmStats::default();
    let mut parts: Vec<Body> = Vec::with_capacity(partners);
    let mut pel: Vec<El> = Vec::with_capacity(partners);
    for fi in 0..focals {
        let i = (fi * 4172 + 11) % 10_000;
        let (pre_el, post_el) = kick_at(&els[i], dv, &mut kr);
        let pre = body_of(&pre_el);
        let post = body_of(&post_el);
        let mut pr = Rng(seed ^ 0x5EED ^ (fi as u64));
        parts.clear();
        pel.clear();
        for _ in 0..partners {
            let u = pr.f64();
            let e = (0.07 * (-2.0 * (1.0 - u).ln()).sqrt()).min(0.4);
            let q = El {
                a: pre_el.a + (pr.f64() - 0.5) * 0.7,
                e,
                pom: TAU * pr.f64(),
                lam: wrap(TAU * pr.f64()),
            };
            pel.push(q);
            parts.push(body_of(&q));
        }
        for (pj, _qj) in parts.iter().zip(pel.iter()) {
            if !is_candidate(&pre, pj, reach) {
                continue;
            }
            evals += 1;
            let (on0, d0) = arm_pair(&pre, pj, reach, SAFETY, 0.0, H, &mut ast);
            let (on1, _d1) = arm_pair(&post, pj, reach, SAFETY, 0.0, H, &mut ast);
            armed_tot += on0 as u64;
            band += (on0 || d0 < BAND) as u64;
            if on0 != on1 {
                if on1 {
                    flips_on += 1;
                } else {
                    flips_off += 1;
                }
                if !(on0 || d0 < BAND) {
                    if on1 {
                        viol_on += 1;
                    } else {
                        viol_off += 1;
                    }
                }
            }
        }
    }
    println!(
        "{{\"exp\":\"anchor\",\"seed\":{},\"focals\":{},\"partners_each\":{},\"dv_2e{}\":{},\"reach_m\":{:.3e},\"armed_sampled\":{},\"armed_per_body_horizon_extrapolated\":{:.1},\"band_or_armed_sampled\":{},\"flips_on\":{},\"flips_off\":{},\"viol_on\":{},\"viol_off\":{},\"flip_fraction_of_armed\":{:.5},\"evals\":{}}}",
        seed,
        focals,
        partners,
        (-dv.log2().round()) as i32,
        dv,
        reach * 1.495978707e11,
        armed_tot,
        armed_tot as f64 * band_true / (focals as f64 * partners as f64),
        band,
        flips_on,
        flips_off,
        viol_on,
        viol_off,
        if armed_tot > 0 { (flips_on + flips_off) as f64 / armed_tot as f64 } else { f64::NAN },
        evals
    );
}

fn main() {
    let t = Instant::now();
    println!(
        "{{\"exp\":\"consts\",\"rho_au2\":{:.6e},\"interval_tu\":{:.5},\"h_tu\":{:.5},\"band_tu\":{:.5},\"reach_au\":{:.6e}}}",
        RHO_AU, INTERVAL, H, BAND, B
    );

    // E1 — the named kill test: cells at 10⁹ density, quantum kick.
    for &(n, seed, kicks) in &[
        (1_000usize, 20261018u64, 600usize),
        (10_000, 20261018, 400),
        (100_000, 20261018, 60),
    ] {
        let o = run_cell(n, seed, 0.07, 2f64.powi(-23), kicks, B, false);
        println!("{}", json_cell(&o));
    }
    // Stability seed and the hot belt at n = 10⁴.
    for &(seed, sigma) in &[(777u64, 0.07f64), (20261018, 0.3)] {
        let o = run_cell(10_000, seed, sigma, 2f64.powi(-23), 400, B, false);
        println!("{}", json_cell(&o));
    }
    // Kick-size controls at n = 10⁴: walk channels scale with dv; re-rolls do not.
    for dv in [2f64.powi(-17), 2f64.powi(-14)] {
        let o = run_cell(10_000, 20261018, 0.07, dv, 200, B, false);
        println!("{}", json_cell(&o));
    }

    // E2 — the live anchor on shipped windows: B (expect near-dead) then ×1000 (live).
    run_anchor(20261018, 24, 30_000, 2f64.powi(-23), B);
    run_anchor(20261018, 24, 30_000, 2f64.powi(-23), B * 1e3);
    run_anchor(31337, 24, 30_000, 2f64.powi(-23), B * 1e3);
    run_anchor(20261018, 24, 30_000, 2f64.powi(-17), B * 1e3);

    // E3 — instrument sanity at amplified reach with the exact machinery as truth.
    let o = run_cell(80, 4242, 0.07, 2f64.powi(-23), 200, 0.02, true);
    println!("{}", json_cell(&o));
    let o = run_cell(80, 4242, 0.07, 2f64.powi(-14), 200, 0.02, true);
    println!("{}", json_cell(&o));

    println!("{{\"exp\":\"done\",\"wall_s\":{:.1}}}", t.elapsed().as_secs_f64());
}

fn json_cell(o: &CellOut) -> String {
    format!(
        "{{\"exp\":\"cell\",\"n\":{},\"seed\":{},\"sigma_e\":{},\"dv_2e{}\":{},\"kicks\":{},\"reach_m\":{:.3e},\"scanned_per_kick\":{:.1},\"evals_per_kick\":{:.1},\"armed_pre_per_kick\":{:.5},\"band_ship_per_kick\":{:.6},\"band_or_armed_per_kick\":{:.6},\"band_conj_per_kick\":{:.6},\"flips_on\":{},\"flips_off\":{},\"tier1_flips\":{},\"viol_on\":{},\"viol_off\":{},\"viol2_on\":{},\"viol2_off\":{},\"viol_on_post_events\":{},\"viol_on_pre_events\":{},\"standing_pairs\":{},\"standing_armed\":{},\"standing_flips\":{},\"viol_due_med_intervals\":{:.4e},\"viol_dn_med\":{:.4e},\"due_move_inband_med\":{:.4e},\"due_move_all_med\":{:.4e},\"us_per_eval\":{:.3},\"hits_truth\":{},\"hits_covered\":{}}}",
        o.n,
        o.seed,
        o.sigma_e,
        (-o.dv.log2().round()) as i32,
        o.dv,
        o.kicks,
        o.reach * 1.495978707e11,
        o.scanned_per_kick,
        o.evals_per_kick,
        o.armed_pre_per_kick,
        o.band_ship_per_kick,
        o.band_or_armed_per_kick,
        o.band_conj_per_kick,
        o.flips_on,
        o.flips_off,
        o.tier1_flips,
        o.viol_on,
        o.viol_off,
        o.viol2_on,
        o.viol2_off,
        o.viol_on_post_events,
        o.viol_on_pre_events,
        o.standing_pairs,
        o.standing_armed,
        o.standing_flips,
        o.viol_due_med_intervals,
        o.viol_dn_med,
        o.due_move_inband_median,
        o.due_move_all_median,
        o.us_per_eval,
        o.hits_truth,
        o.hits_covered
    )
}
