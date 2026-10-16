//! `std`-only localhost server: GET only, read-only, loopback. `/frame` is a pure function of the
//! scene and the query (`w,h,cx,cy,scale,t`); the server holds no session and decides nothing.
use super::draw::{FrameStats, Opts, Renderer, View};
use super::scene::Scene;
use serde_json::{json, Value};
use std::{
    io::{Read, Write},
    net::{TcpListener, TcpStream},
    time::Duration,
};

/// World extent shown by default: the whole galaxy (orbits reach a few 10⁴ M).
pub(super) const R_FAR: f64 = 22000.0;

pub(super) fn stats_json(st: &FrameStats, v: &View) -> Value {
    let ns = st.total_ms * 1e6;
    json!({
        "w": v.w, "h": v.h, "t": v.t.to_string(), "scale": v.scale,
        "samples": st.samples, "tube_samples": st.tube_samples, "fam_samples": st.fam_samples,
        "materialized": st.materialized, "tubes_in_range": st.tubes_in_range,
        "groups_in_range": st.groups_in_range, "stride": st.stride, "m_max": st.m_max,
        "ships_in_view": st.ships_in_view,
        "plan_ms": st.plan_ms, "splat_ms": st.splat_ms, "tone_ms": st.tone_ms,
        "total_ms": st.total_ms, "cpu_ms": st.cpu_ms,
        "ns_per_sample": if st.samples > 0 { ns / st.samples as f64 } else { 0.0 },
        "ns_per_ship_in_view": if st.ships_in_view > 0.0 { ns / st.ships_in_view } else { 0.0 },
    })
}

pub(super) fn config_json(scene: &Scene, threads: usize) -> Value {
    let s = &scene.stats;
    json!({
        "ships": scene.total_ships.to_string(), "tubes": scene.tubes.len(), "families": scene.families.len(),
        "keys_compiled": s.compiled, "lattice_orbits": s.cells_valid, "lookups": s.lookups, "memo_hit_rate": s.hit_rate,
        "ships_per_compile": s.ships_per_compile, "build_s": s.total_wall_s,
        "threads": threads, "r_far": R_FAR, "seed": scene.cfg.seed.to_string(),
    })
}

/// Parse the query into a view, refusing values outside the supported range.
pub(super) fn view_of(query: &str) -> Result<View, String> {
    let mut v = View { w: 960, h: 540, cx: 0.0, cy: 0.0, scale: 2.0 * R_FAR / 540.0, t: 0 };
    for kv in query.split('&').filter(|s| !s.is_empty()) {
        let (k, val) = kv.split_once('=').ok_or("malformed query")?;
        let f = |x: &str| x.parse::<f64>().ok().filter(|f| f.is_finite()).ok_or_else(|| format!("bad number for {k}"));
        match k {
            "w" => v.w = val.parse().map_err(|_| "bad w")?,
            "h" => v.h = val.parse().map_err(|_| "bad h")?,
            "cx" => v.cx = f(val)?,
            "cy" => v.cy = f(val)?,
            "scale" => v.scale = f(val)?,
            "t" => v.t = val.parse().map_err(|_| "bad t")?,
            _ => {}
        }
    }
    if !(16..=2048).contains(&v.w) || !(16..=2048).contains(&v.h) {
        return Err("w and h must be in 16..=2048".into());
    }
    if !(0.01..=1e5).contains(&v.scale) || v.cx.abs() > 1e6 || v.cy.abs() > 1e6 || v.t > 1 << 62 {
        return Err("view outside range".into());
    }
    Ok(v)
}

fn crc32(data: &[u8], mut c: u32) -> u32 {
    c = !c;
    for &b in data {
        c ^= b as u32;
        for _ in 0..8 {
            c = (c >> 1) ^ (0xEDB8_8320 & 0u32.wrapping_sub(c & 1));
        }
    }
    !c
}
/// An uncompressed (stored-block) grayscale PNG: enough to look at a frame with any viewer.
pub(super) fn png(w: usize, h: usize, gray: &[u8]) -> Vec<u8> {
    let mut raw = Vec::with_capacity((w + 1) * h);
    for row in gray.chunks(w) {
        raw.push(0);
        raw.extend_from_slice(row);
    }
    let mut z = vec![0x78, 0x01];
    let mut blocks = raw.chunks(65535).peekable();
    while let Some(b) = blocks.next() {
        z.push(u8::from(blocks.peek().is_none()));
        z.extend_from_slice(&(b.len() as u16).to_le_bytes());
        z.extend_from_slice(&(!(b.len() as u16)).to_le_bytes());
        z.extend_from_slice(b);
    }
    let (mut a, mut b) = (1u32, 0u32);
    for &x in &raw {
        a = (a + x as u32) % 65521;
        b = (b + a) % 65521;
    }
    z.extend_from_slice(&((b << 16) | a).to_be_bytes());
    let mut out = vec![0x89, b'P', b'N', b'G', 0x0D, 0x0A, 0x1A, 0x0A];
    let mut chunk = |kind: &[u8; 4], data: &[u8]| {
        out.extend_from_slice(&(data.len() as u32).to_be_bytes());
        out.extend_from_slice(kind);
        out.extend_from_slice(data);
        out.extend_from_slice(&crc32(data, crc32(kind, 0)).to_be_bytes());
    };
    let mut ihdr = Vec::new();
    ihdr.extend_from_slice(&(w as u32).to_be_bytes());
    ihdr.extend_from_slice(&(h as u32).to_be_bytes());
    ihdr.extend_from_slice(&[8, 0, 0, 0, 0]);
    chunk(b"IHDR", &ihdr);
    chunk(b"IDAT", &z);
    chunk(b"IEND", &[]);
    out
}

