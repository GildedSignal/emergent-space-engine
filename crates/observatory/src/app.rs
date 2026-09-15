use crate::bridge::{BodyKind, ObservatoryBridge, UiBody, UiCommand, UiSnapshot, ViewMode};
use eframe::egui::{
    self, pos2, vec2, Align, Align2, Color32, FontFamily, FontId, Pos2, Rect, RichText, Sense,
    Shape, Stroke,
};
use std::collections::{BTreeMap, VecDeque};
use std::path::PathBuf;
use std::time::{Duration, Instant};

const INK: Color32 = Color32::from_rgb(48, 62, 65);
const MUTED: Color32 = Color32::from_rgb(117, 129, 129);
const PAPER: Color32 = Color32::from_rgb(249, 247, 240);
const PAPER_DARK: Color32 = Color32::from_rgb(238, 236, 226);
const LINE: Color32 = Color32::from_rgb(217, 221, 212);
const OCHRE: Color32 = Color32::from_rgb(160, 121, 64);
const SKY: Color32 = Color32::from_rgb(215, 231, 233);
const ALERT: Color32 = Color32::from_rgb(147, 88, 64);
const SERIF: &str = "observatory-serif";
const HISTORY_LIMIT: usize = 192;
const BODY_DISPLAY_LIMIT: usize = 4096;

#[derive(Clone, Debug, Default)]
pub struct AppOptions {
    pub screenshot: Option<PathBuf>,
    pub frames: Option<u64>,
    pub save_path: Option<PathBuf>,
    pub world: String,
}

#[derive(Clone, Debug)]
struct Camera {
    center: [f64; 2],
    scale: f64,
    fitted: bool,
}
impl Default for Camera {
    fn default() -> Self {
        Self {
            center: [0.0, 0.0],
            scale: 1.0,
            fitted: false,
        }
    }
}
impl Camera {
    fn project(&self, p: [f64; 2], rect: Rect) -> Pos2 {
        let dx = ((p[0] - self.center[0]) * self.scale).clamp(-1e8, 1e8) as f32;
        let dy = ((p[1] - self.center[1]) * self.scale).clamp(-1e8, 1e8) as f32;
        rect.center() + vec2(dx, -dy)
    }
    fn unproject(&self, p: Pos2, rect: Rect) -> [f64; 2] {
        [
            self.center[0] + (p.x - rect.center().x) as f64 / self.scale,
            self.center[1] - (p.y - rect.center().y) as f64 / self.scale,
        ]
    }
    fn fit(&mut self, bodies: &[UiBody], rect: Rect) {
        let mut lo = [f64::INFINITY; 2];
        let mut hi = [f64::NEG_INFINITY; 2];
        for body in bodies
            .iter()
            .filter(|b| finite(b.position))
            .take(BODY_DISPLAY_LIMIT)
        {
            for axis in 0..2 {
                lo[axis] = lo[axis].min(body.position[axis]);
                hi[axis] = hi[axis].max(body.position[axis]);
            }
        }
        if lo[0].is_finite() {
            self.center = [(lo[0] + hi[0]) * 0.5, (lo[1] + hi[1]) * 0.5];
            let width = (hi[0] - lo[0]).max(100.0);
            let height = (hi[1] - lo[1]).max(100.0);
            self.scale = ((rect.width() as f64 * 0.64 / width)
                .min(rect.height() as f64 * 0.60 / height))
            .clamp(1e-15, 1e8);
        } else {
            self.center = [0.0, 0.0];
            self.scale = 1.0;
        }
        self.fitted = true;
    }
    fn zoom_at(&mut self, factor: f64, at: Pos2, rect: Rect) {
        let anchor = self.unproject(at, rect);
        self.scale = (self.scale * factor).clamp(1e-15, 1e8);
        let moved = self.unproject(at, rect);
        for axis in 0..2 {
            self.center[axis] += anchor[axis] - moved[axis];
        }
    }
}

pub struct ObservatoryApp {
    bridge: Box<dyn ObservatoryBridge>,
    options: AppOptions,
    snapshot: UiSnapshot,
    camera: Camera,
    selected: Option<u64>,
    lookup: String,
    jump: String,
    playing: bool,
    speed: u64,
    fraction: f64,
    traces: bool,
    labels: bool,
    grid: bool,
    track_selected: bool,
    navigation: bool,
    navigation_speed: f64,
    history: BTreeMap<u64, VecDeque<[f64; 2]>>,
    last_history_tick: Option<i128>,
    last_mode: ViewMode,
    paper_texture: egui::TextureHandle,
    status: Option<(String, bool, Instant)>,
    save_path: String,
    show_archive: bool,
    show_help: bool,
    show_inspector: bool,
    frame_count: u64,
    screenshot_requested: bool,
    screenshot_finished: bool,
    screenshot_failed: bool,
}

impl ObservatoryApp {
    pub fn new(
        cc: &eframe::CreationContext<'_>,
        bridge: Box<dyn ObservatoryBridge>,
        options: AppOptions,
    ) -> Self {
        install_style(&cc.egui_ctx);
        let snapshot = bridge.snapshot();
        let last_mode = snapshot.mode;
        let selected = snapshot
            .bodies
            .iter()
            .find(|b| b.kind == BodyKind::Observer)
            .map(|b| b.id)
            .or_else(|| snapshot.bodies.first().map(|b| b.id));
        let save_path = options
            .save_path
            .clone()
            .unwrap_or_else(|| {
                std::env::current_dir()
                    .unwrap_or_else(|_| PathBuf::from("."))
                    .join("saves/observatory.json")
            })
            .display()
            .to_string();
        Self {
            bridge,
            options,
            snapshot,
            camera: Camera::default(),
            selected,
            lookup: String::new(),
            jump: "1000".into(),
            playing: false,
            speed: 16,
            fraction: 0.0,
            traces: true,
            labels: true,
            grid: true,
            track_selected: false,
            navigation: false,
            navigation_speed: 0.5,
            history: BTreeMap::new(),
            last_history_tick: None,
            last_mode,
            paper_texture: cc.egui_ctx.load_texture(
                "quiet-cosmic-grain",
                cosmic_paper(),
                egui::TextureOptions::LINEAR,
            ),
            status: None,
            save_path,
            show_archive: false,
            show_help: false,
            show_inspector: true,
            frame_count: 0,
            screenshot_requested: false,
            screenshot_finished: false,
            screenshot_failed: false,
        }
    }

    fn command(&mut self, command: UiCommand) {
        match self.bridge.command(command) {
            Ok(()) => {
                self.snapshot = self.bridge.snapshot();
            }
            Err(error) => {
                self.playing = false;
                self.status = Some((error, true, Instant::now()));
            }
        }
    }

    fn status(&mut self, text: impl Into<String>) {
        self.status = Some((text.into(), false, Instant::now()));
    }

    fn change_mode(&mut self, mode: ViewMode) {
        if mode != self.snapshot.mode {
            self.command(UiCommand::SetViewMode(mode));
            self.history.clear();
            self.last_history_tick = None;
            self.navigation = false;
        }
    }

