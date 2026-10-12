// The rebind component of a kick, against its floor.
// Truth: Rebinding::from_state per kick (the plane's path: fit + compile + decode).
// J0: keep the anchor's compiled table, no correction (readout only).
// J1: the jet — anchor table + exact per-kick fit (new key, new periapsis time),
//     first-order FD correction of the readout in key space; compile only at re-anchor.
use emergent_space::binding::{cartesian, IntegerState, Rebinding, Trajectory};
use emergent_space::orbit::{Orbit, OrbitKey, OrbitState, Scalar};
use std::time::Instant;

fn f(x: Scalar) -> f64 {
    x.significand() as f64 * 2.0f64.powi(x.exponent() as i32)
}

struct Case {
    name: String,
    r_exp: i16,
    d: f64,
    walk: bool,
    kicks: usize,
}

fn period(tr: &Trajectory) -> emergent_space::Result<Scalar> {
    let mut hi = Scalar::integer(1);
    while tr.state(hi)?.cycles < 1 {
        hi = hi.scale(1)?;
    }
    let mut lo = Scalar::ZERO;
    for _ in 0..80 {
        let mid = lo.add(hi)?.scale(-1)?;
        if tr.state(mid)?.cycles >= 1 {
            hi = mid;
        } else {
            lo = mid;
        }
    }
    Ok(hi)
}

