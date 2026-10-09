//! Second author, run 20261009-1345 (lab/results/20261009-1345-second-20261009-1259-fermi-c7eb-46a6).
//!
//! Dumps, for every TRUTH encounter of the shipped verify belts (sets a, b, c, d — specs copied
//! verbatim from crates/encounters/src/main.rs, same seeds, same radial-pair candidate set and the
//! same `truth_pair`), the per-encounter geometry needed for the impulse ledger:
//!   d        closest-approach distance (AU), as recorded by the truth,
//!   vrel     relative speed at t (units v_circ(1 AU) = 1),
//!   cospsi_i dot(v̂_i, b̂), b = r_j − r_i at closest approach (the impulse direction on body i),
//!   xpm_i    Δa_i per unit perturber mass, in units of body i's period-tick quantum Δa_tick(a_i).
//!
//! Impulse form (straight-line weak hyperbola, G = M_sun = 1): integrating −μ d/|d|³ along the
//! unperturbed relative straight line gives Δv_rel = −2 μ b/(|b|² v_rel), so body i's kick depends
//! only on the perturber mass: Δv_i = +2 m_j b/(|b|² v_rel), Δa_i = 2 a_i² (v_i · Δv_i).
//! At the truth's minimum d·v_rel = 0, so b = r_j − r_i at t. Validated by RK4 in validate.py.
//!
//! Also writes a validation sample (initial/final Newton states around each sampled encounter).
//! Truth replication is single-pass over the same code path the shipped bin uses (THREADS = 4).

use emergent_encounters::belt::{make_belt, Spec};
use emergent_encounters::kepler::{rel, Body, TICKS};
use emergent_encounters::pairs::radial_pairs;
use emergent_encounters::truth::{truth_pair, TruthStats};
use std::f64::consts::TAU;
use std::io::Write as _;

const THREADS: usize = 4;

fn spec(name: &str, n: usize, sigma_e: f64, rho: f64, a_lo: f64, a_hi: f64, keys: usize, orbits: f64, seed: u64) -> Spec {
    Spec { name: name.into(), n, sigma_e, rho, a_lo, a_hi, keys, seed, orbits }
}

fn verify_set(set: &str) -> Vec<Spec> {
    let s = 20261001;
    match set {
        // verbatim from crates/encounters/src/main.rs verify_set
        "a" => vec![
            spec("r8like-s1e-3-r1e-4", 1000, 1e-3, 1e-4, 1.0, 1.5, 0, 200.0, s + 1),
            spec("r8like-s3e-3-r1e-4", 1000, 3e-3, 1e-4, 1.0, 1.5, 0, 100.0, s + 2),
            spec("r8like-s1e-2-r1e-4", 1000, 1e-2, 1e-4, 1.0, 1.5, 0, 100.0, s + 3),
            spec("r8like-s3e-2-r1e-4", 1000, 3e-2, 1e-4, 1.0, 1.5, 0, 50.0, s + 4),
        ],
        "b" => vec![
            spec("r8like-s1e-3-r1e-3", 1000, 1e-3, 1e-3, 1.0, 1.5, 0, 100.0, s + 5),
            spec("r8like-s1e-2-r1e-3", 1000, 1e-2, 1e-3, 1.0, 1.5, 0, 50.0, s + 6),
            spec("r8like-s3e-2-r3e-5", 1000, 3e-2, 3e-5, 1.0, 1.5, 0, 50.0, s + 7),
        ],
        "c" => vec![
            spec("narrow-adversarial", 400, 0.025, 3e-3, 1.0, 1.0025, 0, 20.0, s + 8),
            spec("coorbital", 300, 3e-4, 1e-3, 1.0, 1.0001, 0, 50.0, s + 9),
            spec("equal-period-keys", 300, 1e-2, 1e-3, 1.0, 1.001, 3, 50.0, s + 10),
        ],
        "d" => vec![
            spec("hot-s0.1-r1e-3", 500, 0.1, 1e-3, 1.0, 1.5, 0, 50.0, s + 12),
            spec("mixed-a0.5-3-s0.2-r1e-3", 400, 0.2, 1e-3, 0.5, 3.0, 0, 50.0, s + 13),
            spec("dense-n3000-s1e-2-r3e-4", 3000, 1e-2, 3e-4, 1.0, 1.5, 0, 20.0, s + 14),
        ],
        // this run's own: main-belt-like planar conjunction source for the 3-D game-density case
        "game3d" => vec![spec("game3d-planar", 2000, 0.1, 1e-4, 2.45, 2.95, 0, 50.0, 20261009)],
        _ => panic!("unknown set"),
    }
}

#[derive(Clone, Copy)]
struct Enc4(u32, u32, f64, f64);