    fn lookup_identity(&mut self) {
        let id = self.lookup.trim().to_string();
        if id.is_empty() {
            return;
        }
        self.command(UiCommand::LookupIdentity {
            identity: id.clone(),
        });
        if let Ok(parsed) = id.parse::<u64>() {
            self.selected = Some(parsed);
            self.track_selected = true;
            if let Some(body) = self.snapshot.bodies.iter().find(|body| body.id == parsed) {
                self.selected = Some(body.id);
                self.camera.center = body.position;
                self.track_selected = false;
                self.status(format!("Identity {parsed} located"));
            }
        }
    }

    fn record_history(&mut self) {
        if self.last_mode != self.snapshot.mode
            || self
                .last_history_tick
                .is_some_and(|t| t > self.snapshot.time_ticks)
        {
            self.history.clear();
            self.last_history_tick = None;
            self.last_mode = self.snapshot.mode;
        }
        if self.last_history_tick == Some(self.snapshot.time_ticks) {
            return;
        }
        self.last_history_tick = Some(self.snapshot.time_ticks);
        self.history
            .retain(|id, _| self.snapshot.bodies.iter().any(|b| b.id == *id));
        for body in self
            .snapshot
            .bodies
            .iter()
            .take(1024)
            .filter(|b| finite(b.position))
        {
            let points = self.history.entry(body.id).or_default();
            if points.back() != Some(&body.position) {
                points.push_back(body.position);
                while points.len() > HISTORY_LIMIT {
                    points.pop_front();
                }
            }
        }
    }

    fn header(&mut self, ctx: &egui::Context) {
        egui::TopBottomPanel::top("masthead")
            .exact_height(92.0)
            .frame(
                egui::Frame::default()
                    .fill(PAPER)
                    .inner_margin(egui::Margin::symmetric(26, 12)),
            )
            .show(ctx, |ui| {
                ui.horizontal(|ui| {
                    let (mark, _) = ui.allocate_exact_size(vec2(48.0, 57.0), Sense::hover());
                    draw_instrument(ui.painter(), mark.center(), 19.0, INK);
                    ui.add_space(12.0);
                    ui.vertical(|ui| {
                        ui.add_space(1.0);
                        ui.label(
                            RichText::new("EMERGENT SPACE")
                                .size(10.0)
                                .color(MUTED)
                                .extra_letter_spacing(2.7),
                        );
                        ui.label(
                            RichText::new("The observatory")
                                .font(serif(29.0))
                                .color(INK),
                        );
                    });
                    ui.with_layout(egui::Layout::right_to_left(Align::Center), |ui| {
                        if quiet_button(ui, "?", false)
                            .on_hover_text("Navigation & keyboard shortcuts")
                            .clicked()
                        {
                            self.show_help = !self.show_help;
                        }
                        if quiet_button(ui, "Archive", self.show_archive).clicked() {
                            self.show_archive = !self.show_archive;
                        }
                        if quiet_button(ui, "Inspector", self.show_inspector).clicked() {
                            self.show_inspector = !self.show_inspector;
                        }
                        ui.add_space(20.0);
                        if ui.available_width() > 290.0 {
                            ui.allocate_ui_with_layout(
                                vec2(300.0, 48.0),
                                egui::Layout::top_down(Align::RIGHT),
                                |ui| {
                                    ui.label(
                                        RichText::new(&self.snapshot.capability_status)
                                            .size(9.0)
                                            .color(OCHRE)
                                            .extra_letter_spacing(1.0),
                                    );
                                    ui.label(
                                        RichText::new(&self.snapshot.law_name)
                                            .size(12.0)
                                            .color(INK),
                                    );
                                },
                            );
                        }
                    });
                });
            });
    }

    fn footer(&mut self, ctx: &egui::Context) {
        egui::TopBottomPanel::bottom("chronometer")
            .exact_height(104.0)
            .frame(
                egui::Frame::default()
                    .fill(PAPER)
                    .inner_margin(egui::Margin::symmetric(26, 11)),
            )
            .show(ctx, |ui| {
                ui.horizontal(|ui| {
                    ui.vertical(|ui| {
                        eyebrow(ui, "COORDINATE TIME");
                        ui.horizontal(|ui| {
                            ui.label(RichText::new(format_time(&self.snapshot)).font(serif(25.0)));
                            ui.label(
                                RichText::new(&self.snapshot.time_unit)
                                    .size(11.0)
                                    .color(MUTED),
                            );
                        });
                    });
                    ui.add_space(28.0);
                    ui.vertical(|ui| {
                        eyebrow(ui, "OBSERVER CLOCK");
                        ui.label(
                            RichText::new(&self.snapshot.observer_clock)
                                .font(serif(20.0))
                                .color(INK),
                        );
                    });
                    ui.add_space(27.0);
                    let play = if self.playing {
                        "Ⅱ  Pause"
                    } else {
                        "▶  Play"
                    };
                    if ui
                        .add_enabled(
                            self.snapshot.can_advance,
                            egui::Button::new(RichText::new(play).size(13.0).color(PAPER))
                                .fill(INK)
                                .min_size(vec2(90.0, 36.0)),
                        )
                        .clicked()
                    {
                        self.playing = !self.playing;
                    }
                    if ui
                        .add_enabled(
                            self.snapshot.can_advance,
                            egui::Button::new("+1").min_size(vec2(35.0, 36.0)),
                        )
                        .on_hover_text("Advance one canonical tick")
                        .clicked()
                    {
                        self.playing = false;
                        self.command(UiCommand::Advance { ticks: 1 });
                    }
                    egui::ComboBox::from_id_salt("time-speed")
                        .selected_text(format!("{}×", self.speed))
                        .width(67.0)
                        .show_ui(ui, |ui| {
                            for speed in [1, 16, 256, 4096] {
                                ui.selectable_value(&mut self.speed, speed, format!("{speed}×"));
                            }
                        })
                        .response
                        .on_hover_text("1× = one canonical tick per wall-clock second");
                    ui.with_layout(egui::Layout::right_to_left(Align::Center), |ui| {
                        if ui.available_width() > 160.0 {
                            if ui
                                .add_enabled(
                                    self.snapshot.can_advance,
                                    egui::Button::new("Advance").min_size(vec2(70.0, 32.0)),
                                )
                                .clicked()
                            {
                                match self.jump.trim().parse::<u64>() {
                                    Ok(ticks) if ticks > 0 => {
                                        self.playing = false;
                                        self.command(UiCommand::Advance { ticks });
                                    }
                                    _ => {
                                        self.status = Some((
                                            "Enter a positive whole number of ticks.".into(),
                                            true,
                                            Instant::now(),
                                        ));
                                    }
                                }
                            }
                            ui.add(
                                egui::TextEdit::singleline(&mut self.jump)
                                    .desired_width(82.0)
                                    .hint_text("ticks"),
                            );
                            ui.label(RichText::new("Jump +").size(11.0).color(MUTED));
                        }
                    });
                });
                ui.add_space(7.0);
                ui.separator();
                ui.horizontal(|ui| {
                    if let Some((message, is_error, instant)) = &self.status {
                        if instant.elapsed() < Duration::from_secs(if *is_error { 60 } else { 8 }) {
                            ui.label(RichText::new(message).size(10.0).color(if *is_error {
                                ALERT
                            } else {
                                OCHRE
                            }));
                        } else {
                            ui.label(
                                RichText::new(&self.snapshot.progress_label)
                                    .size(10.0)
                                    .color(MUTED),
                            );
                        }
                    } else {
                        ui.label(
                            RichText::new(&self.snapshot.progress_label)
                                .size(10.0)
                                .color(MUTED),
                        );
                    }
                    ui.with_layout(egui::Layout::right_to_left(Align::Center), |ui| {
                        ui.label(
                            RichText::new("Drag to pan   ·   Scroll to zoom   ·   Space to pause")
                                .size(10.0)
                                .color(MUTED),
                        );
                    });
                });
            });
    }

