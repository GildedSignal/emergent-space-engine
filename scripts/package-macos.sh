#!/bin/sh
set -eu
PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$PROJECT_DIR"
cargo build --release --locked -p emergent-observatory
APP_DIR="$PROJECT_DIR/artifacts/Emergent Space.app"
mkdir -p "$APP_DIR/Contents/MacOS"
cp "$PROJECT_DIR/target/release/emergent-observatory" "$APP_DIR/Contents/MacOS/emergent-observatory"
cat > "$APP_DIR/Contents/Info.plist" <<'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>CFBundleExecutable</key><string>emergent-observatory</string>
<key>CFBundleIdentifier</key><string>dev.emergentspace.observatory</string>
<key>CFBundleName</key><string>Emergent Space</string>
<key>CFBundlePackageType</key><string>APPL</string>
<key>CFBundleShortVersionString</key><string>0.1.0</string>
<key>CFBundleVersion</key><string>1</string>
<key>NSHighResolutionCapable</key><true/>
<key>NSPrincipalClass</key><string>NSApplication</string>
</dict></plist>
PLIST
printf '%s\n' "$APP_DIR"
