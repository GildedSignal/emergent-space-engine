// The cursor for gravity-at-c (memo R5) — a falsifier probe.
// Run 20261005-1540-q-gravity-cursor-05b0.  Self-contained: rustc -O cursor.rs -o cursor
//
//   ./cursor exact   — cursor vs brute-force retarded selection on integer worldlines
//   ./cursor cost    — integer tests per kick vs history length K and news rate
//   ./cursor burst   — a 1000-event thrust burst: one heavy kick, amortized O(1)
//   ./cursor laplace — the Laplace control driven through the cursor (ret/news/inst)
//   ./cursor ghost   — ghost memory per scale (star system vs galaxy), computed
//
// Integer form: k* = max{ k : t >= t_k and (t-t_k)^2 >= dx^2+dy^2 }  (i128 products, no roots)

use std::env;

struct Rng(u64);
impl Rng {
    fn next(&mut self) -> u64 {
        let mut x = self.0;
        x ^= x >> 12; x ^= x << 25; x ^= x >> 27;
        self.0 = x;
        x.wrapping_mul(0x2545F4914F6CDD1D)
    }
    fn u(&mut self, lo: u64, hi: u64) -> u64 { lo + self.next() % (hi - lo + 1) }
    fn f(&mut self) -> f64 { (self.next() >> 11) as f64 / (1u64 << 53) as f64 }
}

#[derive(Clone, Copy)]
struct Ev { t: i64, x: i64, y: i64 }

#[inline]
fn visible(t: i64, x: i64, y: i64, e: &Ev) -> bool {
    if e.t > t { return false; }
    let dt = (t - e.t) as i128;
    let dx = (x - e.x) as i128;
    let dy = (y - e.y) as i128;
    dt * dt >= dx * dx + dy * dy
}

/// Brute force with no prefix assumption: the maximum index that is visible.
fn brute_k(t: i64, x: i64, y: i64, ev: &[Ev]) -> i64 {
    let mut k: i64 = -1;
    for (i, e) in ev.iter().enumerate() {
        if visible(t, x, y, e) { k = i as i64; }
    }
    k
}

/// One causal integer worldline step: displacement (fx*dt, fy*dt) clamped so
/// dx^2+dy^2 <= dt^2 exactly in integers (nothing past c, principle 23).
fn causal_step(x: i64, y: i64, fx: f64, fy: f64, dt: i64) -> (i64, i64) {
    let mut dx = (fx * dt as f64).round() as i64;
    let mut dy = (fy * dt as f64).round() as i64;
    while (dx as i128) * (dx as i128) + (dy as i128) * (dy as i128) > (dt as i128) * (dt as i128) {
        dx /= 2; dy /= 2;
    }
    (x + dx, y + dy)
}

struct WlCfg { beta_s: f64, beta_c: f64, ev_int: u64, kick_int: u64, photon_c: bool }

/// Random causal worldlines: a source news chain and a consumer kick chain.
fn gen_pair(seed: u64, n_ev: u64, n_kicks: u64, c: &WlCfg) -> (Vec<Ev>, Vec<Ev>) {
    let mut r = Rng(seed);
    let mut ev = Vec::with_capacity(n_ev as usize);
    let (mut sx, mut sy) = (r.u(0, 400_000) as i64, r.u(0, 400_000) as i64);
    let mut t: i64 = 0;
    for _ in 0..n_ev {
        ev.push(Ev { t, x: sx, y: sy });
        let dt = r.u(1, 2 * c.ev_int.max(1)) as i64;
        let sp = c.beta_s * r.f();
        let an = r.f() * std::f64::consts::TAU;
        let (nx, ny) = causal_step(sx, sy, sp * an.cos(), sp * an.sin(), dt);
        sx = nx; sy = ny; t += dt;
    }
    let mut ks = Vec::with_capacity(n_kicks as usize);
    let (mut cx, mut cy) = (r.u(0, 400_000) as i64, r.u(0, 400_000) as i64);
    let mut ct: i64 = 0;
    for _ in 0..n_kicks {
        ks.push(Ev { t: ct, x: cx, y: cy });
        let dt = r.u(1, 2 * c.kick_int.max(1)) as i64;
        if c.photon_c {
            // exactly lightlike steps: a photon consumer (the view/gather path)
            let sgn = if r.next() & 1 == 0 { 1 } else { -1 };
            if r.next() & 1 == 0 { cx += sgn * dt; } else { cy += sgn * dt; }
        } else {
            let sp = c.beta_c * r.f();
            let an = r.f() * std::f64::consts::TAU;
            let (nx, ny) = causal_step(cx, cy, sp * an.cos(), sp * an.sin(), dt);
            cx = nx; cy = ny;
        }
        ct += dt;
    }
    (ev, ks)
}