    fn sidebar(&mut self, ctx: &egui::Context) {
        if !self.show_inspector {
            return;
        }
        egui::SidePanel::right("folio").resizable(true).default_width(304.0).width_range(270.0..=390.0)
            .frame(egui::Frame::default().fill(PAPER).inner_margin(egui::Margin::symmetric(23, 21)))
            .show(ctx, |ui| {
                egui::ScrollArea::vertical().id_salt("folio-scroll").show(ui, |ui| {
                    ui.horizontal(|ui| { eyebrow(ui, "FIELD NOTES"); ui.with_layout(egui::Layout::right_to_left(Align::Center), |ui| { ui.label(RichText::new("01").font(serif(15.0)).color(OCHRE)); }); });
                    ui.add_space(14.0);
                    let selected = self.selected.and_then(|id| self.snapshot.bodies.iter().find(|b| b.id == id)).cloned();
                    if let Some(body) = selected {
                        let (symbol, _) = ui.allocate_exact_size(vec2(ui.available_width(), 66.0), Sense::hover());
                        draw_body_symbol(ui.painter(), symbol.center(), &body, true, 1.7);
                        ui.add_space(10.0);
                        ui.label(RichText::new(&body.name).font(serif(27.0)).color(INK));
                        ui.add_space(3.0);
                        ui.label(RichText::new(format!("{}   /   {}", kind_name(body.kind).to_uppercase(), body.id)).size(9.0).color(OCHRE).extra_letter_spacing(1.0));
                        ui.add_space(18.0);
                        thin_rule(ui);
                        field(ui, "POSITION", &format!("{} , {}", scientific(body.position[0]), scientific(body.position[1])));
                        field(ui, "CHART UNITS", &self.snapshot.distance_unit);
                        field(ui, "VELOCITY", &format!("{} , {}", scientific(body.velocity[0]), scientific(body.velocity[1])));
                        if !body.mass_label.is_empty() { field(ui, "SOURCE MASS", &body.mass_label); }
                        if !body.clock_label.is_empty() { field(ui, "PROPER CLOCK", &body.clock_label); }
                        if let Some(age) = &body.sensor_age { field(ui, "SIGNAL AGE", age); }
                        if body.population > 1 { field(ui, "REPRESENTED MEMBERS", &separated(body.population)); }
                        if !body.note.is_empty() { ui.add_space(7.0); ui.label(RichText::new(&body.note).size(11.0).color(MUTED)); }
                        ui.add_space(16.0);
                        ui.horizontal(|ui| {
                            if quiet_button(ui, "Locate", false).clicked() { self.camera.center = body.position; }
                            if quiet_button(ui, "Follow", self.track_selected).clicked() { self.track_selected = !self.track_selected; }
                            if ui.add_enabled(self.snapshot.can_signal, egui::Button::new("Send signal")).on_hover_text("Emit a causal signal toward this identity").clicked() {
                                self.command(UiCommand::SendSignal { target_id: body.id });
                            }
                        });
                    } else {
                        ui.add_space(8.0);
                        ui.label(RichText::new("A place in space").font(serif(27.0)));
                        ui.add_space(10.0);
                        ui.label(RichText::new("Select a source or vessel to inspect its identity, motion, and recorded history.").size(12.0).color(MUTED));
                    }
                    ui.add_space(22.0);
                    thin_rule(ui);
                    eyebrow(ui, "FIND AN IDENTITY");
                    ui.add_space(7.0);
                    ui.horizontal(|ui| {
                        let width = (ui.available_width() - 57.0).max(70.0);
                        let input = ui.add(egui::TextEdit::singleline(&mut self.lookup).desired_width(width).hint_text("Stable numeric ID"));
                        let enter = input.lost_focus() && ui.input(|i| i.key_pressed(egui::Key::Enter));
                        if quiet_button(ui, "Find", false).clicked() || enter { self.lookup_identity(); }
                    });
                    ui.add_space(4.0);
                    ui.label(RichText::new("A family member can be revealed by identity.").size(10.0).color(MUTED));
                    ui.add_space(21.0);
                    thin_rule(ui);
                    ui.horizontal(|ui| {
                        ui.label(RichText::new("Event chronicle").font(serif(21.0)));
                        ui.with_layout(egui::Layout::right_to_left(Align::Center), |ui| { ui.label(RichText::new(format!("{}", self.snapshot.events.len())).size(10.0).color(MUTED)); });
                    });
                    ui.add_space(14.0);
                    if self.snapshot.events.is_empty() {
                        ui.label(RichText::new("No events in this view yet.").size(11.0).color(MUTED));
                        ui.add_space(8.0);
                        ui.label(RichText::new("Advance time or send a signal to begin a record.").font(serif(14.0)).color(MUTED));
                    }
                    let events = self.snapshot.events.iter().take(200).cloned().collect::<Vec<_>>();
                    for event in events {
                        ui.horizontal_top(|ui| {
                            let (rect, _) = ui.allocate_exact_size(vec2(8.0, 40.0), Sense::hover());
                            ui.painter().circle_filled(rect.left_top() + vec2(2.5, 7.0), 2.0, OCHRE);
                            ui.painter().line_segment([rect.left_top() + vec2(2.5, 14.0), rect.left_bottom() + vec2(2.5, 0.0)], Stroke::new(0.6, LINE));
                            ui.vertical(|ui| {
                                ui.label(RichText::new(format!("t = {}", event.tick)).size(9.0).color(OCHRE));
                                let response = ui.add(egui::Label::new(RichText::new(&event.title).size(12.0).color(INK)).sense(Sense::click()));
                                if response.clicked() { if let Some(id) = event.body_id { self.selected = Some(id); } }
                                if !event.detail.is_empty() { ui.label(RichText::new(&event.detail).size(10.0).color(MUTED)); }
                            });
                        });
                        ui.add_space(9.0);
                    }
                });
            });
    }

