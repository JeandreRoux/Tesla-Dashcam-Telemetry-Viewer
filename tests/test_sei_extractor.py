import unittest
from unittest.mock import patch

from modules import sei_extractor


class TestBuildCsv(unittest.TestCase):
    def test_returns_empty_string_when_no_rows_exist(self):
        csv_content = sei_extractor.build_csv(["header"], [])

        self.assertEqual(csv_content, "")

    def test_builds_csv_with_headers_and_rows(self):
        csv_content = sei_extractor.build_csv(
            ["speed", "gear"],
            [["10", "D"], ["0", "P"]],
        )

        self.assertEqual(csv_content, "speed,gear\n10,D\n0,P")


class TestMetadataToRow(unittest.TestCase):
    def test_applies_defaults_for_missing_metadata_fields(self):
        headers = [
            "accelerator_pedal_position",
            "autopilot_state",
            "custom_field",
        ]

        with patch(
            "modules.sei_extractor.MessageToDict",
            return_value={"custom_field": "custom"},
        ):
            row = sei_extractor.metadata_to_row(object(), headers)

        self.assertEqual(row, ["0", "NONE", "custom"])


if __name__ == "__main__":
    unittest.main()
