//! Checker-2 adversarial probe for 20261013-2130-redteam-8398 (blind, own attacks).
//! A1: deep transit chains (does the walk converge/cycle/drift? author measured only 2 steps).
//! A2: p outside the author's range (1e4..1e7 vs their max 1000) — maybe the leak closes?
//! A3: retrograde sense (author tested clockwise=false only).
//! A4: unbound passage branch of from_state.
use emergent_space::{binding::{self, Rebinding}, orbit::{Orbit, OrbitKey, Scalar}};
use std::collections::HashSet;

fn keyf(p: i64, e: f64) -> Option<OrbitKey> {
    OrbitKey::bound(Scalar::integer(p), (e * 2f64.powi(48)).round() as u64).ok()
}

fn chain(p: i64, e: f64, coarse: bool, depth: usize) {
    let key0 = match keyf(p, e) { Some(k) => k, None => { println!("chain p={p} e={e}: key refused"); return } };
    let orbit = match Orbit::compile(key0) { Ok(o) => o, Err(_) => { println!("chain p={p} e={e}: compile refused"); return } };
    let period = orbit.period().expect("period");
    let t = period.scale(-2).expect("t");
    let st = orbit.signed_state(t).expect("st");
    let units = if coarse { (-20i16, -50i16) } else {
        (st.radius.exponent() - 60, st.transverse_velocity.abs().exponent() - 60)
    };
    let mut state = binding::cartesian(st, 0, false, units).expect("s0");
    let mut seen = HashSet::new();
    seen.insert(key0);
    let k0 = key0.k as i128;
    let mut first_dks = Vec::new();
    let mut pos = 0i128; let mut neg = 0i128; let mut zero = 0i64;
    let mut cycle_at = None;
    let mut lastk = k0;
    let mut ok = true;
    for i in 0..depth {
        let fit = match Rebinding::from_state(state, t, None) { Ok(f) => f, Err(err) => { println!("chain p={p} e={e} {}: step {i} refused: {err:?}", if coarse {"coarse"} else {"fine"}); ok = false; break } };
        let key = fit.trajectory.key().expect("key");
        if !seen.insert(key) { cycle_at = Some(i); break; }
        lastk = key.k as i128;
        let dk = (key.k as i128 - k0);
        if i < 8 { first_dks.push(key.k.abs_diff(k0 as u64)); }
        if dk > 0 { pos += 1 } else if dk < 0 { neg += 1 } else { zero += 1 }
        state = fit.decoded_event().expect("decode");
    }
    if ok && cycle_at.is_none() {
        println!("chain p={p} e={e} {} depth={depth}: no repeat; net dk/k0 = {}/{} (rel {:.3e}); signs +{pos}/-{neg}/0:{zero}; first dks {first_dks:?}",
            if coarse {"coarse"} else {"fine"}, lastk - k0, k0, (lastk - k0) as f64 / 2f64.powi(48));
    } else if let Some(i) = cycle_at {
        println!("chain p={p} e={e} {}: CYCLE at step {i}", if coarse {"coarse"} else {"fine"});
    }
}

fn one(p: i64, e: f64, phase: i32, coarse: bool, clockwise: bool) -> Option<(bool, u64)> {
    let key = keyf(p, e)?;
    let orbit = Orbit::compile(key).ok()?;
    let period = orbit.period().ok()?;
    let t = period.scale(-(4 - phase)).ok()?; // phase/4 of a period
    let st = orbit.signed_state(t).ok()?;
    let units = if coarse { (-20, -50) } else { (st.radius.exponent() - 60, st.transverse_velocity.abs().exponent() - 60) };
    let state = binding::cartesian(st, 0, clockwise, units).ok()?;
    let fit = Rebinding::from_state(state, t, None).ok()?;
    let key2 = fit.trajectory.key()?;
    Some((key2 == key, key2.k.abs_diff(key.k)))
}

fn main() {
    println!("== A1 deep chains ==");
    for &(p, e, c) in &[(8i64, 0.5f64, false), (20, 0.7, false), (20, 0.7, true), (50, 0.9, false), (8, 0.99, false), (1000, 0.0, false)] {
        chain(p, e, c, 64);
    }
    println!("== A2 out-of-range p (author max 1000) ==");
    for &(p, e) in &[(10_000i64, 0.5f64), (100_000, 0.5), (1_000_000, 0.5), (10_000_000, 0.5), (100_000, 0.9), (1_000_000, 0.9), (1_000_000, 0.9999)] {
        let mut kept = 0; let mut tot = 0; let mut maxdk = 0u64;
        for ph in 1..=4 {
            if let Some((ok, dk)) = one(p, e, ph, false, false) { tot += 1; kept += ok as i32; maxdk = maxdk.max(dk); }
        }
        println!("p={p} e={e}: kept {kept}/{tot}, max dk = {maxdk} q48-ulps (rel {:.3e})", maxdk as f64 / 2f64.powi(48));
    }
    println!("== A3 retrograde (clockwise=true decode) ==");
    for &(p, e) in &[(8, 0.5), (20, 0.7), (50, 0.9), (1000, 0.999)] {
        let mut kept = 0; let mut tot = 0; let mut maxdk = 0u64;
        for ph in 1..=4 {
            if let Some((ok, dk)) = one(p, e, ph, false, true) { tot += 1; kept += ok as i32; maxdk = maxdk.max(dk); }
        }
        println!("retro p={p} e={e}: kept {kept}/{tot}, max dk = {maxdk}");
    }
    println!("== A4 unbound passage branch ==");
    for &(p, e, boost) in &[(20i64, 0.5f64, 1.5f64), (20, 0.7, 2.0), (8, 0.1, 3.0)] {
        let key = match keyf(p, e) { Some(k) => k, None => continue };
        let orbit = match Orbit::compile(key) { Ok(o) => o, Err(_) => continue };
        let period = orbit.period().unwrap();
        let t = period.scale(-2).unwrap();
        let st = orbit.signed_state(t).unwrap();
        let units = (st.radius.exponent() - 60, st.transverse_velocity.abs().exponent() - 60);
        let mut s = binding::cartesian(st, 0, false, units).unwrap();
        // scale the velocity word up: past escape, a passage (unbound) fit
        let (vx, vy) = (s.velocity[0] as f64 * boost, s.velocity[1] as f64 * boost);
        s.velocity = [vx as i64, vy as i64];
        let f1 = match Rebinding::from_state(s, t, None) { Ok(f) => f, Err(err) => { println!("unbound p={p} e={e} boost={boost}: refused {err:?}"); continue } };
        let k1 = f1.trajectory.key().unwrap();
        let s2 = match f1.decoded_event() { Ok(x) => x, Err(err) => { println!("unbound p={p}: decode refused {err:?}"); continue } };
        let f2 = match Rebinding::from_state(s2, t, None) { Ok(f) => f, Err(err) => { println!("unbound p={p} e={e} boost={boost}: refit refused {err:?}"); continue } };
        let k2 = f2.trajectory.key().unwrap();
        println!("unbound p={p} e={e} boost={boost}: periodic={} -> {} key same={} dk={}",
            k1.periodic(), k2.periodic(), k1 == k2, k1.k.abs_diff(k2.k));
    }
}