    fn canvas(&mut self, ctx: &egui::Context) {
        egui::CentralPanel::default()
            .frame(egui::Frame::default().fill(SKY))
            .show(ctx, |ui| {
                let rect = ui.max_rect();
                let response = ui.allocate_rect(rect, Sense::click_and_drag());
                let painter = ui.painter_at(rect);
                if !self.camera.fitted {
                    self.camera.fit(&self.snapshot.bodies, rect);
                }
                if self.track_selected {
                    if let Some(body) = self
                        .selected
                        .and_then(|id| self.snapshot.bodies.iter().find(|b| b.id == id))
                    {
                        self.camera.center = body.position;
                    }
                }
                if response.dragged() {
                    let delta = ctx.input(|i| i.pointer.delta());
                    self.camera.center[0] -= delta.x as f64 / self.camera.scale;
                    self.camera.center[1] += delta.y as f64 / self.camera.scale;
                    self.track_selected = false;
                }
                if response.hovered() {
                    let scroll = ctx.input(|i| i.smooth_scroll_delta.y);
                    let zoom = ctx.input(|i| i.zoom_delta());
                    if scroll.abs() > 0.01 || (zoom - 1.0).abs() > 0.001 {
                        let at = response.hover_pos().unwrap_or(rect.center());
                        self.camera
                            .zoom_at((scroll as f64 * 0.0015).exp() * zoom as f64, at, rect);
                    }
                }
                if response.double_clicked() {
                    self.camera.fit(&self.snapshot.bodies, rect);
                    self.track_selected = false;
                }

                painter.image(
                    self.paper_texture.id(),
                    rect,
                    Rect::from_min_max(Pos2::ZERO, pos2(1.0, 1.0)),
                    Color32::WHITE,
                );
                self.draw_coordinates(&painter, rect);
                self.draw_worldlines(&painter, rect);
                let mut nearest = None;
                let pointer = response.hover_pos();
                for body in self
                    .snapshot
                    .bodies
                    .iter()
                    .take(BODY_DISPLAY_LIMIT)
                    .filter(|b| finite(b.position))
                {
                    let at = self.camera.project(body.position, rect);
                    if !rect.expand(80.0).contains(at) {
                        continue;
                    }
                    let selected = self.selected == Some(body.id);
                    draw_body_symbol(&painter, at, body, selected, 1.0);
                    if let Some(pointer) = pointer {
                        let d = at.distance(pointer);
                        if d < body.radius.max(12.0) + 10.0
                            && nearest.is_none_or(|(_, old)| d < old)
                        {
                            nearest = Some((body.id, d));
                        }
                    }
                    if self.labels
                        && (selected
                            || body.kind == BodyKind::Source
                            || body.kind == BodyKind::Observer
                            || self.snapshot.bodies.len() < 35)
                    {
                        let offset = body.radius.max(6.0) + 10.0;
                        painter.text(
                            at + vec2(offset, -7.0),
                            Align2::LEFT_CENTER,
                            &body.name,
                            serif(if selected { 17.0 } else { 14.0 }),
                            INK,
                        );
                        if selected {
                            painter.text(
                                at + vec2(offset, 10.0),
                                Align2::LEFT_CENTER,
                                format!("{}  ·  {}", kind_name(body.kind), body.id),
                                FontId::proportional(9.0),
                                MUTED,
                            );
                        }
                    }
                }
                if response.clicked() {
                    if self.navigation && self.snapshot.can_navigate {
                        if let Some(point) = response.interact_pointer_pos() {
                            self.command(UiCommand::Navigate {
                                destination: self.camera.unproject(point, rect),
                                speed_fraction: self.navigation_speed,
                            });
                            self.navigation = false;
                            self.status("Course command submitted");
                        }
                    } else {
                        self.selected = nearest.map(|(id, _)| id);
                        self.track_selected = false;
                    }
                }
                if nearest.is_some() {
                    ctx.set_cursor_icon(egui::CursorIcon::PointingHand);
                } else if response.dragged() {
                    ctx.set_cursor_icon(egui::CursorIcon::Grabbing);
                } else if self.navigation && response.hovered() {
                    ctx.set_cursor_icon(egui::CursorIcon::Crosshair);
                }

                self.draw_chart_furniture(&painter, rect);
                if self.snapshot.bodies.is_empty() {
                    painter.text(
                        rect.center() + vec2(0.0, -22.0),
                        Align2::CENTER_CENTER,
                        "A universe, awaiting observation.",
                        serif(30.0),
                        INK,
                    );
                    painter.text(
                        rect.center() + vec2(0.0, 18.0),
                        Align2::CENTER_CENTER,
                        &self.snapshot.progress_label,
                        FontId::proportional(12.0),
                        MUTED,
                    );
                }
                self.canvas_controls(ui, rect);
            });
    }

    fn draw_coordinates(&self, painter: &egui::Painter, rect: Rect) {
        if !self.grid {
            return;
        }
        let step = nice_step(125.0 / self.camera.scale);
        let low = self.camera.unproject(rect.left_bottom(), rect);
        let high = self.camera.unproject(rect.right_top(), rect);
        let grid_color = Color32::from_rgba_unmultiplied(76, 109, 118, 22);
        for axis in 0..2 {
            let first = (low[axis] / step).floor() * step;
            let count = ((high[axis] - first) / step).ceil().clamp(0.0, 100.0) as usize;
            for index in 0..=count {
                let v = first + index as f64 * step;
                let a = if axis == 0 {
                    self.camera.project([v, low[1]], rect)
                } else {
                    self.camera.project([low[0], v], rect)
                };
                let b = if axis == 0 {
                    self.camera.project([v, high[1]], rect)
                } else {
                    self.camera.project([high[0], v], rect)
                };
                dotted_line(painter, a, b, 1.0, 7.0, grid_color);
                let text_pos = if axis == 0 {
                    pos2(a.x + 4.0, rect.bottom() - 27.0)
                } else {
                    pos2(rect.left() + 9.0, a.y - 7.0)
                };
                if axis == 0 && text_pos.x > rect.left() + 200.0
                    || axis == 1 && text_pos.y > rect.top() + 230.0
                {
                    painter.text(
                        text_pos,
                        Align2::LEFT_CENTER,
                        scientific(v),
                        FontId::monospace(8.0),
                        Color32::from_rgb(139, 163, 164),
                    );
                }
            }
        }
        let zero = self.camera.project([0.0, 0.0], rect);
        if rect.contains(zero) {
            painter.line_segment(
                [zero - vec2(12.0, 0.0), zero + vec2(12.0, 0.0)],
                Stroke::new(0.7, Color32::from_rgb(161, 183, 182)),
            );
            painter.line_segment(
                [zero - vec2(0.0, 12.0), zero + vec2(0.0, 12.0)],
                Stroke::new(0.7, Color32::from_rgb(161, 183, 182)),
            );
        }
    }

    fn draw_worldlines(&self, painter: &egui::Painter, rect: Rect) {
        if !self.traces {
            return;
        }
        for body in self.snapshot.bodies.iter().take(BODY_DISPLAY_LIMIT) {
            let selected = self.selected == Some(body.id);
            let stroke = Stroke::new(
                if selected { 1.25 } else { 0.7 },
                if selected {
                    Color32::from_rgba_unmultiplied(155, 111, 64, 170)
                } else {
                    Color32::from_rgba_unmultiplied(64, 97, 110, 85)
                },
            );
            let points: Vec<_> = if body.trace.len() > 1 {
                body.trace
                    .iter()
                    .filter(|p| finite(**p))
                    .take(2048)
                    .map(|p| self.camera.project(*p, rect))
                    .collect()
            } else {
                self.history
                    .get(&body.id)
                    .into_iter()
                    .flat_map(|h| h.iter())
                    .map(|p| self.camera.project(*p, rect))
                    .collect()
            };
            if points.len() > 1 {
                painter.add(Shape::line(points, stroke));
            }
        }
    }

