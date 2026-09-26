//! Interactive stdin playground for the H0042 laboratory `advance_patch` map.
//!
//! The native observatory default world plays the same map. This example is the
//! headless stdin tool.
//!
//! ```sh
//! CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never cargo run -p emergent-law-lab --example playground --offline --locked
//! ```

use emergent_law_lab::{
    advance_patch, dt_q, inspect, laboratory, q, EvolvingPatchError, KernelEvent, PatchSegment,
    PatchState, PATCH_LAW_ID, Q,
};
use std::io::{self, BufRead, IsTerminal, Write};

const ID_A: u64 = 1;
const ID_B: u64 = 2;
const SHIP_X0: i128 = 4;
const MINKOWSKI_DT: f64 = 1.0 / 16.0;

fn main() {
    print_banner();
    match run() {
        Ok(()) => {}
        Err(err) => {
            eprintln!("playground: {err}");
            std::process::exit(1);
        }
    }
}

fn run() -> Result<(), EvolvingPatchError> {
    let mut session = Session::new(false)?;
    let stdin = io::stdin();
    let mut stdout = io::stdout();
    let interactive = stdin.is_terminal();
    let mut lines = stdin.lock().lines();
    let mut saw_command = false;

    loop {
        if interactive {
            print!("patch> ");
            stdout.flush().ok();
        }
        let line = match lines.next() {
            None => break,
            Some(Ok(line)) => line,
            Some(Err(err)) => {
                eprintln!("read error: {err}");
                break;
            }
        };
        let trimmed = line.trim();
        if trimmed.is_empty() {
            continue;
        }
        saw_command = true;
        if !dispatch(&mut session, trimmed)? {
            return Ok(());
        }
    }

    if !saw_command {
        eof_smoke()?;
    }
    Ok(())
}

struct Session {
    changed: bool,
    state: PatchState,
}

impl Session {
    fn new(changed: bool) -> Result<Self, EvolvingPatchError> {
        Ok(Self {
            changed,
            state: laboratory(changed)?,
        })
    }

    fn reset(&mut self, changed: bool) -> Result<(), EvolvingPatchError> {
        *self = Self::new(changed)?;
        Ok(())
    }

    fn goto(&mut self, t: Q) -> Result<(), EvolvingPatchError> {
        self.state = laboratory(self.changed)?;
        self.state = advance_patch(&self.state, t)?;
        Ok(())
    }

    fn step(&mut self) -> Result<(), EvolvingPatchError> {
        let target = self.state.time + dt_q();
        self.state = advance_patch(&self.state, target)?;
        Ok(())
    }
}

fn dispatch(session: &mut Session, line: &str) -> Result<bool, EvolvingPatchError> {
    let mut parts = line.split_whitespace();
    let cmd = parts.next().unwrap_or("").to_ascii_lowercase();
    match cmd.as_str() {
        "help" | "h" => print_help(),
        "status" => print_status(&session.state, session.changed),
        "step" => {
            session.step()?;
            print_observables(&session.state, session.changed);
        }
        "goto" => {
            let Some(token) = parts.next() else {
                eprintln!("usage: goto T   (examples: 1/8, 1/16, 3/16, 0, 1)");
                return Ok(true);
            };
            match parse_tick(token) {
                Ok(t) => {
                    if let Err(err) = session.goto(t) {
                        eprintln!("goto {token}: {err}");
                    } else {
                        print_observables(&session.state, session.changed);
                    }
                }
                Err(err) => eprintln!("{err}"),
            }
        }
        "baseline" => {
            session.reset(false)?;
            println!("reset to P0  laboratory(false)  A μ stays 1");
            print_status(&session.state, session.changed);
        }
        "change" => {
            session.reset(true)?;
            println!("reset to PΔ  laboratory(true)  A μ 1→2 at t=0");
            print_status(&session.state, session.changed);
        }
        "compare" => print_compare(session.state.time)?,
        "ascii" => print_ascii(&session.state),
        "quit" | "q" | "exit" => return Ok(false),
        _ => {
            eprintln!("unknown command {cmd:?} — type help");
        }
    }
    Ok(true)
}

fn eof_smoke() -> Result<(), EvolvingPatchError> {
    println!("(EOF: help, status at t=0, then compare at t=1/8)");
    print_help();
    let genesis = laboratory(false)?;
    print_status(&genesis, false);
    print_compare(q(1, 8))?;
    Ok(())
}

fn print_banner() {
    println!(
        "H0042 laboratory patch  {PATCH_LAW_ID}  — not production gravity."
    );
    println!("Map: advance_patch on two rest masses, one test ship, one post-cone ray, one clock.");
    println!("G2 stays FAIL. Type help.");
    println!();
}

