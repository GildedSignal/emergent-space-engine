//! The decisive experiment (checker's named gold experiment for
//! 20261018-0722-scout-6362): derive the closed form on the SHIPPED v1 Householder
//! operator and fly 1648's criterion on the SHIPPED stepper — a crossed-in-bin head-on
//! pair at 0.9c closing must exchange the exact v1 impulse; the shipped skip is the
//! negative control; the τ-window firing test runs in integer arithmetic.
mod fixed;
mod root;
use emergent_lattice::chronon::Chronon;
use emergent_lattice::law::{hit, Body, Law, Response, World};
use emergent_lattice::relativity::{candidates, carried, momentum, targets, total};
use emergent_lattice::worlds;
use emergent_lattice::{Kind, Stepper};
use fixed::{FixedStepper, ROOT_FIRED};
use root::{exact_candidates, float_candidates, Root};

const Q: i64 = 1 << 20;
const R_REACH: i64 = 2048; // 1648's gas reach (radii 1024 + 1024)

fn pair_world(ma: i64, mb: i64, dx: i64, dy: i64, ka: [i64; 2], kb: [i64; 2], radius: i64) -> World {
    let a = Body::new(1, [0, 0], ka, ma, radius, Response::Bounce);
    let b = Body::new(2, [dx, dy], kb, mb, radius, Response::Bounce);
    World::new(Q, None, vec![a, b]).unwrap().with_law(Law::RelativisticV1).unwrap()
}

/// The selection loop of resolve_law, standalone, over given candidate lists.
fn select(
    q: i64,
    ma: i64,
    mb: i64,
    ka: [i64; 2],
    kb: [i64; 2],
    ca_list: Vec<[i64; 2]>,
    cb_list: Vec<[i64; 2]>,
) -> Option<([i64; 2], [i64; 2], [i128; 3])> {
    let (pa, pb) = (momentum(Law::RelativisticV1, ma, ka, q), momentum(Law::RelativisticV1, mb, kb, q));
    let fa: Vec<([i64; 2], [i128; 3])> = ca_list.into_iter().map(|c| (c, momentum(Law::RelativisticV1, ma, c, q))).collect();
    let fb: Vec<([i64; 2], [i128; 3])> = cb_list.into_iter().map(|c| (c, momentum(Law::RelativisticV1, mb, c, q))).collect();
    let old = [pa[0] + pb[0], pa[1] + pb[1], pa[2] + pb[2]];
    let unchanged_allowed = fa.len() * fb.len() == 1;
    let mut best: Option<(i128, [i64; 2], [i64; 2], [i128; 3])> = None;
    for (ca, ea) in &fa {
        for (cb, eb) in &fb {
            if !unchanged_allowed && *ca == ka && *cb == kb {
                continue;
            }
            let e = [ea[0] + eb[0] - old[0], ea[1] + eb[1] - old[1], ea[2] + eb[2] - old[2]];
            let score = e[0] * e[0] + e[1] * e[1] + e[2] * e[2];
            if best.as_ref().is_none_or(|(s, ..)| score < *s) {
                best = Some((score, *ca, *cb, e));
            }
        }
    }
    best.map(|(_, ca, cb, e)| (ca, cb, e))
}

/// Three-way outcome for one fired pair: exact Z[√D], float oracle, cheap quantized.
struct Outcome {
    exact: Option<([i64; 2], [i64; 2])>,
    float: Option<([i64; 2], [i64; 2])>,
    cheap: Option<([i64; 2], [i64; 2])>,
    margin: f64,
    angle_err: f64,
}

