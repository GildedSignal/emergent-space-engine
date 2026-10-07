//! The live belt: N planar bodies (the shipped belt generator and Kepler `Body`), driven by an
//! event loop on the shipped exact pair-event machinery. Between kicks every body drifts on its
//! exact Kepler orbit (the law's tube); every pair event with closest approach b < b_cap applies
//! a symmetric impulse (hyperbolic, saturated at |dv| = v_rel below b_90, clamped at contact);
//! the kicked bodies' elements are re-derived from state. Counted per body: quantum crossings of
//! the accumulated kick vector at q (|v_acc| >= q, reset — the ledger model's own quantity),
//! element-word changes at element quanta, kicks applied (= recertifications of that body's
//! candidate pairs, law.md "a kick re-sets only its body's candidate pairs").
//!
//! Rung units: star mu = 1, a in AU-like units, v_kep = 1 at a = 1, time in orbital units
//! (2 pi per orbit at a = 1). Body mass m_kg -> mu_i = m / M_sun.

use emergent_encounters::belt::{make_belt, Spec};
use emergent_encounters::kepler::{Body, TICKS};
use emergent_encounters::method::{pair_events, Stats};
use emergent_encounters::pairs::cone_pairs;
use std::f64::consts::TAU;
use std::time::Instant;

const MSUN: f64 = 1.989e30;
const SAFETY: f64 = 1.1;

/// (a, e, pom, mean longitude at the state's time) from a state (x, y, vx, vy), mu = 1.
fn elements(s: [f64; 4]) -> (f64, f64, f64, f64) {
    let (x, y, vx, vy) = (s[0], s[1], s[2], s[3]);
    let r = (x * x + y * y).sqrt();
    let v2 = vx * vx + vy * vy;
    let a = -1.0 / (2.0 * (v2 / 2.0 - 1.0 / r));
    let rv = x * vx + y * vy;
    let ex = (v2 - 1.0 / r) * x - rv * vx;
    let ey = (v2 - 1.0 / r) * y - rv * vy;
    let e = (ex * ex + ey * ey).sqrt();
    let pom = f64::atan2(ey, ex);
    let f = f64::atan2(y, x) - pom;
    let (sf, cf) = (0.5 * f).sin_cos();
    let ea = 2.0 * ((1.0 - e).sqrt() * sf).atan2((1.0 + e).sqrt() * cf);
    let m = ea - e * ea.sin();
    (a, e, pom, pom + m)
}

#[derive(Default)]
struct Counters {
    crossings: u64,       // |v_acc| >= q events (reabsorbed) -- the ledger's quantity
    kicks: u64,           // impulse applications (each = 1 recertification of that body)
    contacts: u64,        // events clamped below 2 x body radius
    strong: u64,          // kicks saturated at |dv| = v_rel (b < b_90)
    word_writes: u64,     // element-word component changes at element quanta
    vrel_sum: f64,        // sum of |v_rel| at events
    dv_sum: f64,          // sum of |dv| applied
    dv_max: f64,
    dv_cross_sum: f64,    // sum of |v_acc| at crossings
    kicks_per_crossing: u64, // kicks applied to crossing bodies since their last crossing
    kick_count_since: Vec<u64>,
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mut arg = |k: usize, d: f64| args.get(k).map(|s| s.parse::<f64>().unwrap()).unwrap_or(d);
    let n = arg(1, 4000.0) as usize;
    let m_kg = arg(2, 1e18);
    let orbits = arg(3, 20.0);
    let q_frac = arg(4, 1e-6); // far quantum, fraction of v_kep
    let b_cap_mult = arg(5, 10.0); // b_cap = mult x b_q
    let seed = arg(6, 20261101.0) as u64;
    let sigma_e = arg(7, 1e-2);
    let a_lo = arg(8, 1.0);
    let a_hi = arg(9, 1.5);
    let win = arg(10, 1.0); // window in orbits

