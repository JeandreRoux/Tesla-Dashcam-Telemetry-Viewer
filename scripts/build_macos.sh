#!/usr/bin/env bash
set -euo pipefail

ARTIFACT_NAME="${1:-TeslaCamTelemetry-macos-portable.zip}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SPEC_FILE="$REPO_ROOT/packaging/TeslaCamTelemetry-macOS.spec"
DIST_DIR="$REPO_ROOT/dist"
BUILD_DIR="$REPO_ROOT/build"
APP_PATH="$DIST_DIR/TeslaCamTelemetry.app"
ZIP_PATH="$DIST_DIR/$ARTIFACT_NAME"
ARTIFACT_DIR="$DIST_DIR/macos-artifact"

cd "$REPO_ROOT"

rm -rf "$BUILD_DIR" "$APP_PATH" "$ZIP_PATH" "$ARTIFACT_DIR"

python -m PyInstaller --noconfirm --clean "$SPEC_FILE"

if [[ ! -d "$APP_PATH" ]]; then
  echo "Expected packaged app was not created: $APP_PATH" >&2
  exit 1
fi

mkdir -p "$DIST_DIR"
ditto -c -k --keepParent "$APP_PATH" "$ZIP_PATH"

if [[ ! -f "$ZIP_PATH" ]]; then
  echo "Expected ZIP artifact was not created: $ZIP_PATH" >&2
  exit 1
fi

mkdir -p "$ARTIFACT_DIR"
cp -R "$APP_PATH" "$ARTIFACT_DIR/"

if [[ ! -d "$ARTIFACT_DIR/TeslaCamTelemetry.app" ]]; then
  echo "Expected workflow artifact app bundle was not staged: $ARTIFACT_DIR/TeslaCamTelemetry.app" >&2
  exit 1
fi

echo "Created $ZIP_PATH"
echo "Staged $ARTIFACT_DIR/TeslaCamTelemetry.app"
