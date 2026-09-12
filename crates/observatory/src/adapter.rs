//! Worker-owned canonical engine. The UI exchanges commands and bounded snapshots.
use crate::bridge::*;
use emergent_engine::{
    math::{r, Vec2},
    runtime::Payload,
    scenario, Command, Engine, WorkBudget,
};
use num_traits::ToPrimitive;
use std::{
    sync::{mpsc, Arc, RwLock},
    thread,
    time::Duration,
};

pub struct EngineBridge {
    sender: mpsc::Sender<UiCommand>,
    snapshot: Arc<RwLock<UiSnapshot>>,
}
impl EngineBridge {
    pub fn new() -> Self {
        let (sender, receiver) = mpsc::channel();
        let initial = UiSnapshot {
            capability_status: "STARTING ENGINE".into(),
            progress_label: "Reconstructing the laboratory universe…".into(),
            ..Default::default()
        };
        let snapshot = Arc::new(RwLock::new(initial));
        let shared = snapshot.clone();
        thread::Builder::new()
            .name("causal-engine".into())
            .spawn(move || run(receiver, shared))
            .expect("engine worker");
        Self { sender, snapshot }
    }
}
impl ObservatoryBridge for EngineBridge {
    fn snapshot(&self) -> UiSnapshot {
        self.snapshot.read().unwrap().clone()
    }
    fn command(&mut self, command: UiCommand) -> Result<(), String> {
        self.sender
            .send(command)
            .map_err(|_| "Engine worker unavailable".into())
    }
}

fn run(receiver: mpsc::Receiver<UiCommand>, shared: Arc<RwLock<UiSnapshot>>) {
    let mut engine = match scenario::observatory() {
        Ok(e) => e,
        Err(e) => {
            shared.write().unwrap().warning = Some(e.to_string());
            return;
        }
    };
    let mut mode = ViewMode::Diagnostic;
    let mut selected_extra = None;
    let mut pending = None;
    let mut warning = None;
    *shared.write().unwrap() = snapshot(&engine, mode, selected_extra, pending, warning.clone());
    loop {
        let mut dirty = false;
        let first = match receiver.recv_timeout(if pending.is_some() {
            Duration::from_millis(1)
        } else {
            Duration::from_millis(80)
        }) {
            Ok(c) => Some(c),
            Err(mpsc::RecvTimeoutError::Timeout) => None,
            Err(_) => return,
        };
        let commands = first.into_iter().chain(receiver.try_iter().take(31));
        for command in commands {
            dirty = true;
            warning = None;
            let result = (|| -> Result<(), String> {
                match command {
                    UiCommand::Advance { ticks } => {
                        pending = Some(
                            pending
                                .unwrap_or(engine.state.clock)
                                .checked_add(ticks as i128)
                                .ok_or("time overflow")?,
                        );
                    }
                    UiCommand::LookupIdentity { identity } => {
                        let id = identity
                            .trim()
                            .parse()
                            .map_err(|_| "Enter a numeric ship identity")?;
                        engine.decode(id).map_err(|e| e.to_string())?;
                        selected_extra = Some(id);
                    }
                    UiCommand::SetViewMode(m) => {
                        mode = m;
                    }
                    UiCommand::Navigate {
                        destination,
                        speed_fraction,
                    } => {
                        if !destination
                            .into_iter()
                            .chain([speed_fraction])
                            .all(f64::is_finite)
                            || !(0.0..1.0).contains(&speed_fraction)
                        {
                            return Err("Invalid navigation parameters".into());
                        }
                        let at = engine
                            .position(1, engine.state.clock)
                            .map_err(|e| e.to_string())?;
                        let dx = destination[0]
                            - at.x.to_f64().ok_or("coordinate exceeds display range")?;
                        let dy = destination[1]
                            - at.y.to_f64().ok_or("coordinate exceeds display range")?;
                        let norm = dx.hypot(dy);
                        if norm < 1e-8 {
                            return Err("Choose a destination away from the ship".into());
                        }
                        let scale = 1_048_576.0;
                        let velocity = Vec2 {
                            x: r((dx / norm * speed_fraction * scale).round() as i128)
                                / r(1_048_576),
                            y: r((dy / norm * speed_fraction * scale).round() as i128)
                                / r(1_048_576),
                        };
                        engine
                            .intervene(1, Command::SetVelocity { velocity })
                            .map_err(|e| e.to_string())?;
                        warning=Some("Heading committed. Laboratory navigation applies a controlled burn; fuel and autonomous arrival are not yet qualified.".into());
                    }
                    UiCommand::SendSignal { target_id } => {
                        engine
                            .intervene(
                                1,
                                Command::SendSignal {
                                    target: target_id,
                                    payload: Payload::Ping,
                                },
                            )
                            .map_err(|e| e.to_string())?;
                    }
                    UiCommand::Save { path } => {
                        engine.checkpoint(path).map_err(|e| e.to_string())?;
                    }
                    UiCommand::Load { path } => {
                        let restored = Engine::restore(path).map_err(|e| e.to_string())?;
                        restored
                            .decode(1)
                            .map_err(|_| "Archive has no observer identity 1")?;
                        engine = restored;
                        pending = None;
                        selected_extra = None;
                    }
                    UiCommand::Reset => {
                        engine = scenario::observatory().map_err(|e| e.to_string())?;
                        pending = None;
                        selected_extra = None;
                    }
                }
                Ok(())
            })();
            if let Err(e) = result {
                warning = Some(e);
            }
        }
        if let Some(target) = pending {
            match engine.advance(
                target,
                WorkBudget {
                    operations: 24,
                    max_events: 32,
                },
            ) {
                Ok(result) => {
                    if result.complete {
                        pending = None;
                    }
                }
                Err(e) => {
                    warning = Some(e.to_string());
                    pending = None;
                }
            }
            dirty = true;
        }
        if dirty {
            *shared.write().unwrap() =
                snapshot(&engine, mode, selected_extra, pending, warning.clone());
        }
    }
}

