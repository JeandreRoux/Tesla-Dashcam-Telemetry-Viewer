"""
TeslaCam Telemetry

Processes TeslaCam MP4 files and accompanying CSV telemetry files to
produce a combined multi-camera video with real-time telemetry
overlay (speed, autopilot state, steering, brake/accelerator, blinkers).

Usage:
    python main.py -i <input_dir> -o <output_dir> [--no-overlay] [--mph] [--preview] [--keep-csv]
"""

import argparse
import sys
from pathlib import Path

from modules import app_service


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="TeslaCam Telemetry",
        description="Processes TeslaCam footage and telemetry data to create a multi-camera overlay video with real-time vehicle telemetry information including speed, autopilot state, steering angle, and pedal positions.",
        allow_abbrev=False,
    )

    parser.add_argument("-i", "--input", help="input directory", required=True)
    parser.add_argument("-o", "--output", help="output directory", required=True)
    parser.add_argument(
        "--no-overlay",
        help="disables the telemetry overlay (enabled by default)",
        action="store_true",
    )
    parser.add_argument(
        "--mph", help="sets speed units to MPH (default is KM/H)", action="store_true"
    )
    parser.add_argument(
        "--preview",
        help="enabled render preview while videos are being processed",
        action="store_true",
    )
    parser.add_argument(
        "--keep-csv",
        help="keep generated telemetry csv in input directory",
        action="store_true",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    settings = app_service.build_render_settings(
        no_overlay=args.no_overlay,
        mph=args.mph,
        preview=args.preview,
        keep_csv=args.keep_csv,
    )

    input_path = Path(args.input)
    output_path = Path(args.output)

    scan_result = app_service.scan_input_folder(input_path, settings)
    print(app_service.format_scan_summary(scan_result))
    if scan_result.errors:
        sys.exit("Preflight scan failed.")

    job = app_service.RenderJob(
        input_path=input_path,
        output_path=output_path,
        settings=settings,
    )
    app_service.render_video(job)


if __name__ == "__main__":
    main()
