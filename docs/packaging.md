# App packaging

TeslaCam Telemetry keeps `v1` reserved for a reliable packaged app. These packaging workflows are pre-v1 portable builds so the desktop app can be tested outside a source checkout.

## Build locally on Windows

From the repository root:

```powershell
python -m pip install -e . pyinstaller
./scripts/build_windows.ps1
```

The script creates:

```text
dist/TeslaCamTelemetry-windows-portable.zip
```

Unzip it and run:

```text
TeslaCamTelemetry.exe
```

## Build locally on macOS

From the repository root:

```bash
python -m pip install -e . pyinstaller
./scripts/build_macos.sh
```

The script creates:

```text
dist/TeslaCamTelemetry-macos-portable.zip
```

Unzip it and run:

```text
TeslaCamTelemetry.app
```

The macOS app is currently unsigned. macOS may show a Gatekeeper warning until signing and notarization are added.

## GitHub Actions

The **Windows App** workflow builds the Windows app folder on `windows-latest` and uploads it as a workflow artifact. GitHub downloads artifacts as ZIP files, so the workflow uploads the app folder directly to avoid a ZIP inside another ZIP.

The **macOS App** workflow builds the macOS `.app` bundle on `macos-latest` and uploads it as a workflow artifact. The artifact is for testing the unsigned app bundle before release packaging.

The **Release** workflow runs when a `v*.*.*` tag is pushed. It builds the Python package, Windows portable app, and macOS portable app, then attaches them to the GitHub Release. The app release assets are named like:

```text
TeslaCamTelemetry-v0.4.0-windows-portable.zip
TeslaCamTelemetry-v0.4.0-macos-portable.zip
```

For now, these ZIPs are pre-v1 portable test builds, not the final `v1` app downloads.

## Current packaging expectations

- Python, PySide6, OpenCV, NumPy, and app modules are bundled by PyInstaller.
- FFmpeg is not bundled. The app checks MP4 output support at startup and shows OS-specific FFmpeg install instructions if needed.
- The macOS app is not signed or notarized yet.
