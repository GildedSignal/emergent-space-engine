mod adapter;
mod app;
mod bridge;

use app::{AppOptions, ObservatoryApp};
use eframe::egui;
use std::path::PathBuf;

fn parse_options() -> Result<AppOptions, String> {
    let mut options = AppOptions::default();
    let mut args = std::env::args().skip(1);
    while let Some(arg) = args.next() {
        match arg.as_str() {
            "--screenshot" => {
                options.screenshot = Some(PathBuf::from(
                    args.next().ok_or("--screenshot needs a PNG path")?,
                ))
            }
            "--frames" => {
                options.frames = Some(
                    args.next()
                        .ok_or("--frames needs a number")?
                        .parse()
                        .map_err(|_| "--frames needs a positive integer")?,
                )
            }
            "--save-path" => {
                options.save_path = Some(PathBuf::from(
                    args.next().ok_or("--save-path needs a path")?,
                ))
            }
            "--help" | "-h" => {
                println!("Emergent Space native observatory\n  --screenshot PATH   Capture a native wgpu frame to PNG\n  --frames N          Close after N rendered frames (minimum 10)\n  --save-path PATH    Set the local archive path");
                std::process::exit(0);
            }
            _ => return Err(format!("Unknown argument: {arg}")),
        }
    }
    Ok(options)
}

fn main() -> eframe::Result {
    let options = parse_options().unwrap_or_else(|message| {
        eprintln!("{message}");
        std::process::exit(2);
    });
    let native = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default()
            .with_title("Emergent Space · The observatory")
            .with_inner_size([1440.0, 960.0])
            .with_min_inner_size([980.0, 680.0]),
        renderer: eframe::Renderer::Wgpu,
        vsync: true,
        ..Default::default()
    };
    eframe::run_native(
        "Emergent Space",
        native,
        Box::new(move |cc| {
            Ok(Box::new(ObservatoryApp::new(
                cc,
                Box::new(adapter::EngineBridge::new()),
                options,
            )))
        }),
    )
}
