//! Dwell arm on the SHIPPED es-space-v2 integer dense order (events/dense.rs),
//! around the L4 co-orbital island of a circular restricted three-body scene.
//!
//! Inputs (JSON on argv[1]): mu (planet mass fraction), radius/edge (separation
//! fractions), L4 disk (centre + rdet, separation fractions), cap_t (orbital time
//! units), ckpt (checkpoint interval, time units), ics: [[x, y, vx, vy], ...]
//! fractions, traj_idx: indices whose readout trajectory is dumped.
//!
//! Everything runs through emergent_space::events::dense::{Scene, Stepper}
//! unmodified: the quantization, the adaptive dyadic step controller and the
//! Q48 flooring are the shipped law's own. ICs are rounded to the Q48 lattice
//! (an orbit entering the dense order arrives at the doll's granularity).
//! speed_unit = 2^-3 => the orbital speed is c/8 (rule 2: at most c/4).
use emergent_space::events::dense::{Scene, Stepper};
use emergent_space::orbit::Scalar;
use serde::Deserialize;
use std::collections::{BTreeMap, BTreeSet};

#[derive(Deserialize)]
struct Cfg {
    mu: f64,
    radius: f64,
    edge: f64,
    cap_t: f64,
    ckpt: f64,
    ics: Vec<[f64; 4]>,
    traj_idx: Vec<usize>,
}

const ONE: f64 = 281474976710656.0; // 2^48

#[derive(serde::Serialize)]
struct Row {
    i: usize,
    esc_t: f64,
    capped: bool,
    err: Option<String>,
    steps: u64,
    fevals: u64,
}

fn q48(x: f64) -> i64 {
    (x * ONE).round() as i64
}

fn run_one(
    scene: Scene,
    cap: i64,
    ckpt: i64,
    keep_traj: bool,
    ic: [i64; 4],
) -> (Row, Vec<[f64; 5]>) {
    let mut st = match Stepper::new(scene, ic) {
        Ok(s) => s,
        Err(e) => {
            return (
                Row { i: usize::MAX, esc_t: -1.0, capped: false, err: Some(format!("new:{e:?}")), steps: 0, fevals: 0 },
                Vec::new(),
            );
        }
    };
    let mut t = 0i64;
    let mut esc_t = -1.0f64;
    let mut err: Option<String> = None;
    let mut traj = Vec::new();
    'run: loop {
        t = (t + ckpt).min(cap);
        match st.at(t) {
            Ok(y) => {
                let q2 = (y[0] as i128).pow(2) + (y[1] as i128).pow(2);
                let d2 = (y[0] as i128 + ONE as i128).pow(2) + (y[1] as i128).pow(2);
                let lo = ((0.5 * ONE) as i128).pow(2);
                let hi = ((1.5 * ONE) as i128).pow(2);
                let outside = y[1] <= 0 || q2 <= lo || q2 >= hi || d2 <= lo || d2 >= hi;
                if outside {
                    esc_t = t as f64 / ONE;
                    break 'run;
                }
                if keep_traj {
                    traj.push([
                        t as f64 / ONE,
                        y[0] as f64 / ONE,
                        y[1] as f64 / ONE,
                        y[2] as f64 / ONE,
                        y[3] as f64 / ONE,
                    ]);
                }
            }
            Err(e) => {
                err = Some(format!("at:{e:?}"));
                break 'run;
            }
        }
        if t >= cap {
            break 'run;
        }
    }
    (
        Row {
            i: usize::MAX,
            esc_t,
            capped: err.is_none() && esc_t < 0.0,
            err,
            steps: st.counts.steps,
            fevals: st.counts.force_evaluations,
        },
        traj,
    )
}

fn main() {
    let path = std::env::args().nth(1).unwrap();
    let cfg: Cfg = serde_json::from_str(&std::fs::read_to_string(path).unwrap()).unwrap();
    let scene = Scene {
        mu: q48(cfg.mu),
        radius: q48(cfg.radius),
        edge: q48(cfg.edge),
        speed_unit: Scalar::power_of_two(-3),
    };
    let cap = q48(cfg.cap_t);
    let ckpt = q48(cfg.ckpt).max(1);
    let want_traj: BTreeSet<usize> = cfg.traj_idx.iter().copied().collect();

    let jobs: Vec<(usize, [i64; 4], bool)> = cfg
        .ics
        .iter()
        .map(|s| [q48(s[0]), q48(s[1]), q48(s[2]), q48(s[3])])
        .enumerate()
        .map(|(i, ic)| (i, ic, want_traj.contains(&i)))
        .collect();
    let mut rows: BTreeMap<usize, Row> = BTreeMap::new();
    let mut trajs: BTreeMap<usize, Vec<[f64; 5]>> = BTreeMap::new();
    std::thread::scope(|sc| {
        let nthreads = std::thread::available_parallelism().map(|n| n.get()).unwrap_or(4);
        let chunk = jobs.len().div_ceil(nthreads).max(1);
        let mut handles = Vec::new();
        for part in jobs.chunks(chunk) {
            handles.push(sc.spawn(move || {
                let mut out = Vec::new();
                for (i, ic, keep) in part {
                    let (row, traj) = run_one(scene, cap, ckpt, *keep, *ic);
                    out.push((*i, row, traj));
                }
                out
            }));
        }
        for h in handles {
            for (i, mut row, traj) in h.join().unwrap() {
                row.i = i;
                if !traj.is_empty() {
                    trajs.insert(i, traj);
                }
                rows.insert(i, row);
            }
        }
    });
    let out = serde_json::json!({
        "rows": rows.values().collect::<Vec<_>>(),
        "trajs": trajs,
        "scene": {"mu": cfg.mu, "radius": cfg.radius, "edge": cfg.edge,
                  "cap_t": cfg.cap_t, "ckpt": cfg.ckpt,
                  "speed_unit_exp": -3, "n_ics": cfg.ics.len()},
    });
    println!("{}", serde_json::to_string(&out).unwrap());
}
