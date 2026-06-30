import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.data_handler import (
    REQUIRED_TELEMETRY_COLUMNS,
    get_available_video_file,
    telemetry_csv_is_valid,
)


class TestGetAvailableVideoFile(unittest.TestCase):
    def test_returns_front_when_available(self):
        files_info = {
            "front": "front.mp4",
            "back": "back.mp4",
            "left_repeater": "left.mp4",
            "right_repeater": "right.mp4",
        }

        video_file = get_available_video_file(files_info)

        self.assertEqual(video_file, "front.mp4")

    def test_falls_back_to_back_when_front_missing(self):
        files_info = {
            "back": "back.mp4",
            "left_repeater": "left.mp4",
            "right_repeater": "right.mp4",
        }

        video_file = get_available_video_file(files_info)

        self.assertEqual(video_file, "back.mp4")

    def test_prefers_front_when_pillar_camera_is_available(self):
        files_info = {
            "left_pillar": "left_pillar.mp4",
            "front": "front.mp4",
        }

        video_file = get_available_video_file(files_info)

        self.assertEqual(video_file, "front.mp4")

    def test_returns_none_when_no_video_files_exist(self):
        files_info = {
            "data": "telemetry.csv",
        }

        video_file = get_available_video_file(files_info)

        self.assertIsNone(video_file)


class TestTelemetryCsvIsValid(unittest.TestCase):
    def test_valid_csv_headers_return_true(self):
        with TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "telemetry.csv"
            csv_path.write_text(",".join(REQUIRED_TELEMETRY_COLUMNS) + "\n")

            is_valid = telemetry_csv_is_valid(csv_path)

            self.assertTrue(is_valid)

    def test_missing_required_header_returns_false(self):
        with TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "telemetry.csv"
            columns = [
                column
                for column in REQUIRED_TELEMETRY_COLUMNS
                if column != "vehicle_speed_mps"
            ]
            csv_path.write_text(",".join(columns) + "\n")

            is_valid = telemetry_csv_is_valid(csv_path)

            self.assertFalse(is_valid)

    def test_non_csv_warning_text_returns_false(self):
        with TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "telemetry.csv"
            csv_path.write_text("No SEI metadata found. Requirements:\n")

            is_valid = telemetry_csv_is_valid(csv_path)

            self.assertFalse(is_valid)

    def test_missing_csv_file_returns_false(self):
        with TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "missing.csv"

            is_valid = telemetry_csv_is_valid(csv_path)

            self.assertFalse(is_valid)


if __name__ == "__main__":
    unittest.main()
