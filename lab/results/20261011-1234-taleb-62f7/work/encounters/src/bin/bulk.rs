//! The bulk probe (lab run 20261011-1234-taleb-62f7). Question: predecessor runs (taleb-236b,
//! taleb-3ebf and their seconds) each measured that when two concentrated packets meet, the real
//! contacts are Θ(n_A·n_B) and punted ("ruin in absolute terms at fleet scale", "the
//! encounter-skin problem"). No tier owns the bulk regime. This run prices the ruin (the law of
//! real-contact counts), names the regime number, and tests the regime-change escape: one
//! aggregate event per packet crossing (per-ship flux λ_i = ρ_B · 2R · L_i, the tube swept by
//! ship i's exact relative trajectory through the opposing packet's measured density grid),
//! O(n) total, zero free parameters, checked against the crate's independent truth.
//!
//! Scenes (rho = 1e-3, all 2-D, deterministic seeds):
//!   belt     uniform belt (control: the discrete regime)
//!   b2-300   the taleb-3ebf interception reproduced at n = 300 (ties to its numbers)
//!   x-*      that interception, n swept 50..800 per fleet
//!   w-*      packet-width sweep at n = 400
//!   a-*      held-out crossing: a = 2.0, e = 0.6 transfer (steeper, faster, non-perihelion)

use emergent_encounters::belt::Rng;
use emergent_encounters::kepler::{Body, TICKS};
use emergent_encounters::pairs::{cone_pairs, radial_pairs};
use emergent_encounters::par_chunks;
use emergent_encounters::truth::{truth_pair, TruthStats};
use std::f64::consts::TAU;
use std::time::Instant;

const THREADS: usize = 4;
const RHO: f64 = 1e-3;
const S0: u64 = 20261012;
const T_MEET: f64 = 2.0 * TAU; // both packets cross longitude 1.0 here

fn wrap(x: f64) -> f64 {
    x.rem_euclid(TAU)
}

fn jitter(rng: &mut Rng, w: f64) -> f64 {
    w * (rng.f64() - rng.f64())
}

fn rayleigh(rng: &mut Rng, sigma: f64, cap: f64) -> f64 {
    let u = rng.f64().min(1.0 - 1e-12);
    sigma * (-2.0 * (1.0 - u).ln()).sqrt().min(cap / sigma)
}

/// A fleet in formation: phase packet of width w on one orbit family (from taleb-3ebf's battle.rs).
fn formation(rng: &mut Rng, n: usize, a0: f64, da: f64, se: f64, e_add: f64, pom_c: Option<f64>, lam_c: f64, w: f64) -> Vec<Body> {
    (0..n)
        .map(|_| {
            let a = a0 + da * rng.f64();
            let e = rayleigh(rng, se, 0.6) + e_add;
            let pom = match pom_c {
                Some(c) => wrap(c + jitter(rng, 0.3)),
                None => TAU * rng.f64(),
            };
            let lam = wrap(lam_c - 0.5 * w + w * rng.f64());
            Body::new(a, e, pom, lam)
        })
        .collect()
}

/// A packet on a transfer orbit that crosses r = 1 at longitude `lam_cross` at t_meet.
/// Perihelion crossings (nu = 0) reproduce taleb-3ebf's `transfer` (pom jitter 0.05, w = 0);
/// nu != 0 (a = 2.0, e = 0.6) is the held-out, steeper and faster crossing.
fn transfer_cross(rng: &mut Rng, n: usize, a: f64, e: f64, lam_cross: f64, t_meet: f64, w: f64, pom_jit: f64, se: f64, da: f64) -> Vec<Body> {
    let p = a * (1.0 - e * e);
    let cos_nu = (p - 1.0) / e;
    assert!(cos_nu >= -1.0 && cos_nu <= 1.0, "orbit does not cross r=1");
    let nu = cos_nu.acos();
    let probe = Body::new(a, e, 0.0, 0.0);
    let m_star = probe.true_to_mean(nu);
    let n_mot = TAU * TICKS / probe.period as f64;
    let pom = wrap(lam_cross - nu);
    let m0 = wrap(m_star - n_mot * t_meet);
    (0..n)
        .map(|_| {
            let a_j = a + da * rng.f64();
            let e_j = e + rayleigh(rng, se, 0.05);
            let pom_j = wrap(pom + jitter(rng, pom_jit));
            let m0_j = wrap(m0 + jitter(rng, w));
            Body::new(a_j, e_j, pom_j, wrap(pom_j + m0_j))
        })
        .collect()
}