fn respond(stream: &mut TcpStream, status: &str, kind: &str, extra: &str, body: &[u8]) -> std::io::Result<()> {
    write!(
        stream,
        "HTTP/1.1 {status}\r\nContent-Type: {kind}\r\nContent-Length: {}\r\nCache-Control: no-store\r\nConnection: close\r\nX-Content-Type-Options: nosniff\r\n{extra}\r\n",
        body.len()
    )?;
    stream.write_all(body)
}

fn request_line(stream: &mut TcpStream) -> Result<String, String> {
    stream.set_read_timeout(Some(Duration::from_secs(2))).map_err(|e| e.to_string())?;
    stream.set_write_timeout(Some(Duration::from_secs(5))).map_err(|e| e.to_string())?;
    let mut bytes = Vec::new();
    let mut buf = [0u8; 4096];
    while !bytes.windows(4).any(|w| w == b"\r\n\r\n") {
        let n = stream.read(&mut buf).map_err(|e| e.to_string())?;
        if n == 0 || bytes.len() > 16384 {
            return Err("incomplete or oversized request".into());
        }
        bytes.extend_from_slice(&buf[..n]);
    }
    let head = String::from_utf8_lossy(&bytes);
    Ok(head.lines().next().unwrap_or("").to_string())
}

pub(super) fn serve(scene: &Scene, port: u16, threads: usize) -> crate::Result<u8> {
    let listener = TcpListener::bind(("127.0.0.1", port))?;
    println!(
        "Galaxy: http://127.0.0.1:{}/ · {} ships ({} tubes, {} families) · {} cycles · memo hit rate {:.4} · built in {:.2} s",
        listener.local_addr()?.port(),
        scene.total_ships,
        scene.tubes.len(),
        scene.families.len(),
        scene.stats.compiled,
        scene.stats.hit_rate,
        scene.stats.total_wall_s
    );
    println!("drag to pan · wheel to zoom · [ ] real-time factor · space pause · 0 reset");
    let mut renderer = Renderer::new();
    let mut out = Vec::new();
    for stream in listener.incoming() {
        let mut stream = stream?;
        let line = match request_line(&mut stream) {
            Ok(l) => l,
            Err(_) => continue,
        };
        let mut words = line.split_whitespace();
        let (method, target) = (words.next().unwrap_or(""), words.next().unwrap_or(""));
        let (path, query) = target.split_once('?').unwrap_or((target, ""));
        let result = match (method, path) {
            ("GET", "/") => respond(&mut stream, "200 OK", "text/html; charset=utf-8", "", include_bytes!("page.html")),
            ("GET", "/config") => respond(&mut stream, "200 OK", "application/json", "", &serde_json::to_vec(&config_json(scene, threads)).unwrap_or_default()),
            ("GET", "/frame") | ("GET", "/frame.png") => match view_of(query) {
                Ok(v) => {
                    let st = renderer.render(scene, &v, &Opts::for_size(v.w, v.h, threads), &mut out);
                    let stats = stats_json(&st, &v).to_string();
                    if path == "/frame" {
                        respond(&mut stream, "200 OK", "application/octet-stream", &format!("X-Galaxy: {stats}\r\nAccess-Control-Expose-Headers: X-Galaxy\r\n"), &out)
                    } else {
                        respond(&mut stream, "200 OK", "image/png", &format!("X-Galaxy: {stats}\r\n"), &png(v.w, v.h, &out))
                    }
                }
                Err(e) => respond(&mut stream, "400 Bad Request", "application/json", "", json!({"error": e}).to_string().as_bytes()),
            },
            _ => respond(&mut stream, "404 Not Found", "application/json", "", b"{\"error\":\"unknown route\"}"),
        };
        let _ = result;
    }
    Ok(0)
}