    fn draw_chart_furniture(&self, painter: &egui::Painter, rect: Rect) {
        let mode = if self.snapshot.mode == ViewMode::Diagnostic {
            "DIAGNOSTIC CHART"
        } else {
            "HISTORICAL SENSOR CHART"
        };
        painter.text(
            rect.left_top() + vec2(27.0, 32.0),
            Align2::LEFT_CENTER,
            mode,
            FontId::proportional(10.0),
            MUTED,
        );
        painter.text(
            rect.left_top() + vec2(27.0, 62.0),
            Align2::LEFT_CENTER,
            if self.snapshot.mode == ViewMode::Diagnostic {
                "The universe at a coordinate time"
            } else {
                "Only what has reached the observer"
            },
            serif(23.0),
            INK,
        );
        painter.text(
            rect.left_top() + vec2(27.0, 89.0),
            Align2::LEFT_CENTER,
            if self.snapshot.mode == ViewMode::Diagnostic {
                "Instrument view · not an observer's knowledge"
            } else {
                "A record carried by finite-speed signals"
            },
            FontId::proportional(11.0),
            MUTED,
        );

        let center = rect.right_top() + vec2(-44.0, 49.0);
        draw_compass(painter, center);
        let step = nice_step(100.0 / self.camera.scale);
        let width = (step * self.camera.scale) as f32;
        let origin = rect.left_bottom() + vec2(28.0, -49.0);
        painter.line_segment([origin, origin + vec2(width, 0.0)], Stroke::new(1.0, INK));
        for x in [0.0, width] {
            painter.line_segment(
                [origin + vec2(x, -3.0), origin + vec2(x, 3.0)],
                Stroke::new(1.0, INK),
            );
        }
        painter.text(
            origin - vec2(0.0, 14.0),
            Align2::LEFT_CENTER,
            format!("{} {}", scientific(step), self.snapshot.distance_unit),
            FontId::proportional(10.0),
            INK,
        );
        painter.text(
            rect.left_bottom() + vec2(28.0, -18.0),
            Align2::LEFT_CENTER,
            "2 + 1 D    /    CAUSAL SPACETIME",
            FontId::proportional(8.0),
            MUTED,
        );
        if self.navigation {
            let at = rect.center_bottom() + vec2(0.0, -110.0);
            painter.rect_filled(Rect::from_center_size(at, vec2(350.0, 34.0)), 3, PAPER);
            painter.text(
                at,
                Align2::CENTER_CENTER,
                "Choose a destination on the chart · Esc to cancel",
                FontId::proportional(11.0),
                OCHRE,
            );
        }
    }

    fn canvas_controls(&mut self, ui: &mut egui::Ui, rect: Rect) {
        let view_rect = Rect::from_min_size(rect.left_top() + vec2(25.0, 114.0), vec2(320.0, 35.0));
        ui.scope_builder(egui::UiBuilder::new().max_rect(view_rect), |ui| {
            ui.horizontal(|ui| {
                let observed = self.snapshot.mode == ViewMode::HistoricalSensor;
                if ui
                    .add_enabled(
                        self.snapshot.can_observe,
                        egui::Button::new(
                            RichText::new("Historical sensor")
                                .size(11.0)
                                .color(if observed { PAPER } else { INK }),
                        )
                        .fill(if observed {
                            INK
                        } else {
                            PAPER.linear_multiply(0.97)
                        }),
                    )
                    .on_hover_text("Only events whose information has arrived at the observer")
                    .clicked()
                {
                    self.change_mode(ViewMode::HistoricalSensor);
                }
                if quiet_button(ui, "Diagnostic", !observed)
                    .on_hover_text("Scientific view of canonical coordinate-time state")
                    .clicked()
                {
                    self.change_mode(ViewMode::Diagnostic);
                }
            });
        });
        let info_rect = Rect::from_min_size(rect.left_top() + vec2(27.0, 173.0), vec2(260.0, 83.0));
        ui.scope_builder(egui::UiBuilder::new().max_rect(info_rect), |ui| {
            eyebrow(ui, "POPULATION REPRESENTATION");
            ui.add_space(4.0);
            ui.horizontal(|ui| {
                ui.label(
                    RichText::new(separated(self.snapshot.conceptual_population))
                        .font(serif(23.0))
                        .color(INK),
                );
                ui.label(RichText::new("conceptual ships").size(10.0).color(MUTED));
            });
            ui.label(
                RichText::new(format!(
                    "{} families · {} explicit records",
                    separated(self.snapshot.family_count as u64),
                    separated(self.snapshot.explicit_population as u64)
                ))
                .size(10.0)
                .color(MUTED),
            );
        });
        let control_rect =
            Rect::from_min_size(rect.right_bottom() + vec2(-340.0, -69.0), vec2(316.0, 42.0));
        ui.scope_builder(egui::UiBuilder::new().max_rect(control_rect), |ui| {
            ui.horizontal(|ui| {
                if quiet_button(ui, "Traces", self.traces).clicked() {
                    self.traces = !self.traces;
                }
                if quiet_button(ui, "Labels", self.labels).clicked() {
                    self.labels = !self.labels;
                }
                if quiet_button(ui, "Grid", self.grid).clicked() {
                    self.grid = !self.grid;
                }
                if quiet_button(ui, "−", false).clicked() {
                    self.camera.zoom_at(1.0 / 1.4, rect.center(), rect);
                }
                if quiet_button(ui, "+", false).clicked() {
                    self.camera.zoom_at(1.4, rect.center(), rect);
                }
                if quiet_button(ui, "Fit", false).clicked() {
                    self.camera.fit(&self.snapshot.bodies, rect);
                    self.track_selected = false;
                }
            });
        });
        if self.snapshot.can_navigate {
            let control_rect =
                Rect::from_min_size(rect.right_top() + vec2(-168.0, 109.0), vec2(143.0, 86.0));
            ui.scope_builder(egui::UiBuilder::new().max_rect(control_rect), |ui| {
                if quiet_button(ui, "Set course", self.navigation).clicked() {
                    self.navigation = !self.navigation;
                }
                if self.navigation {
                    ui.add(
                        egui::Slider::new(&mut self.navigation_speed, 0.01..=0.95)
                            .suffix(" c")
                            .fixed_decimals(2)
                            .show_value(true),
                    );
                }
            });
        }
        let status_width = (rect.width() - 54.0).min(620.0);
        let cap_rect = Rect::from_min_size(
            rect.left_bottom() + vec2(27.0, -111.0),
            vec2(status_width, 31.0),
        );
        ui.scope_builder(egui::UiBuilder::new().max_rect(cap_rect), |ui| {
            ui.label(
                RichText::new(&self.snapshot.capability_detail)
                    .size(10.0)
                    .color(MUTED),
            );
            if let Some(warning) = &self.snapshot.warning {
                ui.label(RichText::new(warning).size(10.0).color(ALERT));
            }
        });
    }