struct SceneSpec {
    name: String,
    bodies: Vec<Body>,
    fleets: Vec<u8>,
    t_end: f64,
    meet: Option<(usize, usize, f64)>, // (fleet A, fleet B, t*) for the aggregate; belt: None
}

/// length of segment (p, q) inside the axis-aligned box centered at the origin with half-widths lt, hr
fn clip_len(p: [f64; 2], q: [f64; 2], lt: f64, hr: f64) -> f64 {
    let d = [q[0] - p[0], q[1] - p[1]];
    let mut t0 = 0.0f64;
    let mut t1 = 1.0f64;
    for k in 0..2 {
        let (lo, hi) = if k == 0 { (-lt, lt) } else { (-hr, hr) };
        if d[k] == 0.0 {
            if p[k] < lo || p[k] > hi {
                return 0.0;
            }
        } else {
            let mut ta = (lo - p[k]) / d[k];
            let mut tb = (hi - p[k]) / d[k];
            if ta > tb {
                std::mem::swap(&mut ta, &mut tb);
            }
            t0 = t0.max(ta);
            t1 = t1.min(tb);
        }
    }
    if t0 >= t1 {
        0.0
    } else {
        (t1 - t0) * (d[0] * d[0] + d[1] * d[1]).sqrt()
    }
}