fn point(v: &Vec2) -> [f64; 2] {
    [v.x.to_f64().unwrap_or(0.0), v.y.to_f64().unwrap_or(0.0)]
}
fn snapshot(
    engine: &Engine,
    mode: ViewMode,
    extra: Option<u64>,
    pending: Option<i128>,
    warning: Option<String>,
) -> UiSnapshot {
    let mut warning = warning;
    let now = engine.state.clock;
    let mut ids = vec![1, 2, 3, 4, 5];
    if let Some(id) = extra {
        if !ids.contains(&id) {
            ids.push(id);
        }
    }
    let observations = if mode == ViewMode::HistoricalSensor {
        match engine.observe(1, now, &ids) {
            Ok(observations) => observations,
            Err(error) => {
                warning = Some(format!("Sensor query incomplete: {error}"));
                vec![]
            }
        }
    } else {
        vec![]
    };
    let mut bodies = Vec::new();
    for id in ids {
        let Ok(body) = engine.decode(id) else {
            continue;
        };
        let emission = if mode == ViewMode::HistoricalSensor && id != 1 {
            match observations.iter().find(|o| o.entity == id) {
                Some(o) => o.emission_tick,
                None => continue,
            }
        } else {
            now
        };
        let kind = match id {
            1 => BodyKind::Observer,
            2..=4 => BodyKind::Source,
            _ => BodyKind::Ship,
        };
        let radius = match id {
            3 => 34.,
            2 => 13.,
            4 => 7.,
            1 => 8.,
            _ => 5.,
        };
        let trace = if mode == ViewMode::Diagnostic {
            let start = 0.max(now - 500);
            (0..33)
                .map(|i| point(&body.at(start + (now - start) * i / 32)))
                .collect()
        } else {
            vec![]
        };
        bodies.push(UiBody{id,name:body.name.clone(),kind,position:point(&body.at(emission)),velocity:if mode==ViewMode::Diagnostic||id==1{point(&body.flow().velocity)}else{[0.,0.]},radius,
    mass_label:if mode==ViewMode::Diagnostic||id==1 {format!("{} canonical mass unit",body.mass)}else{"Not measured".into()},
    clock_label:if mode==ViewMode::Diagnostic||id==1 {format!("{:.3} proper ticks",body.proper_time(emission).ok().and_then(|x|x.to_f64()).unwrap_or(0.))}else{"Remote clock unmeasured".into()},
    sensor_age:if id==1{None}else{Some(format!("{} ticks ago",now-emission))},population:1,
    note:if id>=10_000{"Decoded on demand from an exact route family. Identity lookup changes no canonical state.".into()}else{match id{3=>"Finite-radius occluder in the inertial laboratory. Gravitational acceleration is not enabled.".into(),_=>"Canonical inertial worldline; sensor messages propagate at c = 1.".into()}},trace});
    }
    let events = engine
        .sorted_events()
        .into_iter()
        .rev()
        .filter(|e| {
            mode == ViewMode::Diagnostic
                || match e.kind.as_str() {
                    "signal_emitted" => e.subjects.first() == Some(&1),
                    "signal_arrived" => e.subjects.last() == Some(&1),
                    _ => e.subjects.contains(&1),
                }
        })
        .take(200)
        .map(|e| UiEvent {
            tick: e.tick,
            title: match e.kind.as_str() {
                "signal_emitted" => "Transmission dispatched",
                "signal_arrived" => "Signal received",
                "burn" => "Course changed",
                "contact" => "Contact detected",
                _ => &e.kind,
            }
            .into(),
            detail: format!(
                "{} · {}",
                e.subjects
                    .iter()
                    .map(|x| format!("#{x}"))
                    .collect::<Vec<_>>()
                    .join(" → "),
                e.detail.chars().take(55).collect::<String>()
            ),
            body_id: e.subjects.last().copied(),
        })
        .collect();
    let proper = engine
        .decode(1)
        .ok()
        .and_then(|b| b.proper_time(now).ok())
        .and_then(|q| q.to_f64())
        .unwrap_or(0.);
    UiSnapshot{time_ticks:now,time_per_tick:1.,time_unit:"canonical ticks".into(),distance_unit:"light-ticks".into(),observer_clock:format!("{proper:.3} proper ticks"),mode,bodies,events,
  conceptual_population:engine.logical_count().min(u64::MAX as u128)as u64,explicit_population:engine.state.bodies.len(),family_count:engine.state.families.len(),
  canonical_hash:engine.history_digest(now).unwrap_or_default(),law_name:"INERTIAL CAUSAL LAB · v1".into(),capability_status:"EXACT CAUSAL LABORATORY".into(),
  capability_detail:"Generator-native motion, causal signals, exact contact predicates and replay. Gravity candidates remain unqualified; population count is compressed addressable state, not a claim of integrated gravitational scale.".into(),
  progress_label:pending.map_or_else(||format!("Certified through tick {now}"),|target|format!("Computing to {target} · committed {now}")),
  can_advance:true,can_navigate:true,can_signal:true,can_save:true,can_load:true,can_observe:true,warning}
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::time::Instant;
    fn wait(bridge: &EngineBridge, predicate: impl Fn(&UiSnapshot) -> bool) -> UiSnapshot {
        let start = Instant::now();
        loop {
            let s = bridge.snapshot();
            if predicate(&s) {
                return s;
            }
            assert!(
                start.elapsed() < Duration::from_secs(10),
                "worker did not reach expected state: {}",
                s.progress_label
            );
            thread::sleep(Duration::from_millis(5));
        }
    }
    #[test]
    fn worker_commands_observation_lookup_and_archive_are_real() {
        let mut bridge = EngineBridge::new();
        let initial = wait(&bridge, |s| s.can_advance);
        assert_eq!(initial.conceptual_population, 1_000_000_005);
        bridge
            .command(UiCommand::SetViewMode(ViewMode::HistoricalSensor))
            .unwrap();
        let sensor = wait(&bridge, |s| s.mode == ViewMode::HistoricalSensor);
        assert_eq!(sensor.canonical_hash, initial.canonical_hash);
        assert!(sensor
            .bodies
            .iter()
            .filter(|b| b.id != 1)
            .all(|b| b.mass_label == "Not measured"));
        bridge
            .command(UiCommand::SetViewMode(ViewMode::Diagnostic))
            .unwrap();
        bridge
            .command(UiCommand::LookupIdentity {
                identity: "700010000".into(),
            })
            .unwrap();
        let lookup = wait(&bridge, |s| s.bodies.iter().any(|b| b.id == 700010000));
        assert_eq!(lookup.canonical_hash, initial.canonical_hash);
        assert_eq!(lookup.explicit_population, 5);
        bridge
            .command(UiCommand::Navigate {
                destination: [-50., 100.],
                speed_fraction: 0.5,
            })
            .unwrap();
        let course = wait(&bridge, |s| {
            s.bodies
                .iter()
                .any(|b| b.id == 1 && b.velocity == [0., 0.5])
        });
        assert_ne!(course.canonical_hash, initial.canonical_hash);
        bridge
            .command(UiCommand::SendSignal { target_id: 2 })
            .unwrap();
        bridge.command(UiCommand::Advance { ticks: 100 }).unwrap();
        let later = wait(&bridge, |s| s.time_ticks == initial.time_ticks + 100);
        assert_ne!(later.canonical_hash, initial.canonical_hash);
        let path =
            std::env::temp_dir().join(format!("es-adapter-{}.checkpoint", std::process::id()));
        let _ = std::fs::remove_file(&path);
        bridge
            .command(UiCommand::Save { path: path.clone() })
            .unwrap();
        let start = Instant::now();
        while !path.exists() {
            assert!(start.elapsed() < Duration::from_secs(5));
            thread::sleep(Duration::from_millis(5));
        }
        let restored = Engine::restore(&path).unwrap();
        assert_eq!(restored.state.clock, later.time_ticks);
        bridge.command(UiCommand::Advance { ticks: 1 }).unwrap();
        wait(&bridge, |s| s.time_ticks == later.time_ticks + 1);
        bridge
            .command(UiCommand::Load { path: path.clone() })
            .unwrap();
        let loaded = wait(&bridge, |s| s.time_ticks == later.time_ticks);
        assert_eq!(loaded.canonical_hash, later.canonical_hash);
        std::fs::remove_file(path).unwrap();
    }
    #[test]
    fn sensor_capability_failures_are_visible() {
        let mut e = scenario::observatory().unwrap();
        e.max_pending_jobs = 0;
        let s = snapshot(&e, ViewMode::HistoricalSensor, None, None, None);
        assert!(s.warning.unwrap().contains("Sensor query incomplete"));
    }
}