struct Cost { tests: u64, kicks: u64, advances: u64, mismatch: u64, ahead: u64, max_tpk: u64, tpk: Vec<u64> }

/// Walk the per-(body,source) cursor through the kick chain. check_every = 1 checks
/// the selection against brute force at every kick; >1 samples it; 0 disables it.
fn run_cursor(ev: &[Ev], ks: &[Ev], check_every: u64) -> Cost {
    let mut c = Cost { tests: 0, kicks: 0, advances: 0, mismatch: 0, ahead: 0, max_tpk: 0, tpk: Vec::new() };
    let mut cur: i64 = -1;
    let mut i: u64 = 0;
    for k in ks {
        let mut tpk = 0u64;
        while (cur as usize + 1) < ev.len() {
            c.tests += 1; tpk += 1;
            if visible(k.t, k.x, k.y, &ev[cur as usize + 1]) { cur += 1; c.advances += 1; }
            else { break; }
        }
        c.max_tpk = c.max_tpk.max(tpk);
        c.tpk.push(tpk);
        if check_every > 0 && i % check_every == 0 {
            let b = brute_k(k.t, k.x, k.y, ev);
            if b != cur { c.mismatch += 1; }
            if b < cur { c.ahead += 1; } // cursor ran ahead of the true cone
        }
        c.kicks += 1; i += 1;
    }
    c
}

fn pct(v: &[u64], p: f64) -> u64 {
    let mut s = v.to_vec(); s.sort_unstable();
    s[(((s.len() as f64) * p).floor() as usize).min(s.len() - 1)]
}

