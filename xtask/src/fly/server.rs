use super::{
    flight::{Flight, Input, TPS},
    view,
};
use emergent_lattice::Stepper;
use serde::{Deserialize, Serialize};
use serde_json::json;
use std::{
    fs,
    io::{Read, Write},
    net::{TcpListener, TcpStream},
    time::{Duration, Instant},
};

#[derive(Serialize, Deserialize)]
struct Replay {
    version: String,
    seed: u64,
    inputs: Vec<Input>,
    horizon: i64,
    digest: String,
}
impl Replay {
    fn of(f: &Flight) -> Self {
        Self {
            version: "es-flight-v0".into(),
            seed: f.seed,
            inputs: f.inputs.clone(),
            horizon: f.core.tick(),
            digest: f.digest(),
        }
    }
    fn execute(&self) -> crate::Result<Flight> {
        if self.version != "es-flight-v0" {
            return Err("unknown flight version".into());
        }
        let mut f = Flight::new(self.seed);
        for i in &self.inputs {
            f.input(*i)?;
        }
        f.advance(self.horizon)?;
        if f.digest() != self.digest {
            return Err("replay digest mismatch".into());
        }
        Ok(f)
    }
}

#[derive(Deserialize)]
struct Request {
    tick: i64,
    inputs: Vec<Input>,
}

fn receive(stream: &mut TcpStream) -> crate::Result<(String, Vec<u8>)> {
    stream.set_read_timeout(Some(Duration::from_secs(2)))?;
    stream.set_write_timeout(Some(Duration::from_secs(2)))?;
    let mut bytes = Vec::new();
    let mut buf = [0u8; 8192];
    let head_end = loop {
        let n = stream.read(&mut buf)?;
        if n == 0 {
            return Err("incomplete HTTP request".into());
        }
        bytes.extend_from_slice(&buf[..n]);
        if bytes.len() > 65536 {
            return Err("request exceeds 64 KiB".into());
        }
        if let Some(p) = bytes.windows(4).position(|w| w == b"\r\n\r\n") {
            break p + 4;
        }
    };
    let head = std::str::from_utf8(&bytes[..head_end])?;
    let line = head
        .lines()
        .next()
        .ok_or("missing request line")?
        .to_string();
    let length = head
        .lines()
        .find_map(|l| {
            l.split_once(':')
                .filter(|(k, _)| k.eq_ignore_ascii_case("content-length"))
                .map(|(_, v)| v.trim().parse::<usize>())
        })
        .transpose()?
        .unwrap_or(0);
    if length > 65536 {
        return Err("request body exceeds 64 KiB".into());
    }
    // Mutations come only from this page's same-origin JSON fetch, never a form
    // or cross-origin request. The listener itself binds IPv4 loopback only.
    if line.starts_with("POST ") {
        let json = head.lines().any(|l| {
            l.split_once(':').is_some_and(|(k, v)| {
                k.eq_ignore_ascii_case("content-type") && v.trim() == "application/json"
            })
        });
        if !json {
            return Err("POST requires application/json".into());
        }
        if let Some(origin) = head.lines().find_map(|l| {
            l.split_once(':')
                .filter(|(k, _)| k.eq_ignore_ascii_case("origin"))
                .map(|(_, v)| v.trim())
        }) {
            let expected = format!("http://{}", stream.local_addr()?);
            if origin != expected {
                return Err("cross-origin request refused".into());
            }
        }
    }
    while bytes.len() < head_end + length {
        let n = stream.read(&mut buf)?;
        if n == 0 {
            return Err("incomplete HTTP body".into());
        }
        bytes.extend_from_slice(&buf[..n]);
    }
    Ok((line, bytes[head_end..head_end + length].to_vec()))
}

fn respond(
    stream: &mut TcpStream,
    status: &str,
    content_type: &str,
    body: &[u8],
) -> std::io::Result<()> {
    write!(stream,"HTTP/1.1 {status}\r\nContent-Type: {content_type}\r\nContent-Length: {}\r\nCache-Control: no-store\r\nConnection: close\r\nX-Content-Type-Options: nosniff\r\n\r\n",body.len())?;
    stream.write_all(body)
}

/// Validate the whole batch before mutating flight, including replay order.
fn step(f: &mut Flight, req: Request, c_scale: f64) -> crate::Result<Vec<u8>> {
    let mut previous = f.core.tick();
    if req.tick < previous || req.tick - previous > TPS * 30 || req.inputs.len() > 2048 {
        return Err("frame horizon or input batch outside limits".into());
    }
    for i in &req.inputs {
        if i.tick < previous || i.tick > req.tick || i.keys > 15 {
            return Err("unordered, future or invalid input".into());
        }
        previous = i.tick;
    }
    let start = Instant::now();
    for i in req.inputs {
        f.input(i)?;
    }
    f.advance(req.tick)?;
    let frame = view::frame(f, c_scale);
    Ok(serde_json::to_vec(
        &json!({"frame":frame,"server_ms":start.elapsed().as_secs_f64()*1000.}),
    )?)
}

