//! Dumps the err series B12 actually sees, per law per judged ship, and recomputes the gate's
//! own numbers from them (growth exponent, floor rule, median, worst err) so the dump can be
//! checked against `behave --law <law> --gates B12`'s detail line.
use crate::handoff::{coarse_times, err_series, judged_ships, median, kept, FLOOR};
use crate::laws::{Drift, Echo, LeakPeriod, PlantedBounded, PlantedCompound, Scaled};
use crate::plane::Plane;

mod fit;
mod handoff;
mod laws;
mod plane;
mod restricted;
mod sample;

fn main() {
    let scene = restricted::JUPITER;
    let times = coarse_times(&scene);
    let judged = judged_ships();
    println!(
        "# kept={} judged={} (crossings {:?}) samples={} FLOOR={FLOOR:.0e}",
        kept().len(),
        judged.len(),
        judged.iter().map(|k| k.crossings).collect::<Vec<_>>(),
        times.len()
    );
    let laws: Vec<(&str, Box<dyn handoff::LawR>)> = vec![
        ("echo", Box::new(Echo)),
        ("scaled1e-11", Box::new(Scaled(1e-11))),
        ("planted-bounded", Box::new(PlantedBounded)),
        ("planted-compound", Box::new(PlantedCompound)),
        ("planted-drift", Box::new(Drift)),
        ("leak-per-period", Box::new(LeakPeriod)),
        ("plane", Box::new(Plane::new(None))),
    ];
    let out = std::env::args().nth(1).unwrap_or_else(|| "series".into());
    for (name, law) in &laws {
        let judged = judged_ships();
        let (mut rising, mut worst_err, mut lost) = (Vec::new(), 0.0f64, 0usize);
        let path = format!("{out}_{}.tsv", name.replace('-', "_"));
        let mut per = format!("{out}_pership_{}.tsv", name.replace('-', "_"));
        per = per;
        let mut perbuf = String::new();
        let mut buf = String::new();
        for (si, k) in judged.iter().enumerate() {
            let err = err_series(&scene, law.as_ref(), k.ship, &times);
            let answered = err.iter().all(|e| e.is_finite());
            let top = err.iter().fold(0.0f64, |m, e| if e.is_finite() { m.max(*e) } else { f64::INFINITY });
            if !answered {
                lost += 1;
            } else if !(top <= FLOOR) {
                rising.push(fit::growth_exponent(&err));
            }
            worst_err = if top.is_infinite() { f64::INFINITY } else { worst_err.max(top) };
            for e in &err {
                buf.push_str(&format!("{e:.17e}\t"));
            }
            buf.push('\n');
            let expo = if answered && !(top <= FLOOR) { fit::growth_exponent(&err) } else if answered { 0.0 } else { f64::NAN };
            perbuf.push_str(&format!("{si}\t{answered}\t{top:.17e}\t{expo:.17e}\n"));
        }
        std::fs::write(&per, perbuf).unwrap();
        std::fs::write(&path, buf).unwrap();
        let med = if rising.is_empty() { 0.0 } else { median(rising.clone()) };
        let wor = if rising.is_empty() { 0.0 } else { rising.iter().fold(f64::NEG_INFINITY, |m: f64, &e| if e.is_nan() { f64::INFINITY } else { m.max(e) }) };
        println!(
            "{name:18} answered {}/{} lost {lost} rising {} median-exp {med:.3} worst-exp {wor:.3} worst-err {worst_err:.2e} -> {path}",
            judged.len() - lost,
            judged.len(),
            rising.len()
        );
    }
}