// ---------------- exact ----------------
fn cmd_exact() {
    println!("== exact: cursor vs brute force on integer worldlines (300 pairs x 3000 kicks each) ==");
    // (name, beta_source, beta_consumer, ev_int, kick_int)
    let cfgs: &[(&str, f64, f64, u64, u64)] = &[
        ("b_s0.1/c0.1 sparse", 0.1, 0.1, 60_000, 12_000),
        ("b_s0.3/c0.3 sparse", 0.3, 0.3, 60_000, 12_000),
        ("b_s0.5/c0.5 mid",    0.5, 0.5, 20_000, 4_000),
        ("b_s0.9/c0.9 sparse", 0.9, 0.9, 60_000, 12_000),
        ("b_s0.9/c0.1 dense",  0.9, 0.1, 300, 60),
        ("b_s0.1/c0.9 dense",  0.1, 0.9, 300, 60),
        ("b_s0.5/c0.5 dense",  0.5, 0.5, 100, 20),
    ];
    let mut tot_kicks = 0u64; let mut tot_mm = 0u64;
    for (i, (name, bs, bc, ei, ki)) in cfgs.iter().enumerate() {
        let w = WlCfg { beta_s: *bs, beta_c: *bc, ev_int: *ei, kick_int: *ki, photon_c: false };
        let (mut tests, mut adv, mut kicks, mut mm, mut ahead) = (0u64, 0u64, 0u64, 0u64, 0u64);
        for p in 0..300u64 {
            let (ev, ks) = gen_pair(0x9E37_79B9_7F4A_7C15 ^ (i as u64 * 7919 + p), 600, 3000, &w);
            let c = run_cursor(&ev, &ks, 1);
            tests += c.tests; adv += c.advances; kicks += c.kicks; mm += c.mismatch; ahead += c.ahead;
        }
        println!("{:>19}: kicks {:>7} mismatch {:>2} cursor-ahead {:>2} tests/kick {:>6.3} advances/kick {:>7.4}",
            name, kicks, mm, ahead, tests as f64 / kicks as f64, adv as f64 / kicks as f64);
        tot_kicks += kicks; tot_mm += mm;
    }
    // photon consumer: exactly lightlike steps at c
    let w = WlCfg { beta_s: 0.9, beta_c: 1.0, ev_int: 60_000, kick_int: 12_000, photon_c: true };
    let (mut kicks, mut mm, mut ahead) = (0u64, 0u64, 0u64);
    for p in 0..300u64 {
        let (ev, ks) = gen_pair(0xDEAD_BEEF ^ p, 600, 3000, &w);
        let c = run_cursor(&ev, &ks, 1);
        kicks += c.kicks; mm += c.mismatch; ahead += c.ahead;
    }
    println!("{:>19}: kicks {:>7} mismatch {:>2} cursor-ahead {:>2}", "photon at c", kicks, mm, ahead);
    tot_kicks += kicks; tot_mm += mm;

    // head-on closing: source walks +x at 0.9c, consumer walks -x at 0.9c
    {
        let mut ev = Vec::new(); let (mut sx, mut t) = (0i64, 0i64);
        for _ in 0..600 { ev.push(Ev { t, x: sx, y: 500_000 }); sx += 9000; t += 10_000; }
        let mut ks = Vec::new(); let (mut cx, mut ct) = (900_000i64, 0i64);
        for _ in 0..3000 { ks.push(Ev { t: ct, x: cx, y: 500_000 }); cx -= 9000; ct += 10_000; }
        let c = run_cursor(&ev, &ks, 1);
        println!("{:>19}: kicks {:>7} mismatch {:>2} cursor-ahead {:>2} max tests/kick {}",
            "head-on 0.9c", c.kicks, c.mismatch, c.ahead, c.max_tpk);
        tot_kicks += c.kicks; tot_mm += c.mismatch;
    }

    // exact lightlike ties: an event exactly on the kick's past cone must be visible
    let mut tie_ok = 0i64;
    for d in 1..2000i64 {
        let (t, x, y) = (100_000i64, 50_000i64, 60_000i64);
        let on = Ev { t: t - d, x: x - d, y };        // (t-t_k)^2 = d^2 = dx^2: exactly on the cone
        let off = Ev { t: t - d, x: x - d - 1, y };   // one unit farther: outside
        let chain = vec![Ev { t: 0, x: 0, y: 0 }, on]; // causal worldline ending on the cone
        let cur = run_cursor(&chain, &[Ev { t, x, y }], 1);
        if visible(t, x, y, &on) && !visible(t, x, y, &off)
            && cur.mismatch == 0 && cur.advances == 2 { tie_ok += 1; }
    }
    println!("{:>19}: {} / {} tie cases correct (>= includes the cone; +1 quantum excludes it)", "ties", tie_ok, 1999);
    let tot_mm_all = tot_mm + (1999 - tie_ok) as u64;
    println!("\nTOTAL kicks {:>9}  mismatches {}  => {}",
        tot_kicks, tot_mm_all,
        if tot_mm_all == 0 { "CURSOR == BRUTE FORCE EVERYWHERE" } else { "FALSIFIED" });
}

// ---------------- cost ----------------
fn cost_row(label: &str, seed_base: u64, pairs: u64, n_ev: u64, n_kicks: u64, ev_int: u64, kick_int: u64) {
    let w = WlCfg { beta_s: 0.5, beta_c: 0.3, ev_int, kick_int, photon_c: false };
    let (mut tests, mut adv, mut kicks, mut evs, mut mm) = (0u64, 0u64, 0u64, 0u64, 0u64);
    let mut all_tpk: Vec<u64> = Vec::new();
    for p in 0..pairs {
        let (ev, ks) = gen_pair(seed_base ^ (p.wrapping_mul(0x9E37_79B9_7F4A_7C15)), n_ev, n_kicks, &w);
        let c = run_cursor(&ev, &ks, 53);
        tests += c.tests; adv += c.advances; kicks += c.kicks; evs += ev.len() as u64; mm += c.mismatch;
        all_tpk.extend(c.tpk.iter().cloned());
    }
    println!("{:>22}: K {:>7} kicks {:>8} tests/kick {:>7.3} adv/kick {:>8.3} p50 {} p99 {:>3} max {:>4} identity {:>5} brute/kick {:>7} mm {}",
        label, n_ev, kicks, tests as f64 / kicks as f64, adv as f64 / kicks as f64,
        pct(&all_tpk, 0.5), pct(&all_tpk, 0.99), all_tpk.iter().max().unwrap(),
        if tests <= kicks + evs { "OK" } else { "VIOL" }, n_ev, mm);
}