pub(super) fn run(args: Vec<String>) -> crate::Result<u8> {
    let (mut seed, mut c_scale, mut port, mut rtf) = (1u64, 200_f64, 8787u16, 1_f64);
    let (mut replay, mut bench) = (None, false);
    let mut it = args.into_iter();
    while let Some(arg) = it.next() {
        match arg.as_str() {
            "--seed" => seed = it.next().ok_or("missing seed")?.parse()?,
            "--c-scale" => c_scale = it.next().ok_or("missing c-scale")?.parse()?,
            "--port" => port = it.next().ok_or("missing port")?.parse()?,
            "--rtf" => rtf = it.next().ok_or("missing rtf")?.parse()?,
            "--replay" => replay = Some(it.next().ok_or("missing replay path")?),
            "--bench" => bench = true,
            "--help" => {
                println!("fly [--seed N] [--c-scale UNITS_PER_SECOND] [--port 8787] [--rtf 1]\nfly --replay LOG.json\nfly --bench [--seed N] [--c-scale N]");
                return Ok(0);
            }
            _ => return Err(format!("unknown fly argument {arg}").into()),
        }
    }
    if !c_scale.is_finite()
        || !(0.01..=1e6).contains(&c_scale)
        || !rtf.is_finite()
        || !(0.01..=16.).contains(&rtf)
    {
        return Err("c-scale or real-time factor outside finite positive range".into());
    }
    if let Some(path) = replay {
        let r: Replay = serde_json::from_slice(&fs::read(path)?)?;
        let f = r.execute()?;
        println!("REPLAY PASS {} tick {}", f.digest(), f.core.tick());
        return Ok(0);
    }
    if bench {
        return benchmark(seed, c_scale);
    }
    let listener = TcpListener::bind(("127.0.0.1", port))?;
    println!("Fly: http://127.0.0.1:{}/ · seed {seed} · c {c_scale} units/s · {rtf}× coordinate real time",listener.local_addr()?.port());
    println!("W/up thrust · S/down reverse thrust · A/D or left/right turn · space cut thrust · download replay on page");
    let mut f = Flight::new(seed);
    for stream in listener.incoming() {
        let mut stream = stream?;
        let response = (|| -> crate::Result<(String, Vec<u8>)> {
            let (line, body) = receive(&mut stream)?;
            let mut words = line.split_whitespace();
            let method = words.next().unwrap_or("");
            let path = words.next().unwrap_or("").split('?').next().unwrap_or("");
            match (method, path) {
                ("GET", "/") => Ok((
                    "text/html; charset=utf-8".into(),
                    include_bytes!("page.html").to_vec(),
                )),
                ("GET", "/config") => Ok((
                    "application/json".into(),
                    serde_json::to_vec(
                        &json!({"seed":seed.to_string(),"c_scale":c_scale,"rtf":rtf,"tps":TPS,"tick":f.core.tick()}),
                    )?,
                )),
                ("GET", "/log") => Ok((
                    "application/json".into(),
                    serde_json::to_vec_pretty(&Replay::of(&f))?,
                )),
                ("POST", "/frame") => Ok((
                    "application/json".into(),
                    step(&mut f, serde_json::from_slice(&body)?, c_scale)?,
                )),
                _ => Err("unknown route".into()),
            }
        })();
        match response {
            Ok((kind, body)) => {
                let _ = respond(&mut stream, "200 OK", &kind, &body);
            }
            Err(e) => {
                let body = serde_json::to_vec(&json!({"error":e.to_string()}))?;
                let _ = respond(&mut stream, "400 Bad Request", "application/json", &body);
            }
        }
    }
    Ok(0)
}

fn benchmark(seed: u64, c_scale: f64) -> crate::Result<u8> {
    // Same step/gather/serialize pipeline as /frame. Browser paint and transport
    // are deliberately excluded and reported separately by the page's telemetry.
    let before = crate::measure::machine_state("before");
    let mut f = Flight::new(seed);
    let mut samples = Vec::new();
    for n in 1..=1200 {
        let tick = n * TPS / 60;
        let keys = if n == 1 {
            Some(1)
        } else if n == 300 {
            Some(9)
        } else if n == 600 {
            Some(0)
        } else {
            None
        };
        let inputs = keys
            .map(|keys| {
                vec![Input {
                    tick: f.core.tick(),
                    keys,
                }]
            })
            .unwrap_or_default();
        let start = Instant::now();
        let _ = step(&mut f, Request { tick, inputs }, c_scale)?;
        samples.push(start.elapsed().as_secs_f64() * 1000.);
    }
    samples.sort_by(f64::total_cmp);
    println!(
        "{}",
        json!({"scope":"Rust advance + gather + JSON only; no browser or HTTP", "frames":samples.len(),"seed":seed,"median_ms":crate::measure::percentile(&samples,0.5),"p99_ms":crate::measure::percentile(&samples,0.99),"max_ms":samples.last(),"contacts":f.core.log().contacts,"burns":f.burns,"digest":f.digest(),"machine_before":before,"machine_after":crate::measure::machine_state("after")})
    );
    Ok(0)
}