fn three_way(rt: &Root, ma: i64, mb: i64, ka: [i64; 2], kb: [i64; 2], j: u32) -> Outcome {
    let q = Q;
    let (pa, pb) = (momentum(Law::RelativisticV1, ma, ka, q), momentum(Law::RelativisticV1, mb, kb, q));
    let ex = rt
        .exact_targets(pa, pb, q)
        .and_then(|(ta, tb)| select(q, ma, mb, ka, kb, exact_candidates(&ta, q), exact_candidates(&tb, q)).map(|(ca, cb, _)| (ca, cb)));
    let ((fta, ftb), margin) = rt.float_targets(pa, pb, q);
    let fl = select(q, ma, mb, ka, kb, float_candidates(fta, q), float_candidates(ftb, q)).map(|(ca, cb, _)| (ca, cb));
    let m = rt.quantized_dir(j);
    let ch = targets(pa, pb, m, q)
        .and_then(|(ta, tb)| select(q, ma, mb, ka, kb, candidates(ta, q), candidates(tb, q)).map(|(ca, cb, _)| (ca, cb)));
    // Angular error of the quantized direction vs the float root normal.
    let sq = (rt.disc as f64).sqrt();
    let nx = (rt.pnum[0] as f64 - sq * rt.w[0] as f64) / rt.ww as f64;
    let ny = (rt.pnum[1] as f64 - sq * rt.w[1] as f64) / rt.ww as f64;
    let n = (nx * nx + ny * ny).sqrt();
    let mn = ((m[0] as f64) * (m[0] as f64) + (m[1] as f64) * (m[1] as f64)).sqrt();
    let dotp = ((m[0] as f64 / mn) * (nx / n) + (m[1] as f64 / mn) * (ny / n)).clamp(-1.0, 1.0);
    Outcome { exact: ex, float: fl, cheap: ch, margin, angle_err: dotp.acos() }
}

fn ledger_ok(w0: &World, w1: &World) -> bool {
    let t0 = total(w0);
    let t1 = total(w1);
    let c1 = carried(w1);
    let de = t1[0] - t0[0];
    let dp0 = t1[1] - t0[1] + (w1.wall_momentum[0] - w0.wall_momentum[0]) as i128;
    let dp1 = t1[2] - t0[2] + (w1.wall_momentum[1] - w0.wall_momentum[1]) as i128;
    de == c1[0] && dp0 == c1[1] && dp1 == c1[2]
}

fn subluminal(w: &World) -> bool {
    let q2 = (w.q * w.q) as i128;
    w.bodies.iter().all(|b| (b.k[0] as i128 * b.k[0] as i128 + b.k[1] as i128 * b.k[1] as i128) < q2)
}

/// 1648's criterion scene: crossed-in-bin head-on pair at 0.9c closing.
fn criterion() {
    println!("== 1648's criterion: crossed-in-bin head-on pair, closing 0.9c, reach {R_REACH}, Q = 2^20 ==");
    let k = 471_859; // ±0.44999c each; |w| = 943718 = 0.89997c
    let (ka, kb) = ([k, 0], [-k, 0]);
    let dx = 3000; // |d0| = 3000 > 2048; both roots of |d0 + s·w| = 2048 lie in (0, 1)
    let w0 = pair_world(1, 1, dx, 0, ka, kb, R_REACH / 2);

    // Negative control: the SHIPPED stepper.
    let mut c = Chronon::new(w0.clone(), true).unwrap();
    for _ in 0..300 {
        c.step();
    }
    let contacts = c.log().sorted().iter().filter(|e| matches!(e.kind, Kind::Contact)).count();
    let ws = c.world();
    let k_unchanged = ws.bodies[0].k == ka && ws.bodies[1].k == kb;
    let passed_through = ws.bodies[0].x[0] > ws.bodies[1].x[0];
    println!("shipped  : contacts logged {contacts} (consumed, no re-fire), velocities unchanged = {k_unchanged}, a passed b = {passed_through}  [THE SKIP]");
    println!("           shipped hit(d0, w, R) = {}", hit([dx as i128, 0], [kb[0] as i128 - ka[0] as i128, 0], R_REACH as i128));

    // The fix: same stepper code, one branch.
    ROOT_FIRED.with(|f| f.set(0));
    let mut fx = FixedStepper::new(w0.clone(), true, true).unwrap();
    for _ in 0..300 {
        fx.step();
    }
    let wf = fx.w.clone();
    let fired = ROOT_FIRED.with(|f| f.get());
    let (ba, bb) = (&wf.bodies[0], &wf.bodies[1]);
    let swapped = ba.k == [-k, 0] && bb.k == [k, 0];
    println!("fixed    : root fired {fired}x, a.k = {:?}, b.k = {:?}, exact head-on swap = {swapped}", ba.k, bb.k);
    println!("           ledger exact = {}, subluminal = {}, residual_a = {}, carry_a = {:?}", ledger_ok(&w0, &wf), subluminal(&wf), ba.residual, ba.carry);

    // Three-way on the root data (exact Z[√D] vs float oracle vs cheap quantized).
    let rt = Root::new([dx as i128, 0], [kb[0] as i128 - ka[0] as i128, 0], R_REACH as i128);
    assert!(rt.fires(), "criterion must fire");
    assert!(rt.identities_hold());
    let ow = three_way(&rt, 1, 1, ka, kb, 31);
    println!("exact==float {} ; exact==cheap(j=31) {} ; margin {:.3e} ; quantized angle {:.3e} rad ; tau- = {:.6}", ow.exact == ow.float, ow.exact == ow.cheap, ow.margin, ow.angle_err, rt.tau_minus_f64());
}

