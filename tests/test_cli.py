import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import main
from modules import app_service, layouts


TIMESTAMP = "2026-06-19_23-08-01"
FOUR_CAMERAS = ("front", "back", "left_repeater", "right_repeater")


def touch_camera_files(directory: Path, cameras: tuple[str, ...], timestamp: str = TIMESTAMP) -> None:
    for camera in cameras:
        (directory / f"{timestamp}-{camera}.mp4").write_text("placeholder")


class TestCliMp4Preflight(unittest.TestCase):
    def test_exits_before_scan_when_mp4_codec_is_missing(self):
        with TemporaryDirectory() as temp_input, TemporaryDirectory() as temp_output:
            input_path = Path(temp_input)
            touch_camera_files(input_path, FOUR_CAMERAS)
            argv = [
                "teslacam-telemetry",
                "--input",
                str(input_path),
                "--output",
                temp_output,
            ]

            with patch.object(sys, "argv", argv), patch(
                "modules.app_service.check_mp4_output_support",
                return_value=app_service.CodecCheckResult(
                    is_supported=False,
                    message="MP4 video support is missing.\n\nWindows: winget install ffmpeg",
                ),
            ), patch("modules.app_service.scan_input_folder") as scan_input_folder:
                with self.assertRaises(SystemExit) as raised:
                    main.main()

            self.assertIn("winget install ffmpeg", str(raised.exception))
            scan_input_folder.assert_not_called()

    def test_runs_scan_when_mp4_codec_is_available(self):
        with TemporaryDirectory() as temp_input, TemporaryDirectory() as temp_output:
            input_path = Path(temp_input)
            argv = [
                "teslacam-telemetry",
                "--input",
                str(input_path),
                "--output",
                temp_output,
                "--no-overlay",
            ]
            scan = app_service.ScanResult(
                input_path=input_path,
                layout=layouts.FOUR_CAMERA_DEFAULT,
                camera_set="four-camera",
                clip_group_count=1,
            )

            with patch.object(sys, "argv", argv), patch(
                "modules.app_service.check_mp4_output_support",
                return_value=app_service.CodecCheckResult(is_supported=True),
            ), patch(
                "modules.app_service.scan_input_folder", return_value=scan
            ) as scan_input_folder, patch("modules.app_service.render_video") as render_video:
                main.main()

            scan_input_folder.assert_called_once()
            render_video.assert_called_once()


if __name__ == "__main__":
    unittest.main()