    fn archive_window(&mut self, ctx: &egui::Context) {
        if !self.show_archive {
            return;
        }
        let mut open = self.show_archive;
        egui::Window::new("Archive & replay").open(&mut open).resizable(false).default_width(480.0).show(ctx, |ui| {
            ui.label(RichText::new("A record of this universe").font(serif(25.0)));
            ui.add_space(8.0);
            ui.label(RichText::new("Save or restore the engine's canonical state. Chart settings are presentation only.").size(12.0).color(MUTED));
            ui.add_space(18.0);
            eyebrow(ui, "LOCAL ARCHIVE PATH");
            ui.add_space(6.0);
            ui.add(egui::TextEdit::singleline(&mut self.save_path).desired_width(f32::INFINITY));
            ui.add_space(11.0);
            ui.horizontal(|ui| {
                if ui.add_enabled(self.snapshot.can_save, egui::Button::new("Save universe")).clicked() {
                    self.command(UiCommand::Save { path: PathBuf::from(&self.save_path) });
                    self.status("Archive write requested");
                }
                if ui.add_enabled(self.snapshot.can_load, egui::Button::new("Load universe")).clicked() {
                    self.playing = false;
                    self.command(UiCommand::Load { path: PathBuf::from(&self.save_path) });
                    self.history.clear(); self.last_history_tick = None; self.camera.fitted = false;
                }
            });
            ui.add_space(18.0);
            thin_rule(ui);
            eyebrow(ui, "CANONICAL COMMITMENT");
            if self.snapshot.canonical_hash.is_empty() { ui.label(RichText::new("Not available").size(11.0).color(MUTED)); }
            else { ui.add(egui::Label::new(RichText::new(&self.snapshot.canonical_hash).monospace().size(10.0)).wrap()); }
            ui.add_space(11.0);
            if quiet_button(ui, "Reset laboratory", false).clicked() {
                self.playing = false; self.command(UiCommand::Reset); self.history.clear(); self.last_history_tick = None; self.camera.fitted = false;
            }
        });
        self.show_archive = open;
    }

    fn help_window(&mut self, ctx: &egui::Context) {
        if !self.show_help {
            return;
        }
        egui::Window::new("Using the observatory").open(&mut self.show_help).resizable(false).default_width(400.0).show(ctx, |ui| {
            ui.label(RichText::new("An instrument for a causal universe").font(serif(24.0)));
            ui.add_space(14.0);
            for (action, control) in [("Pan the chart", "Drag empty space"), ("Zoom around pointer", "Scroll / pinch"), ("Inspect an identity", "Click its symbol"), ("Fit all visible bodies", "Double click / R"), ("Play or pause", "Space"), ("Toggle historical traces", "T"), ("Save canonical state", "⌘S / Ctrl+S"), ("Cancel course setting", "Esc")] { field(ui, action, control); }
            ui.add_space(14.0);
            ui.label(RichText::new("Historical sensor view contains only information that has reached the observer. Diagnostic view is a scientific instrument and may reveal coordinate-time state.").size(12.0).color(MUTED));
            ui.add_space(8.0);
            ui.label(RichText::new("Display coordinates and symbol sizes are schematic. The laboratory capability label states the active law; conceptual population is not a measured performance claim.").size(11.0).color(MUTED));
        });
    }

    fn capture_and_exit(&mut self, ctx: &egui::Context) {
        let screenshot = ctx.input(|i| {
            i.events.iter().find_map(|event| {
                if let egui::Event::Screenshot { image, .. } = event {
                    Some(image.clone())
                } else {
                    None
                }
            })
        });
        if let Some(image) = screenshot {
            if let Some(path) = &self.options.screenshot {
                match save_png(path, &image) {
                    Ok(()) => {
                        self.screenshot_finished = true;
                        eprintln!("Observatory screenshot: {}", path.display());
                    }
                    Err(error) => {
                        self.screenshot_failed = true;
                        eprintln!("Observatory screenshot failed: {error}");
                    }
                }
            }
        }
        if self.options.screenshot.is_some()
            && self.frame_count >= 10
            && (self.snapshot.can_advance || self.frame_count > 300)
            && !self.screenshot_requested
        {
            ctx.send_viewport_cmd(egui::ViewportCommand::Screenshot(Default::default()));
            self.screenshot_requested = true;
        }
        let capture_done =
            self.options.screenshot.is_none() || self.screenshot_finished || self.screenshot_failed;
        let frame_limit = self.options.frames;
        if frame_limit.is_some_and(|limit| self.frame_count >= limit.max(10)) && capture_done {
            ctx.send_viewport_cmd(egui::ViewportCommand::Close);
        }
        if self.screenshot_requested && !capture_done && self.frame_count > 300 {
            self.screenshot_failed = true;
            eprintln!("Observatory screenshot failed: renderer did not return a screenshot within 300 frames");
        }
        if self.options.frames.is_some() || self.options.screenshot.is_some() && !capture_done {
            ctx.request_repaint();
        }
    }
}

impl eframe::App for ObservatoryApp {
    fn clear_color(&self, _visuals: &egui::Visuals) -> [f32; 4] {
        egui::Rgba::from(PAPER).to_array()
    }
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        self.frame_count += 1;
        self.snapshot = self.bridge.snapshot();
        if !ctx.wants_keyboard_input() {
            if ctx.input(|i| i.key_pressed(egui::Key::Space)) && self.snapshot.can_advance {
                self.playing = !self.playing;
            }
            if ctx.input(|i| i.key_pressed(egui::Key::R)) {
                self.camera.fitted = false;
                self.track_selected = false;
            }
            if ctx.input(|i| i.key_pressed(egui::Key::T)) {
                self.traces = !self.traces;
            }
            if ctx.input(|i| i.key_pressed(egui::Key::Escape)) {
                self.navigation = false;
                self.show_archive = false;
                self.show_help = false;
            }
            if ctx.input(|i| i.modifiers.command && i.key_pressed(egui::Key::S))
                && self.snapshot.can_save
            {
                self.command(UiCommand::Save {
                    path: PathBuf::from(&self.save_path),
                });
            }
        }
        if self.playing && self.snapshot.can_advance {
            let dt = ctx.input(|i| i.stable_dt).clamp(0.0, 0.1) as f64;
            self.fraction += dt * self.speed as f64;
            if self.fraction >= 1.0 {
                let ticks = (self.fraction.floor() as u64).min(4096);
                self.fraction -= ticks as f64;
                self.command(UiCommand::Advance { ticks });
            }
            ctx.request_repaint_after(Duration::from_millis(16));
        }
        self.record_history();
        self.header(ctx);
        self.footer(ctx);
        self.sidebar(ctx);
        self.canvas(ctx);
        self.archive_window(ctx);
        self.help_window(ctx);
        self.capture_and_exit(ctx);
        // Worker snapshots can change while paused, without a native input event.
        ctx.request_repaint_after(Duration::from_millis(100));
    }
}