/// Arms: off-axis geometry, grazing clearance, speed, mass contrast.
fn arms() {
    println!("\n== arms: impact parameter x closing speed x mass contrast (crossed-in-bin, R = {R_REACH}) ==");
    println!("{:>8} {:>5} {:>9} | {:>5} {:>13} {:>5} {:>5} {:>9} {:>9} {:>4}", "b", "close", "mass", "fires", "exact a.k", "e=f", "e=c", "margin", "ang_err", "int");
    let (mut all_ef, mut all_ec, mut all_int) = (true, true, true);
    let (mut worst_margin, mut worst_angle) = (f64::INFINITY, 0f64);
    for (name_b, dy) in [("0", 0i64), ("R/16", 128), ("R/2", 1024), ("39R/40", 1997), ("R-8", 2040), ("R-2", 2046), ("R-1", 2047), ("R exactly (tangent, D=0)", 2048)] {
        for close in [0.9f64, 0.5, 0.99] {
            for (ma, mb) in [(1i64, 1i64), (1, 1000), (1, 10000)] {
                let k = ((close / 2.0) * Q as f64) as i64;
                let (ka, kb) = ([k, 0], [-k, 0]);
                let dx = 3000;
                let rt = Root::new([dx as i128, dy as i128], [kb[0] as i128 - ka[0] as i128, 0], R_REACH as i128);
                if !rt.fires() {
                    continue;
                }
                assert!(rt.identities_hold());
                let ow = three_way(&rt, ma, mb, ka, kb, 31);
                all_ef &= ow.exact == ow.float;
                all_ec &= ow.exact == ow.cheap;
                worst_margin = worst_margin.min(ow.margin);
                worst_angle = worst_angle.max(ow.angle_err);
                let w0 = pair_world(ma, mb, dx, dy, ka, kb, R_REACH / 2);
                let mut fx = FixedStepper::new(w0.clone(), false, true).unwrap();
                fx.step();
                let wf = fx.w.clone();
                assert!(ledger_ok(&w0, &wf) && subluminal(&wf), "ledger/subluminal must hold on every arm");
                let int = Some(wf.bodies[0].k) == ow.exact.map(|(c, _)| c);
                all_int &= int;
                println!("{:>8} {:>5.2} {:>4}:{:<5} | {:>5} {:>13?} {:>5} {:>5} {:>9.2e} {:>9.2e} {:>4}", name_b, close, ma, mb, rt.fires(), ow.exact.map(|(c, _)| c), ow.exact == ow.float, ow.exact == ow.cheap, ow.margin, ow.angle_err, int);
            }
        }
    }
    println!("ALL arms: exact==float {all_ef}, exact==cheap {all_ec}, integrated==standalone {all_int}, worst margin {worst_margin:.3e}, worst quantized angle {worst_angle:.3e} rad");
}