    let sp = Spec {
        name: "live".into(),
        n,
        sigma_e,
        rho: 1e-4, // placeholder, unused before events
        a_lo,
        a_hi,
        keys: 0,
        seed,
        orbits: 0.0,
    };
    let mu = m_kg / MSUN; // per-body mass parameter
    let v_kep = 1.0f64 / a_lo.sqrt().max(1e-9); // v at inner edge; q is quoted at v_kep(a=1)
    let _ = v_kep;
    let q = q_frac; // far quantum in v units (v_kep = 1 at a = 1)
    let v_typ = 1.4 * sigma_e; // model v_rel for b_cap sizing only
    let b_q = 2.0 * mu / (v_typ * q);
    let b90 = mu / (v_typ * v_typ);
    let b_cap = b_cap_mult * b_q;
    let r_body = (3.0 * mu / (4.0 * std::f64::consts::PI * 2500.0 / MSUN * (1.496e11f64).powi(3))).cbrt(); // rho=2500 kg/m3, a-units
    let b_min = (2.0 * r_body).max(0.0);

    let mut b: Vec<Body> = make_belt(&sp);
    let mut c = Counters::default();
    c.kick_count_since = vec![0; n];
    let mut vac: Vec<[f64; 2]> = vec![[0.0; 2]; n]; // accumulated kick vector per body
    let e_quanta = |x: &Body| [2e-6 * x.a, 1e-6, 1e-6];
    let mut words: Vec<[i64; 3]> = b
        .iter()
        .map(|x| {
            let qt = e_quanta(x);
            [(x.a / qt[0]) as i64, (x.e / qt[1]) as i64, (x.pom / qt[2]) as i64]
        })
        .collect();