fn cmd_cost() {
    println!("== cost A: history length K sweep, news rate == kick rate (adv/kick ~ 1), 100 pairs each ==");
    for &k in &[600u64, 6_000, 60_000] {
        cost_row("K sweep", 0xABCD_0001, 100, k, k, 20_000, 20_000);
    }
    println!("\n== cost B: news rate sweep, fixed kick cadence (mean 45k), K = same duration, 100 pairs each ==");
    for &ev_int in &[300_000u64, 30_000, 3_000, 300] {
        let n_ev = (3000u64 * 45_000 / ev_int).clamp(600, 400_000); // source spans the consumer's era
        cost_row("rate sweep", 0xABCD_0002, 100, n_ev, 3000, ev_int, 30_000);
    }
    println!("\ncursor cost = 1 + arrivals since last kick (adv/kick), independent of K;\n\
              brute force pays K per kick. Identity: total tests <= total kicks + total events.");
}

// ---------------- burst ----------------
fn cmd_burst() {
    println!("== burst: source emits 1000 news events (a thrust phase), consumer kicks sparsely ==");
    let (mut sx, mut sy, mut t) = (500_000i64, 500_000i64, 0i64);
    let mut ev = Vec::new();
    for _ in 0..1000 { ev.push(Ev { t, x: sx, y: sy }); sx += 3; sy += 1; t += 10; }
    let (mut cx, mut cy, mut ct) = (0i64, 0i64, 0i64);
    let mut ks = Vec::new();
    while ct < t + 1_000_000 {
        ks.push(Ev { t: ct, x: cx, y: cy });
        ct += 20_000; cx += 60; cy += 2_000;
    }
    let c = run_cursor(&ev, &ks, 1);
    println!("events {}  kicks {}  advances {}  tests {}  mean tests/kick {:.4}  max tests/kick {}",
        ev.len(), c.kicks, c.advances, c.tests, c.tests as f64 / c.kicks as f64, c.max_tpk);
    println!("identity: tests {} <= kicks {} + events {} = {}  => {}",
        c.tests, c.kicks, ev.len(), c.kicks + ev.len() as u64,
        if c.tests <= c.kicks + ev.len() as u64 { "holds" } else { "VIOLATED" });
}

// ---------------- laplace ----------------
const TAU: f64 = std::f64::consts::TAU;

#[derive(Clone, Copy, PartialEq)]
enum Sel { Cursor, Brute }
#[derive(Clone, Copy, PartialEq)]
enum Law { Inst, Ret, News, News0 }
struct Ver { t: f64, x: f64, y: f64, vx: f64, vy: f64 }

/// Kepler-propagate the pair's relative orbit from a recorded version to time t.
/// Versions store absolute state; for equal masses about a fixed CM, relative = 2 x absolute.
/// Returns the source body's absolute position at t (the "where it is now" of old news).
// (kepler_pos now below, universal-variable form)
fn kepler_pos(v: &Ver, t: f64, mu: f64) -> (f64, f64) {
    // Universal-variable two-body propagation (Stumpff f&g): regular at e = 0
    // (the e-vector parametrization is degenerate for circular orbits).
    let (x, y, vx, vy) = (2.0 * v.x, 2.0 * v.y, 2.0 * v.vx, 2.0 * v.vy);
    let (px, py) = uv_prop(x, y, vx, vy, t - v.t, mu);
    (0.5 * px, 0.5 * py)
}

