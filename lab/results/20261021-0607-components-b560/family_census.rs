//! The engine-side key census for formation families (formation-family od 2): do same-orbit
//! members keep one shared due stream in the shipped calendar, and for how many fires?
//! Families of F members on one circular orbit (same r, e = 0), neighbours δx root units apart
//! along the orbit (phase = the fraction of the radial period since periapsis, Q32), plus a
//! clone control (identical spec). The census reads every member's `next_time` — the
//! calendar's own key — once per generation and asks when the streams fork.
use emergent_space::orbit::Scalar;
use emergent_universe::num::{s, Tick};
use emergent_universe::scenario::{AU, STAR_RADIUS};
use emergent_universe::{Budget, Config, Kind, Mass, OrbitSpec, Universe};

fn main() {
    // Arms: neighbour spacing δx in root units; 0.0 = clone control (identical members).
    let arms: [f64; 6] = [0.0, 1e2, 1e3, 1e4, 1e5, 1e6];
    let f: usize = 16;
    let r = std::env::args().nth(1).and_then(|a| a.parse::<i64>().ok()).unwrap_or(AU);
    let fires_cap: usize = std::env::args().nth(2).and_then(|a| a.parse::<usize>().ok()).unwrap_or(300);
    let wall_cap_s: u64 = std::env::args().nth(3).and_then(|a| a.parse::<u64>().ok()).unwrap_or(40);

    let t0 = std::time::Instant::now();
    let mut u = Universe::new(s(STAR_RADIUS), Config::default());
    u.threads = 1;
    let planet = u
        .add_body(
            Kind::Planet,
            OrbitSpec { doll: 0, periapsis: s(r), e_q48: 0, clockwise: false, angle: 0, phase: 0 },
            Scalar::ZERO,
        )
        .expect("planet");
    let mu = Mass::ratio(1, 999).expect("mass");
    let surface = Scalar::raw(4312, -mu.octave).expect("surface");
    u.add_doll("planet", planet, mu, surface).expect("doll");

    let q32 = |turns: f64| (turns * 4294967296.0).round() as u32;
    let dphi = |dx: f64| q32(dx / (std::f64::consts::TAU * r as f64));
    let mut ids: Vec<usize> = Vec::new(); // arm-major: ids[k*f + m]
    for (k, &dx) in arms.iter().enumerate() {
        let base = q32((k as f64 + 0.25) / arms.len() as f64);
        let step = if dx == 0.0 { 0u32 } else { dphi(dx) };
        for m in 0..f {
            let id = u
                .add_body(
                    Kind::Ship,
                    OrbitSpec { doll: 0, periapsis: s(r), e_q48: 0, clockwise: false, angle: 0, phase: base.wrapping_add(step.wrapping_mul(m as u32)) },
                    Scalar::ZERO,
                )
                .expect("ship");
            ids.push(id);
        }
    }
    // The aligned-grid control: two same-orbit planets (the doll split's block time steps, step.rs:19) at
    // δx = 1e6 root apart. If the aligned grid interns dues, their keys coincide forever.
    let pq = q32(0.75);
    let pdx = dphi(1e6);
    let p0 = u.add_body(Kind::Planet, OrbitSpec { doll: 0, periapsis: s(r), e_q48: 0, clockwise: false, angle: 0, phase: pq }, Scalar::ZERO).expect("planet pair 0");
    let p1 = u.add_body(Kind::Planet, OrbitSpec { doll: 0, periapsis: s(r), e_q48: 0, clockwise: false, angle: 0, phase: pq.wrapping_add(pdx) }, Scalar::ZERO).expect("planet pair 1");
    u.start().expect("start");

    let n = ids.len();
    let mut seq: Vec<Vec<i64>> = vec![Vec::new(); n];
    let mut last: Vec<i64> = vec![-1; n];
    let mut distinct: Vec<usize> = vec![0; arms.len()]; // summed distinct dues per census
    let mut censuses = 0usize;
    let mut target: Tick = 0;
    let mut pseq: Vec<Vec<i64>> = vec![Vec::new(); 2];
    let mut plast: [i64; 2] = [-1; 2];
    let pair = [p0, p1];
    let mut pair_cofire = 0usize;
    let mut pair_censuses = 0usize;
    loop {
        let store = u.bodies();
        let mut min_due = i64::MAX;
        for k in 0..arms.len() {
            let mut v: Vec<i64> = Vec::new();
            for m in 0..f {
                let i = k * f + m;
                if let Some(t) = store.next_time(ids[i]) {
                    let t = (t as i128).min(Tick::MAX as i128) as i64;
                    if t != last[i] {
                        seq[i].push(t);
                        last[i] = t;
                    }
                    v.push(t);
                    min_due = min_due.min(t);
                }
            }
            v.sort_unstable();
            v.dedup();
            distinct[k] += v.len();
        }
        {
            let mut pd: Vec<Option<i64>> = pair.iter().map(|&p| store.next_time(p).map(|t| (t as i128).min(Tick::MAX as i128) as i64)).collect();
            for (j, d) in pd.iter().enumerate() {
                if let Some(t) = d {
                    if *t != plast[j] {
                        pseq[j].push(*t);
                        plast[j] = *t;
                    }
                }
            }
            if pd[0].is_some() && pd[1].is_some() {
                pair_censuses += 1;
                pair_cofire += (pd[0] == pd[1]) as usize;
            }
        }
        if min_due == i64::MAX || t0.elapsed().as_secs() >= wall_cap_s {
            break;
        }
        censuses += 1;
        target = if target < min_due { min_due } else { target + 1 };
        u.advance(target, Budget::unlimited());
        let min_fires = (0..arms.len())
            .map(|k| (0..f).map(|m| seq[k * f + m].len()).min().unwrap_or(0))
            .min()
            .unwrap_or(0);
        if min_fires >= fires_cap {
            break;
        }
    }

    let store = u.bodies();
    println!("arm_dx | fires(min/med) | g_fork(min/med/max or none<lo/hi>) | cofire_idx_frac | mean_distinct_dues | step_H_med | anchors_eq | steps_eq");
    for (k, &dx) in arms.iter().enumerate() {
        let ref_seq = &seq[k * f];
        let mut known: Vec<usize> = Vec::new();
        let mut eq_idx = 0usize;
        let mut tot_idx = 0usize;
        let anchors: Vec<i64> = (0..f).map(|m| store.rec(ids[k * f + m]).anchor).collect();
        let steps_all: Vec<i64> = (0..f).map(|m| store.rec(ids[k * f + m]).step).collect();
        let a_spread = anchors.iter().max().unwrap() - anchors.iter().min().unwrap();
        let s_spread = steps_all.iter().max().unwrap() - steps_all.iter().min().unwrap();
        let d0: Vec<i64> = (0..f).map(|m| seq[k * f + m].first().copied().unwrap_or(-1)).collect();
        let d0_spread = d0.iter().max().unwrap() - d0.iter().min().unwrap();
        let dN: Vec<i64> = (0..f).map(|m| seq[k * f + m].last().copied().unwrap_or(-1)).collect();
        let dN_spread = dN.iter().max().unwrap() - dN.iter().min().unwrap();
        eprintln!(
            "arm dx={dx:.0} anchor_spread={a_spread} step_spread={s_spread} first_due_spread={d0_spread} last_due_spread={dN_spread} light_off={light_off:.0}",
            light_off = (f - 1) as f64 * dx
        );
        for m in 0..f {
            let s = &seq[k * f + m];
            let mut g: Option<usize> = None;
            for (j, t) in s.iter().enumerate() {
                if j >= ref_seq.len() || *t != ref_seq[j] {
                    g = Some(j);
                    break;
                }
            }
            if g.is_none() && s.len() < ref_seq.len() {
                g = Some(s.len());
            }
            if let Some(g) = g {
                known.push(g);
            }
            let nc = s.len().min(ref_seq.len());
            tot_idx += nc;
            eq_idx += s.iter().zip(ref_seq.iter()).take(nc).filter(|(a, b)| a == b).count();
        }
        let mut fires: Vec<usize> = (0..f).map(|m| seq[k * f + m].len()).collect();
        fires.sort_unstable();
        let fork_col = if known.is_empty() {
            format!("none<{}/{}>", fires[0], fires[fires.len() - 1])
        } else {
            known.sort_unstable();
            format!("{}/{}/{}", known[0], known[known.len() / 2], known[known.len() - 1])
        };
        let mut steps: Vec<i64> = (0..f).map(|m| store.rec(ids[k * f + m]).step).collect();
        steps.sort_unstable();
        let steps_all_eq = (0..f).all(|m| store.rec(ids[k * f + m]).step == steps[0]);
        let anchors_eq = (0..f).all(|m| store.rec(ids[k * f + m]).anchor == store.rec(ids[k * f]).anchor);
        println!(
            "{dx:7.0} | {}/{:4} | {fork_col:26} | {:.4} | {:6.2} | {} | {} | {}",
            fires[0],
            fires[fires.len() - 1],
            eq_idx as f64 / tot_idx.max(1) as f64,
            distinct[k] as f64 / censuses.max(1) as f64,
            steps[f / 2],
            anchors_eq,
            steps_all_eq
        );
        eprintln!(
            "arm dx={dx:.0} fires={fires:?} forks={known:?} distinct_mean={:.2}",
            distinct[k] as f64 / censuses.max(1) as f64
        );
    }
    // The aligned pair's verdict: equal dues per census, first index where the streams differ.
    let pref = &pseq[0];
    let mut pg = None;
    for (j, t) in pseq[1].iter().enumerate() {
        if j >= pref.len() || *t != pref[j] {
            pg = Some(j);
            break;
        }
    }
    println!(
        "aligned pair (2 planets, same r/e, dx=1e6): co-fire censuses {}/{} (frac {:.4}), stream fork idx {:?}, fires {}/{}, steps {}/{}",
        pair_cofire,
        pair_censuses,
        pair_cofire as f64 / pair_censuses.max(1) as f64,
        pg,
        pseq[0].len(),
        pseq[1].len(),
        store.rec(p0).step,
        store.rec(p1).step
    );
}
