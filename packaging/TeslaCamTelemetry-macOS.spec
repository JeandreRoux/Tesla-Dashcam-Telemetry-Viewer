# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
import tomllib

from PyInstaller.utils.hooks import collect_data_files

block_cipher = None
repo_root = Path(SPECPATH).parent
version = tomllib.loads((repo_root / "pyproject.toml").read_text())["project"]["version"]

# Bundle package data used by the render pipeline, including protobuf files and fonts.
datas = collect_data_files("utils")


a = Analysis(
    [str(repo_root / "desktop_ui.py")],
    pathex=[str(repo_root)],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="TeslaCamTelemetry",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="TeslaCamTelemetry",
)

app = BUNDLE(
    coll,
    name="TeslaCamTelemetry.app",
    icon=None,
    bundle_identifier="com.jeandreroux.teslacamtelemetry",
    info_plist={
        "CFBundleName": "TeslaCam Telemetry",
        "CFBundleDisplayName": "TeslaCam Telemetry",
        "CFBundleShortVersionString": version,
        "CFBundleVersion": version,
        "NSHighResolutionCapable": True,
    },
)