fn stump(z: f64) -> (f64, f64) {
    let (mut c, mut s);
    if z.abs() < 1e-2 {
        c = 0.5 - z / 24.0 + z * z / 720.0 - z * z * z / 40320.0;
        s = 1.0 / 6.0 - z / 120.0 + z * z / 5040.0 - z * z * z / 362880.0;
    } else if z > 0.0 {
        let sz = z.sqrt();
        c = (1.0 - sz.cos()) / z;
        s = (sz - sz.sin()) / (z * sz);
    } else {
        let sz = (-z).sqrt();
        c = (sz.cosh() - 1.0) / (-z);
        s = (sz.sinh() - sz) / ((-z) * sz);
    }
    if !c.is_finite() { c = 0.5; }
    if !s.is_finite() { s = 1.0 / 6.0; }
    (c, s)
}

/// Stumpff universal propagation of (r0, v0) by dt; fixed 24 secant iterations
/// on the time equation (monotone in chi), then f&g.
fn uv_prop(x0: f64, y0: f64, vx: f64, vy: f64, dt: f64, mu: f64) -> (f64, f64) {
    let r0 = (x0 * x0 + y0 * y0).sqrt();
    let v2 = vx * vx + vy * vy;
    let alpha = 2.0 / r0 - v2 / mu;
    let sq = mu.sqrt();
    let rv = (x0 * vx + y0 * vy) / sq;
    // time as a function of chi
    let t_of = |chi: f64| -> f64 {
        let z = alpha * chi * chi;
        let (c, s) = stump(z);
        (rv * chi * chi * c + (1.0 - alpha * r0) * chi * chi * chi * s + r0 * chi) / sq
    };
    let mut chi = if alpha > 0.0 { sq * dt * alpha } else { sq * dt / r0 };
    let mut chi_prev = chi * 0.99;
    let mut f_prev = t_of(chi_prev) - dt;
    for _ in 0..24 {
        let f = t_of(chi) - dt;
        let d = f - f_prev;
        if d.abs() < 1e-18 { break; }
        let chi_next = chi - f * (chi - chi_prev) / d;
        chi_prev = chi; f_prev = f;
        chi = chi_next;
        if !chi.is_finite() { chi = 0.0; break; }
    }
    let z = alpha * chi * chi;
    let (c, s) = stump(z);
    let f = 1.0 - chi * chi / r0 * c;
    let g = dt - chi * chi * chi / sq * s;
    (f * x0 + g * vx, f * y0 + g * vy)
}
fn interp_path(hist: &[Ver], t: f64) -> (f64, f64) {
    if hist.len() < 2 {
        let v = hist.last().unwrap();
        return (v.x, v.y);
    }
    let dt = hist[1].t - hist[0].t;
    let mut i0 = (((t - hist[0].t) / dt).floor() as isize).max(0) as usize;
    i0 = i0.min(hist.len() - 2);
    let f = ((t - hist[i0].t) / dt).clamp(0.0, 1.0);
    let (v0, v1) = (&hist[i0], &hist[i0 + 1]);
    let h00 = 2.0 * f * f * f - 3.0 * f * f + 1.0;
    let h10 = f * f * f - 2.0 * f * f + f;
    let h01 = -2.0 * f * f * f + 3.0 * f * f;
    let h11 = f * f * f - f * f;
    (h00 * v0.x + h10 * dt * v0.vx + h01 * v1.x + h11 * dt * v1.vx,
     h00 * v0.y + h10 * dt * v0.vy + h01 * v1.y + h11 * dt * v1.vy)
}

struct LapResult {
    unbound_at: Option<f64>, dE: f64, a_drift: f64, ecc: f64,
    sel_diff: u64, sel_checks: u64, lag_mean: f64, lag_max: i64, bits: [u64; 8],
}

