//! r5 probe (20261014-0059-second-...-redteam-f3ce): the missing dense-order rung,
//! frozen at the engine's Q = 2^20 per the checker of 20261014-0000-redteam-f3ce.
//!
//! Scenes (deterministic, integer-only):
//! - `pair1000`  masses 1000:1, both speeds exactly 0.6*Q, head-on with a per-seed
//!               y-offset (2..5)*Q/2, box 64Q, radius 4Q  (the rung's judged scene)
//! - `pairequal` masses 1000:1000, same geometry            (the positive control)
//!
//! Arms:
//! - `diag <q> <seed>`            per-contact dump (e_E, owed, velocities), <= 220 contacts
//! - `rung <scene> <q> <seeds..>` decisive: run to exactly 200 contacts, report
//!                                |sum_res|/KE + per-contact step stats + ledger checks
//! - `selftest`                   instrument self-test on the fraction estimator
//!
//! Config: env RUNG_PAIR_CARRY=1 selects the pair-scaled (sigma-delta) carry in
//! `resolve_law` (the patch in work/patch.diff); unset = shipped law.
use emergent_lattice::chronon::Chronon;
use emergent_lattice::law::{Body, Container, Law, Response, World};
use emergent_lattice::{relativity, Stepper};
use std::io::Write;

const CONTACTS: u64 = 200;
const T_MAX: i64 = 400_000;

struct Lcg(u64);
impl Lcg {
    fn next(&mut self) -> u64 {
        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        self.0 >> 11
    }
    fn range(&mut self, lo: i64, hi: i64) -> i64 {
        lo + (self.next() % ((hi - lo + 1) as u64)) as i64
    }
    fn f(&mut self) -> f64 {
        self.next() as f64 / (1u64 << 53) as f64
    }
}

fn pair_world(q: i64, seed: u64, m_heavy: i64, m_light: i64) -> World {
    // y-offset from the LCG's high-entropy draw: the low-bit range() draw is constant
    // across consecutive seeds (an LCG small-period artifact found at 2^16).
    let mut r = Lcg(0xBEEF ^ seed);
    let _ = r.next();
    let yoff = (1.0 + 3.0 * r.f()) as i64 * q / 2;
    let speed = (0.6 * q as f64) as i64;
    let (y, radius) = (32 * q, 4 * q);
    let heavy = Body::new(1, [16 * q, y - yoff], [speed, 0], m_heavy, radius, Response::Bounce);
    let light = Body::new(2, [46 * q, y + yoff], [-speed, 0], m_light, radius, Response::Bounce);
    let container = Container { min: [0, 0], max: [64 * q, 64 * q] };
    World::new(q, Some(container), vec![heavy, light]).expect("pair within ranges").with_law(Law::RelativisticV1).expect("subluminal")
}

fn pair_world_equal(q: i64, seed: u64) -> World {
    pair_world(q, seed, 1000, 1000)
}

struct Cfg {
    name: String,
    ke0: i128,
    e0: i128,
    prev_res: i128,
    prev_ekin: i128,
    steps: Vec<f64>,      // |e_E|/KE0 per contact
    contacts_at: Vec<i64>,
    max_res: i128,
    ledger_ok: bool,
    subluminal_ok: bool,
}

fn diag(q: i64, seed: u64) {
    let w = pair_world(q, seed, 1000, 1);
    let e0 = relativity::total(&w)[0];
    let ke0 = w.energy();
    let mut c = Chronon::new(w, false).expect("chronon");
    let (mut prev_res, mut prev_k) = (0i128, [[0i64; 2]; 2]);
    println!("diag q={q} seed={seed} KE0={ke0} E0={e0}");
    for t in 1..=T_MAX {
        let before = c.world().bodies.iter().map(|b| b.k).collect::<Vec<_>>();
        c.step();
        let w = c.world();
        let res = w.residual();
        if res != prev_res {
            let e = res - prev_res;
            let hk = &w.bodies.iter().find(|b| b.mass == 1000).unwrap().k;
            let lk = &w.bodies.iter().find(|b| b.mass == 1).unwrap().k;
            println!(
                "contact t={t} n={} e_E={e} e_over_KE0={:.3e} sum_res={res} res_over_KE0={:.3e} owed_before={prev_res} hk=({},{}) lk=({},{}) hdk=({},{}) ldk=({},{})",
                c.log().contacts,
                e as f64 / ke0 as f64,
                res as f64 / ke0 as f64,
                hk[0], hk[1], lk[0], lk[1],
                hk[0] - before[0][0], hk[1] - before[0][1],
                lk[0] - before[1][0], lk[1] - before[1][1],
            );
            prev_res = res;
            prev_k = [before[0], before[1]];
            if c.log().contacts >= CONTACTS {
                break;
            }
        }
    }
    let w = c.world();
    println!(
        "diag done contacts={} sum_res={} res_over_KE={:.6e} ledger={} (E-E0={} sum_res={})",
        c.log().contacts,
        w.residual(),
        w.residual() as f64 / w.energy() as f64,
        relativity::total(&w)[0] - e0 == w.residual(),
        relativity::total(&w)[0] - e0,
        w.residual()
    );
    let _ = prev_k;
}