fn run(sc: SceneSpec) {
    let t_wall = Instant::now();
    let b = &sc.bodies;
    let t_end = sc.t_end;
    let inside = |t: f64| t > 0.05 && t < t_end - 0.05;

    // ---- truth: independent conservative advancement on all radially overlapping pairs ----
    let t0 = Instant::now();
    let radial = radial_pairs(b, RHO);
    let parts = par_chunks(radial.len(), 256, THREADS, |r| {
        let mut out = Vec::new();
        let mut st = TruthStats::default();
        let mut tmp = Vec::new();
        for &(i, j) in &radial[r] {
            tmp.clear();
            truth_pair(&b[i as usize], &b[j as usize], RHO, t_end, &mut tmp, &mut st);
            out.extend(tmp.iter().map(|&(t, d)| (i, j, t, d)));
        }
        (out, st)
    });
    let mut truth = Vec::new();
    for (o, _) in parts {
        truth.extend(o);
    }
    let truth_s = t0.elapsed().as_secs_f64();

    let cone = cone_pairs(b, RHO);
    let cone_cross = cone
        .pairs
        .iter()
        .filter(|&&(i, j)| sc.fleets[i as usize] != sc.fleets[j as usize])
        .count();
    let radial_cross = radial
        .iter()
        .filter(|&&(i, j)| sc.fleets[i as usize] != sc.fleets[j as usize])
        .count();

    let mut enc_cross = 0usize;
    let mut enc_within = 0usize;
    let mut enc_cross_outside = 0usize; // truth contacts the aggregate's window cannot see
    let mut c_counts: std::collections::HashMap<u32, usize> = std::collections::HashMap::new();
    for e in &truth {
        if !inside(e.2) {
            continue;
        }
        let (i, j) = (e.0 as usize, e.1 as usize);
        if sc.fleets[i] == sc.fleets[j] {
            enc_within += 1;
        } else {
            enc_cross += 1;
            if let Some((_, _, tstar)) = sc.meet {
                if (e.2 - tstar).abs() > 0.5 * TAU {
                    enc_cross_outside += 1;
                }
            }
            *c_counts.entry(e.0).or_insert(0) += 1;
            *c_counts.entry(e.1).or_insert(0) += 1;
        }
    }

    // ---- the aggregate: one flux integral per packet pair, O((n_A + n_B) * K) Kepler evals ----
    let mut pred_total = 0.0f64;
    let mut corr_n = 0usize;
    let mut sxy = 0.0;
    let mut sx = 0.0;
    let mut sy = 0.0;
    let mut sxx = 0.0;
    let mut syy = 0.0;
    let mut mean_c = 0.0;
    let mut var_c = 0.0;
    let mut lambda_gt0 = 0usize;
    let mut c_gt0 = 0usize;
    let mut pred_active_sum = 0.0;
    let mut c_active_sum = 0.0;
    let mut one_minus_cos_theta = 0.0;
    let mut agg_evals = 0u64;
    if let Some((fa, fb, tstar)) = sc.meet {
        let ia: Vec<usize> = (0..b.len()).filter(|&k| sc.fleets[k] as usize == fa).collect();
        let ib: Vec<usize> = (0..b.len()).filter(|&k| sc.fleets[k] as usize == fb).collect();
        let st_b: Vec<[f64; 4]> = ib.iter().map(|&k| b[k].state(tstar)).collect();
        let (mut cx, mut cy, mut cvx, mut cvy) = (0.0, 0.0, 0.0, 0.0);
        for s in &st_b {
            cx += s[0];
            cy += s[1];
            cvx += s[2];
            cvy += s[3];
        }
        let nb = st_b.len() as f64;
        cx /= nb;
        cy /= nb;
        cvx /= nb;
        cvy /= nb;
        let r0 = (cx * cx + cy * cy).sqrt();
        let ut = [-cy / r0, cx / r0]; // tangential at the packet's mean position
        let ur = [cx / r0, cy / r0]; // radial
        let (mut tmin, mut tmax, mut rmin, mut rmax) = (f64::MAX, f64::MIN, f64::MAX, f64::MIN);
        for s in &st_b {
            let dt = (s[0] - cx) * ut[0] + (s[1] - cy) * ut[1];
            let dr = (s[0] - cx) * ur[0] + (s[1] - cy) * ur[1];
            tmin = tmin.min(dt);
            tmax = tmax.max(dt);
            rmin = rmin.min(dr);
            rmax = rmax.max(dr);
        }
        // measured 2-D density grid over the packet in its own (t, r) frame (no uniformity assumed)
        let (nt, nr) = (24usize, 6usize);
        let dt_w = (tmax - tmin) / nt as f64;
        let dr_w = (rmax - rmin) / nr as f64;
        let mut dens = vec![0u32; nt * nr];
        for s in &st_b {
            let dt = (s[0] - cx) * ut[0] + (s[1] - cy) * ut[1];
            let dr = (s[0] - cx) * ur[0] + (s[1] - cy) * ur[1];
            let it = (((dt - tmin) / dt_w).floor() as i64).clamp(0, nt as i64 - 1) as usize;
            let ir = (((dr - rmin) / dr_w).floor() as i64).clamp(0, nr as i64 - 1) as usize;
            dens[it * nr + ir] += 1;
        }
        let cell_area = dt_w * dr_w;
        // the packet's actual mean flow, sampled (exact Kepler states)
        let k = 257usize;
        let half = 0.5 * TAU;
        let tsamp = |s: usize| tstar - half + (2.0 * half) * (s as f64) / ((k - 1) as f64);
        let mut bmean = Vec::with_capacity(k);
        for s in 0..k {
            let t = tsamp(s);
            let (mut mx, mut my) = (0.0, 0.0);
            for &j in &ib {
                let st = b[j].state(t);
                mx += st[0];
                my += st[1];
            }
            bmean.push([mx / nb, my / nb]);
        }
        agg_evals += (k * (ib.len() + ia.len())) as u64;
        // per A ship: exact relative polyline; flux = sum over grid cells of rho_cell * 2R * (clipped length)
        for &i in &ia {
            let mut prev: Option<[f64; 2]> = None;
            let mut flux = 0.0;
            for s in 0..k {
                let t = tsamp(s);
                let st = b[i].state(t);
                let rel = [st[0] - bmean[s][0], st[1] - bmean[s][1]];
                // co-rotating frame: axes from the packet's mean position at THIS time,
                // so the cloud stays axis-aligned in its own frame across the window
                let br = (bmean[s][0] * bmean[s][0] + bmean[s][1] * bmean[s][1]).sqrt();
                let ut_s = [-bmean[s][1] / br, bmean[s][0] / br];
                let ur_s = [bmean[s][0] / br, bmean[s][1] / br];
                let p = [rel[0] * ut_s[0] + rel[1] * ut_s[1], rel[0] * ur_s[0] + rel[1] * ur_s[1]];
                if let Some(q) = prev {
                    for it in 0..nt {
                        for ir in 0..nr {
                            let cnt = dens[it * nr + ir];
                            if cnt == 0 {
                                continue;
                            }
                            let c_t = tmin + (it as f64 + 0.5) * dt_w;
                            let c_r = rmin + (ir as f64 + 0.5) * dr_w;
                            let l = clip_len([q[0] - c_t, q[1] - c_r], [p[0] - c_t, p[1] - c_r], 0.5 * dt_w, 0.5 * dr_w);
                            flux += cnt as f64 / cell_area * 2.0 * RHO * l;
                        }
                    }
                }
                prev = Some(p);
            }
            let lam = flux;
            pred_total += lam;
            if lam > 0.0 {
                lambda_gt0 += 1;
                pred_active_sum += lam;
            }
            let c = *c_counts.get(&(i as u32)).unwrap_or(&0) as f64;
            if c > 0.0 {
                c_gt0 += 1;
                c_active_sum += c;
            }
            corr_n += 1;
            sxy += lam * c;
            sx += lam;
            sy += c;
            sxx += lam * lam;
            syy += c * c;
        }
        let mid = ia[ia.len() / 2];
        let sa = b[mid].state(tstar);
        let dot = sa[2] * cvx + sa[3] * cvy;
        let ca = (sa[2] * sa[2] + sa[3] * sa[3]).sqrt();
        let cb = (cvx * cvx + cvy * cvy).sqrt();
        one_minus_cos_theta = 1.0 - (dot / (ca * cb)).clamp(-1.0, 1.0);
        if corr_n > 0 {
            mean_c = sy / corr_n as f64;
            var_c = (syy - sy * sy / corr_n as f64) / corr_n as f64;
        }
    }

    let (n_a, n_b) = (
        sc.fleets.iter().filter(|&&f| f == 0).count(),
        sc.fleets.iter().filter(|&&f| f == 1).count(),
    );
    let lam_mean = if corr_n > 0 { sx / corr_n as f64 } else { 0.0 };
    let (corr, vome) = if corr_n > 2 {
        let cov = sxy / corr_n as f64 - (sx / corr_n as f64) * (sy / corr_n as f64);
        let sl = (sxx / corr_n as f64 - (sx / corr_n as f64).powi(2)).max(1e-30);
        let sc_ = (syy / corr_n as f64 - (sy / corr_n as f64).powi(2)).max(1e-30);
        (cov / (sl * sc_).sqrt(), var_c / mean_c.max(1e-30))
    } else {
        (0.0, 0.0)
    };
    let ratio = if enc_cross > 0 { pred_total / enc_cross as f64 } else { 0.0 };
    let orbits = t_end / TAU;
    let per_ship_orbit = if n_a + n_b > 0 {
        (enc_cross + enc_within) as f64 / (n_a + n_b) as f64 / orbits
    } else {
        0.0
    };
    let load = std::fs::read_to_string("/proc/loadavg").unwrap_or_default();
    let load1 = load.split_whitespace().next().unwrap_or("?").to_string();
    let j = |a: Vec<(&str, String)>| {
        let body: Vec<String> = a.iter().map(|(k, v)| format!("\"{}\":{}", k, v)).collect();
        println!("{{{}}}", body.join(","))
    };
    j(vec![
        ("scene", format!("\"{}\"", sc.name)),
        ("n_a", n_a.to_string()),
        ("n_b", n_b.to_string()),
        ("orbits", format!("{:.1}", orbits)),
        ("radial_pairs", radial.len().to_string()),
        ("radial_cross", radial_cross.to_string()),
        ("cone_cross", cone_cross.to_string()),
        ("truth_cross", enc_cross.to_string()),
        ("truth_within", enc_within.to_string()),
        ("cross_outside_window", enc_cross_outside.to_string()),
        ("contacts_per_ship_per_orbit", format!("{:.5}", per_ship_orbit)),
        ("tau_cross_per_ship", format!("{:.4}", enc_cross as f64 / n_a.max(1) as f64)),
        ("p_pair_cross", format!("{:.5}", enc_cross as f64 / ((n_a.max(1) * n_b.max(1)) as f64))),
        ("pred_total", format!("{:.1}", pred_total)),
        ("ratio_pred_truth", format!("{:.3}", ratio)),
        ("lambda_gt0_frac", format!("{:.3}", lambda_gt0 as f64 / corr_n.max(1) as f64)),
        ("lambda_mean", format!("{:.4}", lam_mean)),
        ("counts_mean", format!("{:.4}", mean_c)),
        ("counts_var_over_mean", format!("{:.3}", vome)),
        ("corr_lambda_count", format!("{:.3}", corr)),
        ("frac_a_contact", format!("{:.3}", c_gt0 as f64 / corr_n.max(1) as f64)),
        ("pred_per_active", format!("{:.2}", if lambda_gt0 > 0 { pred_active_sum / lambda_gt0 as f64 } else { 0.0 })),
        ("counts_per_active", format!("{:.2}", if c_gt0 > 0 { c_active_sum / c_gt0 as f64 } else { 0.0 })),
        ("one_minus_cos_theta", format!("{:.4}", one_minus_cos_theta)),
        ("agg_evals", agg_evals.to_string()),
        ("truth_s", format!("{:.2}", truth_s)),
        ("wall_s", format!("{:.2}", t_wall.elapsed().as_secs_f64())),
        ("load1", format!("\"{}\"", load1)),
    ]);
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let which = args.get(1).map(|s| s.as_str()).unwrap_or("all");
    let mk = |name: String, parts: Vec<(Vec<Body>, u8)>, orbits: f64, meet: Option<(usize, usize, f64)>| SceneSpec {
        name,
        bodies: parts.iter().flat_map(|(v, _)| v.iter().copied()).collect(),
        fleets: parts.iter().flat_map(|(v, f)| std::iter::repeat(*f).take(v.len())).collect(),
        t_end: orbits * TAU,
        meet,
    };
    let mut scenes: Vec<SceneSpec> = vec![];
    let meet = Some((0usize, 1usize, T_MEET));
    if which == "all" || which == "control" {
        // uniform belt: the discrete regime (control)
        let mut rng = Rng(S0 + 1);
        let belt: Vec<Body> = (0..1000)
            .map(|_| {
                let a = 1.0 + 1e-3 * rng.f64();
                let e = rayleigh(&mut rng, 3e-4, 0.6);
                let pom = TAU * rng.f64();
                let lam = TAU * rng.f64();
                Body::new(a, e, pom, lam)
            })
            .collect();
        scenes.push(mk("belt-1000".into(), vec![(belt, 0)], 6.0, None));
        // the taleb-3ebf interception at n = 300 (ties to its published numbers)
        let mut rng = Rng(S0 + 2);
        let a = formation(&mut rng, 300, 1.0, 1e-4, 3e-4, 0.0, None, 1.0, 0.5);
        let b = transfer_cross(&mut rng, 300, 1.07, 0.0655, 1.0, T_MEET, 0.0, 0.05, 1e-3, 1e-4);
        scenes.push(mk("b2-300".into(), vec![(a, 0), (b, 1)], 6.0, meet));
    }
    if which == "all" || which == "x" {
        for (n, seed) in [(50usize, S0 + 11), (100, S0 + 12), (200, S0 + 13), (400, S0 + 14), (800, S0 + 15)] {
            let mut rng = Rng(seed);
            let a = formation(&mut rng, n, 1.0, 1e-4, 3e-4, 0.0, None, 1.0, 0.5);
            let b = transfer_cross(&mut rng, n, 1.07, 0.0655, 1.0, T_MEET, 0.0, 0.05, 1e-3, 1e-4);
            scenes.push(mk(format!("x-{}", n), vec![(a, 0), (b, 1)], 6.0, meet));
        }
    }
    if which == "all" || which == "w" {
        for (w, seed) in [(0.5f64, S0 + 21), (0.125, S0 + 22), (0.03125, S0 + 23)] {
            let mut rng = Rng(seed);
            let a = formation(&mut rng, 400, 1.0, 1e-4, 3e-4, 0.0, None, 1.0, w);
            let b = transfer_cross(&mut rng, 400, 1.07, 0.0655, 1.0, T_MEET, 0.0, 0.05, 1e-3, 1e-4);
            scenes.push(mk(format!("w-{:.5}", w), vec![(a, 0), (b, 1)], 6.0, meet));
        }
    }
    if which == "all" || which == "a" {
        // held out: a = 2.0, e = 0.6 crosses r = 1 at nu = 1.085 rad (non-perihelion);
        // steeper (22.6 deg off tangential) and faster (1.225 vs 1.03) than the b2 flow — no refit
        for (n, seed) in [(200usize, S0 + 31), (400, S0 + 32)] {
            let mut rng = Rng(seed);
            let a = formation(&mut rng, n, 1.0, 1e-4, 3e-4, 0.0, None, 1.0, 0.5);
            let b = transfer_cross(&mut rng, n, 2.0, 0.6, 1.0, T_MEET, 0.05, 0.05, 1e-3, 1e-3);
            scenes.push(mk(format!("a-{}", n), vec![(a, 0), (b, 1)], 6.0, meet));
        }
    }
    for sc in scenes {
        run(sc);
    }
}