fn laplace_run(law: Law, sel: Sel, beta: f64, n_orbits: usize, steps_per_orbit: usize) -> LapResult {
    let c = 0.5 / beta;              // equal-mass binary, relative a=1, so each body moves at 0.5
    let mu = 1.0f64;
    let period = TAU;
    let dt = period / steps_per_orbit as f64;
    let dth = 0.5 * dt;
    let (mut ax, mut ay, mut avx, mut avy) = (-0.5f64, 0.0, 0.0, -0.5f64);
    let (mut bx, mut by, mut bvx, mut bvy) = (0.5f64, 0.0, 0.0, 0.5f64);
    let mut t = 0.0f64;
    let mut hist_a: Vec<Ver> = vec![Ver { t, x: ax, y: ay, vx: avx, vy: avy }];
    let mut hist_b: Vec<Ver> = vec![Ver { t, x: bx, y: by, vx: bvx, vy: bvy }];
    let (mut cur_a, mut cur_b): (i64, i64) = (-1, -1); // per (body, source) pair
    let (mut sel_diff, mut sel_checks) = (0u64, 0u64);
    let (mut lag_sum, mut lag_n, mut lag_max) = (0.0f64, 0u64, 0i64);
    let mut unbound_at: Option<f64> = None;
    let n_steps = n_orbits * steps_per_orbit;

    // News selection in the scene's light speed: (c*dtl)^2 >= dx^2+dy^2.
    let select = |t: f64, xo: (f64, f64), hist_o: &[Ver], cur: &mut i64| -> i64 {
        match sel {
            Sel::Cursor => {
                loop {
                    let nxt = *cur + 1;
                    if (nxt as usize) < hist_o.len() {
                        let v = &hist_o[nxt as usize];
                        let dtl = t - v.t;
                        if dtl >= 0.0 {
                            let (dx, dy) = (xo.0 - v.x, xo.1 - v.y);
                            if (c * dtl) * (c * dtl) >= dx * dx + dy * dy { *cur = nxt; continue; }
                        }
                    }
                    break;
                }
                *cur
            }
            Sel::Brute => {
                let mut k: i64 = -1;
                for (i, v) in hist_o.iter().enumerate() {
                    let dtl = t - v.t;
                    if dtl >= 0.0 {
                        let (dx, dy) = (xo.0 - v.x, xo.1 - v.y);
                        if (c * dtl) * (c * dtl) >= dx * dx + dy * dy { k = i as i64; }
                    }
                }
                k
            }
        }
    };

    // acceleration on body at (xo) from source with history hist_o, at time t.
    // other_now = the source's position at t (for the instantaneous control).
    let force = |t: f64, xo: (f64, f64), other_now: (f64, f64), hist_o: &[Ver], cur: &mut i64| -> (f64, f64) {
        match law {
            Law::Inst => {
                let (dx, dy) = (other_now.0 - xo.0, other_now.1 - xo.1);
                let r2 = dx * dx + dy * dy;
                let f = 0.5 / (r2 * r2.sqrt());
                (f * dx, f * dy)
            }
            Law::Ret => {
                let mut s = (xo.0 - hist_o.last().unwrap().x).hypot(xo.1 - hist_o.last().unwrap().y) / c;
                for _ in 0..60 {
                    let (px, py) = interp_path(hist_o, t - s);
                    let s2 = (xo.0 - px).hypot(xo.1 - py) / c;
                    if (s2 - s).abs() < 1e-14 { s = s2; break; }
                    s = s2;
                }
                let (px, py) = interp_path(hist_o, t - s);
                let (dx, dy) = (px - xo.0, py - xo.1);
                let r2 = dx * dx + dy * dy;
                let f = 0.5 / (r2 * r2.sqrt());
                (f * dx, f * dy)
            }
            Law::News | Law::News0 => {
                let k = if law == Law::News { select(t, xo, hist_o, cur).max(0) as usize } else { 0 };
                let (px, py) = kepler_pos(&hist_o[k], t, mu);
                let (dx, dy) = (px - xo.0, py - xo.1);
                let r2 = dx * dx + dy * dy;
                let f = 0.5 / (r2 * r2.sqrt());
                (f * dx, f * dy)
            }
        }
    };

    let (mut aax, mut aay) = force(t, (ax, ay), (bx, by), &hist_b, &mut cur_a);
    let (mut abx, mut aby) = force(t, (bx, by), (ax, ay), &hist_a, &mut cur_b);
    for step in 0..n_steps {
        // velocity Verlet; versions are recorded only at boundaries where
        // (x, v) are consistent, so every Kepler extrapolation starts exact.
        let (nax_, nay_, nbx_, nby_) = (ax + avx * dt + 0.5 * aax * dt * dt,
                                         ay + avy * dt + 0.5 * aay * dt * dt,
                                         bx + bvx * dt + 0.5 * abx * dt * dt,
                                         by + bvy * dt + 0.5 * aby * dt * dt);
        let t_new = t + dt;
        ax = nax_; ay = nay_; bx = nbx_; by = nby_;
        let (nax, nay) = force(t_new, (ax, ay), (bx, by), &hist_b, &mut cur_a);
        let (nbx, nby) = force(t_new, (bx, by), (ax, ay), &hist_a, &mut cur_b);
        avx += 0.5 * (aax + nax) * dt; avy += 0.5 * (aay + nay) * dt;
        bvx += 0.5 * (abx + nbx) * dt; bvy += 0.5 * (aby + nby) * dt;
        t = t_new;
        hist_a.push(Ver { t, x: ax, y: ay, vx: avx, vy: avy });
        hist_b.push(Ver { t, x: bx, y: by, vx: bvx, vy: bvy });
        aax = nax; aay = nay; abx = nbx; aby = nby;

        if law == Law::News && sel == Sel::Cursor && step % 20 == 0 {
            // independent brute check of the selection + lag statistics
            let mut d = -1i64;
            for (i, v) in hist_b.iter().enumerate() {
                let dtl = t - v.t;
                if dtl >= 0.0 {
                    let (dx, dy) = (ax - v.x, ay - v.y);
                    if (c * dtl) * (c * dtl) >= dx * dx + dy * dy { d = i as i64; }
                }
            }
            if d != cur_a { sel_diff += 1; }
            sel_checks += 1;
            let newest = hist_b.len() as i64 - 1;
            lag_sum += (newest - cur_a) as f64; lag_n += 1;
            lag_max = lag_max.max(newest - cur_a);
        }
        if unbound_at.is_none() && step % 10 == 0 {
            let (rx, ry, vx, vy) = (bx - ax, by - ay, bvx - avx, bvy - avy);
            let en = 0.5 * (vx * vx + vy * vy) - mu / (rx * rx + ry * ry).sqrt();
            if en >= 0.0 { unbound_at = Some(t / period); }
        }
    }
    let (rx, ry, vx, vy) = (bx - ax, by - ay, bvx - avx, bvy - avy);
    let r = (rx * rx + ry * ry).sqrt();
    let v2 = vx * vx + vy * vy;
    let en = 0.5 * v2 - mu / r;
    let a_fin = -mu / (2.0 * en);
    let exx = (v2 - mu / r) * rx - (rx * vx + ry * vy) * vx;
    let eyy = (v2 - mu / r) * ry - (rx * vx + ry * vy) * vy;
    let ecc = (exx * exx + eyy * eyy).sqrt() / mu;
    let e0rel = -0.5f64;
    LapResult {
        unbound_at, dE: (en - e0rel) / e0rel.abs(), a_drift: (a_fin - 1.0).abs(), ecc,
        sel_diff, sel_checks,
        lag_mean: if lag_n > 0 { lag_sum / lag_n as f64 } else { 0.0 }, lag_max,
        bits: [ax.to_bits(), ay.to_bits(), avx.to_bits(), avy.to_bits(),
               bx.to_bits(), by.to_bits(), bvx.to_bits(), bvy.to_bits()],
    }
}

