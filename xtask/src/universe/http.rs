//! The localhost page and its one route, after `xtask fly`: mutations come only from this page's
//! same-origin JSON fetch; the listener binds IPv4 loopback only.
use super::session::Session;
use serde_json::json;
use std::{
    io::{Read, Write},
    net::{TcpListener, TcpStream},
    os::fd::AsRawFd,
    sync::atomic::{AtomicBool, Ordering},
    time::{Duration, Instant},
};

/// Set by SIGINT, SIGTERM and SIGHUP: the server leaves its loop, and the flight is written on the way out. A second signal
/// while it writes ends the process at once.
static STOP: AtomicBool = AtomicBool::new(false);

extern "C" fn on_signal(_: libc::c_int) {
    if STOP.swap(true, Ordering::SeqCst) {
        // SAFETY: _exit is async-signal-safe.
        unsafe { libc::_exit(130) };
    }
}

fn catch_signals() {
    for sig in [libc::SIGINT, libc::SIGTERM, libc::SIGHUP] {
        // SAFETY: the handler only touches an atomic and calls _exit.
        unsafe { libc::signal(sig, on_signal as extern "C" fn(libc::c_int) as libc::sighandler_t) };
    }
}

fn panic_text(p: &(dyn std::any::Any + Send)) -> String {
    p.downcast_ref::<&str>().map(|s| s.to_string()).or_else(|| p.downcast_ref::<String>().cloned()).unwrap_or_else(|| "(no message)".into())
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
    println!("W/up thrust · S/down reverse · A D / left right turn · space cuts thrust · 1-9 or + - throttle · [ ] halve and double the time factor · M map/sky");
    if s.recording() {
        println!("recording the flight: written at every decision and every 10 s, and at exit, loss and restart; replay it with --replay <file>, all of them with --replay-all");
    }
    catch_signals();
    let mut last = Instant::now();
    loop {
        // Wait for a request, looking up from time to time at whether the process was asked to leave.
        let mut fds = [libc::pollfd { fd: listener.as_raw_fd(), events: libc::POLLIN, revents: 0 }];
        // SAFETY: one valid pollfd for the listener's descriptor.
        let ready = unsafe { libc::poll(fds.as_mut_ptr(), 1, 200) };
        if STOP.load(Ordering::SeqCst) {
            break;
        }
        if ready <= 0 {
            continue;
        }
        let (mut stream, _) = listener.accept()?;
        let response = (|| -> crate::Result<(String, Vec<u8>)> {
            let (line, body) = receive(&mut stream)?;
            let mut words = line.split_whitespace();
            let (method, path) = (words.next().unwrap_or(""), words.next().unwrap_or("").split('?').next().unwrap_or(""));
            match (method, path) {
                ("GET", "/") => Ok(("text/html; charset=utf-8".into(), include_bytes!("page.html").to_vec())),
                ("GET", "/config") => Ok(("application/json".into(), serde_json::to_vec(&s.config())?)),
                ("GET", "/log") => Ok(("application/json".into(), serde_json::to_vec_pretty(&s.log())?)),
                ("POST", "/restart") => {
                    if let Some(p) = s.finish("restart") {
                        println!("flight recorded: {}", p.display());
                    }
                    s = s.restarted()?;
                    last = Instant::now();
                    Ok(("application/json".into(), serde_json::to_vec(&s.config())?))
                }
                ("POST", "/frame") => {
                    let req: serde_json::Value = serde_json::from_slice(&body)?;
                    // The decision: the keys held and the throttle level, one logged word.
                    let keys = emergent_universe::thrust::word(req["keys"].as_u64().unwrap_or(0).min(15) as u8, req["throttle"].as_u64().unwrap_or(0).min(15) as u8);
                    if let Some(r) = req["rtf"].as_f64() {
                        if r.is_finite() && (0.01..=1e7).contains(&r) {
                            s.rtf = r;
                        }
                    }
                    let dt = last.elapsed().as_secs_f64().min(0.1);
                    last = Instant::now();
                    // An engine panic is a bug the player found: the inputs so far are its reproduction. Write them, then die as before.
                    let stepped = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| s.step(Some(keys), dt)));
                    let (v, ms) = match stepped {
                        Ok(r) => r?,
                        Err(p) => {
                            let message = panic_text(&*p);
                            if let Some(path) = s.record_panic(&message) {
                                eprintln!("flight recorded: {} (the engine panicked: {message})", path.display());
                            }
                            std::panic::resume_unwind(p);
                        }
                    };
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
    if let Some(p) = s.finish("exit") {
        println!("flight recorded: {}", p.display());
    }
    Ok(0)
}