fn install_style(ctx: &egui::Context) {
    let mut fonts = egui::FontDefinitions::default();
    let font_path = [
        "/System/Library/Fonts/Supplemental/Georgia.ttf",
        "/Library/Fonts/Georgia.ttf",
    ]
    .into_iter()
    .find_map(|path| std::fs::read(path).ok());
    let family = if let Some(data) = font_path {
        fonts
            .font_data
            .insert(SERIF.into(), egui::FontData::from_owned(data).into());
        vec![SERIF.into()]
    } else {
        fonts
            .families
            .get(&FontFamily::Proportional)
            .cloned()
            .unwrap_or_default()
    };
    fonts
        .families
        .insert(FontFamily::Name(SERIF.into()), family);
    ctx.set_fonts(fonts);
    let mut visuals = egui::Visuals::light();
    visuals.override_text_color = Some(INK);
    visuals.panel_fill = PAPER;
    visuals.window_fill = PAPER;
    visuals.extreme_bg_color = Color32::from_rgb(243, 242, 234);
    visuals.faint_bg_color = PAPER_DARK;
    visuals.window_stroke = Stroke::new(1.0, LINE);
    visuals.selection.bg_fill = Color32::from_rgb(220, 215, 189);
    visuals.selection.stroke = Stroke::new(1.0, INK);
    visuals.widgets.noninteractive.bg_stroke = Stroke::new(0.7, LINE);
    visuals.widgets.inactive.bg_fill = PAPER;
    visuals.widgets.inactive.weak_bg_fill = PAPER;
    visuals.widgets.inactive.bg_stroke = Stroke::new(0.7, LINE);
    visuals.widgets.hovered.bg_fill = PAPER_DARK;
    visuals.widgets.hovered.weak_bg_fill = PAPER_DARK;
    visuals.widgets.hovered.bg_stroke = Stroke::new(0.8, OCHRE);
    visuals.widgets.active.bg_fill = PAPER_DARK;
    visuals.widgets.active.weak_bg_fill = PAPER_DARK;
    visuals.widgets.active.bg_stroke = Stroke::new(1.0, OCHRE);
    ctx.set_visuals(visuals);
    let mut style = (*ctx.style()).clone();
    style.spacing.item_spacing = vec2(9.0, 6.0);
    style.spacing.button_padding = vec2(10.0, 7.0);
    style.spacing.interact_size.y = 28.0;
    style
        .text_styles
        .insert(egui::TextStyle::Body, FontId::proportional(12.0));
    style
        .text_styles
        .insert(egui::TextStyle::Button, FontId::proportional(11.0));
    style
        .text_styles
        .insert(egui::TextStyle::Small, FontId::proportional(10.0));
    ctx.set_style(style);
}

fn cosmic_paper() -> egui::ColorImage {
    let size = 384;
    let mut pixels = Vec::with_capacity(size * size);
    for y in 0..size {
        for x in 0..size {
            let u = x as f32 / size as f32;
            let v = y as f32 / size as f32;
            let wave = ((u * 4.1 + v * 2.6).sin() * 0.55 + (v * 5.2 - u * 1.7).cos() * 0.45) * 3.7;
            let cloud = (-((u - 0.48).powi(2) / 0.14 + (v - 0.40).powi(2) / 0.18)).exp() * 10.0;
            let mut h = (x as u32)
                .wrapping_mul(374761393)
                .wrapping_add((y as u32).wrapping_mul(668265263));
            h = (h ^ (h >> 13)).wrapping_mul(1274126177);
            h ^= h >> 16;
            let grain = ((h & 1023) as f32 / 1023.0 - 0.5) * 3.3;
            let lift = wave + cloud + grain;
            pixels.push(Color32::from_rgb(
                (211.0 + lift) as u8,
                (226.0 + lift * 0.8) as u8,
                (227.0 + lift * 0.78) as u8,
            ));
        }
    }
    egui::ColorImage {
        size: [size, size],
        pixels,
    }
}

fn draw_body_symbol(painter: &egui::Painter, at: Pos2, body: &UiBody, selected: bool, factor: f32) {
    let r = body.radius.clamp(3.5, 29.0) * factor;
    if selected {
        painter.circle_stroke(at, r + 11.0 * factor, Stroke::new(0.8, OCHRE));
        for d in [
            vec2(1.0, 0.0),
            vec2(-1.0, 0.0),
            vec2(0.0, 1.0),
            vec2(0.0, -1.0),
        ] {
            painter.line_segment(
                [at + d * (r + 14.0 * factor), at + d * (r + 19.0 * factor)],
                Stroke::new(0.9, OCHRE),
            );
        }
    }
    match body.kind {
        BodyKind::Source => {
            for k in (1..=7).rev() {
                let alpha = (7.0 - k as f32 * 0.7) as u8;
                painter.circle_filled(
                    at,
                    r + k as f32 * 6.5 * factor,
                    Color32::from_rgba_unmultiplied(194, 152, 99, alpha),
                );
            }
            painter.circle_stroke(
                at,
                r + 4.0 * factor,
                Stroke::new(0.55, Color32::from_rgb(155, 163, 149)),
            );
            painter.circle_filled(at, r, Color32::from_rgb(239, 221, 178));
            painter.circle_stroke(at, r, Stroke::new(0.9, INK));
            painter.circle_filled(
                at - vec2(r * 0.24, r * 0.27),
                r * 0.52,
                Color32::from_rgba_unmultiplied(253, 249, 218, 90),
            );
            let start = at + vec2(-r * 0.57, r * 0.55);
            painter.line_segment(
                [start, at + vec2(r * 0.60, r * 0.25)],
                Stroke::new(0.55, Color32::from_rgb(190, 169, 119)),
            );
        }
        BodyKind::Ship | BodyKind::Observer => {
            let length = body.velocity[0].hypot(body.velocity[1]);
            let d = if length.is_finite() && length > 1e-15 {
                vec2(
                    (body.velocity[0] / length) as f32,
                    -(body.velocity[1] / length) as f32,
                )
            } else {
                vec2(0.65, -0.76)
            };
            let side = vec2(-d.y, d.x);
            let points = vec![
                at + d * r * 1.6,
                at - d * r + side * r * 0.7,
                at - d * r * 0.42,
                at - d * r - side * r * 0.7,
            ];
            let fill = if body.kind == BodyKind::Observer {
                Color32::from_rgb(167, 124, 63)
            } else {
                Color32::from_rgb(95, 126, 135)
            };
            painter.add(Shape::convex_polygon(points, fill, Stroke::new(0.85, INK)));
            painter.line_segment(
                [at + d * r * 0.9, at - d * r * 0.3],
                Stroke::new(0.7, PAPER),
            );
            if body.kind == BodyKind::Observer {
                painter.circle_stroke(at, r * 2.1, Stroke::new(0.45, OCHRE));
            }
        }
        BodyKind::Signal => {
            painter.circle_filled(at, 2.4 * factor, OCHRE);
            painter.circle_stroke(at, 6.0 * factor, Stroke::new(0.8, OCHRE));
            painter.circle_stroke(
                at,
                10.0 * factor,
                Stroke::new(0.4, Color32::from_rgba_unmultiplied(160, 121, 64, 90)),
            );
        }
    }
}