/// Random sweep at shipped magnitudes: classification, firing controls, three-way agreement.
fn sweep(n: usize, seed: u64) {
    println!("\n== random sweep (target {n} crossed-in-bin resolved, seed {seed}; |w| <= 1.88e6, R = {R_REACH}) ==");
    let mut rng = worlds::Rng(seed);
    let (mut cross, mut miss, mut past, mut inside, mut class_disagree, mut bad_fire, mut identity_fail) = (0u32, 0u32, 0u32, 0u32, 0u32, 0u32, 0u32);
    let (mut ef, mut ec, mut fired_pairs) = (0u32, 0u32, 0u32);
    let (mut worst_margin, mut worst_angle) = (f64::INFINITY, 0f64);
    let q2 = (Q * Q) as i128;
    let mut attempted = 0u32;
    while fired_pairs < n as u32 && attempted < n as u32 * 60 {
        attempted += 1;
        let kx = rng.range(-Q / 2, Q / 2);
        let ky = rng.range(-Q / 2, Q / 2);
        let wx = rng.range(-940_000, 940_000);
        let wy = rng.range(-940_000, 940_000);
        if wx == 0 && wy == 0 {
            continue;
        }
        let (ka, kb) = ([kx, ky], [kx + wx, ky + wy]);
        if (kb[0] as i128 * kb[0] as i128 + kb[1] as i128 * kb[1] as i128) >= q2 {
            continue;
        }
        let dx = rng.range(-3 * R_REACH, 3 * R_REACH);
        let dy = rng.range(-3 * R_REACH, 3 * R_REACH);
        let d0 = [dx as i128, dy as i128];
        let w_rel = [wx as i128, wy as i128];
        let rt = Root::new(d0, w_rel, R_REACH as i128);
        if !rt.identities_hold() {
            identity_fail += 1;
        }
        let sqd = (rt.disc.max(0) as f64).sqrt();
        let tau = (-rt.dw as f64 - sqd) / rt.ww as f64;
        let fclass = rt.dw < 0 && rt.dd > (R_REACH * R_REACH) as i128 && rt.disc >= 0 && tau >= 0.0 && tau <= 1.0;
        if rt.fires() != fclass {
            class_disagree += 1;
        }
        if rt.disc < 0 {
            miss += 1;
            bad_fire += rt.fires() as u32;
            continue;
        }
        if rt.dd <= (R_REACH * R_REACH) as i128 {
            inside += 1;
            bad_fire += rt.fires() as u32;
            continue;
        }
        if !fclass {
            past += 1;
            bad_fire += rt.fires() as u32;
            continue;
        }
        cross += 1;
        if !rt.fires() || !hit(d0, w_rel, R_REACH as i128) {
            continue;
        }
        let ma = [1i64, 1, 1000, 10000][(attempted % 4) as usize];
        let mb = [1i64, 1000, 1, 10000][(attempted % 4) as usize];
        let ow = three_way(&rt, ma, mb, ka, kb, 31);
        ef += (ow.exact == ow.float) as u32;
        ec += (ow.exact == ow.cheap) as u32;
        worst_margin = worst_margin.min(ow.margin);
        worst_angle = worst_angle.max(ow.angle_err);
        fired_pairs += 1;
    }
    println!("attempted {attempted}: crossed-in-bin {cross} (resolved {fired_pairs}), miss {miss}, past/future {past}, inside {inside}");
    println!("classification (integer window vs float tau-): {class_disagree} disagreements; bad fires: {bad_fire}; identity failures: {identity_fail}");
    println!("exact==float {ef}/{fired_pairs}, exact==cheap(j=31) {ec}/{fired_pairs}, worst margin {worst_margin:.3e}, worst quantized angle {worst_angle:.3e} rad");
}