fn cmd_laplace() {
    let (n_orbits, spo) = (60usize, 400usize);
    println!("== Laplace control through the cursor (equal-mass binary, c lowered so v_orb/c = beta) ==");
    println!("{} steps/orbit, {} orbits; 'unbound' = relative energy >= 0; versions every step\n", spo, n_orbits);
    for &beta in &[0.1f64, 0.3f64, 0.9f64] {
        for (lname, law) in [("inst", Law::Inst), ("ret ", Law::Ret), ("news", Law::News), ("ns0 ", Law::News0)] {
            let r = laplace_run(law, Sel::Cursor, beta, n_orbits, spo);
            println!("beta {:>3}: {} unbound_at {:>6}  |dE| {:>9.3e}  |a-1| {:>9.3e}  e_fin {:>7.4}",
                beta, lname,
                r.unbound_at.map(|o| format!("{:.1}", o)).unwrap_or_else(|| "-".into()),
                r.dE, r.a_drift, r.ecc);
        }
        if beta == 0.1 {
            for &spo2 in &[100usize, 400, 1600, 6400] {
                let r = laplace_run(Law::News0, Sel::Cursor, 0.1, 60, spo2);
                println!("ns0 cadence check: {:>5} steps/orbit -> unbound_at {} |dE| {:.3e}",
                    spo2, r.unbound_at.map(|o| format!("{:.2}", o)).unwrap_or_else(|| "-".into()), r.dE);
            }
        }
        let r1 = laplace_run(Law::News, Sel::Cursor, beta, n_orbits, spo);
        let r2 = laplace_run(Law::News, Sel::Brute, beta, n_orbits, spo);
        let bits_eq = r1.bits == r2.bits;
        println!("beta {:>3}: news cursor-vs-brute: sel mismatches {}/{}  final state bit-identical: {}  lag mean {:>6.1} versions (max {})\n",
            beta, r1.sel_diff, r1.sel_checks, bits_eq, r1.lag_mean, r1.lag_max);
    }
}