fn draw_instrument(painter: &egui::Painter, center: Pos2, r: f32, color: Color32) {
    painter.circle_stroke(center, r, Stroke::new(0.85, color));
    painter.circle_stroke(center, r * 0.74, Stroke::new(0.55, color));
    painter.line_segment(
        [center - vec2(r * 1.17, 0.0), center + vec2(r * 1.17, 0.0)],
        Stroke::new(0.7, color),
    );
    painter.line_segment(
        [center - vec2(0.0, r * 1.17), center + vec2(0.0, r * 1.17)],
        Stroke::new(0.7, color),
    );
    let d = vec2(0.68, -0.73);
    painter.line_segment(
        [center - d * r * 0.90, center + d * r * 1.27],
        Stroke::new(1.0, OCHRE),
    );
    painter.circle_filled(center + d * r * 0.87, 2.4, OCHRE);
    painter.circle_filled(center, 1.8, color);
}
fn draw_compass(painter: &egui::Painter, at: Pos2) {
    painter.circle_stroke(
        at,
        18.0,
        Stroke::new(0.55, Color32::from_rgb(153, 176, 176)),
    );
    painter.line_segment(
        [at - vec2(24.0, 0.0), at + vec2(24.0, 0.0)],
        Stroke::new(0.6, MUTED),
    );
    painter.line_segment(
        [at - vec2(0.0, 24.0), at + vec2(0.0, 24.0)],
        Stroke::new(0.6, MUTED),
    );
    painter.text(
        at - vec2(0.0, 33.0),
        Align2::CENTER_CENTER,
        "+Y",
        FontId::proportional(8.0),
        MUTED,
    );
    painter.text(
        at + vec2(32.0, 0.0),
        Align2::CENTER_CENTER,
        "+X",
        FontId::proportional(8.0),
        MUTED,
    );
    painter.circle_filled(at, 1.7, OCHRE);
}
fn dotted_line(painter: &egui::Painter, a: Pos2, b: Pos2, dash: f32, gap: f32, color: Color32) {
    let length = a.distance(b);
    if length <= 0.0 || !length.is_finite() {
        return;
    }
    let direction = (b - a) / length;
    let mut d = 0.0;
    while d < length && d < 20000.0 {
        painter.line_segment(
            [a + direction * d, a + direction * (d + dash).min(length)],
            Stroke::new(0.7, color),
        );
        d += dash + gap;
    }
}
fn serif(size: f32) -> FontId {
    FontId::new(size, FontFamily::Name(SERIF.into()))
}
fn eyebrow(ui: &mut egui::Ui, text: &str) {
    ui.label(
        RichText::new(text)
            .size(9.0)
            .color(MUTED)
            .extra_letter_spacing(1.3),
    );
}
fn thin_rule(ui: &mut egui::Ui) {
    ui.separator();
    ui.add_space(11.0);
}
fn field(ui: &mut egui::Ui, name: &str, value: &str) {
    ui.horizontal(|ui| {
        ui.label(RichText::new(name).size(9.0).color(MUTED));
        ui.with_layout(egui::Layout::right_to_left(Align::Center), |ui| {
            ui.label(RichText::new(value).size(11.0).color(INK));
        });
    });
    ui.add_space(3.0);
}
fn quiet_button(ui: &mut egui::Ui, label: &str, selected: bool) -> egui::Response {
    ui.add(
        egui::Button::new(RichText::new(label).size(11.0).color(if selected {
            OCHRE
        } else {
            INK
        }))
        .fill(if selected {
            Color32::from_rgb(236, 232, 210)
        } else {
            PAPER
        })
        .stroke(Stroke::new(
            0.7,
            if selected {
                Color32::from_rgb(194, 181, 147)
            } else {
                LINE
            },
        )),
    )
}
fn finite(p: [f64; 2]) -> bool {
    p[0].is_finite() && p[1].is_finite()
}
fn kind_name(kind: BodyKind) -> &'static str {
    match kind {
        BodyKind::Source => "Source",
        BodyKind::Ship => "Ship",
        BodyKind::Observer => "Observer",
        BodyKind::Signal => "Signal",
    }
}
fn nice_step(raw: f64) -> f64 {
    let power = 10f64.powf(raw.max(1e-16).log10().floor());
    let scaled = raw / power;
    let unit = if scaled < 2.0 {
        1.0
    } else if scaled < 5.0 {
        2.0
    } else {
        5.0
    };
    unit * power
}
fn scientific(value: f64) -> String {
    if !value.is_finite() {
        return "unavailable".into();
    }
    let abs = value.abs();
    if abs >= 1e7 || abs > 0.0 && abs < 0.001 {
        format!("{value:.2e}")
    } else if abs >= 1000.0 {
        format!("{value:.0}")
    } else {
        format!("{value:.2}")
            .trim_end_matches('0')
            .trim_end_matches('.')
            .to_string()
    }
}
fn separated(n: u64) -> String {
    let raw = n.to_string();
    let mut output = String::with_capacity(raw.len() + raw.len() / 3);
    for (index, ch) in raw.chars().enumerate() {
        if index > 0 && (raw.len() - index).is_multiple_of(3) {
            output.push(',');
        }
        output.push(ch);
    }
    output
}
fn format_time(snapshot: &UiSnapshot) -> String {
    if snapshot.time_per_tick == 1.0 {
        snapshot.time_ticks.to_string()
    } else {
        scientific(snapshot.time_ticks as f64 * snapshot.time_per_tick)
    }
}
fn save_png(path: &std::path::Path, image: &egui::ColorImage) -> Result<(), String> {
    if let Some(parent) = path.parent().filter(|p| !p.as_os_str().is_empty()) {
        std::fs::create_dir_all(parent).map_err(|e| e.to_string())?;
    }
    let file = std::fs::File::create(path).map_err(|e| e.to_string())?;
    let mut encoder = png::Encoder::new(
        std::io::BufWriter::new(file),
        image.size[0] as u32,
        image.size[1] as u32,
    );
    encoder.set_color(png::ColorType::Rgba);
    encoder.set_depth(png::BitDepth::Eight);
    let mut writer = encoder.write_header().map_err(|e| e.to_string())?;
    let rgba: Vec<u8> = image
        .pixels
        .iter()
        .flat_map(|pixel| pixel.to_srgba_unmultiplied())
        .collect();
    writer.write_image_data(&rgba).map_err(|e| e.to_string())?;
    writer.finish().map_err(|e| e.to_string())
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn camera_roundtrip_and_zoom_keep_anchor() {
        let rect = Rect::from_min_size(pos2(17.0, 22.0), vec2(900.0, 600.0));
        let mut camera = Camera {
            center: [190.0, -44.0],
            scale: 3.2,
            fitted: true,
        };
        let point = [200.0, 57.0];
        let screen = camera.project(point, rect);
        let decoded = camera.unproject(screen, rect);
        assert!((decoded[0] - point[0]).abs() < 1e-4 && (decoded[1] - point[1]).abs() < 1e-4);
        camera.zoom_at(2.5, screen, rect);
        assert!(camera.project(point, rect).distance(screen) < 1e-3);
    }
    #[test]
    fn camera_fit_rejects_invalid_samples() {
        let rect = Rect::from_min_size(Pos2::ZERO, vec2(800.0, 600.0));
        let mut camera = Camera::default();
        camera.fit(
            &[
                UiBody {
                    position: [f64::NAN, 2.0],
                    ..Default::default()
                },
                UiBody {
                    position: [1.0, 9.0],
                    ..Default::default()
                },
            ],
            rect,
        );
        assert_eq!(camera.center, [1.0, 9.0]);
        assert!(camera.scale.is_finite());
    }
    #[test]
    fn canonical_ticks_are_not_rounded_for_display() {
        let snapshot = UiSnapshot {
            time_ticks: 9_007_199_254_740_993,
            ..Default::default()
        };
        assert_eq!(format_time(&snapshot), "9007199254740993");
    }
}