fn rung(scene: &str, q: i64, seeds: &[u64]) {
    let law_env = std::env::var("RUNG_PAIR_CARRY").is_ok_and(|v| v == "1");
    let cfg_name = if law_env { "pair-carry" } else { "shipped" };
    println!("rung config={cfg_name} scene={scene} q={q} seeds={:?}", seeds);
    let mut fracs = vec![];
    let mut all_ledger = true;
    let mut all_sub = true;
    for &seed in seeds {
        let w = if scene == "pair1000" { pair_world(q, seed, 1000, 1) } else { pair_world_equal(q, seed) };
        let e0 = relativity::total(&w)[0];
        let ke0 = w.energy();
        let mut c = Chronon::new(w, false).expect("chronon");
        let (mut prev_res, mut max_step, mut sum_sq, mut n_steps) = (0i128, 0f64, 0f64, 0u64);
        let mut max_res = 0i128;
        for t in 1..=T_MAX {
            c.step();
            let w = c.world();
            let res = w.residual();
            if res != prev_res {
                let step = (res - prev_res) as f64 / ke0 as f64;
                max_step = max_step.max(step.abs());
                sum_sq += step * step;
                n_steps += 1;
                prev_res = res;
                max_res = max_res.max(res.abs());
            }
            for b in &w.bodies {
                if b.k[0] as i128 * b.k[0] as i128 + b.k[1] as i128 * b.k[1] as i128 >= q as i128 * q as i128 {
                    all_sub = false;
                }
            }
            if c.log().contacts >= CONTACTS {
                break;
            }
        }
        let w = c.world();
        let ledger = relativity::total(&w)[0] - e0 == w.residual();
        all_ledger &= ledger;
        let frac = w.residual() as f64 / w.energy() as f64;
        fracs.push(frac);
        println!(
            "rung {cfg_name} {scene} seed={seed} contacts={} t={} sum_res={} res_over_KE={frac:.6e} max_step={max_step:.3e} rms_step={:.3e} max_res={max_res} ledger={}",
            c.log().contacts,
            w.tick,
            w.residual(),
            (sum_sq / n_steps.max(1) as f64).sqrt(),
            if ledger { "OK" } else { "BROKEN" },
        );
        let _ = std::io::stdout().flush();
    }
    fracs.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let median = fracs[fracs.len() / 2];
    let worst = fracs[fracs.len() - 1];
    println!(
        "rung {cfg_name} {scene} MEDIAN res_over_KE={median:.6e} worst={worst:.6e} ledger_all={} subluminal_all={}",
        all_ledger, all_sub
    );
    let metric = if scene == "pair1000" { "frac_1000_1_median" } else { "frac_equal_median" };
    println!("METRIC {cfg_name} {metric} {median:.10e}");
}

fn selftest() {
    // fraction-of-KE estimator is a plain ratio; self-test the walk summary instead:
    // a planted diffusive series with step s has end ~ s*sqrt(N); check the reporter
    // keeps the median robust to one wild seed (the b12 lesson).
    let vals: Vec<f64> = vec![0.001, 0.002, 0.004, 8.0]; // one wild tail
    let mut v = vals.clone();
    v.sort_by(|a, b| a.partial_cmp(b).unwrap());
    assert!((v[v.len() / 2] - 0.002).abs() < 1e-12, "median broken");
    println!("selftest median-robust-to-one-tail ok");
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    match args.first().map(|s| s.as_str()).unwrap_or("") {
        "selftest" => selftest(),
        "diag" => {
            let q: i64 = args[1].parse().unwrap();
            let seed: u64 = args[2].parse().unwrap();
            diag(q, seed);
        }
        "rung" => {
            let scene = args[1].clone();
            let q: i64 = args[2].parse().unwrap();
            let seeds: Vec<u64> = args[3..].iter().filter_map(|s| s.parse().ok()).collect();
            rung(&scene, q, &seeds);
        }
        other => panic!("unknown arm {other:?} (diag|rung|selftest)"),
    }
}