fn run(c: Case) -> emergent_space::Result<()> {
    let r0 = Scalar::power_of_two(c.r_exp);
    let vc = r0.reciprocal()?.sqrt()?;
    let p_exp = c.r_exp - 60;
    let v_exp = -c.r_exp / 2 - 60; // |v| ~ 2^-(r_exp/2): word of 60 bits
    let px = r0.fixed(-(p_exp as i32))? as i64;
    let vt = vc.mul(Scalar::raw(3, -2)?)?;
    let vtq = vt.fixed(-(v_exp as i32))? as i64;
    let st0 = IntegerState {
        position: [px, 0],
        velocity: [0, vtq],
        length_exponent: p_exp,
        velocity_exponent: v_exp,
    };
    let anchor = Rebinding::from_state(st0, Scalar::ZERO, None)?;
    let orbit0 = match &anchor.trajectory {
        Trajectory::Cycle(o) => o.clone(),
        _ => return Err(emergent_space::Error::NotPeriodic),
    };
    let key0 = orbit0.key();
    let peri0 = anchor.periapsis_time;
    let p0 = period(&anchor.trajectory)?;

    // FD tables for the jet: central differences at the anchor key (compiled once per anchor).
    let dk = 1u64 << 37;
    let eps_step = Scalar::power_of_two(-11);
    let keys: Vec<OrbitKey> = vec![
        OrbitKey::new(key0.periapsis, key0.k + dk)?,
        OrbitKey::new(key0.periapsis, key0.k - dk)?,
        OrbitKey::new(key0.periapsis.mul(Scalar::ONE.add(eps_step)?)?, key0.k)?,
        OrbitKey::new(key0.periapsis.mul(Scalar::ONE.sub(eps_step)?)?, key0.k)?,
    ];
    let fd: Vec<Orbit> = keys.iter().map(|k| Orbit::compile(*k)).collect::<Result<_, _>>()?;

    let h = p0.mul(Scalar::raw(1, -3)?)?; // cadence 8 per orbit
    let probes: Vec<Scalar> = vec![p0, p0.mul(Scalar::raw(5, -2)?)?, p0.mul(Scalar::raw(3, -1)?)?, p0.mul(Scalar::raw(7, -2)?)?];
    let dv_rel = Scalar::raw((c.d * 2f64.powi(40)) as i128, -40)?;
    let c2 = Scalar::ONE.div(Scalar::integer(2))?.sqrt()?; // cos 45 = sin 45
    let mut lcg: u64 = 0x243F_6A88_85A3_08D3;

    let mut truth = anchor.clone();
    let mut t = Scalar::ZERO;
    let mut from_state_ns: u128 = 0;
    let mut keys_seen: Vec<OrbitKey> = Vec::new();
    let mut cross = |thr: f64, first: &mut Option<usize>, i: usize, e: f64| {
        if e > thr && first.is_none() {
            *first = Some(i);
        }
    };
    let mut e1t_6: Option<usize> = None;
    let mut e1t_last = 0.0f64;
    let mut e1_6: Option<usize> = None;
    let mut e1_5: Option<usize> = None;
    let mut e0_6: Option<usize> = None;
    let mut e1_last = 0.0f64;
    let mut e0_last = 0.0f64;

    for i in 1..=c.kicks {
        t = t.add(h)?;
        let s = t.sub(truth.periapsis_time)?;
        let ost = truth.trajectory.state(s)?;
        let ist = cartesian(ost, truth.periapsis_angle, truth.clockwise, (p_exp, v_exp))?;
        // kick: d*|v| at 45 deg in the local polar frame (correlated) or an axis (walk)
        let (mut cr, mut ct) = (c2, c2);
        if c.walk {
            lcg = lcg.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            cr = Scalar::ZERO;
            ct = if (lcg >> 63) & 1 == 0 { Scalar::ONE } else { Scalar::ONE.negate() };
            if (lcg >> 62) & 1 == 1 {
                std::mem::swap(&mut cr, &mut ct);
            }
        }
        let vmod = ost.radial_velocity.mul(ost.radial_velocity)?.add(ost.transverse_velocity.mul(ost.transverse_velocity)?)?.sqrt()?;
        let (dvr, dvt) = (dv_rel.mul(vmod)?.mul(cr)?, dv_rel.mul(vmod)?.mul(ct)?);
        let p = [
            Scalar::raw(ist.position[0] as i128, ist.length_exponent as i32)?,
            Scalar::raw(ist.position[1] as i128, ist.length_exponent as i32)?,
        ];
        let r = ost.radius;
        let (cf, sf) = (p[0].div(r)?, p[1].div(r)?);
        let dvx = dvr.mul(cf)?.sub(dvt.mul(sf)?)?;
        let dvy = dvr.mul(sf)?.add(dvt.mul(cf)?)?;
        let mut st = ist;
        st.velocity = [
            st.velocity[0] + dvx.fixed(-(v_exp as i32))? as i64,
            st.velocity[1] + dvy.fixed(-(v_exp as i32))? as i64,
        ];
        let t0 = Instant::now();
        truth = Rebinding::from_state(st, t, None)?;
        from_state_ns += t0.elapsed().as_nanos();
        let key = truth.trajectory.key();
        keys_seen.push(key);

        // probes
        let mut e0m = 0.0f64;
        let mut e1tm = 0.0f64;
        let mut e1m = 0.0f64;
        for pp in &probes {
            let tp = t.add(*pp)?;
            let st_true = truth.trajectory.state(tp.sub(truth.periapsis_time)?)?;
            let st_old = orbit0.signed_state(tp.sub(peri0)?);
            e0m = e0m.max((f(st_old?.radius) - f(st_true.radius)).abs() / f(st_true.radius));
            // J1t: the fit-free jet's bound — the time anchor also stays the anchor's
            let wk2 = Scalar::raw(tp.sub(t)?.significand() as i128 * 0 + key.k as i128 - key0.k as i128, -38)?;
            let wp2 = key.periapsis.sub(key0.periapsis)?.div(key0.periapsis)?.scale(10)?;
            let s1t = tp.sub(peri0)?;
            let baset = orbit0.signed_state(s1t)?;
            let fdkp_t = fd[0].signed_state(s1t)?;
            let fdkm_t = fd[1].signed_state(s1t)?;
            let fdpp_t = fd[2].signed_state(s1t)?;
            let fdpm_t = fd[3].signed_state(s1t)?;
            let jrt = baset
                .radius
                .add(fdkp_t.radius.sub(fdkm_t.radius)?.mul(wk2)?)?
                .add(fdpp_t.radius.sub(fdpm_t.radius)?.mul(wp2)?)?;
            e1tm = e1tm.max((f(jrt) - f(st_true.radius)).abs() / f(st_true.radius));
            let s1 = tp.sub(truth.periapsis_time)?;
            let base = orbit0.signed_state(s1)?;
            let dk_word = key.k as i128 - key0.k as i128;
            let u = key.periapsis.sub(key0.periapsis)?.div(key0.periapsis)?;
            let mut jr = base.radius;
            let mut jvt = base.transverse_velocity;
            let fd_k_p = fd[0].signed_state(s1)?;
            let fd_k_m = fd[1].signed_state(s1)?;
            let fd_p_p = fd[2].signed_state(s1)?;
            let fd_p_m = fd[3].signed_state(s1)?;
            let wk = Scalar::raw(dk_word, -38)?;
            let wp = u.scale(10)?;
            jr = jr
                .add(fd_k_p.radius.sub(fd_k_m.radius)?.mul(wk)?)?
                .add(fd_p_p.radius.sub(fd_p_m.radius)?.mul(wp)?)?;
            jvt = jvt
                .add(fd_k_p.transverse_velocity.sub(fd_k_m.transverse_velocity)?.mul(wk)?)?
                .add(fd_p_p.transverse_velocity.sub(fd_p_m.transverse_velocity)?.mul(wp)?)?;
            e1m = e1m.max((f(jr) - f(st_true.radius)).abs() / f(st_true.radius));
        }
        cross(1e-6, &mut e1t_6, i, e1tm);
        cross(1e-6, &mut e1_6, i, e1m);
        cross(1e-5, &mut e1_5, i, e1m);
        cross(1e-6, &mut e0_6, i, e0m);
        e1_last = e1m;
        e1t_last = e1tm;
        e0_last = e0m;
    }

    // E1: decode-only, jet readout (5 decodes + arithmetic), compile per distinct key
    let s_sample = p0.mul(Scalar::raw(9, -3)?)?;
    let n = 20_000u32;
    let t0 = Instant::now();
    for _ in 0..n {
        let _ = orbit0.signed_state(s_sample)?;
    }
    let decode_ns = t0.elapsed().as_nanos() as f64 / n as f64;
    let t0 = Instant::now();
    for _ in 0..n {
        let s1 = s_sample;
        let base = orbit0.signed_state(s1)?;
        let mut jr = base.radius;
        for k in 0..4 {
            let diff = fd[k].signed_state(s1)?;
            jr = jr.add(diff.radius)?;
        }
        let _ = jr;
    }
    let jet_read_ns = t0.elapsed().as_nanos() as f64 / n as f64;
    let m = keys_seen.len().min(400);
    let t0 = Instant::now();
    for k in &keys_seen[..m] {
        let _ = Orbit::compile(*k)?;
    }
    let compile_us = t0.elapsed().as_secs_f64() * 1e6 / m as f64;

    let distinct = {
        let mut v: Vec<u64> = keys_seen.iter().map(|k| k.k).collect();
        v.sort_unstable();
        v.dedup();
        v.len()
    };
    println!(
        "{}",
        serde_json::json!({
            "case": c.name,
            "kicks": c.kicks,
            "e0_cross_1e-6": e0_6,
            "e1_cross_1e-6": e1_6,
            "e1t_cross_1e-6": e1t_6,
            "e1t_last": e1t_last,
            "e1_cross_1e-5": e1_5,
            "e0_last": e0_last,
            "e1_last": e1_last,
            "from_state_us": from_state_ns as f64 / c.kicks as f64 / 1e3,
            "compile_us": compile_us,
            "decode_ns": decode_ns,
            "jet_read_ns": jet_read_ns,
            "distinct_k_words": distinct,
            "r_exp": c.r_exp,
            "d": c.d,
        })
    );
    Ok(())
}

fn main() -> emergent_space::Result<()> {
    run(Case { name: "weak-corr".into(), r_exp: 24, d: 1e-6, walk: false, kicks: 2000 })?;
    run(Case { name: "weak-walk".into(), r_exp: 24, d: 1e-6, walk: true, kicks: 2000 })?;
    run(Case { name: "weak-corr-d1e-7".into(), r_exp: 24, d: 1e-7, walk: false, kicks: 2000 })?;
    run(Case { name: "strong-corr".into(), r_exp: 12, d: 1e-6, walk: false, kicks: 1000 })?;
    Ok(())
}