/// Digest controls: the copy is faithful (fix off = shipped bits), the fix is dormant
/// where nothing crosses, active where pairs do, and the ledger holds end to end.
fn digest_control() {
    println!("\n== digest controls (gas 256 bodies, Q = 2^20, v1, 2000 chronons) ==");
    for (name, vmax) in [("dormant (vmax 256: bodies never meet)", 256i64), ("middle (vmax 2^16: contacts, rho >= 16)", 1 << 16), ("active  (vmax 2^18: rho to 4)", 1 << 18)] {
        let w0 = worlds::gas(256, 0.1, Q, vmax, 3).with_law(Law::RelativisticV1).unwrap();
        let mut ship = Chronon::new(w0.clone(), true).unwrap();
        for _ in 0..2000 {
            ship.step();
        }
        let ds = ship.world().digest();
        let ship_contacts = ship.log().sorted().iter().filter(|e| matches!(e.kind, Kind::Contact)).count();
        ROOT_FIRED.with(|f| f.set(0));
        let mut off = FixedStepper::new(w0.clone(), false, false).unwrap();
        for _ in 0..2000 {
            off.step();
        }
        let d_off = off.w.digest();
        let mut on = FixedStepper::new(w0.clone(), true, true).unwrap();
        for _ in 0..2000 {
            on.step();
        }
        let d_on = on.w.digest();
        let fired = ROOT_FIRED.with(|f| f.get());
        let on_contacts = on.log().sorted().iter().filter(|e| matches!(e.kind, Kind::Contact)).count();
        println!("{name}:");
        println!("  contacts {on_contacts}, root fired {fired} ({:.3}% of contacts)", 100.0 * fired as f64 / on_contacts.max(1) as f64);
        println!("  fix OFF digest == shipped: {} [{:>12}]", d_off == ds, &ds[..12]);
        println!("  fix ON  digest == shipped: {} ; ledger exact (on) = {}, subluminal = {}", d_on == ds, ledger_ok(&w0, &on.w), subluminal(&on.w));
    }
}

/// Overflow audit: the biggest Z[√D] intermediates at the worst shipped magnitudes.
fn overflow_audit() {
    println!("\n== overflow audit (worst shipped magnitudes; exact rule in BigInt) ==");
    for (r_half, k_each, label) in [
        (R_REACH / 2, 471_859i64, "criterion (reach 2048, 0.9c)"),
        (1 << 29, (1 << 20) - 8, "reach 2^30, k = Q-8 (gamma ~ 128)"),
        (1 << 29, 500_000, "reach 2^30, 0.95c closing"),
    ] {
        let reach = 2 * r_half;
        let d0 = [reach as i128 + k_each as i128, 3];
        let w_rel = [-2 * k_each as i128, 1];
        let rt = Root::new(d0, w_rel, reach as i128);
        assert!(rt.fires(), "{label} must fire");
        let pa = momentum(Law::RelativisticV1, 65_536, [k_each, 3], Q);
        let pb = momentum(Law::RelativisticV1, 1, [1 - k_each, 2], Q);
        let out = rt.exact_targets(pa, pb, Q);
        let bits = out.as_ref().map(|(x, y)| x.m0[0].bits().max(x.m1[0].bits()).max(y.m0[1].bits()).max(y.m1[1].bits()).max(x.delta.bits())).unwrap_or(0);
        let dbits = (rt.disc as f64).log2();
        println!("{label}: D = 2^{dbits:.1}, exact-target numerators/denominator <= 2^{bits}; u128 isqrt(D<<2j) needs 2j <= {:.0}", 126.0 - dbits);
    }
}

fn main() {
    println!("contact-root-v1: the scout's closed form on the shipped v1 operator, exact in Z[sqrt D]\n");
    criterion();
    arms();
    sweep(5000, 20261018);
    digest_control();
    overflow_audit();
    println!("\nDONE");
}