// ---------------- ghost ----------------
fn cmd_ghost() {
    println!("== ghost memory per scale: retention = influence radius / c =\n   how long a source's pre-news path ('ghost') is still felt by someone ==");
    let au_c = 499.0;   // s
    let pc_c = 3.26;    // yr
    let kpc_c = 3260.0; // yr
    println!("{:>36}: {:>12}", "Earth doll   (r_H ~ 0.01 AU)", format!("{:.0} s", 0.01 * au_c));
    println!("{:>36}: {:>12}", "Jupiter doll (r_H ~ 0.35 AU)", format!("{:.0} s", 0.35 * au_c));
    println!("{:>36}: {:>12}", "Sun doll     (R    ~ 50 AU)", format!("{:.1} h", 50.0 * au_c / 3600.0));
    println!("{:>36}: {:>12}", "a star, individually (r_H ~ 1 pc)", format!("{:.1} yr", pc_c));
    println!("{:>36}: {:>12}", "galaxy cell, consumers at 1 kpc", format!("{:.0} yr", kpc_c));
    println!("{:>36}: {:>12}", "galaxy cell, consumers at 8 kpc", format!("{:.0} yr", 8.0 * kpc_c));
    println!("\nnews-only history per source = 24 B (t,x,y for the cone test) x depth + 16 B tube (shared)\n\
              + 4 B cursor per (body, source) pair; depth = news events inside the retention window.");
    println!("  star system: thrust/contact/rebind news ~ 0 in hours => depth ~1 => ~40 B/source.");
    println!("  every-step ring (a237 probe policy): 16 B x cadence x (light time in orbits) per source.");
    println!("  galaxy: cell-cell news ~ 1/(5e8 yr); retention 3e3..2.6e4 yr => alive ghosts ~ 1e-5..1e-4/cell.");
    println!("\nwhat the galaxy case requires: the ghost must be a GENERATOR — the cell's orbital program\n\
              in the smooth galactic field, advanced by addition (zero kicks). A stepped ghost would\n\
              cost a second body per news event for 1e4..1e5 yr. Ghost fields enter as aggregate\n\
              multipole differences (old program - new program), shrinking to zero as cones pass;\n\
              ghost-of-ghost branches are second order in the news size and pruned at retention.");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    match args.get(1).map(|s| s.as_str()) {
        Some("exact") => cmd_exact(),
        Some("cost") => cmd_cost(),
        Some("burst") => cmd_burst(),
        Some("laplace") => cmd_laplace(),
        Some("ghost") => cmd_ghost(),
        _ => println!("usage: cursor exact|cost|burst|laplace|ghost"),
    }
}
