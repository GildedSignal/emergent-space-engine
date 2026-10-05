//! Deterministic kick replay on the plane's own scene, without changing its resolver.
use super::{script, Session};
use emergent_universe::{body::What, step, Budget, Kind};
use serde_json::json;
use std::time::Instant;

pub(super) fn run(mut s: Session, seconds: f64) -> crate::Result<u8> {
    let machine_before = crate::measure::machine_state("before");
    let mut samples = Vec::new();
    let mut digest = blake3::Hasher::new();
    let mut refused = 0;
    let mut last = vec![None; s.n_bodies()];
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
            samples.push(t0.elapsed().as_secs_f64() * 1e6);
            refused += usize::from(upd.kind != step::Resolved::Kick);
            digest.update(format!("{i} {item:?} {:?}", upd.rec).as_bytes());
        }
        s.p.u.frame(1.0 / 60.0, s.rtf, Budget::unlimited());
        s.p.u.settle(s.p.u.now);
        frames = n;
    }
    samples.sort_by(f64::total_cmp);
    let percentile = |p: f64| samples.get(((samples.len().saturating_sub(1)) as f64 * p).ceil() as usize).copied();
    println!("{}", serde_json::to_string_pretty(&json!({
        "scope": "one replay per distinct pending ship kick at deterministic 60 Hz plane snapshots; pure resolver only; scheduler/application/view excluded",
        "seed": s.seed, "rtf_target": s.rtf, "frames": frames, "samples": samples.len(),
        "kick_us": {"median": percentile(0.5), "p99": percentile(0.99)},
        "refused": refused, "replay_digest": digest.finalize().to_hex().to_string(),
        "digest": s.digest_at_cut(), "machine_before": machine_before,
        "machine_after": crate::measure::machine_state("after"), "wall_seconds": wall.elapsed().as_secs_f64()
    }))?);
    Ok(u8::from(refused != 0))
}
