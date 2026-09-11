//! Presentation-only bridge. Floating coordinates are chart samples, never canonical state.
use std::path::PathBuf;

#[derive(Clone, Copy, Debug, Default, Eq, PartialEq)]
pub enum ViewMode {
    HistoricalSensor,
    #[default]
    Diagnostic,
}

#[derive(Clone, Copy, Debug, Default, Eq, PartialEq)]
pub enum BodyKind {
    Source,
    #[default]
    Ship,
    Observer,
    Signal,
}

#[derive(Clone, Debug, Default)]
pub struct UiBody {
    pub id: u64,
    pub name: String,
    pub kind: BodyKind,
    pub position: [f64; 2],
    pub velocity: [f64; 2],
    /// Display radius in chart points; this is not a physical collision radius.
    pub radius: f32,
    pub mass_label: String,
    pub clock_label: String,
    pub sensor_age: Option<String>,
    pub population: u64,
    pub note: String,
    /// Historical samples explicitly supplied by the bridge, in snapshot mode.
    pub trace: Vec<[f64; 2]>,
}

#[derive(Clone, Debug, Default)]
pub struct UiEvent {
    pub tick: i128,
    pub title: String,
    pub detail: String,
    pub body_id: Option<u64>,
}

#[derive(Clone, Debug)]
pub struct UiSnapshot {
    pub time_ticks: i128,
    pub time_per_tick: f64,
    pub time_unit: String,
    pub distance_unit: String,
    pub observer_clock: String,
    pub mode: ViewMode,
    pub bodies: Vec<UiBody>,
    /// Newest first. The observatory displays at most 200 records.
    pub events: Vec<UiEvent>,
    pub conceptual_population: u64,
    pub explicit_population: usize,
    pub family_count: usize,
    pub canonical_hash: String,
    pub law_name: String,
    pub capability_status: String,
    pub capability_detail: String,
    /// Honest completion/work status supplied by the engine.
    pub progress_label: String,
    pub can_advance: bool,
    pub can_navigate: bool,
    pub can_signal: bool,
    pub can_save: bool,
    pub can_load: bool,
    pub can_observe: bool,
    pub warning: Option<String>,
}

impl Default for UiSnapshot {
    fn default() -> Self {
        Self {
            time_ticks: 0,
            time_per_tick: 1.0,
            time_unit: "ticks".into(),
            distance_unit: "units".into(),
            observer_clock: "Not available".into(),
            mode: ViewMode::Diagnostic,
            bodies: Vec::new(),
            events: Vec::new(),
            conceptual_population: 0,
            explicit_population: 0,
            family_count: 0,
            canonical_hash: String::new(),
            law_name: "Laboratory law".into(),
            capability_status: "BRIDGE NOT CONNECTED".into(),
            capability_detail: "Connect the canonical engine to populate this observatory.".into(),
            progress_label: "Awaiting engine".into(),
            can_advance: false,
            can_navigate: false,
            can_signal: false,
            can_save: false,
            can_load: false,
            can_observe: false,
            warning: None,
        }
    }
}

#[derive(Clone, Debug)]
pub enum UiCommand {
    Advance {
        ticks: u64,
    },
    LookupIdentity {
        identity: String,
    },
    SetViewMode(ViewMode),
    Navigate {
        destination: [f64; 2],
        speed_fraction: f64,
    },
    SendSignal {
        target_id: u64,
    },
    Save {
        path: PathBuf,
    },
    Load {
        path: PathBuf,
    },
    Reset,
}

pub trait ObservatoryBridge {
    fn snapshot(&self) -> UiSnapshot;
    fn command(&mut self, command: UiCommand) -> Result<(), String>;
}

/// Explicitly empty scaffold; the real native entrypoint installs the engine adapter.
pub struct DisconnectedBridge;
impl ObservatoryBridge for DisconnectedBridge {
    fn snapshot(&self) -> UiSnapshot {
        UiSnapshot::default()
    }
    fn command(&mut self, _: UiCommand) -> Result<(), String> {
        Err("The canonical engine is not connected.".into())
    }
}
