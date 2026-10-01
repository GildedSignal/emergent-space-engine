//! The localhost page and its one route, after `xtask fly`: mutations come only from this page's
//! same-origin JSON fetch; the listener binds IPv4 loopback only.
use super::session::Session;
use serde_json::json;
use std::{
    io::{Read, Write},
    net::{TcpListener, TcpStream},
    time::{Duration, Instant},
};

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
    let line = head.lines().next().ok_or("missing request line")?.to_string();
    let length = head
        .lines()
        .find_map(|l| l.split_once(':').filter(|(k, _)| k.eq_ignore_ascii_case("content-length")).map(|(_, v)| v.trim().parse::<usize>()))
        .transpose()?
        .unwrap_or(0);
    if length > 65536 {
        return Err("request body exceeds 64 KiB".into());
    }
    if line.starts_with("POST ") {
        let json = head.lines().any(|l| l.split_once(':').is_some_and(|(k, v)| k.eq_ignore_ascii_case("content-type") && v.trim() == "application/json"));
        if !json {
            return Err("POST requires application/json".into());
        }
        if let Some(origin) = head.lines().find_map(|l| l.split_once(':').filter(|(k, _)| k.eq_ignore_ascii_case("origin")).map(|(_, v)| v.trim())) {
            let port = stream.local_addr()?.port();
            if origin != format!("http://127.0.0.1:{port}") && origin != format!("http://localhost:{port}") {
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

fn respond(stream: &mut TcpStream, status: &str, content_type: &str, body: &[u8]) -> std::io::Result<()> {
    write!(stream, "HTTP/1.1 {status}\r\nContent-Type: {content_type}\r\nContent-Length: {}\r\nCache-Control: no-store\r\nConnection: close\r\nX-Content-Type-Options: nosniff\r\n\r\n", body.len())?;
    stream.write_all(body)
}

pub(super) fn serve(mut s: Session, port: u16) -> crate::Result<u8> {
    let listener = TcpListener::bind(("127.0.0.1", port))?;
    println!("Universe: http://127.0.0.1:{}/ · seed {} · {}x game time · the star system, whole", listener.local_addr()?.port(), s.seed, s.rtf);
    println!("W/up thrust · S/down reverse · A D / left right turn · space cuts thrust · [ ] halve and double the time factor");
    let mut last = Instant::now();
    for stream in listener.incoming() {
        let mut stream = stream?;
        let response = (|| -> crate::Result<(String, Vec<u8>)> {
            let (line, body) = receive(&mut stream)?;
            let mut words = line.split_whitespace();
            let (method, path) = (words.next().unwrap_or(""), words.next().unwrap_or("").split('?').next().unwrap_or(""));
            match (method, path) {
                ("GET", "/") => Ok(("text/html; charset=utf-8".into(), include_bytes!("page.html").to_vec())),
                ("GET", "/config") => Ok(("application/json".into(), serde_json::to_vec(&json!({"seed": s.seed, "rtf": s.rtf}))?)),
                ("GET", "/log") => Ok(("application/json".into(), serde_json::to_vec_pretty(&s.log())?)),
                ("POST", "/frame") => {
                    let req: serde_json::Value = serde_json::from_slice(&body)?;
                    let keys = req["keys"].as_u64().unwrap_or(0).min(15) as u8;
                    if let Some(r) = req["rtf"].as_f64() {
                        if r.is_finite() && (0.01..=1e7).contains(&r) {
                            s.rtf = r;
                        }
                    }
                    let dt = last.elapsed().as_secs_f64().min(0.1);
                    last = Instant::now();
                    let (v, ms) = s.step(keys, dt)?;
                    Ok(("application/json".into(), serde_json::to_vec(&json!({"frame": v, "server_ms": ms, "dash": s.dash_json()}))?))
                }
                _ => Err("unknown route".into()),
            }
        })();
        match response {
            Ok((kind, body)) => {
                let _ = respond(&mut stream, "200 OK", &kind, &body);
            }
            Err(e) => {
                let _ = respond(&mut stream, "400 Bad Request", "application/json", &serde_json::to_vec(&json!({"error": e.to_string()}))?);
            }
        }
    }
    Ok(0)
}