    let t0 = Instant::now();
    let n_win = (orbits / win).round() as usize;
    let mut total_events = 0u64;
    let mut scanned_total = 0u64;
    for w in 0..n_win {
        let t0w = w as f64 * win * TAU;
        let t1w = (w + 1) as f64 * win * TAU;
        let cs = cone_pairs(&b, b_cap);
        scanned_total += cs.scanned;
        // events of the window, from current elements (parallel over pair chunks)
        let mut events: Vec<(f64, u32, u32, f64)> = Vec::new(); // (t, i, j, b_pred)
        let pairs = &cs.pairs;
        let parts = emergent_encounters::par_chunks(pairs.len(), 512, 8, |r| {
            let mut ev: Vec<(f64, u32, u32, f64)> = Vec::new();
            let mut st = Stats::default();
            for k in r {
                let &(i, j) = &pairs[k];
                let mut out = Vec::new();
                pair_events(&b[i as usize], &b[j as usize], b_cap, SAFETY, t0w, t1w, &mut st, &mut out);
                for (t, bm) in out {
                    ev.push((t, i, j, bm));
                }
            }
            ev
        });
        for p in parts {
            events.extend(p);
        }
        events.sort_by(|x, y| x.0.total_cmp(&y.0));
        total_events += events.len() as u64;
        for (t, i, j, _bpred) in events {
            let si = b[i as usize].state(t);
            let sj = b[j as usize].state(t);
            let (rx, ry) = (si[0] - sj[0], si[1] - sj[1]);
            let (dvx, dvy) = (si[2] - sj[2], si[3] - sj[3]);
            let r = (rx * rx + ry * ry).sqrt();
            let vrel = (dvx * dvx + dvy * dvy).sqrt();
            if !(r.is_finite() && vrel > 1e-12) {
                continue;
            }
            let bc = r.max(b_min);
            if bc <= b90 * 2.0 {
                c.strong += 1;
            }
            if r < b_min {
                c.contacts += 1;
            }
            // relative impulse magnitude, saturated at v_rel (b <= b_90) and finite at contact
            let dvr = (2.0 * (2.0 * mu) / (bc * vrel)).min(vrel);
            let ux = -rx / r; // u = (ux, uy) = -r̂ points from i to j (r = r_i - r_j)
            let uy = -ry / r;
            // Body i deflects toward j (+dvr/2·u), body j toward i (-dvr/2·u); momentum conserved,
            // |dv| = dvr/2 each, Δv_rel = dvr·r̂ (outward past periapsis, the hyperbolic sense).
            let (dvi, dvj) = ((dvr * 0.5 * ux, dvr * 0.5 * uy), (-dvr * 0.5 * ux, -dvr * 0.5 * uy));
            for (k, dv) in [(i as usize, dvi), (j as usize, dvj)] {
                let s = [b[k].state(t)[0], b[k].state(t)[1], b[k].state(t)[2] + dv.0, b[k].state(t)[3] + dv.1];
                let (a, e, pom, lam) = elements(s);
                if a <= 0.0 || e >= 0.99 || !a.is_finite() {
                    continue; // ejected/collided: leave on old orbit (counted; none expected at these masses)
                }
                let n_new = a.powf(-1.5);
                let lam0 = lam - n_new * t;
                b[k] = Body::new(a, e, pom, lam0);
                c.kicks += 1;
                c.kick_count_since[k] += 1;
                c.dv_sum += (dv.0 * dv.0 + dv.1 * dv.1).sqrt();
                c.dv_max = c.dv_max.max((dv.0 * dv.0 + dv.1 * dv.1).sqrt());
                vac[k][0] += dv.0;
                vac[k][1] += dv.1;
                let qt = e_quanta(&b[k]);
                let w_new = [(b[k].a / qt[0]) as i64, (b[k].e / qt[1]) as i64, (b[k].pom / qt[2]) as i64];
                for cmp in 0..3 {
                    if w_new[cmp] != words[k][cmp] {
                        c.word_writes += 1;
                        words[k][cmp] = w_new[cmp];
                    }
                }
                let vm = (vac[k][0] * vac[k][0] + vac[k][1] * vac[k][1]).sqrt();
                if vm >= q {
                    c.crossings += 1;
                    c.dv_cross_sum += vm;
                    c.kicks_per_crossing += c.kick_count_since[k];
                    c.kick_count_since[k] = 0;
                    vac[k] = [0.0; 2];
                }
            }
            c.vrel_sum += vrel;
        }
    }
    let wall = t0.elapsed().as_secs_f64();
    let orbs = n_win as f64 * win;
    let per_body_orbit = |x: u64| x as f64 / (n as f64 * orbs);
    println!(
        "{{\"exp\":\"livebelt\",\"n\":{},\"m_kg\":{:.3e},\"orbits\":{},\"q\":{:.1e},\"b_cap\":{:.3e},\"b_q\":{:.3e},\"b90\":{:.3e},\"b_min\":{:.3e},\"sigma_e\":{},\
\"events\":{},\"scanned\":{},\"wall_s\":{:.1},\
\"crossings_per_body_orbit\":{:.4e},\"kicks_per_body_orbit\":{:.4e},\"word_writes_per_body_orbit\":{:.4e},\"crossings\":{},\"kicks\":{},\
\"strong_frac\":{:.3},\"contacts\":{},\"mean_vrel\":{:.4e},\"mean_dv\":{:.4e},\"dv_max\":{:.4e},\"mean_dv_at_crossing\":{:.4e},\
\"kicks_per_crossing\":{:.2}}}",
        n, m_kg, orbs, q, b_cap, b_q, b90, b_min, sigma_e,
        total_events, scanned_total, wall,
        per_body_orbit(c.crossings), per_body_orbit(c.kicks), per_body_orbit(c.word_writes), c.crossings, c.kicks,
        c.strong as f64 / total_events.max(1) as f64, c.contacts,
        c.vrel_sum / total_events.max(1) as f64, c.dv_sum / c.kicks.max(1) as f64, c.dv_max,
        c.dv_cross_sum / c.crossings.max(1) as f64, c.kicks_per_crossing as f64 / c.crossings.max(1) as f64
    );
}
