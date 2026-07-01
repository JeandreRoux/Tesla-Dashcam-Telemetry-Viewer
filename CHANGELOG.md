# Changelog

All notable changes to TeslaCam Telemetry will be documented in this file.

This project follows semantic versioning where practical.

## [Unreleased]

- No unreleased changes yet.

## [0.4.0] - 2026-07-01

### Added

- Desktop app entry point for rendering TeslaCam clips through a simple guided workflow.
- MP4 output preflight check with desktop and CLI guidance when FFmpeg support is missing.
- Windows portable app packaging with a GitHub Actions build artifact.
- Tagged releases now attach the Windows portable app ZIP alongside the Python package files.

### Changed

- README now documents the desktop app workflow and keeps MP4 support guidance concise.
- Desktop UI copy, screenshot, and scan progress behaviour were refined for the pre-v1 app.

### Fixed

- GitHub Actions Windows app artifacts no longer require unzipping a ZIP inside another ZIP.

## [0.2.0] - 2026-06-30

### Added

- Six-camera TeslaCam support for `left_pillar` and `right_pillar` clips.
- Automatic default layout selection for complete four-camera or six-camera clip sets.
- Default six-camera 3x2 grid layout.
- Tests for six-camera layout selection and camera reference preference.

### Changed

- README documents four-camera and six-camera input file sets.
- README documents package update and uninstall commands.

### Fixed

- Mixed or incomplete camera sets now fail with a clear error instead of silently rendering an unexpected layout.

## [0.1.0] - 2026-06-30

### Added

- Python packaging via `pyproject.toml`.
- Installable `teslacam-telemetry` console command.
- GitHub Actions test workflow for Python 3.11 and 3.12.
- Package build validation workflow.
- GitHub Release workflow for version tags.
- TeslaCam Telemetry project branding.

### Fixed

- Bundled font/resource loading so the installed command works outside the repository directory.
- Python support metadata aligned to Python 3.11+ based on pinned dependency compatibility.

[Unreleased]: https://github.com/JeandreRoux/teslacam-telemetry/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/JeandreRoux/teslacam-telemetry/compare/v0.2.0...v0.4.0
[0.2.0]: https://github.com/JeandreRoux/teslacam-telemetry/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/JeandreRoux/teslacam-telemetry/releases/tag/v0.1.0