fn print_help() {
    println!("Commands:");
    println!("  help       this text");
    println!("  status     time, A/B μ and positions, ship, clock τ, ray, P0 vs PΔ");
    println!("  step       one admitted tick (dt = {})", fmt_q(dt_q()));
    println!("  goto T     advance_patch to tick T  (1/8, 1/16, 3/16, integers)");
    println!("  baseline   reset laboratory(false) — P0, A μ stays 1");
    println!("  change     reset laboratory(true)  — PΔ, A μ 1→2 at t=0");
    println!("  compare    P0 vs PΔ at current time (both worlds run to that t)");
    println!("  ascii      1D sketch A(~0), ship(~4), B(~8); receiver at (4,4)");
    println!("  quit       exit");
}

fn print_status(p: &PatchState, changed: bool) {
    let world = if changed { "PΔ" } else { "P0" };
    let origin = if changed {
        "changed laboratory(true): A μ 1→2 at t=0"
    } else {
        "baseline laboratory(false)"
    };
    println!("status  t={}  {world}  {origin}", fmt_q(p.time));
    if let Some(a) = last_source(p, ID_A) {
        println!(
            "  A  μ={}  pos=({}, {})  v=({:.6e}, {:.6e})",
            fmt_q(a.mu),
            fmt_q(a.position[0]),
            fmt_q(a.position[1]),
            a.velocity[0],
            a.velocity[1]
        );
    }
    if let Some(b) = last_source(p, ID_B) {
        println!(
            "  B  μ={}  pos=({}, {})  v=({:.6e}, {:.6e})",
            fmt_q(b.mu),
            fmt_q(b.position[0]),
            fmt_q(b.position[1]),
            b.velocity[0],
            b.velocity[1]
        );
    }
    println!(
        "  ship  pos=({}, {})  v=({:.6e}, {:.6e})",
        fmt_q(p.ship.position[0]),
        fmt_q(p.ship.position[1]),
        p.ship.velocity[0],
        p.ship.velocity[1]
    );
    println!(
        "  clock τ={}  ≈ {:.12}",
        fmt_q(p.clock.tau),
        as_f64(p.clock.tau)
    );
    match p.ray.as_ref() {
        None => println!("  ray  missing"),
        Some(ray) => {
            let delivery = match ray.tick_delivery {
                Some(tick) => format!("delivered at t={}", fmt_q(tick)),
                None if p.time < ray.emit_time => "scheduled, not yet emitted".into(),
                None => "in flight, delivery pending".into(),
            };
            println!(
                "  ray  emit t={} from ({}, {}) → receiver ({}, {})",
                fmt_q(ray.emit_time),
                fmt_q(ray.emit_position[0]),
                fmt_q(ray.emit_position[1]),
                fmt_q(ray.receiver[0]),
                fmt_q(ray.receiver[1])
            );
            println!(
                "       dt={:.12}  affine_arrival={:.12}  {delivery}",
                ray.coordinate_dt, ray.affine_arrival
            );
        }
    }
    let event = KernelEvent {
        time: p.time,
        position: p.ship.position,
    };
    match inspect(p, event) {
        Ok(field) => println!(
            "  inspect Φ={:.12}  ξ=({:.6e}, {:.6e})",
            field.phi, field.xi[0], field.xi[1]
        ),
        Err(err) => println!("  inspect failed: {err}"),
    }
}

fn print_observables(p: &PatchState, changed: bool) {
    let world = if changed { "PΔ" } else { "P0" };
    println!("observables at t={}  {world}", fmt_q(p.time));
    let rest = p.ship.position == [q(SHIP_X0, 1), q(0, 1)]
        && p.ship.velocity[0] == 0.0
        && p.ship.velocity[1] == 0.0;
    if rest {
        println!("  ship  still at rest at x=4");
    } else {
        println!(
            "  ship  moved to ({}, {})  v=({:.6e}, {:.6e})",
            fmt_q(p.ship.position[0]),
            fmt_q(p.ship.position[1]),
            p.ship.velocity[0],
            p.ship.velocity[1]
        );
    }

    match p.ray.as_ref() {
        None => println!("  light  no ray in P"),
        Some(ray) if p.time < ray.emit_time => {
            println!(
                "  light  not yet emitted (scheduled t={}); Minkowski 4/c = 1/16",
                fmt_q(ray.emit_time)
            );
        }
        Some(ray) => {
            let vs = vs_minkowski(ray.coordinate_dt);
            let delivery = match ray.tick_delivery {
                Some(tick) => format!("delivered at t={}", fmt_q(tick)),
                None => "in flight".into(),
            };
            println!(
                "  light  dt={:.12} vs Minkowski 4/c=1/16={MINKOWSKI_DT}  ({vs}; {delivery})",
                ray.coordinate_dt
            );
        }
    }

    println!(
        "  clock  τ={}  ≈ {:.12}",
        fmt_q(p.clock.tau),
        as_f64(p.clock.tau)
    );
}