fn main() {
    let set = std::env::args().nth(1).expect("usage: enc-dump <set> <out-prefix> [sample-every]");
    let prefix = std::env::args().nth(2).expect("out prefix");
    let sample_every: usize = std::env::args().nth(3).and_then(|x| x.parse().ok()).unwrap_or(30);

    let mut enc_f = std::fs::File::create(format!("{prefix}-enc.jsonl")).unwrap();
    let mut sam_f = std::fs::File::create(format!("{prefix}-sample.jsonl")).unwrap();

    for sp in verify_set(&set) {
        let t0 = std::time::Instant::now();
        let b = make_belt(&sp);
        let t_end = sp.orbits * TAU;
        let rp = radial_pairs(&b, sp.rho);
        // identical structure to the shipped truth_all (par_chunks, THREADS = 4)
        let parts = emergent_encounters::par_chunks(rp.len(), 256, THREADS, |r| {
            let mut out: Vec<Enc4> = Vec::new();
            let mut st = TruthStats::default();
            let mut tmp = Vec::new();
            for &(i, j) in &rp[r] {
                tmp.clear();
                truth_pair(&b[i as usize], &b[j as usize], sp.rho, t_end, &mut tmp, &mut st);
                out.extend(tmp.iter().map(|&(t, d)| Enc4(i, j, t, d)));
            }
            (out, st)
        });
        let mut truth = Vec::new();
        for (o, s) in parts {
            truth.extend(o);
        }
        truth.sort_by(|x, y| (x.0, x.1, x.2).partial_cmp(&(y.0, y.1, y.2)).unwrap());
        eprintln!(
            "  belt {} n={} orbits={} radial_pairs={} truth_enc={} rate={:.3e}/body/orbit ({:.1}s)",
            sp.name, sp.n, sp.orbits, rp.len(), truth.len(),
            truth.len() as f64 / (sp.n as f64 * sp.orbits), t0.elapsed().as_secs_f32()
        );

        let mut k = 0usize;
        for e in &truth {
            let Enc4(i, j, t, d) = *e;
            let (bi, bj) = (&b[i as usize], &b[j as usize]);
            let (dr, dv, _) = rel(bi, bj, t, true); // dr = r_i − r_j
            let vrel = (dv[0] * dv[0] + dv[1] * dv[1]).sqrt();
            let bx = -dr[0]; // b = r_j − r_i, ⊥ v_rel at the minimum
            let by = -dr[1];
            let vi = bi.state_halley(t);
            let vj = bj.state_halley(t);

            // kick Δv = ±2 m_other b/(|b|² v_rel); returns Δa per unit perturber mass in
            // period ticks of the kicked body, and cosψ = v̂ · (kick direction)
            let kick = |v: [f64; 4], a: f64, sgn: f64| -> (f64, f64) {
                let dva = [sgn * 2.0 * bx / (d * d * vrel), sgn * 2.0 * by / (d * d * vrel)];
                let da = 2.0 * a * a * (v[2] * dva[0] + v[3] * dva[1]);
                let p_ticks = TAU * a.powf(1.5) * TICKS;
                let da_tick = (2.0 / 3.0) * a / p_ticks;
                let vnorm = (v[2] * v[2] + v[3] * v[3]).sqrt();
                (da / da_tick, sgn * (v[2] * bx + v[3] * by) / (vnorm * d))
            };
            let (xpm_i, cos_i) = kick(vi, bi.a, 1.0);  // i is pulled toward j: +b
            let (xpm_j, cos_j) = kick(vj, bj.a, -1.0); // j is pulled toward i: −b

            writeln!(
                enc_f,
                "{{\"belt\":\"{}\",\"i\":{},\"j\":{},\"t\":{:.17e},\"d\":{:.17e},\"vrel\":{:.17e},\
\"ai\":{:.17e},\"aj\":{:.17e},\"xpm_i\":{:.17e},\"xpm_j\":{:.17e},\"cospsi_i\":{:.6},\"cospsi_j\":{:.6}}}",
                sp.name, i, j, t, d, vrel, bi.a, bj.a, xpm_i, xpm_j, cos_i, cos_j
            )
            .unwrap();

            if k % sample_every == 0 {
                // validation sample: Newton states at t ± Δ (IC and the Kepler-only counterfactual)
                let delta = (5.0 * d / vrel).max(0.05);
                let si0 = bi.state(t - delta);
                let sj0 = bj.state(t - delta);
                let si1 = bi.state(t + delta);
                let sj1 = bj.state(t + delta);
                writeln!(
                    sam_f,
                    "{{\"belt\":\"{}\",\"i\":{},\"j\":{},\"t\":{:.17e},\"d\":{:.17e},\"vrel\":{:.17e},\
\"delta\":{:.17e},\"xpm_i\":{:.17e},\"ai\":{:.17e},\"aj\":{:.17e},\
\"si0\":[{:.17e},{:.17e},{:.17e},{:.17e}],\"sj0\":[{:.17e},{:.17e},{:.17e},{:.17e}],\
\"si1k\":[{:.17e},{:.17e},{:.17e},{:.17e}],\"sj1k\":[{:.17e},{:.17e},{:.17e},{:.17e}]}}",
                    sp.name, i, j, t, d, vrel, delta, xpm_i, bi.a, bj.a,
                    si0[0], si0[1], si0[2], si0[3], sj0[0], sj0[1], sj0[2], sj0[3],
                    si1[0], si1[1], si1[2], si1[3], sj1[0], sj1[1], sj1[2], sj1[3]
                )
                .unwrap();
            }
            k += 1;
        }
    }
}
