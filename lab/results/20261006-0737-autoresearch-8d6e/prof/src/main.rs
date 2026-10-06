//! Replay of the plane's bind() inputs, with per-part timing. Measurement only: the law is untouched.
use emergent_space::binding::IntegerState;
use emergent_space::orbit::{Orbit, Passage};
use emergent_space::binding::Trajectory;
use emergent_space::orbit::Scalar;
use emergent_universe::bind::{bind, Binding};
use emergent_universe::world::Unit;
use std::time::Instant;

fn sc(v: &str) -> Option<Scalar> {
    let (s, e) = v.split_once(',')?;
    let (s, e): (i64, i32) = (s.parse().ok()?, e.parse().ok()?);
    if s == 0 { return Some(Scalar::ZERO); }
    Scalar::raw(s as i128, e - 62).ok()
}

fn median(mut s: Vec<f64>) -> f64 {
    s.sort_by(f64::total_cmp);
    s[s.len() / 2]
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let path = args.get(1).expect("dump file");
    let reps: usize = args.get(2).map(|x| x.parse().unwrap()).unwrap_or(300);
    let text = std::fs::read_to_string(path).unwrap();
    let mut total_bind = Vec::new();
    let mut total_read = Vec::new();
    let mut total_compile = Vec::new();
    let mut n = 0usize;
    let mut total_hash: u64 = 0;
    for line in text.lines().filter(|l| !l.is_empty()) {
        let j: serde_json::Value = serde_json::from_str(line).unwrap();
        let t: i64 = j["t"].as_i64().unwrap();
        let clock_exp: i16 = j["clock_exp"].as_i64().unwrap() as i16;
        let edge = j["edge"].as_str().and_then(sc);
        let u = j["unit"].as_array().unwrap();
        let num = |j: &serde_json::Value, i: usize| -> Scalar {
            let a = j["unit"].as_array().unwrap();
            let s = a[i].as_i64().unwrap();
            let e = a[i + 1].as_i64().unwrap() as i32;
            if s == 0 { Scalar::ZERO } else { Scalar::raw(s as i128, e - 62).unwrap() }
        };
        let unit = Unit { mu: num(&j, 0), inverse: num(&j, 2), unity: j["unit"].as_array().unwrap()[4].as_bool().unwrap() };
        let exact = IntegerState {
            position: [j["p"][0].as_i64().unwrap(), j["p"][1].as_i64().unwrap()],
            velocity: [j["v"][0].as_i64().unwrap(), j["v"][1].as_i64().unwrap()],
            length_exponent: j["le"].as_i64().unwrap() as i16,
            velocity_exponent: j["ve"].as_i64().unwrap() as i16,
        };
        let bound = bind(exact, t, clock_exp, edge, unit).expect("bind refused");
        let mut hash = 0xcbf29ce484222325u64;
        for b in format!("{:?}|{:?}|{:?}|{:?}|{:?}|{}|{:?}",
            bound.tube, bound.residual, bound.turn, bound.orbit, bound.units, bound.entry.clockwise,
            bound.entry.trajectory.key()).bytes() {
            hash ^= b as u64; hash = hash.wrapping_mul(0x100000001b3);
        }
        let mut tbind = Vec::with_capacity(reps);
        for _ in 0..reps {
            let t0 = Instant::now();
            let _ = bind(exact, t, clock_exp, edge, unit).unwrap();
            tbind.push(t0.elapsed().as_secs_f64() * 1e6);
        }
        let binding = Binding {
            doll: 0,
            tube: bound.tube,
            entry: bound.entry.clone(),
            residual: bound.residual,
            turn: bound.turn,
            units: bound.units,
            clock_exp,
            event_time: t,
            kick: emergent_universe::bind::Kick::NONE,
        };
        let _ = binding.readout(t).unwrap();
        let mut tread = Vec::with_capacity(reps);
        for _ in 0..reps {
            let t0 = Instant::now();
            let _ = binding.readout(t).unwrap();
            tread.push(t0.elapsed().as_secs_f64() * 1e6);
        }
        let key = bound.entry.trajectory.key();
        let mut tcompile = Vec::with_capacity(reps);
        for _ in 0..reps {
            let t0 = Instant::now();
            match &bound.entry.trajectory {
                Trajectory::Cycle(_) => { let _ = Orbit::compile(key).unwrap(); }
                Trajectory::Passage(p) => { let _ = Passage::compile(key, p.outer_radius).unwrap(); }
            }
            tcompile.push(t0.elapsed().as_secs_f64() * 1e6);
        }
        let knots = match &bound.entry.trajectory {
            Trajectory::Cycle(c) => c.shape().knots().len(),
            Trajectory::Passage(_) => 0,
        };
        println!(
            "{:3} bind={:7.2}us read={:7.2}us compile={:7.2}us knots={:3} kind={:?}",
            n, median(tbind.clone()), median(tread.clone()), median(tcompile.clone()), knots,
            match &bound.entry.trajectory { Trajectory::Cycle(_) => "cycle", Trajectory::Passage(_) => "passage" }
        );
        total_bind.extend(tbind); total_read.extend(tread); total_compile.extend(tcompile);
        n += 1;
        total_hash = total_hash ^ hash; total_hash = total_hash.wrapping_mul(0x100000001b3);
    }
    println!(
        "\nsummary over {n} inputs x {reps} reps: bind median {:.2}us mean {:.2}us | readout median {:.2}us | compile median {:.2}us",
        median(total_bind.clone()), total_bind.iter().sum::<f64>() / total_bind.len() as f64,
        median(total_read.clone()), median(total_compile.clone())
    );
    println!("output_hash {total_hash:016x}");
}