fn print_compare(t: Q) -> Result<(), EvolvingPatchError> {
    let p0 = advance_patch(&laboratory(false)?, t)?;
    let pd = advance_patch(&laboratory(true)?, t)?;
    println!(
        "compare at t={}  P0 = laboratory(false)  PΔ = laboratory(true)",
        fmt_q(t)
    );
    compare_row("", "P0 baseline", "PΔ  A μ 1→2 at t=0");
    compare_row(
        "ship x",
        &fmt_q(p0.ship.position[0]),
        &fmt_q(pd.ship.position[0]),
    );
    compare_row(
        "ship y",
        &fmt_q(p0.ship.position[1]),
        &fmt_q(pd.ship.position[1]),
    );
    compare_row(
        "ship vx",
        &format!("{:.6e}", p0.ship.velocity[0]),
        &format!("{:.6e}", pd.ship.velocity[0]),
    );
    compare_row(
        "ship vy",
        &format!("{:.6e}", p0.ship.velocity[1]),
        &format!("{:.6e}", pd.ship.velocity[1]),
    );
    let (dt0, vs0, del0) = ray_cells(&p0);
    let (dtd, vsd, deld) = ray_cells(&pd);
    compare_row("light dt", &dt0, &dtd);
    compare_row("vs 4/c", &vs0, &vsd);
    compare_row("delivery", &del0, &deld);
    compare_row("τ", &fmt_q(p0.clock.tau), &fmt_q(pd.clock.tau));
    compare_row(
        "τ ≈",
        &format!("{:.12}", as_f64(p0.clock.tau)),
        &format!("{:.12}", as_f64(pd.clock.tau)),
    );
    println!(
        "  Minkowski 4/c = 1/16 = {MINKOWSKI_DT}; a later dt is a Shapiro delay, not a frozen magnitude."
    );
    Ok(())
}

fn compare_row(label: &str, left: &str, right: &str) {
    println!("  {label:<10} {left:<28} {right}");
}

fn print_ascii(p: &PatchState) {
    const W: usize = 41;
    const X0: f64 = -0.5;
    const X1: f64 = 8.5;
    let mut buf = vec![b'-'; W];
    let mut place = |x: f64, mark: u8| {
        let t = (x - X0) / (X1 - X0);
        let i = (t * (W - 1) as f64).round().clamp(0.0, (W - 1) as f64) as usize;
        buf[i] = mark;
    };
    if let Some(a) = last_source(p, ID_A) {
        place(as_f64(a.position[0]), b'A');
    }
    if let Some(b) = last_source(p, ID_B) {
        place(as_f64(b.position[0]), b'B');
    }
    place(as_f64(p.ship.position[0]), b'S');
    println!("ascii  x-axis  A(~0)  ship S(~4)  B(~8); marks from live P");
    println!("  {}", String::from_utf8_lossy(&buf));
    println!("  0                   4                   8");
    println!(
        "  ship y={}  receiver sits at (4, 4), off this line",
        fmt_q(p.ship.position[1])
    );
}

fn last_source(p: &PatchState, id: u64) -> Option<&PatchSegment> {
    p.sources
        .iter()
        .find(|source| source.id == id)
        .and_then(|source| source.segments.last())
}

fn ray_cells(p: &PatchState) -> (String, String, String) {
    match p.ray.as_ref() {
        None => ("missing".into(), "missing".into(), "missing".into()),
        Some(ray) if p.time < ray.emit_time => (
            "not emitted".into(),
            "n/a".into(),
            format!("scheduled t={}", fmt_q(ray.emit_time)),
        ),
        Some(ray) => {
            let dt = format!("{:.12}", ray.coordinate_dt);
            let delivery = match ray.tick_delivery {
                Some(tick) => format!("t={}", fmt_q(tick)),
                None => "pending".into(),
            };
            (dt, vs_minkowski(ray.coordinate_dt).into(), delivery)
        }
    }
}

fn vs_minkowski(dt: f64) -> &'static str {
    if dt > MINKOWSKI_DT {
        "longer than Minkowski"
    } else if dt < MINKOWSKI_DT {
        "shorter than Minkowski"
    } else {
        "equal to Minkowski"
    }
}

fn parse_tick(token: &str) -> Result<Q, String> {
    if let Some((n, d)) = token.split_once('/') {
        let n = parse_i128(n.trim())?;
        let d = parse_i128(d.trim())?;
        if d == 0 {
            return Err("goto: denominator cannot be 0".into());
        }
        Ok(q(n, d))
    } else {
        Ok(q(parse_i128(token)?, 1))
    }
}

fn parse_i128(token: &str) -> Result<i128, String> {
    token
        .parse()
        .map_err(|_| format!("goto: not a tick {token:?} (try 1/8, 1/16, 3/16, 0)"))
}

fn fmt_q(value: Q) -> String {
    if *value.denom() == 1 {
        format!("{}", value.numer())
    } else {
        format!("{}/{}", value.numer(), value.denom())
    }
}

fn as_f64(value: Q) -> f64 {
    *value.numer() as f64 / *value.denom() as f64
}
