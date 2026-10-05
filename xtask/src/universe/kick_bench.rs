//! Deterministic kick replay on the plane's own scene, without changing its resolver.
use super::{script, Session};
use emergent_space::{
    binding::Trajectory,
    orbit::{MemoCode, ShapeKey},
};
use emergent_universe::{body::What, step, Budget, Kind};
use serde_json::json;
use std::collections::HashSet;
use std::time::Instant;

/// The shapes the rebinds of the replayed kicks asked for, under the exact key and under the law's
/// quantized 12+12-bit memo key (docs/law.md: the cycle memo). A distinct kick is counted once.
#[derive(Default)]
struct Shapes {
    cycles: u64,
    exact: HashSet<ShapeKey>,
    quantized: HashSet<u64>,
}
impl Shapes {
    fn note(&mut self, t: &Trajectory) {
        let Trajectory::Cycle(c) = t else { return };
        self.cycles += 1;
        let key = c.key();
        if let Ok(k) = ShapeKey::for_orbit(key) {
            self.exact.insert(k);
        }
        if let Ok(c) = MemoCode::encode(key) {
            self.quantized.insert(c.bits());
        }
    }
    fn json(&self) -> serde_json::Value {
        let hit = |n: usize| if self.cycles == 0 { 0.0 } else { 1.0 - n as f64 / self.cycles as f64 };
        json!({
            "cycle_rebinds": self.cycles,
            "exact_shapes": self.exact.len(), "exact_hit_rate": hit(self.exact.len()),
            "quantized_shapes": self.quantized.len(), "quantized_hit_rate": hit(self.quantized.len()),
        })
    }
}

fn percentiles(samples: &mut [f64]) -> serde_json::Value {
    samples.sort_by(f64::total_cmp);
    let at = |p: f64| samples.get(((samples.len().saturating_sub(1)) as f64 * p).ceil() as usize).copied();
    json!({"median": at(0.5), "p99": at(0.99), "samples": samples.len()})
}

pub(super) fn run(mut s: Session, seconds: f64) -> crate::Result<u8> {
    let machine_before = crate::measure::machine_state("before");
    // Two populations: the bodies made with the plane (comparable with every earlier run of this bench)
    // and the members a fleet hands out later (the bench once skipped them; they are most of the kicks).
    let (mut made, mut leavers) = (Vec::new(), Vec::new());
    let mut shapes = Shapes::default();
    let made_n = s.n_bodies();
    let mut digest = blake3::Hasher::new();
    let mut refused = 0;
    let mut last: Vec<Option<i64>> = vec![None; made_n];
    let wall = Instant::now();
    let mut frames = 0;
    let mut keys = 0;
    for n in 1..=(seconds * 60.0) as usize {
        if wall.elapsed().as_secs_f64() >= 55.0 {
            return Err("kick replay exceeded 55 s; no complete result".into());
        }
        let now = s.p.u.now;
        if keys != script(n) {
            keys = script(n);
            s.p.u.input(now, keys).map_err(|e| format!("input: {e:?}"))?;
        }
        last.resize(s.n_bodies(), None);
        for (i, seen) in last.iter_mut().enumerate() {
            let rec = s.p.u.rec(i);
            if rec.kind != Kind::Ship || !rec.alive {
                continue;
            }
            let Some(item) = rec.plan.first().copied() else { continue };
            if !matches!(item.what, What::Kick(_)) || *seen == Some(item.t) {
                continue;
            }
            *seen = Some(item.t);
            // Pure resolver, against this exact plane snapshot. Timing includes
            // drift readout, forces, sigma-delta, fitting and the exact remainder;
            // allocator, application, view and formatting are outside the sample.
            let t0 = Instant::now();
            let upd = step::process(&s.p.u.ctx(), i, rec);
            let us = t0.elapsed().as_secs_f64() * 1e6;
            if i < made_n { &mut made } else { &mut leavers }.push(us);
            refused += usize::from(upd.kind != step::Resolved::Kick);
            if let Some(e) = &upd.new_entry {
                shapes.note(&e.trajectory);
            }
            digest.update(format!("{i} {item:?} {:?}", upd.rec).as_bytes());
        }
        s.p.u.frame(1.0 / 60.0, s.rtf, Budget::unlimited());
        s.p.u.settle(s.p.u.now);
        frames = n;
    }
    let mut all: Vec<f64> = made.iter().chain(leavers.iter()).copied().collect();
    println!("{}", serde_json::to_string_pretty(&json!({
        "scope": "one replay per distinct pending ship kick at deterministic 60 Hz plane snapshots; pure resolver only; scheduler/application/view excluded",
        "seed": s.seed, "rtf_target": s.rtf, "frames": frames, "samples": all.len(),
        "kick_us": percentiles(&mut made),
        "kick_us_leavers": percentiles(&mut leavers),
        "kick_us_all": percentiles(&mut all),
        "memo": shapes.json(),
        "refused": refused, "replay_digest": digest.finalize().to_hex().to_string(),
        "digest": s.digest_at_cut(), "machine_before": machine_before,
        "machine_after": crate::measure::machine_state("after"), "wall_seconds": wall.elapsed().as_secs_f64()
    }))?);
    Ok(u8::from(refused != 0))
}
